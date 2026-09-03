"""Build an event table from pattern detections.

Every *confirmed* pattern becomes one event.  To keep the study honest:

* The signal bar is the later of the breakout bar and the bar at which the
  last swing point of the structure became knowable (``pivot idx + order``),
  because a swing high/low only exists once ``order`` bars have printed after
  it.  Detecting on the full history would otherwise leak the future.
* Entry is the *next bar's open* after the signal bar.
* Outcomes are measured against three baselines: raw, minus the benchmark
  (SPY) over the same window, and minus random-date entries in the same
  stock and direction (which cancels the stock's drift and survivorship).
"""

from __future__ import annotations

import zlib
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.core.geometry import volume_ratio
from algovision.core.types import DetectorConfig, PatternMatch
from algovision.patterns import detect_all

HORIZONS: Tuple[int, ...] = (5, 10, 20, 40, 60)
MAX_HOLD = 60
RANDOM_DRAWS = 20


def _direction(m: PatternMatch) -> int:
    return 1 if m.direction == "bullish" else -1 if m.direction == "bearish" else 0


_STATUS_PENALTY = {"failed": 0.6, "expired": 0.7}


def raw_score(m: PatternMatch) -> float:
    """Score before the status penalty applied by the detectors."""
    return m.score / _STATUS_PENALTY.get(m.status, 1.0)


def structure_complete_idx(m: PatternMatch) -> int:
    """Bar at which the pattern's structure was knowable in real time."""
    last_kp = max((kp.idx for kp in m.key_points), default=m.start_idx)
    return last_kp + int(m.scale or 0)


def align_benchmark(df: pd.DataFrame, bench: Optional[pd.DataFrame]) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    if bench is None:
        return None
    b = bench.reindex(df.index).ffill().bfill()
    return b["Open"].to_numpy(dtype=float), b["Close"].to_numpy(dtype=float)


def simulate_trade(high: np.ndarray, low: np.ndarray, close: np.ndarray, e: int, entry: float, direction: int,
                   target: Optional[float], stop: Optional[float], max_hold: int) -> Dict:
    """Walk forward from entry bar ``e``; exit at target/stop (stop wins ties) or time."""
    n = len(close)
    last = min(n - 1, e + max_hold - 1)
    out: Dict = {"exit_reason": "time", "exit_idx": last, "bars_held": last - e + 1}
    risk = abs(entry - stop) if stop is not None else np.nan
    valid_r = np.isfinite(risk) and risk > 0.003 * entry
    mfe = mae = 0.0
    for j in range(e, last + 1):
        fav = (high[j] - entry) if direction > 0 else (entry - low[j])
        adv = (entry - low[j]) if direction > 0 else (high[j] - entry)
        mfe, mae = max(mfe, fav), max(mae, adv)
        hit_stop = stop is not None and ((direction > 0 and low[j] <= stop) or (direction < 0 and high[j] >= stop))
        hit_tgt = target is not None and ((direction > 0 and high[j] >= target) or (direction < 0 and low[j] <= target))
        if hit_stop:
            out.update(exit_reason="stop", exit_idx=j, bars_held=j - e + 1, exit_price=float(stop))
            break
        if hit_tgt:
            out.update(exit_reason="target", exit_idx=j, bars_held=j - e + 1, exit_price=float(target))
            break
    else:
        out["exit_price"] = float(close[last])
    out["trade_ret"] = direction * (out["exit_price"] / entry - 1.0)
    out["mfe_pct"], out["mae_pct"] = mfe / entry, mae / entry
    if valid_r:
        out["r_multiple"] = direction * (out["exit_price"] - entry) / risk
        out["mfe_r"], out["mae_r"] = mfe / risk, mae / risk
        out["reward_risk"] = abs(target - entry) / risk if target is not None else np.nan
    else:
        out["r_multiple"] = out["mfe_r"] = out["mae_r"] = out["reward_risk"] = np.nan
    return out


def build_events(symbol: str, df: pd.DataFrame, bench: Optional[pd.DataFrame] = None,
                 config: Optional[DetectorConfig] = None, horizons: Sequence[int] = HORIZONS,
                 random_draws: int = RANDOM_DRAWS, max_hold: int = MAX_HOLD, seed: int = 0,
                 matches: Optional[List[PatternMatch]] = None) -> Tuple[List[Dict], List[Dict]]:
    """Return (events, structures).

    ``events``     one row per confirmed pattern with forward outcomes.
    ``structures`` one row per completed structure (any status) - used to ask
                   "given the shape is complete, how often does it confirm?".
    """
    cfg = config or DetectorConfig()
    if matches is None:
        matches = detect_all(df, symbol=symbol, config=cfg)
        # failed / expired matches carry a score penalty (x0.6 / x0.7) that usually pushes
        # them under min_score; for the "does a complete shape confirm?" question we need
        # them back, judged on their pre-penalty score.
        struct_matches = [m for m in detect_all(df, symbol=symbol, config=cfg, min_score=0.0)
                          if raw_score(m) >= cfg.min_score]
    else:
        struct_matches = matches
    n = len(df)
    open_ = df["Open"].to_numpy(dtype=float)
    high = df["High"].to_numpy(dtype=float)
    low = df["Low"].to_numpy(dtype=float)
    close = df["Close"].to_numpy(dtype=float)
    vol = df["Volume"].to_numpy(dtype=float) if "Volume" in df.columns else None
    b = align_benchmark(df, bench)
    rng = np.random.default_rng(seed + (zlib.crc32(symbol.encode()) % 100000))
    dates = df.index
    events: List[Dict] = []
    structures: List[Dict] = []
    hmax = max(horizons)

    for m in struct_matches:
        complete = structure_complete_idx(m)
        if n - 1 - complete >= max_hold:
            structures.append({
                "symbol": symbol, "pattern": m.pattern, "status": m.status, "score": raw_score(m),
                "expected_dir": m.direction, "scale": m.scale,
                "date": str(pd.Timestamp(dates[min(complete, n - 1)]).date()),
            })
    for m in matches:
        d = _direction(m)
        complete = structure_complete_idx(m)
        if m.status != "confirmed" or m.breakout_idx is None or d == 0:
            continue
        signal = max(int(m.breakout_idx), complete)
        e = signal + 1
        if e >= n:
            continue
        entry = open_[e]
        row: Dict = {
            "symbol": symbol, "pattern": m.pattern, "direction": m.direction, "dir": d, "score": m.score,
            "scale": m.scale, "width": m.width, "signal_idx": signal, "entry_idx": e,
            "signal_date": str(pd.Timestamp(dates[signal]).date()), "year": int(pd.Timestamp(dates[signal]).year),
            "delay_bars": signal - int(m.breakout_idx), "entry": float(entry),
            "level": m.level, "target": m.target, "stop": m.stop,
            "breakout_vol_ratio": volume_ratio(vol, int(m.breakout_idx), cfg.volume_lookback),
            "gap_from_level": (entry / m.level - 1.0) * d if m.level else np.nan,
            "complete": bool(e + hmax - 1 < n),
        }
        for h in horizons:
            j = e + h - 1
            if j < n:
                r = close[j] / entry - 1.0
                row[f"ret_{h}"] = d * r
                row[f"xspy_{h}"] = d * (r - (b[1][j] / b[0][e] - 1.0)) if b is not None else np.nan
                # random-date entries in the same stock, same direction, same holding period
                cand = rng.integers(1, n - h + 1, size=random_draws)
                rr = d * (close[cand + h - 1] / open_[cand] - 1.0)
                for k, v in enumerate(rr):
                    row[f"rand_{h}_{k}"] = float(v)
                row[f"xrand_{h}"] = row[f"ret_{h}"] - float(rr.mean())
            else:
                row[f"ret_{h}"] = row[f"xspy_{h}"] = row[f"xrand_{h}"] = np.nan
                for k in range(random_draws):
                    row[f"rand_{h}_{k}"] = np.nan
        row.update(simulate_trade(high, low, close, e, entry, d, m.target, m.stop, max_hold))
        events.append(row)
    return events, structures


LOCAL_WINDOW = 126   # +- half a year of bars around the signal


def add_local_baseline(events: pd.DataFrame, get_frame, horizons: Sequence[int] = HORIZONS,
                       random_draws: int = RANDOM_DRAWS, window: int = LOCAL_WINDOW, seed: int = 1) -> pd.DataFrame:
    """Add ``xloc_h`` / ``loc_h_k`` columns: excess over random entries near the signal.

    Random dates are drawn from the same stock within ``window`` bars before or
    after the entry (excluding the event's own holding window), same direction
    and holding period.  This cancels the *regime* around the signal, not just
    the stock's long-run drift.  ``get_frame(symbol)`` must return the OHLCV
    DataFrame the events were built from.
    """
    ev = events.copy()
    for h in horizons:
        ev[f"xloc_{h}"] = np.nan
        for k in range(random_draws):
            ev[f"loc_{h}_{k}"] = np.nan
    for symbol, idx in ev.groupby("symbol").groups.items():
        df = get_frame(symbol)
        open_ = df["Open"].to_numpy(dtype=float)
        close = df["Close"].to_numpy(dtype=float)
        n = len(df)
        rng = np.random.default_rng(seed + (zlib.crc32(symbol.encode()) % 100000))
        for i in idx:
            e = int(ev.at[i, "entry_idx"])
            d = int(ev.at[i, "dir"])
            for h in horizons:
                if not np.isfinite(ev.at[i, f"ret_{h}"]):
                    continue
                lo, hi = max(1, e - window), min(n - h, e + window)
                cand = np.arange(lo, hi + 1)
                cand = cand[(cand < e - h) | (cand > e + h)]      # do not overlap the event itself
                if len(cand) < 5:
                    continue
                pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                rr = d * (close[pick + h - 1] / open_[pick] - 1.0)
                ev.loc[i, [f"loc_{h}_{k}" for k in range(random_draws)]] = rr
                ev.at[i, f"xloc_{h}"] = ev.at[i, f"ret_{h}"] - float(rr.mean())
    return ev
