"""Statistics over the event table."""

from __future__ import annotations

from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats as sps

from algovision.research.events import HORIZONS, RANDOM_DRAWS


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (centre - half, centre + half)


def bootstrap_mean_ci(x: np.ndarray, reps: int = 2000, seed: int = 0):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 2:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(reps, len(x)))
    means = x[idx].mean(axis=1)
    return (float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5)))


def permutation_pvalue(actual: np.ndarray, rand_matrix: np.ndarray, reps: int = 2000, seed: int = 0) -> Dict:
    """Is the mean pattern return higher than random-date entries in the same stocks?

    ``rand_matrix`` is (n_events, K): K random-entry returns per event.  Each
    replicate picks one random draw per event and averages, giving the
    distribution of the mean under "no timing skill".
    """
    ok = np.isfinite(actual) & np.isfinite(rand_matrix).all(axis=1)
    actual, rand_matrix = actual[ok], rand_matrix[ok]
    n, k = rand_matrix.shape
    if n < 5:
        return {"p_one_sided": np.nan, "p_two_sided": np.nan, "z": np.nan, "rand_mean": np.nan}
    rng = np.random.default_rng(seed)
    picks = rng.integers(0, k, size=(reps, n))
    null_means = rand_matrix[np.arange(n)[None, :], picks].mean(axis=1)
    obs = float(actual.mean())
    p1 = float((null_means >= obs).mean())
    mu, sd = null_means.mean(), null_means.std(ddof=1)
    z = (obs - mu) / sd if sd > 0 else np.nan
    p2 = float((np.abs(null_means - mu) >= abs(obs - mu)).mean())
    return {"p_one_sided": p1, "p_two_sided": p2, "z": float(z), "rand_mean": float(mu)}


def _rand_matrix(g: pd.DataFrame, h: int, prefix: str = "rand") -> np.ndarray:
    cols = [f"{prefix}_{h}_{k}" for k in range(RANDOM_DRAWS) if f"{prefix}_{h}_{k}" in g.columns]
    return g[cols].to_numpy(dtype=float)


def summarize_group(g: pd.DataFrame, horizons: Sequence[int] = HORIZONS, key_h: int = 20) -> Dict:
    out: Dict = {"n": int(len(g)), "n_symbols": int(g["symbol"].nunique())}
    for h in horizons:
        r = g[f"ret_{h}"].to_numpy(dtype=float)
        ok = np.isfinite(r)
        out[f"n_{h}"] = int(ok.sum())
        if ok.sum() == 0:
            continue
        out[f"ret_{h}"] = float(np.nanmean(r))
        out[f"med_{h}"] = float(np.nanmedian(r))
        out[f"hit_{h}"] = float((r[ok] > 0).mean())
        out[f"hit_lo_{h}"], out[f"hit_hi_{h}"] = wilson(int((r[ok] > 0).sum()), int(ok.sum()))
        xs = g[f"xspy_{h}"].to_numpy(dtype=float)
        out[f"xspy_{h}"] = float(np.nanmean(xs)) if np.isfinite(xs).any() else np.nan
        xr = g[f"xrand_{h}"].to_numpy(dtype=float)
        out[f"xrand_{h}"] = float(np.nanmean(xr))
        out[f"xrand_lo_{h}"], out[f"xrand_hi_{h}"] = bootstrap_mean_ci(xr)
        rm = _rand_matrix(g, h)
        out[f"rand_hit_{h}"] = float(np.nanmean(rm > 0)) if rm.size else np.nan
        pv = permutation_pvalue(r, rm)
        out[f"p_{h}"] = pv["p_one_sided"]
        out[f"z_{h}"] = pv["z"]
        if ok.sum() > 2:
            t = sps.ttest_1samp(xr[np.isfinite(xr)], 0.0)
            out[f"t_{h}"] = float(t.statistic)
        if f"xloc_{h}" in g.columns and np.isfinite(g[f"xloc_{h}"]).any():
            xl = g[f"xloc_{h}"].to_numpy(dtype=float)
            out[f"xloc_{h}"] = float(np.nanmean(xl))
            out[f"xloc_lo_{h}"], out[f"xloc_hi_{h}"] = bootstrap_mean_ci(xl)
            lm = _rand_matrix(g, h, "loc")
            out[f"loc_hit_{h}"] = float(np.nanmean(lm > 0)) if lm.size else np.nan
            out[f"ploc_{h}"] = permutation_pvalue(r, lm)["p_one_sided"] if lm.size else np.nan
    # trade simulation
    out["target_rate"] = float((g["exit_reason"] == "target").mean())
    out["stop_rate"] = float((g["exit_reason"] == "stop").mean())
    out["time_rate"] = float((g["exit_reason"] == "time").mean())
    rr = g["r_multiple"].to_numpy(dtype=float)
    rr = rr[np.isfinite(rr)]
    if len(rr):
        out["n_r"] = int(len(rr))
        out["avg_r"] = float(rr.mean())
        out["win_rate_r"] = float((rr > 0).mean())
        pos, neg = rr[rr > 0].sum(), -rr[rr < 0].sum()
        out["profit_factor"] = float(pos / neg) if neg > 0 else np.inf
        out["avg_reward_risk"] = float(np.nanmean(g["reward_risk"]))
        out["avg_bars_held"] = float(g["bars_held"].mean())
    out["avg_trade_ret"] = float(g["trade_ret"].mean())
    out["avg_score"] = float(g["score"].mean())
    out["avg_delay"] = float(g["delay_bars"].mean())
    return out


def summary_table(events: pd.DataFrame, by: str = "pattern", horizons: Sequence[int] = HORIZONS,
                  min_n: int = 1) -> pd.DataFrame:
    rows = []
    for key, g in events.groupby(by):
        if len(g) < min_n:
            continue
        d = summarize_group(g, horizons)
        d[by] = key
        rows.append(d)
    d = summarize_group(events, horizons)
    d[by] = "ALL"
    rows.append(d)
    t = pd.DataFrame(rows).set_index(by)
    return t


def calibration(events: pd.DataFrame, h: int = 20, bins: int = 5) -> pd.DataFrame:
    """Does a higher score mean a better outcome?"""
    g = events[np.isfinite(events[f"ret_{h}"])].copy()
    if len(g) < bins * 5:
        return pd.DataFrame()
    g["score_bin"] = pd.qcut(g["score"], bins, duplicates="drop")
    agg = dict(
        n=("score", "size"), score_min=("score", "min"), score_max=("score", "max"),
        ret=(f"ret_{h}", "mean"), xrand=(f"xrand_{h}", "mean"), hit=(f"ret_{h}", lambda x: float((x > 0).mean())),
        target_rate=("exit_reason", lambda x: float((x == "target").mean())),
        avg_r=("r_multiple", "mean"))
    xcol = f"xloc_{h}" if f"xloc_{h}" in g.columns else f"xrand_{h}"
    if xcol != f"xrand_{h}":
        agg["xloc"] = (xcol, "mean")
    t = g.groupby("score_bin", observed=True).agg(**agg)
    rho, p = sps.spearmanr(g["score"], g[xcol], nan_policy="omit")
    t.attrs["spearman_rho"], t.attrs["spearman_p"] = float(rho), float(p)
    return t


def breakdown(events: pd.DataFrame, col: str, h: int = 20) -> pd.DataFrame:
    g = events[np.isfinite(events[f"ret_{h}"])]
    agg = dict(
        n=("score", "size"), ret=(f"ret_{h}", "mean"), xspy=(f"xspy_{h}", "mean"), xrand=(f"xrand_{h}", "mean"),
        hit=(f"ret_{h}", lambda x: float((x > 0).mean())),
        target_rate=("exit_reason", lambda x: float((x == "target").mean())),
        stop_rate=("exit_reason", lambda x: float((x == "stop").mean())), avg_r=("r_multiple", "mean"))
    if f"xloc_{h}" in g.columns:
        agg["xloc"] = (f"xloc_{h}", "mean")
    t = g.groupby(col, observed=True).agg(**agg)
    return t


def volume_buckets(events: pd.DataFrame) -> pd.Series:
    v = events["breakout_vol_ratio"]
    return pd.cut(v, [0, 0.8, 1.1, 1.5, 2.5, np.inf], labels=["<0.8x", "0.8-1.1x", "1.1-1.5x", "1.5-2.5x", ">2.5x"])


def structure_table(structures: pd.DataFrame) -> pd.DataFrame:
    """Given a completed structure, how often does it confirm / fail / expire?"""
    s = structures.copy()
    t = s.groupby("pattern")["status"].value_counts().unstack(fill_value=0)
    for c in ("confirmed", "failed", "expired", "forming"):
        if c not in t.columns:
            t[c] = 0
    t["n"] = t[["confirmed", "failed", "expired"]].sum(axis=1)
    t["confirm_rate"] = t["confirmed"] / t["n"]
    t["fail_rate"] = t["failed"] / t["n"]
    t["expire_rate"] = t["expired"] / t["n"]
    tot = t[["confirmed", "failed", "expired", "forming"]].sum()
    tot["n"] = tot[["confirmed", "failed", "expired"]].sum()
    tot["confirm_rate"] = tot["confirmed"] / tot["n"]
    tot["fail_rate"] = tot["failed"] / tot["n"]
    tot["expire_rate"] = tot["expired"] / tot["n"]
    t.loc["ALL"] = tot
    return t[["n", "confirmed", "failed", "expired", "confirm_rate", "fail_rate", "expire_rate"]]


def compare_walkforward(hind: pd.DataFrame, wf: pd.DataFrame, h: int = 20, tol_bars: int = 3) -> Dict:
    """Overlap and outcome comparison between hindsight and point-in-time events."""
    def keyset(df):
        return {(r.symbol, r.pattern, int(r.signal_idx)) for r in df.itertuples()}

    hk, wk = keyset(hind), keyset(wf)
    matched = 0
    wf_index = {}
    for s, p, i in wk:
        wf_index.setdefault((s, p), []).append(i)
    for s, p, i in hk:
        if any(abs(i - j) <= tol_bars for j in wf_index.get((s, p), [])):
            matched += 1
    out = {
        "hindsight_events": len(hk), "walkforward_events": len(wk), "hindsight_matched_in_wf": matched,
        "match_rate": matched / len(hk) if hk else np.nan,
    }
    for name, df in (("hindsight", hind), ("walkforward", wf)):
        r = df[f"ret_{h}"].to_numpy(dtype=float)
        r = r[np.isfinite(r)]
        out[f"{name}_ret_{h}"] = float(r.mean()) if len(r) else np.nan
        out[f"{name}_hit_{h}"] = float((r > 0).mean()) if len(r) else np.nan
        out[f"{name}_xrand_{h}"] = float(np.nanmean(df[f"xrand_{h}"])) if len(df) else np.nan
        out[f"{name}_xloc_{h}"] = float(np.nanmean(df[f"xloc_{h}"])) if len(df) and f"xloc_{h}" in df.columns else np.nan
        out[f"{name}_target_rate"] = float((df["exit_reason"] == "target").mean()) if len(df) else np.nan
        out[f"{name}_avg_r"] = float(np.nanmean(df["r_multiple"])) if len(df) else np.nan
    return out


def conditional_table(events: pd.DataFrame, h: int = 20, min_n: int = 100) -> pd.DataFrame:
    """Per-pattern excess return under a few trading-relevant conditions."""
    g = events[np.isfinite(events[f"ret_{h}"])].copy()
    xcol = f"xloc_{h}" if f"xloc_{h}" in g.columns else f"xrand_{h}"
    g["vol_hi"] = g["breakout_vol_ratio"] >= 1.5
    g["delayed"] = g["delay_bars"] > 0
    g["extended"] = g["gap_from_level"] > 0.03
    rows = []
    for pat, gg in g.groupby("pattern"):
        row = {"pattern": pat, "n": len(gg), "xrand_all": gg[xcol].mean()}
        for name, mask in (("vol>=1.5x", gg["vol_hi"]), ("vol<1.5x", ~gg["vol_hi"]),
                           ("same-bar", ~gg["delayed"]), ("delayed", gg["delayed"]),
                           ("extended>3%", gg["extended"]), ("near level", ~gg["extended"])):
            sub = gg[mask]
            row[f"n {name}"] = len(sub)
            row[f"xrand {name}"] = sub[xcol].mean() if len(sub) >= min_n else np.nan
        # stability: share of years with positive excess
        yr = gg.groupby("year")[xcol].agg(["mean", "size"])
        yr = yr[yr["size"] >= 30]
        row["years"] = int(len(yr))
        row["years_positive"] = int((yr["mean"] > 0).sum())
        rows.append(row)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).set_index("pattern")


def score_threshold_table(events: pd.DataFrame, h: int = 20, thresholds=(0.6, 0.7, 0.8, 0.9)) -> pd.DataFrame:
    """Does raising the scanner's min_score improve outcomes?"""
    rows = []
    for th in thresholds:
        g = events[(events["score"] >= th) & np.isfinite(events[f"ret_{h}"])]
        if len(g) < 30:
            continue
        r = g[f"ret_{h}"].to_numpy(dtype=float)
        rows.append({"min_score": th, "n": len(g), "hit": float((r > 0).mean()), "ret": float(r.mean()),
                     "xrand": float(g[f"xrand_{h}"].mean()),
                     "xloc": float(g[f"xloc_{h}"].mean()) if f"xloc_{h}" in g.columns else np.nan,
                     "target_rate": float((g["exit_reason"] == "target").mean()),
                     "avg_r": float(np.nanmean(g["r_multiple"]))})
    if not rows:
        return pd.DataFrame(columns=["n", "hit", "ret", "xrand", "xloc", "target_rate", "avg_r"])
    return pd.DataFrame(rows).set_index("min_score")
