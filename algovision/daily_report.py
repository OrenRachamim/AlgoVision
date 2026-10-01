"""One-file daily report: insider buying, short-horizon signals, one research brief per listed stock, forward-test results.

Designed to run right after ``journal`` (which refreshes prices and EDGAR filings), from cache except the
per-stock briefs (analysts, estimates, news from Yahoo Finance, cached for a day), and to be pasted / translated verbatim by the scheduled routine.
"""

from __future__ import annotations

import datetime as dt
import os
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.data.provider import DataProvider, _DEFAULT_CACHE
from algovision.data.universe import get_universe, load_snapshot
from algovision.links import tv


# where the committed files can be read (the journal directory is pushed after every run)
REPORT_URL = os.environ.get("ALGOVISION_REPORT_URL", "https://github.com/OrenRachamim/AlgoVision/blob/claude/stock-pattern-detection-b94x35/journal/report_{date}.md")
BRIEFS_URL = os.environ.get("ALGOVISION_BRIEFS_URL", "https://github.com/OrenRachamim/AlgoVision/blob/claude/stock-pattern-detection-b94x35/journal/briefs_{date}.md")
# the one-rule Hebrew file for the falling wedge (same directory, same push)
WEDGE_URL = os.environ.get("ALGOVISION_WEDGE_URL", "https://github.com/OrenRachamim/AlgoVision/blob/claude/stock-pattern-detection-b94x35/journal/wedge_{date}.md")


def _pct(v, d=0):
    return "" if v is None or pd.isna(v) else f"{v * 100:+.{d}f}%"


def build_report(out_dir: Path, universe: str = "all", cache_dir: Optional[Path] = None, insider_days: int = 45,
                 growth_top: int = 15, today: Optional[str] = None, workers: int = 4, briefs: bool = True) -> Path:
    """``growth_top`` is accepted for backward compatibility and ignored: the growth screen is no longer part of the report."""
    from algovision.insiders_scan import insider_signals
    from algovision.research.anomalies import newsday_signals

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    today = today or dt.date.today().isoformat()
    cache = Path(cache_dir) if cache_dir else _DEFAULT_CACHE
    symbols = get_universe(universe)
    provider = DataProvider(cache_dir=cache, offline=True, workers=workers)
    frames = provider.get_many(symbols, "2y", "1d")
    last_bar = max(pd.Timestamp(df.index[-1]) for df in frames.values()).strftime("%Y-%m-%d")
    sectors = {x["symbol"]: x["sector"] for x in load_snapshot()["sp500"]}
    md: List[str] = [f"# AlgoVision daily report - {today}\n", f"Prices through {last_bar}; {len(frames)} of {len(symbols)} symbols. "
                     "Every ticker links to its TradingView chart.\n"]

    # 1. insider buying (the strongest tested rule)
    md.append("## 1. Insider buying (SEC Form 4, officers & directors, last "
              f"{insider_days} days)\n")
    md.append("Rule tested 2016-2026: purchase >= $100k in a **beaten-down** stock (below 200-day MA, 6-month return < -8%): "
              "+10% vs random entry over 60 bars, +15% over 120, hit ~68%, both halves of the decade. Purchases in "
              "uptrending stocks showed no edge and are listed for context only.\n")
    try:
        sig, tx = insider_signals(frames, symbols, days=insider_days, min_value=100_000, require_beaten=False, cache_dir=cache, workers=workers)
    except Exception as exc:  # noqa: BLE001
        sig, tx = pd.DataFrame(), pd.DataFrame()
        md.append(f"EDGAR scan failed: {exc}\n")
    brief_tables: Dict[str, List[str]] = {}

    def tag(syms, label):
        for x in syms:
            brief_tables.setdefault(x, []).append(label)

    if len(sig):
        bd = sig[sig["beaten_down"]]
        rest = sig[~sig["beaten_down"]]
        tag(bd["symbol"], "insider buys (beaten-down)")
        tag(rest["symbol"], "insider buys (other)")
        for title, d in (("### Beaten-down stocks (the tested setup)", bd), ("### Other stocks with insider purchases (context)", rest)):
            md.append(title + "\n")
            if not len(d):
                md.append("none\n")
                continue
            t = pd.DataFrame({
                "symbol": d["symbol"].map(tv), "sector": d["symbol"].map(lambda s: sectors.get(s, "")), "last filing": d["last_filing"],
                "cluster (2+ insiders/30d)": np.where(d["cluster"], "yes", "no"), "insiders 30d": d["n_insiders_30d"],
                "buys": d["n_buys"], "total": d["total_value"].map(lambda v: f"${v / 1e6:.2f}M"),
                "avg price": d["avg_price"].map(lambda v: f"{v:.2f}"), "last": d["last_close"].map(lambda v: f"{v:.2f}"),
                "6m": d["ret_6m"].map(_pct), "vs MA200": d["dist_ma200"].map(_pct), "CEO/CFO": np.where(d["ceo_cfo"], "yes", ""),
                "buyers": d["buyers"].str.slice(0, 70)})
            md.append(t.to_markdown(index=False) + "\n")
        md.append(f"{len(tx)} officer/director open-market trades scanned.\n")
    # 2. short-horizon signals
    md.append("## 2. Short-horizon signals\n")
    nd = newsday_signals(lambda s: frames[s], [s for s in symbols if s in frames], max_age=5)
    md.append("### News-day rule (>=4% gap on >=3x volume in a beaten-down stock, last 5 bars; hold ~60 bars; tested +6-7% vs random)\n")
    if len(nd):
        tag(nd["symbol"], "news-day")
        t = nd[["symbol", "news_date", "bars_ago", "gap", "volume_ratio", "ret_6m", "dist_ma200", "last_close", "since_news", "bars_left"]].copy()
        for c in ("gap", "ret_6m", "dist_ma200", "since_news"):
            t[c] = t[c].map(lambda v: _pct(v, 1))
        t["volume_ratio"] = t["volume_ratio"].map(lambda v: f"{v:.1f}x")
        t["sector"] = t["symbol"].map(lambda s: sectors.get(s, ""))
        t["symbol"] = t["symbol"].map(tv)
        md.append(t.to_markdown(index=False) + "\n")
    else:
        md.append("none\n")
    from algovision.wedge_report import wedge_matches
    wedges = wedge_matches(frames, symbols)
    # peer groups (cached a week) and today's divergence / group state for every listed name
    peers: Dict[str, Dict] = {}
    try:
        from algovision.peers import load_peers
        from algovision.research.groups import group_context_today
        listed = list(dict.fromkeys(list(brief_tables) + list(nd["symbol"]) + list(wedges)))
        peers = load_peers(frames, cache, symbols=listed)
        import json as _json
        model = _json.loads((cache / "peers.json").read_text())
        for s, g in group_context_today(frames, model, listed).items():
            peers.setdefault(s, {}).update(g)
    except Exception as exc:  # noqa: BLE001
        md.append(f"peer context unavailable: {exc}\n")

    def group_cell(s):
        p = peers.get(s) or {}
        if p.get("g_beaten") is None:
            return ""
        return (("beaten" if p["g_beaten"] else "not beaten") + (f" ({p['share_beaten'] * 100:.0f}%)" if p.get("share_beaten") == p.get("share_beaten") else "")
                + (f" + wedge {p['g_wedge']}" if p.get("g_wedge") else ""))

    rows = []
    for s, m in wedges.items():
        tag([s], "falling wedge")
        rows.append({"symbol": tv(s), "status": m.status, "score": round(m.score, 2), "start": m.start_date, "end": m.end_date,
                     "breakout": m.breakout_date or "", "level": round(m.level, 2), "stop": round(m.stop, 2),
                     "last": round(m.last_close, 2), "6m": _pct(m.metrics["context"]["ret_126"]), "vs MA200": _pct(m.metrics["context"]["dist_ma200"]),
                     "group": group_cell(s)})
    md.append("### Falling Wedge in beaten-down stocks (confirmed = broke out within 5 bars; forming = still inside; hold ~20 bars; tested +3% vs random)\n")
    md.append((pd.DataFrame(rows).sort_values(["status", "score"], ascending=[True, False]).to_markdown(index=False) if rows else "none") + "\n")
    if rows:
        md.append("*group*: the stock's peer group as one equal-weight basket, beaten down or not (in brackets the share of the other members "
                  "that are beaten down), and \"+ wedge\" when the basket itself is in a falling wedge. Signals where most of the group was beaten "
                  "down too earned +1.2% (train) / +1.9% (test) more over 20 bars, positive in all 6 years tested, not confirmed at 60 bars "
                  "(docs/research_groups.md); moderate evidence, context not a filter.\n")
    if wedges:
        md.append(f"One-rule file in Hebrew with the full technical analysis of every wedge, why the stock fell and the brief, "
                  f"each table row linked to its section: `wedge_{today}.md` ({WEDGE_URL.format(date=today)}).\n")
    # 3. one research brief per name in the tables above
    md.append("## 3. Stock briefs (one per name in the tables above)\n")
    briefs_written = False
    wedge_written = False
    if briefs and brief_tables:
        from algovision.briefs import write_briefs
        try:
            bench = provider.get_many(["SPY"], "2y", "1d").get("SPY")
            bpath, brows = write_briefs(out_dir, today, list(brief_tables), frames, brief_tables,
                                        insider_symbols=[x for x, t in brief_tables.items() if any(l.startswith("insider") for l in t)],
                                        cache_dir=cache, workers=workers, bench=bench, peers=peers)
            if wedges:
                from algovision.wedge_report import build_wedge_report
                try:  # the briefs data is cached by write_briefs, so this reads from cache
                    build_wedge_report(out_dir, today, frames, wedges, sectors, cache_dir=cache, workers=workers, bench=bench, peers=peers)
                    wedge_written = True
                except Exception as exc:  # noqa: BLE001
                    md.append(f"wedge file unavailable: {exc}\n")
            from algovision.briefs import summary_table
            md.append(f"Full briefs (price context, why it fell, investor concerns and sentiment, analysts, last report, fundamentals) for {len(brows)} stocks in "
                      f"`{bpath.name}`. The *read* column is a rule-based score over listed signals (signs of a bottom / undecided / "
                      "still falling), not a forecast. *Why fell* names the evidence found around the largest down days "
                      "(headlines naming the company, rating cuts, market-wide days) or says \"not found\"; nothing is inferred. *Vs peers 20d* is "
                      "the stock's 20-day return relative to its peer group (the stocks most correlated with it after removing the market, "
                      "from prices) and its z-score against the last year; below -2 means an unusual drop versus peers.\n")
            md.append(summary_table(brows))
            briefs_written = True
        except Exception as exc:  # noqa: BLE001
            md.append(f"briefs unavailable: {exc}\n")
    else:
        md.append("skipped\n")
    # 4. forward-test journal
    md.append("## 4. Forward test (journal)\n")
    latest = out_dir / "latest.md"
    if latest.exists():
        text = latest.read_text(encoding="utf-8")
        i = text.find("## Running results")
        md.append(text[i:] if i >= 0 else text)
    else:
        md.append("no journal yet\n")
    md.append("\n---\nSystematic screens and a forward test, not investment advice. Survivorship bias applies to all backtests "
              "(today's index members); see docs/research*.md for methods and caveats.\n")
    from algovision.whatsnew import write_whatsnew

    text = "\n".join(md)
    briefs_url = BRIEFS_URL.format(date=today) if briefs_written else None
    wedge_url = WEDGE_URL.format(date=today) if wedge_written else None
    write_whatsnew(out_dir, today, text, briefs_url, wedge_url, REPORT_URL.format(date=today))   # compares with the previous dated report before it is overwritten
    path = out_dir / f"report_{today}.md"
    path.write_text(text, encoding="utf-8")
    (out_dir / "report_latest.md").write_text(text, encoding="utf-8")
    return path
