"""Forward-test journal.

Every run logs today's live signals (news-day rule, beaten-down Falling Wedge)
to ``signals.csv`` and marks all previously logged signals to market, so the
rules are tested on data that did not exist when they were written.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig
from algovision.data.provider import DataProvider, _DEFAULT_CACHE
from algovision.links import tv
from algovision.data.universe import get_universe
from algovision.research.anomalies import newsday_signals
from algovision.scanner import Scanner

RULES = {
    "newsday": {"hold": 60, "expect": "+6-7% vs random, hit ~62% (docs/research_anomalies.md)"},
    "falling_wedge_beaten_down": {"hold": 20, "expect": "+3% vs random, hit ~60% (docs/research_falling_wedge.md)"},
    "growth_top10": {"hold": 250, "expect": "long-horizon growth screen, judged against SPY over the same period (docs/growth_screen.md)"},
    "insider_buy_beaten_down": {"hold": 120, "expect": "+10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md)"},
}
COLS = ["logged", "rule", "symbol", "signal_date", "status", "ref_price", "entry_date", "entry_price", "hold_bars",
        "note"]


def _load(path: Path) -> pd.DataFrame:
    if path.exists():
        df = pd.read_csv(path, dtype=str)
        for c in COLS:
            if c not in df.columns:
                df[c] = ""
        return df[COLS]
    return pd.DataFrame(columns=COLS)


def collect_growth(frames: Dict[str, pd.DataFrame], symbols: List[str], today: str, cache_dir=None, n: int = 10) -> List[Dict]:
    """Today's diversified growth top-10 as long-horizon positions (entry next open, reviewed after 250 bars)."""
    from algovision.data.fundamentals import FundamentalsProvider
    from algovision.data.universe import load_snapshot
    from algovision.growth import diversified_top, price_features, score
    fund = FundamentalsProvider(cache_dir=cache_dir if cache_dir else _DEFAULT_CACHE, max_age_hours=24).feature_table(symbols)
    if not len(fund):
        return []
    sectors = {x["symbol"]: x["sector"] for x in load_snapshot()["sp500"]}
    top = diversified_top(score(fund, price_features(frames), sectors), n, 3)
    rows = []
    for sym, r in top.iterrows():
        df = frames[sym]
        rows.append({"logged": today, "rule": "growth_top10", "symbol": sym,
                     "signal_date": pd.Timestamp(df.index[-1]).strftime("%Y-%m-%d"), "status": "open",
                     "ref_price": f"{float(df['Close'].iloc[-1]):.4f}", "entry_date": "", "entry_price": "",
                     "hold_bars": RULES["growth_top10"]["hold"], "note": f"score {r['score']:.2f}; {r['why'][:160]}"})
    return rows


def collect_insiders(frames: Dict[str, pd.DataFrame], symbols: List[str], today: str, cache_dir=None) -> List[Dict]:
    """Officer/director purchases >= $100k filed in the last 7 days in beaten-down stocks."""
    from algovision.insiders_scan import insider_signals
    sig, _ = insider_signals(frames, symbols, days=7, min_value=100_000, require_beaten=True, cache_dir=cache_dir)
    rows = []
    for r in sig.itertuples():
        rows.append({"logged": today, "rule": "insider_buy_beaten_down", "symbol": r.symbol, "signal_date": r.last_filing,
                     "status": "open", "ref_price": f"{r.last_close:.4f}", "entry_date": "", "entry_price": "",
                     "hold_bars": RULES["insider_buy_beaten_down"]["hold"],
                     "note": f"{'cluster, ' if r.cluster else ''}{r.n_buys} buy(s) ${r.total_value / 1e6:.2f}M @ {r.avg_price:.2f}, "
                             f"6m {r.ret_6m * 100:+.0f}%, vs MA200 {r.dist_ma200 * 100:+.0f}%; {r.buyers[:60]}"})
    return rows


def collect_signals(frames: Dict[str, pd.DataFrame], symbols: List[str], today: str) -> List[Dict]:
    rows: List[Dict] = []
    nd = newsday_signals(lambda s: frames[s], [s for s in symbols if s in frames], max_age=1)
    for r in nd.itertuples():
        rows.append({"logged": today, "rule": "newsday", "symbol": r.symbol, "signal_date": r.news_date, "status": "open",
                     "ref_price": f"{r.close_on_news_day:.4f}", "entry_date": "", "entry_price": "",
                     "hold_bars": RULES["newsday"]["hold"],
                     "note": f"gap {r.gap * 100:+.1f}%, vol {r.volume_ratio:.1f}x, 6m {r.ret_6m * 100:+.0f}%, vs MA200 {r.dist_ma200 * 100:+.0f}%"})
    cfg = DetectorConfig(filter_max_ret_126=-0.08, filter_below_ma200=True, recent_bars=1)
    sc = Scanner(DataProvider(cache_dir=None, offline=True), cfg, ["Falling Wedge"])
    for s in symbols:
        df = frames.get(s)
        if df is None or len(df) < 260:
            continue
        for m in sc.analyse_frame(s, df, mode="current"):
            if m.status != "confirmed" or m.breakout_idx is None or m.breakout_idx != len(df) - 1:
                continue
            rows.append({"logged": today, "rule": "falling_wedge_beaten_down", "symbol": s,
                         "signal_date": pd.Timestamp(df.index[m.breakout_idx]).strftime("%Y-%m-%d"), "status": "open",
                         "ref_price": f"{m.breakout_price:.4f}", "entry_date": "", "entry_price": "",
                         "hold_bars": RULES["falling_wedge_beaten_down"]["hold"],
                         "note": f"score {m.score:.2f}, stop {m.stop:.2f}, level {m.level:.2f}"})
    return rows


def mark_to_market(journal: pd.DataFrame, frames: Dict[str, pd.DataFrame], bench: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Fill entry prices (next open after the signal) and compute results for every logged signal."""
    out = []
    for r in journal.itertuples():
        rec = r._asdict()
        rec.pop("Index", None)
        df = frames.get(r.symbol)
        rec.update({"bars_elapsed": np.nan, "last_price": np.nan, "ret": np.nan, "done": False, "spy_ret": np.nan})
        if df is None:
            out.append(rec)
            continue
        idx = df.index
        pos = idx.searchsorted(pd.Timestamp(r.signal_date))
        entry_pos = pos + 1
        if entry_pos < len(df):
            rec["entry_date"] = pd.Timestamp(idx[entry_pos]).strftime("%Y-%m-%d")
            rec["entry_price"] = f"{float(df['Open'].iloc[entry_pos]):.4f}"
            hold = int(float(r.hold_bars))
            exit_pos = min(len(df) - 1, entry_pos + hold - 1)
            last = float(df["Close"].iloc[exit_pos])
            rec["bars_elapsed"] = int(exit_pos - entry_pos + 1)
            rec["last_price"] = last
            rec["ret"] = last / float(rec["entry_price"]) - 1.0
            rec["done"] = bool(entry_pos + hold - 1 <= len(df) - 1)
            rec["status"] = "closed" if rec["done"] else "open"
            if bench is not None:
                b = bench.reindex(idx).ffill()
                rec["spy_ret"] = float(b["Close"].iloc[exit_pos] / b["Open"].iloc[entry_pos] - 1.0)
        out.append(rec)
    return pd.DataFrame(out)


def summary(mtm: pd.DataFrame) -> str:
    lines = []
    for rule, g in mtm.groupby("rule"):
        closed = g[g["done"] == True]  # noqa: E712
        open_ = g[g["done"] != True]  # noqa: E712
        lines.append(f"**{rule}** (expected: {RULES.get(rule, {}).get('expect', '')})")
        lines.append(f"- logged: {len(g)}, closed: {len(closed)}, open: {len(open_)}")
        if len(closed):
            r = closed["ret"].astype(float)
            lines.append(f"- closed trades: mean {r.mean() * 100:+.2f}%, median {r.median() * 100:+.2f}%, hit {(r > 0).mean() * 100:.0f}%, "
                         f"best {r.max() * 100:+.1f}%, worst {r.min() * 100:+.1f}%")
        if len(open_):
            r = open_["ret"].astype(float).dropna()
            if len(r):
                lines.append(f"- open trades mark-to-market: mean {r.mean() * 100:+.2f}%, hit {(r > 0).mean() * 100:.0f}%")
        sp = g["spy_ret"].astype(float).dropna() if "spy_ret" in g.columns else pd.Series(dtype=float)
        if len(sp):
            lines.append(f"- SPY over the same holding periods: mean {sp.mean() * 100:+.2f}% (excess {(g['ret'].astype(float).dropna().mean() - sp.mean()) * 100:+.2f}%)")
        lines.append("")
    return "\n".join(lines)


def run(out_dir: Path, universe: str = "all", period: str = "2y", cache_dir: Optional[Path] = None,
        max_age_hours: float = 0.5, workers: int = 4, today: Optional[str] = None) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    today = today or dt.date.today().isoformat()
    symbols = get_universe(universe)
    provider = DataProvider(cache_dir=cache_dir if cache_dir else _DEFAULT_CACHE, max_age_hours=max_age_hours,
                            workers=workers)
    frames = provider.get_many(list(symbols) + ["SPY"], period, "1d")
    bench = frames.pop("SPY", None)
    last_bar = max(pd.Timestamp(df.index[-1]) for df in frames.values()).strftime("%Y-%m-%d")
    journal = _load(out_dir / "signals.csv")
    new_rows = collect_signals(frames, symbols, today)
    try:
        growth_rows = collect_growth(frames, symbols, today, cache_dir)
    except Exception as exc:  # noqa: BLE001 - fundamentals are optional for the journal
        growth_rows = []
        print(f"growth screen skipped: {exc}")
    # a growth name already held (open position) is not re-logged; a name that drops out simply stops being added
    open_growth = set(journal[(journal["rule"] == "growth_top10") & (journal["status"] != "closed")]["symbol"])
    growth_rows = [r for r in growth_rows if r["symbol"] not in open_growth]
    new_rows += growth_rows
    try:
        ins_rows = collect_insiders(frames, symbols, today, cache_dir)
    except Exception as exc:  # noqa: BLE001 - EDGAR is optional for the journal
        ins_rows = []
        print(f"insider scan skipped: {exc}")
    open_ins = set(journal[(journal["rule"] == "insider_buy_beaten_down") & (journal["status"] != "closed")]["symbol"])
    new_rows += [r for r in ins_rows if r["symbol"] not in open_ins]
    existing = set(zip(journal["rule"], journal["symbol"], journal["signal_date"]))
    added = [r for r in new_rows if (r["rule"], r["symbol"], r["signal_date"]) not in existing]
    if added:
        journal = pd.concat([journal, pd.DataFrame(added)[COLS].astype(str)], ignore_index=True)
    mtm = mark_to_market(journal, frames, bench) if len(journal) else journal.assign(ret=np.nan, done=False)
    if len(mtm):
        journal = mtm[COLS].astype(str)
    journal.to_csv(out_dir / "signals.csv", index=False)
    if len(mtm):
        mtm.to_csv(out_dir / "mark_to_market.csv", index=False)
    md = [f"# Forward-test journal - {today}\n", f"Data through {last_bar}; {len(frames)} of {len(symbols)} symbols loaded.\n",
          f"## New signals today ({len(added)})\n"]
    if added:
        show = pd.DataFrame(added)[["rule", "symbol", "signal_date", "ref_price", "hold_bars", "note"]].copy()
        show["symbol"] = show["symbol"].map(tv)
        md.append(show.to_markdown(index=False))
    else:
        md.append("none")
    md.append("\n## Running results\n")
    md.append(summary(mtm) if len(mtm) else "no signals logged yet")
    if len(mtm):
        open_ = mtm[mtm["done"] != True]  # noqa: E712
        if len(open_):
            md.append("\n## Open positions\n")
            show = open_[["rule", "symbol", "signal_date", "entry_date", "entry_price", "bars_elapsed", "hold_bars", "ret"]].copy()
            show["ret"] = show["ret"].astype(float).map(lambda v: "" if pd.isna(v) else f"{v * 100:+.2f}%")
            show["symbol"] = show["symbol"].map(tv)
            md.append(show.to_markdown(index=False))
    daily = out_dir / f"{today}.md"
    daily.write_text("\n".join(md), encoding="utf-8")
    (out_dir / "latest.md").write_text("\n".join(md), encoding="utf-8")
    return daily
