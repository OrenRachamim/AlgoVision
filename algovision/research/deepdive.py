"""Deep dive on one pattern: what, if anything, makes it more profitable?

Discipline against data-mining: every question is answered on a *training*
period and then checked on a held-out *test* period.  Only effects that hold
in both are reported as findings.
"""

from __future__ import annotations

import zlib
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats as sps

from algovision.core.pivots import atr
from algovision.core.types import DetectorConfig
from algovision.data.provider import DataProvider
from algovision.patterns import detect_all
from algovision.research.events import HORIZONS, build_events, simulate_trade
from algovision.research.stats import bootstrap_mean_ci, wilson

FEATURES = [
    "score", "width", "scale", "convergence", "touches", "max_residual", "prior_trend", "volume_trend",
    "height_pct", "breakout_vol_ratio", "gap_from_level", "delay_bars", "dist_ma200", "dist_ma50",
    "atr_pct", "ret_126", "spy_above_ma200", "breakout_close_strength", "apex_gap",
]

_PROVIDER: Optional[DataProvider] = None
_SPY: Optional[pd.DataFrame] = None


def _init(provider_kwargs: Dict, period: str, interval: str) -> None:
    global _PROVIDER, _SPY
    import warnings
    warnings.filterwarnings("ignore")
    _PROVIDER = DataProvider(**provider_kwargs)
    _SPY = _PROVIDER.get("SPY", period, interval)


def context_features(df: pd.DataFrame, spy: Optional[pd.DataFrame], signal: int) -> Dict:
    close = df["Close"].to_numpy(dtype=float)
    high = df["High"].to_numpy(dtype=float)
    low = df["Low"].to_numpy(dtype=float)
    open_ = df["Open"].to_numpy(dtype=float)
    a = atr(df)
    s = signal
    ma200 = close[max(0, s - 199):s + 1].mean()
    ma50 = close[max(0, s - 49):s + 1].mean()
    out = {
        "dist_ma200": close[s] / ma200 - 1.0,
        "dist_ma50": close[s] / ma50 - 1.0,
        "atr_pct": a[s] / close[s],
        "ret_126": close[s] / close[max(0, s - 126)] - 1.0,
        "breakout_close_strength": (close[s] - low[s]) / (high[s] - low[s]) if high[s] > low[s] else 0.5,
        "breakout_gap": open_[s] / close[s - 1] - 1.0 if s > 0 else 0.0,
    }
    if spy is not None:
        sc = spy["Close"].reindex(df.index).ffill().to_numpy(dtype=float)
        sma = sc[max(0, s - 199):s + 1].mean()
        out["spy_above_ma200"] = float(sc[s] > sma)
        out["spy_ret_20"] = sc[s] / sc[max(0, s - 20)] - 1.0
    return out


def _task(args) -> Tuple[str, List[Dict], Optional[str]]:
    symbol, pattern, period, interval, cfg_dict = args
    try:
        df = _PROVIDER.get(symbol, period, interval)
        if len(df) < 300:
            return symbol, [], "short"
        cfg = DetectorConfig(**cfg_dict)
        matches = [m for m in detect_all(df, symbol=symbol, config=cfg) if m.pattern == pattern]
        events, _ = build_events(symbol, df, _SPY, cfg, matches=matches)
        from algovision.research.events import structure_complete_idx
        by_signal = {}
        for m in matches:
            if m.status == "confirmed" and m.breakout_idx is not None:
                by_signal.setdefault(max(int(m.breakout_idx), structure_complete_idx(m)), m)
        close = df["Close"].to_numpy(dtype=float)
        for e in events:
            m = by_signal.get(e["signal_idx"])
            if m is None:
                continue
            mt = m.metrics
            price = close[m.start_idx]
            e.update({
                "start_idx": m.start_idx, "convergence": mt.get("convergence"), "touches": mt.get("touches"),
                "max_residual": mt.get("max_residual"), "prior_trend": mt.get("prior_trend"),
                "volume_trend": mt.get("volume_trend"), "violations": mt.get("violations"),
                "upper_slope": mt.get("upper_slope"), "lower_slope": mt.get("lower_slope"),
                "apex_gap": (mt.get("apex") - m.end_idx) / max(1, m.width) if mt.get("apex") is not None else np.nan,
                "height_pct": abs(m.lines[0].y0 - m.lines[1].y0) / price if len(m.lines) >= 2 else np.nan,
                "level_at_signal": m.level, "stop_pattern": m.stop, "target_pattern": m.target,
                "atr_at_signal": float(atr(df)[e["signal_idx"]]),
            })
            e.update(context_features(df, _SPY, e["signal_idx"]))
        return symbol, events, None
    except Exception as exc:  # noqa: BLE001
        return symbol, [], str(exc)


def collect_pattern_events(symbols: Sequence[str], provider_kwargs: Dict, pattern: str,
                           config: Optional[DetectorConfig] = None, period: str = "10y", interval: str = "1d",
                           workers: int = 4, progress=None) -> Tuple[pd.DataFrame, Dict[str, str]]:
    cfg = config or DetectorConfig()
    rows: List[Dict] = []
    errors: Dict[str, str] = {}
    with ProcessPoolExecutor(max_workers=workers, initializer=_init, initargs=(provider_kwargs, period, interval)) as ex:
        futs = [ex.submit(_task, (s, pattern, period, interval, cfg.to_dict())) for s in symbols]
        for i, f in enumerate(as_completed(futs), 1):
            sym, ev, err = f.result()
            rows.extend(ev)
            if err and err != "short":
                errors[sym] = err
            if progress and (i % 50 == 0 or i == len(futs)):
                progress(i, len(futs), len(rows))
    return pd.DataFrame(rows), errors


# ----------------------------------------------------------------------------
# analyses
# ----------------------------------------------------------------------------
def _stats(g: pd.DataFrame, h: int = 20) -> Dict:
    r = g[f"ret_{h}"].to_numpy(dtype=float)
    x = g[f"xloc_{h}"].to_numpy(dtype=float) if f"xloc_{h}" in g.columns else g[f"xrand_{h}"].to_numpy(dtype=float)
    ok = np.isfinite(r) & np.isfinite(x)
    r, x = r[ok], x[ok]
    if len(r) == 0:
        return {"n": 0}
    lo, hi = bootstrap_mean_ci(x, reps=500)
    rr = g["r_multiple"].to_numpy(dtype=float)
    rr = rr[np.isfinite(rr)]
    return {"n": int(len(r)), "ret": float(r.mean()), "hit": float((r > 0).mean()), "xloc": float(x.mean()),
            "xloc_lo": lo, "xloc_hi": hi, "avg_r": float(rr.mean()) if len(rr) else np.nan,
            "pf": float(rr[rr > 0].sum() / -rr[rr < 0].sum()) if len(rr) and (rr < 0).any() else np.nan,
            "target_rate": float((g["exit_reason"] == "target").mean())}


def split_periods(events: pd.DataFrame, split_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    d = pd.to_datetime(events["signal_date"])
    return events[d < split_date], events[d >= split_date]


def feature_table(events: pd.DataFrame, split_date: str, features: Sequence[str] = FEATURES, h: int = 20,
                  bins: int = 3, min_events: int = 100, min_bin: int = 20) -> pd.DataFrame:
    """Tercile splits defined on the training period, evaluated on both periods."""
    train, test = split_periods(events, split_date)
    rows = []
    for f in features:
        if f not in events.columns or events[f].notna().sum() < min_events:
            continue
        v = train[f].astype(float)
        if v.nunique() <= 2:
            edges = None
        else:
            edges = np.unique(np.quantile(v.dropna(), np.linspace(0, 1, bins + 1)))
            if len(edges) < 3:
                edges = None
        for name, g in (("train", train), ("test", test)):
            x = g[f].astype(float)
            if edges is None:
                lab = x.round().astype("Int64").astype(str)
            else:
                lab = pd.cut(x, edges, labels=[f"T{i + 1}" for i in range(len(edges) - 1)], include_lowest=True).astype(str)
            for b, gg in g.groupby(lab):
                if b == "<NA>" or b == "nan" or len(gg) < min_bin:
                    continue
                s = _stats(gg, h)
                rows.append({"feature": f, "period": name, "bin": b, **s})
        # rank correlation in both periods
        for name, g in (("train", train), ("test", test)):
            ok = g[f].notna() & g[f"xloc_{h}"].notna()
            if ok.sum() > 30:
                rho, p = sps.spearmanr(g.loc[ok, f], g.loc[ok, f"xloc_{h}"])
                rows.append({"feature": f, "period": name, "bin": "rho", "n": int(ok.sum()), "xloc": float(rho), "hit": float(p)})
    return pd.DataFrame(rows)


def consistent_features(ft: pd.DataFrame, min_effect: float = 0.005) -> pd.DataFrame:
    """Features whose top-vs-bottom tercile gap has the same sign and size in train and test."""
    out = []
    for f, g in ft[ft["bin"].str.startswith("T")].groupby("feature"):
        rec = {"feature": f}
        ok = True
        for period in ("train", "test"):
            gg = g[g["period"] == period].set_index("bin")
            if "T1" not in gg.index or gg.index[-1] == "T1":
                ok = False
                break
            top = gg.iloc[-1]
            rec[f"{period}_T1_xloc"] = gg.loc["T1", "xloc"]
            rec[f"{period}_T3_xloc"] = top["xloc"]
            rec[f"{period}_gap"] = top["xloc"] - gg.loc["T1", "xloc"]
            rec[f"{period}_n"] = int(gg["n"].sum())
        if not ok:
            continue
        rec["consistent"] = bool(np.sign(rec["train_gap"]) == np.sign(rec["test_gap"]) and
                                 min(abs(rec["train_gap"]), abs(rec["test_gap"])) >= min_effect)
        out.append(rec)
    return pd.DataFrame(out).sort_values("consistent", ascending=False) if out else pd.DataFrame()


def exit_table(events: pd.DataFrame, get_frame: Callable[[str], pd.DataFrame], split_date: str,
               max_hold: int = 60) -> pd.DataFrame:
    """Compare exit rules; R is measured against each rule's own stop."""
    rules = {
        "time 10": dict(target=None, stop=None, hold=10),
        "time 20": dict(target=None, stop=None, hold=20),
        "time 40": dict(target=None, stop=None, hold=40),
        "time 60": dict(target=None, stop=None, hold=60),
        "pattern target / pattern stop (60)": dict(target="pattern", stop="pattern", hold=60),
        "pattern target / 2 ATR stop (60)": dict(target="pattern", stop="atr2", hold=60),
        "no target / pattern stop (20)": dict(target=None, stop="pattern", hold=20),
        "no target / 2 ATR stop (20)": dict(target=None, stop="atr2", hold=20),
        "no target / 3 ATR stop (40)": dict(target=None, stop="atr3", hold=40),
        "+1 height target / pattern stop (60)": dict(target="height", stop="pattern", hold=60),
        "+2 ATR target / 2 ATR stop (20)": dict(target="atr2", stop="atr2", hold=20),
    }
    frames: Dict[str, pd.DataFrame] = {}
    per_rule: Dict[str, List[Dict]] = {k: [] for k in rules}
    for row in events.itertuples():
        sym = row.symbol
        if sym not in frames:
            frames[sym] = get_frame(sym)
        df = frames[sym]
        high, low, close = (df[c].to_numpy(dtype=float) for c in ("High", "Low", "Close"))
        e, d, entry = int(row.entry_idx), int(row.dir), float(row.entry)
        a = float(row.atr_at_signal) if np.isfinite(row.atr_at_signal) else np.nan
        height = float(row.height_pct) * entry if np.isfinite(row.height_pct) else np.nan
        for name, spec in rules.items():
            t = spec["target"]
            s = spec["stop"]
            target = (row.target_pattern if t == "pattern" else entry + d * height if t == "height"
                      else entry + d * 2 * a if t == "atr2" else None)
            stop = (row.stop_pattern if s == "pattern" else entry - d * 2 * a if s == "atr2"
                    else entry - d * 3 * a if s == "atr3" else None)
            if (target is not None and not np.isfinite(target)) or (stop is not None and not np.isfinite(stop)):
                continue
            res = simulate_trade(high, low, close, e, entry, d, target, stop, spec["hold"])
            per_rule[name].append({"signal_date": row.signal_date, "ret": res["trade_ret"], "r": res["r_multiple"],
                                   "reason": res["exit_reason"], "bars": res["bars_held"], "mae": res["mae_pct"]})
    rows = []
    for name, lst in per_rule.items():
        d = pd.DataFrame(lst)
        if not len(d):
            continue
        d["period"] = np.where(pd.to_datetime(d["signal_date"]) < split_date, "train", "test")
        for period, g in list(d.groupby("period")) + [("all", d)]:
            rr = g["r"].to_numpy(dtype=float)
            rr = rr[np.isfinite(rr)]
            rows.append({"rule": name, "period": period, "n": len(g), "mean_ret": g["ret"].mean(),
                         "hit": (g["ret"] > 0).mean(), "avg_r": rr.mean() if len(rr) else np.nan,
                         "pf": rr[rr > 0].sum() / -rr[rr < 0].sum() if len(rr) and (rr < 0).any() else np.nan,
                         "target_rate": (g["reason"] == "target").mean(), "stop_rate": (g["reason"] == "stop").mean(),
                         "avg_bars": g["bars"].mean(), "ret_per_bar_bp": g["ret"].mean() / g["bars"].mean() * 1e4})
    return pd.DataFrame(rows)


def entry_table(events: pd.DataFrame, get_frame: Callable[[str], pd.DataFrame], split_date: str, h: int = 20,
                retest_bars: int = 5, retest_tol: float = 0.01) -> pd.DataFrame:
    """Next-open (base) vs. signal-bar close vs. waiting for a retest of the broken line."""
    frames: Dict[str, pd.DataFrame] = {}
    rows = []
    for row in events.itertuples():
        sym = row.symbol
        if sym not in frames:
            frames[sym] = get_frame(sym)
        df = frames[sym]
        o, hi, lo, c = (df[x].to_numpy(dtype=float) for x in ("Open", "High", "Low", "Close"))
        n = len(c)
        s, e, d = int(row.signal_idx), int(row.entry_idx), int(row.dir)
        level = float(row.level_at_signal) if np.isfinite(row.level_at_signal) else np.nan
        rec = {"signal_date": row.signal_date}
        j = s + h
        if j < n:
            rec["signal close"] = d * (c[j] / c[s] - 1.0)
        j = e + h - 1
        if j < n:
            rec["next open"] = d * (c[j] / o[e] - 1.0)
        # retest: first bar within retest_bars whose low (long) touches the level (+tol)
        if np.isfinite(level):
            hit = None
            for k in range(e, min(n, e + retest_bars)):
                touched = (lo[k] <= level * (1 + retest_tol)) if d > 0 else (hi[k] >= level * (1 - retest_tol))
                if touched:
                    hit = k
                    break
            if hit is not None:
                px = min(o[hit], level * (1 + retest_tol)) if d > 0 else max(o[hit], level * (1 - retest_tol))
                j = hit + h - 1
                if j < n:
                    rec["retest (within 5 bars)"] = d * (c[j] / px - 1.0)
                rec["retest_happened"] = 1.0
            else:
                rec["retest_happened"] = 0.0
        rows.append(rec)
    d = pd.DataFrame(rows)
    d["period"] = np.where(pd.to_datetime(d["signal_date"]) < split_date, "train", "test")
    out = []
    for col in ("signal close", "next open", "retest (within 5 bars)"):
        if col not in d.columns:
            continue
        for period, g in list(d.groupby("period")) + [("all", d)]:
            v = g[col].dropna()
            if len(v) < 20:
                continue
            out.append({"entry": col, "period": period, "n": len(v), "mean_ret": v.mean(), "hit": (v > 0).mean(),
                        "share_of_signals": len(v) / len(g)})
    return pd.DataFrame(out)


def portfolio_curve(events: pd.DataFrame, get_frame: Callable[[str], pd.DataFrame], hold: int = 20,
                    max_positions: Optional[int] = None, cost: float = 0.0005, seed: int = 3,
                    random_shift: bool = False) -> pd.Series:
    """Daily equal-weight return series of a portfolio holding every signal for ``hold`` bars.

    Each open position gets weight 1/N(t) where N(t) is the number of open positions that day
    (capital fully invested across positions; cash earns 0 when N(t) == 0).
    """
    frames: Dict[str, pd.DataFrame] = {}
    daily: Dict[pd.Timestamp, List[float]] = {}
    rng = np.random.default_rng(seed)
    for row in events.itertuples():
        sym = row.symbol
        if sym not in frames:
            frames[sym] = get_frame(sym)
        df = frames[sym]
        o, c = df["Open"].to_numpy(dtype=float), df["Close"].to_numpy(dtype=float)
        n = len(c)
        e, d = int(row.entry_idx), int(row.dir)
        if random_shift:
            e = int(np.clip(e + rng.integers(-126, 127), 1, n - hold - 1))
        if e + hold >= n:
            continue
        prev = o[e]
        for k in range(hold):
            j = e + k
            r = d * (c[j] / prev - 1.0)
            if k == 0:
                r -= cost
            prev = c[j]
            daily.setdefault(df.index[j], []).append(r)
    idx = sorted(daily)
    return pd.Series([float(np.mean(daily[t])) for t in idx], index=pd.DatetimeIndex(idx), name="ret")


def curve_stats(r: pd.Series, bench: Optional[pd.Series] = None) -> Dict:
    if len(r) == 0:
        return {}
    eq = (1 + r).cumprod()
    years = (r.index[-1] - r.index[0]).days / 365.25
    cagr = eq.iloc[-1] ** (1 / years) - 1 if years > 0 else np.nan
    vol = r.std() * np.sqrt(252)
    dd = (eq / eq.cummax() - 1).min()
    out = {"days": int(len(r)), "cagr": float(cagr), "vol": float(vol), "sharpe": float(r.mean() / r.std() * np.sqrt(252)) if r.std() > 0 else np.nan,
           "max_drawdown": float(dd), "total_return": float(eq.iloc[-1] - 1),
           "share_of_days_invested": float(len(r) / max(1, len(pd.bdate_range(r.index[0], r.index[-1]))))}
    if bench is not None:
        b = bench.reindex(r.index).fillna(0.0)
        out["bench_total_return"] = float((1 + b).prod() - 1)
        out["bench_sharpe"] = float(b.mean() / b.std() * np.sqrt(252)) if b.std() > 0 else np.nan
    return out


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------
def filter_table(events: pd.DataFrame, split_date: str, h: int = 20) -> pd.DataFrame:
    """A few pre-registered filters, thresholds fixed on the training period."""
    train, test = split_periods(events, split_date)
    q1, q3 = np.quantile(train["ret_126"].dropna(), [1 / 3, 2 / 3])
    med_atr = train["atr_pct"].median()
    rules = {
        "all": lambda g: np.ones(len(g), bool),
        f"beaten down (6m return < {q1 * 100:.0f}%)": lambda g: (g["ret_126"] < q1).to_numpy(),
        "below 200-day MA": lambda g: (g["dist_ma200"] < 0).to_numpy(),
        "beaten down AND below 200-day MA": lambda g: ((g["ret_126"] < q1) & (g["dist_ma200"] < 0)).to_numpy(),
        "beaten down AND high volatility": lambda g: ((g["ret_126"] < q1) & (g["atr_pct"] > med_atr)).to_numpy(),
        f"uptrend (6m return > {q3 * 100:.0f}%)": lambda g: (g["ret_126"] > q3).to_numpy(),
        "above 200-day MA": lambda g: (g["dist_ma200"] >= 0).to_numpy(),
        "SPY below its 200-day MA": lambda g: (g.get("spy_above_ma200", pd.Series(1, index=g.index)) == 0).to_numpy(),
    }
    rows = []
    for name, f in rules.items():
        for period, g in (("train", train), ("test", test)):
            sub = g[f(g)]
            s = _stats(sub, h)
            years = max(1e-9, (pd.to_datetime(g["signal_date"]).max() - pd.to_datetime(g["signal_date"]).min()).days / 365.25)
            s.update(filter=name, period=period, per_year=len(sub) / years)
            rows.append(s)
    return pd.DataFrame(rows).set_index(["filter", "period"])


def write_deepdive_report(out_dir, pattern: str, events: pd.DataFrame, get_frame, split_date: str = "2023-01-01",
                          h: int = 20) -> "Path":
    from pathlib import Path
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    events.to_csv(out / "events.csv", index=False)
    train, test = split_periods(events, split_date)
    base = pd.DataFrame({k: _stats(g, h) for k, g in (("train", train), ("test", test), ("all", events))}).T
    base.to_csv(out / "base.csv")
    by_year = events.groupby("year").apply(lambda g: pd.Series(_stats(g, h)))
    by_year.to_csv(out / "by_year.csv")
    ft = feature_table(events, split_date, h=h)
    ft.to_csv(out / "features.csv", index=False)
    cf = consistent_features(ft)
    cf.to_csv(out / "features_consistent.csv", index=False)
    flt = filter_table(events, split_date, h)
    flt.to_csv(out / "filters.csv")
    ex = exit_table(events, get_frame, split_date)
    ex.to_csv(out / "exits.csv", index=False)
    en = entry_table(events, get_frame, split_date, h)
    en.to_csv(out / "entries.csv", index=False)
    spy = None
    try:
        spy = get_frame("SPY")["Close"].pct_change().dropna()
    except Exception:  # noqa: BLE001
        pass
    c = portfolio_curve(events, get_frame, hold=h)
    r = portfolio_curve(events, get_frame, hold=h, random_shift=True)
    pstats = pd.DataFrame({
        "pattern all": curve_stats(c, spy), "random-shift all": curve_stats(r, spy),
        "pattern test": curve_stats(c[c.index >= split_date], spy), "random-shift test": curve_stats(r[r.index >= split_date], spy),
    })
    pstats.to_csv(out / "portfolio.csv")
    pd.DataFrame({"pattern": c, "random": r}).to_csv(out / "curves.csv")
    _equity_chart(pattern, c, r, spy, split_date, out / "equity.png")

    pct = lambda v: "" if v is None or pd.isna(v) else f"{v * 100:+.2f}%"  # noqa: E731
    md = [f"# Deep dive: {pattern}\n",
          f"{len(events)} confirmed events, {events['symbol'].nunique()} symbols. Training period before {split_date}, "
          f"test period from {split_date}. `xloc` = mean {h}-bar return in excess of random entries within +-6 months "
          "in the same stock and direction.\n",
          "## Base result\n", base.round(4).to_markdown(), "\n## By year\n", by_year.round(4).to_markdown(),
          "\n## Features consistent across train and test (tercile T3 minus T1, thresholds set on train)\n"]
    if len(cf):
        md.append(cf.round(4).to_markdown(index=False))
    md += ["\n## Pre-registered filters\n", flt.round(4).to_markdown(), "\n## Exit rules\n", ex.round(4).to_markdown(index=False),
           "\n## Entry variants\n", en.round(4).to_markdown(index=False), "\n## Portfolio (equal weight, fully invested, 5 bps)\n",
           pstats.round(4).to_markdown()]
    path = out / "report.md"
    path.write_text("\n".join(md), encoding="utf-8")
    return path


def _equity_chart(pattern: str, c: pd.Series, r: pd.Series, spy: Optional[pd.Series], split_date: str, path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    C = {"s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
         "grid": "#e1e0d9", "axis": "#c3c2b7", "surface": "#fcfcfb"}
    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=120)
    fig.patch.set_facecolor(C["surface"])
    ax.set_facecolor(C["surface"])
    ax.plot((1 + c).cumprod(), color=C["s1"], lw=2, label=f"{pattern}, hold 20 bars, equal weight")
    ax.plot((1 + r).cumprod(), color=C["s2"], lw=2, label="same trades shifted to random nearby dates")
    if spy is not None:
        b = spy.reindex(c.index).fillna(0)
        ax.plot((1 + b).cumprod(), color=C["s3"], lw=2, label="SPY buy & hold")
    ax.axvline(pd.Timestamp(split_date), color=C["axis"], lw=1, ls="--")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(colors=C["muted"], labelsize=8)
    ax.grid(True, color=C["grid"], lw=0.6)
    ax.set_axisbelow(True)
    ax.set_yscale("log")
    ax.set_title(f"{pattern}: growth of 1 unit (5 bps per trade, fully invested across open positions)", fontsize=10,
                 loc="left", color=C["ink"])
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
