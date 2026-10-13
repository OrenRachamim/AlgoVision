import numpy as np
import pandas as pd

from algovision.research import volume as V


def _frame(seed, n=400):
    r = np.random.default_rng(seed)
    c = 100 * np.cumprod(1 + r.normal(0, 0.01, n))
    v = r.integers(900_000, 1_100_000, n).astype(float)
    idx = pd.bdate_range("2024-01-01", periods=n)
    return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": v}, index=idx)


def test_volume_features_and_conditions():
    fr = {"AAA": _frame(1), "BBB": _frame(2)}
    idx = fr["AAA"].index
    fr["AAA"].loc[idx[300], "Volume"] = 6e6            # about a 6x day
    panel = {k: pd.DataFrame({s: f[k] for s, f in fr.items()}) for k in ("Open", "High", "Low", "Close", "Volume")}
    vc = V.volume_context(panel)
    expect = 6e6 / fr["AAA"]["Volume"].iloc[280:300].mean()     # prior 20 bars, the signal day excluded
    assert abs(vc["day"]["AAA"].iloc[300] - expect) < 1e-9
    assert vc["climax"]["AAA"].iloc[305] >= 3.0 and vc["climax"]["AAA"].iloc[311] < 3.0   # within 10 bars only
    ev = pd.DataFrame({"symbol": ["AAA", "AAA", "BBB", "ZZZ"], "date": [idx[300], idx[305], idx[300], idx[300]],
                       "ret_20": [0.01, 0.02, 0.0, 0.0], "xloc_20": [0.0, 0.0, 0.0, 0.0]})
    out = V.attach_volume(ev, vc)
    assert bool(out["c_vol_day_2_5"].iloc[0]) and bool(out["c_vol_day_5"].iloc[0])
    assert bool(out["c_vol_climax10"].iloc[1]) and not bool(out["c_vol_day_1_5"].iloc[1])
    assert not bool(out["c_vol_day_1_5"].iloc[2])
    assert not bool(out["vol_ok"].iloc[3]) and np.isnan(out["x_vol_day"].iloc[3])     # unknown symbol: no context, no condition
    b = V.volume_buckets(out)
    assert b["vol_day_bucket"].iloc[0] == "> 3x"
    assert V.volume_buckets(out, newsday=True)["vol_day_bucket"].iloc[0] == "5-8x" or V.volume_buckets(out, newsday=True)["vol_day_bucket"].iloc[0] == "> 8x"


def test_lowday_ratio_picks_the_low_close():
    c = np.array([5, 4, 3, 2, 1, 2, 3, 4, 5, 6.0])
    r = np.arange(10, dtype=float)
    lr = V._lowday_ratio(c, r, 5)
    assert np.isnan(lr[3]) and lr[4] == 4 and lr[8] == 4 and lr[9] == 5


def test_volume_report_writes(tmp_path):
    rng = np.random.default_rng(3)
    n = 400
    dates = pd.to_datetime(rng.choice(pd.bdate_range("2018-01-01", "2026-01-01"), n))
    ev = pd.DataFrame({"symbol": rng.choice(["A", "B", "C"], n), "date": dates, "ret_20": rng.normal(0.01, 0.05, n),
                       "ret_60": rng.normal(0.02, 0.08, n), "xloc_20": rng.normal(0, 0.05, n), "xloc_60": rng.normal(0, 0.08, n),
                       "vol_ok": True, "x_vol_day": rng.lognormal(0, 0.5, n), "x_vol_climax10": rng.lognormal(0.5, 0.5, n),
                       "x_vol_5d": 1.0, "x_vol_lowday": 1.0, "x_vol_upshare": 0.5})
    for c in V.VOL_NAMES:
        ev[c] = rng.random(n) < 0.4
    p = V.write_volume_report(tmp_path, "2023-01-01", {"fam": {"events": ev, "ret_col": "ret", "x_col": "xloc", "date_col": "date", "slug": "fam"}})
    text = p.read_text(encoding="utf-8")
    assert "## Verdicts" in text and "Signal-day volume" in text and (tmp_path / "fam_volume_findings.csv").exists()


def test_volume_at_last_bar_and_breakout_bar():
    df = _frame(5)
    df.loc[df.index[390], "Volume"] = 7e6
    last = V.volume_at(df)                       # the last bar: the spike sits inside the last 10 bars
    assert last["climax10"] >= 3.0 and 0 < last["day"] < 1.5
    at = V.volume_at(df, 390)
    assert at["day"] >= 5.0
    assert all(np.isnan(x) for x in V.volume_at(df.iloc[:10]).values())     # too short


def test_base_events_and_direction_table():
    rng = np.random.default_rng(9)
    n = 700
    idx = pd.bdate_range("2023-01-02", periods=n)
    c = np.r_[100 * np.cumprod(1 + rng.normal(0.0002, 0.004, 300)), None][:300].astype(float)
    down = c[-1] * np.cumprod(1 + rng.normal(-0.004, 0.006, 150))          # a decline
    base = down[-1] * (1 + rng.normal(0, 0.004, 250)).cumprod() ** 0.1       # then a flat, tight range
    close = np.r_[c, down, base]
    v = rng.integers(900_000, 1_100_000, n).astype(float)
    v[520:] *= 1.6                                                            # volume rises in the base
    df = pd.DataFrame({"Open": close, "High": close * 1.003, "Low": close * 0.997, "Close": close, "Volume": v}, index=idx)
    panel = {k: pd.DataFrame({"AAA": df[k], "BBB": df[k] * 2}) for k in ("Open", "High", "Low", "Close", "Volume")}
    vc = V.volume_context(panel)
    assert bool(vc["base"]["AAA"].iloc[480:600].any())
    spy = pd.Series(np.linspace(100, 120, n), index=idx)
    ev = V.base_events(vc, spy)
    assert len(ev) and {"ret_20", "xloc_60", "up_20", "down_60", "base_vol_bucket"} <= set(ev.columns)
    t = V.base_direction_table(ev, "2024-06-01")
    assert len(t) and (t["up_20"] + t["down_20"] <= 1.0 + 1e-9).all()
