"""Synthetic OHLCV generators that draw textbook chart patterns.

Used by the test-suite and the ``demo`` CLI command so the detectors can be
exercised without network access.  Each generator returns a DataFrame with a
business-day index and a ``meta`` dict describing where the pattern sits.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


def _to_ohlcv(path: np.ndarray, noise: float, seed: int, start: str = "2024-01-01",
              volume_profile: Optional[np.ndarray] = None) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = len(path)
    close = path * (1 + rng.normal(0, noise, n))
    open_ = np.concatenate([[close[0]], close[:-1]]) * (1 + rng.normal(0, noise / 2, n))
    spread = np.abs(rng.normal(0, noise, n)) * close + 0.002 * close
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread
    vol = 1_000_000 * (1 + np.abs(rng.normal(0, 0.3, n)))
    if volume_profile is not None:
        vol = vol * volume_profile
    idx = pd.bdate_range(start, periods=n)
    return pd.DataFrame({"Open": open_, "High": high, "Low": low, "Close": close, "Volume": vol}, index=idx)


def _segments(points: Sequence[Tuple[int, float]]) -> np.ndarray:
    """Piece-wise linear path through (bar, price) anchor points."""
    xs = np.array([p[0] for p in points], dtype=float)
    ys = np.array([p[1] for p in points], dtype=float)
    x = np.arange(int(xs[-1]) + 1)
    return np.interp(x, xs, ys)


def _smooth(path: np.ndarray, win: int = 3) -> np.ndarray:
    if win <= 1:
        return path
    k = np.ones(win) / win
    padded = np.concatenate([np.full(win // 2, path[0]), path, np.full(win - 1 - win // 2, path[-1])])
    return np.convolve(padded, k, mode="valid")


def head_and_shoulders(inverse: bool = False, noise: float = 0.004, seed: int = 1,
                       with_breakout: bool = True) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    up = 1 if not inverse else -1
    pts = [(0, base * (1 - 0.18 * up)),          # prior trend start
           (40, base),                            # into pattern
           (55, base * (1 + 0.06 * up)),          # left shoulder
           (68, base * (1 + 0.005 * up)),         # trough 1
           (85, base * (1 + 0.14 * up)),          # head
           (102, base * (1 + 0.01 * up)),         # trough 2
           (116, base * (1 + 0.065 * up))]        # right shoulder
    if with_breakout:
        pts += [(130, base * (1 - 0.02 * up)),     # neckline break
                (150, base * (1 - 0.12 * up)), (170, base * (1 - 0.10 * up))]
    else:
        pts += [(124, base * (1 + 0.025 * up)), (130, base * (1 + 0.04 * up))]
    path = _smooth(_segments(pts), 3)
    vol = np.ones(len(path))
    vol[126:134] = 2.2   # breakout volume
    df = _to_ohlcv(path, noise, seed, volume_profile=vol)
    return df, {"pattern": "Inverse Head and Shoulders" if inverse else "Head and Shoulders",
                "start": 55, "end": 116, "breakout": 128 if with_breakout else None}


def double_top(bottom: bool = False, noise: float = 0.004, seed: int = 2,
               with_breakout: bool = True) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    up = -1 if bottom else 1
    pts = [(0, base * (1 - 0.20 * up)), (40, base * (1 + 0.10 * up)), (55, base * (1 + 0.02 * up)),
           (72, base * (1 + 0.102 * up))]
    if with_breakout:
        pts += [(86, base * (1 + 0.0 * up)), (110, base * (1 - 0.10 * up)), (125, base * (1 - 0.08 * up))]
    else:
        pts += [(84, base * (1 + 0.04 * up)), (92, base * (1 + 0.07 * up)), (100, base * (1 + 0.05 * up))]
    path = _smooth(_segments(pts), 3)
    df = _to_ohlcv(path, noise, seed)
    return df, {"pattern": "Double Bottom" if bottom else "Double Top", "start": 40, "end": 72,
                "breakout": 90 if with_breakout else None}


def cup_and_handle(noise: float = 0.003, seed: int = 3, with_breakout: bool = True,
                   cup_len: int = 90, depth: float = 0.25) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    pre = _segments([(0, base * 0.8), (30, base)])
    x = np.linspace(-1, 1, cup_len)
    cup = base * (1 - depth * (1 - x ** 2))            # parabola, rims at ``base``
    handle_len = 18
    handle = _segments([(0, base), (8, base * 0.93), (handle_len - 1, base * 0.985)])
    parts = [pre, cup[1:], handle[1:]]
    if with_breakout:
        parts.append(_segments([(0, base * 0.985), (3, base * 1.03), (25, base * 1.18)])[1:])
    else:
        parts.append(_segments([(0, base * 0.985), (4, base * 0.99)])[1:])
    path = _smooth(np.concatenate(parts), 3)
    vol = np.ones(len(path))
    if with_breakout:
        b = len(pre) + cup_len + handle_len - 3
        vol[b:b + 5] = 2.0
    df = _to_ohlcv(path, noise, seed, volume_profile=vol)
    return df, {"pattern": "Cup and Handle", "start": 30, "end": 30 + cup_len + handle_len,
                "breakout": 30 + cup_len + handle_len + 1 if with_breakout else None}


def triangle(kind: str = "ascending", noise: float = 0.003, seed: int = 4,
             with_breakout: bool = True) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    n_sw = 6
    top_start, top_end = base * 1.10, base * 1.10
    bot_start, bot_end = base * 0.90, base * 1.06
    if kind == "descending":
        top_start, top_end = base * 1.10, base * 0.94
        bot_start, bot_end = base * 0.90, base * 0.90
    elif kind == "symmetrical":
        top_start, top_end = base * 1.10, base * 1.02
        bot_start, bot_end = base * 0.90, base * 0.98
    pts: List[Tuple[int, float]] = [(0, base * 0.85), (30, top_start)]
    x = 30
    for i in range(n_sw):
        frac = (i + 1) / n_sw
        x += 12
        if i % 2 == 0:
            pts.append((x, bot_start + (bot_end - bot_start) * frac))
        else:
            pts.append((x, top_start + (top_end - top_start) * frac))
    if with_breakout:
        bull = kind in ("ascending", "symmetrical")
        lvl = top_end if bull else bot_end
        pts += [(x + 6, lvl * (1.04 if bull else 0.96)), (x + 30, lvl * (1.18 if bull else 0.84))]
    path = _smooth(_segments(pts), 3)
    df = _to_ohlcv(path, noise, seed)
    name = {"ascending": "Ascending Triangle", "descending": "Descending Triangle",
            "symmetrical": "Symmetrical Triangle"}[kind]
    return df, {"pattern": name, "start": 30, "end": x, "breakout": x + 4 if with_breakout else None}


def wedge(kind: str = "falling", noise: float = 0.003, seed: int = 5,
          with_breakout: bool = True) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    n_sw = 6
    if kind == "falling":
        top_start, top_end = base * 1.10, base * 0.92
        bot_start, bot_end = base * 0.96, base * 0.885
        pre = base * 1.25
    else:
        top_start, top_end = base * 1.04, base * 1.115
        bot_start, bot_end = base * 0.90, base * 1.08
        pre = base * 0.75
    pts: List[Tuple[int, float]] = [(0, pre), (30, top_start)]
    x = 30
    for i in range(n_sw):
        frac = (i + 1) / n_sw
        x += 12
        if i % 2 == 0:
            pts.append((x, bot_start + (bot_end - bot_start) * frac))
        else:
            pts.append((x, top_start + (top_end - top_start) * frac))
    if with_breakout:
        bull = kind == "falling"
        lvl = top_end if bull else bot_end
        pts += [(x + 6, lvl * (1.05 if bull else 0.95)), (x + 30, lvl * (1.20 if bull else 0.82))]
    path = _smooth(_segments(pts), 3)
    df = _to_ohlcv(path, noise, seed)
    return df, {"pattern": "Falling Wedge" if kind == "falling" else "Rising Wedge",
                "start": 30, "end": x, "breakout": x + 4 if with_breakout else None}


def flag(bearish: bool = False, noise: float = 0.003, seed: int = 6,
         with_breakout: bool = True) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    up = -1 if bearish else 1
    pts: List[Tuple[int, float]] = [(0, base), (30, base * (1 + 0.01 * up)), (40, base * (1 + 0.16 * up))]
    x = 40
    top = base * (1 + 0.16 * up)
    for i in range(6):   # tight down-sloping channel
        x += 2
        drift = -0.006 * up * (i + 1)
        pts.append((x, top * (1 + drift + (0.012 * up if i % 2 else -0.012 * up))))
    if with_breakout:
        pts += [(x + 3, top * (1 + 0.03 * up)), (x + 20, top * (1 + 0.15 * up))]
    path = _segments(pts)
    vol = np.ones(len(path))
    vol[31:41] = 2.0
    df = _to_ohlcv(path, noise, seed, volume_profile=vol)
    return df, {"pattern": "Bear Flag" if bearish else "Bull Flag", "start": 30, "end": x,
                "breakout": x + 3 if with_breakout else None}


def rectangle(noise: float = 0.003, seed: int = 7, with_breakout: bool = True) -> Tuple[pd.DataFrame, Dict]:
    base = 100.0
    pts: List[Tuple[int, float]] = [(0, base * 0.80), (30, base * 1.08)]
    x = 30
    for i in range(6):
        x += 10
        pts.append((x, base * (0.96 if i % 2 == 0 else 1.08)))
    if with_breakout:
        pts += [(x + 5, base * 1.13), (x + 30, base * 1.25)]
    else:
        pts += [(x + 5, base * 1.02), (x + 8, base * 1.0)]
    path = _smooth(_segments(pts), 3)
    df = _to_ohlcv(path, noise, seed)
    return df, {"pattern": "Rectangle", "start": 30, "end": x, "breakout": x + 4 if with_breakout else None}


def random_walk(n: int = 400, noise: float = 0.012, seed: int = 8, drift: float = 0.0002) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    path = 100 * np.exp(np.cumsum(rng.normal(drift, noise, n)))
    return _to_ohlcv(path, noise / 3, seed + 1)


GENERATORS = {
    "Head and Shoulders": lambda **k: head_and_shoulders(inverse=False, **k),
    "Inverse Head and Shoulders": lambda **k: head_and_shoulders(inverse=True, **k),
    "Double Top": lambda **k: double_top(bottom=False, **k),
    "Double Bottom": lambda **k: double_top(bottom=True, **k),
    "Cup and Handle": lambda **k: cup_and_handle(**k),
    "Ascending Triangle": lambda **k: triangle("ascending", **k),
    "Descending Triangle": lambda **k: triangle("descending", **k),
    "Symmetrical Triangle": lambda **k: triangle("symmetrical", **k),
    "Falling Wedge": lambda **k: wedge("falling", **k),
    "Rising Wedge": lambda **k: wedge("rising", **k),
    "Bull Flag": lambda **k: flag(bearish=False, **k),
    "Bear Flag": lambda **k: flag(bearish=True, **k),
    "Rectangle": lambda **k: rectangle(**k),
}
