"""One-file daily report: insider buying, short-horizon signals, growth screen, forward-test results.

Designed to run right after ``journal`` (which refreshes prices, fundamentals and EDGAR filings), fully from
cache, and to be pasted / translated verbatim by the scheduled routine.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig
from algovision.data.provider import DataProvider, _DEFAULT_CACHE
from algovision.data.universe import get_universe, load_snapshot
from algovision.links import tv
from algovision.scanner import Scanner


def _pct(v, d=0):
    return "" if v is None or pd.isna(v) else f"{v * 100:+.{d}f}%"


def build_report(out_dir: Path, universe: str = "all", cache_dir: Optional[Path] = None, insider_days: int = 45,
                 growth_top: int = 15, today: Optional[str] = None, workers: int = 4) -> Path:
    from algovision.data.fundamentals import FundamentalsProvider
    from algovision.growth import diversified_top, price_features, score
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
    if len(sig):
        bd = sig[sig["beaten_down"]]
        rest = sig[~sig["beaten_down"]]
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
        t = nd[["symbol", "news_date", "bars_ago", "gap", "volume_ratio", "ret_6m", "dist_ma200", "last_close", "since_news", "bars_left"]].copy()
        for c in ("gap", "ret_6m", "dist_ma200", "since_news"):
            t[c] = t[c].map(lambda v: _pct(v, 1))
        t["volume_ratio"] = t["volume_ratio"].map(lambda v: f"{v:.1f}x")
        t["sector"] = t["symbol"].map(lambda s: sectors.get(s, ""))
        t["symbol"] = t["symbol"].map(tv)
        md.append(t.to_markdown(index=False) + "\n")
    else:
        md.append("none\n")
    cfg = DetectorConfig(filter_max_ret_126=-0.08, filter_below_ma200=True, recent_bars=5)
    sc = Scanner(DataProvider(cache_dir=None, offline=True), cfg, ["Falling Wedge"])
    rows = []
    for s in symbols:
        df = frames.get(s)
        if df is None or len(df) < 260:
            continue
        for m in sc.analyse_frame(s, df, mode="current"):
            rows.append({"symbol": tv(s), "status": m.status, "score": round(m.score, 2), "start": m.start_date, "end": m.end_date,
                         "breakout": m.breakout_date or "", "level": round(m.level, 2), "stop": round(m.stop, 2),
                         "last": round(m.last_close, 2), "6m": _pct(m.metrics["context"]["ret_126"]), "vs MA200": _pct(m.metrics["context"]["dist_ma200"])})
    md.append("### Falling Wedge in beaten-down stocks (confirmed = broke out within 5 bars; forming = still inside; hold ~20 bars; tested +3% vs random)\n")
    md.append((pd.DataFrame(rows).sort_values(["status", "score"], ascending=[True, False]).to_markdown(index=False) if rows else "none") + "\n")
    # 3. growth screen
    md.append(f"## 3. Growth screen (top {growth_top}, max 3 per sector)\n")
    md.append("Growth 40% (revenue yoy, 3y CAGR, EPS yoy, margin change), quality 20%, momentum 25% (the only backtested block), "
              "valuation 15%. Not investment advice; the fundamental blocks are untested and are being forward-tested in the journal.\n")
    try:
        fund = FundamentalsProvider(cache_dir=cache, offline=True).feature_table(symbols)
        scored = score(fund, price_features(frames), sectors)
        top = diversified_top(scored, growth_top, 3)
        t = pd.DataFrame({
            "symbol": [tv(x) for x in top.index], "sector": top["sector"].values, "score": top["score"].round(2).values,
            "rev yoy": top["rev_yoy_q"].map(_pct).values, "3y CAGR": top["rev_cagr_3y"].map(_pct).values,
            "op margin": top["op_margin"].map(_pct).values, "FCF margin": top["fcf_margin"].map(_pct).values,
            "12-1 mom": top["ret_12_1"].map(_pct).values, "fwd P/E": top["forward_pe"].map(lambda v: "" if pd.isna(v) else f"{v:.0f}").values,
            "PEG": top["peg"].map(lambda v: "" if pd.isna(v) else f"{v:.1f}").values,
            "caution": np.where(top["cyclical_flag"].values, "cyclical peak", "")})
        md.append(t.to_markdown(index=False) + "\n")
        md.append("Why (top 5):\n")
        for sym, r in top.head(5).iterrows():
            md.append(f"- **{tv(sym)}**: {r['why']}")
        conc = top["sector"].value_counts()
        md.append(f"\nSector concentration in the top {growth_top}: " + ", ".join(f"{k} {v}" for k, v in conc.items()) + "\n")
    except Exception as exc:  # noqa: BLE001
        md.append(f"growth screen unavailable: {exc}\n")
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
    path = out_dir / f"report_{today}.md"
    path.write_text("\n".join(md), encoding="utf-8")
    (out_dir / "report_latest.md").write_text("\n".join(md), encoding="utf-8")
    return path
