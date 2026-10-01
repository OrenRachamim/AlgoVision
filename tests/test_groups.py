import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig
from algovision.research import groups as G
from tests.test_peers import _frames


def test_basket_frame_is_an_equal_weight_index():
    frames = _frames(n_groups=1, per_group=4, n=400)
    members = list(frames)
    b = G.basket_frame(frames, members)
    assert b is not None and list(b.columns) == ["Open", "High", "Low", "Close", "Volume", "n_members"]
    assert abs(b["Close"].iloc[0] - 100 * (1 + np.mean([frames[m]["Close"].pct_change().iloc[0] for m in members]))) < 1e-9 or b["Close"].iloc[0] == 100
    # the basket's daily return is the mean of the members' daily returns
    r_b = b["Close"].pct_change().iloc[5:50].to_numpy()
    r_m = pd.DataFrame({m: frames[m]["Close"].pct_change() for m in members}).mean(axis=1).iloc[5:50].to_numpy()
    assert np.allclose(r_b, r_m)
    assert (b["High"] >= b[["Open", "Close"]].max(axis=1)).all() and (b["Low"] <= b[["Open", "Close"]].min(axis=1)).all()
    assert (b["n_members"] == 4).iloc[1:].all() and b["Volume"].iloc[100:].between(1e5, 1e7).all()
    assert G.basket_frame(frames, members[:2]) is None
    sub = G.basket_frame(frames, members, start="2024-01-01", end="2024-06-30")
    assert sub is not None and sub.index[0] >= pd.Timestamp("2024-01-01") and sub.index[-1] <= pd.Timestamp("2024-06-30")


def test_point_in_time_models_and_context():
    frames = _frames(n_groups=2, per_group=5, n=1300, seed=11)
    models = G.point_in_time_models(frames, [2027], lookback_years=3, per_group=5, min_clusters=2)
    m = models[2027]
    assert m["n"] == 10 and all(len(v) == 5 for v in m["groups"].values())
    b = G.basket_frame(frames, list(frames)[:5])
    cx = G.context_at(b, len(b) - 1)
    assert set(cx) == {"ret_126", "dist_ma200", "beaten"} and G.context_at(b, 10)["beaten"] is False
    rel, z = G._divergence_z(frames, "G0S4", [f"G0S{j}" for j in range(5)], frames["G0S4"].index[-1])
    assert np.isfinite(rel) and np.isfinite(z) and rel < -0.1 and z < -2


def test_condition_table_and_report(tmp_path):
    rng = np.random.default_rng(0)
    n = 200
    ev = pd.DataFrame({"symbol": ["X"] * n, "signal_date": pd.bdate_range("2021-01-04", periods=n).strftime("%Y-%m-%d"),
                       "year": [2021 + i // 100 for i in range(n)], "ret_20": rng.normal(0.01, 0.05, n), "xrand_20": rng.normal(0.005, 0.05, n),
                       "ret_126": -0.2, "dist_ma200": -0.1, "n_members": 5, "g_beaten": rng.random(n) < 0.5, "g_wedge_breakout": False,
                       "g_in_wedge": False, "share_beaten": rng.random(n), "co_signals": rng.integers(0, 3, n), "z_vs_group": rng.normal(0, 1.5, n)})
    t = G.condition_table(ev, "2022-01-01", {"group beaten down": ev["g_beaten"]})
    assert len(t) == 4 and t["n"].sum() == n and set(t["state"]) == {"yes", "no"}
    grp = pd.DataFrame({"signal_date": ["2021-03-01", "2023-03-01"], "ret_20": [0.02, -0.01], "xrand_20": [0.01, -0.02], "g_beaten": [True, True],
                        "share_beaten": [0.8, 0.2], "mem_ret_20": [0.015, -0.005], "mem_hit_20": [0.7, 0.4]})
    p = G.write_groups_report(tmp_path / "out", ev, grp, "2022-01-01", doc_path=tmp_path / "doc.md")
    text = p.read_text()
    assert "## 1. Confirmation by the group" in text and "## 2. The group as the instrument" in text and (tmp_path / "doc.md").exists()
    assert (tmp_path / "out" / "confirmation.csv").exists() and "beaten-down baskets" in text


def test_group_signals_today_runs():
    frames = _frames(n_groups=2, per_group=5, n=700, seed=5)
    model = {"groups": {"1": list(frames)[:5], "2": list(frames)[5:]}}
    out = G.group_signals_today(frames, model, DetectorConfig(filter_max_ret_126=None, filter_below_ma200=False))
    assert isinstance(out, list) and all(set(r) >= {"group", "status", "members", "share_beaten"} for r in out)
