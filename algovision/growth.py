"""Long-horizon growth screen.

Ranks the universe on four blocks and explains each pick:

* growth    (40 %) - revenue yoy (latest quarter), 3-year revenue CAGR, EPS yoy, operating-margin change
* quality   (20 %) - operating margin, FCF margin, ROE, low leverage, shrinking share count
* momentum  (25 %) - 12-1 and 6-1 price momentum, above the 200-day MA   (the only backtested block:
                     top-decile momentum beat the universe in both 2016-22 and 2023-26, see docs/research_factors.md)
* valuation (15 %) - PEG and forward P/E, cheaper is better (a sanity check, not a value strategy)

Hard filters: revenue growing year on year, positive free cash flow or operating profit, price data available.
The fundamental blocks are *not* backtested here (Yahoo gives 4 years of history); treat them as a structured
description of the business, and the forward-test journal as the test.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

from algovision.core.pivots import atr

WEIGHTS = {"growth": 0.40, "quality": 0.20, "momentum": 0.25, "valuation": 0.15}


def price_features(frames: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for s, df in frames.items():
        if df is None or len(df) < 260:
            continue
        c = df["Close"].to_numpy(dtype=float)
        ma200 = c[-200:].mean()
        rows.append({"symbol": s, "last_close": c[-1], "ret_12_1": c[-22] / c[-253] - 1.0, "ret_6_1": c[-22] / c[-127] - 1.0,
                     "ret_1m": c[-1] / c[-22] - 1.0, "dist_ma200": c[-1] / ma200 - 1.0, "above_ma200": bool(c[-1] > ma200),
                     "atr_pct": float(atr(df)[-1] / c[-1]), "drawdown_1y": float(c[-1] / c[-252:].max() - 1.0)})
    return pd.DataFrame(rows).set_index("symbol")


def _rank(s: pd.Series, higher_is_better: bool = True) -> pd.Series:
    r = s.rank(pct=True) if higher_is_better else (-s).rank(pct=True)
    return r


def score(fund: pd.DataFrame, price: pd.DataFrame, sectors: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    df = fund.join(price, how="inner")
    # hard filters
    ok = (df["rev_yoy_q"] > 0) & ((df["fcf_margin"] > 0) | (df["op_margin"] > 0)) & df["market_cap"].notna()
    df = df[ok].copy()
    blocks = {
        "growth": [_rank(df["rev_yoy_q"]), _rank(df["rev_cagr_3y"]), _rank(df["eps_yoy_q"]), _rank(df["op_margin_change"])],
        "quality": [_rank(df["op_margin"]), _rank(df["fcf_margin"]), _rank(df["roe"]), _rank(df["debt_to_equity"], False),
                    _rank(df["share_change_1y"], False)],
        "momentum": [_rank(df["ret_12_1"]), _rank(df["ret_6_1"]), df["above_ma200"].astype(float)],
        "valuation": [_rank(df["peg"].where(df["peg"] > 0), False), _rank(df["forward_pe"].where(df["forward_pe"] > 0), False)],
    }
    for name, parts in blocks.items():
        df[f"{name}_score"] = pd.concat(parts, axis=1).mean(axis=1, skipna=True)
    df["score"] = sum(WEIGHTS[k] * df[f"{k}_score"] for k in WEIGHTS)
    if sectors:
        df["sector"] = df.index.map(lambda s: sectors.get(s, "(NASDAQ-only)"))
    # cyclical-spike flag: this year's growth far above the 3-year trend (memory chips, energy, airlines...)
    df["cyclical_flag"] = (df["rev_yoy_q"] > 0.30) & (df["rev_yoy_q"] > 3 * df["rev_cagr_3y"].clip(lower=0.01))
    df["why"] = [explain(r) for _, r in df.iterrows()]
    df = df.sort_values("score", ascending=False)
    # drop duplicate share classes (GOOG/GOOGL, FOX/FOXA...): same market cap and revenue
    df = df[~df.duplicated(subset=["market_cap", "rev_ttm"], keep="first")]
    return df


def _pct(v, d=0):
    return "n/a" if v is None or pd.isna(v) else f"{v * 100:+.{d}f}%"


def explain(r: pd.Series) -> str:
    bits = [f"revenue {_pct(r['rev_yoy_q'])} yoy (3y CAGR {_pct(r['rev_cagr_3y'])})"]
    if pd.notna(r.get("eps_yoy_q")):
        bits.append(f"EPS {_pct(r['eps_yoy_q'])} yoy")
    bits.append(f"op margin {_pct(r['op_margin'])} ({_pct(r['op_margin_change'], 1)} vs last year), FCF margin {_pct(r['fcf_margin'])}")
    if pd.notna(r.get("roe")):
        bits.append(f"ROE {_pct(r['roe'])}")
    bits.append(f"12-1 momentum {_pct(r['ret_12_1'])} ({'above' if r['above_ma200'] else 'below'} 200-day MA, "
                f"{_pct(r['dist_ma200'])}), 1y drawdown {_pct(r['drawdown_1y'])}")
    if bool(r.get("cyclical_flag", False)):
        bits.append("CAUTION: growth far above the 3-year trend, likely a cyclical peak")
    val = []
    if pd.notna(r.get("forward_pe")):
        val.append(f"fwd P/E {r['forward_pe']:.0f}")
    if pd.notna(r.get("peg")):
        val.append(f"PEG {r['peg']:.2f}")
    if val:
        bits.append(", ".join(val))
    return "; ".join(bits)


def top_table(scored: pd.DataFrame, n: int = 20) -> pd.DataFrame:
    cols = ["score", "growth_score", "quality_score", "momentum_score", "valuation_score", "sector", "market_cap",
            "rev_yoy_q", "rev_cagr_3y", "eps_yoy_q", "op_margin", "fcf_margin", "ret_12_1", "dist_ma200", "forward_pe", "peg", "last_close", "why"]
    cols = [c for c in cols if c in scored.columns]
    return scored[cols].head(n)


def format_table(t: pd.DataFrame) -> str:
    d = t.copy()
    for c in ("score", "growth_score", "quality_score", "momentum_score", "valuation_score"):
        if c in d:
            d[c] = d[c].map(lambda v: f"{v:.2f}")
    for c in ("rev_yoy_q", "rev_cagr_3y", "eps_yoy_q", "op_margin", "fcf_margin", "ret_12_1", "dist_ma200"):
        if c in d:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v * 100:+.0f}%")
    if "market_cap" in d:
        d["market_cap"] = d["market_cap"].map(lambda v: "" if pd.isna(v) else f"{v / 1e9:.0f}B")
    for c in ("forward_pe", "peg"):
        if c in d:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.1f}")
    if "last_close" in d:
        d["last_close"] = d["last_close"].map(lambda v: f"{v:.2f}")
    return d.drop(columns=["why"]).to_string()


def diversified_top(scored: pd.DataFrame, n: int = 10, max_per_sector: int = 3) -> pd.DataFrame:
    """Top ``n`` by score with at most ``max_per_sector`` names from one sector."""
    if "sector" not in scored.columns:
        return scored.head(n)
    keep, counts = [], {}
    for sym, r in scored.iterrows():
        sec = r["sector"]
        if counts.get(sec, 0) >= max_per_sector:
            continue
        counts[sec] = counts.get(sec, 0) + 1
        keep.append(sym)
        if len(keep) >= n:
            break
    return scored.loc[keep]
