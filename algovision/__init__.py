"""AlgoVision - visual chart-pattern detection for US equities.

The package finds classic technical-analysis setups (head & shoulders,
cup & handle, double tops/bottoms, triangles, wedges, flags, rectangles)
on OHLCV price series, explains *why* each match qualifies, and can scan
whole universes (S&P 500, NASDAQ-100) for both current and historical
occurrences.
"""

from algovision.core.types import PatternMatch, Pivot, DetectorConfig
from algovision.patterns import detect_all, PATTERN_REGISTRY
from algovision.scanner import Scanner, ScanResult

__version__ = "0.1.0"

__all__ = [
    "PatternMatch",
    "Pivot",
    "DetectorConfig",
    "detect_all",
    "PATTERN_REGISTRY",
    "Scanner",
    "ScanResult",
    "__version__",
]
