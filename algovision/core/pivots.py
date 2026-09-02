"""Swing-point (pivot) detection.

A chartist reads a chart through its swing highs and lows.  Every pattern
detector in this package is expressed as a geometric rule over the sequence
of alternating pivots produced here, which keeps the rules close to how the
patterns are described in trading literature.
"""

from __future__ import annotations

from typing import List, Sequence

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

from algovision.core.types import Pivot


def atr(df: pd.DataFrame, period: int = 14) -> np.ndarray:
    """Average True Range as a numpy array (NaN-free, back-filled)."""
    high = df["High"].to_numpy(dtype=float)
    low = df["Low"].to_numpy(dtype=float)
    close = df["Close"].to_numpy(dtype=float)
    prev_close = np.concatenate([[close[0]], close[:-1]])
    tr = np.maximum(high - low, np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    s = pd.Series(tr).rolling(period, min_periods=1).mean()
    return s.to_numpy(dtype=float)


def _alternate(pivots: List[Pivot]) -> List[Pivot]:
    """Enforce strict high/low alternation, keeping the more extreme of runs."""
    out: List[Pivot] = []
    for p in pivots:
        if out and out[-1].kind == p.kind:
            prev = out[-1]
            better = p if (p.kind > 0 and p.price >= prev.price) or (p.kind < 0 and p.price <= prev.price) else prev
            out[-1] = better
        else:
            out.append(p)
    return out


def find_pivots(
    df: pd.DataFrame,
    order: int = 5,
    min_move_atr: float = 1.0,
    min_move_pct: float = 0.01,
) -> List[Pivot]:
    """Return alternating swing highs/lows.

    Parameters
    ----------
    order:
        A bar is a swing high if its High is the maximum within ``order`` bars
        on each side (and symmetrically for lows).  Larger values yield fewer,
        bigger swings.
    min_move_atr / min_move_pct:
        Swings smaller than ``max(min_move_atr * ATR, min_move_pct * price)``
        are treated as noise and merged away (zig-zag style filtering).
    """
    n = len(df)
    if n < 2 * order + 3:
        return []
    high = df["High"].to_numpy(dtype=float)
    low = df["Low"].to_numpy(dtype=float)

    hi_idx = argrelextrema(high, np.greater_equal, order=order)[0]
    lo_idx = argrelextrema(low, np.less_equal, order=order)[0]

    # argrelextrema with >= can return plateaus; keep the first bar of each plateau run
    def dedupe_runs(idx: np.ndarray, values: np.ndarray) -> List[int]:
        keep: List[int] = []
        for i in idx:
            if keep and i - keep[-1] <= order and values[i] == values[keep[-1]]:
                continue
            keep.append(int(i))
        return keep

    pivots = [Pivot(i, float(high[i]), +1) for i in dedupe_runs(hi_idx, high)]
    pivots += [Pivot(i, float(low[i]), -1) for i in dedupe_runs(lo_idx, low)]
    pivots.sort(key=lambda p: (p.idx, -p.kind))
    # a single wide-range bar can be both a swing high and a swing low; keep the
    # one that continues the alternation with the previous pivot
    cleaned: List[Pivot] = []
    for p in pivots:
        if cleaned and cleaned[-1].idx == p.idx:
            if len(cleaned) >= 2 and cleaned[-2].kind == cleaned[-1].kind:
                cleaned[-1] = p
            continue
        cleaned.append(p)
    pivots = _alternate(cleaned)

    if len(pivots) < 2:
        return pivots

    a = atr(df)
    thr = np.maximum(min_move_atr * a, min_move_pct * df["Close"].to_numpy(dtype=float))

    # zig-zag filtering: repeatedly remove the end pivot of the smallest sub-threshold swing
    changed = True
    while changed and len(pivots) >= 2:
        changed = False
        smallest_i = -1
        smallest_ratio = 1.0
        for i in range(1, len(pivots)):
            move = abs(pivots[i].price - pivots[i - 1].price)
            t = thr[pivots[i].idx]
            ratio = move / t if t > 0 else 1.0
            if ratio < 1.0 and ratio < smallest_ratio:
                smallest_ratio = ratio
                smallest_i = i
        if smallest_i > 0:
            del pivots[smallest_i]
            pivots = _alternate(pivots)
            changed = True
    return pivots


def pivots_to_arrays(pivots: Sequence[Pivot]):
    idx = np.array([p.idx for p in pivots], dtype=int)
    price = np.array([p.price for p in pivots], dtype=float)
    kind = np.array([p.kind for p in pivots], dtype=int)
    return idx, price, kind
