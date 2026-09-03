import numpy as np
import pandas as pd
import pytest

from algovision.data.synthetic import GENERATORS, random_walk
from algovision.research.events import build_events, simulate_trade, structure_complete_idx
from algovision.research.stats import (bootstrap_mean_ci, compare_walkforward, permutation_pvalue, summary_table,
                                       structure_table, wilson)
from algovision.research.walkforward import walk_forward_events


@pytest.fixture(scope="module")
def synthetic_events():
    ev, st = [], []
    for name, gen in GENERATORS.items():
        df, _ = gen()
        e, s = build_events(name, df)
        ev += e
        st += s
    df = random_walk(700, seed=3)
    e, s = build_events("RW", df)
    return pd.DataFrame(ev + e), pd.DataFrame(st + s)


def test_events_are_point_in_time_and_next_open(synthetic_events):
    E, _ = synthetic_events
    assert len(E) > 10
    assert (E["entry_idx"] == E["signal_idx"] + 1).all()
    assert (E["delay_bars"] >= 0).all()
    assert set(E["direction"]) <= {"bullish", "bearish"}
    assert E["exit_reason"].isin(["target", "stop", "time"]).all()
    # a textbook confirmed pattern should be profitable at 20 bars in its direction
    cup = E[(E["symbol"] == "Cup and Handle") & (E["pattern"] == "Cup and Handle")].iloc[0]
    assert cup["ret_20"] > 0 and cup["exit_reason"] != "stop"


def test_random_baseline_columns(synthetic_events):
    E, _ = synthetic_events
    cols = [c for c in E.columns if c.startswith("rand_20_")]
    assert len(cols) == 20
    row = E.iloc[0]
    assert np.isclose(row["xrand_20"], row["ret_20"] - np.nanmean(row[cols].astype(float)))


def test_simulate_trade_target_and_stop():
    close = np.array([100, 101, 103, 106, 104, 102.0])
    high = close + 1
    low = close - 1
    r = simulate_trade(high, low, close, 0, 100.0, +1, target=105.0, stop=97.0, max_hold=10)
    assert r["exit_reason"] == "target" and r["r_multiple"] == pytest.approx(5 / 3)
    r = simulate_trade(high, low, close, 0, 100.0, -1, target=95.0, stop=102.0, max_hold=10)
    assert r["exit_reason"] == "stop" and r["r_multiple"] == pytest.approx(-1.0)
    r = simulate_trade(high, low, close, 0, 100.0, +1, target=200.0, stop=50.0, max_hold=3)
    assert r["exit_reason"] == "time" and r["bars_held"] == 3


def test_stats_helpers():
    lo, hi = wilson(60, 100)
    assert 0.49 < lo < 0.6 < hi < 0.71
    ci = bootstrap_mean_ci(np.random.default_rng(0).normal(1, 1, 500))
    assert ci[0] < 1 < ci[1]
    rng = np.random.default_rng(1)
    actual = rng.normal(0.02, 0.05, 300)
    rand = rng.normal(0.0, 0.05, (300, 20))
    pv = permutation_pvalue(actual, rand)
    assert pv["p_one_sided"] < 0.01 and pv["z"] > 3
    pv = permutation_pvalue(rng.normal(0, 0.05, 300), rand)
    assert pv["p_one_sided"] > 0.05


def test_summary_and_structure_tables(synthetic_events):
    E, S = synthetic_events
    t = summary_table(E)
    assert "ALL" in t.index and t.loc["ALL", "n"] == len(E)
    assert {"hit_20", "xrand_20", "p_20", "target_rate", "avg_r"} <= set(t.columns)
    st = structure_table(S)
    assert "ALL" in st.index and st.loc["ALL", "confirm_rate"] <= 1.0


def test_walkforward_matches_hindsight_on_clean_pattern():
    df, meta = GENERATORS["Double Bottom"]()
    hind, _ = build_events("X", df)
    wf = walk_forward_events("X", df, window=80, start=60)
    assert wf
    H, W = pd.DataFrame(hind), pd.DataFrame(wf)
    cmp_ = compare_walkforward(H, W)
    assert cmp_["walkforward_events"] >= 1
    db = W[W["pattern"] == "Double Bottom"]
    assert len(db) == 1 and abs(int(db["signal_idx"].iloc[0]) - int(H[H["pattern"] == "Double Bottom"]["signal_idx"].iloc[0])) <= 3


def test_report_writes_files(synthetic_events, tmp_path):
    from algovision.research.report import write_research_report
    E, S = synthetic_events
    p = write_research_report(tmp_path, E, S, None, {"generated": "now", "universe": "synthetic", "n_symbols": 14,
                                                       "period": "-", "benchmark": "-", "config": {"min_score": 0.6}})
    assert p.exists() and (tmp_path / "report.md").exists() and (tmp_path / "summary_by_pattern.csv").exists()
    assert "Per-pattern results" in (tmp_path / "report.md").read_text()


def test_local_baseline_columns():
    from algovision.research.events import add_local_baseline
    df, _ = GENERATORS["Falling Wedge"]()
    ev, _ = build_events("FW", df)
    E = add_local_baseline(pd.DataFrame(ev), lambda s: df)
    assert "xloc_20" in E.columns and E["xloc_5"].notna().any()
    cols = [c for c in E.columns if c.startswith("loc_5_")]
    assert len(cols) == 20
    row = E[E["xloc_5"].notna()].iloc[0]
    assert np.isclose(row["xloc_5"], row["ret_5"] - np.mean(row[cols].astype(float)))
