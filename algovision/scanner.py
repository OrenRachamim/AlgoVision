"""Scan a universe of symbols for chart patterns, now and in the past."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Optional, Sequence

import pandas as pd

from algovision.core.geometry import forward_outcome
from algovision.core.types import DetectorConfig, PatternMatch
from algovision.data.provider import DataProvider
from algovision.patterns import detect_all, resolve_patterns

log = logging.getLogger(__name__)


@dataclass
class ScanResult:
    matches: List[PatternMatch] = field(default_factory=list)
    frames: Dict[str, pd.DataFrame] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)

    def to_frame(self) -> pd.DataFrame:
        rows = []
        for m in self.matches:
            rows.append({
                "symbol": m.symbol, "pattern": m.pattern, "direction": m.direction, "status": m.status,
                "score": round(m.score, 3), "start": m.start_date, "end": m.end_date,
                "breakout": m.breakout_date, "breakout_price": m.breakout_price, "level": m.level,
                "target": m.target, "stop": m.stop, "last_close": m.last_close, "bars": m.width, "scale": m.scale,
                "ret_10": m.outcome.get("ret_10"), "ret_20": m.outcome.get("ret_20"),
                "target_hit": m.outcome.get("target_hit"),
                "why": " | ".join(m.reasons),
            })
        cols = ["symbol", "pattern", "direction", "status", "score", "start", "end", "breakout", "breakout_price",
                "level", "target", "stop", "last_close", "bars", "scale", "ret_10", "ret_20", "target_hit", "why"]
        return pd.DataFrame(rows, columns=cols)

    def by_pattern(self) -> Dict[str, List[PatternMatch]]:
        out: Dict[str, List[PatternMatch]] = {}
        for m in self.matches:
            out.setdefault(m.pattern, []).append(m)
        return out


class Scanner:
    """Run pattern detection across many symbols.

    ``mode``:
      * ``current`` - only setups that are forming right now or confirmed within
        the last ``config.recent_bars`` bars.
      * ``history`` - every occurrence in the loaded window, annotated with what
        happened afterwards (forward returns, target hit).
      * ``all``     - both.
    """

    def __init__(self, provider: Optional[DataProvider] = None, config: Optional[DetectorConfig] = None,
                 patterns: Optional[Iterable[str]] = None, period: str = "2y", interval: str = "1d",
                 min_score: Optional[float] = None):
        self.provider = provider or DataProvider()
        self.cfg = config or DetectorConfig()
        self.patterns = resolve_patterns(patterns)
        self.period = period
        self.interval = interval
        self.min_score = min_score

    # ------------------------------------------------------------------
    def analyse_frame(self, symbol: str, df: pd.DataFrame, mode: str = "all") -> List[PatternMatch]:
        matches = detect_all(df, symbol=symbol, patterns=self.patterns, config=self.cfg, min_score=self.min_score)
        n = len(df)
        out: List[PatternMatch] = []
        for m in matches:
            is_current = (n - 1 - m.end_idx) <= self.cfg.recent_bars and m.status in ("forming", "confirmed")
            if mode == "current" and not is_current:
                continue
            if mode == "history" and is_current and m.status == "forming":
                continue
            if m.status == "confirmed" and m.breakout_idx is not None:
                m.outcome = forward_outcome(df, m.breakout_idx, 1 if m.direction == "bullish" else -1, m.target, m.stop)
            m.metrics["is_current"] = is_current
            m.metrics["bars_since_end"] = n - 1 - m.end_idx
            out.append(m)
        return out

    def scan(self, symbols: Sequence[str], mode: str = "current",
             progress: Optional[Callable[[str, int, int, int], None]] = None) -> ScanResult:
        symbols = list(symbols)
        result = ScanResult()
        total = len(symbols)
        done = 0

        def fetched(sym: str, ok: bool) -> None:
            pass

        frames = self.provider.get_many(symbols, self.period, self.interval, progress=fetched)
        for sym in symbols:
            done += 1
            df = frames.get(sym)
            if df is None:
                result.errors[sym] = "no data"
                if progress:
                    progress(sym, done, total, 0)
                continue
            try:
                ms = self.analyse_frame(sym, df, mode)
            except Exception as exc:  # noqa: BLE001 - one bad symbol must not kill the scan
                log.exception("%s: detection failed", sym)
                result.errors[sym] = str(exc)
                ms = []
            result.matches.extend(ms)
            result.frames[sym] = df
            if progress:
                progress(sym, done, total, len(ms))
        result.matches.sort(key=lambda m: (-(m.status == "confirmed"), -m.score))
        return result
