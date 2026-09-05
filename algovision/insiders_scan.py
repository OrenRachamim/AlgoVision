"""Live insider-buying signals: the rule from docs/research_insiders.md applied to recent Form 4 filings."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from algovision.data.insiders_live import recent_transactions


def stock_state(df: pd.DataFrame) -> Dict[str, float]:
    c = df["Close"].to_numpy(dtype=float)
    ma200 = c[-200:].mean()
    return {"last_close": float(c[-1]), "ret_6m": float(c[-1] / c[-127] - 1.0), "dist_ma200": float(c[-1] / ma200 - 1.0),
            "beaten_down": bool(c[-1] < ma200 and c[-1] / c[-127] - 1.0 < -0.08)}


def insider_signals(frames: Dict[str, pd.DataFrame], symbols: Iterable[str], days: int = 45, min_value: float = 100_000,
                    require_beaten: bool = True, cache_dir=None, progress=None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    tx = recent_transactions(days=days, cache_dir=cache_dir, symbols=symbols, progress=progress)
    if not len(tx):
        return pd.DataFrame(), tx
    buys = tx[(tx["code"] == "P") & (tx["value"] >= min_value)]
    rows = []
    for sym, g in buys.groupby("symbol"):
        df = frames.get(sym)
        if df is None or len(df) < 260:
            continue
        st = stock_state(df)
        if require_beaten and not st["beaten_down"]:
            continue
        last = g["filing_date"].max()
        recent30 = g[g["filing_date"] > last - pd.Timedelta(days=30)]
        rows.append({"symbol": sym, "last_filing": last.strftime("%Y-%m-%d"), "n_insiders_30d": recent30["owner_cik"].nunique(),
                     "n_buys": len(g), "total_value": float(g["value"].sum()), "ceo_cfo": bool(g["is_ceo_cfo"].any()),
                     "buyers": "; ".join(sorted(set(g["owner_name"].astype(str))))[:120],
                     "avg_price": float((g["value"].sum() / g["shares"].sum())), **st,
                     "cluster": bool(recent30["owner_cik"].nunique() >= 2)})
    sig = pd.DataFrame(rows)
    if len(sig):
        sig = sig.sort_values(["cluster", "beaten_down", "total_value"], ascending=[False, False, False]).reset_index(drop=True)
    return sig, tx


def format_signals(sig: pd.DataFrame, tx: pd.DataFrame) -> str:
    if not len(sig):
        return f"No qualifying insider purchases ({len(tx)} officer/director trades scanned)."
    d = sig.copy()
    for c in ("ret_6m", "dist_ma200"):
        d[c] = (d[c] * 100).map(lambda v: f"{v:+.0f}%")
    d["total_value"] = d["total_value"].map(lambda v: f"${v / 1e6:.2f}M")
    d["avg_price"] = d["avg_price"].map(lambda v: f"{v:.2f}")
    d["last_close"] = d["last_close"].map(lambda v: f"{v:.2f}")
    cols = ["symbol", "last_filing", "cluster", "n_insiders_30d", "n_buys", "total_value", "avg_price", "last_close", "ret_6m", "dist_ma200", "beaten_down", "ceo_cfo", "buyers"]
    with pd.option_context("display.width", 250, "display.max_columns", None, "display.max_colwidth", 60):
        body = d[cols].to_string(index=False)
    return (body + f"\n\n{len(sig)} symbol(s) with officer/director purchases >= threshold out of {len(tx)} trades scanned. "
            "Rule (docs/research_insiders.md): buy at the next open after the filing, hold ~120 bars; in beaten-down stocks "
            "+10% vs random at 60 bars, +15% at 120, in both 2016-22 and 2023-26. 'cluster' = 2+ distinct insiders within 30 days.")
