"""Classic anomalies on the same universe, tested with the same discipline.

* Cross-sectional momentum: rank stocks on past returns, hold the top / bottom
  group for a period, rebalance.  Reported as group returns, long-short spread,
  turnover-adjusted costs, train/test periods.
* Time-series momentum on the index (trend filter).
* Short-term reversal: (a) event study - buy a stock after an N-sigma down day
  and compare with local random entries; (b) weekly cross-sectional reversal.

Survivorship warning: the universe is today's index members, which biases
long-only results upward and, for momentum, removes the delisted losers from
the bottom group.  Group-vs-group comparisons inside the universe are the
robust part; absolute levels are not.
"""

from __future__ import annotations

import zlib
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats as sps

from algovision.research.stats import bootstrap_mean_ci, wilson


# ----------------------------------------------------------------------------
# panel
# ----------------------------------------------------------------------------
def load_panel(symbols: Sequence[str], get_frame: Callable[[str], pd.DataFrame], min_bars: int = 300) -> Dict[str, pd.DataFrame]:
    """Wide Open/High/Low/Close frames (dates x symbols), NaN where a stock has no bar."""
    cols = {"Open": {}, "High": {}, "Low": {}, "Close": {}}
    for s in symbols:
        try:
            df = get_frame(s)
        except Exception:  # noqa: BLE001
            continue
        if len(df) < min_bars:
            continue
        for c in cols:
            cols[c][s] = df[c]
    out = {c: pd.DataFrame(v).sort_index() for c, v in cols.items()}
    idx = out["Close"].index
    return {c: f.reindex(idx) for c, f in out.items()}


def perf_stats(r: pd.Series, periods_per_year: float) -> Dict:
    r = r.dropna()
    if len(r) < 2:
        return {"n": len(r)}
    mean, sd = r.mean(), r.std(ddof=1)
    eq = (1 + r).cumprod()
    years = len(r) / periods_per_year
    return {
        "n": int(len(r)), "ann_return": float(eq.iloc[-1] ** (1 / years) - 1) if years > 0 else np.nan,
        "ann_vol": float(sd * np.sqrt(periods_per_year)),
        "sharpe": float(mean / sd * np.sqrt(periods_per_year)) if sd > 0 else np.nan,
        "t_stat": float(mean / sd * np.sqrt(len(r))) if sd > 0 else np.nan,
        "hit": float((r > 0).mean()), "max_drawdown": float((eq / eq.cummax() - 1).min()),
        "mean_period": float(mean), "total_return": float(eq.iloc[-1] - 1),
    }


# ----------------------------------------------------------------------------
# cross-sectional backtest engine
# ----------------------------------------------------------------------------
def cross_sectional_backtest(panel: Dict[str, pd.DataFrame], signal: Callable[[pd.DataFrame, int], pd.Series],
                             rebalance: str = "M", n_groups: int = 10, cost_bps: float = 10.0,
                             min_names: int = 100) -> Dict[str, pd.DataFrame]:
    """Generic ranked-portfolio backtest.

    ``signal(close, t)`` returns one value per symbol using closes up to row ``t``
    (inclusive).  Trades happen at the *next* open; each holding period runs from
    that open to the open following the next rebalance date.  Groups are
    equal-weighted; ``cost_bps`` is charged per side on turnover.
    """
    close, open_ = panel["Close"], panel["Open"]
    idx = close.index
    if rebalance == "M":
        reb = idx.to_series().groupby([idx.year, idx.month]).tail(1).index
    else:  # weekly
        reb = idx.to_series().groupby([idx.isocalendar().year, idx.isocalendar().week]).tail(1).index
    reb_pos = [idx.get_loc(d) for d in reb]
    rows = []
    prev_groups: Dict[int, set] = {}
    for a, b in zip(reb_pos[:-1], reb_pos[1:]):
        if a + 1 >= len(idx) or b + 1 >= len(idx):
            break
        sig = signal(close, a).dropna()
        valid = sig.index[open_.iloc[a + 1][sig.index].notna() & open_.iloc[b + 1][sig.index].notna()]
        sig = sig[valid]
        if len(sig) < min_names:
            continue
        ranks = pd.qcut(sig.rank(method="first"), n_groups, labels=False) + 1
        ret = open_.iloc[b + 1][sig.index] / open_.iloc[a + 1][sig.index] - 1.0
        rec = {"date": idx[a], "n": len(sig), "universe": float(ret.mean())}
        for g in range(1, n_groups + 1):
            names = set(ranks.index[ranks == g])
            gross = float(ret[list(names)].mean())
            turnover = 1.0 if g not in prev_groups else len(names - prev_groups[g]) / max(1, len(names))
            rec[f"G{g}"] = gross - 2 * turnover * cost_bps / 1e4
            rec[f"G{g}_gross"] = gross
            rec[f"G{g}_turnover"] = turnover
            prev_groups[g] = names
        # long the top group, short the bottom group: both legs pay their own turnover costs
        cost_top = 2 * rec[f"G{n_groups}_turnover"] * cost_bps / 1e4
        cost_bot = 2 * rec["G1_turnover"] * cost_bps / 1e4
        rec["long_short_gross"] = rec[f"G{n_groups}_gross"] - rec["G1_gross"]
        rec["long_short"] = rec["long_short_gross"] - cost_top - cost_bot
        rec["top_minus_universe"] = rec[f"G{n_groups}"] - rec["universe"]
        rec["bottom_minus_universe"] = rec["G1"] - rec["universe"]
        rows.append(rec)
    return pd.DataFrame(rows).set_index("date")


def momentum_signal(lookback: int, skip: int) -> Callable[[pd.DataFrame, int], pd.Series]:
    """Return over [t-lookback, t-skip] in trading days."""
    def f(close: pd.DataFrame, t: int) -> pd.Series:
        if t - lookback < 0:
            return pd.Series(dtype=float)
        a = close.iloc[t - lookback]
        b = close.iloc[t - skip] if skip > 0 else close.iloc[t]
        return (b / a - 1.0).replace([np.inf, -np.inf], np.nan)
    return f


def summarize_groups(bt: pd.DataFrame, periods_per_year: float, n_groups: int = 10, split_date: Optional[str] = None) -> pd.DataFrame:
    rows = []
    periods = [("all", bt)]
    if split_date:
        periods += [("train", bt[bt.index < split_date]), ("test", bt[bt.index >= split_date])]
    for pname, b in periods:
        for col in [f"G{g}" for g in range(1, n_groups + 1)] + ["universe", "long_short", "long_short_gross",
                                                                  "top_minus_universe", "bottom_minus_universe"]:
            s = perf_stats(b[col], periods_per_year)
            s.update(period=pname, portfolio=col)
            if col.startswith("G") and f"{col}_turnover" in b.columns:
                s["turnover"] = float(b[f"{col}_turnover"].mean())
            rows.append(s)
    return pd.DataFrame(rows).set_index(["period", "portfolio"])


def timeseries_momentum(spy: pd.DataFrame, lookback: int = 252, cost_bps: float = 5.0) -> Dict[str, pd.Series]:
    """Long SPY when its trailing return is positive, else cash. Daily, signal lagged one day."""
    c = spy["Close"]
    sig = (c / c.shift(lookback) - 1.0 > 0).astype(float).shift(1)
    daily = c.pct_change()
    pos_change = sig.diff().abs().fillna(0)
    strat = sig * daily - pos_change * cost_bps / 1e4
    ma_sig = (c > c.rolling(200).mean()).astype(float).shift(1)
    strat_ma = ma_sig * daily - ma_sig.diff().abs().fillna(0) * cost_bps / 1e4
    return {"buy_and_hold": daily.dropna(), f"tsmom_{lookback}": strat.dropna(), "ma200": strat_ma.dropna(),
            "exposure_tsmom": sig.dropna(), "exposure_ma200": ma_sig.dropna()}


# ----------------------------------------------------------------------------
# short-term reversal: event study
# ----------------------------------------------------------------------------
def reversal_events(panel: Dict[str, pd.DataFrame], spy_close: pd.Series, thresholds: Sequence[float] = (2.0, 2.5, 3.0),
                    horizons: Sequence[int] = (1, 2, 3, 5, 10), vol_window: int = 60, ret_days: int = 1,
                    random_draws: int = 10, local_window: int = 126, seed: int = 11,
                    require_ma200: Optional[str] = None) -> pd.DataFrame:
    """One row per (symbol, day) whose ``ret_days``-day return is beyond +-threshold sigmas.

    ``direction`` +1 = buy after a crash, -1 = short after a spike.  Forward
    returns from the next open, signed by direction, with local random baselines.
    """
    close, open_ = panel["Close"], panel["Open"]
    rows: List[Dict] = []
    hmax = max(horizons)
    spy_ret = spy_close.reindex(close.index).ffill()
    for s in close.columns:
        c = close[s].to_numpy(dtype=float)
        o = open_[s].to_numpy(dtype=float)
        n = len(c)
        valid = np.isfinite(c) & np.isfinite(o)
        r1 = np.full(n, np.nan)
        r1[1:] = c[1:] / c[:-1] - 1.0
        rk = np.full(n, np.nan)
        rk[ret_days:] = c[ret_days:] / c[:-ret_days] - 1.0
        sd = pd.Series(r1).rolling(vol_window, min_periods=40).std().shift(1).to_numpy() * np.sqrt(ret_days)
        z = rk / sd
        ma200 = pd.Series(c).rolling(200).mean().to_numpy()
        rng = np.random.default_rng(seed + zlib.crc32(s.encode()) % 100000)
        for thr in thresholds:
            for direction in (1, -1):
                hits = np.where(np.isfinite(z) & valid & ((z <= -thr) if direction > 0 else (z >= thr)))[0]
                last = -100
                for t in hits:
                    if t - last < 3:          # one event per cluster
                        continue
                    e = t + 1
                    if e + hmax >= n or not np.isfinite(o[e]):
                        continue
                    last = t
                    if require_ma200 == "below" and not c[t] < ma200[t]:
                        continue
                    if require_ma200 == "above" and not c[t] > ma200[t]:
                        continue
                    row = {"symbol": s, "date": close.index[t], "threshold": thr, "direction": direction, "z": float(z[t]),
                           "move": float(rk[t]), "ret_days": ret_days,
                           "below_ma200": bool(c[t] < ma200[t]) if np.isfinite(ma200[t]) else None,
                           "ret_126": float(c[t] / c[t - 126] - 1.0) if t >= 126 and np.isfinite(c[t - 126]) else np.nan}
                    for h in horizons:
                        j = e + h - 1
                        row[f"ret_{h}"] = direction * (c[j] / o[e] - 1.0)
                        row[f"xspy_{h}"] = row[f"ret_{h}"] - direction * (spy_ret.iloc[j] / spy_ret.iloc[e] - 1.0)
                        lo, hi = max(1, e - local_window), min(n - h - 1, e + local_window)
                        cand = np.arange(lo, hi + 1)
                        cand = cand[(np.abs(cand - e) > h) & np.isfinite(o[cand]) & np.isfinite(c[cand + h - 1])]
                        if len(cand) >= 5:
                            pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                            rr = direction * (c[pick + h - 1] / o[pick] - 1.0)
                            row[f"xloc_{h}"] = row[f"ret_{h}"] - float(rr.mean())
                            row[f"loc_hit_{h}"] = float((rr > 0).mean())
                        else:
                            row[f"xloc_{h}"] = np.nan
                            row[f"loc_hit_{h}"] = np.nan
                    rows.append(row)
    return pd.DataFrame(rows)


def reversal_table(ev: pd.DataFrame, horizons: Sequence[int] = (1, 2, 3, 5, 10), cost: float = 0.0005,
                   split_date: Optional[str] = None, by: Sequence[str] = ("threshold", "direction")) -> pd.DataFrame:
    rows = []
    periods = [("all", ev)]
    if split_date:
        d = pd.to_datetime(ev["date"])
        periods += [("train", ev[d < split_date]), ("test", ev[d >= split_date])]
    for pname, g in periods:
        for key, gg in g.groupby(list(by)):
            rec = {"period": pname, **dict(zip(by, key)), "n": len(gg), "n_symbols": gg["symbol"].nunique(),
                   "avg_move": float(gg["move"].mean())}
            for h in horizons:
                r = gg[f"ret_{h}"].to_numpy(dtype=float) - cost
                x = gg[f"xloc_{h}"].to_numpy(dtype=float)
                ok = np.isfinite(r) & np.isfinite(x)
                if ok.sum() < 20:
                    continue
                lo, hi = bootstrap_mean_ci(x[ok], reps=500)
                rec[f"net_{h}"] = float(r[ok].mean())
                rec[f"hit_{h}"] = float((r[ok] > 0).mean())
                rec[f"lochit_{h}"] = float(np.nanmean(gg[f"loc_hit_{h}"]))
                rec[f"xspy_{h}"] = float(np.nanmean(gg[f"xspy_{h}"]))
                rec[f"xloc_{h}"] = float(x[ok].mean())
                rec[f"xloc_lo_{h}"], rec[f"xloc_hi_{h}"] = lo, hi
                rec[f"t_{h}"] = float(sps.ttest_1samp(x[ok], 0).statistic)
            rows.append(rec)
    return pd.DataFrame(rows).set_index(["period", *by])


def reversal_portfolio(ev: pd.DataFrame, panel: Dict[str, pd.DataFrame], hold: int = 3, cost: float = 0.0005,
                       threshold: float = 2.0, direction: int = 1) -> pd.Series:
    """Daily equal-weight curve of all events with the given threshold/direction."""
    close, open_ = panel["Close"], panel["Open"]
    idx = close.index
    pos = {d: i for i, d in enumerate(idx)}
    daily: Dict[pd.Timestamp, List[float]] = {}
    sub = ev[(ev["threshold"] == threshold) & (ev["direction"] == direction)]
    for row in sub.itertuples():
        t = pos[pd.Timestamp(row.date)]
        c = close[row.symbol].to_numpy(dtype=float)
        o = open_[row.symbol].to_numpy(dtype=float)
        e = t + 1
        if e + hold >= len(c):
            continue
        prev = o[e]
        for k in range(hold):
            j = e + k
            r = direction * (c[j] / prev - 1.0) - (cost if k == 0 else 0.0)
            prev = c[j]
            daily.setdefault(idx[j], []).append(r)
    dates = sorted(daily)
    return pd.Series([float(np.mean(daily[d])) for d in dates], index=pd.DatetimeIndex(dates))


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------
def write_factors_report(out_dir, symbols: Sequence[str], get_frame: Callable[[str], pd.DataFrame],
                         split_date: str = "2023-01-01", cost_bps: float = 10.0, progress=None) -> "Path":
    from pathlib import Path
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    log = progress or (lambda m: None)
    panel = load_panel(symbols, get_frame)
    spy = get_frame("SPY")
    log(f"panel {panel['Close'].shape}")
    md = [f"# Momentum and short-term reversal on {panel['Close'].shape[1]} symbols\n",
          f"Train before {split_date}, test from {split_date}. Ranked portfolios trade at the next open, equal weight, "
          f"{cost_bps:.0f} bps per side on turnover. Survivorship: today's index members.\n"]
    for name, lb, skip, freq, ppy in (("Momentum 12-1", 252, 21, "M", 12), ("Momentum 6-1", 126, 21, "M", 12),
                                      ("Momentum 3-1", 63, 21, "M", 12), ("Last month (1-0)", 21, 0, "M", 12),
                                      ("Weekly reversal (5-day return)", 5, 0, "W", 52)):
        bt = cross_sectional_backtest(panel, momentum_signal(lb, skip), freq, n_groups=10, cost_bps=cost_bps)
        tag = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")
        bt.to_csv(out / f"{tag}_bt.csv")
        summ = summarize_groups(bt, ppy, 10, split_date)
        summ.to_csv(out / f"{tag}_summary.csv")
        md.append(f"## {name}\n")
        md.append(summ.round(3).to_markdown())
        log(name)
    ts = timeseries_momentum(spy)
    tst = pd.DataFrame({k: perf_stats(v, 252) for k, v in ts.items() if not k.startswith("exposure")})
    tst.to_csv(out / "tsmom.csv")
    md.append("## Time-series momentum on SPY (daily, 5 bps per switch)\n")
    md.append(tst.round(3).to_markdown())
    for rd in (1, 3):
        ev = reversal_events(panel, spy["Close"], ret_days=rd)
        ev.to_csv(out / f"reversal_events_{rd}d.csv", index=False)
        tab = reversal_table(ev, split_date=split_date)
        tab.to_csv(out / f"reversal_table_{rd}d.csv")
        md.append(f"## Short-term reversal after a {rd}-day move (event study, 5 bps)\n")
        cols = [c for c in tab.columns if c.split("_")[0] in ("n", "net", "hit", "lochit", "xloc", "t")]
        md.append(tab[cols].round(4).to_markdown())
        log(f"reversal {rd}d: {len(ev)} events")
    path = out / "report.md"
    path.write_text("\n".join(md), encoding="utf-8")
    return path
