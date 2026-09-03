"""Pre-registered anomaly tests beyond chart patterns.

Each test reports train / test periods separately with t-statistics and, where
a trade is implied, returns net of a stated cost.  The bar for "real" is set
before looking: |t| > 2 in *both* periods, positive net of 10 bps per side,
and economically meaningful.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats as sps

from algovision.research.factors import cross_sectional_backtest, perf_stats, summarize_groups
from algovision.research.stats import bootstrap_mean_ci


def _tstat(x: np.ndarray) -> float:
    x = x[np.isfinite(x)]
    return float(x.mean() / x.std(ddof=1) * np.sqrt(len(x))) if len(x) > 2 and x.std() > 0 else np.nan


def _periods(idx: pd.DatetimeIndex, split: str):
    return {"all": np.ones(len(idx), bool), "train": (idx < split), "test": (idx >= split)}


# ----------------------------------------------------------------------------
# 1. news-gap drift (proxy for post-earnings-announcement drift)
# ----------------------------------------------------------------------------
def news_gap_events(panel: Dict[str, pd.DataFrame], spy_close: pd.Series, gap_min: float = 0.04,
                    vol_mult: float = 3.0, horizons: Sequence[int] = (1, 5, 10, 20, 40, 60),
                    local_window: int = 126, random_draws: int = 10, seed: int = 5,
                    entry: str = "close") -> pd.DataFrame:
    """Days where |open / prev close - 1| >= gap_min and volume >= vol_mult x 20-day average.

    ``entry="close"``: enter at the close of the gap day; ``entry="next_open"``: at the
    next day's open (the signal is fully known at the close, so both are point-in-time).
    Returns are signed by the gap direction and measured to the close ``h`` bars after
    the gap day.
    """
    import zlib
    close, open_, vol = panel["Close"], panel["Open"], panel["Volume"]
    spy = spy_close.reindex(close.index).ffill().to_numpy(dtype=float)
    rows: List[Dict] = []
    hmax = max(horizons)
    for s in close.columns:
        c, o, v = close[s].to_numpy(dtype=float), open_[s].to_numpy(dtype=float), vol[s].to_numpy(dtype=float)
        n = len(c)
        gap = np.full(n, np.nan)
        gap[1:] = o[1:] / c[:-1] - 1.0
        avgv = pd.Series(v).rolling(20).mean().shift(1).to_numpy()
        day_ret = np.full(n, np.nan)
        day_ret[1:] = c[1:] / c[:-1] - 1.0
        hits = np.where(np.isfinite(gap) & (np.abs(gap) >= gap_min) & np.isfinite(avgv) & (v >= vol_mult * avgv))[0]
        rng = np.random.default_rng(seed + zlib.crc32(s.encode()) % 100000)
        last = -100
        for t in hits:
            if t - last < 5 or t + hmax >= n or t < 260:
                continue
            last = t
            d = 1 if gap[t] > 0 else -1
            ma200 = np.nanmean(c[t - 199:t + 1])
            row = {"symbol": s, "date": close.index[t], "dir": d, "gap": float(gap[t]), "day_ret": float(day_ret[t]),
                   "vol_ratio": float(v[t] / avgv[t]), "close_vs_open": float(c[t] / o[t] - 1.0),
                   "ret_126": float(c[t] / c[t - 126] - 1.0), "below_ma200": bool(c[t] < ma200)}
            px = c[t] if entry == "close" else o[t + 1]
            row["entry"] = float(px)
            for h in horizons:
                r = d * (c[t + h] / px - 1.0)
                row[f"ret_{h}"] = r
                row[f"xspy_{h}"] = r - d * (spy[t + h] / spy[t] - 1.0)
                lo, hi = max(1, t - local_window), min(n - h - 2, t + local_window)
                cand = np.arange(lo, hi + 1)
                cand = cand[np.abs(cand - t) > h]
                if len(cand) >= 5:
                    pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                    base = c[pick] if entry == "close" else o[pick + 1]
                    row[f"xloc_{h}"] = r - float(np.mean(d * (c[pick + h] / base - 1.0)))
                else:
                    row[f"xloc_{h}"] = np.nan
            rows.append(row)
    return pd.DataFrame(rows)


def news_gap_table(ev: pd.DataFrame, split: str, horizons=(1, 5, 10, 20, 40, 60), cost: float = 0.001,
                   by: Sequence[str] = ("dir",)) -> pd.DataFrame:
    rows = []
    d = pd.to_datetime(ev["date"])
    for pname, mask in (("all", np.ones(len(ev), bool)), ("train", (d < split).to_numpy()), ("test", (d >= split).to_numpy())):
        g0 = ev[mask]
        for key, g in g0.groupby(list(by)):
            rec = {"period": pname, **dict(zip(by, key if isinstance(key, tuple) else (key,))), "n": len(g),
                   "avg_gap": float(g["gap"].mean()), "avg_day_ret": float(g["day_ret"].mean())}
            for h in horizons:
                r = g[f"ret_{h}"].to_numpy(dtype=float) - cost
                x = g[f"xloc_{h}"].to_numpy(dtype=float)
                rec[f"net_{h}"] = float(np.nanmean(r))
                rec[f"hit_{h}"] = float(np.nanmean(r > 0))
                rec[f"xspy_{h}"] = float(np.nanmean(g[f"xspy_{h}"]))
                rec[f"xloc_{h}"] = float(np.nanmean(x))
                rec[f"t_{h}"] = _tstat(x)
            rows.append(rec)
    return pd.DataFrame(rows).set_index(["period", *by])


# ----------------------------------------------------------------------------
# 2. overnight vs intraday
# ----------------------------------------------------------------------------
def overnight_intraday(panel: Dict[str, pd.DataFrame], spy: pd.DataFrame, split: str) -> pd.DataFrame:
    close, open_ = panel["Close"], panel["Open"]
    on = (open_ / close.shift(1) - 1.0)          # close(t-1) -> open(t)
    intra = (close / open_ - 1.0)                 # open(t) -> close(t)
    rows = []
    for name, o_, i_ in (("universe (equal weight)", on.mean(axis=1), intra.mean(axis=1)),
                         ("SPY", spy["Open"] / spy["Close"].shift(1) - 1.0, spy["Close"] / spy["Open"] - 1.0)):
        for pname, mask in _periods(o_.index, split).items():
            for leg, r in (("overnight", o_[mask].dropna()), ("intraday", i_[mask].dropna())):
                st = perf_stats(r, 252)
                st.update(series=name, leg=leg, period=pname, daily_bp=float(r.mean() * 1e4))
                rows.append(st)
    return pd.DataFrame(rows).set_index(["series", "leg", "period"])


# ----------------------------------------------------------------------------
# 3. turn of the month
# ----------------------------------------------------------------------------
def turn_of_month(daily: pd.Series, split: str, last_n: int = 4, first_n: int = 3, cost: float = 0.0005) -> pd.DataFrame:
    """Long only over the last ``last_n`` and first ``first_n`` trading days of each month."""
    idx = daily.index
    ym = idx.to_period("M")
    pos_in_month = pd.Series(np.arange(len(idx)), index=idx).groupby(ym).rank(method="first").astype(int)
    size = pd.Series(np.arange(len(idx)), index=idx).groupby(ym).transform("size")
    in_window = (pos_in_month <= first_n) | (pos_in_month > size - last_n)
    rows = []
    for pname, mask in _periods(idx, split).items():
        r_all = daily[mask]
        r_in = daily[mask & in_window.to_numpy()]
        r_out = daily[mask & ~in_window.to_numpy()]
        strat = daily[mask] * in_window[mask].astype(float) - (in_window[mask].astype(float).diff().abs().fillna(0)) * cost
        rows.append({"period": pname, "days_in": int(len(r_in)), "days_out": int(len(r_out)),
                     "mean_bp_in": float(r_in.mean() * 1e4), "mean_bp_out": float(r_out.mean() * 1e4),
                     "t_diff": float((r_in.mean() - r_out.mean()) / np.sqrt(r_in.var() / len(r_in) + r_out.var() / len(r_out))),
                     "strategy_ann": perf_stats(strat, 252)["ann_return"], "strategy_sharpe": perf_stats(strat, 252)["sharpe"],
                     "buy_hold_ann": perf_stats(r_all, 252)["ann_return"], "buy_hold_sharpe": perf_stats(r_all, 252)["sharpe"],
                     "share_invested": float(in_window[mask].mean())})
    return pd.DataFrame(rows).set_index("period")


# ----------------------------------------------------------------------------
# 4. low volatility (cross-section) and volatility-managed index
# ----------------------------------------------------------------------------
def vol_signal(window: int = 60) -> Callable[[pd.DataFrame, int], pd.Series]:
    def f(close: pd.DataFrame, t: int) -> pd.Series:
        if t - window < 1:
            return pd.Series(dtype=float)
        r = close.iloc[t - window:t + 1].pct_change()
        return -r.std()          # negative so that the top group is LOW volatility
    return f


def vol_managed(spy: pd.DataFrame, split: str, target: float = 0.15, window: int = 21, max_lev: float = 1.5,
                cost: float = 0.0005) -> pd.DataFrame:
    daily = spy["Close"].pct_change().dropna()
    rv = daily.rolling(window).std() * np.sqrt(252)
    w = (target / rv).clip(upper=max_lev).shift(1).fillna(0)
    strat = w * daily - w.diff().abs().fillna(0) * cost
    rows = []
    for pname, mask in _periods(daily.index, split).items():
        a = perf_stats(daily[mask], 252)
        b = perf_stats(strat[mask], 252)
        rows.append({"period": pname, "bh_ann": a["ann_return"], "bh_sharpe": a["sharpe"], "bh_dd": a["max_drawdown"],
                     "vm_ann": b["ann_return"], "vm_sharpe": b["sharpe"], "vm_dd": b["max_drawdown"],
                     "avg_exposure": float(w[mask].mean())})
    return pd.DataFrame(rows).set_index("period")


# ----------------------------------------------------------------------------
# 5. sector-residual reversal
# ----------------------------------------------------------------------------
def residual_signal(sectors: Dict[str, str], lookback: int) -> Callable[[pd.DataFrame, int], pd.Series]:
    """Stock return over ``lookback`` days minus its sector's average return."""
    sec = pd.Series(sectors)

    def f(close: pd.DataFrame, t: int) -> pd.Series:
        if t - lookback < 0:
            return pd.Series(dtype=float)
        r = (close.iloc[t] / close.iloc[t - lookback] - 1.0).dropna()
        s = sec.reindex(r.index)
        r = r[s.notna()]
        s = s[r.index]
        return r - r.groupby(s).transform("mean")
    return f


# ----------------------------------------------------------------------------
# live scan for the one effect that passed: big news day in a beaten-down stock
# ----------------------------------------------------------------------------
def newsday_signals(get_frame: Callable[[str], pd.DataFrame], symbols: Sequence[str], gap_min: float = 0.04,
                    vol_mult: float = 3.0, max_age: int = 5, require_deep: bool = True, deep_ret: float = -0.08,
                    hold: int = 60) -> pd.DataFrame:
    """Stocks below their 200-day MA (and, by default, down > 8% over six months) that printed a
    >= ``gap_min`` gap on >= ``vol_mult`` x average volume within the last ``max_age`` bars."""
    rows = []
    for s in symbols:
        try:
            df = get_frame(s)
        except Exception:  # noqa: BLE001
            continue
        if len(df) < 260:
            continue
        c, o, v = (df[x].to_numpy(dtype=float) for x in ("Close", "Open", "Volume"))
        n = len(c)
        avgv = pd.Series(v).rolling(20).mean().shift(1).to_numpy()
        for t in range(n - max_age, n):
            gap = o[t] / c[t - 1] - 1.0
            if not (abs(gap) >= gap_min and np.isfinite(avgv[t]) and v[t] >= vol_mult * avgv[t]):
                continue
            ma200 = c[t - 199:t + 1].mean()
            r126 = c[t] / c[t - 126] - 1.0
            if not c[t] < ma200 or (require_deep and not r126 < deep_ret):
                continue
            rows.append({"symbol": s, "news_date": df.index[t].strftime("%Y-%m-%d"), "bars_ago": n - 1 - t,
                         "gap": gap, "day_return": c[t] / c[t - 1] - 1.0, "volume_ratio": v[t] / avgv[t],
                         "ret_6m": r126, "dist_ma200": c[t] / ma200 - 1.0, "close_on_news_day": c[t],
                         "last_close": c[-1], "since_news": c[-1] / c[t] - 1.0, "bars_left": hold - (n - 1 - t)})
            break
    cols = ["symbol", "news_date", "bars_ago", "gap", "day_return", "volume_ratio", "ret_6m", "dist_ma200",
            "close_on_news_day", "last_close", "since_news", "bars_left"]
    return pd.DataFrame(rows, columns=cols).sort_values(["bars_ago", "ret_6m"]).reset_index(drop=True)
