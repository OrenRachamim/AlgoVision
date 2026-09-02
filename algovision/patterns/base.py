"""Base class shared by all pattern detectors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Sequence

import numpy as np
import pandas as pd

from algovision.core.geometry import first_cross, volume_ratio
from algovision.core.types import DetectorConfig, PatternMatch, Pivot


class Detector(ABC):
    """A pattern detector turns (df, pivots) into a list of PatternMatch."""

    #: Names of the patterns this detector may emit.
    names: Sequence[str] = ()

    def __init__(self, config: Optional[DetectorConfig] = None):
        self.cfg = config or DetectorConfig()

    @abstractmethod
    def detect(self, symbol: str, df: pd.DataFrame, pivots: List[Pivot], order: int) -> List[PatternMatch]:
        ...

    # ---- shared helpers ------------------------------------------------
    @staticmethod
    def arrays(df: pd.DataFrame):
        close = df["Close"].to_numpy(dtype=float)
        high = df["High"].to_numpy(dtype=float)
        low = df["Low"].to_numpy(dtype=float)
        vol = df["Volume"].to_numpy(dtype=float) if "Volume" in df.columns else None
        return close, high, low, vol

    def breakout(self, close: np.ndarray, start: int, level_fn, direction: int, stop: Optional[int] = None):
        return first_cross(close, start, level_fn, direction, self.cfg.breakout_confirm_pct, stop)

    def breakout_volume_reason(self, vol: Optional[np.ndarray], idx: int) -> tuple:
        """Return (score, reason) for volume expansion on the breakout bar."""
        vr = volume_ratio(vol, idx, self.cfg.volume_lookback)
        if vr is None:
            return 0.5, None
        if vr >= 1.5:
            return 1.0, f"breakout volume {vr:.1f}x the {self.cfg.volume_lookback}-bar average (strong confirmation)"
        if vr >= 1.1:
            return 0.75, f"breakout volume {vr:.1f}x the {self.cfg.volume_lookback}-bar average"
        return 0.35, f"breakout volume only {vr:.1f}x average (weak confirmation)"

    @staticmethod
    def pct(a: float, b: float) -> float:
        """Percentage difference of a relative to b."""
        return (a / b - 1.0) if b else 0.0
