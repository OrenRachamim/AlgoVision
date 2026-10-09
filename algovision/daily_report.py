"""One-file daily report: regime, insider buying, short-horizon signals, one research brief per listed stock, the look-back
ledger of the reports themselves, forward-test results.

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
# everything in one Hebrew file (same directory, same push): the one the Telegram job sends
DAILY_URL = os.environ.get("ALGOVISION_DAILY_URL", "https://github.com/OrenRachamim/AlgoVision/blob/claude/stock-pattern-detection-b94x35/journal/daily_{date}.md")

# the signal tables keyed by the 'what is new' section labels, for the 'days listed' column
DAYS_LABEL = {"insider_beaten": "Insider buys, beaten-down (tested setup)", "insider_other": "Insider buys, other stocks", "newsday": "News-day",
              "wedge": "Falling wedge, beaten-down", "rally": "Early rally, beaten-down", "watch": "Wedge watch list (forming, not a signal)"}


def _pct(v, d=0):
    return "" if v is None or pd.isna(v) else f"{v * 100:+.{d}f}%"


def _days(days: Dict[str, Dict[str, int]], key: str, symbol: str) -> int:
    """Days listed including today: in the wedge table a forming wedge that moved to the watch list keeps its count."""
    label = DAYS_LABEL[key]
    n = days.get(label, {}).get(symbol, 0)
    if key == "watch":
        n = max(n, days.get(DAYS_LABEL["wedge"], {}).get(symbol, 0))
    return n + 1


def build_report(out_dir: Path, universe: str = "all", cache_dir: Optional[Path] = None, insider_days: int = 45,
                 growth_top: int = 15, today: Optional[str] = None, workers: int = 4, briefs: bool = True) -> Path:
    """``growth_top`` is accepted for backward compatibility and ignored: the growth screen is no longer part of the report."""
    from algovision.insiders_scan import insider_signals
    from algovision.research.anomalies import newsday_signals
    from algovision.regime import regime_markdown, regime_stats
    from algovision.whatsnew import days_listed

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    today = today or dt.date.today().isoformat()
    cache = Path(cache_dir) if cache_dir else _DEFAULT_CACHE
    symbols = get_universe(universe)
    provider = DataProvider(cache_dir=cache, offline=True, workers=workers)
    frames = provider.get_many(symbols, "2y", "1d")
    last_bar = max(pd.Timestamp(df.index[-1]) for df in frames.values()).strftime("%Y-%m-%d")
    sectors = {x["symbol"]: x["sector"] for x in load_snapshot()["sp500"]}
    bench = provider.get_many(["SPY"], "2y", "1d").get("SPY")
    days = days_listed(out_dir, today)
    md: List[str] = [f"# AlgoVision daily report - {today}\n", f"Prices through {last_bar}; {len(frames)} of {len(symbols)} symbols. "
                     "Every ticker links to its TradingView chart.\n"]
    # 0. the regime: is the beaten-down basket itself falling?
    regime: Dict = {}
    try:
        regime = regime_stats(frames, bench)
        md += regime_markdown(regime, "en")
    except Exception as exc:  # noqa: BLE001
        md.append(f"regime line unavailable: {exc}\n")

    # 1. insider buying (the strongest tested rule)
    md.append("## 1. Insider buying (SEC Form 4, officers & directors, last "
              f"{insider_days} days)\n")
    md.append("Rule tested 2016-2026: purchase >= $100k in a **beaten-down** stock (below 200-day MA, 6-month return < -8%): "
              "+10% vs random entry over 60 bars, +15% over 120, hit ~68%, both halves of the decade. Purchases in "
              "uptrending stocks showed no edge and are listed in one line for context only.\n")
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
        md.append("### Beaten-down stocks (the tested setup)\n")
        if len(bd):
            t = pd.DataFrame({
                "symbol": bd["symbol"].map(tv), "days listed": bd["symbol"].map(lambda s: _days(days, "insider_beaten", s)),
                "sector": bd["symbol"].map(lambda s: sectors.get(s, "")), "last filing": bd["last_filing"],
                "cluster (2+ insiders/30d)": np.where(bd["cluster"], "yes", "no"), "insiders 30d": bd["n_insiders_30d"],
                "buys": bd["n_buys"], "total": bd["total_value"].map(lambda v: f"${v / 1e6:.2f}M"),
                "avg price": bd["avg_price"].map(lambda v: f"{v:.2f}"), "last": bd["last_close"].map(lambda v: f"{v:.2f}"),
                "6m": bd["ret_6m"].map(_pct), "vs MA200": bd["dist_ma200"].map(_pct), "CEO/CFO": np.where(bd["ceo_cfo"], "yes", ""),
                "buyers": bd["buyers"].str.slice(0, 70)})
            md.append(t.to_markdown(index=False) + "\n")
        else:
            md.append("none\n")
        md.append("### Other stocks with insider purchases (context)\n")
        if len(rest):
            md.append("No tested edge (uptrending stocks), one line only: " + ", ".join(
                f"{tv(r.symbol)} {r.last_filing} ${r.total_value / 1e6:.2f}M{' CEO/CFO' if r.ceo_cfo else ''}{' cluster' if r.cluster else ''}"
                for r in rest.itertuples()) + ".\n")
        else:
            md.append("none\n")
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
        t.insert(1, "days listed", t["symbol"].map(lambda s: _days(days, "newsday", s)))
        t["symbol"] = t["symbol"].map(tv)
        md.append(t.to_markdown(index=False) + "\n")
    else:
        md.append("none\n")
    from algovision.wedge_report import wedge_matches
    wedges = wedge_matches(frames, symbols)
    from algovision.research.rally import early_rally_signals
    rally = early_rally_signals(frames, [s for s in symbols if s in frames], max_age=3)
    # peer groups (cached a week) and today's divergence / group state for every listed name
    peers: Dict[str, Dict] = {}
    try:
        from algovision.peers import load_peers
        from algovision.research.groups import group_context_today
        listed = list(dict.fromkeys(list(brief_tables) + list(nd["symbol"]) + list(wedges) + list(rally["symbol"])))
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

    confirmed = {s: m for s, m in wedges.items() if m.status == "confirmed"}
    forming = {s: m for s, m in wedges.items() if m.status != "confirmed"}

    def wedge_row(s, m, key):
        df = frames[s]
        since = ""
        if m.breakout_idx is not None:
            since = len(df) - 1 - int(m.breakout_idx)
        return {"symbol": tv(s), "days listed": _days(days, key, s), "status": m.status, "score": round(m.score, 2), "start": m.start_date, "end": m.end_date,
                "breakout": m.breakout_date or "", "bars since breakout": since, "level": round(m.level, 2), "stop": round(m.stop, 2),
                "last": round(m.last_close, 2), "6m": _pct(m.metrics["context"]["ret_126"]), "vs MA200": _pct(m.metrics["context"]["dist_ma200"]),
                "group": group_cell(s)}

    rows = [wedge_row(s, m, "wedge") for s, m in confirmed.items()]
    tag(confirmed, "falling wedge")
    md.append("### Falling Wedge in beaten-down stocks (confirmed = closed above the upper line within the last 5 bars; hold ~20 bars; "
              "tested +3% vs random). Wedges still forming are on the watch list at the end of this section, not here.\n")
    md.append((pd.DataFrame(rows).sort_values("score", ascending=False).drop(columns=["status"]).to_markdown(index=False) if rows else "none") + "\n")
    if rows:
        md.append("*group*: the stock's peer group as one equal-weight basket, beaten down or not (in brackets the share of the other members "
                  "that are beaten down), and \"+ wedge\" when the basket itself is in a falling wedge. Signals where most of the group was beaten "
                  "down too earned +1.2% (train) / +1.9% (test) more over 20 bars, positive in all 6 years tested, not confirmed at 60 bars "
                  "(docs/research_groups.md); moderate evidence, context not a filter.\n")
    if wedges:
        md.append(f"One-rule file in Hebrew with the full technical analysis of every wedge (confirmed and forming), why the stock fell and the brief, "
                  f"each table row linked to its section: `wedge_{today}.md` ({WEDGE_URL.format(date=today)}).\n")
    md.append("### Early rally in beaten-down stocks (a turn rule fired in the last 3 bars; hold ~20 bars; tested +2-3% net, "
              "hit ~58-61%, +3.5-4% vs random entry, about 0 vs SPY at 20 bars)\n")
    if len(rally):
        tag(rally["symbol"], "early rally")
        t = rally[["symbol", "rules", "n_rules", "signal_date", "bars_ago", "day_ret", "ret_10", "ret_6m", "from_52w_high", "dist_ma50",
                   "dist_ma200", "volume_ratio", "last"]].copy()
        for c in ("day_ret", "ret_10", "ret_6m", "from_52w_high", "dist_ma50", "dist_ma200"):
            t[c] = t[c].map(lambda v: _pct(v, 1))
        t["volume_ratio"] = t["volume_ratio"].map(lambda v: "" if pd.isna(v) else f"{v:.1f}x")
        t["group"] = t["symbol"].map(group_cell)
        t["sector"] = t["symbol"].map(lambda s: sectors.get(s, ""))
        t.insert(1, "days listed", t["symbol"].map(lambda s: _days(days, "rally", s)))
        t["symbol"] = t["symbol"].map(tv)
        t = t.rename(columns={"n_rules": "rules fired", "day_ret": "signal day", "ret_10": "10d", "ret_6m": "6m", "from_52w_high": "from 52w high",
                              "dist_ma50": "vs MA50", "dist_ma200": "vs MA200", "volume_ratio": "volume"})
        md.append(t.to_markdown(index=False) + "\n")
        md.append("*rules*: `ma50_cross` = close back above the 50-day MA after >= 15 of 20 bars below it; `golden_20_50` = 20-day MA crosses "
                  "above the 50-day; `higher_high` = first close above the swing high after a higher low (Dow turn); `thrust` = +8% in 10 bars "
                  "from the 60-bar low after a flat or negative 6 months; `rsi_turn` = RSI(14) back above 50 after < 35. Tested 2016-2026 on "
                  "beaten-down stocks only (below the 200-day MA, 6-month return < -8%), one entry per stock per 30 days, entry at the next open, "
                  "10 bps cost: 20 bars +2.7% (train) / +2.2% (test), hit 61% / 58%, +4.0% / +3.5% over random entries in the same stocks "
                  "(t 19 / 13), positive in all 10 years, but only +0.6% / 0.0% over the SPY at 20 bars and +0.8% / -0.4% at 60 (the rule times "
                  "the stock's own turn, it does not beat the index). Only the deepest declines beat the SPY (6m < -30%: +6.1% / +4.5% net at 20 bars, "
                  "+2.5% / +2.1% over the SPY); two or more rules within a week helps a little. The journal logs the day-0 rows as "
                  "`early_rally_beaten_down` (docs/research_rally.md).\n")
    else:
        md.append("none\n")
    # the watch list: wedges still forming (no signal yet)
    tag(forming, "falling wedge (forming)")
    md.append("### Watch list: falling wedges still forming (not a signal; the signal is the close above the upper line)\n")
    if forming:
        wrows = [wedge_row(s, m, "watch") for s, m in forming.items()]
        md.append(pd.DataFrame(wrows).sort_values("score", ascending=False).drop(columns=["status", "breakout", "bars since breakout"]).to_markdown(index=False) + "\n")
        md.append("In the first five weeks of the forward test the forming wedges lost about 6% over 20 bars (hit 11%), the confirmed ones did not; "
                  "a stock inside a falling wedge is a stock still falling. The journal logs a wedge only on its breakout day.\n")
    else:
        md.append("none\n")
    md.append("*days listed*: reports (of the last 30) in which the name sat in that table, today included. In the first five weeks the names "
              "listed 4-7 days did worst; a fresh listing was better than a stale one.\n")
    # 3. one research brief per name in the tables above
    md.append("## 3. Stock briefs (one per name in the tables above)\n")
    briefs_written = False
    wedge_written = False
    brows: List[Dict] = []
    decisions: Dict[str, Dict] = {}
    picks: List[str] = []
    skips: List[str] = []
    if briefs and brief_tables:
        from algovision.briefs import write_briefs
        try:
            from algovision import decide
            use_ai = decide.available()
            bpath, brows = write_briefs(out_dir, today, list(brief_tables), frames, brief_tables,
                                        insider_symbols=[x for x, t in brief_tables.items() if any(l.startswith("insider") for l in t)],
                                        cache_dir=cache, workers=workers, bench=bench, peers=peers, decisions=use_ai)
            decisions = {}
            for r in brows:
                if r.get("_decision"):
                    decisions[r["symbol"]] = {**r["_decision"], "tables": r.get("tables"), "read": r.get("read"), "score": r.get("score")}
            if decisions:
                try:
                    decide.write_decisions(out_dir, today, decisions)
                    picks = decide.log_picks(out_dir, today, decisions, frames)
                    skips = decide.log_skips(out_dir, today, decisions, frames)
                except Exception as exc:  # noqa: BLE001
                    md.append(f"decision log unavailable: {exc}\n")
            if wedges:
                from algovision.wedge_report import build_wedge_report
                try:  # the briefs data is cached by write_briefs, so this reads from cache
                    build_wedge_report(out_dir, today, frames, wedges, sectors, cache_dir=cache, workers=workers, bench=bench, peers=peers,
                                       decisions=decisions, briefs_url=BRIEFS_URL.format(date=today))
                    wedge_written = True
                except Exception as exc:  # noqa: BLE001
                    md.append(f"wedge file unavailable: {exc}\n")
            from algovision.briefs import flags_legend, summary_table
            from algovision.checklist import checklist_markdown
            md += checklist_markdown(brows, "en", regime.get("warning"))
            md.append("### Summary table\n")
            md.append(f"Full briefs (price context, why it fell, investor concerns and sentiment, analysts, last report, fundamentals) for {len(brows)} stocks in "
                      f"`{bpath.name}`. The *read* column is a rule-based score over listed signals (signs of a bottom / undecided / "
                      "still falling), not a forecast. *Why fell* names the evidence found around the largest down days "
                      "(headlines naming the company, rating cuts, market-wide days) or says \"not found\"; nothing is inferred. *Vs peers 20d* is "
                      "the stock's 20-day return relative to its peer group (the stocks most correlated with it after removing the market, "
                      "from prices) and its z-score against the last year; below -2 means an unusual drop versus peers.\n")
            md.append(flags_legend("en") + "\n")
            md.append(summary_table(brows))
            md.append("### Model decisions (Jev), a forward test\n")
            if decisions:
                md.append("A typed decision model (TypeSafe Jev 1.13 through OpenRouter) read each brief above, and only the brief, and "
                          "answered fixed questions with calibrated probabilities: the action for a one-month hold (buy / watch / skip), the "
                          "kind of decline, whether the drop is a corporate action or data artefact rather than a real decline, whether a "
                          "known event is due within four weeks, whether the evidence supports or contradicts the setup, and how bad the "
                          "news is for the business (0-3). It gives no rationale. Its 'buy' calls with P(buy) >= 0.6 are logged in the "
                          "journal as the rule `jev_pick` and its 'skip' calls with P(skip) >= 0.5 as `jev_skip` (hold 20 bars; a skip is right "
                          "when the stock falls), both marked to market like every other rule. In the first week the 'skip' names did better than "
                          "the 'buy' names, so until the forward test has 20+ closed trades the column is context, not a recommendation. The *AI* "
                          "column of the summary table carries the same action; `!` marks a likely corporate action or data problem.\n")
                md.append(decide.decisions_table(decisions, tv))
                md.append(("Logged in the journal as jev_pick today: " + ", ".join(tv(s) for s in picks) if picks
                           else "No new jev_pick logged today (no 'buy' with P >= 0.6 without an open position).")
                          + (" Logged as jev_skip today: " + ", ".join(tv(s) for s in skips) + "." if skips else "") + "\n")
            else:
                md.append("skipped (no OpenRouter API key, or the model was unreachable)\n")
            briefs_written = True
        except Exception as exc:  # noqa: BLE001
            md.append(f"briefs unavailable: {exc}\n")
    else:
        md.append("skipped\n")
    # 4. the look-back ledger: what every listed name did after it was listed
    look: Dict = {"rows": [], "forward": pd.DataFrame()}
    try:
        from algovision.lookback import lookback_markdown, run_lookback
        look = run_lookback(out_dir, frames, bench)
        md += lookback_markdown(look["rows"], look["forward"], "en")
    except Exception as exc:  # noqa: BLE001
        md.append(f"## 4. What has worked so far\n\nlook-back unavailable: {exc}\n")
    # 5. forward-test journal
    md.append("## 5. Forward test (journal)\n")
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
    daily_url = DAILY_URL.format(date=today) if briefs_written else None
    write_whatsnew(out_dir, today, text, briefs_url, wedge_url, REPORT_URL.format(date=today), daily_url)   # compares with the previous dated report before it is overwritten
    path = out_dir / f"report_{today}.md"
    path.write_text(text, encoding="utf-8")
    (out_dir / "report_latest.md").write_text(text, encoding="utf-8")
    if briefs_written:
        # everything in one Hebrew file: the tables, the summary and Jev, a full section per stock, the journal
        from algovision.daily_he import build_daily_he
        try:
            note_he = (out_dir / "new_he_latest.md").read_text(encoding="utf-8")
            build_daily_he(out_dir, today, last_bar, len(frames), len(symbols), insider_days, sig, tx, nd, wedges, rally, brows, frames, peers,
                           decisions, picks, sectors, bench, note_he, regime=regime, days=days, lookback=look, skips=skips)
        except Exception as exc:  # noqa: BLE001
            print(f"hebrew daily file unavailable: {exc}")
    return path
