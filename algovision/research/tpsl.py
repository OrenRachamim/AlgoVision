"""Take-profit / stop-loss exit rules on (near-)random entries.

Answers "enter any day above the 200-day MA, exit at +X% or -Y%": per-trade
hit rate, holding time, expectancy, return per day of capital, and a
capital-constrained portfolio simulation (N slots) so that the compounding
claim can be checked against what the capital actually earns.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.research.factors import perf_stats


def simulate_rule(panel: Dict[str, pd.DataFrame], tp: float, sl: Optional[float], max_hold: int = 250,
                  filter_fn=None, entry_stride: int = 1, cost: float = 0.0005, start_bar: int = 200) -> pd.DataFrame:
    """One row per trade: every ``entry_stride``-th eligible day of every stock is an entry.

    Entry at the next open after the signal day.  Take-profit fills at the target
    (or at the open when the bar gaps through it); stop fills at the stop (or the
    open when it gaps through); stop wins ties; time exit at the close after
    ``max_hold`` bars.  ``filter_fn(close_array, t) -> bool`` decides eligibility.
    """
    close, open_, high, low = (panel[k] for k in ("Close", "Open", "High", "Low"))
    rows: List[Dict] = []
    for s in close.columns:
        c, o, h, l = (x[s].to_numpy(dtype=float) for x in (close, open_, high, low))
        n = len(c)
        ok = np.isfinite(c) & np.isfinite(o)
        ma200 = pd.Series(c).rolling(200).mean().to_numpy()
        tr_ = np.maximum(h - l, np.maximum(np.abs(h - np.roll(c, 1)), np.abs(l - np.roll(c, 1))))
        atr = pd.Series(tr_).rolling(14).mean().to_numpy()
        for t in range(start_bar, n - 2, entry_stride):
            if not ok[t] or not ok[t + 1]:
                continue
            if filter_fn is not None and not filter_fn(c, ma200, t):
                continue
            e = t + 1
            px = o[e]
            tgt = px * (1 + tp)
            stp = px * (1 - sl) if sl is not None else -np.inf
            last = min(n - 1, e + max_hold - 1)
            hh, ll, oo = h[e:last + 1], l[e:last + 1], o[e:last + 1]
            hit_t = np.where(hh >= tgt)[0]
            hit_s = np.where(ll <= stp)[0] if sl is not None else np.array([], dtype=int)
            kt = hit_t[0] if len(hit_t) else np.inf
            ks = hit_s[0] if len(hit_s) else np.inf
            if ks <= kt and np.isfinite(ks):
                k = int(ks)
                exit_px = min(oo[k], stp) if k > 0 else stp
                reason = "stop"
            elif np.isfinite(kt):
                k = int(kt)
                exit_px = max(oo[k], tgt) if k > 0 else tgt
                reason = "target"
            else:
                k = last - e
                exit_px = c[last]
                reason = "time" if last == e + max_hold - 1 else "end"
            days = k + 1
            ret = exit_px / px - 1.0 - cost
            rows.append({"symbol": s, "date": close.index[t], "entry": px, "exit": exit_px, "days": days,
                         "reason": reason, "ret": ret, "bh_ret": c[e + k] / px - 1.0,
                         "above_ma200": bool(c[t] > ma200[t]) if np.isfinite(ma200[t]) else None,
                         "ret_126": c[t] / c[t - 126] - 1.0 if t >= 126 and np.isfinite(c[t - 126]) else np.nan,
                         "atr_pct": atr[t] / c[t] if np.isfinite(atr[t]) else np.nan})
    return pd.DataFrame(rows)


def trade_stats(tr: pd.DataFrame) -> Dict:
    if not len(tr):
        return {"n": 0}
    r, d = tr["ret"].to_numpy(dtype=float), tr["days"].to_numpy(dtype=float)
    per_day = r.sum() / d.sum()
    return {"n": int(len(tr)), "hit": float((r > 0).mean()), "target_rate": float((tr["reason"] == "target").mean()),
            "stop_rate": float((tr["reason"] == "stop").mean()), "unresolved": float(tr["reason"].isin(["time", "end"]).mean()),
            "mean_ret": float(r.mean()), "median_ret": float(np.median(r)), "mean_days": float(d.mean()),
            "median_days": float(np.median(d)), "p90_days": float(np.percentile(d, 90)),
            "ret_per_day_bp": float(per_day * 1e4), "ann_return_of_capital": float((1 + per_day) ** 252 - 1),
            "profit_factor": float(r[r > 0].sum() / -r[r < 0].sum()) if (r < 0).any() else np.inf,
            "avg_win": float(r[r > 0].mean()) if (r > 0).any() else np.nan, "avg_loss": float(r[r < 0].mean()) if (r < 0).any() else np.nan,
            "bh_same_days_per_day_bp": float(tr["bh_ret"].sum() / d.sum() * 1e4)}


def slot_portfolio(panel: Dict[str, pd.DataFrame], tp: float, sl: Optional[float], slots: int = 20, max_hold: int = 250,
                   filter_fn=None, cost: float = 0.0005, seed: int = 0, start_bar: int = 200) -> pd.Series:
    """Capital in ``slots`` equal parts; each day every free slot buys a random eligible stock at the open.

    A slot stays occupied until its take-profit / stop / time exit; the daily
    portfolio return is the average of the slots' daily returns (cash earns 0).
    """
    close, open_, high, low = (panel[k].to_numpy(dtype=float) for k in ("Close", "Open", "High", "Low"))
    idx = panel["Close"].index
    n, m = close.shape
    ma200 = pd.DataFrame(close).rolling(200).mean().to_numpy()
    rng = np.random.default_rng(seed)
    # slot state
    sym = np.full(slots, -1)
    entry = np.zeros(slots)
    prev = np.zeros(slots)
    opened = np.zeros(slots, dtype=int)
    daily = np.zeros(n)
    for t in range(start_bar + 1, n):
        rets = np.zeros(slots)
        # 1. open free slots at today's open using yesterday's information
        free = np.where(sym < 0)[0]
        if len(free):
            elig = np.where(np.isfinite(close[t - 1]) & np.isfinite(open_[t]) &
                            (np.ones(m, bool) if filter_fn is None else filter_fn(close, ma200, t - 1)))[0]
            elig = elig[~np.isin(elig, sym)]
            if len(elig):
                pick = rng.choice(elig, size=min(len(free), len(elig)), replace=False)
                for k, j in zip(free, pick):
                    sym[k] = j
                    entry[k] = open_[t, j]
                    prev[k] = open_[t, j]
                    opened[k] = t
                    rets[k] -= cost
        # 2. mark / exit occupied slots
        for k in range(slots):
            j = sym[k]
            if j < 0:
                continue
            px = entry[k]
            tgt, stp = px * (1 + tp), (px * (1 - sl) if sl is not None else -np.inf)
            hi, lo, op, cl = high[t, j], low[t, j], open_[t, j], close[t, j]
            if not np.isfinite(cl):
                sym[k] = -1
                continue
            fill = None
            if lo <= stp:
                fill = min(op, stp) if t > opened[k] else stp
            elif hi >= tgt:
                fill = max(op, tgt) if t > opened[k] else tgt
            elif t - opened[k] + 1 >= max_hold:
                fill = cl
            if fill is not None:
                rets[k] += fill / prev[k] - 1.0
                sym[k] = -1
            else:
                rets[k] += cl / prev[k] - 1.0
                prev[k] = cl
        daily[t] = rets.mean()
    return pd.Series(daily[start_bar + 1:], index=idx[start_bar + 1:])


ABOVE_MA200 = lambda c, ma, t: bool(np.isfinite(ma[t]) and c[t] > ma[t])   # noqa: E731
BELOW_MA200 = lambda c, ma, t: bool(np.isfinite(ma[t]) and c[t] < ma[t])   # noqa: E731


def above_ma200_vec(close: np.ndarray, ma: np.ndarray, t: int) -> np.ndarray:
    return np.isfinite(ma[t]) & (close[t] > ma[t])
