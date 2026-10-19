"""Stocks that crossed back above their 200-day moving average after a long run below it.

The list (``ma200_cross_signals``): a close above the 200-day MA whose previous close was at or below it, after at
least ``min_below`` consecutive closes at or below the line (default 120 bars, about six months). The report shows the
crosses of the last ``max_age`` bars with the length of the run that ended, like the early-rally table.

The backtest (``ma200_cross_study``, ``research-ma200`` command): every such cross over ten years, entry at the next
open, returns at 20 and 60 bars against random entries in the same stock around the same date (``xloc``) and against
the SPY, by period (train < split / test >= split) and by the length of the run below. The heading of the daily table
quotes the result; until a cut passes in both periods the table is context, not a rule, and nothing enters the
journal, the checklist or the flags.
"""
from __future__ import annotations

import zlib
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

MIN_BELOW = 120          # bars at or below the 200-day MA before the cross counts as "a long time"
RUN_BINS = [60, 120, 200, 10 ** 6]
RUN_LABELS = ["60-119", "120-199", "200+"]


def _run_below(close: np.ndarray, ma: np.ndarray) -> np.ndarray:
    """Consecutive bars with close <= MA200 ending at each bar (0 where the close is above or the MA is undefined)."""
    below = np.isfinite(ma) & (close <= ma)
    run = np.zeros(len(close), dtype=int)
    for i in range(len(close)):
        run[i] = run[i - 1] + 1 if below[i] and i else (1 if below[i] else 0)
    return run


def cross_points(close: pd.Series, min_below: int = MIN_BELOW) -> pd.DataFrame:
    """Every cross above the 200-day MA after >= ``min_below`` bars at or below it: index position, date, run length."""
    c = close.to_numpy(dtype=float)
    ma = close.rolling(200, min_periods=200).mean().to_numpy(dtype=float)
    run = _run_below(c, ma)
    above = np.isfinite(ma) & (c > ma)
    out = []
    for t in range(1, len(c)):
        if above[t] and run[t - 1] >= min_below:
            out.append({"pos": t, "date": close.index[t], "bars_below": int(run[t - 1])})
    return pd.DataFrame(out, columns=["pos", "date", "bars_below"])


def ma200_cross_signals(frames: Dict[str, pd.DataFrame], symbols: Sequence[str], max_age: int = 3, min_below: int = MIN_BELOW) -> pd.DataFrame:
    """One row per stock whose close crossed above the 200-day MA in the last ``max_age`` bars after a run of at least
    ``min_below`` bars below it (the most recent such cross). Context columns match the early-rally table."""
    rows: List[Dict] = []
    for s in symbols:
        df = frames.get(s)
        if df is None or len(df) < 260:
            continue
        close = df["Close"].astype(float)
        cp = cross_points(close, min_below)
        if not len(cp):
            continue
        last = cp.iloc[-1]
        n = len(close)
        t = int(last["pos"])
        ago = n - 1 - t
        if ago > max_age:
            continue
        c = close.to_numpy(dtype=float)
        ma200 = float(close.rolling(200).mean().iloc[-1])
        ma50 = float(close.rolling(50).mean().iloc[-1])
        vol = df["Volume"].astype(float).to_numpy()
        vr = vol[t] / np.nanmean(vol[max(0, t - 20):t]) if t >= 5 and np.nanmean(vol[max(0, t - 20):t]) > 0 else np.nan
        hi252 = float(np.nanmax(c[max(0, n - 252):]))
        rows.append({"symbol": s, "signal_date": close.index[t].strftime("%Y-%m-%d"), "bars_ago": int(ago), "bars_below": int(last["bars_below"]),
                     "below_since": close.index[t - int(last["bars_below"])].strftime("%Y-%m-%d"),
                     "day_ret": float(c[t] / c[t - 1] - 1.0), "ret_10": float(c[-1] / c[-11] - 1.0) if n > 11 else np.nan,
                     "ret_6m": float(c[-1] / c[-127] - 1.0) if n > 127 else np.nan, "from_52w_high": float(c[-1] / hi252 - 1.0) if hi252 > 0 else np.nan,
                     "dist_ma50": float(c[-1] / ma50 - 1.0) if ma50 > 0 else np.nan, "dist_ma200": float(c[-1] / ma200 - 1.0) if ma200 > 0 else np.nan,
                     "volume_ratio": float(vr) if np.isfinite(vr) else np.nan, "last": float(c[-1]), "ma200": ma200})
    cols = ["symbol", "signal_date", "bars_ago", "bars_below", "below_since", "day_ret", "ret_10", "ret_6m", "from_52w_high", "dist_ma50", "dist_ma200",
            "volume_ratio", "last", "ma200"]
    out = pd.DataFrame(rows, columns=cols)
    if len(out):
        out = out.sort_values(["bars_ago", "bars_below"], ascending=[True, False]).reset_index(drop=True)
    return out


# ----------------------------------------------------------------------------
# the backtest
# ----------------------------------------------------------------------------
def ma200_cross_study(frames: Dict[str, pd.DataFrame], spy_close: pd.Series, min_below: int = 60, horizons: Sequence[int] = (20, 60),
                      min_gap: int = 20, local_window: int = 126, random_draws: int = 10, seed: int = 11) -> pd.DataFrame:
    """One row per cross (run >= ``min_below``, at most one per stock per ``min_gap`` bars): forward returns from the next
    open, the SPY excess and the excess over random entries in the same stock within +-``local_window`` bars."""
    rows: List[Dict] = []
    hmax = max(horizons)
    for s, df in frames.items():
        if df is None or len(df) < 300:
            continue
        close = df["Close"].astype(float)
        cp = cross_points(close, min_below)
        if not len(cp):
            continue
        c, o = close.to_numpy(dtype=float), df["Open"].astype(float).to_numpy()
        spy = spy_close.reindex(close.index).ffill().to_numpy(dtype=float)
        n = len(c)
        rng = np.random.default_rng(seed + zlib.crc32(s.encode()) % 100000)
        last = -10 ** 6
        for t, date, run in cp[["pos", "date", "bars_below"]].itertuples(index=False):
            t = int(t)
            if t - last < min_gap or t + hmax + 1 >= n:
                continue
            last = t
            entry = o[t + 1]
            if not np.isfinite(entry) or entry <= 0:
                continue
            row = {"symbol": s, "date": date, "bars_below": int(run), "entry": float(entry), "day_ret": float(c[t] / c[t - 1] - 1.0),
                   "ret_126": float(c[t] / c[t - 126] - 1.0) if t >= 126 else np.nan}
            for h in horizons:
                r = c[t + h] / entry - 1.0
                row[f"ret_{h}"] = float(r)
                row[f"xspy_{h}"] = float(r - (spy[t + h] / spy[t + 1] - 1.0)) if np.isfinite(spy[t + 1]) and np.isfinite(spy[t + h]) else np.nan
                lo_, hi_ = max(1, t - local_window), min(n - h - 3, t + local_window)
                cand = np.arange(lo_, hi_ + 1)
                cand = cand[np.abs(cand - t) > h]
                if len(cand) >= 5:
                    pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                    row[f"xloc_{h}"] = float(r - np.mean(c[pick + h] / o[pick + 1] - 1.0))
                else:
                    row[f"xloc_{h}"] = np.nan
            rows.append(row)
    ev = pd.DataFrame(rows)
    if len(ev):
        ev["run_bucket"] = pd.cut(ev["bars_below"], RUN_BINS, labels=RUN_LABELS, right=False)
    return ev


def _stats(g: pd.DataFrame, h: int) -> Dict:
    x = g[f"xloc_{h}"].dropna()
    t = float(x.mean() / x.std() * np.sqrt(len(x))) if len(x) > 2 and x.std() > 0 else np.nan
    return {"n": int(len(g)), f"ret_{h}": float(g[f"ret_{h}"].mean()), f"hit_{h}": float((g[f"ret_{h}"] > 0).mean()),
            f"xspy_{h}": float(g[f"xspy_{h}"].mean()), f"xloc_{h}": float(x.mean()) if len(x) else np.nan, f"t_{h}": t}


def ma200_summary(ev: pd.DataFrame, split: str, horizons: Sequence[int] = (20, 60)) -> pd.DataFrame:
    """Per run-length bucket (and all crosses) and period: n, mean return, hit rate, SPY excess, local-random excess, t."""
    d = pd.to_datetime(ev["date"])
    rows = []
    for period, mask in (("train", d < split), ("test", d >= split)):
        groups = [("all (60+)", ev[mask])] + [(str(k), g) for k, g in ev[mask].groupby("run_bucket", observed=True)]
        groups.append(("120+", ev[mask & (ev["bars_below"] >= 120)]))
        for name, g in groups:
            if not len(g):
                continue
            rec = {"bucket": name, "period": period}
            for h in horizons:
                rec.update(_stats(g, h))
            rows.append(rec)
    return pd.DataFrame(rows)


def ma200_by_year(ev: pd.DataFrame, min_below: int = MIN_BELOW, h: int = 20) -> pd.DataFrame:
    e = ev[ev["bars_below"] >= min_below].copy()
    e["year"] = pd.to_datetime(e["date"]).dt.year
    out = e.groupby("year").apply(lambda g: pd.Series({"n": len(g), f"ret_{h}": g[f"ret_{h}"].mean(), f"xloc_{h}": g[f"xloc_{h}"].mean(),
                                                       f"xspy_{h}": g[f"xspy_{h}"].mean(), f"hit_{h}": (g[f"ret_{h}"] > 0).mean()}))
    return out.reset_index()


def verdict(summary: pd.DataFrame, bucket: str = "120+", h: int = 20, threshold: float = 0.005) -> Dict:
    """Passes when the local-random excess at ``h`` bars is at least ``threshold`` in both periods with >= 30 events each."""
    tr = summary[(summary["bucket"] == bucket) & (summary["period"] == "train")]
    te = summary[(summary["bucket"] == bucket) & (summary["period"] == "test")]
    if not len(tr) or not len(te):
        return {"passed": False, "reason": "no events"}
    a, b = tr.iloc[0], te.iloc[0]
    ok = a["n"] >= 30 and b["n"] >= 30 and a[f"xloc_{h}"] >= threshold and b[f"xloc_{h}"] >= threshold
    return {"passed": bool(ok), "train": {"n": int(a["n"]), "xloc": float(a[f"xloc_{h}"]), "xspy": float(a[f"xspy_{h}"]), "hit": float(a[f"hit_{h}"]), "ret": float(a[f"ret_{h}"])},
            "test": {"n": int(b["n"]), "xloc": float(b[f"xloc_{h}"]), "xspy": float(b[f"xspy_{h}"]), "hit": float(b[f"hit_{h}"]), "ret": float(b[f"ret_{h}"])}}


def _pct(v, d=1):
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def write_ma200_report(doc_path: Path, ev: pd.DataFrame, split: str, out_dir: Optional[Path] = None, horizons: Sequence[int] = (20, 60)) -> Path:
    doc_path = Path(doc_path)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    summ = ma200_summary(ev, split, horizons)
    years = ma200_by_year(ev)
    v = verdict(summ)
    if out_dir:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ev.to_csv(out_dir / "ma200_events.csv", index=False)
        summ.to_csv(out_dir / "ma200_summary.csv", index=False)
        years.to_csv(out_dir / "ma200_by_year.csv", index=False)
    d = pd.to_datetime(ev["date"])
    md = ["# Crossing back above the 200-day MA after a long run below it", "",
          f"Event: a close above the 200-day moving average whose previous close was at or below it, after at least 60 consecutive closes at or below "
          f"the line; at most one event per stock per 20 bars; entry at the next open; {len(ev)} events, {d.min().date()} to {d.max().date()}, "
          f"train < {split} / test >= {split}. *xloc* = the return minus the mean return of 10 random entries in the same stock within +-126 bars "
          "(the same horizon), *xspy* = minus the SPY over the same window, *hit* = share of positive returns, *t* = t-statistic of xloc. "
          "Buckets by the length of the run below the line (bars).", "",
          "## Verdict", ""]
    if v.get("passed"):
        md.append(f"**Passed** for runs of 120+ bars at 20 bars: xloc {_pct(v['train']['xloc'])} (train, n {v['train']['n']}) / {_pct(v['test']['xloc'])} "
                  f"(test, n {v['test']['n']}); vs SPY {_pct(v['train']['xspy'])} / {_pct(v['test']['xspy'])}; hit {v['train']['hit'] * 100:.0f}% / {v['test']['hit'] * 100:.0f}%.")
    elif "train" in v:
        md.append(f"**Not passed** for runs of 120+ bars at 20 bars (the rule: at least +0.5% over local random entries in both periods with 30+ events each): "
                  f"xloc {_pct(v['train']['xloc'])} (train, n {v['train']['n']}) / {_pct(v['test']['xloc'])} (test, n {v['test']['n']}); vs SPY "
                  f"{_pct(v['train']['xspy'])} / {_pct(v['test']['xspy'])}; hit {v['train']['hit'] * 100:.0f}% / {v['test']['hit'] * 100:.0f}%; "
                  f"raw {_pct(v['train']['ret'])} / {_pct(v['test']['ret'])}.")
    else:
        md.append("No events.")
    md += ["", "## By run length and period", ""]
    t = summ.copy()
    for h in horizons:
        for c in (f"ret_{h}", f"hit_{h}", f"xspy_{h}", f"xloc_{h}"):
            t[c] = t[c].map(lambda x: _pct(x, 1) if "hit" not in c else ("" if not np.isfinite(x) else f"{x * 100:.0f}%"))
        t[f"t_{h}"] = t[f"t_{h}"].map(lambda x: "" if not np.isfinite(x) else f"{x:.1f}")
    md += [t.to_markdown(index=False), "", "## By year (runs of 120+ bars, 20 bars)", ""]
    y = years.copy()
    if len(y):
        for c in ("ret_20", "xloc_20", "xspy_20"):
            y[c] = y[c].map(lambda x: _pct(x, 1))
        y["hit_20"] = y["hit_20"].map(lambda x: f"{x * 100:.0f}%")
        y["n"] = y["n"].astype(int)
        md += [y.to_markdown(index=False), ""]
    md += ["Survivorship bias applies (today's index members). Not investment advice.", ""]
    doc_path.write_text("\n".join(md), encoding="utf-8")
    return doc_path


# the verdict of the last ``research-ma200`` run (docs/research_ma200.md), quoted in the daily table heading
BACKTEST: Dict = {"passed": False, "as_of": "2026-10-19", "split": "2023-01-01",
                  "train": {"n": 446, "ret": 0.011, "xloc": 0.001, "xspy": 0.007, "hit": 0.54},
                  "test": {"n": 361, "ret": 0.012, "xloc": 0.009, "xspy": 0.001, "hit": 0.52},
                  "h60": {"train": {"xloc": 0.031, "xspy": 0.027, "hit": 0.64}, "test": {"xloc": 0.017, "xspy": -0.025, "hit": 0.52}}}


def heading_note(doc: Optional[Dict] = None) -> str:
    """The one-line backtest summary quoted in the daily table heading; ``doc`` is the verdict dict (from docs/research_ma200.md)."""
    if not doc or "train" in doc and doc["train"]["n"] == 0:
        return "not backtested yet"
    tr, te = doc["train"], doc["test"]
    body = (f"runs of 120+ bars, 20 bars: {_pct(tr['ret'])} / {_pct(te['ret'])} raw, {_pct(tr['xloc'])} / {_pct(te['xloc'])} vs random entries in the "
            f"same stock, {_pct(tr['xspy'])} / {_pct(te['xspy'])} vs SPY, hit {tr['hit'] * 100:.0f}% / {te['hit'] * 100:.0f}% (train / test, "
            f"n {tr['n']} / {te['n']})")
    return ("tested edge: " if doc.get("passed") else "no tested edge: ") + body


def heading_note_he(doc: Optional[Dict] = None) -> str:
    if not doc or "train" in doc and doc["train"]["n"] == 0:
        return "טרם נבדק לאחור"
    tr, te = doc["train"], doc["test"]
    body = (f"רצפים של 120+ נרות, 20 נרות: {_pct(tr['ret'])} / {_pct(te['ret'])} גולמי, {_pct(tr['xloc'])} / {_pct(te['xloc'])} מול כניסות אקראיות "
            f"באותה מניה, {_pct(tr['xspy'])} / {_pct(te['xspy'])} מול SPY, הצלחה {tr['hit'] * 100:.0f}% / {te['hit'] * 100:.0f}% (אימון / מבחן, "
            f"n {tr['n']} / {te['n']})")
    return ("יתרון שנבדק: " if doc.get("passed") else "אין יתרון שנבדק: ") + body
