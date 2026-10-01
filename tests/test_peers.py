import json

import numpy as np
import pandas as pd

from algovision import peers as P


def _frames(n_groups=3, per_group=6, n=900, seed=3):
    """Synthetic universe: a market factor, a strong group factor per group, idiosyncratic noise. The last stock of
    group 0 is pushed 25% below its group over the final 20 days."""
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range("2023-01-02", periods=n)
    mkt = rng.normal(0, 0.01, n)
    frames = {}
    for g in range(n_groups):
        fac = rng.normal(0, 0.012, n)
        for j in range(per_group):
            r = 0.9 * mkt + fac + rng.normal(0, 0.006, n)
            if g == 0 and j == per_group - 1:
                r[-20:] -= 0.0125
            close = 100 * np.exp(np.cumsum(r))
            frames[f"G{g}S{j}"] = pd.DataFrame({"Open": close, "High": close * 1.01, "Low": close * 0.99, "Close": close,
                                                "Volume": 1e6 + 1e5 * j}, index=idx)
    return frames


def test_groups_and_divergence(tmp_path):
    frames = _frames()
    model = P.build_groups(frames, per_group=6, min_clusters=3)
    assert model["n"] == 18 and model["k"] == 3
    groups = {tuple(sorted(m)) for m in model["groups"].values()}
    assert groups == {tuple(f"G{g}S{j}" for j in range(6)) for g in range(3)}
    me = model["symbols"]["G0S5"]
    assert {s for s, _ in me["peers"]} <= {f"G0S{j}" for j in range(5)} and me["group_corr"] > 0.5
    (tmp_path / "peers.json").write_text(json.dumps(model))      # the weekly cache; load_peers reads it and adds today's divergence
    ctx = P.load_peers(frames, tmp_path, symbols=["G0S5", "G1S0"])
    d = ctx["G0S5"]
    assert d["n_group"] == 6 and d["rel20"] < -0.15 and d["z"] is not None and d["z"] < -2
    assert d["ret20"] < d["group_ret20"] and len(d["top"]) == 4 and "G0S5" not in d["top"]
    assert abs(ctx["G1S0"]["z"]) < 2
    # the cached model is reused, the divergence recomputed
    again = P.load_peers(frames, tmp_path, symbols=["G0S5"])
    assert again["G0S5"]["peers"] == d["peers"]
    en = "\n".join(P.peers_markdown(d, "en"))
    he = "\n".join(P.peers_markdown(d, "he"))
    assert en.startswith("**Peers and group.**") and "unusually far below its peers" in en and "group of 6 stocks" in en
    assert he.startswith("### עמיתים וקבוצת ההשוואה") and "חריג כלפי מטה" in he
    assert P.peers_short(d).startswith("-") and "(z -" in P.peers_short(d) and P.peers_short(None) == ""


def test_signal_in_verdict():
    from algovision import briefs as B
    from tests.test_briefs import _profile

    prof = _profile()
    an, ea, fu = B.analyst_view(prof), B.earnings_view(prof), B.fundamentals_view(prof)
    ctx = {"dist_ma50": 0.01, "ma50_rising": True, "higher_low": False, "new_low_5d": False}
    _, s0, f0 = B.verdict_signals(ctx, an, ea, fu)
    _, s1, f1 = B.verdict_signals(ctx, an, ea, fu, peers={"z": -2.4})
    assert s1 == s0 + 0.5 and [c for c, _, _ in f1 if c == "peer_oversold"] and not [c for c, _, _ in f0 if c == "peer_oversold"]
    assert "z -2.4" in B.render_signals(f1)[-1]
