"""Groups as one stock: aggregate each peer group into an equal-weight basket and ask two questions.

1. **Confirmation.** When a single stock gives a signal (a beaten-down falling-wedge breakout), does it do
   better when its peer group, aggregated, is in the same state (beaten down, in a wedge of its own, with
   other members signalling at the same time)? If "the whole group has upside" adds confidence, the forward
   return of confirmed signals should beat the unconfirmed ones in both the train and the test period.
2. **The group itself as the instrument.** Run the same screen on the basket: a beaten-down basket that
   breaks out of a falling wedge. Measure the basket's forward return against random entries in the same
   basket, and the members' forward returns.

Point-in-time groups: for the signals of year Y the groups are built from the three years before Y only
(``algovision.peers.build_groups`` on truncated frames), so no future co-movement leaks into the test.

Baskets: equal-weight, rebalanced daily. Close follows the mean daily return of the members; Open / High / Low
are the mean of the members' open / high / low relative to their own previous close; Volume is the mean of the
members' volume relative to their own 60-day median (times 1e6), so volume ratios on the basket mean the same
thing as on a stock.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig
from algovision.patterns import detect_all
from algovision.peers import build_groups
from algovision.research.events import build_events
from algovision.research.stats import bootstrap_mean_ci

MIN_MEMBERS = 3
BASKET_YEARS = 3            # window of history behind every basket
NEAR = 10                   # bars: a group wedge breakout within this many bars before the stock's signal counts


# ----------------------------------------------------------------------------
# baskets
# ----------------------------------------------------------------------------
def basket_frame(frames: Dict[str, pd.DataFrame], members: Sequence[str], start=None, end=None) -> Optional[pd.DataFrame]:
    """Equal-weight, daily-rebalanced OHLCV index of ``members`` (level 100 at the start). None when too few have data."""
    mem = [m for m in members if m in frames]
    if len(mem) < MIN_MEMBERS:
        return None
    cols = {}
    for k in ("Open", "High", "Low", "Close", "Volume"):
        cols[k] = pd.DataFrame({m: frames[m][k].astype(float) for m in mem}).sort_index()
    idx = cols["Close"].index
    if start is not None:
        idx = idx[idx >= pd.Timestamp(start)]
    if end is not None:
        idx = idx[idx <= pd.Timestamp(end)]
    if len(idx) < 60:
        return None
    for k in cols:
        cols[k] = cols[k].reindex(idx)
    close = cols["Close"].ffill(limit=3)
    prev = close.shift(1)
    present = close.notna() & prev.notna()
    if (present.sum(axis=1) < MIN_MEMBERS).all():
        return None
    ret = (close / prev - 1.0).where(present)
    o_rel = (cols["Open"] / prev - 1.0).where(present)
    h_rel = (cols["High"] / prev - 1.0).where(present)
    l_rel = (cols["Low"] / prev - 1.0).where(present)
    med = cols["Volume"].rolling(60, min_periods=20).median().shift(1)
    v_rel = (cols["Volume"] / med).where(present & med.notna() & (med > 0))
    r = ret.mean(axis=1).fillna(0.0)
    level = 100.0 * np.cumprod(1.0 + r.to_numpy())
    lp = np.concatenate([[100.0], level[:-1]])
    out = pd.DataFrame({
        "Open": lp * (1.0 + o_rel.mean(axis=1).fillna(0.0).to_numpy()),
        "High": lp * (1.0 + h_rel.mean(axis=1).fillna(0.0).to_numpy()),
        "Low": lp * (1.0 + l_rel.mean(axis=1).fillna(0.0).to_numpy()),
        "Close": level,
        "Volume": 1e6 * v_rel.mean(axis=1).fillna(1.0).to_numpy(),
        "n_members": present.sum(axis=1).to_numpy(),
    }, index=idx)
    out["High"] = out[["High", "Open", "Close"]].max(axis=1)
    out["Low"] = out[["Low", "Open", "Close"]].min(axis=1)
    return out


def point_in_time_models(frames: Dict[str, pd.DataFrame], years: Sequence[int], lookback_years: int = 3,
                         per_group: int = 8, min_clusters: int = 5) -> Dict[int, Dict]:
    """For every year, the peer groups built from the ``lookback_years`` before it (nothing from the year itself)."""
    models = {}
    for y in years:
        end = pd.Timestamp(f"{y}-01-01")
        start = pd.Timestamp(f"{y - lookback_years}-01-01")
        sub = {}
        for s, df in frames.items():
            d = df[(df.index >= start) & (df.index < end)]
            if len(d) >= 400:
                sub[s] = d
        models[y] = build_groups(sub, per_group=per_group, min_clusters=min_clusters) if len(sub) >= 2 * MIN_MEMBERS else {"symbols": {}, "groups": {}}
    return models


def context_at(df: pd.DataFrame, i: int) -> Dict:
    """6-month return, distance from the 200-day MA and the beaten-down flag at bar ``i``."""
    c = df["Close"].to_numpy(dtype=float)
    if i < 200:
        return {"ret_126": np.nan, "dist_ma200": np.nan, "beaten": False}
    ret = c[i] / c[max(0, i - 126)] - 1.0
    dist = c[i] / c[i - 199:i + 1].mean() - 1.0
    return {"ret_126": ret, "dist_ma200": dist, "beaten": bool(ret < -0.08 and dist < 0)}


def _divergence_z(frames: Dict[str, pd.DataFrame], symbol: str, members: Sequence[str], date, win: int = 20,
                  hist: int = 252) -> Tuple[float, float]:
    """The stock's ``win``-day return relative to the rest of its group (beta-adjusted) at ``date``, and its z-score
    against the trailing ``hist`` such windows. (nan, nan) when there is not enough history."""
    others = [m for m in members if m != symbol and m in frames]
    if symbol not in frames or len(others) < MIN_MEMBERS - 1:
        return np.nan, np.nan
    close = pd.DataFrame({m: frames[m]["Close"].astype(float) for m in [symbol] + others}).sort_index()
    close = close[close.index <= pd.Timestamp(date)].tail(hist + win + 40).ffill(limit=3)
    r = np.log(close).diff().iloc[1:]
    r = r.where(r.abs() < 0.58).fillna(0.0)
    if len(r) < 200:
        return np.nan, np.nan
    peer = r[others].mean(axis=1)
    pv = float(peer.var())
    b = float(np.cov(r[symbol], peer)[0, 1] / pv) if pv > 0 else 1.0
    roll = (r[symbol] - b * peer).rolling(win).sum()
    h = roll.iloc[:-1].tail(hist)
    sd = float(h.std())
    rel = float(np.expm1(roll.iloc[-1]))
    return rel, ((float(roll.iloc[-1]) - float(h.mean())) / sd if h.notna().sum() >= 126 and sd > 0 else np.nan)


# ----------------------------------------------------------------------------
# group-level signals and events
# ----------------------------------------------------------------------------
def group_wedges(basket: pd.DataFrame, cfg: DetectorConfig) -> Dict[str, List]:
    """Falling-wedge matches on a basket: confirmed breakout dates and (start, end) of every forming/confirmed wedge."""
    matches = [m for m in detect_all(basket, symbol="basket", patterns=["Falling Wedge"], config=cfg) if m.pattern == "Falling Wedge"]
    idx = basket.index
    out = {"breakouts": [], "wedges": [], "matches": matches}
    for m in matches:
        if m.status == "confirmed" and m.breakout_idx is not None:
            out["breakouts"].append(idx[int(m.breakout_idx)])
        if m.status in ("forming", "confirmed"):
            out["wedges"].append((idx[m.start_idx], idx[min(m.end_idx, len(idx) - 1)]))
    return out


def group_events(frames: Dict[str, pd.DataFrame], models: Dict[int, Dict], spy: Optional[pd.DataFrame],
                 cfg: DetectorConfig, horizons: Sequence[int] = (5, 20, 60), progress=None) -> Tuple[pd.DataFrame, Dict]:
    """Falling-wedge events on every point-in-time basket (signals in the model's year only), with the basket's
    forward return vs random entries in the same basket, and the members' mean forward return.

    Also returns ``wedge_index[(year, group)] = {"breakouts", "wedges", "members"}`` for the confirmation study."""
    rows: List[Dict] = []
    wedge_index: Dict[Tuple[int, str], Dict] = {}
    years = sorted(models)
    for k, y in enumerate(years):
        model = models[y]
        y0, y1 = pd.Timestamp(f"{y - BASKET_YEARS}-01-01"), pd.Timestamp(f"{y}-12-31")
        for gid, members in model.get("groups", {}).items():
            basket = basket_frame(frames, members, y0, y1)
            if basket is None or len(basket) < 300:
                continue
            w = group_wedges(basket, cfg)
            wedge_index[(y, gid)] = {"breakouts": w["breakouts"], "wedges": w["wedges"], "members": list(members)}
            ev, _ = build_events(f"G{y}-{gid}", basket, spy, cfg, horizons=horizons, matches=w["matches"], random_draws=20)
            for e in ev:
                d = pd.Timestamp(e["signal_date"])
                if d.year != y:
                    continue
                i = e["signal_idx"]
                e.update({"year": y, "group": gid, "n_members": int(basket["n_members"].iloc[i])})
                e.update({f"g_{a}": b for a, b in context_at(basket, i).items()})
                # members' own forward returns from the next open, and how many of them were beaten down
                mem_ret, beaten = {h: [] for h in horizons}, 0
                for m in members:
                    df = frames.get(m)
                    if df is None:
                        continue
                    j = df.index.searchsorted(d)
                    if j >= len(df) or df.index[j] != d or j + 1 >= len(df):
                        continue
                    o = float(df["Open"].iloc[j + 1])
                    c = df["Close"].to_numpy(dtype=float)
                    for h in horizons:
                        if j + h < len(df):
                            mem_ret[h].append(c[j + h] / o - 1.0)
                    beaten += context_at(df, j)["beaten"]
                for h in horizons:
                    e[f"mem_ret_{h}"] = float(np.mean(mem_ret[h])) if mem_ret[h] else np.nan
                    e[f"mem_hit_{h}"] = float(np.mean([x > 0 for x in mem_ret[h]])) if mem_ret[h] else np.nan
                e["share_beaten"] = beaten / max(1, len(members))
                rows.append(e)
        if progress:
            progress(k + 1, len(years), len(rows))
    return pd.DataFrame(rows), wedge_index


# ----------------------------------------------------------------------------
# confirmation features for stock-level events
# ----------------------------------------------------------------------------
def confirmation_features(events: pd.DataFrame, frames: Dict[str, pd.DataFrame], models: Dict[int, Dict],
                          wedge_index: Dict, progress=None) -> pd.DataFrame:
    """Add to every stock event: the group's state at the signal (beaten-down basket, basket wedge nearby, share of
    members beaten down, members signalling within +-NEAR bars, the stock's divergence from the group)."""
    ev = events.copy()
    ev["signal_ts"] = pd.to_datetime(ev["signal_date"])
    cols = {c: [] for c in ("group", "n_members", "g_ret_126", "g_dist_ma200", "g_beaten", "g_wedge_breakout", "g_in_wedge",
                            "share_beaten", "co_signals", "share_co_signals", "rel20_vs_group", "z_vs_group")}
    by_sym_date = {}
    for s, d in zip(ev["symbol"], ev["signal_ts"]):
        by_sym_date.setdefault(s, []).append(d)
    baskets: Dict[Tuple[int, str], Optional[pd.DataFrame]] = {}
    for n, (i, e) in enumerate(ev.iterrows()):
        y, s, d = int(e["year"]), e["symbol"], e["signal_ts"]
        model = models.get(y) or {}
        info = (model.get("symbols") or {}).get(s)
        gid = str(info["group"]) if info else None
        members = (model.get("groups") or {}).get(gid, []) if gid else []
        vals = dict.fromkeys(cols, np.nan)
        vals.update({"group": gid or "", "n_members": len(members), "g_beaten": False, "g_wedge_breakout": False, "g_in_wedge": False})
        if gid and len(members) >= MIN_MEMBERS:
            key = (y, gid)
            if key not in baskets:
                baskets[key] = basket_frame(frames, members, pd.Timestamp(f"{y - BASKET_YEARS}-01-01"), pd.Timestamp(f"{y}-12-31"))
            b = baskets[key]
            if b is not None:
                j = b.index.searchsorted(d)
                if j < len(b) and b.index[j] == d:
                    cx = context_at(b, j)
                    vals.update({"g_ret_126": cx["ret_126"], "g_dist_ma200": cx["dist_ma200"], "g_beaten": cx["beaten"]})
                    w = wedge_index.get(key)
                    if w:
                        lo = b.index[max(0, j - NEAR)]
                        vals["g_wedge_breakout"] = any(lo <= bd <= d for bd in w["breakouts"])
                        vals["g_in_wedge"] = any(ws <= d <= we for ws, we in w["wedges"])
            beaten = 0
            co = 0
            for m in members:
                df = frames.get(m)
                if df is None or m == s:
                    continue
                j = df.index.searchsorted(d)
                if j < len(df):
                    beaten += context_at(df, min(j, len(df) - 1))["beaten"]
                for od in by_sym_date.get(m, []):
                    if abs((od - d).days) <= NEAR * 1.5:
                        co += 1
                        break
            vals["share_beaten"] = beaten / max(1, len(members) - 1)
            vals["co_signals"] = co
            vals["share_co_signals"] = co / max(1, len(members) - 1)
            vals["rel20_vs_group"], vals["z_vs_group"] = _divergence_z(frames, s, members, d)
        for c in cols:
            cols[c].append(vals[c])
        if progress and (n % 500 == 0 or n == len(ev) - 1):
            progress(n + 1, len(ev))
    for c, v in cols.items():
        ev[c] = v
    return ev


# ----------------------------------------------------------------------------
# tables
# ----------------------------------------------------------------------------
def _stats(g: pd.DataFrame, h: int = 20, ret_col: str = "ret", x_col: str = "xrand") -> Dict:
    if f"{ret_col}_{h}" not in g:
        return {"n": 0, "ret": np.nan, "hit": np.nan, "excess": np.nan, "lo": np.nan, "hi": np.nan}
    r = g[f"{ret_col}_{h}"].to_numpy(dtype=float)
    x = g[f"{x_col}_{h}"].to_numpy(dtype=float) if f"{x_col}_{h}" in g else np.full(len(r), np.nan)
    ok = np.isfinite(r)
    r = r[ok]
    x = x[ok]
    if len(r) == 0:
        return {"n": 0, "ret": np.nan, "hit": np.nan, "excess": np.nan, "lo": np.nan, "hi": np.nan}
    xs = x[np.isfinite(x)]
    lo, hi = bootstrap_mean_ci(xs, reps=500) if len(xs) > 1 else (np.nan, np.nan)
    return {"n": int(len(r)), "ret": float(r.mean()), "hit": float((r > 0).mean()),
            "excess": float(xs.mean()) if len(xs) else np.nan, "lo": lo, "hi": hi}


def condition_table(ev: pd.DataFrame, split: str, conditions: Dict[str, pd.Series], h: int = 20) -> pd.DataFrame:
    """For every named condition: n / return / hit / excess (with CI) when true and when false, train and test."""
    d = pd.to_datetime(ev["signal_date"])
    rows = []
    for name, cond in conditions.items():
        cond = cond.fillna(False).astype(bool)
        for period, mask in (("train", d < split), ("test", d >= split)):
            for state, sel in (("yes", cond), ("no", ~cond)):
                st = _stats(ev[mask & sel], h)
                rows.append({"condition": name, "period": period, "state": state, **st})
    return pd.DataFrame(rows)


def findings_table(ev: pd.DataFrame, split: str, conditions: Dict[str, pd.Series], h: int = 20, h2: int = 60) -> pd.DataFrame:
    """Per condition: the excess of *yes* minus *no* in train and test at ``h`` and ``h2`` bars, and in how many years
    the ``h``-bar difference was positive. Consistent = positive in both periods at ``h`` with at least +0.5%."""
    d = pd.to_datetime(ev["signal_date"])
    rows = []
    for name, cond in conditions.items():
        cond = cond.fillna(False).astype(bool)
        r = {"condition": name}
        for period, mask in (("train", d < split), ("test", d >= split)):
            for hh in (h, h2):
                a, b = _stats(ev[mask & cond], hh), _stats(ev[mask & ~cond], hh)
                r[f"{period}_diff_{hh}"] = a["excess"] - b["excess"] if a["n"] and b["n"] else np.nan
                r[f"{period}_n_yes_{hh}"] = a["n"]
        pos = tot = 0
        for y, g in ev.groupby(d.dt.year):
            a, b = _stats(g[cond.loc[g.index]], h), _stats(g[~cond.loc[g.index]], h)
            if a["n"] >= 5 and b["n"] >= 5:
                tot += 1
                pos += (a["excess"] - b["excess"]) > 0
        r["years_positive"] = f"{pos}/{tot}"
        r["consistent"] = bool(np.isfinite(r[f"train_diff_{h}"]) and np.isfinite(r[f"test_diff_{h}"])
                               and r[f"train_diff_{h}"] >= 0.005 and r[f"test_diff_{h}"] >= 0.005)
        rows.append(r)
    return pd.DataFrame(rows)


def _fmt_findings(t: pd.DataFrame, h: int, h2: int) -> str:
    lines = [f"| condition | yes - no, train ({h} bars) | yes - no, test ({h} bars) | yes - no, train ({h2} bars) | yes - no, test ({h2} bars) | years positive ({h} bars) | consistent |",
             "|---|---|---|---|---|---|---|"]
    f = lambda v: "" if not np.isfinite(v) else f"{v * 100:+.2f}%"
    for r in t.itertuples():
        lines.append(f"| {r.condition} | {f(getattr(r, f'train_diff_{h}'))} (n={getattr(r, f'train_n_yes_{h}')}) | {f(getattr(r, f'test_diff_{h}'))} (n={getattr(r, f'test_n_yes_{h}')}) | "
                     f"{f(getattr(r, f'train_diff_{h2}'))} | {f(getattr(r, f'test_diff_{h2}'))} | {r.years_positive} | {'**yes**' if r.consistent else 'no'} |")
    return "\n".join(lines)


def _fmt(t: pd.DataFrame, h: int) -> str:
    lines = [f"| condition | period | state | n | {h}-bar return | hit | excess over random (95% CI) |", "|---|---|---|---|---|---|---|"]
    for r in t.itertuples():
        if r.n == 0:
            lines.append(f"| {r.condition} | {r.period} | {r.state} | 0 | | | |")
            continue
        lines.append(f"| {r.condition} | {r.period} | {r.state} | {r.n} | {r.ret * 100:+.2f}% | {r.hit * 100:.0f}% | "
                     f"{r.excess * 100:+.2f}% ({r.lo * 100:+.1f} to {r.hi * 100:+.1f}) |")
    return "\n".join(lines)


def write_groups_report(out_dir: Path, stock_ev: pd.DataFrame, grp_ev: pd.DataFrame, split: str, h: int = 20,
                        doc_path: Optional[Path] = None) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stock_ev.to_csv(out / "stock_events_with_group.csv", index=False)
    grp_ev.to_csv(out / "group_events.csv", index=False)
    md = ["# Groups as one stock: does the peer group confirm a signal, and is the group itself a signal?", "",
          f"Tables: `{out}/`. Reproduce with `python -m algovision research-groups`.", "",
          "Peer groups are built point-in-time (from the three years before each signal's year, "
          "`algovision/peers.py`), aggregated into equal-weight daily-rebalanced baskets (`algovision/research/groups.py`), "
          f"and the falling-wedge screen is run on stocks and on baskets alike. Train = signals before {split}, test = after. "
          "Excess = return over random entries in the same stock (or basket) over the same holding period.", ""]
    beaten = stock_ev[(stock_ev["ret_126"] < -0.08) & (stock_ev["dist_ma200"] < 0)]
    md += ["## 1. Confirmation by the group (stock-level beaten-down falling-wedge breakouts)", "",
           f"{len(beaten)} beaten-down wedge breakouts in stocks with a point-in-time group ({(beaten['n_members'] >= MIN_MEMBERS).sum()} "
           "with a group of 3+ members). Conditions:", "",
           "- **group beaten down**: the basket itself has a 6-month return below -8% and is below its 200-day MA at the signal.",
           f"- **group wedge breakout**: the basket broke out of its own falling wedge within the {NEAR} bars before the signal.",
           "- **group in a wedge**: the basket is inside a forming or confirmed falling wedge at the signal.",
           "- **most members beaten down**: more than half of the other members are beaten down.",
           f"- **another member signalled**: at least one other member had a wedge breakout within about {NEAR} bars.",
           "- **stock below its group (z < -1)**: the stock's 20-day return relative to the group is more than one standard deviation under its norm.",
           "- **stock above its group (z > +1)**: the opposite.", ""]
    b = beaten[beaten["n_members"] >= MIN_MEMBERS]
    conds = {"group beaten down": b["g_beaten"], "group wedge breakout": b["g_wedge_breakout"], "group in a wedge": b["g_in_wedge"],
             "most members beaten down": b["share_beaten"] > 0.5, "another member signalled": b["co_signals"] >= 1,
             "stock below its group (z < -1)": b["z_vs_group"] < -1, "stock above its group (z > +1)": b["z_vs_group"] > 1,
             "group beaten down AND group wedge breakout": b["g_beaten"] & b["g_wedge_breakout"],
             "group beaten down OR most members beaten down": b["g_beaten"] | (b["share_beaten"] > 0.5)}
    t1 = condition_table(b, split, conds, h)
    t1.to_csv(out / "confirmation.csv", index=False)
    md += [_fmt(t1, h), ""]
    fnd = findings_table(b, split, conds, h, 60)
    fnd.to_csv(out / "findings.csv", index=False)
    md += ["### Is any condition consistent?", "",
           "The difference between the *yes* and the *no* rows (excess over random), train and test, at 20 and at 60 bars, "
           "and the number of years (with 5+ signals on each side) in which the 20-bar difference was positive. "
           "\"Consistent\" = at least +0.5% in both periods at 20 bars.", "", _fmt_findings(fnd, h, 60), ""]
    # the same for all wedge breakouts (not only beaten-down), as a robustness check
    a = stock_ev[stock_ev["n_members"] >= MIN_MEMBERS]
    conds_all = {"group beaten down": a["g_beaten"], "group wedge breakout": a["g_wedge_breakout"],
                 "another member signalled": a["co_signals"] >= 1, "stock below its group (z < -1)": a["z_vs_group"] < -1}
    t1b = condition_table(a, split, conds_all, h)
    t1b.to_csv(out / "confirmation_all_wedges.csv", index=False)
    md += ["Robustness: the same conditions on **all** wedge breakouts (beaten-down or not):", "", _fmt(t1b, h), ""]
    md += ["## 2. The group as the instrument (falling-wedge breakouts on the baskets)", ""]
    if len(grp_ev):
        gb = grp_ev[grp_ev["g_beaten"]]
        d = pd.to_datetime(grp_ev["signal_date"])
        rows = []
        for name, sel in (("all basket breakouts", np.ones(len(grp_ev), bool)), ("beaten-down baskets", grp_ev["g_beaten"].to_numpy(bool)),
                          ("beaten-down baskets, most members beaten", (grp_ev["g_beaten"] & (grp_ev["share_beaten"] > 0.5)).to_numpy(bool))):
            for period, mask in (("train", (d < split).to_numpy()), ("test", (d >= split).to_numpy())):
                g = grp_ev[sel & mask]
                st = _stats(g, h)
                mem = g[f"mem_ret_{h}"].to_numpy(dtype=float)
                mem = mem[np.isfinite(mem)]
                rows.append({"set": name, "period": period, "n": st["n"], "basket_ret": st["ret"], "basket_hit": st["hit"],
                             "basket_excess": st["excess"], "lo": st["lo"], "hi": st["hi"],
                             "members_ret": float(mem.mean()) if len(mem) else np.nan,
                             "members_hit": float(g[f"mem_hit_{h}"].mean()) if len(g) else np.nan})
        t2 = pd.DataFrame(rows)
        t2.to_csv(out / "group_as_instrument.csv", index=False)
        lines = [f"| set | period | n | basket {h}-bar return | basket hit | basket excess over random (95% CI) | members' mean {h}-bar return | members' hit |",
                 "|---|---|---|---|---|---|---|---|"]
        for r in t2.itertuples():
            if r.n == 0:
                lines.append(f"| {r.set} | {r.period} | 0 | | | | | |")
            else:
                lines.append(f"| {r.set} | {r.period} | {r.n} | {r.basket_ret * 100:+.2f}% | {r.basket_hit * 100:.0f}% | "
                             f"{r.basket_excess * 100:+.2f}% ({r.lo * 100:+.1f} to {r.hi * 100:+.1f}) | {r.members_ret * 100:+.2f}% | {r.members_hit * 100:.0f}% |")
        md += [f"{len(grp_ev)} basket breakouts, {len(gb)} in beaten-down baskets.", "", "\n".join(lines), ""]
    else:
        md += ["no basket events", ""]
    md += ["## 3. Reading", "", "A condition counts only if the *yes* rows beat the *no* rows in excess return in **both** periods "
           "with a meaningful size (about +1% or more over 20 bars) and a usable sample. Everything else is noise, however "
           "good it looks in one period.", "",
           "Systematic screens and an event study on today's index members (survivorship bias), not investment advice.", ""]
    text = "\n".join(md)
    (out / "README.md").write_text(text, encoding="utf-8")
    if doc_path:
        Path(doc_path).write_text(text, encoding="utf-8")
    return out / "README.md"


# ----------------------------------------------------------------------------
# live: the state of each stock's group today, and groups meeting the screen
# ----------------------------------------------------------------------------
def group_context_today(frames: Dict[str, pd.DataFrame], model: Dict, symbols: Sequence[str],
                        cfg: Optional[DetectorConfig] = None) -> Dict[str, Dict]:
    """For every listed symbol: is its peer group, as a basket, beaten down; what share of the other members are; and
    is the basket in / just out of a falling wedge. Context for the reports (tested in docs/research_groups.md)."""
    cfg = cfg or DetectorConfig(recent_bars=NEAR)
    want = set(symbols)
    out: Dict[str, Dict] = {}
    for gid, members in model.get("groups", {}).items():
        hit = [s for s in members if s in want]
        if not hit or len(members) < MIN_MEMBERS:
            continue
        b = basket_frame(frames, members)
        if b is None or len(b) < 260:
            continue
        cx = context_at(b, len(b) - 1)
        beaten_members = {m: context_at(frames[m], len(frames[m]) - 1)["beaten"] for m in members if m in frames and len(frames[m]) >= 200}
        w = group_wedges(b, cfg)
        last = b.index[-1]
        status, bo = "", ""
        for m in w["matches"]:
            if m.status in ("forming", "confirmed") and len(b) - 1 - m.end_idx <= NEAR:
                status = m.status
                bo = str(b.index[m.breakout_idx].date()) if m.breakout_idx is not None else ""
                break
        recent_bo = any((last - d).days <= NEAR * 1.5 for d in w["breakouts"])
        for s in hit:
            others = [m for m in beaten_members if m != s]
            out[s] = {"g_beaten": cx["beaten"], "g_ret_126": cx["ret_126"], "g_dist_ma200": cx["dist_ma200"],
                      "share_beaten": float(np.mean([beaten_members[m] for m in others])) if others else np.nan,
                      "g_wedge": status, "g_breakout": bo, "g_wedge_breakout": bool(recent_bo), "n_group": len(members)}
    return out


def group_signals_today(frames: Dict[str, pd.DataFrame], model: Dict, cfg: Optional[DetectorConfig] = None,
                        recent: int = 5) -> List[Dict]:
    """Groups whose basket is beaten down and in / just out of a falling wedge at the last bar."""
    cfg = cfg or DetectorConfig(filter_max_ret_126=-0.08, filter_below_ma200=True, recent_bars=recent)
    out = []
    for gid, members in model.get("groups", {}).items():
        b = basket_frame(frames, members)
        if b is None or len(b) < 260:
            continue
        cx = context_at(b, len(b) - 1)
        if not cx["beaten"]:
            continue
        for m in detect_all(b, symbol=f"G{gid}", patterns=["Falling Wedge"], config=cfg):
            if m.status not in ("forming", "confirmed") or len(b) - 1 - m.end_idx > recent:
                continue
            out.append({"group": gid, "status": m.status, "score": round(m.score, 2), "start": str(b.index[m.start_idx].date()),
                        "breakout": str(b.index[m.breakout_idx].date()) if m.breakout_idx is not None else "",
                        "n_members": len(members), "members": list(members), "ret_126": cx["ret_126"], "dist_ma200": cx["dist_ma200"],
                        "share_beaten": float(np.mean([context_at(frames[x], len(frames[x]) - 1)["beaten"] for x in members if x in frames]))})
            break
    return sorted(out, key=lambda r: (r["status"] != "confirmed", -r["score"]))
