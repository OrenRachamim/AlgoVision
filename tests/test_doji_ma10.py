import numpy as np
import pandas as pd

from algovision.research import doji_ma10 as D


def _frame(n=400, seed=3):
    r = np.random.default_rng(seed)
    c = 100 * np.cumprod(1 + r.normal(0.0003, 0.012, n))
    o = c * (1 + r.normal(0, 0.004, n))
    h = np.maximum(o, c) * (1 + np.abs(r.normal(0, 0.006, n)))
    l = np.minimum(o, c) * (1 - np.abs(r.normal(0, 0.006, n)))
    idx = pd.bdate_range("2024-01-01", periods=n)
    return pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": c, "Volume": 1e6}, index=idx)


def test_doji_and_ma10_masks():
    df = _frame()
    # plant a textbook doji sitting on the MA10 at bar 100
    ma = df["Close"].rolling(10).mean()
    t = 100
    df.iloc[t, df.columns.get_loc("Open")] = ma.iloc[t] * 1.0005
    df.iloc[t, df.columns.get_loc("Close")] = ma.iloc[t] * 0.9995
    df.iloc[t, df.columns.get_loc("High")] = ma.iloc[t] * 1.02
    df.iloc[t, df.columns.get_loc("Low")] = ma.iloc[t] * 0.98
    ma = df["Close"].rolling(10).mean()  # the planted close moves the MA a little; the line is still inside the 4% range
    dm, om = D.doji_mask(df), D.on_ma10_mask(df)
    assert dm[t] and om[t] and D.on_ma10_mask(df, D.STRICT_TOL)[t]
    # a wide-bodied candle is not a doji, a candle far from the line is not on it
    df2 = df.copy()
    df2.iloc[t, df2.columns.get_loc("Open")] = ma.iloc[t] * 0.985
    assert not D.doji_mask(df2)[t]
    df3 = df.copy()
    df3.iloc[t, df3.columns.get_loc("Low")] = ma.iloc[t] * 1.005
    df3.iloc[t, df3.columns.get_loc("High")] = ma.iloc[t] * 1.03
    df3.iloc[t, [df3.columns.get_loc("Open"), df3.columns.get_loc("Close")]] = ma.iloc[t] * 1.01
    assert not D.on_ma10_mask(df3)[t]


def test_events_summary_and_report(tmp_path):
    frames = {f"S{i}": _frame(seed=i) for i in range(12)}
    spy = _frame(seed=99)["Close"]
    ev = D.doji_on_ma10_events(frames, spy)
    assert len(ev) > 20 and {"ret_1", "ret_5", "ret_21", "oret_5", "xloc_21", "xspy_1", "on_line", "ma10_slope", "from_above"} <= set(ev.columns)
    # forward returns are measured from the doji's close
    e = ev.iloc[0]
    df = frames[e["symbol"]]
    t = df.index.get_loc(e["date"])
    assert abs(e["ret_5"] - (df["Close"].iloc[t + 5] / df["Close"].iloc[t] - 1)) < 1e-12
    assert abs(e["oret_1"] - (df["Close"].iloc[t + 1] / df["Open"].iloc[t + 1] - 1)) < 1e-12
    # at most one event per stock per 5 bars
    for s, g in ev.groupby("symbol"):
        pos = [df.index.get_loc(d) for d in g["date"]] if (df := frames[s]) is not None else []
        assert all(b - a >= D.MIN_GAP for a, b in zip(pos, pos[1:]))
    summ = D.summarise(ev)
    assert summ.iloc[0]["group"] == "all" and summ.iloc[0]["n"] == len(ev) and 0 <= summ.iloc[0]["hit_21"] <= 1
    base = D.base_rates(frames, ev["date"].min(), ev["date"].max())
    assert base["n"] > len(ev) and np.isfinite(base["ret_21"])
    p = D.write_doji_report(tmp_path / "doji.md", frames, spy, split="2025-01-01", out_dir=tmp_path / "out", window=120)
    text = p.read_text(encoding="utf-8")
    assert "## Verdict" in text and "by context" in text and "Sensitivity" in text and "By year" in text
    assert (tmp_path / "out" / "doji_ma10_events.csv").exists() and (tmp_path / "out" / "doji_ma10_context_control.csv").exists()
    ctx = D.context_base_rates(frames, ev["date"].min(), ev["date"].max())
    assert ctx.iloc[0]["group"] == "all" and ctx.iloc[0]["n (any day)"] > ctx.iloc[0]["n (doji)"] > 0 and "Control" in text


def test_verdict_rule():
    def s(x, n=40):
        return pd.DataFrame([{"group": "all", "n": n, "xloc_21": x, "hit_21": 0.55, "ret_21": 0.01}])
    assert D.verdict(s(0.01), s(0.008), s(0.006))["passed"] and D.verdict(s(0.01), s(0.008), s(0.006))["direction"] == "up"
    assert D.verdict(s(-0.01), s(-0.008), s(-0.006))["direction"] == "down"
    assert not D.verdict(s(0.01), s(-0.008), s(0.006))["passed"]
    assert not D.verdict(s(0.01, n=10), s(0.008), s(0.006))["passed"]


def test_weekly_resample_and_report(tmp_path):
    df = _frame(n=600, seed=5)
    w = D.to_weekly(df)
    assert len(w) > 100 and (w["High"] >= w[["Open", "Close"]].max(axis=1)).all() and (w["Low"] <= w[["Open", "Close"]].min(axis=1)).all()
    first_week = df.loc[: w.index[0]]
    assert w["Open"].iloc[0] == first_week["Open"].iloc[0] and w["Close"].iloc[0] == first_week["Close"].iloc[-1]
    # a frame ending mid-week drops the unfinished week
    cut = df.iloc[:-2] if df.index[-1].weekday() == 4 else df
    assert D.to_weekly(cut).index[-1] < cut.index[-1] or cut.index[-1].weekday() == 4
    frames = {f"S{i}": _frame(n=1500, seed=20 + i) for i in range(15)}
    spy = _frame(n=1500, seed=98)["Close"]
    p = D.write_doji_report(tmp_path / "w.md", frames, spy, split="2027-01-01", out_dir=tmp_path / "w", weekly=True)
    text = p.read_text(encoding="utf-8")
    assert "weekly bars" in text and "12 weeks" in text and "Last 52 weeks" in text
    ev = pd.read_csv(tmp_path / "w" / "doji_ma10_events.csv")
    assert {"ret_1", "ret_4", "ret_12", "xloc_12"} <= set(ev.columns) and "ret_21" not in ev.columns
