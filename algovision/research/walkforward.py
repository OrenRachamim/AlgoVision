"""Point-in-time (walk-forward) detection.

For every bar ``t`` the detectors only see ``df[:t+1]``.  An event is recorded
the first time a confirmed pattern appears, so the signal bar is exactly when
a live scanner would have printed it.  This is the ground truth against which
the fast hindsight method in :mod:`events` is validated.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig, PatternMatch
from algovision.patterns import detect_all
from algovision.research.events import HORIZONS, MAX_HOLD, RANDOM_DRAWS, build_events


def walk_forward_matches(symbol: str, df: pd.DataFrame, config: Optional[DetectorConfig] = None,
                         window: int = 400, start: Optional[int] = None, step: int = 1,
                         max_lag: int = 15) -> List[PatternMatch]:
    """Return confirmed matches as first seen in real time.

    Each returned match has ``breakout_idx`` set to the bar at which it was
    first observable (absolute index) and key points shifted to absolute bars.
    """
    cfg = config or DetectorConfig()
    n = len(df)
    start = window if start is None else max(start, 50)
    seen: Dict[Tuple[str, int, int], PatternMatch] = {}
    out: List[PatternMatch] = []
    for t in range(start, n, step):
        lo = max(0, t - window + 1)
        sub = df.iloc[lo:t + 1]
        for m in detect_all(sub, symbol=symbol, config=cfg):
            if m.status != "confirmed" or m.breakout_idx is None:
                continue
            bo_abs = lo + int(m.breakout_idx)
            if t - bo_abs > max_lag:
                continue            # old breakout: it would have been reported earlier (or never, if not visible)
            key = (m.pattern, lo + m.start_idx // 3 * 3, bo_abs // 3)   # coarse identity across windows
            key = (m.pattern, bo_abs, round(m.start_idx + lo, -1))
            if any(k[0] == m.pattern and abs(k[1] - bo_abs) <= 2 and abs(k[2] - key[2]) <= 10 for k in seen):
                continue
            # shift to absolute indices; the signal bar is *now* (t)
            m.start_idx += lo
            m.end_idx += lo
            m.breakout_idx = t
            for kp in m.key_points:
                kp.idx += lo
            for ln in m.lines:
                ln.x0 += lo
                ln.x1 += lo
            m.scale = 0                 # already point-in-time: no extra delay needed
            m.attach_dates(df.index)
            seen[key] = m
            out.append(m)
    return out


def walk_forward_events(symbol: str, df: pd.DataFrame, bench: Optional[pd.DataFrame] = None,
                        config: Optional[DetectorConfig] = None, window: int = 400, start: Optional[int] = None,
                        step: int = 1, horizons: Sequence[int] = HORIZONS, random_draws: int = RANDOM_DRAWS,
                        max_hold: int = MAX_HOLD, seed: int = 0) -> List[Dict]:
    matches = walk_forward_matches(symbol, df, config, window, start, step)
    events, _ = build_events(symbol, df, bench, config, horizons, random_draws, max_hold, seed, matches=matches)
    for e in events:
        e["method"] = "walkforward"
    return events
