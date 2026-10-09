import numpy as np
import pandas as pd

from algovision import regime as R


def _frame(n=320, drift=0.0, seed=0, start=100.0):
    rng = np.random.default_rng(seed)
    close = start * np.cumprod(1 + rng.normal(drift, 0.01, n))
    idx = pd.bdate_range("2025-06-02", periods=n)
    o = np.r_[close[0], close[:-1]]
    return pd.DataFrame({"Open": o, "High": np.maximum(o, close) * 1.004, "Low": np.minimum(o, close) * 0.996, "Close": close,
                         "Volume": np.full(n, 1e6)}, index=idx)


def test_beaten_mask_and_basket_return():
    frames = {"DOWN": _frame(drift=-0.003, seed=1), "UP": _frame(drift=0.003, seed=2), "FLAT": _frame(seed=3)}
    o, c = R.build_panels(frames)
    last = len(c) - 1
    m = R.beaten_mask(c, last)
    assert bool(m["DOWN"]) and not bool(m["UP"])
    r = R.basket_return(o, c, ["DOWN", "UP"], last - 20, last)
    expect = np.mean([c["DOWN"].iloc[last] / o["DOWN"].iloc[last - 20] - 1, c["UP"].iloc[last] / o["UP"].iloc[last - 20] - 1])
    assert abs(r - expect) < 1e-12
    assert np.isnan(R.basket_return(o, c, [], last - 20, last))


def test_regime_stats_and_markdown_warning():
    frames = {f"D{i}": _frame(drift=-0.004, seed=10 + i) for i in range(5)}
    frames.update({f"U{i}": _frame(drift=0.003, seed=20 + i) for i in range(5)})
    spy = _frame(drift=0.0005, seed=99, start=500)
    st = R.regime_stats(frames, spy)
    assert st["n_symbols"] == 10 and 0 < st["share_beaten"] <= 1
    assert st["basket_20"] < 0 and st["warning"] is True
    en = "\n".join(R.regime_markdown(st, "en"))
    he = "\n".join(R.regime_markdown(st, "he"))
    assert "against the wind" in en and "Breadth" in en
    assert "נגד הרוח" in he and "רוחב" in he
    st["warning"] = False
    assert "against the wind" not in "\n".join(R.regime_markdown(st, "en"))
