"""Side study: a doji candle sitting on the 10-day moving average, on daily bars.

Event (``doji_on_ma10_events``): a daily candle whose body is at most ``body_max`` of its high-low range (default 10%,
a doji), whose range is at least ``min_range`` of the close (0.25%, to skip flat prints), and whose 10-day simple
moving average of closes (including the day itself) lies inside the candle's low-high range: the candle sits on the
line. The strict variant (``on_line``) also asks the line to pass within 0.25% of the body's midpoint. At most one
event per stock per ``min_gap`` bars (default 5) so the 5-bar windows do not overlap much.

What is measured: the close-to-close return 1, 5 and 21 bars after the doji (what the stock does next), and the same
from the next open (what a trade could get), each against (a) the SPY over the same window (``xspy``), (b) ten random
days of the same stock within +-63 bars (``xloc``, with a t-statistic), and (c) the unconditional base rate of the same
stocks over the same period (the share of up moves and the mean return on any day). Context splits: the slope of the
10-day MA, the side the price came from (a pullback to the line from above or a bounce up to it from below), above or
below the 50-day MA, and the candle's range against the 20-day ATR. The main window is the last ``window`` bars (one
year by default); the ten-year train/test split is reported as a robustness check. ``research-doji`` writes
docs/research_doji_ma10.md. Nothing here feeds the daily report: a side study, not a rule.
"""
from __future__ import annotations

import zlib
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

HORIZONS = (1, 5, 21)
BODY_MAX = 0.10
MIN_RANGE = 0.0025
STRICT_TOL = 0.0025
MIN_GAP = 5
WINDOW = 252
WEEKLY_HORIZONS = (1, 4, 12)
WEEKLY_WINDOW = 52


def to_weekly(df: pd.DataFrame, min_days: int = 3) -> pd.DataFrame:
    """Daily bars to weekly bars (Monday to Friday): open = first, high = max, low = min, close = last, volume = sum.
    Weeks with fewer than ``min_days`` sessions are dropped, and so is the last week when it has not reached Friday."""
    if df is None or not len(df):
        return df
    g = df.resample("W-FRI")
    w = pd.DataFrame({"Open": g["Open"].first(), "High": g["High"].max(), "Low": g["Low"].min(), "Close": g["Close"].last(),
                      "Volume": g["Volume"].sum() if "Volume" in df.columns else g["Close"].count(), "days": g["Close"].count()})
    w = w[w["days"] >= min_days].drop(columns="days")
    if len(w) and df.index[-1].weekday() < 4:
        w = w.iloc[:-1]
    return w


def weekly_frames(frames: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    return {s: to_weekly(df) for s, df in frames.items() if df is not None and len(df)}


def doji_mask(df: pd.DataFrame, body_max: float = BODY_MAX, min_range: float = MIN_RANGE) -> np.ndarray:
    """True where the candle is a doji: |close-open| <= body_max * (high-low), range >= min_range * close."""
    o, h, l, c = (df[k].astype(float).to_numpy() for k in ("Open", "High", "Low", "Close"))
    rng = h - l
    with np.errstate(invalid="ignore", divide="ignore"):
        ok = (rng > 0) & (rng >= min_range * c) & (np.abs(c - o) <= body_max * rng)
    return np.where(np.isfinite(ok), ok, False).astype(bool)


def on_ma10_mask(df: pd.DataFrame, strict_tol: Optional[float] = None) -> np.ndarray:
    """True where the 10-day SMA of closes lies inside [low, high]; with ``strict_tol`` also within that share of the
    close from the body's midpoint."""
    h, l, o, c = (df[k].astype(float).to_numpy() for k in ("High", "Low", "Open", "Close"))
    ma = df["Close"].astype(float).rolling(10, min_periods=10).mean().to_numpy()
    ok = np.isfinite(ma) & (ma >= l) & (ma <= h)
    if strict_tol is not None:
        ok &= np.abs(ma - (o + c) / 2.0) <= strict_tol * c
    return ok


def doji_on_ma10_events(frames: Dict[str, pd.DataFrame], spy_close: pd.Series, horizons: Sequence[int] = HORIZONS, body_max: float = BODY_MAX,
                        min_range: float = MIN_RANGE, min_gap: int = MIN_GAP, local_window: int = 63, random_draws: int = 10,
                        seed: int = 7) -> pd.DataFrame:
    """One row per doji on the 10-day MA with forward returns, SPY and local-random excess and context columns."""
    rows: List[Dict] = []
    hmax = max(horizons)
    for s, df in frames.items():
        if df is None or len(df) < 80:
            continue
        df = df.dropna(subset=["Open", "High", "Low", "Close"])
        o, h, l, c = (df[k].astype(float).to_numpy() for k in ("Open", "High", "Low", "Close"))
        n = len(c)
        close = df["Close"].astype(float)
        ma10 = close.rolling(10, min_periods=10).mean().to_numpy()
        ma50 = close.rolling(50, min_periods=50).mean().to_numpy()
        tr = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)), np.abs(l - np.roll(c, 1))))
        tr[0] = h[0] - l[0]
        atr20 = pd.Series(tr).rolling(20, min_periods=20).mean().to_numpy()
        spy = spy_close.reindex(df.index).ffill().to_numpy(dtype=float)
        mask = doji_mask(df, body_max, min_range) & on_ma10_mask(df)
        strict = on_ma10_mask(df, STRICT_TOL)
        rng = np.random.default_rng(seed + zlib.crc32(s.encode()) % 100000)
        last = -10 ** 6
        for t in np.flatnonzero(mask):
            t = int(t)
            if t < 55 or t - last < min_gap or t + hmax >= n:
                continue
            last = t
            row = {"symbol": s, "date": df.index[t], "close": float(c[t]), "ma10": float(ma10[t]), "on_line": bool(strict[t]),
                   "body_pct": float(abs(c[t] - o[t]) / (h[t] - l[t])), "range_atr": float((h[t] - l[t]) / atr20[t]) if atr20[t] > 0 else np.nan,
                   "ma10_slope": float(ma10[t] / ma10[t - 5] - 1.0), "ret_5_before": float(c[t] / c[t - 5] - 1.0),
                   "from_above": bool(c[t - 5] > ma10[t - 5] * 1.01), "from_below": bool(c[t - 5] < ma10[t - 5] * 0.99),
                   "above_ma50": bool(c[t] > ma50[t]) if np.isfinite(ma50[t]) else None, "day_ret": float(c[t] / c[t - 1] - 1.0)}
            for hz in horizons:
                r = c[t + hz] / c[t] - 1.0
                row[f"ret_{hz}"] = float(r)
                row[f"oret_{hz}"] = float(c[t + hz] / o[t + 1] - 1.0) if o[t + 1] > 0 else np.nan
                row[f"xspy_{hz}"] = float(r - (spy[t + hz] / spy[t] - 1.0)) if np.isfinite(spy[t]) and np.isfinite(spy[t + hz]) else np.nan
                lo_, hi_ = max(1, t - local_window), min(n - hz - 1, t + local_window)
                cand = np.arange(lo_, hi_ + 1)
                cand = cand[np.abs(cand - t) > hz]
                if len(cand) >= 5:
                    pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                    row[f"xloc_{hz}"] = float(r - np.mean(c[pick + hz] / c[pick] - 1.0))
                else:
                    row[f"xloc_{hz}"] = np.nan
            rows.append(row)
    return pd.DataFrame(rows)


def base_rates(frames: Dict[str, pd.DataFrame], start, end, horizons: Sequence[int] = HORIZONS) -> Dict[str, float]:
    """Unconditional mean return and share of up moves over every day of every stock between ``start`` and ``end``."""
    acc = {f"ret_{hz}": [] for hz in horizons}
    hit = {f"hit_{hz}": [] for hz in horizons}
    for df in frames.values():
        if df is None or len(df) < 80:
            continue
        c = df["Close"].astype(float).to_numpy()
        idx = df.index
        for hz in horizons:
            r = c[hz:] / c[:-hz] - 1.0
            d = idx[:-hz]
            m = (d >= start) & (d <= end)
            acc[f"ret_{hz}"].append(r[m])
            hit[f"hit_{hz}"].append(r[m] > 0)
    out = {"n": int(sum(len(x) for x in acc[f"ret_{horizons[0]}"]))}
    for hz in horizons:
        r = np.concatenate(acc[f"ret_{hz}"]) if acc[f"ret_{hz}"] else np.array([])
        out[f"ret_{hz}"] = float(np.nanmean(r)) if len(r) else np.nan
        out[f"hit_{hz}"] = float(np.nanmean(np.concatenate(hit[f"hit_{hz}"]))) if len(r) else np.nan
    return out


def context_base_rates(frames: Dict[str, pd.DataFrame], start, end, horizons: Sequence[int] = HORIZONS) -> pd.DataFrame:
    """The same context splits over every bar of every stock in the window, doji or not: the control for the context
    table (does the doji add anything beyond the trend it sits in?)."""
    parts = []
    for s, df in frames.items():
        if df is None or len(df) < 80:
            continue
        df = df.dropna(subset=["Open", "High", "Low", "Close"])
        h, l, c = (df[k].astype(float).to_numpy() for k in ("High", "Low", "Close"))
        close = df["Close"].astype(float)
        ma10 = close.rolling(10, min_periods=10).mean().to_numpy()
        ma50 = close.rolling(50, min_periods=50).mean().to_numpy()
        tr = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)), np.abs(l - np.roll(c, 1))))
        tr[0] = h[0] - l[0]
        atr20 = pd.Series(tr).rolling(20, min_periods=20).mean().to_numpy()
        n = len(c)
        hmax = max(horizons)
        t = np.arange(55, n - hmax)
        d = df.index[t]
        m = (d >= start) & (d <= end)
        t = t[m]
        if not len(t):
            continue
        with np.errstate(invalid="ignore", divide="ignore"):
            rec = {"ma10_slope": ma10[t] / ma10[t - 5] - 1.0, "from_above": c[t - 5] > ma10[t - 5] * 1.01, "from_below": c[t - 5] < ma10[t - 5] * 0.99,
                   "above_ma50": c[t] > ma50[t], "range_atr": (h[t] - l[t]) / atr20[t], "ret_5_before": c[t] / c[t - 5] - 1.0, "doji": doji_mask(df)[t] & on_ma10_mask(df)[t]}
            for hz in horizons:
                rec[f"ret_{hz}"] = c[t + hz] / c[t] - 1.0
        parts.append(pd.DataFrame(rec))
    if not parts:
        return pd.DataFrame()
    allday = pd.concat(parts, ignore_index=True)
    groups = [("all", allday), ("MA10 rising", allday[allday["ma10_slope"] > 0]), ("MA10 falling", allday[allday["ma10_slope"] <= 0]),
              ("pullback from above", allday[allday["from_above"]]), ("bounce from below", allday[allday["from_below"]]),
              ("above MA50", allday[allday["above_ma50"]]), ("below MA50", allday[~allday["above_ma50"]]),
              ("range >= 1.2 ATR", allday[allday["range_atr"] >= 1.2]), ("range < 0.8 ATR", allday[allday["range_atr"] < 0.8]),
              ("down day before (5 bars < -2%)", allday[allday["ret_5_before"] < -0.02]), ("up run before (5 bars > +2%)", allday[allday["ret_5_before"] > 0.02])]
    rows = []
    for name, g in groups:
        if not len(g):
            continue
        rec = {"group": name, "n (any day)": int(len(g)), "n (doji)": int(g["doji"].sum())}
        for hz in horizons:
            dj, nd = g[g["doji"]], g[~g["doji"]]
            rec[f"ret_{hz} any day"] = float(g[f"ret_{hz}"].mean())
            rec[f"hit_{hz} any day"] = float((g[f"ret_{hz}"] > 0).mean())
            rec[f"ret_{hz} doji"] = float(dj[f"ret_{hz}"].mean()) if len(dj) else np.nan
            rec[f"hit_{hz} doji"] = float((dj[f"ret_{hz}"] > 0).mean()) if len(dj) else np.nan
            a, b = dj[f"ret_{hz}"].dropna(), nd[f"ret_{hz}"].dropna()
            rec[f"t_{hz} doji-rest"] = float((a.mean() - b.mean()) / np.sqrt(a.var() / len(a) + b.var() / len(b))) if len(a) > 2 and len(b) > 2 else np.nan
        rows.append(rec)
    return pd.DataFrame(rows)


def _stats(g: pd.DataFrame, hz: int, col: str = "ret") -> Dict:
    x = g[f"xloc_{hz}"].dropna()
    t = float(x.mean() / x.std() * np.sqrt(len(x))) if len(x) > 2 and x.std() > 0 else np.nan
    r = g[f"{col}_{hz}"]
    return {f"ret_{hz}": float(r.mean()), f"med_{hz}": float(r.median()), f"hit_{hz}": float((r > 0).mean()),
            f"xspy_{hz}": float(g[f"xspy_{hz}"].mean()), f"xloc_{hz}": float(x.mean()) if len(x) else np.nan, f"t_{hz}": t}


def summarise(ev: pd.DataFrame, horizons: Sequence[int] = HORIZONS, col: str = "ret") -> pd.DataFrame:
    """Rows: all events, strict on-line events, and each context split (with n per side)."""
    if not len(ev):
        return pd.DataFrame()
    groups = [("all", ev), ("on the line (strict)", ev[ev["on_line"]]),
              ("MA10 rising", ev[ev["ma10_slope"] > 0]), ("MA10 falling", ev[ev["ma10_slope"] <= 0]),
              ("pullback from above", ev[ev["from_above"]]), ("bounce from below", ev[ev["from_below"]]),
              ("above MA50", ev[ev["above_ma50"] == True]), ("below MA50", ev[ev["above_ma50"] == False]),  # noqa: E712
              ("range >= 1.2 ATR", ev[ev["range_atr"] >= 1.2]), ("range < 0.8 ATR", ev[ev["range_atr"] < 0.8]),
              ("down day before (5 bars < -2%)", ev[ev["ret_5_before"] < -0.02]), ("up run before (5 bars > +2%)", ev[ev["ret_5_before"] > 0.02])]
    rows = []
    for name, g in groups:
        if not len(g):
            continue
        rec = {"group": name, "n": int(len(g))}
        for hz in horizons:
            rec.update(_stats(g, hz, col))
        rows.append(rec)
    return pd.DataFrame(rows)


def sensitivity(frames: Dict[str, pd.DataFrame], spy_close: pd.Series, start, end, horizons: Sequence[int] = HORIZONS, min_gap: int = MIN_GAP,
                local_window: int = 63) -> pd.DataFrame:
    """Body thresholds 5/10/20% x (MA inside the range / strict on the line) at the last horizon, within the window."""
    hz = horizons[-1]
    rows = []
    for body in (0.05, 0.10, 0.20):
        ev = doji_on_ma10_events(frames, spy_close, horizons, body_max=body, min_gap=min_gap, local_window=local_window)
        if not len(ev):
            continue
        d = pd.to_datetime(ev["date"])
        ev = ev[(d >= start) & (d <= end)]
        for name, g in (("MA10 inside the range", ev), ("strict on the line", ev[ev["on_line"]])):
            if len(g) < 5:
                continue
            st = _stats(g, hz)
            rows.append({"body <= % of range": f"{body:.0%}", "position": name, "n": len(g), f"ret_{hz}": st[f"ret_{hz}"], f"hit_{hz}": st[f"hit_{hz}"],
                         f"xloc_{hz}": st[f"xloc_{hz}"], f"t_{hz}": st[f"t_{hz}"], "ret_1": float(g["ret_1"].mean()), "hit_1": float((g["ret_1"] > 0).mean())})
    return pd.DataFrame(rows)


def by_year(ev: pd.DataFrame, horizons: Sequence[int] = HORIZONS) -> pd.DataFrame:
    e = ev.copy()
    e["year"] = pd.to_datetime(e["date"]).dt.year
    hz = horizons[-1]

    def agg(g):
        rec = {"n": len(g)}
        for k in horizons:
            rec[f"ret_{k}"] = g[f"ret_{k}"].mean()
            rec[f"hit_{k}"] = (g[f"ret_{k}"] > 0).mean()
        rec[f"xloc_{hz}"] = g[f"xloc_{hz}"].mean()
        return pd.Series(rec)
    return e.groupby("year").apply(agg, include_groups=False).reset_index()


def verdict(summ_year: pd.DataFrame, summ_train: pd.DataFrame, summ_test: pd.DataFrame, hz: int = 21, threshold: float = 0.005) -> Dict:
    """Passes when the local-random excess at ``hz`` bars is at least ``threshold`` (same sign) in the last year, in train
    and in test, with 30+ events in each, for the 'all' group. A direction (up or down) only counts with the sign agreeing."""
    def row(s):
        r = s[s["group"] == "all"]
        return None if not len(r) else r.iloc[0]
    y, a, b = row(summ_year), row(summ_train), row(summ_test)
    if y is None or a is None or b is None:
        return {"passed": False, "reason": "no events"}
    xs = [float(y[f"xloc_{hz}"]), float(a[f"xloc_{hz}"]), float(b[f"xloc_{hz}"])]
    ns = [int(y["n"]), int(a["n"]), int(b["n"])]
    up = all(x >= threshold for x in xs) and all(n >= 30 for n in ns)
    down = all(x <= -threshold for x in xs) and all(n >= 30 for n in ns)
    return {"passed": bool(up or down), "direction": "up" if up else ("down" if down else "none"),
            "year": {"n": ns[0], "xloc": xs[0], "hit": float(y[f"hit_{hz}"]), "ret": float(y[f"ret_{hz}"])},
            "train": {"n": ns[1], "xloc": xs[1], "hit": float(a[f"hit_{hz}"]), "ret": float(a[f"ret_{hz}"])},
            "test": {"n": ns[2], "xloc": xs[2], "hit": float(b[f"hit_{hz}"]), "ret": float(b[f"ret_{hz}"])}}


def _pct(v, d=1):
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def _table(df: pd.DataFrame) -> str:
    d = df.copy()
    for col in d.columns:
        if col.startswith(("ret_", "med_", "xspy_", "xloc_")):
            d[col] = d[col].map(lambda v: _pct(v, 2))
        elif col.startswith("hit_"):
            d[col] = d[col].map(lambda v: "" if v is None or not np.isfinite(v) else f"{v * 100:.0f}%")
        elif col.startswith("t_"):
            d[col] = d[col].map(lambda v: "" if not np.isfinite(v) else f"{v:.1f}")
    return d.to_markdown(index=False)


def write_doji_report(doc_path: Path, frames: Dict[str, pd.DataFrame], spy_close: pd.Series, split: str, out_dir: Optional[Path] = None,
                      window: int = WINDOW, horizons: Sequence[int] = HORIZONS, weekly: bool = False) -> Path:
    """``weekly=True`` resamples the daily frames to weekly bars first and uses weekly horizons (1, 4, 12 weeks), a
    52-week main window, a 2-bar gap between events and +-26 weeks for the random days."""
    doc_path = Path(doc_path)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    bar = "week" if weekly else "day"
    if weekly:
        frames = weekly_frames(frames)
        spy_close = to_weekly(spy_close.to_frame("Close").assign(Open=spy_close, High=spy_close, Low=spy_close))["Close"]
        horizons = tuple(horizons) if tuple(horizons) != HORIZONS else WEEKLY_HORIZONS
        window = window if window != WINDOW else WEEKLY_WINDOW
    min_gap, local_window = (2, 26) if weekly else (MIN_GAP, 63)
    hz = horizons[-1]
    ev = doji_on_ma10_events(frames, spy_close, horizons, min_gap=min_gap, local_window=local_window)
    if not len(ev):
        doc_path.write_text("# Doji on the 10-day MA\n\nNo events.\n", encoding="utf-8")
        return doc_path
    d = pd.to_datetime(ev["date"])
    last_date = max(df.index[-1] for df in frames.values() if df is not None and len(df))
    # the last `window` bars of the longest frame define the one-year window
    dates = max((df.index for df in frames.values() if df is not None and len(df)), key=len)
    start = dates[-window] if len(dates) >= window else dates[0]
    ev_year = ev[(d >= start)]
    ev_train, ev_test = ev[d < split], ev[d >= split]
    s_year, s_train, s_test = summarise(ev_year, horizons), summarise(ev_train, horizons), summarise(ev_test, horizons)
    s_year_open = summarise(ev_year, horizons, col="oret")
    base = base_rates(frames, start, last_date, horizons)
    ctx = context_base_rates(frames, start, last_date, horizons)
    sens = sensitivity(frames, spy_close, start, last_date, horizons, min_gap=min_gap, local_window=local_window)
    years = by_year(ev, horizons)
    v = verdict(s_year, s_train, s_test, hz=hz)
    if out_dir:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ev.to_csv(out_dir / "doji_ma10_events.csv", index=False)
        s_year.to_csv(out_dir / "doji_ma10_last_year.csv", index=False)
        pd.concat([s_train.assign(period="train"), s_test.assign(period="test")]).to_csv(out_dir / "doji_ma10_train_test.csv", index=False)
        sens.to_csv(out_dir / "doji_ma10_sensitivity.csv", index=False)
        years.to_csv(out_dir / "doji_ma10_by_year.csv", index=False)
        ctx.to_csv(out_dir / "doji_ma10_context_control.csv", index=False)
    yr = s_year[s_year["group"] == "all"].iloc[0] if len(s_year) else None
    hz_txt = ", ".join(str(k) for k in horizons[:-1]) + f" and {hz} {bar}s"
    md = [f"# A doji sitting on the 10-{bar} moving average ({'weekly' if weekly else 'daily'} bars)", "",
          f"Event: a {'weekly' if weekly else 'daily'} candle whose body is at most {BODY_MAX:.0%} of its high-low range (range at least {MIN_RANGE:.2%} "
          f"of the close) with the 10-{bar} simple moving average of closes inside the candle's low-high range; at most one event per stock per {min_gap} "
          f"{bar}s. Returns are close-to-close from the doji's close at {hz_txt} (and from the next open in a separate table). *xloc* = the return minus "
          f"the mean return of 10 random {bar}s of the same stock within +-{local_window} {bar}s over the same horizon, *xspy* = minus the SPY over the "
          f"same window, *hit* = share of positive returns, *med* = median, *t* = t-statistic of xloc. {len(ev)} events in {ev['symbol'].nunique()} "
          f"stocks, {d.min().date()} to {d.max().date()}; the main window is the last {window} {bar}s ({start.date()} to {last_date.date()}, "
          f"{len(ev_year)} events); the ten-year train < {split} / test >= {split} split is the robustness check."
          + (" Weekly bars are Monday-to-Friday aggregates of the daily cache (open = first, high = max, low = min, close = last); weeks with fewer than "
             "3 sessions and the current unfinished week are dropped. The context splits use the same bar counts (MA10 = 10 weeks, MA50 = 50 weeks, "
             "ATR20 = 20 weeks, the 5-bar move before = 5 weeks)." if weekly else ""), ""]
    md += ["## Verdict", ""]
    if v.get("reason"):
        md.append(f"No verdict: {v['reason']}.")
    else:
        md.append(f"**{'Passed' if v['passed'] else 'Not passed'}** (direction: {v['direction']}) at {hz} {bar}s for all events. The rule: at least +0.5% "
                  f"(or at most -0.5%) over random days of the same stock in the last year, in train and in test, with 30+ events each. Last year: xloc "
                  f"{_pct(v['year']['xloc'], 2)}, hit {v['year']['hit']:.0%}, raw {_pct(v['year']['ret'], 2)} (n {v['year']['n']}); train {_pct(v['train']['xloc'], 2)} "
                  f"(n {v['train']['n']}); test {_pct(v['test']['xloc'], 2)} (n {v['test']['n']}).")
    if yr is not None:
        after = ", ".join(f"{k} {bar}{'s' if k > 1 else ''} {_pct(yr[f'ret_{k}'], 2)} (hit {yr[f'hit_{k}']:.0%})" for k in horizons)
        anyd = ", ".join(f"{k} {bar}{'s' if k > 1 else ''} {_pct(base[f'ret_{k}'], 2)} (up {base[f'hit_{k}']:.0%})" for k in horizons)
        md += ["", f"Last year, after the doji: {after}. The same stocks on any {bar} over the same period: {anyd}, n {base['n']:,} stock-{bar}s."]
    md += ["", f"## Last {window} {bar}s, by context (close-to-close)", "", _table(s_year), "",
           f"## Last {window} {bar}s, from the next open (a trade's entry)", "", _table(s_year_open), "",
           f"## Control: the same context on any {bar} of the last {window} {bar}s (doji or not)", "",
           f"Every stock-{bar} in the window split by the same context; the doji columns are the dojis on the MA10 within that context (no {min_gap}-{bar} "
           f"gap here, so n differs a little from the table above) and *t doji-rest* is the Welch t of the doji {bar}s against the other {bar}s of the "
           f"same context. If the doji adds nothing, its columns match the any-{bar} columns.", "", _table(ctx) if len(ctx) else "No data.", "",
           "## Sensitivity (last year, body threshold x position on the line)", "", _table(sens) if len(sens) else "No events.", "",
           "## Ten years, train / test", "", "Train:", "", _table(s_train) if len(s_train) else "No events.", "", "Test:", "",
           _table(s_test) if len(s_test) else "No events.", "", "## By year (all events)", "", _table(years), "",
           "Survivorship bias applies (today's index members). Overlapping windows inflate t. A side study: nothing here enters the daily report. "
           "Systematic screens and a forward test, not investment advice.", ""]
    doc_path.write_text("\n".join(md), encoding="utf-8")
    return doc_path
