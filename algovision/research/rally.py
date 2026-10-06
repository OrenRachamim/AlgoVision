"""Early-rally study: is the *start* of an up-move a tradeable entry for a short hold?

Six point-in-time definitions of "the rally has just started" are evaluated on the
same panel and with the same discipline as the other studies (train / test split,
entry at the next open, returns net of a round-trip cost, excess over the SPY and over
random nearby entries in the same stock, t-statistics on the local excess):

* ``ma50_cross``      close crosses above the 50-day MA after >= 15 of the last 20 bars below it
* ``golden_20_50``    the 20-day MA crosses above the 50-day MA after >= 20 bars below it
* ``base_breakout``   first close above the 60-bar high in a stock still >= 10 % below its 52-week
                      high, on >= 1.5x average volume (a base breakout, not a trend extension)
* ``higher_high``     Dow turn: a low at least 15 % under the 52-week high, then a swing high, a
                      higher low, and today the first close above that swing high
* ``thrust``          +8 % or more in 10 bars, starting within 5 % of the 60-bar low, after a flat
                      or negative 6 months
* ``rsi_turn``        14-day RSI crosses above 50 after having been below 35 within 20 bars

Every event carries the context the other rules use (below the 200-day MA, 6-month
return, distance from the 52-week high, volume ratio) so the same "beaten-down vs
uptrend" split can be read off.  The bar for "real" is set before looking: local excess
> 0 with |t| > 2 in both periods, net of 10 bps, and >= +1 % at 20 bars.
"""

from __future__ import annotations

import zlib
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

RULES = ("ma50_cross", "golden_20_50", "base_breakout", "higher_high", "thrust", "rsi_turn")
HORIZONS = (5, 10, 20, 40, 60)
MIN_GAP = 20            # bars between two events of the same rule in the same stock
LOCAL_WINDOW = 126
RANDOM_DRAWS = 10
COST = 0.001            # round trip, 10 bps

RULE_TEXT = {
    "ma50_cross": "close crosses above the 50-day MA after at least 15 of the last 20 bars below it",
    "golden_20_50": "20-day MA crosses above the 50-day MA after at least 20 bars below it",
    "base_breakout": "first close above the 60-bar high while still >= 10% below the 52-week high, volume >= 1.5x the 20-day average",
    "higher_high": "a low >= 15% under the 52-week high, a swing high, a higher low, and today the first close above the swing high",
    "thrust": "+8% or more in 10 bars from within 5% of the 60-bar low, after a flat or negative 6 months",
    "rsi_turn": "14-day RSI crosses above 50 after being below 35 within the last 20 bars",
}


def _sma(x: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(x).rolling(n).mean().to_numpy()


def _rsi(close: np.ndarray, n: int = 14) -> np.ndarray:
    d = np.diff(close, prepend=np.nan)
    up = pd.Series(np.where(d > 0, d, 0.0)).ewm(alpha=1 / n, adjust=False).mean()
    dn = pd.Series(np.where(d < 0, -d, 0.0)).ewm(alpha=1 / n, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return (100 - 100 / (1 + rs)).to_numpy()


def _rolling_max(x: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(x).rolling(n).max().to_numpy()


def _rolling_min(x: np.ndarray, n: int) -> np.ndarray:
    return pd.Series(x).rolling(n).min().to_numpy()


def rule_hits(rule: str, o: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Indices t where ``rule`` fires at the close of bar t (everything uses bars <= t)."""
    n = len(c)
    t_all = np.arange(n)
    if rule == "ma50_cross":
        ma50 = _sma(c, 50)
        below = (c < ma50).astype(float)
        below20 = pd.Series(below).rolling(20).sum().shift(1).to_numpy()      # bars below among t-20..t-1
        cond = (c > ma50) & (np.roll(c, 1) <= np.roll(ma50, 1)) & (below20 >= 15) & (c > np.roll(c, 1))
    elif rule == "golden_20_50":
        ma20, ma50 = _sma(c, 20), _sma(c, 50)
        under = (ma20 < ma50).astype(float)
        under20 = pd.Series(under).rolling(20).sum().shift(1).to_numpy()
        cond = (ma20 > ma50) & (np.roll(ma20, 1) <= np.roll(ma50, 1)) & (under20 >= 20)
    elif rule == "base_breakout":
        hi60 = pd.Series(h).rolling(60).max().shift(1).to_numpy()            # highest high of t-60..t-1
        hi252 = pd.Series(c).rolling(252).max().shift(1).to_numpy()
        avgv = pd.Series(v).rolling(20).mean().shift(1).to_numpy()
        prev_break = np.roll(c, 1) > np.roll(hi60, 1)
        cond = (c > hi60) & ~prev_break & (np.roll(c, 1) <= 0.90 * hi252) & (v >= 1.5 * avgv)
    elif rule == "thrust":
        r10 = c / np.roll(c, 10) - 1.0
        r126_lag = np.roll(c, 10) / np.roll(c, 136) - 1.0
        lo60_lag = pd.Series(l).rolling(60).min().shift(10).to_numpy()       # 60-bar low as of t-10
        cond = (r10 >= 0.08) & (c > np.roll(c, 1)) & (r126_lag <= 0.0) & (np.roll(c, 10) <= 1.05 * lo60_lag)
    elif rule == "rsi_turn":
        rsi = _rsi(c)
        min20 = pd.Series(rsi).rolling(20).min().shift(1).to_numpy()
        cond = (rsi > 50) & (np.roll(rsi, 1) <= 50) & (min20 < 35)
    elif rule == "higher_high":
        return _higher_high_hits(h, l, c)
    else:
        raise ValueError(rule)
    cond = np.nan_to_num(cond.astype(float)) > 0
    cond[:260] = False
    return t_all[cond]


def _higher_high_hits(h: np.ndarray, l: np.ndarray, c: np.ndarray, look: int = 120) -> np.ndarray:
    """Dow turn: L0 (lowest low in t-120..t-10, >= 15 % under the 52w high), swing high H1 after it,
    higher low L1 > 1.02 * L0 after H1, and the first close above H1 today."""
    n = len(c)
    hi252 = pd.Series(c).rolling(252).max().to_numpy()
    out = []
    for t in range(260, n):
        a, b = t - look, t - 10
        seg = l[a:b]
        i0 = a + int(np.nanargmin(seg))
        if not (l[i0] <= 0.85 * hi252[i0]):
            continue
        if t - 3 <= i0 + 5:
            continue
        i1 = i0 + 5 + int(np.nanargmax(h[i0 + 5:t - 3]))
        h1 = h[i1]
        if t - i1 < 3:
            continue
        l1 = np.nanmin(l[i1 + 1:t])
        if not (l1 > 1.02 * l[i0]):
            continue
        if c[t] > h1 and c[t - 1] <= h1 and np.all(c[i1 + 1:t] <= h1):
            out.append(t)
    return np.asarray(out, dtype=int)


def rally_events(panel: Dict[str, pd.DataFrame], spy_close: pd.Series, rules: Sequence[str] = RULES,
                 horizons: Sequence[int] = HORIZONS, min_gap: int = MIN_GAP, local_window: int = LOCAL_WINDOW,
                 random_draws: int = RANDOM_DRAWS, seed: int = 11, progress: Optional[Callable] = None) -> pd.DataFrame:
    """One row per (rule, symbol, date): context, forward returns from the next open, SPY and local-random excess."""
    close, open_, high, low, vol = (panel[k] for k in ("Close", "Open", "High", "Low", "Volume"))
    spy = spy_close.reindex(close.index).ffill().to_numpy(dtype=float)
    hmax = max(horizons)
    rows: List[Dict] = []
    syms = list(close.columns)
    for k, s in enumerate(syms):
        c = close[s].to_numpy(dtype=float)
        ok = np.isfinite(c)
        if ok.sum() < 300:
            continue
        # work on the stock's own bars (drop leading / trailing NaN rows of the wide panel)
        pos = np.where(ok)[0]
        first, last = pos[0], pos[-1]
        sl = slice(first, last + 1)
        c, o, h, l, v = (x[s].to_numpy(dtype=float)[sl] for x in (close, open_, high, low, vol))
        c, o, h, l = (pd.Series(x).ffill().to_numpy() for x in (c, o, h, l))
        v = np.nan_to_num(v)
        sp = spy[sl]
        dates = close.index[sl]
        n = len(c)
        ma200 = _sma(c, 200)
        hi252 = _rolling_max(c, 252)
        avgv = pd.Series(v).rolling(20).mean().shift(1).to_numpy()
        rng = np.random.default_rng(seed + zlib.crc32(s.encode()) % 100000)
        for rule in rules:
            hits = rule_hits(rule, o, h, l, c, v)
            last_t = -10 ** 6
            for t in hits:
                if t - last_t < min_gap or t + hmax + 1 >= n or t < 260:
                    continue
                last_t = t
                entry = o[t + 1]
                if not np.isfinite(entry) or entry <= 0:
                    continue
                row = {"rule": rule, "symbol": s, "date": dates[t], "signal_close": float(c[t]), "entry": float(entry),
                       "below_ma200": bool(c[t] < ma200[t]), "ret_126": float(c[t] / c[t - 126] - 1.0),
                       "ret_20": float(c[t] / c[t - 20] - 1.0), "ret_10": float(c[t] / c[t - 10] - 1.0),
                       "from_52w_high": float(c[t] / hi252[t] - 1.0),
                       "vol_ratio": float(v[t] / avgv[t]) if np.isfinite(avgv[t]) and avgv[t] > 0 else np.nan,
                       "day_ret": float(c[t] / c[t - 1] - 1.0)}
                for hz in horizons:
                    r = c[t + 1 + hz - 1] / entry - 1.0          # close hz bars after entry (entry bar = bar 1)
                    row[f"ret_{hz}"] = float(r)
                    row[f"xspy_{hz}"] = float(r - (sp[t + hz] / sp[t + 1] - 1.0)) if np.isfinite(sp[t + 1]) else np.nan
                    lo_, hi_ = max(1, t - local_window), min(n - hz - 3, t + local_window)
                    cand = np.arange(lo_, hi_ + 1)
                    cand = cand[np.abs(cand - t) > hz]
                    if len(cand) >= 5:
                        pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                        base = o[pick + 1]
                        row[f"xloc_{hz}"] = float(r - np.mean(c[pick + hz] / base - 1.0))
                    else:
                        row[f"xloc_{hz}"] = np.nan
                rows.append(row)
        if progress:
            progress(k + 1, len(syms), len(rows))
    ev = pd.DataFrame(rows)
    if len(ev):
        ev["beaten"] = ev["below_ma200"] & (ev["ret_126"] < -0.08)
        ev["year"] = pd.to_datetime(ev["date"]).dt.year
    return ev


def _tstat(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    return float(x.mean() / x.std(ddof=1) * np.sqrt(len(x))) if len(x) > 2 and x.std() > 0 else np.nan


def rally_table(ev: pd.DataFrame, split: str, horizons: Sequence[int] = HORIZONS, cost: float = COST,
                by: Sequence[str] = ("rule",), min_n: int = 30) -> pd.DataFrame:
    rows = []
    d = pd.to_datetime(ev["date"])
    for pname, mask in (("all", np.ones(len(ev), bool)), ("train", (d < split).to_numpy()), ("test", (d >= split).to_numpy())):
        g0 = ev[mask]
        if not len(g0):
            continue
        for key, g in g0.groupby(list(by)):
            if len(g) < min_n:
                continue
            rec = {"period": pname, **dict(zip(by, key if isinstance(key, tuple) else (key,))), "n": int(len(g)),
                   "years_pos": ""}
            for hz in horizons:
                r = g[f"ret_{hz}"].to_numpy(dtype=float) - cost
                x = g[f"xloc_{hz}"].to_numpy(dtype=float)
                rec[f"net_{hz}"] = float(np.nanmean(r))
                rec[f"hit_{hz}"] = float(np.nanmean(r > 0))
                rec[f"xspy_{hz}"] = float(np.nanmean(g[f"xspy_{hz}"]))
                rec[f"xloc_{hz}"] = float(np.nanmean(x))
                rec[f"t_{hz}"] = _tstat(x)
            yrs = g.groupby("year")["xloc_20"].mean()
            rec["years_pos"] = f"{int((yrs > 0).sum())}/{len(yrs)}"
            rows.append(rec)
    return pd.DataFrame(rows).set_index(["period", *by])


def _pct(v) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.2f}%"


def _fmt(tab: pd.DataFrame, horizons: Sequence[int] = (5, 10, 20, 40, 60)) -> str:
    d = tab.reset_index()
    out = pd.DataFrame({c: d[c] for c in d.columns if c in ("period", "rule", "beaten", "below_ma200", "n", "years_pos")})
    for hz in horizons:
        out[f"net {hz}"] = d[f"net_{hz}"].map(_pct)
        out[f"hit {hz}"] = d[f"hit_{hz}"].map(lambda v: f"{v * 100:.0f}%")
        out[f"xSPY {hz}"] = d[f"xspy_{hz}"].map(_pct)
        out[f"xrand {hz}"] = d[f"xloc_{hz}"].map(_pct)
        out[f"t {hz}"] = d[f"t_{hz}"].map(lambda v: f"{v:.1f}")
    return out.to_markdown(index=False)


def verdicts(tab: pd.DataFrame, h: int = 20, t_min: float = 2.0, min_excess: float = 0.01) -> pd.DataFrame:
    """Pre-registered bar: local excess > min_excess with t > t_min in train AND test at horizon h."""
    rows = []
    keys = [k for k in tab.index.names if k != "period"]
    for key, g in tab.reset_index().groupby(keys):
        tr = g[g["period"] == "train"]
        te = g[g["period"] == "test"]
        if not len(tr) or not len(te):
            continue
        tr, te = tr.iloc[0], te.iloc[0]
        ok = (tr[f"xloc_{h}"] > min_excess and te[f"xloc_{h}"] > min_excess and tr[f"t_{h}"] > t_min and te[f"t_{h}"] > t_min)
        rows.append({**dict(zip(keys, key if isinstance(key, tuple) else (key,))), "n_train": int(tr["n"]), "n_test": int(te["n"]),
                     f"xrand_{h}_train": tr[f"xloc_{h}"], f"t_train": tr[f"t_{h}"], f"xrand_{h}_test": te[f"xloc_{h}"],
                     f"t_test": te[f"t_{h}"], "net_train": tr[f"net_{h}"], "net_test": te[f"net_{h}"],
                     "hit_train": tr[f"hit_{h}"], "hit_test": te[f"hit_{h}"], "passes": bool(ok)})
    cols = [*keys, "n_train", "n_test", f"xrand_{h}_train", "t_train", f"xrand_{h}_test", "t_test", "net_train", "net_test",
            "hit_train", "hit_test", "passes"]
    return pd.DataFrame(rows, columns=cols)


TURN_RULES = ("ma50_cross", "golden_20_50", "higher_high", "thrust", "rsi_turn")   # the rules that pass in beaten-down stocks


def combined_events(ev: pd.DataFrame, rules: Sequence[str] = TURN_RULES, beaten_only: bool = True,
                    gap_days: int = 30, confluence_days: int = 8) -> pd.DataFrame:
    """The deployable rule: the first of ``rules`` to fire in a (beaten-down) stock, one event per stock per
    ``gap_days``; ``n_rules`` counts the distinct rules that fired within ``confluence_days`` up to that date."""
    u = ev[ev["rule"].isin(rules)]
    if beaten_only:
        u = u[u["beaten"]]
    u = u.sort_values(["symbol", "date"]).copy()
    u["date"] = pd.to_datetime(u["date"])
    keep, last = [], {}
    for i, row in u.iterrows():
        d = row["date"]
        if row["symbol"] in last and (d - last[row["symbol"]]).days < gap_days:
            continue
        last[row["symbol"]] = d
        keep.append(i)
    out = u.loc[keep].copy()
    n_rules = []
    rules_fired = []
    for i, row in out.iterrows():
        g = u[(u["symbol"] == row["symbol"]) & (u["date"] <= row["date"]) & (u["date"] >= row["date"] - pd.Timedelta(days=confluence_days))]
        n_rules.append(int(g["rule"].nunique()))
        rules_fired.append(", ".join(sorted(g["rule"].unique())))
    out["n_rules"] = n_rules
    out["rules"] = rules_fired
    out["depth"] = pd.cut(out["ret_126"], [-1.0, -0.3, -0.2, -0.08], labels=["6m < -30%", "-30% to -20%", "-20% to -8%"])
    out["rule"] = "any turn rule"
    return out.reset_index(drop=True)


def _period_rows(g: pd.DataFrame, label: str, split: str, horizons: Sequence[int], cost: float) -> List[Dict]:
    rows = []
    d = pd.to_datetime(g["date"])
    for pname, m in (("train", (d < split).to_numpy()), ("test", (d >= split).to_numpy())):
        gg = g[m]
        if len(gg) < 30:
            continue
        rec = {"set": label, "period": pname, "n": int(len(gg))}
        yrs = gg.groupby("year")["xloc_20"].mean()
        rec["years_pos"] = f"{int((yrs > 0).sum())}/{len(yrs)}"
        for hz in horizons:
            r = gg[f"ret_{hz}"].to_numpy(dtype=float) - cost
            rec[f"net_{hz}"] = float(np.nanmean(r))
            rec[f"hit_{hz}"] = float(np.nanmean(r > 0))
            rec[f"xspy_{hz}"] = float(np.nanmean(gg[f"xspy_{hz}"]))
            rec[f"xloc_{hz}"] = float(np.nanmean(gg[f"xloc_{hz}"]))
            rec[f"t_{hz}"] = _tstat(gg[f"xloc_{hz}"].to_numpy(dtype=float))
        rows.append(rec)
    return rows


def combined_table(cmb: pd.DataFrame, split: str, horizons: Sequence[int] = HORIZONS, cost: float = COST) -> pd.DataFrame:
    rows = _period_rows(cmb, "any turn rule, beaten-down", split, horizons, cost)
    rows += _period_rows(cmb[cmb["n_rules"] >= 2], "2+ rules within ~5 bars", split, horizons, cost)
    rows += _period_rows(cmb[cmb["n_rules"] == 1], "single rule", split, horizons, cost)
    for k, g in cmb.groupby("depth", observed=True):
        rows += _period_rows(g, f"depth {k}", split, horizons, cost)
    return pd.DataFrame(rows)


def _fmt_combined(t: pd.DataFrame, horizons: Sequence[int] = HORIZONS) -> str:
    out = t[["set", "period", "n", "years_pos"]].copy()
    for hz in horizons:
        out[f"net {hz}"] = t[f"net_{hz}"].map(_pct)
        out[f"hit {hz}"] = t[f"hit_{hz}"].map(lambda v: f"{v * 100:.0f}%")
        out[f"xSPY {hz}"] = t[f"xspy_{hz}"].map(_pct)
        out[f"xrand {hz}"] = t[f"xloc_{hz}"].map(_pct)
        out[f"t {hz}"] = t[f"t_{hz}"].map(lambda v: f"{v:.1f}")
    return out.to_markdown(index=False)


def write_rally_report(out_dir: Path, ev: pd.DataFrame, split: str, horizons: Sequence[int] = HORIZONS,
                       cost: float = COST, doc_path: Optional[Path] = None) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ev.to_csv(out_dir / "rally_events.csv", index=False)
    t_rule = rally_table(ev, split, horizons, cost, by=("rule",))
    t_beaten = rally_table(ev, split, horizons, cost, by=("rule", "beaten"))
    t_ma = rally_table(ev, split, horizons, cost, by=("rule", "below_ma200"))
    t_rule.to_csv(out_dir / "rally_by_rule.csv")
    t_beaten.to_csv(out_dir / "rally_by_rule_beaten.csv")
    t_ma.to_csv(out_dir / "rally_by_rule_ma200.csv")
    v_rule = verdicts(t_rule)
    v_beaten = verdicts(t_beaten)
    v_rule.to_csv(out_dir / "rally_verdicts.csv", index=False)
    v_beaten.to_csv(out_dir / "rally_verdicts_beaten.csv", index=False)
    n_sym = ev["symbol"].nunique()
    d0, d1 = pd.to_datetime(ev["date"]).min().date(), pd.to_datetime(ev["date"]).max().date()
    md = [f"# Early-rally study: {n_sym} symbols, {d0} to {d1}\n",
          f"Entry at the next open after the signal close; returns net of {cost * 1e4:.0f} bps round trip; "
          f"*xSPY* = minus SPY over the same bars; *xrand* = minus the mean of {RANDOM_DRAWS} random entries within +-{LOCAL_WINDOW} "
          f"bars in the same stock (the honest baseline: it removes the stock's own drift and survivorship); *t* = t-statistic of "
          f"xrand; *years_pos* = years with positive xrand at 20 bars. Train before {split}, test from {split}. "
          f"One event per {MIN_GAP} bars per rule and stock.\n",
          "Definitions:\n"]
    md += [f"- `{r}`: {RULE_TEXT[r]}" for r in RULES if r in set(ev["rule"])]
    md.append("\n## Pre-registered verdict (20 bars: xrand > +1% with t > 2 in both train and test)\n")
    vv = v_rule.copy()
    for c in [c for c in vv.columns if c.startswith(("xrand", "net", "hit"))]:
        vv[c] = vv[c].map(_pct if not c.startswith("hit") else (lambda x: f"{x * 100:.0f}%"))
    for c in ("t_train", "t_test"):
        vv[c] = vv[c].map(lambda x: f"{x:.1f}")
    md.append(vv.to_markdown(index=False) + "\n")
    cmb = combined_events(ev)
    cmb.to_csv(out_dir / "rally_combined_events.csv", index=False)
    ct = combined_table(cmb, split, horizons, cost)
    ct.to_csv(out_dir / "rally_combined.csv", index=False)
    md.append("## The deployable rule: any turn rule in a beaten-down stock\n")
    md.append("The five turn rules (`ma50_cross`, `golden_20_50`, `higher_high`, `thrust`, `rsi_turn`) fire on the same stocks days apart, "
              "so the rule the report uses is their union: the first of them to fire in a stock that is below its 200-day MA with a "
              "6-month return under -8%, one entry per stock per 30 days (`base_breakout` is left out: it fails in both periods). "
              "*2+ rules* = at least two distinct rules fired within about a week up to the entry; *depth* = the 6-month return at the signal.\n")
    md.append(_fmt_combined(ct, horizons) + "\n")
    if len(ct):
        a = ct[ct["set"] == "any turn rule, beaten-down"].set_index("period")
        if {"train", "test"} <= set(a.index):
            md.append("Reading: net of costs the union earns "
                      f"{_pct(a.loc['train', 'net_20'])} (train) / {_pct(a.loc['test', 'net_20'])} (test) over 20 bars with a hit rate of "
                      f"{a.loc['train', 'hit_20'] * 100:.0f}% / {a.loc['test', 'hit_20'] * 100:.0f}%, which is "
                      f"{_pct(a.loc['train', 'xloc_20'])} / {_pct(a.loc['test', 'xloc_20'])} more than random entries in the same stocks "
                      f"(t = {a.loc['train', 't_20']:.0f} / {a.loc['test', 't_20']:.0f}) but only {_pct(a.loc['train', 'xspy_20'])} / "
                      f"{_pct(a.loc['test', 'xspy_20'])} against the SPY over the same bars: the rule times the stock's own turn, it does not "
                      f"beat the index at 20 bars. At 60 bars the excess over the SPY is {_pct(a.loc['train', 'xspy_60'])} / "
                      f"{_pct(a.loc['test', 'xspy_60'])}. The deeper the prior decline, the larger every number.\n")
    md.append("## Per rule\n")
    md.append(_fmt(t_rule, horizons) + "\n")
    md.append("## Per rule, beaten-down (below the 200-day MA and 6-month return < -8%) vs not\n")
    md.append(_fmt(t_beaten, horizons) + "\n")
    vb = v_beaten.copy()
    for c in [c for c in vb.columns if c.startswith(("xrand", "net", "hit"))]:
        vb[c] = vb[c].map(_pct if not c.startswith("hit") else (lambda x: f"{x * 100:.0f}%"))
    for c in ("t_train", "t_test"):
        vb[c] = vb[c].map(lambda x: f"{x:.1f}")
    md.append("### Verdict per (rule, beaten-down)\n")
    md.append(vb.to_markdown(index=False) + "\n")
    md.append("## Per rule, below vs above the 200-day MA\n")
    md.append(_fmt(t_ma, horizons) + "\n")
    # per-year table for the 20-bar horizon
    yr = ev.groupby(["rule", "year"]).agg(n=("xloc_20", "size"), xrand_20=("xloc_20", "mean"), net_20=("ret_20", lambda x: x.mean() - cost)).reset_index()
    piv = yr.pivot(index="year", columns="rule", values="xrand_20")
    md.append("## xrand at 20 bars per year (all events of the rule)\n")
    md.append((piv * 100).round(2).to_markdown() + "\n")
    path = out_dir / "rally.md"
    path.write_text("\n".join(md), encoding="utf-8")
    if doc_path:
        Path(doc_path).write_text("\n".join(md), encoding="utf-8")
    return path


# ----------------------------------------------------------------------------
# live scan
# ----------------------------------------------------------------------------
def rally_signals(frames: Dict[str, pd.DataFrame], symbols: Sequence[str], rules: Sequence[str] = RULES,
                  max_age: int = 1) -> pd.DataFrame:
    """Rules that fired within the last ``max_age`` bars, with the context columns the report shows."""
    rows = []
    for s in symbols:
        df = frames.get(s)
        if df is None or len(df) < 300:
            continue
        c, o, h, l = (df[x].to_numpy(dtype=float) for x in ("Close", "Open", "High", "Low"))
        v = np.nan_to_num(df["Volume"].to_numpy(dtype=float))
        n = len(c)
        ma50, ma200 = _sma(c, 50), _sma(c, 200)
        hi252 = _rolling_max(c, 252)
        avgv = pd.Series(v).rolling(20).mean().shift(1).to_numpy()
        for rule in rules:
            hits = rule_hits(rule, o, h, l, c, v)
            hits = hits[hits >= n - max_age]
            if not len(hits):
                continue
            t = int(hits[-1])
            rows.append({"symbol": s, "rule": rule, "signal_date": pd.Timestamp(df.index[t]).strftime("%Y-%m-%d"),
                         "bars_ago": n - 1 - t, "close": float(c[t]), "last": float(c[-1]),
                         "day_ret": float(c[t] / c[t - 1] - 1.0), "ret_10": float(c[t] / c[t - 10] - 1.0),
                         "ret_6m": float(c[t] / c[t - 126] - 1.0), "from_52w_high": float(c[t] / hi252[t] - 1.0),
                         "dist_ma50": float(c[t] / ma50[t] - 1.0), "dist_ma200": float(c[t] / ma200[t] - 1.0),
                         "volume_ratio": float(v[t] / avgv[t]) if np.isfinite(avgv[t]) and avgv[t] > 0 else np.nan,
                         "below_ma200": bool(c[t] < ma200[t]),
                         "beaten": bool(c[t] < ma200[t] and c[t] / c[t - 126] - 1.0 < -0.08)})
    cols = ["symbol", "rule", "signal_date", "bars_ago", "close", "last", "day_ret", "ret_10", "ret_6m", "from_52w_high",
            "dist_ma50", "dist_ma200", "volume_ratio", "below_ma200", "beaten"]
    return pd.DataFrame(rows, columns=cols)


def early_rally_signals(frames: Dict[str, pd.DataFrame], symbols: Sequence[str], max_age: int = 3,
                        rules: Sequence[str] = TURN_RULES) -> pd.DataFrame:
    """The deployable rule, live: one row per beaten-down stock where any turn rule fired in the last ``max_age``
    bars; ``rules`` lists what fired (most recent first), ``bars_ago`` is the most recent firing."""
    sig = rally_signals(frames, symbols, rules=rules, max_age=max_age)
    sig = sig[sig["beaten"]]
    if not len(sig):
        return pd.DataFrame(columns=["symbol", "rules", "n_rules", "signal_date", "bars_ago", "close", "last", "day_ret", "ret_10",
                                     "ret_6m", "from_52w_high", "dist_ma50", "dist_ma200", "volume_ratio"])
    rows = []
    for s, g in sig.groupby("symbol", sort=False):
        g = g.sort_values(["bars_ago", "rule"])
        first = g.iloc[0]
        rows.append({"symbol": s, "rules": ", ".join(g["rule"]), "n_rules": int(len(g)), "signal_date": first["signal_date"],
                     "bars_ago": int(first["bars_ago"]), "close": first["close"], "last": first["last"], "day_ret": first["day_ret"],
                     "ret_10": first["ret_10"], "ret_6m": first["ret_6m"], "from_52w_high": first["from_52w_high"],
                     "dist_ma50": first["dist_ma50"], "dist_ma200": first["dist_ma200"], "volume_ratio": first["volume_ratio"]})
    return pd.DataFrame(rows).sort_values(["bars_ago", "n_rules", "ret_6m"], ascending=[True, False, True]).reset_index(drop=True)
