import numpy as np
import pandas as pd

from algovision.research import rally as R

COLS = ("Open", "High", "Low", "Close", "Volume")


def _frame(close: np.ndarray, vol_spike_at=None) -> pd.DataFrame:
    n = len(close)
    idx = pd.bdate_range("2020-01-01", periods=n)
    o = np.r_[close[0], close[:-1]]
    h = np.maximum(o, close) * 1.005
    l = np.minimum(o, close) * 0.995
    v = np.full(n, 1_000_000.0)
    if vol_spike_at is not None:
        v[vol_spike_at] = 3_000_000.0
    return pd.DataFrame({"Open": o, "High": h, "Low": l, "Close": close, "Volume": v}, index=idx)


def _arrays(df):
    return tuple(df[x].to_numpy() for x in COLS)


def _decline_then_rise(n_down=400, n_up=80, start=100.0, bottom=60.0, top_mult=1.8):
    """A 400-bar slide to 60, then a steep rise (about +1%/bar) to 108."""
    down = np.linspace(start, bottom, n_down)
    up = np.linspace(bottom, bottom * top_mult, n_up)
    return np.r_[down, up]


def _first_breakout_bar(df):
    h, c = df["High"].to_numpy(), df["Close"].to_numpy()
    hi60 = pd.Series(h).rolling(60).max().shift(1).to_numpy()
    return int(np.where((c > hi60) & np.r_[False, (c[:-1] <= hi60[:-1])])[0][0])


def test_turn_rules_fire_once_shortly_after_the_bottom():
    c = _decline_then_rise()
    o, h, l, cl, v = _arrays(_frame(c))
    cross = R.rule_hits("ma50_cross", o, h, l, cl, v)
    assert len(cross) == 1 and 400 < cross[0] < 430
    rsi = R.rule_hits("rsi_turn", o, h, l, cl, v)
    assert len(rsi) == 1 and 400 < rsi[0] < 420
    th = R.rule_hits("thrust", o, h, l, cl, v)
    assert len(th) >= 1 and 405 <= th[0] <= 415            # +8% in 10 bars from the 60-bar low
    gc = R.rule_hits("golden_20_50", o, h, l, cl, v)
    assert len(gc) == 1 and gc[0] > cross[0]               # the MA cross comes after the price cross
    assert len(R.rule_hits("ma50_cross", *_arrays(_frame(np.linspace(50, 150, 600))))) == 0   # a straight uptrend never "turns"


def test_base_breakout_needs_volume_and_room_below_the_high():
    c = _decline_then_rise()
    df = _frame(c)
    t = _first_breakout_bar(df)
    assert len(R.rule_hits("base_breakout", *_arrays(df))) == 0          # no volume -> no signal
    hits = R.rule_hits("base_breakout", *_arrays(_frame(c, vol_spike_at=t)))
    assert list(hits) == [t]
    # a stock making the breakout within 10 % of its 52-week high is a trend extension, not a base breakout
    c2 = np.r_[np.linspace(100, 95, 400), np.linspace(95, 150, 80)]
    df2 = _frame(c2)
    t2 = _first_breakout_bar(df2)
    hits2 = R.rule_hits("base_breakout", *_arrays(_frame(c2, vol_spike_at=t2)))
    assert t2 not in hits2


def test_higher_high_dow_turn():
    # 300 bars down to 60, a bounce to 70, a higher low at 65, then a close above 70
    c = np.r_[np.linspace(100, 60, 300), np.linspace(60, 70, 15), np.linspace(70, 65, 10), np.linspace(65, 75, 20)]
    hits = R.rule_hits("higher_high", *_arrays(_frame(c)))
    assert len(hits) == 1 and 325 <= hits[0] <= 345
    # no higher low (the pullback undercuts the first low) -> no signal
    c2 = np.r_[np.linspace(100, 60, 300), np.linspace(60, 70, 15), np.linspace(70, 58, 10), np.linspace(58, 75, 20)]
    assert len(R.rule_hits("higher_high", *_arrays(_frame(c2)))) == 0


def test_events_table_and_live_scan():
    c = _decline_then_rise()
    t = _first_breakout_bar(_frame(c))
    frames = {"AAA": _frame(c, vol_spike_at=t), "BBB": _frame(c * 2, vol_spike_at=t)}
    panel = {k: pd.DataFrame({s: f[k] for s, f in frames.items()}) for k in COLS}
    spy = pd.Series(np.linspace(300, 330, len(c)), index=frames["AAA"].index)
    ev = R.rally_events(panel, spy, horizons=(5, 20))
    assert set(ev["symbol"]) == {"AAA", "BBB"} and {"ma50_cross", "rsi_turn", "thrust", "base_breakout"} <= set(ev["rule"])
    assert (ev["ret_20"] > 0).all()
    assert ev[ev["rule"] != "golden_20_50"]["beaten"].all()        # the MA cross comes late, when the 6-month return has recovered
    tab = R.rally_table(ev, "2021-06-01", horizons=(5, 20), min_n=1)
    assert ("all", "ma50_cross") in tab.index and tab.loc[("all", "ma50_cross"), "n"] == 2
    assert "passes" in R.verdicts(tab).columns
    cmb = R.combined_events(ev, gap_days=30)
    assert set(cmb["symbol"]) == {"AAA", "BBB"} and (cmb["rule"] == "any turn rule").all() and len(cmb) == 2
    assert cmb["n_rules"].min() >= 1 and cmb["rules"].str.contains("rsi_turn").all()
    ct = R.combined_table(cmb, "2021-06-01", horizons=(5, 20))
    assert ct.empty or "set" in ct.columns                           # fewer than 30 events: no rows, no crash
    tr = R.rule_hits("rsi_turn", *_arrays(frames["AAA"]))[0]
    live = R.early_rally_signals({"AAA": frames["AAA"].iloc[: tr + 2], "BBB": frames["BBB"].iloc[:200]}, ["AAA", "BBB"], max_age=3)
    assert list(live["symbol"]) == ["AAA"] and live["bars_ago"].iloc[0] == 1 and "rsi_turn" in live["rules"].iloc[0]
    # live scan: a frame whose last bar is the MA50 cross
    tc = R.rule_hits("ma50_cross", *_arrays(frames["AAA"]))[0]
    sig = R.rally_signals({"AAA": frames["AAA"].iloc[: tc + 1]}, ["AAA"], max_age=1)
    assert list(sig["rule"]).count("ma50_cross") == 1 and sig["bars_ago"].min() == 0 and bool(sig["beaten"].iloc[0])
    assert R.rally_signals({"AAA": frames["AAA"].iloc[:200]}, ["AAA"]).empty
