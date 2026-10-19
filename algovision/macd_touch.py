"""MACD "pre-touch" forecast: will the daily MACD line reach (touch or cross) its signal line at the next close,
while the two lines are still apart today?

Definition and calibration come from the AdaptiveMACD project (``OrenRachamim/AdaptiveMACD``, ``docs/macd_touch_forecast.md``):

* the lines "touch" when ``signal - MACD <= 5% x |signal|``;
* the forecast is only meaningful while MACD is below the signal line and the lines are apart (``hist < -5% x |signal|``);
  otherwise the status is ``touching`` or ``above_signal``;
* MACD is linear in tomorrow's close, so the close at which the lines touch (``touch_price``) and cross (``cross_price``)
  are exact; the probability maps the move the touch needs (in units of the 60-day daily volatility) through a
  calibration table fitted on 2.2M US stock-days; at >= 70% about 82% of the flagged stocks touched or crossed the next
  day in 2015-2026 out of sample (79-83% every year).

It predicts the movement of the indicator lines, not the price direction, and nothing here has been tested against
returns, so the daily report shows it as context only (a cell per listed stock), never as a filter or a rank.

The inputs are split-adjusted but **not** dividend-adjusted closes (yfinance ``auto_adjust=False``). The report's price
cache is dividend-adjusted, and the difference moves the MACD of dividend payers enough to flip a status, so
:class:`MacdTouch` fetches the raw closes of the listed names from the Yahoo chart endpoint (cached per day) and only
falls back to the adjusted cache, marked ``~`` in the cell, when that fetch fails.
"""
from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

FAST, SLOW, SIGNAL = 12, 26, 9
A_F, A_S, A_G = 2 / (FAST + 1), 2 / (SLOW + 1), 2 / (SIGNAL + 1)
TOLERANCE = 0.05   # lines "touch" when signal - MACD <= 5% of |signal|
VOL_WINDOW = 60    # daily volatility: std of daily % returns over 60 days
MIN_BARS = 200
ALERT = 0.70       # the alert threshold on the probability

# Calibration z -> probability of touching/crossing at the next close (fitted on 2.2M US stock-days)
_Z = [-3, -2.5, -2, -1.5, -1.4, -1.3, -1.2, -1.1, -1, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1,
      0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 2, 2.5, 3]
_P = [0.944, 0.944, 0.944, 0.915, 0.906, 0.897, 0.887, 0.874, 0.856, 0.839, 0.814, 0.788, 0.755, 0.726,
      0.693, 0.649, 0.599, 0.562, 0.505, 0.431, 0.392, 0.339, 0.297, 0.260, 0.224, 0.194, 0.165, 0.140,
      0.121, 0.106, 0.087, 0.080, 0.067, 0.055, 0.025, 0.012, 0.006]


def macd_touch_forecast(close: pd.Series, tolerance: float = TOLERANCE) -> dict:
    """Forecast for the next daily close from daily closes up to today (oldest first)."""
    close = close.dropna().astype(float)
    if len(close) < MIN_BARS:
        return {"status": "insufficient_data"}
    ef = close.ewm(span=FAST, adjust=False).mean()
    es = close.ewm(span=SLOW, adjust=False).mean()
    macd = ef - es
    signal = macd.ewm(span=SIGNAL, adjust=False).mean()
    m, s, e_f, e_s, c = (float(x.iloc[-1]) for x in (macd, signal, ef, es, close))
    hist = m - s
    eps = tolerance * abs(s)
    gap_pct = -hist / abs(s) * 100 if s else float("nan")
    # MACD is linear in tomorrow's close, so these thresholds are exact
    cross_price = (s - (1 - A_F) * e_f + (1 - A_S) * e_s) / (A_F - A_S)
    touch_price = cross_price - eps / ((1 - A_G) * (A_F - A_S))
    base = {"date": close.index[-1], "close": round(c, 4), "macd": round(m, 6), "signal": round(s, 6),
            "hist": round(hist, 6), "gap_pct_of_signal": round(gap_pct, 2),
            "touch_price": round(touch_price, 4), "cross_price": round(cross_price, 4)}
    if hist >= 0:
        return {**base, "status": "above_signal"}   # already crossed
    if hist >= -eps:
        return {**base, "status": "touching"}       # already touching today
    vol = float(close.pct_change().rolling(VOL_WINDOW).std().iloc[-1] * 100)
    required = (touch_price / c - 1) * 100
    z = required / vol if vol else float("nan")
    prob = float(np.interp(z, _Z, _P)) if np.isfinite(z) else float("nan")
    return {**base, "status": "apart",
            "required_change_pct": round(required, 2),  # negative = touch happens even on a drop this size
            "daily_vol_pct": round(vol, 2), "z": round(z, 3) if np.isfinite(z) else z,
            "touch_prob": round(prob, 3) if np.isfinite(prob) else prob, "signal_70": bool(np.isfinite(prob) and prob >= ALERT)}


# ----------------------------------------------------------------------------
# raw (dividend-unadjusted) closes
# ----------------------------------------------------------------------------
_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
       "Accept": "application/json,text/plain,*/*"}


def fetch_raw_close(symbol: str, period: str = "2y", timeout: int = 30, retries: int = 3) -> pd.Series:
    """Daily closes, split-adjusted but not dividend-adjusted (the ``close`` of the Yahoo chart endpoint, which is
    what yfinance returns as ``Close`` with ``auto_adjust=False``)."""
    import requests

    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol.upper().replace('.', '-')}"
    params = {"range": period, "interval": "1d", "events": "div,splits"}
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
            idx = pd.to_datetime(ts, unit="s", utc=True).tz_convert(None).normalize()
            s = pd.Series(res["indicators"]["quote"][0]["close"], index=idx, dtype=float, name="Close")
            s = s[~s.index.duplicated(keep="last")].dropna().sort_index()
            s.index.name = "Date"
            return s
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"raw close request failed for {symbol}: {last_exc}")


class MacdTouch:
    """Per-stock forecasts for the daily report, fetched on first use and cached on disk per day.

    ``get(symbol)`` returns the forecast dict with a ``source`` key: ``raw`` (dividend-unadjusted closes, the inputs the
    calibration was fitted on) or ``adjusted`` (the report's dividend-adjusted cache, used only when the raw fetch failed
    or the report runs offline)."""

    def __init__(self, frames: Dict[str, pd.DataFrame], cache_dir: Optional[Path] = None, offline: bool = False):
        self.frames = frames
        self.cache_dir = Path(cache_dir) / "macd_raw" if cache_dir else None
        self.offline = offline
        self._memo: Dict[str, dict] = {}
        self._lock = threading.Lock()

    def _last_bar(self, symbol: str) -> Optional[pd.Timestamp]:
        df = self.frames.get(symbol)
        return pd.Timestamp(df.index[-1]) if df is not None and len(df) else None

    def _raw(self, symbol: str) -> Optional[pd.Series]:
        want = self._last_bar(symbol)
        path = self.cache_dir / f"{symbol}.csv" if self.cache_dir else None
        if path is not None and path.exists():
            try:
                s = pd.read_csv(path, index_col=0, parse_dates=True)["Close"].astype(float)
                if want is None or (len(s) and pd.Timestamp(s.index[-1]) >= want):
                    return s
            except Exception:  # noqa: BLE001
                pass
        if self.offline:
            return None
        try:
            s = fetch_raw_close(symbol)
        except Exception as exc:  # noqa: BLE001
            log.warning("%s: raw closes unavailable (%s)", symbol, exc)
            return None
        if want is not None and len(s) and pd.Timestamp(s.index[-1]) < want:
            log.warning("%s: raw closes end %s, before the cached %s", symbol, s.index[-1].date(), want.date())
        if path is not None:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                s.to_frame().to_csv(path)
            except Exception:  # noqa: BLE001
                pass
        return s

    def get(self, symbol: str) -> dict:
        with self._lock:
            if symbol in self._memo:
                return self._memo[symbol]
        raw = self._raw(symbol)
        want = self._last_bar(symbol)
        if raw is not None and len(raw) and want is not None:
            raw = raw[:want]           # never look past the report's last bar
        if raw is not None and len(raw) >= MIN_BARS:
            fc = {**macd_touch_forecast(raw), "source": "raw"}
        else:
            df = self.frames.get(symbol)
            fc = {**macd_touch_forecast(df["Close"]), "source": "adjusted"} if df is not None else {"status": "insufficient_data", "source": "none"}
        with self._lock:
            self._memo[symbol] = fc
        return fc

    def cell(self, symbol: str, lang: str = "en") -> str:
        return macd_cell(self.get(symbol), lang)


def macd_cell(fc: Optional[dict], lang: str = "en") -> str:
    """One table cell: probability, the close at which the lines touch and the move it needs, today's gap; bold at >= 70%.
    ``~`` marks a forecast computed on the dividend-adjusted cache instead of raw closes."""
    if not fc or fc.get("status") in (None, "insufficient_data"):
        return ""
    approx = "~" if fc.get("source") == "adjusted" else ""
    st = fc["status"]
    if st == "above_signal":
        return approx + ("מעל הסיגנל" if lang == "he" else "above signal")
    if st == "touching":
        return approx + ("נוגעים" if lang == "he" else "touching")
    p = fc.get("touch_prob")
    if p is None or not np.isfinite(p):
        return ""
    prob = f"{p * 100:.0f}%"
    if fc.get("signal_70"):
        prob = f"**{prob}**"
    if lang == "he":
        txt = f"{approx}{prob} · נגיעה מ-{fc['touch_price']:.2f} ({fc['required_change_pct']:+.1f}%) · פער {fc['gap_pct_of_signal']:.1f}%"
    else:
        txt = f"{approx}{prob} · touch >= {fc['touch_price']:.2f} ({fc['required_change_pct']:+.1f}%) · gap {fc['gap_pct_of_signal']:.1f}%"
    return txt


def macd_note(lang: str = "en") -> str:
    if lang == "he":
        return ("*MACD נגיעה צפויה*: האם קו ה-MACD היומי (12/26) יגיע לקו הסיגנל (9) בסגירה הבאה, בעוד הקווים עדיין מופרדים היום (פער מעל 5% "
                "מ-|סיגנל|)? התא מציג את ההסתברות, את הסגירה שמעליה הקווים נוגעים מחר ואת התזוזה הנדרשת מהסגירה האחרונה (שלילי = נוגעים גם "
                "בירידה בגודל הזה), ואת הפער של היום; מודגש כשההסתברות 70% ומעלה; \"נוגעים\" / \"מעל הסיגנל\" כשאין תחזית. הכיול מפרויקט "
                "AdaptiveMACD (הותאם על 2.2 מיליון ימי-מניה בארה\"ב; מחוץ למדגם 2015-2026, ב-70%+ כ-82% מהמניות שסומנו נגעו או חצו למחרת). "
                "זו תחזית לתנועת קווי האינדיקטור, לא לכיוון המחיר, ואין לה קשר שנבדק לתשואות כאן: הקשר, לא מסנן ולא דירוג. מחושב על סגירות "
                "מותאמות-פיצול ולא מותאמות-דיבידנד שנמשכות לצורך זה (\"~\" מסמן שם שחושב מהמטמון המותאם לדיבידנד בלבד).")
    return ("*MACD pre-touch*: will the daily MACD line (12/26) reach its signal line (9) at the next close, while the lines are still apart "
            "today (gap above 5% of |signal|)? The cell shows the probability, the close above which the lines touch tomorrow and the move it "
            "needs from the last close (negative = they touch even on a drop that size), and today's gap; bold when the probability is 70% or "
            "more; \"touching\" / \"above signal\" when there is nothing to forecast. Calibration from the AdaptiveMACD project (fitted on 2.2M US "
            "stock-days; 2015-2026 out of sample, at >= 70% about 82% of the flagged stocks touched or crossed the next day). It predicts the "
            "movement of the indicator lines, not the price direction, and has no tested link to returns here: context, not a filter or a rank. "
            "Computed on split-adjusted, dividend-unadjusted closes fetched for this purpose (a `~` marks a name computed from the "
            "dividend-adjusted cache only).")
