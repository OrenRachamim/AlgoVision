"""Pattern registry and the top-level ``detect_all`` entry point."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Type

import pandas as pd

from algovision.core.pivots import find_pivots
from algovision.core.types import DetectorConfig, PatternMatch
from algovision.patterns.base import Detector
from algovision.patterns.cup_handle import CupAndHandleDetector
from algovision.patterns.double import DoubleTopBottomDetector
from algovision.patterns.flags import FlagDetector
from algovision.patterns.head_shoulders import HeadAndShouldersDetector
from algovision.patterns.trendlines import TrendlinePatternDetector

DETECTORS: Sequence[Type[Detector]] = (
    HeadAndShouldersDetector,
    DoubleTopBottomDetector,
    CupAndHandleDetector,
    TrendlinePatternDetector,
    FlagDetector,
)

#: pattern name -> detector class
PATTERN_REGISTRY: Dict[str, Type[Detector]] = {name: d for d in DETECTORS for name in d.names}
ALL_PATTERNS: List[str] = list(PATTERN_REGISTRY)

# handy aliases for the CLI
ALIASES = {
    "hs": "Head and Shoulders", "head-and-shoulders": "Head and Shoulders",
    "ihs": "Inverse Head and Shoulders", "inverse-head-and-shoulders": "Inverse Head and Shoulders",
    "double-top": "Double Top", "double-bottom": "Double Bottom",
    "triple-top": "Triple Top", "triple-bottom": "Triple Bottom",
    "cup": "Cup and Handle", "cup-and-handle": "Cup and Handle", "inverted-cup": "Inverted Cup and Handle",
    "ascending-triangle": "Ascending Triangle", "descending-triangle": "Descending Triangle",
    "symmetrical-triangle": "Symmetrical Triangle", "rising-wedge": "Rising Wedge", "falling-wedge": "Falling Wedge",
    "rectangle": "Rectangle", "bull-flag": "Bull Flag", "bear-flag": "Bear Flag",
}


def resolve_patterns(names: Optional[Iterable[str]]) -> List[str]:
    if not names:
        return list(ALL_PATTERNS)
    out: List[str] = []
    for n in names:
        key = n.strip()
        if key.lower() in ("all", "*"):
            return list(ALL_PATTERNS)
        canon = ALIASES.get(key.lower())
        if canon is None:
            matches = [p for p in ALL_PATTERNS if p.lower() == key.lower() or p.lower().replace(" ", "-") == key.lower()]
            if not matches:
                raise ValueError(f"unknown pattern {n!r}; known: {', '.join(ALL_PATTERNS)}")
            canon = matches[0]
        if canon not in out:
            out.append(canon)
    return out


def _overlap_frac(a: PatternMatch, b: PatternMatch) -> float:
    """Intersection relative to the *shorter* match."""
    lo, hi = max(a.start_idx, b.start_idx), min(a.end_idx, b.end_idx)
    return max(0, hi - lo) / max(1, min(a.width, b.width))


#: More specific (more constrained) patterns win ties against generic ones when
#: both describe the same bars.  A cup with level rims is also a "double top"
#: until it breaks out; the cup is the more informative reading.
SPECIFICITY = {
    "Cup and Handle": 2, "Inverted Cup and Handle": 2,
    "Head and Shoulders": 2, "Inverse Head and Shoulders": 2,
    "Ascending Triangle": 1, "Descending Triangle": 1, "Symmetrical Triangle": 1,
    "Rising Wedge": 1, "Falling Wedge": 1, "Rectangle": 1,
    "Double Top": 0, "Double Bottom": 0, "Triple Top": 0, "Triple Bottom": 0,
    "Bull Flag": 0, "Bear Flag": 0,
}
_SPECIFICITY_BONUS = 0.06


def _rank(m: PatternMatch) -> float:
    return m.score + _SPECIFICITY_BONUS * SPECIFICITY.get(m.pattern, 0)


def _iou(a: PatternMatch, b: PatternMatch) -> float:
    """Intersection over union of the two bar ranges."""
    lo, hi = max(a.start_idx, b.start_idx), min(a.end_idx, b.end_idx)
    inter = max(0, hi - lo)
    union = max(a.end_idx, b.end_idx) - min(a.start_idx, b.start_idx)
    return inter / max(1, union)


def dedupe(matches: List[PatternMatch], min_overlap: float = 0.5,
           cross_pattern_overlap: Optional[float] = 0.75) -> List[PatternMatch]:
    """Drop lower-scoring duplicates.

    Two matches of the *same* pattern covering >= ``min_overlap`` of the shorter
    one are duplicates (typically the same structure seen at two pivot scales).
    When ``cross_pattern_overlap`` is set, different patterns whose bar ranges
    have an intersection-over-union >= that value are reduced to the
    best-scoring interpretation, so one consolidation is not reported as both
    a wedge and a triangle.  A small pattern nested inside a large one (a flag
    in a cup's handle) is *not* suppressed.
    """
    kept: List[PatternMatch] = []
    for m in sorted(matches, key=lambda x: (-_rank(x), -x.width)):
        dup = False
        for k in kept:
            f = _overlap_frac(m, k)
            if k.pattern == m.pattern and f >= min_overlap:
                dup = True
                break
            if cross_pattern_overlap is not None and _iou(m, k) >= cross_pattern_overlap:
                dup = True
                break
        if not dup:
            kept.append(m)
    kept.sort(key=lambda x: (x.end_idx, -x.score))
    return kept


def detect_all(
    df: pd.DataFrame,
    symbol: str = "",
    patterns: Optional[Iterable[str]] = None,
    config: Optional[DetectorConfig] = None,
    orders: Optional[Sequence[int]] = None,
    min_score: Optional[float] = None,
) -> List[PatternMatch]:
    """Run every requested detector at every pivot scale and return de-duplicated matches.

    The DataFrame must contain ``Open, High, Low, Close`` (and optionally ``Volume``)
    columns with a chronological index.
    """
    cfg = config or DetectorConfig()
    wanted = set(resolve_patterns(patterns))
    detectors = [d(cfg) for d in DETECTORS if any(n in wanted for n in d.names)]
    threshold = cfg.min_score if min_score is None else min_score
    matches: List[PatternMatch] = []
    scales = tuple(orders or cfg.pivot_orders)
    for order in scales:
        pivots = find_pivots(df, order=order, min_move_atr=cfg.pivot_min_move_atr, min_move_pct=cfg.pivot_min_move_pct)
        if len(pivots) < 3:
            continue
        for det in detectors:
            if getattr(det, "single_scale", False) and order != min(scales):
                continue
            for m in det.detect(symbol, df, pivots, order):
                if m.pattern in wanted and m.score >= threshold:
                    matches.append(m)
    matches = dedupe(matches, cross_pattern_overlap=cfg.cross_pattern_overlap)
    for m in matches:
        m.attach_dates(df.index)
        m.last_close = float(df["Close"].iloc[-1])
    return matches


__all__ = ["DETECTORS", "PATTERN_REGISTRY", "ALL_PATTERNS", "ALIASES", "resolve_patterns", "dedupe", "detect_all"]
