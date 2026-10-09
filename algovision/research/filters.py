"""Backtests of the filters the first five weeks of the forward test suggested (docs/research_filters.md).

The look-back of the reports (2026-09-05 to 2026-10-08) said: the beaten-down basket itself fell and every table
lost with it; names with an unusual drop against their peers, more than 40% below their 52-week high or with a
negative sentiment read kept falling; declines the market dragged recovered better than company-specific ones;
forming wedges were not a signal. Five weeks and one regime prove nothing, so every candidate is tested here on
2016-2026 with the train (< split) / test (>= split) protocol of the other studies, on the three rules that have
10-year event tables:

* the beaten-down falling-wedge breakout (``algovision.research.events``);
* the news-day rule, long after a >= 4% gap on >= 3x volume in a beaten-down stock (``algovision.research.anomalies``);
* the early-rally rule, the first turn rule to fire in a beaten-down stock (``algovision.research.rally``).

Conditions, all point-in-time at the signal bar:

* **regime: basket 20d > 0**: the equal-weight basket of the stocks that were beaten down 20 bars earlier is up over
  those 20 bars (the gate the regime line of the report describes);
* **regime: breadth rising**: the share of the universe above its 50-day MA is higher than 20 bars earlier;
* **SPY above its 50-day MA**;
* **flag D: > 40% below the 52-week high**;
* **flag Z (proxy): 20-day return vs the sector mean, z-scored against the stock's own last year, below -1**
  (the reports use correlation peer groups; sectors are the 10-year proxy);
* **market-driven decline**: over the 60 bars before the signal the stock fell and its sector's mean return explains
  at least half of the fall (the backtestable analogue of "market-wide" among the causes);
* **wedge score tercile**, **gap size**, **rally depth** as bucket tables;
* **news-day late entry**: instead of the next open, the first close above the previous bar's high within 10 bars.

A condition counts only if the yes rows beat the no rows in excess return over local random entries in **both**
periods by a meaningful size (+0.5% or more over 20 bars) with a usable sample; everything else is noise however
good one period looks. Survivorship bias applies (today's index members).
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.regime import BEATEN_RET_126

MIN_SIDE = 30          # events on each side of a condition before a period counts
MIN_DIFF = 0.005       # yes minus no, excess over local random, 20 bars
COST = 0.001


# ----------------------------------------------------------------------------
# point-in-time context from the price panel
# ----------------------------------------------------------------------------
def panel_context(panel: Dict[str, pd.DataFrame], spy_close: pd.Series, sectors: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """Per-date series (and per-stock frames) every condition needs, computed once on the wide panel."""
    close = panel["Close"].astype(float)
    idx = close.index
    ma200 = close.rolling(200, min_periods=200).mean()
    ma50 = close.rolling(50, min_periods=50).mean()
    r126 = close / close.shift(126) - 1.0
    beaten = (close < ma200) & (r126 < BEATEN_RET_126)
    r20 = close / close.shift(20) - 1.0
    r60 = close / close.shift(60) - 1.0
    # the basket: members fixed 20 bars earlier, equal weight
    mem = beaten.shift(20).fillna(False)
    basket20 = (r20.where(mem)).mean(axis=1)
    breadth50 = (close > ma50).where(ma50.notna()).mean(axis=1)
    spy = spy_close.reindex(idx).ffill()
    spy_ma50 = spy.rolling(50, min_periods=50).mean()
    hi252 = close.rolling(252, min_periods=120).max()
    dd252 = close / hi252 - 1.0
    sec = pd.Series({s: sectors.get(s, "other") for s in close.columns})
    sec_r20 = r20.T.groupby(sec).transform("mean").T
    sec_r60 = r60.T.groupby(sec).transform("mean").T
    rel20 = r20 - sec_r20
    z_rel20 = (rel20 - rel20.rolling(252, min_periods=120).mean()) / rel20.rolling(252, min_periods=120).std()
    return {"basket20": basket20, "breadth50": breadth50, "breadth50_ago": breadth50.shift(20), "spy_above_ma50": (spy > spy_ma50),
            "dd252": dd252, "r60": r60, "sec_r60": sec_r60, "z_rel20": z_rel20, "close": close}


def attach_conditions(ev: pd.DataFrame, ctx: Dict[str, pd.DataFrame], date_col: str = "date") -> pd.DataFrame:
    """Boolean condition columns for every event (symbol, date), NaN-safe (missing context -> False, flagged in ``ctx_ok``)."""
    out = ev.copy()
    d = pd.to_datetime(out[date_col])
    idx = ctx["close"].index
    pos = idx.searchsorted(d, side="right") - 1
    ok = (pos >= 0) & (pos < len(idx))
    cols = list(ctx["close"].columns)
    col_pos = pd.Series(range(len(cols)), index=cols)
    cp = out["symbol"].map(col_pos)
    ok &= cp.notna().to_numpy()
    cp = cp.fillna(0).astype(int).to_numpy()
    pos = np.where(ok, pos, 0)

    def per_date(series: pd.Series) -> np.ndarray:
        return series.to_numpy(dtype=float)[pos]

    def per_stock(frame: pd.DataFrame) -> np.ndarray:
        return frame.to_numpy(dtype=float)[pos, cp]

    basket = per_date(ctx["basket20"])
    b_now, b_ago = per_date(ctx["breadth50"]), per_date(ctx["breadth50_ago"])
    spy_up = ctx["spy_above_ma50"].to_numpy()[pos]
    dd = per_stock(ctx["dd252"])
    r60, s60 = per_stock(ctx["r60"]), per_stock(ctx["sec_r60"])
    z = per_stock(ctx["z_rel20"])
    with np.errstate(invalid="ignore", divide="ignore"):
        share = np.where(r60 < 0, s60 / r60, np.nan)      # share of the stock's 60-bar fall explained by the sector mean
    out["ctx_ok"] = ok
    out["c_regime_basket_pos"] = ok & np.nan_to_num(basket > 0, nan=False)
    out["c_regime_breadth_up"] = ok & np.nan_to_num(b_now > b_ago, nan=False)
    out["c_spy_above_ma50"] = ok & np.nan_to_num(spy_up.astype(bool), nan=False)
    out["c_flag_D_deep"] = ok & np.nan_to_num(dd <= -0.40, nan=False)
    out["c_flag_Z_vs_sector"] = ok & np.nan_to_num(z <= -1.0, nan=False)
    out["c_market_driven"] = ok & np.nan_to_num((r60 < 0) & (share >= 0.5), nan=False)
    out["x_basket20"], out["x_dd252"], out["x_z_rel20"], out["x_sector_share"] = basket, dd, z, share
    return out


CONDITION_NAMES = {
    "c_regime_basket_pos": "regime: beaten-down basket up over the last 20 bars",
    "c_regime_breadth_up": "regime: breadth (share above the 50-day MA) rising vs 20 bars ago",
    "c_spy_above_ma50": "SPY above its 50-day MA",
    "c_flag_D_deep": "flag D: more than 40% below the 52-week high",
    "c_flag_Z_vs_sector": "flag Z (proxy): 20-day return vs sector, z below -1",
    "c_market_driven": "market-driven decline: sector explains >= 50% of the 60-bar fall",
}


# ----------------------------------------------------------------------------
# the condition study
# ----------------------------------------------------------------------------
def _side(g: pd.DataFrame, h: int, ret_col: str, x_col: str) -> Dict:
    r = g[f"{ret_col}_{h}"].to_numpy(dtype=float)
    x = g[f"{x_col}_{h}"].to_numpy(dtype=float) if f"{x_col}_{h}" in g else np.full(len(r), np.nan)
    ok = np.isfinite(r)
    r, x = r[ok], x[ok]
    xs = x[np.isfinite(x)]
    return {"n": int(len(r)), "net": float(r.mean() - COST) if len(r) else np.nan, "hit": float((r - COST > 0).mean()) if len(r) else np.nan,
            "excess": float(xs.mean()) if len(xs) else np.nan}


def condition_study(ev: pd.DataFrame, split: str, conditions: Sequence[str], h: int = 20, h2: int = 60, ret_col: str = "ret",
                    x_col: str = "xloc", date_col: str = "date") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """(detail, findings): per condition x period x yes/no stats, and the yes-minus-no verdict table."""
    d = pd.to_datetime(ev[date_col])
    years = d.dt.year
    detail, find = [], []
    for c in conditions:
        cond = ev[c].fillna(False).astype(bool)
        rec: Dict = {"condition": CONDITION_NAMES.get(c, c), "key": c}
        for period, mask in (("train", d < split), ("test", d >= split)):
            for state, sel in (("yes", cond), ("no", ~cond)):
                for hh in (h, h2):
                    st = _side(ev[mask & sel], hh, ret_col, x_col)
                    detail.append({"condition": rec["condition"], "period": period, "state": state, "h": hh, **st})
                    rec[f"{period}_n_{state}_{hh}"] = st["n"]
                    rec[f"{period}_excess_{state}_{hh}"] = st["excess"]
                    rec[f"{period}_net_{state}_{hh}"] = st["net"]
                    rec[f"{period}_hit_{state}_{hh}"] = st["hit"]
            for hh in (h, h2):
                y, n = rec[f"{period}_excess_yes_{hh}"], rec[f"{period}_excess_no_{hh}"]
                rec[f"{period}_diff_{hh}"] = y - n if np.isfinite(y) and np.isfinite(n) else np.nan
        # years in which the 20-bar difference was positive (years with >= 5 events on each side)
        pos_years, n_years = 0, 0
        for yr, g in ev.groupby(years):
            cy = cond[g.index]
            a, b = g[cy], g[~cy]
            if len(a) >= 5 and len(b) >= 5:
                n_years += 1
                xa, xb = a[f"{x_col}_{h}"].dropna().mean(), b[f"{x_col}_{h}"].dropna().mean()
                pos_years += int(np.isfinite(xa) and np.isfinite(xb) and xa > xb)
        rec["years_positive"] = f"{pos_years}/{n_years}"
        usable = all(rec[f"{p}_n_{s}_{h}"] >= MIN_SIDE for p in ("train", "test") for s in ("yes", "no"))
        rec["consistent"] = bool(usable and np.isfinite(rec[f"train_diff_{h}"]) and np.isfinite(rec[f"test_diff_{h}"])
                                 and rec[f"train_diff_{h}"] >= MIN_DIFF and rec[f"test_diff_{h}"] >= MIN_DIFF)
        rec["consistent_negative"] = bool(usable and np.isfinite(rec[f"train_diff_{h}"]) and np.isfinite(rec[f"test_diff_{h}"])
                                          and rec[f"train_diff_{h}"] <= -MIN_DIFF and rec[f"test_diff_{h}"] <= -MIN_DIFF)
        find.append(rec)
    return pd.DataFrame(detail), pd.DataFrame(find)


def bucket_table(ev: pd.DataFrame, by: str, split: str, h: int = 20, ret_col: str = "ret", x_col: str = "xloc", date_col: str = "date") -> pd.DataFrame:
    d = pd.to_datetime(ev[date_col])
    rows = []
    for period, mask in (("train", d < split), ("test", d >= split)):
        for key, g in ev[mask].groupby(by, observed=True):
            st = _side(g, h, ret_col, x_col)
            rows.append({"bucket": str(key), "period": period, **st})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# news-day: late entry
# ----------------------------------------------------------------------------
def newsday_late_entry(panel: Dict[str, pd.DataFrame], spy_close: pd.Series, ev: pd.DataFrame, within: int = 10,
                       horizons: Sequence[int] = (20, 60)) -> pd.DataFrame:
    """For every news-day event: the standard entry (next open) and the late entry (the first close above the previous
    bar's high within ``within`` bars after the gap day), long returns to the close ``h`` bars after each entry, SPY-adjusted."""
    close, open_, high = panel["Close"], panel["Open"], panel["High"]
    idx = close.index
    spy = spy_close.reindex(idx).ffill().to_numpy(dtype=float)
    rows = []
    for r in ev.itertuples():
        s = r.symbol
        if s not in close.columns:
            continue
        t = idx.searchsorted(pd.Timestamp(getattr(r, "date")))
        c, o, hgh = close[s].to_numpy(dtype=float), open_[s].to_numpy(dtype=float), high[s].to_numpy(dtype=float)
        n = len(c)
        if t + 1 >= n:
            continue
        rec = {"symbol": s, "date": idx[t], "std_entry_pos": t + 1, "late_entry_pos": np.nan}
        for j in range(t + 1, min(n, t + 1 + within)):
            if np.isfinite(c[j]) and np.isfinite(hgh[j - 1]) and c[j] > hgh[j - 1]:
                rec["late_entry_pos"] = j
                break
        for h in horizons:
            e = t + 1
            if e + h < n and np.isfinite(o[e]):
                rec[f"std_ret_{h}"] = c[e + h - 1] / o[e] - 1.0
                rec[f"std_xspy_{h}"] = rec[f"std_ret_{h}"] - (spy[e + h - 1] / spy[e] - 1.0)
            else:
                rec[f"std_ret_{h}"] = rec[f"std_xspy_{h}"] = np.nan
            j = rec["late_entry_pos"]
            if np.isfinite(j) and int(j) + 1 + h < n:
                e2 = int(j) + 1      # the next open after the confirming close
                rec[f"late_ret_{h}"] = c[e2 + h - 1] / o[e2] - 1.0
                rec[f"late_xspy_{h}"] = rec[f"late_ret_{h}"] - (spy[e2 + h - 1] / spy[e2] - 1.0)
            else:
                rec[f"late_ret_{h}"] = rec[f"late_xspy_{h}"] = np.nan
        rows.append(rec)
    return pd.DataFrame(rows)


def late_entry_table(le: pd.DataFrame, split: str, horizons: Sequence[int] = (20, 60)) -> pd.DataFrame:
    d = pd.to_datetime(le["date"])
    rows = []
    for period, mask in (("train", d < split), ("test", d >= split)):
        g = le[mask]
        rec = {"period": period, "n": len(g), "late_entry_found": float(g["late_entry_pos"].notna().mean()) if len(g) else np.nan}
        for h in horizons:
            for kind in ("std", "late"):
                r = g[f"{kind}_ret_{h}"].dropna() - COST
                x = g[f"{kind}_xspy_{h}"].dropna()
                rec[f"{kind}_net_{h}"] = float(r.mean()) if len(r) else np.nan
                rec[f"{kind}_hit_{h}"] = float((r > 0).mean()) if len(r) else np.nan
                rec[f"{kind}_xspy_{h}"] = float(x.mean()) if len(x) else np.nan
                rec[f"{kind}_n_{h}"] = int(len(r))
        rows.append(rec)
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# the report
# ----------------------------------------------------------------------------
def _p(v, d=2) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def _h(v) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:.0f}%"


def _fmt_findings(f: pd.DataFrame, h: int, h2: int) -> str:
    lines = [f"| condition | train: yes n / excess / hit vs no n / excess / hit ({h}) | test: the same ({h}) | yes - no train / test ({h}) | yes - no train / test ({h2}) | years positive | verdict |",
             "|---|---|---|---|---|---|---|"]
    for r in f.itertuples():
        def side(p):
            return (f"{getattr(r, f'{p}_n_yes_{h}')} / {_p(getattr(r, f'{p}_excess_yes_{h}'))} / {_h(getattr(r, f'{p}_hit_yes_{h}'))} vs "
                    f"{getattr(r, f'{p}_n_no_{h}')} / {_p(getattr(r, f'{p}_excess_no_{h}'))} / {_h(getattr(r, f'{p}_hit_no_{h}'))}")
        verdict = "**helps (consistent)**" if r.consistent else ("**hurts (consistent)**" if r.consistent_negative else "noise")
        lines.append(f"| {r.condition} | {side('train')} | {side('test')} | {_p(getattr(r, f'train_diff_{h}'))} / {_p(getattr(r, f'test_diff_{h}'))} | "
                     f"{_p(getattr(r, f'train_diff_{h2}'))} / {_p(getattr(r, f'test_diff_{h2}'))} | {r.years_positive} | {verdict} |")
    return "\n".join(lines)


def _fmt_buckets(t: pd.DataFrame, h: int) -> str:
    lines = [f"| bucket | period | n | net {h}-bar return | hit | excess over local random |", "|---|---|---|---|---|---|"]
    for r in t.itertuples():
        lines.append(f"| {r.bucket} | {r.period} | {r.n} | {_p(r.net)} | {_h(r.hit)} | {_p(r.excess)} |")
    return "\n".join(lines)


def _fmt_late(t: pd.DataFrame, horizons=(20, 60)) -> str:
    cols = " | ".join(f"next open {h}: net / hit / vs SPY | late entry {h}: net / hit / vs SPY" for h in horizons)
    lines = [f"| period | n | late entry found | {cols} |", "|" + "---|" * (3 + 2 * len(horizons))]
    for r in t.itertuples():
        cells = []
        for h in horizons:
            cells.append(f"{_p(getattr(r, f'std_net_{h}'))} / {_h(getattr(r, f'std_hit_{h}'))} / {_p(getattr(r, f'std_xspy_{h}'))} (n={getattr(r, f'std_n_{h}')})")
            cells.append(f"{_p(getattr(r, f'late_net_{h}'))} / {_h(getattr(r, f'late_hit_{h}'))} / {_p(getattr(r, f'late_xspy_{h}'))} (n={getattr(r, f'late_n_{h}')})")
        lines.append(f"| {r.period} | {r.n} | {_h(r.late_entry_found)} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_filters_report(out_dir: Path, split: str, families: Dict[str, Dict], doc_path: Optional[Path] = None) -> Path:
    """``families`` = {name: {"events": ev with conditions, "ret_col", "x_col", "date_col", "buckets": {label: column}, "late": table or None}}."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    md = ["# Filters from the forward test, backtested (2016-2026)", "",
          "The first five weeks of the daily reports (2026-09-05 to 2026-10-08) suggested a few filters: a regime gate on the beaten-down "
          "basket, two of the flags (an unusual drop against peers, a decline deeper than 40% from the 52-week high), a preference for "
          "declines the market dragged, and that forming wedges are not a signal. Five weeks and one regime prove nothing, so each "
          "candidate is tested here on the three rules with ten-year event tables, train (before "
          f"{split}) and test (from {split}) separately. Entry at the next open, 10 bps cost, excess measured over random entries in "
          "the same stock within half a year of the signal (``xloc``), which cancels the stock's drift and the regime around the signal.", "",
          f"A condition **helps** when the yes rows beat the no rows in excess return in **both** periods by at least {MIN_DIFF * 100:.1f}% over "
          f"20 bars with at least {MIN_SIDE} events on each side; it **hurts** when the no rows beat the yes rows by the same margin in both "
          "periods; everything else is noise however good one period looks. Conditions are point-in-time at the signal bar: the basket "
          "and the breadth use membership fixed 20 bars earlier; the sector proxies stand in for the correlation peer groups of the "
          "reports, which have no ten-year history.", ""]
    verdicts: List[str] = []
    for name, fam in families.items():
        ev = fam["events"]
        md += [f"## {name}", "", f"{len(ev)} events, {ev['symbol'].nunique()} stocks, {pd.to_datetime(ev[fam['date_col']]).min().date()} to "
               f"{pd.to_datetime(ev[fam['date_col']]).max().date()}; context available for {int(ev['ctx_ok'].sum())} of them.", ""]
        conds = [c for c in CONDITION_NAMES if c in ev]
        detail, find = condition_study(ev, split, conds, 20, 60, fam["ret_col"], fam["x_col"], fam["date_col"])
        detail.to_csv(out / f"{fam['slug']}_conditions.csv", index=False)
        find.to_csv(out / f"{fam['slug']}_findings.csv", index=False)
        md += ["### Conditions", "", _fmt_findings(find, 20, 60), ""]
        for r in find.itertuples():
            if r.consistent:
                verdicts.append(f"- **{name}**: *{r.condition}* helps ({_p(getattr(r, 'train_diff_20'))} train, {_p(getattr(r, 'test_diff_20'))} test at 20 bars).")
            elif r.consistent_negative:
                verdicts.append(f"- **{name}**: *{r.condition}* hurts ({_p(getattr(r, 'train_diff_20'))} train, {_p(getattr(r, 'test_diff_20'))} test at 20 bars).")
        for label, col in (fam.get("buckets") or {}).items():
            if col in ev:
                t = bucket_table(ev, col, split, 20, fam["ret_col"], fam["x_col"], fam["date_col"])
                t.to_csv(out / f"{fam['slug']}_{col}.csv", index=False)
                md += [f"### {label}", "", _fmt_buckets(t, 20), ""]
        if fam.get("late") is not None and len(fam["late"]):
            t = late_entry_table(fam["late"], split)
            t.to_csv(out / f"{fam['slug']}_late_entry.csv", index=False)
            md += ["### Late entry (first close above the previous bar's high within 10 bars) vs the next open", "", _fmt_late(t), ""]
    md += ["## Verdicts", ""] + (verdicts or ["- No condition passed in both periods; nothing here should change a rule."]) + [""]
    md += ["## Reading", "",
           "Only a condition marked **helps** or **hurts** in a family is a candidate for that family's rule, and only as the filter "
           "stated (a gate on entry, not a score). A condition that passes in one family and fails in another stays confined to the "
           "family where it passed. The reports keep showing the flags and the regime line as context either way; this file says which "
           "of them earned the right to be a rule.", "",
           "Systematic screens and an event study on today's index members (survivorship bias), not investment advice.", ""]
    text = "\n".join(md)
    (out / "README.md").write_text(text, encoding="utf-8")
    if doc_path:
        Path(doc_path).write_text(text, encoding="utf-8")
    return out / "README.md"
