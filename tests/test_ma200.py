import numpy as np
import pandas as pd

from algovision import ma200 as M


def _frame(n=600, seed=1, cross_at=None, run=150):
    """A random walk; with ``cross_at`` the closes sit below the 200-day MA for ``run`` bars and cross above at that position."""
    r = np.random.default_rng(seed)
    idx = pd.bdate_range("2023-01-02", periods=n)
    if cross_at is None:
        c = 100 * np.cumprod(1 + r.normal(0, 0.004, n))
    else:
        c = 100 * (1.0005 ** np.arange(n)) * (1 + r.normal(0, 0.001, n))     # a slow uptrend: the close sits above its 200-day MA
        lo = cross_at - run
        c[lo:cross_at] = c[lo - 1] * 0.85 * (1 + r.normal(0, 0.001, cross_at - lo))     # a flat stretch well below the line
        c[cross_at:] = c[cross_at - 1] * 1.25                                               # the jump above the line
    v = r.integers(900_000, 1_100_000, n).astype(float)
    return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": v}, index=idx)


def test_cross_points_and_run_length():
    df = _frame(cross_at=500, run=150)
    cp = M.cross_points(df["Close"], min_below=120)
    assert len(cp) >= 1
    last = cp.iloc[-1]
    assert int(last["pos"]) == 500 and int(last["bars_below"]) >= 120
    # a short run does not qualify at the default threshold
    short = _frame(seed=2, cross_at=500, run=40)
    assert not len(M.cross_points(short["Close"], min_below=120)[lambda d: d["pos"] == 500])


def test_signals_table():
    frames = {"AAA": _frame(cross_at=598, run=150), "BBB": _frame(seed=3), "CCC": _frame(seed=4, cross_at=400, run=150)}
    out = M.ma200_cross_signals(frames, list(frames), max_age=3, min_below=120)
    assert list(out["symbol"]) == ["AAA"]            # CCC crossed too long ago, BBB never after a long run
    row = out.iloc[0]
    assert row["bars_ago"] == 1 and row["bars_below"] >= 120 and row["dist_ma200"] > 0
    assert set(["below_since", "day_ret", "ret_10", "ret_6m", "from_52w_high", "dist_ma50", "volume_ratio", "last", "ma200"]) <= set(out.columns)
    assert M.ma200_cross_signals({}, [], max_age=3).empty


def test_study_summary_verdict_and_report(tmp_path):
    frames = {f"S{i}": _frame(n=900, seed=10 + i, cross_at=300 + 40 * (i % 5), run=130 + 10 * i) for i in range(8)}
    spy = _frame(n=900, seed=99)["Close"]
    ev = M.ma200_cross_study(frames, spy, min_below=60)
    assert len(ev) and {"ret_20", "ret_60", "xspy_20", "xloc_20", "run_bucket", "bars_below"} <= set(ev.columns)
    summ = M.ma200_summary(ev, "2024-01-01")
    assert len(summ) and {"bucket", "period", "n", "xloc_20", "t_20"} <= set(summ.columns)
    v = M.verdict(summ)
    assert "passed" in v
    doc = M.write_ma200_report(tmp_path / "doc.md", ev, "2024-01-01", out_dir=tmp_path / "out")
    text = doc.read_text(encoding="utf-8")
    assert "## Verdict" in text and "## By run length and period" in text and (tmp_path / "out" / "ma200_summary.csv").exists()


def test_heading_notes_quote_the_backtest():
    en, he = M.heading_note(M.BACKTEST), M.heading_note_he(M.BACKTEST)
    assert en.startswith("no tested edge") and "n 446 / 361" in en and "hit 54% / 52%" in en
    assert he.startswith("אין יתרון שנבדק") and "n 446 / 361" in he
    assert M.heading_note({}) == "not backtested yet"
