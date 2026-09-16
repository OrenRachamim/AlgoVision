"""Exit-rule evaluation: fills and holding times for each exit family on hand-made paths."""

import numpy as np

from algovision.research.exits import Rule, evaluate
from algovision.research.shortterm import Paths


def _path(closes, highs=None, opens=None):
    cl = np.array([closes], dtype=float)
    hi = np.array([highs if highs is not None else closes], dtype=float)
    op = np.array([opens if opens is not None else [0.0] + list(closes[:-1])], dtype=float)
    return Paths(op, hi, np.minimum(op, cl), cl, np.array([True]))


def test_time_exit_uses_close_of_last_bar():
    p = _path([0.01, 0.02, -0.01, 0.03])
    r, b = evaluate(p, Rule("t3", "time", 3))
    assert r[0] == -0.01 and b[0] == 3


def test_fixed_target_fills_at_target_or_gap_open():
    p = _path([0.005, 0.03, 0.04], highs=[0.01, 0.035, 0.05])
    r, b = evaluate(p, Rule("tp2", "target", 3, 0.02))
    assert r[0] == 0.02 and b[0] == 2
    gap = _path([0.05, 0.06], highs=[0.06, 0.07], opens=[0.04, 0.05])   # opens above the target on bar 1
    r, b = evaluate(gap, Rule("tp2", "target", 2, 0.02))
    assert r[0] == 0.04 and b[0] == 1


def test_rising_target_grows_each_bar():
    # target: 2% on bar 1, 2.5% on bar 2, 3% on bar 3; highs reach 2.4% only on bar 2 (miss) and 3.1% on bar 3
    p = _path([0.0, 0.02, 0.03], highs=[0.01, 0.024, 0.031])
    r, b = evaluate(p, Rule("r", "rising", 3, 0.02, 0.005))
    assert b[0] == 3 and r[0] == 0.03


def test_per_day_threshold_exits_on_close():
    p = _path([0.004, 0.012, 0.02])          # 0.4% after 1 bar (<0.5%), 1.2% after 2 bars (>= 1.0%)
    r, b = evaluate(p, Rule("pd", "perday", 3, 0.005))
    assert b[0] == 2 and r[0] == 0.012


def test_hybrid_takes_2pct_on_day_one_then_6pct():
    day1 = _path([0.03, 0.0], highs=[0.03, 0.0])
    r, b = evaluate(day1, Rule("h", "hybrid", 2, 0.02, 0.06))
    assert r[0] == 0.02 and b[0] == 1
    later = _path([0.0, 0.03, 0.07, 0.0], highs=[0.01, 0.05, 0.065, 0.0])
    r, b = evaluate(later, Rule("h", "hybrid", 4, 0.02, 0.06))
    assert r[0] == 0.06 and b[0] == 3


def test_trailing_stop_from_peak_close():
    p = _path([0.02, 0.05, 0.03, -0.01, 0.0])     # peak 5% at bar 2; bar 4 closes 5.7% below it
    r, b = evaluate(p, Rule("tr", "trail", 5, 0.05))
    assert b[0] == 4 and r[0] == -0.01
    r, b = evaluate(p, Rule("tr8", "trail", 5, 0.08))
    assert b[0] == 5 and r[0] == 0.0


def test_incomplete_path_gives_nan():
    p = _path([0.01, np.nan, np.nan])
    r, _ = evaluate(p, Rule("t3", "time", 3))
    assert np.isnan(r[0])
