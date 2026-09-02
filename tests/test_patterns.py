import numpy as np
import pytest

from algovision.core.types import DetectorConfig
from algovision.data.synthetic import GENERATORS, random_walk
from algovision.patterns import ALL_PATTERNS, dedupe, detect_all, resolve_patterns


@pytest.mark.parametrize("name", list(GENERATORS))
def test_detects_confirmed_textbook_pattern(name):
    df, meta = GENERATORS[name](with_breakout=True)
    matches = detect_all(df, symbol="SYN")
    hits = [m for m in matches if m.pattern == name]
    assert hits, f"{name} not detected; got {[m.pattern for m in matches]}"
    best = max(hits, key=lambda m: m.score)
    assert best.status == "confirmed"
    assert best.breakout_idx is not None
    assert abs(best.start_idx - meta["start"]) <= 15
    assert best.score >= 0.55
    assert best.reasons and any("Confirmed" in r for r in best.reasons)
    assert best.target is not None and best.level is not None
    if best.direction == "bullish":
        assert best.target > best.level
    elif best.direction == "bearish":
        assert best.target < best.level
    assert best.start_date is not None and best.end_date is not None


@pytest.mark.parametrize("name", list(GENERATORS))
def test_detects_forming_pattern_without_breakout(name):
    df, meta = GENERATORS[name](with_breakout=False)
    matches = detect_all(df, symbol="SYN")
    hits = [m for m in matches if m.pattern == name]
    assert hits, f"{name} (forming) not detected; got {[m.pattern for m in matches]}"
    best = max(hits, key=lambda m: m.score)
    assert best.status == "forming"
    assert best.breakout_idx is None
    assert best.end_idx == len(df) - 1


def test_direction_matches_pattern_semantics():
    expected = {
        "Head and Shoulders": "bearish", "Inverse Head and Shoulders": "bullish",
        "Double Top": "bearish", "Double Bottom": "bullish", "Cup and Handle": "bullish",
        "Ascending Triangle": "bullish", "Descending Triangle": "bearish",
        "Falling Wedge": "bullish", "Rising Wedge": "bearish", "Bull Flag": "bullish", "Bear Flag": "bearish",
    }
    for name, direction in expected.items():
        df, _ = GENERATORS[name]()
        hits = [m for m in detect_all(df) if m.pattern == name]
        assert hits and max(hits, key=lambda m: m.score).direction == direction, name


def test_pattern_filter_and_aliases():
    df, _ = GENERATORS["Cup and Handle"]()
    ms = detect_all(df, patterns=["cup"])
    assert ms and all(m.pattern == "Cup and Handle" for m in ms)
    assert resolve_patterns(["hs", "Double Top", "falling-wedge"]) == ["Head and Shoulders", "Double Top", "Falling Wedge"]
    assert resolve_patterns(None) == ALL_PATTERNS
    with pytest.raises(ValueError):
        resolve_patterns(["no-such-pattern"])


def test_random_walk_does_not_crash_and_matches_are_sane():
    for seed in range(4):
        df = random_walk(500, seed=seed)
        for m in detect_all(df, symbol="RW"):
            assert 0 <= m.start_idx < m.end_idx < len(df)
            assert 0.0 <= m.score <= 1.0
            assert m.status in ("forming", "confirmed", "failed", "expired")
            if m.breakout_idx is not None:
                assert m.start_idx < m.breakout_idx <= m.end_idx


def test_dedupe_keeps_best_of_overlapping():
    df, _ = GENERATORS["Head and Shoulders"]()
    raw = detect_all(df, config=DetectorConfig(cross_pattern_overlap=None))
    same = [m for m in raw if m.pattern == "Head and Shoulders"]
    for a in same:
        for b in same:
            if a is not b:
                assert not a.overlaps(b, 0.5)


def test_min_score_threshold():
    df, _ = GENERATORS["Double Top"]()
    assert len(detect_all(df, min_score=0.0)) >= len(detect_all(df, min_score=0.7))
    assert all(m.score >= 0.9 for m in detect_all(df, min_score=0.9))


def test_to_dict_is_json_serialisable():
    import json
    df, _ = GENERATORS["Bull Flag"]()
    ms = detect_all(df)
    assert ms
    json.dumps([m.to_dict() for m in ms], default=str)
