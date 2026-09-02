"""Small geometric / statistical helpers shared by the detectors."""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import numpy as np
import pandas as pd


def fit_line(xs: Sequence[float], ys: Sequence[float]) -> Tuple[float, float, float]:
    """Least-squares line.  Returns (slope, intercept, max_abs_residual)."""
    x = np.asarray(xs, dtype=float)
    y = np.asarray(ys, dtype=float)
    if len(x) < 2:
        return 0.0, float(y[0]) if len(y) else 0.0, 0.0
    if len(x) == 2:
        slope = (y[1] - y[0]) / (x[1] - x[0]) if x[1] != x[0] else 0.0
        return float(slope), float(y[0] - slope * x[0]), 0.0
    A = np.vstack([x, np.ones_like(x)]).T
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intercept = sol
    resid = y - (slope * x + intercept)
    return float(slope), float(intercept), float(np.max(np.abs(resid)))


def r_squared(y: np.ndarray, y_hat: np.ndarray) -> float:
    y = np.asarray(y, dtype=float)
    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot <= 0:
        return 0.0
    return max(0.0, 1.0 - ss_res / ss_tot)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return float(max(lo, min(hi, x)))


def tolerance_score(value: float, tol: float) -> float:
    """1.0 when value == 0, linearly down to 0.0 at value == tol."""
    if tol <= 0:
        return 0.0
    return clamp(1.0 - abs(value) / tol)


def ramp_score(value: float, lo: float, hi: float) -> float:
    """0.0 at ``lo`` rising linearly to 1.0 at ``hi``."""
    if hi <= lo:
        return 1.0 if value >= hi else 0.0
    return clamp((value - lo) / (hi - lo))


def prior_trend(close: np.ndarray, at_idx: int, lookback: int) -> float:
    """Fractional price change over ``lookback`` bars ending at ``at_idx``.

    Positive == the market rose into the pattern.
    """
    j = max(0, at_idx - lookback)
    if at_idx <= j or close[j] <= 0:
        return 0.0
    return float(close[at_idx] / close[j] - 1.0)


def volume_ratio(volume: Optional[np.ndarray], idx: int, lookback: int = 20) -> Optional[float]:
    """Volume at ``idx`` divided by the average of the preceding ``lookback`` bars."""
    if volume is None or len(volume) == 0 or idx <= 0:
        return None
    j = max(0, idx - lookback)
    base = volume[j:idx]
    base = base[np.isfinite(base) & (base > 0)]
    if len(base) == 0 or not np.isfinite(volume[idx]) or volume[idx] <= 0:
        return None
    return float(volume[idx] / base.mean())


def volume_trend(volume: Optional[np.ndarray], start: int, end: int) -> Optional[float]:
    """Slope sign of volume over a window as (second-half mean / first-half mean) - 1."""
    if volume is None or end - start < 4:
        return None
    seg = volume[start:end + 1]
    seg = np.where(np.isfinite(seg), seg, 0.0)
    h = len(seg) // 2
    a, b = seg[:h].mean(), seg[h:].mean()
    if a <= 0:
        return None
    return float(b / a - 1.0)


def first_cross(
    close: np.ndarray,
    start: int,
    level_fn,
    direction: int,
    confirm_pct: float = 0.002,
    stop: Optional[int] = None,
) -> Optional[int]:
    """First bar index >= ``start`` where close crosses the (possibly sloping) level.

    ``level_fn(i)`` returns the level at bar ``i``; ``direction`` +1 looks for a
    close above the level, -1 for a close below.
    """
    n = len(close) if stop is None else min(len(close), stop)
    for i in range(start, n):
        lvl = level_fn(i)
        if direction > 0 and close[i] > lvl * (1 + confirm_pct):
            return i
        if direction < 0 and close[i] < lvl * (1 - confirm_pct):
            return i
    return None


def forward_outcome(
    df: pd.DataFrame,
    idx: int,
    direction: int,
    target: Optional[float],
    stop: Optional[float],
    horizons: Sequence[int] = (5, 10, 20, 40),
) -> dict:
    """What happened after bar ``idx``: forward returns, target/stop hits, excursions."""
    close = df["Close"].to_numpy(dtype=float)
    high = df["High"].to_numpy(dtype=float)
    low = df["Low"].to_numpy(dtype=float)
    n = len(close)
    out: dict = {}
    base = close[idx]
    for h in horizons:
        j = idx + h
        out[f"ret_{h}"] = float(close[j] / base - 1.0) if j < n else None
    horizon = min(n - 1, idx + max(horizons))
    if horizon > idx:
        fh = high[idx + 1:horizon + 1]
        fl = low[idx + 1:horizon + 1]
        if direction >= 0:
            out["max_favorable"] = float(fh.max() / base - 1.0)
            out["max_adverse"] = float(fl.min() / base - 1.0)
        else:
            out["max_favorable"] = float(base / fl.min() - 1.0)
            out["max_adverse"] = float(base / fh.max() - 1.0)
        if target is not None:
            hit = (fh >= target) if direction >= 0 else (fl <= target)
            out["target_hit"] = bool(hit.any())
            out["bars_to_target"] = int(np.argmax(hit) + 1) if hit.any() else None
        if stop is not None:
            stopped = (fl <= stop) if direction >= 0 else (fh >= stop)
            out["stop_hit"] = bool(stopped.any())
    out["bars_available"] = int(n - 1 - idx)
    return out
