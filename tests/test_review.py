import json

import numpy as np
import pandas as pd

from algovision import review as R


def _frame(n=400, seed=1):
    r = np.random.default_rng(seed)
    c = 100 * np.cumprod(1 + r.normal(0.0005, 0.01, n))
    idx = pd.bdate_range("2025-01-01", periods=n)
    return pd.DataFrame({"Open": c, "High": c * 1.01, "Low": c * 0.99, "Close": c, "Volume": 1e6}, index=idx)


def _report(date, syms_wedge, syms_briefs, flags):
    tv = lambda s: f"[{s}](https://www.tradingview.com/chart/?symbol={s})"
    lines = [f"# AlgoVision daily report - {date}", "", "## 2. Short-horizon signals", "",
             "### Falling Wedge in beaten-down stocks (confirmed = ...)", "",
             "| symbol | days listed | score | 6m | volume | group |", "|:--|--:|--:|:--|:--|:--|"]
    for s in syms_wedge:
        lines.append(f"| {tv(s)} | 1 | 0.7 | -20% | 1.8x | beaten (60%) |")
    lines += ["", "## 3. Stock briefs (one per name in the tables above)", "", "### Checklist: the names passing the most checks today", "",
              "| symbol | in tables | checks passed |", "|:--|:--|:--|"]
    for s in syms_briefs[:2]:
        lines.append(f"| {tv(s)} | falling wedge | 4/5 |")
    lines += ["", "### Summary table", "", "| symbol | in tables | read | score | flags | why fell | sentiment | last | from 52w high | vs MA50 | vs peers 20d | consensus | target upside |",
              "|:--|:--|:--|--:|:--|:--|:--|--:|:--|:--|:--|:--|:--|"]
    for s, f in zip(syms_briefs, flags):
        lines.append(f"| {tv(s)} | falling wedge | undecided | 1 | {f} | earnings, market-wide | positive | 50.00 | -25% | +1% | +1.0% (z +0.5) | buy | +20% |")
    return "\n".join(lines) + "\n"


def test_review_end_to_end(tmp_path):
    syms = [f"S{i:02d}" for i in range(30)]
    frames = {s: _frame(seed=i) for i, s in enumerate(syms)}
    frames["SPY"] = _frame(seed=99)
    dates = [str(d.date()) for d in pd.bdate_range("2025-06-02", periods=6, freq="5B")]
    for k, d in enumerate(dates):
        batch = syms[k * 5:(k + 1) * 5]
        (tmp_path / f"report_{d}.md").write_text(_report(d, batch, batch, ["", "Z", "", "S T", ""]), encoding="utf-8")
    pd.DataFrame({"logged": dates[:3], "rule": ["falling_wedge_beaten_down"] * 3, "symbol": syms[:3], "signal_date": dates[:3], "status": ["closed"] * 3,
                  "ref_price": [1.0] * 3, "entry_date": dates[:3], "entry_price": [1.0] * 3, "hold_bars": [20] * 3, "note": [""] * 3, "bars_elapsed": [20] * 3,
                  "last_price": [1.02] * 3, "ret": [0.02, -0.01, 0.03], "done": [True] * 3, "spy_ret": [0.0] * 3, "basket_ret": [0.0] * 3}).to_csv(tmp_path / "mark_to_market.csv", index=False)
    en, he, res = R.write_review(tmp_path, frames, frames["SPY"], today="2025-09-01")
    assert en.exists() and he.exists() and (tmp_path / "review_latest.md").exists() and (tmp_path / "review_he_latest.md").exists()
    text = en.read_text(encoding="utf-8")
    assert "## Bottom line" in text and "## By table (20 bars)" in text and "## By condition" in text and "falling wedge (confirmed)" in text
    assert "First review" in text
    t = {x["section"]: x for x in res["tables"]}
    assert t["wedge"]["n"] == 30 and t["wedge"]["verdict"] in ("works", "fails", "noise", "early")
    keys = {c["key"] for c in res["conditions"]}
    assert {"flag_Z", "no_warning", "market_wide", "sent_pos", "fresh", "group_beaten"} <= keys
    j = {x["rule"]: x for x in res["journal"]}
    assert j["falling_wedge_beaten_down"]["closed"] == 3 and j["falling_wedge_beaten_down"]["verdict"] == "early"
    prev = json.loads((tmp_path / "review_latest.json").read_text(encoding="utf-8"))
    assert prev["date"] == "2025-09-01" and len(prev["tables"]) == len(res["tables"])
    # a second run compares with the first
    en2, _, res2 = R.write_review(tmp_path, frames, frames["SPY"], today="2025-09-03")
    assert "since the previous review" in en2.read_text(encoding="utf-8") and "2025-09-01" in en2.read_text(encoding="utf-8")
    he_text = he.read_text(encoding="utf-8")
    assert "## השורה התחתונה" in he_text and "לפי טבלה" in he_text


def test_verdict_rules():
    assert R.table_verdict({"n_h": 5, "xbk": 0.05, "t_xbk": 3.0}) == "early"
    assert R.table_verdict({"n_h": 25, "xbk": 0.02, "t_xbk": 2.5}) == "works"
    assert R.table_verdict({"n_h": 25, "xbk": -0.02, "t_xbk": -2.5}) == "fails"
    assert R.table_verdict({"n_h": 25, "xbk": 0.01, "t_xbk": 0.8}) == "noise"
    assert R.split_verdict({"n_yes": 5, "n_no": 40, "t": 4.0}) == "early"
    assert R.split_verdict({"n_yes": 15, "n_no": 40, "t": 2.4}) == "better_yes"
    assert R.split_verdict({"n_yes": 15, "n_no": 40, "t": -2.4}) == "better_no"
    assert R.split_verdict({"n_yes": 15, "n_no": 40, "t": 0.3}) == "noise"
