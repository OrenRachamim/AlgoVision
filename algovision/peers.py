"""Peer groups from price data, and each stock's divergence from its group.

Ported from the full-universe scan in ``research/peers/`` (OrenRachamim/DataStoreApi, branch ``ccr-bafd8b58-nwg5rq``)
and run on the frames AlgoVision already holds:

1. Daily log returns, bad prints dropped; the market factor is the equal-weight mean of all stocks in the frames
   (the scan used RSP, the equal-weight S&P 500 ETF; the universe mean plays the same role here).
2. Market-neutral residuals (each stock minus its beta times the market), their correlation matrix, and Ward
   clustering of the correlation distance into about one group per eight stocks.
3. Per stock: the five closest peers by residual correlation, its group, the mean correlation to the group, beta,
   annualised volatility.
4. Divergence: the stock's return minus beta times the equal-weight basket of the rest of its group, summed over
   the last 20 days, as a z-score against its own last year of such sums. In the scan, stocks more than two
   standard deviations BELOW their peers regained +0.65% relative to them over the next 20 days (t = 2.3, 24
   non-overlapping samples); stocks stretched above their peers showed nothing. Weak evidence: context, not a rule.

The grouping is cached for a week (``peers.json`` in the cache directory); the divergence is recomputed from the
frames on every run, so the numbers in the reports are current while the groups stay stable within a week.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

LOOKBACK = 756          # ~3 years of daily bars for the correlation structure
REL_WIN = 20            # the divergence window
Z_WIN = 252             # the history the z-score is measured against
MAX_ABS_RET = 0.58      # drop daily log moves beyond +/-80% (mis-adjusted splits)
MIN_GROUP = 3


def _returns(frames: Dict[str, pd.DataFrame], lookback: int = LOOKBACK) -> pd.DataFrame:
    close = pd.DataFrame({s: df["Close"].astype(float) for s, df in frames.items() if len(df) >= 260}).sort_index()
    close = close.iloc[-lookback - 1:].ffill(limit=3)
    r = np.log(close).diff().iloc[1:]
    return r.where(r.abs() < MAX_ABS_RET)


def _market_resid(r: pd.DataFrame, mkt: pd.Series):
    x = mkt - mkt.mean()
    xx = float((x * x).sum())
    beta = {}
    E = pd.DataFrame(index=r.index)
    cols = {}
    for s in r.columns:
        y = r[s]
        ok = y.notna()
        b = float((x[ok] * (y[ok] - y[ok].mean())).sum() / (x[ok] * x[ok]).sum()) if ok.sum() > 60 and xx > 0 else 1.0
        beta[s] = b
        cols[s] = y - b * mkt
    E = pd.DataFrame(cols, index=r.index)
    return E, pd.Series(beta)


def build_groups(frames: Dict[str, pd.DataFrame], per_group: int = 8, min_clusters: int = 5) -> Dict:
    """Cluster the stocks in ``frames`` by market-neutral correlation. Returns the serialisable model."""
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import squareform

    r = _returns(frames)
    if r.shape[1] < 2 * MIN_GROUP:
        return {"asof": "", "built": time.time(), "symbols": {}, "groups": {}}
    mkt = r.mean(axis=1)
    E, beta = _market_resid(r, mkt)
    C = E.corr(min_periods=120).fillna(0.0)
    tick = list(C.index)
    Cv = C.values.copy()
    np.fill_diagonal(Cv, 1.0)
    dist = np.sqrt(np.clip(2 * (1 - Cv), 0, None))
    np.fill_diagonal(dist, 0)
    k = max(min_clusters, int(round(len(tick) / per_group)))
    lab = fcluster(linkage(squareform(dist, checks=False), method="ward"), t=k, criterion="maxclust")
    vol = E.std() * np.sqrt(252)
    groups: Dict[int, List[str]] = {}
    for s, g in zip(tick, lab):
        groups.setdefault(int(g), []).append(s)
    np.fill_diagonal(Cv, -np.inf)
    symbols = {}
    for i, s in enumerate(tick):
        members = [m for m in groups[int(lab[i])] if m != s]
        order = np.argsort(-Cv[i])[:5]
        symbols[s] = {"group": int(lab[i]), "peers": [[tick[j], round(float(Cv[i, j]), 2)] for j in order],
                      "group_corr": round(float(np.mean([Cv[i, tick.index(m)] for m in members])), 3) if members else None,
                      "beta": round(float(beta[s]), 2), "vol": round(float(vol[s]), 3)}
    return {"asof": str(r.index[-1].date()), "built": time.time(), "k": k, "n": len(tick),
            "symbols": symbols, "groups": {str(g): m for g, m in groups.items()}}


def divergence(frames: Dict[str, pd.DataFrame], model: Dict, symbols: Optional[List[str]] = None) -> Dict[str, Dict]:
    """Current divergence of each stock from its group: {sym: {z, rel20, ret20, group_ret20, group_ret126, n_group}}."""
    r = _returns(frames, lookback=Z_WIN + REL_WIN + 30)
    close = pd.DataFrame({s: df["Close"].astype(float) for s, df in frames.items() if len(df) >= 260}).sort_index()
    Sf = r.fillna(0.0)
    want = set(symbols) if symbols is not None else set(model.get("symbols", {}))
    out: Dict[str, Dict] = {}
    for g, members in model.get("groups", {}).items():
        members = [m for m in members if m in Sf.columns]
        if len(members) < MIN_GROUP or not (want & set(members)):
            continue
        tot = Sf[members].sum(axis=1)
        for s in members:
            if s not in want:
                continue
            peer = (tot - Sf[s]) / (len(members) - 1)
            pv = float(peer.var())
            b = float(np.cov(Sf[s], peer)[0, 1] / pv) if pv > 0 else 1.0
            rel = Sf[s] - b * peer
            roll = rel.rolling(REL_WIN).sum()
            hist = roll.iloc[:-1].tail(Z_WIN)
            mu, sd = float(hist.mean()), float(hist.std())
            z = (float(roll.iloc[-1]) - mu) / sd if hist.notna().sum() >= 126 and sd > 0 else None
            others = [m for m in members if m != s]
            px = close[others].ffill()
            g20 = float((px.iloc[-1] / px.iloc[-REL_WIN - 1] - 1).mean()) if len(px) > REL_WIN else None
            g126 = float((px.iloc[-1] / px.iloc[-127] - 1).mean()) if len(px) > 126 else None
            c = close[s].ffill()
            out[s] = {"z": round(z, 2) if z is not None else None, "rel20": round(float(np.expm1(roll.iloc[-1])), 4),
                      "ret20": round(float(c.iloc[-1] / c.iloc[-REL_WIN - 1] - 1), 4) if len(c) > REL_WIN else None,
                      "group_ret20": round(g20, 4) if g20 is not None else None,
                      "group_ret126": round(g126, 4) if g126 is not None else None,
                      "n_group": len(members), "top": sorted(others, key=lambda m: -float(close[m].iloc[-1] * 0 + _dollar(frames[m])))[:4]}
    return out


def _dollar(df: pd.DataFrame) -> float:
    """Median 60-day dollar volume, used only to pick the 'largest' members of a group for display."""
    try:
        return float((df["Close"].astype(float) * df["Volume"].astype(float)).tail(60).median())
    except Exception:  # noqa: BLE001
        return 0.0


def load_peers(frames: Dict[str, pd.DataFrame], cache_dir: Optional[Path] = None, max_age_days: float = 7.0,
               symbols: Optional[List[str]] = None, refresh: bool = False) -> Dict[str, Dict]:
    """Per-symbol peer context for the given ``symbols`` (all when None): the cached grouping plus today's divergence.

    {sym: {group, peers, group_corr, beta, vol, z, rel20, ret20, group_ret20, group_ret126, n_group, top}}"""
    p = Path(cache_dir) / "peers.json" if cache_dir else None
    model = None
    if p and p.exists() and not refresh and time.time() - p.stat().st_mtime < max_age_days * 86400:
        try:
            model = json.loads(p.read_text())
            if set(model.get("symbols", {})) != {s for s, df in frames.items() if len(df) >= 260}:
                model = None                      # the universe changed: rebuild
        except Exception:  # noqa: BLE001
            model = None
    if model is None:
        model = build_groups(frames)
        if p:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(model))
    div = divergence(frames, model, symbols)
    out = {}
    for s in (symbols if symbols is not None else list(model.get("symbols", {}))):
        base = model.get("symbols", {}).get(s)
        if not base:
            continue
        out[s] = {**base, **div.get(s, {})}
    return out


def peers_markdown(p: Dict, lang: str = "en") -> List[str]:
    """The 'peers and group' block for one stock, English or Hebrew."""
    he = lang == "he"
    md = ["### עמיתים וקבוצת ההשוואה", ""] if he else []
    peers = ", ".join(f"{s} ({c:.2f})" for s, c in p.get("peers", [])[:5])
    parts = []
    if peers:
        parts.append((f"המניות הקרובות ביותר לפי מתאם ניטרלי לשוק: {peers}" if he else f"Closest by market-neutral correlation: {peers}"))
    if p.get("n_group"):
        top = ", ".join(p.get("top", [])[:4])
        parts.append((f"קבוצת השוואה של {p['n_group']} מניות (הגדולות: {top}), מתאם ממוצע לקבוצה {p.get('group_corr') if p.get('group_corr') is not None else '?'}"
                      if he else f"group of {p['n_group']} stocks (largest: {top}), mean correlation to the group {p.get('group_corr') if p.get('group_corr') is not None else '?'}"))
    if p.get("beta") is not None:
        parts.append((f"בטא {p['beta']:.2f} למדד שווה-המשקל, תנודתיות שאריתית {p['vol'] * 100:.0f}% לשנה" if he
                      else f"beta {p['beta']:.2f} to the equal-weight market, residual volatility {p['vol'] * 100:.0f}% a year"))
    md.append(("" if he else "**Peers and group.** ") + (("; ".join(parts) + ".") if parts else ("אין נתוני עמיתים." if he else "No peer data.")))
    if p.get("ret20") is not None and p.get("group_ret20") is not None:
        z = p.get("z")
        zt = ""
        if z is not None:
            if z <= -2:
                zt = (f" z={z:+.1f}: חריג כלפי מטה (מתחת ל-2-); בסריקה ההיסטורית מניות במצב הזה החזירו בממוצע +0.65% מול העמיתים ב-20 הימים הבאים (t=2.3, ראיה חלשה)."
                      if he else f" z={z:+.1f}: unusually far below its peers (under -2); in the historical scan such stocks regained +0.65% vs peers over the next 20 days (t=2.3, weak evidence).")
            elif z >= 2:
                zt = (f" z={z:+.1f}: חריג כלפי מעלה (מעל 2+); בסריקה ההיסטורית לא נמצא שם אפקט." if he
                      else f" z={z:+.1f}: unusually far above its peers (over +2); the historical scan found no effect there.")
            else:
                zt = f" z={z:+.1f}, בטווח הרגיל." if he else f" z={z:+.1f}, within its normal range."
        line = (f"**20 הימים האחרונים:** המניה {_pct(p['ret20'])}, קבוצת העמיתים {_pct(p['group_ret20'])}, יחסית לקבוצה (מתוקנן בטא) {_pct(p['rel20'])}."
                if he else f"**Last 20 days:** stock {_pct(p['ret20'])}, peer group {_pct(p['group_ret20'])}, relative to the group (beta-adjusted) {_pct(p['rel20'])}.")
        if p.get("group_ret126") is not None:
            line += (f" הקבוצה ב-6 חודשים: {_pct(p['group_ret126'])}." if he else f" The group over 6 months: {_pct(p['group_ret126'])}.")
        md.append(line + zt)
    md.append("")
    return md


def peers_short(p: Optional[Dict], lang: str = "en") -> str:
    """One cell for the summary tables: '-7.1% (z -2.3)' or ''."""
    if not p or p.get("rel20") is None:
        return ""
    z = p.get("z")
    return f"{_pct(p['rel20'])}" + (f" (z {z:+.1f})" if z is not None else "")


def _pct(v, d=1):
    return "" if v is None else f"{v * 100:+.{d}f}%"
