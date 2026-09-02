"""OHLCV data access.

Primary source is Yahoo Finance's public chart endpoint (queried directly
with ``requests`` so it works behind corporate proxies); ``yfinance`` is used
as a fallback when it is installed.  Downloads are cached on disk as CSV so
repeated scans are fast and offline-friendly.  A directory of your own CSV
files can be used instead of any network source.
"""

from __future__ import annotations

import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

COLUMNS = ["Open", "High", "Low", "Close", "Volume"]
_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
       "Accept": "application/json"}
_DEFAULT_CACHE = Path(os.environ.get("ALGOVISION_CACHE", Path.home() / ".algovision" / "cache"))


def normalise_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce any reasonably named OHLCV frame into the canonical layout."""
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = [c[0] for c in df.columns]
    ren = {}
    for c in df.columns:
        lc = str(c).strip().lower()
        for want in COLUMNS:
            if lc == want.lower() or lc.replace(" ", "") == want.lower():
                ren[c] = want
        if lc in ("adj close", "adj_close", "adjclose"):
            ren.setdefault(c, "Adj Close")
        if lc in ("date", "datetime", "timestamp", "time"):
            ren[c] = "Date"
    df = df.rename(columns=ren)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], utc=False, errors="coerce")
        df = df.set_index("Date")
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index, errors="coerce")
    if getattr(df.index, "tz", None) is not None:
        df.index = df.index.tz_localize(None)
    missing = [c for c in ("Open", "High", "Low", "Close") if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns {missing}; have {list(df.columns)}")
    if "Volume" not in df.columns:
        df["Volume"] = np.nan
    out = df[COLUMNS].astype(float)
    out = out[~out.index.isna()].sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out = out.dropna(subset=["Open", "High", "Low", "Close"])
    out.index.name = "Date"
    return out


# --------------------------------------------------------------------------
# Yahoo chart endpoint
# --------------------------------------------------------------------------
def fetch_yahoo_chart(symbol: str, period: str = "2y", interval: str = "1d", timeout: int = 30,
                      retries: int = 3) -> pd.DataFrame:
    import requests

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"range": period, "interval": interval, "events": "div,splits", "includeAdjustedClose": "true"}
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=_UA, timeout=timeout)
            if r.status_code == 429:
                time.sleep(2.0 * (attempt + 1))
                continue
            r.raise_for_status()
            payload = r.json()["chart"]
            if payload.get("error"):
                raise RuntimeError(str(payload["error"]))
            res = payload["result"][0]
            ts = res.get("timestamp")
            if not ts:
                raise RuntimeError("empty response")
            q = res["indicators"]["quote"][0]
            df = pd.DataFrame({
                "Open": q["open"], "High": q["high"], "Low": q["low"], "Close": q["close"], "Volume": q["volume"],
            }, index=pd.to_datetime(ts, unit="s", utc=True).tz_convert(None))
            if interval.endswith("d") or interval.endswith("wk") or interval.endswith("mo"):
                df.index = df.index.normalize()
            adj = res["indicators"].get("adjclose")
            if adj and adj[0].get("adjclose"):
                # adjust OHLC for splits/dividends using the adjusted-close ratio
                ratio = np.asarray(adj[0]["adjclose"], dtype=float) / df["Close"].to_numpy(dtype=float)
                ratio = np.where(np.isfinite(ratio), ratio, 1.0)
                for c in ("Open", "High", "Low", "Close"):
                    df[c] = df[c].to_numpy(dtype=float) * ratio
            return normalise_ohlcv(df)
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"Yahoo chart request failed for {symbol}: {last_exc}")


def fetch_yfinance(symbol: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    import yfinance as yf  # optional dependency

    df = yf.download(symbol, period=period, interval=interval, progress=False, auto_adjust=True, threads=False)
    if df is None or len(df) == 0:
        raise RuntimeError(f"yfinance returned no data for {symbol}")
    return normalise_ohlcv(df)


# --------------------------------------------------------------------------
# Provider with disk cache
# --------------------------------------------------------------------------
class DataProvider:
    """Fetch + cache OHLCV frames.

    Parameters
    ----------
    cache_dir:
        Where CSV caches live.  ``None`` disables caching.
    csv_dir:
        Directory of ``SYMBOL.csv`` files used instead of the network.
    max_age_hours:
        Cached frames older than this are refreshed (when online).
    offline:
        Never touch the network; raise if a symbol is not cached.
    """

    def __init__(self, cache_dir: Optional[Path] = _DEFAULT_CACHE, csv_dir: Optional[Path] = None,
                 max_age_hours: float = 12.0, offline: bool = False, workers: int = 4,
                 sources: Iterable[str] = ("yahoo", "yfinance")):
        self.cache_dir = Path(cache_dir) if cache_dir else None
        self.csv_dir = Path(csv_dir) if csv_dir else None
        self.max_age = max_age_hours * 3600.0
        self.offline = offline
        self.workers = workers
        self.sources = tuple(sources)
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    # -- cache helpers --------------------------------------------------
    def _cache_path(self, symbol: str, period: str, interval: str) -> Optional[Path]:
        if not self.cache_dir:
            return None
        return self.cache_dir / f"{symbol}_{period}_{interval}.csv"

    def _read_cache(self, path: Optional[Path], ignore_age: bool = False) -> Optional[pd.DataFrame]:
        if path is None or not path.exists():
            return None
        if not ignore_age and (time.time() - path.stat().st_mtime) > self.max_age:
            return None
        try:
            return normalise_ohlcv(pd.read_csv(path))
        except Exception as exc:  # corrupt cache -> ignore
            log.warning("ignoring corrupt cache %s (%s)", path, exc)
            return None

    # -- public API -----------------------------------------------------
    def get(self, symbol: str, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
        symbol = symbol.upper().replace(".", "-")
        if self.csv_dir is not None:
            p = self.csv_dir / f"{symbol}.csv"
            if not p.exists():
                raise FileNotFoundError(p)
            return normalise_ohlcv(pd.read_csv(p))

        path = self._cache_path(symbol, period, interval)
        cached = self._read_cache(path, ignore_age=self.offline)
        if cached is not None:
            return cached
        if self.offline:
            raise RuntimeError(f"{symbol}: not in cache and provider is offline")

        errors: List[str] = []
        for src in self.sources:
            try:
                if src == "yahoo":
                    df = fetch_yahoo_chart(symbol, period, interval)
                elif src == "yfinance":
                    df = fetch_yfinance(symbol, period, interval)
                else:
                    continue
                if path is not None:
                    df.to_csv(path)
                return df
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{src}: {exc}")
        stale = self._read_cache(path, ignore_age=True)
        if stale is not None:
            log.warning("%s: using stale cache (%s)", symbol, "; ".join(errors))
            return stale
        raise RuntimeError(f"{symbol}: all sources failed ({'; '.join(errors)})")

    def get_many(self, symbols: Iterable[str], period: str = "2y", interval: str = "1d",
                 progress: Optional[Callable[[str, bool], None]] = None) -> Dict[str, pd.DataFrame]:
        """Fetch several symbols concurrently.  Failures are logged and skipped."""
        symbols = list(symbols)
        out: Dict[str, pd.DataFrame] = {}
        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as ex:
            futs = {ex.submit(self.get, s, period, interval): s for s in symbols}
            for fut in as_completed(futs):
                s = futs[fut]
                try:
                    out[s] = fut.result()
                    if progress:
                        progress(s, True)
                except Exception as exc:  # noqa: BLE001
                    log.warning("%s: %s", s, exc)
                    if progress:
                        progress(s, False)
        return out
