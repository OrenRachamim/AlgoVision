import numpy as np
import pandas as pd

from algovision import lookback as L
from algovision.checklist import checklist_markdown, checklist_rows

TV = "https://www.tradingview.com/chart/?symbol="


def _frame(n=320, drift=0.0, seed=0):
    rng = np.random.default_rng(seed)
    close = 100 * np.cumprod(1 + rng.normal(drift, 0.01, n))
    idx = pd.bdate_range("2025-06-02", periods=n)
    o = np.r_[close[0], close[:-1]]
    return pd.DataFrame({"Open": o, "High": np.maximum(o, close) * 1.004, "Low": np.minimum(o, close) * 0.996, "Close": close,
                         "Volume": np.full(n, 1e6)}, index=idx)


def _report(date, wedge_status="forming"):
    return (f"# AlgoVision daily report - {date}\n\n## 2. Short-horizon signals\n\n### News-day rule (x)\n\n"
            f"| symbol | news_date | gap |\n|:--|:--|--:|\n| [AAA]({TV}AAA) | {date} | -6.0% |\n\n"
            f"### Falling Wedge in beaten-down stocks (x)\n\n| symbol | status | score |\n|:--|:--|--:|\n| [BBB]({TV}BBB) | {wedge_status} | 0.7 |\n\n"
            f"## 3. Stock briefs (one per name)\n\n| symbol | in tables | read | score | why fell | sentiment | from 52w high | vs peers 20d | target upside |\n"
            f"|:--|:--|:--|--:|:--|:--|:--|:--|:--|\n"
            f"| [AAA]({TV}AAA) | news-day | signs of a bottom | 4 | earnings, market-wide | positive | -20% | +1.0% (z +0.3) | +20% |\n"
            f"| [BBB]({TV}BBB) | falling wedge | undecided | 1 | earnings | negative | -45% | -8.0% (z -1.4) | +60% |\n\n"
            f"### AI decisions (Jev)\n\n| symbol | action | P(buy) |\n|:--|:--|--:|\n| [AAA]({TV}AAA) | buy | 0.70 |\n")


def test_events_forward_and_scorecard(tmp_path):
    for d in ("2026-06-01", "2026-06-02", "2026-06-03"):       # 250+ bars into the synthetic frames, so the beaten-down basket exists
        (tmp_path / f"report_{d}.md").write_text(_report(d, "confirmed" if d == "2026-06-03" else "forming"), encoding="utf-8")
    ev = L.events(tmp_path)
    assert set(ev["section"]) == {"newsday", "wedge_watch", "wedge", "briefs", "jev"}
    first = ev[(ev.section == "newsday") & (ev.symbol == "AAA")].iloc[0]
    assert first["date"] == "2026-06-01" and first["n_days"] == 3
    bbb = ev[(ev.section == "briefs") & (ev.symbol == "BBB")].iloc[0]
    assert set(bbb["flags"].split()) == {"Z", "D", "S", "T"} and bbb["n_flags"] == 4
    aaa = ev[(ev.section == "briefs") & (ev.symbol == "AAA")].iloc[0]
    assert aaa["n_flags"] == 0 and bool(aaa["market_wide"])
    frames = {"AAA": _frame(seed=1), "BBB": _frame(drift=-0.003, seed=2), **{f"X{i}": _frame(drift=-0.003, seed=10 + i) for i in range(4)}}
    spy = _frame(seed=5)
    F = L.forward(ev, frames, spy)
    assert len(F) == len(ev) and F["ret_5"].notna().all() and F["bk_5"].notna().all()
    rows = L.scorecard(F, min_n=1)
    groups = {r["group"] for r in rows}
    assert {"table", "briefs", "flags", "flag", "read", "cause", "days", "jev"} <= groups
    md = "\n".join(L.lookback_markdown(rows, F, "en"))
    assert "What has worked so far" in md and "falling wedge (confirmed)" in md and "vs basket" in md
    he = "\n".join(L.lookback_markdown(rows, F, "he"))
    assert "מה עבד עד עכשיו" in he and "מול הסל" in he
    res = L.run_lookback(tmp_path, frames, spy)
    assert (tmp_path / "lookback.csv").exists() and len(res["forward"]) == len(ev)     # rows need min_n names per group


def test_checklist():
    rows = [{"symbol": "AAA", "tables": "news-day", "read": "signs of a bottom", "score": 4.0, "why fell": "earnings, market-wide", "flags": [], "sentiment": "positive"},
            {"symbol": "BBB", "tables": "falling wedge", "read": "undecided", "score": 1.0, "why fell": "earnings", "flags": ["Z"], "sentiment": "negative"},
            {"symbol": "CCC", "tables": ["falling wedge (forming)"], "read": "signs of a bottom", "score": 5.0, "why fell": "market-wide", "flags": [], "sentiment": "mixed"},
            {"symbol": "DDD", "tables": "early rally", "read": "undecided", "score": 0.5, "why fell": "guidance", "flags": [], "sentiment": "mixed"}]
    ck = checklist_rows(rows)
    assert [d["symbol"] for d in ck] == ["AAA", "DDD"]           # BBB has a flag, CCC is only on the watch list
    assert ck[0]["passes"] == 4 and ck[1]["passes"] == 2
    en = "\n".join(checklist_markdown(rows, "en", True))
    assert "Checklist" in en and "Regime against" in en and "4/4" in en
    he = "\n".join(checklist_markdown(rows, "he", False, anchor=lambda s: "s-" + s.lower()))
    assert "רשימת הבדיקות" in he and "[פירוט](#s-aaa)" in he and "המשטר נגד" not in he
    assert "No name passes" in "\n".join(checklist_markdown([], "en"))
