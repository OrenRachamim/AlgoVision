"""Shared data structures used by every detector."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
import datetime as _dt

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Pivot:
    """A swing point on the chart.

    ``kind`` is +1 for a swing high (peak) and -1 for a swing low (trough).
    ``idx`` is the integer bar position inside the analysed DataFrame.
    """

    idx: int
    price: float
    kind: int

    @property
    def is_high(self) -> bool:
        return self.kind > 0

    @property
    def is_low(self) -> bool:
        return self.kind < 0


@dataclass
class KeyPoint:
    """A labelled point drawn on the chart (e.g. "Head", "Left shoulder")."""

    idx: int
    price: float
    label: str
    date: Optional[str] = None


@dataclass
class Line:
    """A straight line segment drawn on the chart (neckline, trendline...)."""

    x0: int
    y0: float
    x1: int
    y1: float
    label: str
    style: str = "solid"

    def value_at(self, x: float) -> float:
        if self.x1 == self.x0:
            return self.y0
        slope = (self.y1 - self.y0) / (self.x1 - self.x0)
        return self.y0 + slope * (x - self.x0)


@dataclass
class PatternMatch:
    """One detected occurrence of a chart pattern on one symbol."""

    symbol: str
    pattern: str
    direction: str                    # "bullish" | "bearish" | "neutral"
    status: str                       # "forming" | "confirmed" | "failed" | "expired"
    start_idx: int
    end_idx: int
    score: float
    reasons: List[str] = field(default_factory=list)
    key_points: List[KeyPoint] = field(default_factory=list)
    lines: List[Line] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    breakout_idx: Optional[int] = None
    breakout_price: Optional[float] = None
    level: Optional[float] = None     # the line/level whose break confirms the pattern
    target: Optional[float] = None
    stop: Optional[float] = None
    scale: Optional[int] = None       # pivot "order" that produced the match
    # Filled in by the scanner:
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    breakout_date: Optional[str] = None
    last_close: Optional[float] = None
    outcome: Dict[str, Any] = field(default_factory=dict)

    # ---- helpers -----------------------------------------------------
    @property
    def width(self) -> int:
        return self.end_idx - self.start_idx

    def overlaps(self, other: "PatternMatch", min_frac: float = 0.5) -> bool:
        """True when two matches of the same pattern cover mostly the same bars."""
        if self.pattern != other.pattern:
            return False
        lo = max(self.start_idx, other.start_idx)
        hi = min(self.end_idx, other.end_idx)
        inter = max(0, hi - lo)
        shorter = max(1, min(self.width, other.width))
        return inter / shorter >= min_frac

    def attach_dates(self, index: pd.Index) -> None:
        def d(i: Optional[int]) -> Optional[str]:
            if i is None:
                return None
            i = int(min(max(i, 0), len(index) - 1))
            v = index[i]
            if isinstance(v, (pd.Timestamp, _dt.datetime, _dt.date)):
                return pd.Timestamp(v).strftime("%Y-%m-%d")
            return str(v)

        self.start_date = d(self.start_idx)
        self.end_date = d(self.end_idx)
        self.breakout_date = d(self.breakout_idx)
        for kp in self.key_points:
            kp.date = d(kp.idx)

    def to_dict(self) -> Dict[str, Any]:
        out = asdict(self)
        out["width"] = self.width
        return out

    def summary(self) -> str:
        """One-line, human-readable description."""
        where = f"{self.start_date} -> {self.end_date}" if self.start_date else f"bars {self.start_idx}-{self.end_idx}"
        bo = ""
        if self.status == "confirmed" and self.breakout_date:
            bo = f", breakout {self.breakout_date} @ {self.breakout_price:.2f}"
        tgt = f", target {self.target:.2f}" if self.target is not None else ""
        return (f"{self.symbol}: {self.pattern} ({self.direction}, {self.status}, "
                f"score {self.score:.2f}) {where}{bo}{tgt}")

    def explanation(self) -> str:
        """Multi-line 'why' text."""
        lines = [self.summary()]
        for r in self.reasons:
            lines.append(f"  - {r}")
        if self.outcome:
            parts = []
            for k in ("ret_5", "ret_10", "ret_20", "ret_40"):
                if k in self.outcome and self.outcome[k] is not None:
                    parts.append(f"{k.replace('ret_', '+')}b: {self.outcome[k] * 100:+.1f}%")
            if "target_hit" in self.outcome:
                parts.append("target hit" if self.outcome["target_hit"] else "target not hit")
            if parts:
                lines.append("  outcome after breakout: " + ", ".join(parts))
        return "\n".join(lines)


@dataclass
class DetectorConfig:
    """Tunable tolerances shared across detectors.

    All percentages are fractions (0.03 == 3%).
    """

    # pivot detection
    pivot_orders: Tuple[int, ...] = (3, 5, 8, 13)
    pivot_min_move_atr: float = 1.0      # discard swings smaller than N * ATR(14)
    pivot_min_move_pct: float = 0.01     # ... or smaller than this fraction of price

    # generic
    min_score: float = 0.60
    recent_bars: int = 15                # a pattern is "current" if it ended within N bars
    breakout_confirm_pct: float = 0.002  # close must exceed level by this fraction
    volume_lookback: int = 20
    cross_pattern_overlap: Optional[float] = 0.6   # IoU above which two patterns are one interpretation

    # head & shoulders
    hs_shoulder_tol: float = 0.06
    hs_min_head_prominence: float = 0.015
    hs_neckline_tol: float = 0.05
    hs_time_symmetry: Tuple[float, float] = (0.4, 2.5)

    # double / triple tops & bottoms
    dt_peak_tol: float = 0.035
    dt_min_depth: float = 0.03
    dt_min_separation: int = 8

    # cup & handle
    cup_min_bars: int = 20
    cup_max_bars: int = 300
    cup_min_depth: float = 0.10
    cup_max_depth: float = 0.55
    cup_rim_tol: float = 0.06
    cup_min_r2: float = 0.65
    handle_min_bars: int = 3
    handle_max_frac: float = 0.5          # handle length <= this fraction of cup length
    handle_max_depth_frac: float = 0.5    # handle depth <= this fraction of cup depth
    handle_max_depth: float = 0.18

    # trendline patterns (triangles, wedges, rectangles)
    tl_min_pivots: int = 5
    tl_max_pivots: int = 7
    tl_max_residual: float = 0.20        # max |residual| as fraction of pattern height
    tl_flat_slope: float = 0.25          # |normalised slope| below this == flat
    tl_min_height: float = 0.03          # initial height as fraction of price
    tl_max_height: float = 0.35          # taller than this is a swing, not a consolidation
    tl_apex_max_frac: float = 2.0        # apex must be within N pattern widths after end

    # flags
    flag_pole_max_bars: int = 20
    flag_pole_min_pct: float = 0.08
    flag_pole_min_atr: float = 3.0
    flag_min_bars: int = 5
    flag_max_bars: int = 30
    flag_max_retrace: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def as_float_array(x) -> np.ndarray:
    return np.asarray(x, dtype=float)
