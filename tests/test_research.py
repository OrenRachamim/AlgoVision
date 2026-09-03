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


def test_shortterm_evaluate_rules():
    from algovision.research.shortterm import Paths, evaluate
    p = Paths(op=np.array([[0.0, 0.01, 0.05]]), hi=np.array([[0.005, 0.03, 0.06]]), lo=np.array([[-0.01, -0.005, 0.0]]),
              cl=np.array([[0.002, 0.02, 0.055]]), valid=np.array([True]))
    r, b = evaluate(p, 3, 0.02, None)
    assert r[0] == pytest.approx(0.02) and b[0] == 2          # target touched on bar 2, fills at target
    r, b = evaluate(p, 3, 0.04, None)
    assert r[0] == pytest.approx(0.05) and b[0] == 3          # gaps through target: fills at the open
    r, b = evaluate(p, 3, None, 0.008)
    assert r[0] == pytest.approx(-0.008) and b[0] == 1        # stop on bar 1
    r, b = evaluate(p, 3, 0.02, 0.008)
    assert r[0] == pytest.approx(-0.008)                      # stop wins
    r, b = evaluate(p, 1, None, None)
    assert r[0] == pytest.approx(0.002)                       # time exit at close


def test_shortterm_grid_on_synthetic():
    from algovision.research.shortterm import build_paths, strategy_grid
    frames, ev = {}, []
    for name, gen in GENERATORS.items():
        df, _ = gen()
        frames[name] = df
        e, _ = build_events(name, df)
        ev += e
    E = pd.DataFrame(ev)
    pe, pr, order = build_paths(E, lambda s: frames[s])
    g = strategy_grid(E, pe, pr, order, holds=(2,), targets=(0.02, None), stops=(None,), min_n=5)
    assert len(g) == 2 and (g["n"] == len(E)).all()
    assert {"net_ret", "excess", "p", "profit_factor", "hit"} <= set(g.columns)
    assert g["excess"].iloc[0] > 0     # textbook breakouts continue for a couple of bars


def test_deepdive_analyses_on_synthetic():
    from algovision.core.types import DetectorConfig
    from algovision.data.synthetic import random_walk
    from algovision.research import deepdive as dd
    from algovision.research.events import add_local_baseline
    frames = {f"RW{i}": random_walk(900, seed=10 + i, noise=0.015) for i in range(6)}

    class P:
        def get(self, s, period, interval):
            return frames[s]

    dd._PROVIDER, dd._SPY = P(), None
    rows = []
    for s in frames:
        for pat in ("Falling Wedge", "Rising Wedge", "Symmetrical Triangle"):
            _, ev, err = dd._task((s, pat, "10y", "1d", DetectorConfig().to_dict()))
            assert err is None, err
            rows += ev
    E = pd.DataFrame(rows)
    assert len(E) >= 10 and {"convergence", "height_pct", "dist_ma200", "atr_at_signal"} <= set(E.columns)
    E = add_local_baseline(E, lambda s: frames[s])
    split = str(pd.to_datetime(E["signal_date"]).median().date())
    ft = dd.feature_table(E, split, features=["score", "convergence"], bins=2, min_events=20, min_bin=5)
    assert len(ft) and {"train", "test"} <= set(ft["period"])
    ex = dd.exit_table(E, lambda s: frames[s], split)
    assert len(ex) and "avg_r" in ex.columns
    en = dd.entry_table(E, lambda s: frames[s], split)
    assert len(en) and "next open" in set(en["entry"])
    curve = dd.portfolio_curve(E, lambda s: frames[s], hold=10)
    st = dd.curve_stats(curve)
    assert st["days"] > 0 and "max_drawdown" in st


def test_deepdive_report_writes(tmp_path):
    from algovision.core.types import DetectorConfig
    from algovision.data.synthetic import random_walk
    from algovision.research import deepdive as dd
    from algovision.research.events import add_local_baseline
    frames = {f"RW{i}": random_walk(1200, seed=20 + i, noise=0.015) for i in range(8)}

    class P:
        def get(self, s, period, interval):
            return frames[s]

    dd._PROVIDER, dd._SPY = P(), None
    rows = []
    for s in frames:
        for pat in ("Falling Wedge", "Rising Wedge", "Symmetrical Triangle", "Double Bottom"):
            rows += dd._task((s, pat, "10y", "1d", DetectorConfig().to_dict()))[1]
    E = add_local_baseline(pd.DataFrame(rows), lambda s: frames[s])
    split = str(pd.to_datetime(E["signal_date"]).median().date())
    p = dd.write_deepdive_report(tmp_path, "Synthetic", E, lambda s: frames[s], split)
    assert p.exists() and (tmp_path / "equity.png").exists() and (tmp_path / "filters.csv").exists()


def test_factors_engine_on_synthetic():
    from algovision.data.synthetic import random_walk
    from algovision.research import factors as F
    frames = {f"S{i}": random_walk(1500, seed=100 + i, noise=0.015, drift=0.0003 * (i % 5)) for i in range(120)}
    spy = random_walk(1500, seed=999, noise=0.01)
    panel = F.load_panel(list(frames), lambda s: frames[s])
    assert panel["Close"].shape == (1500, 120)
    bt = F.cross_sectional_backtest(panel, F.momentum_signal(252, 21), "M", n_groups=5, min_names=50)
    assert len(bt) > 10 and {"G1", "G5", "long_short", "universe"} <= set(bt.columns)
    assert (bt["G1_turnover"].between(0, 1)).all()
    summ = F.summarize_groups(bt, 12, 5, split_date=str(bt.index[len(bt) // 2].date()))
    assert ("test", "long_short") in summ.index and "sharpe" in summ.columns
    # persistent drift differences must show up as a positive momentum spread
    assert summ.loc[("all", "long_short"), "mean_period"] > 0
    assert summ.loc[("all", "top_minus_universe"), "mean_period"] > 0
    ts = F.timeseries_momentum(spy)
    assert set(ts) >= {"buy_and_hold", "tsmom_252", "ma200"}
    ev = F.reversal_events(panel, spy["Close"], thresholds=(2.0,), horizons=(1, 3))
    assert len(ev) > 100 and {"xloc_1", "ret_3", "direction"} <= set(ev.columns)
    tab = F.reversal_table(ev, (1, 3))
    assert ("all", 2.0, 1) in tab.index
    curve = F.reversal_portfolio(ev, panel, hold=3)
    assert len(curve) > 100
