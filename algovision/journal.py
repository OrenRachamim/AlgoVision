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
    "insider_buy_beaten_down": {"hold": 120, "expect": "+10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md)"},
    "jev_pick": {"hold": 20, "expect": "untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py)"},
    "jev_skip": {"hold": 20, "expect": "untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case"},
    "early_rally_beaten_down": {"hold": 20, "expect": "+2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md)"},
}
# the research expectation in a few words, for the expectation-vs-realised table
EXPECT_SHORT = {
    "newsday": {"en": "+6-7% vs random at 60 bars, hit ~62%", "he": "+6-7% מול אקראי ב-60 נרות, פגיעה ~62%"},
    "falling_wedge_beaten_down": {"en": "+3% vs random at 20 bars, hit ~60%", "he": "+3% מול אקראי ב-20 נרות, פגיעה ~60%"},
    "insider_buy_beaten_down": {"en": "+10% vs random at 60 bars, +15% at 120, hit ~68%", "he": "+10% מול אקראי ב-60 נרות, +15% ב-120, פגיעה ~68%"},
    "jev_pick": {"en": "untested (forward test only)", "he": "לא נבדק (מבחן קדימה בלבד)"},
    "jev_skip": {"en": "untested; a fall is the success case", "he": "לא נבדק; ירידה היא ההצלחה"},
    "early_rally_beaten_down": {"en": "+2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY", "he": "+2-3% נטו ב-20 נרות, פגיעה ~58-61%, ~0 מול SPY"},
}
# rules that were logged in the past but are no longer tracked or reported (rows stay in signals.csv)
RETIRED_RULES = {"growth_top10"}
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


def collect_rally(frames: Dict[str, pd.DataFrame], symbols: List[str], today: str) -> List[Dict]:
    """Beaten-down stocks where a turn rule fired on the last bar (docs/research_rally.md); one row per stock."""
    from algovision.research.rally import early_rally_signals
    rows: List[Dict] = []
    sig = early_rally_signals(frames, [s for s in symbols if s in frames], max_age=1)
    for r in sig.itertuples():
        rows.append({"logged": today, "rule": "early_rally_beaten_down", "symbol": r.symbol, "signal_date": r.signal_date, "status": "open",
                     "ref_price": f"{r.close:.4f}", "entry_date": "", "entry_price": "",
                     "hold_bars": RULES["early_rally_beaten_down"]["hold"],
                     "note": f"{r.rules}; day {r.day_ret * 100:+.1f}%, 10d {r.ret_10 * 100:+.1f}%, 6m {r.ret_6m * 100:+.0f}%, vs MA200 {r.dist_ma200 * 100:+.0f}%"})
    return rows


def mark_to_market(journal: pd.DataFrame, frames: Dict[str, pd.DataFrame], bench: Optional[pd.DataFrame] = None,
                   panels=None) -> pd.DataFrame:
    """Fill entry prices (next open after the signal) and compute results for every logged signal.

    ``panels`` = ``(open, close)`` panels from :func:`algovision.regime.build_panels` (built here when None); they give
    ``basket_ret``, the equal-weight return of the stocks that were beaten down on the signal date over the same window,
    the fair benchmark for a rule that only buys beaten-down stocks."""
    from algovision.regime import basket_return, beaten_mask, build_panels

    if panels is None:
        panels = build_panels({s: df for s, df in frames.items() if s != "SPY"})
    p_open, p_close = panels
    members_cache: Dict[int, List[str]] = {}
    out = []
    for r in journal.itertuples():
        rec = r._asdict()
        rec.pop("Index", None)
        df = frames.get(r.symbol)
        rec.update({"bars_elapsed": np.nan, "last_price": np.nan, "ret": np.nan, "done": False, "spy_ret": np.nan, "basket_ret": np.nan})
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
            if len(p_close):
                sig_pos = p_close.index.searchsorted(pd.Timestamp(r.signal_date), side="right") - 1
                e = p_close.index.searchsorted(pd.Timestamp(idx[entry_pos]))
                x = p_close.index.searchsorted(pd.Timestamp(idx[exit_pos]))
                if sig_pos >= 200 and e < len(p_close) and x < len(p_close):
                    if sig_pos not in members_cache:
                        bm = beaten_mask(p_close, sig_pos)
                        members_cache[sig_pos] = bm[bm].index.tolist()
                    rec["basket_ret"] = basket_return(p_open, p_close, members_cache[sig_pos], e, x)
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
        bk = g["basket_ret"].astype(float).dropna() if "basket_ret" in g.columns else pd.Series(dtype=float)
        if len(bk):
            lines.append(f"- beaten-down basket over the same holding periods: mean {bk.mean() * 100:+.2f}% "
                         f"(excess {(g['ret'].astype(float).dropna().mean() - bk.mean()) * 100:+.2f}%; the fair benchmark for a rule that only buys beaten-down stocks)")
        lines.append("")
    return "\n".join(lines)


def expectation_table(mtm: pd.DataFrame, lang: str = "en") -> str:
    """One line per rule: what the research expected and what the journal realised so far (all logged trades, closed and marked to market)."""
    he = lang == "he"
    rows = []
    for rule, g in mtm.groupby("rule"):
        r = g["ret"].astype(float).dropna()
        closed = g[g["done"] == True]  # noqa: E712
        sp = g["spy_ret"].astype(float).dropna() if "spy_ret" in g.columns else pd.Series(dtype=float)
        bk = g["basket_ret"].astype(float).dropna() if "basket_ret" in g.columns else pd.Series(dtype=float)
        rows.append({
            ("כלל" if he else "rule"): rule,
            ("המחקר ציפה" if he else "research expected"): EXPECT_SHORT.get(rule, {}).get("he" if he else "en", RULES.get(rule, {}).get("expect", "")),
            ("נרשמו" if he else "logged"): len(g), ("נסגרו" if he else "closed"): len(closed),
            ("ממוצע" if he else "mean"): f"{r.mean() * 100:+.2f}%" if len(r) else "",
            ("פגיעה" if he else "hit"): f"{(r > 0).mean() * 100:.0f}%" if len(r) else "",
            ("מול SPY" if he else "vs SPY"): f"{(r.mean() - sp.mean()) * 100:+.2f}%" if len(r) and len(sp) else "",
            ("מול סל המוכות" if he else "vs beaten basket"): f"{(r.mean() - bk.mean()) * 100:+.2f}%" if len(r) and len(bk) else "",
        })
    if not rows:
        return ""
    return pd.DataFrame(rows).to_markdown(index=False) + "\n"


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
        ins_rows = collect_insiders(frames, symbols, today, cache_dir)
    except Exception as exc:  # noqa: BLE001 - EDGAR is optional for the journal
        ins_rows = []
        print(f"insider scan skipped: {exc}")
    open_ins = set(journal[(journal["rule"] == "insider_buy_beaten_down") & (journal["status"] != "closed")]["symbol"])
    new_rows += [r for r in ins_rows if r["symbol"] not in open_ins]
    # one early-rally position per stock at a time (the tested rule is "first turn rule to fire, one entry per 30 days")
    open_rally = set(journal[(journal["rule"] == "early_rally_beaten_down") & (journal["status"] != "closed")]["symbol"])
    new_rows += [r for r in collect_rally(frames, symbols, today) if r["symbol"] not in open_rally]
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
    shown = mtm[~mtm["rule"].isin(RETIRED_RULES)] if len(mtm) else mtm
    md.append("\n## Running results\n")
    if len(shown):
        md.append("Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight "
                  "return of the stocks that were beaten down on the signal date over the same window):\n")
        md.append(expectation_table(shown))
    md.append(summary(shown) if len(shown) else "no signals logged yet")
    if len(shown):
        open_ = shown[shown["done"] != True]  # noqa: E712
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
