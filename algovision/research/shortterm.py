"""Short-horizon exit study: hold a few bars, take a few percent, repeat.

For every event the next ``max_hold`` bars of OHLC are collected once; each
strategy (hold, take-profit, stop) is then evaluated vectorised over all
events, and over random nearby entries in the same stock and direction with
the *same* exit rules, so the comparison isolates what the pattern adds.
Fills: a take-profit fills at the target, or at the open if the bar gaps
through it (better); a stop fills at the stop, or at the open if the bar gaps
through it (worse); if both are touched in one bar the stop wins.  Entry is
the open of the bar after the signal; a round-trip cost is subtracted.
"""

from __future__ import annotations

import zlib
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.research.stats import bootstrap_mean_ci, wilson

HOLDS = (1, 2, 3, 5)
TARGETS = (0.01, 0.02, 0.03, None)
STOPS = (None, 0.02, 0.03)
COSTS = (0.0, 0.0005, 0.001)      # round trip: none, 5 bps, 10 bps
LOCAL_WINDOW = 126


@dataclass
class Paths:
    """Relative OHLC paths after entry, already signed by direction (long frame)."""
    op: np.ndarray    # (N, H) open / entry - 1, signed
    hi: np.ndarray    # best excursion within bar (signed)
    lo: np.ndarray    # worst excursion within bar (signed)
    cl: np.ndarray    # close / entry - 1, signed
    valid: np.ndarray  # (N,) all H bars available


def _paths(open_, high, low, close, entries: np.ndarray, dirs: np.ndarray, hmax: int) -> Paths:
    n = len(close)
    N = len(entries)
    op = np.full((N, hmax), np.nan)
    hi = np.full((N, hmax), np.nan)
    lo = np.full((N, hmax), np.nan)
    cl = np.full((N, hmax), np.nan)
    valid = (entries + hmax - 1) < n
    for k in range(hmax):
        idx = entries + k
        ok = idx < n
        e = open_[entries[ok]]
        d = dirs[ok]
        op[ok, k] = d * (open_[idx[ok]] / e - 1.0)
        h = high[idx[ok]] / e - 1.0
        l = low[idx[ok]] / e - 1.0
        hi[ok, k] = np.where(d > 0, h, -l)
        lo[ok, k] = np.where(d > 0, l, -h)
        cl[ok, k] = d * (close[idx[ok]] / e - 1.0)
    return Paths(op, hi, lo, cl, valid)


def evaluate(paths: Paths, hold: int, target: Optional[float], stop: Optional[float]) -> Tuple[np.ndarray, np.ndarray]:
    """Return (gross return per trade, bars held) under the given exit rules."""
    N = paths.op.shape[0]
    ret = np.full(N, np.nan)
    bars = np.full(N, hold, dtype=int)
    done = np.zeros(N, dtype=bool)
    for k in range(hold):
        op, hi, lo = paths.op[:, k], paths.hi[:, k], paths.lo[:, k]
        live = ~done & np.isfinite(op)
        hit_stop = live & (stop is not None) & (lo <= -(stop or 0))
        hit_tgt = live & (target is not None) & (hi >= (target or np.inf))
        # stop first (conservative), gap-through fills at the open
        s_idx = hit_stop
        ret[s_idx] = np.where(op[s_idx] <= -(stop or 0), op[s_idx], -(stop or 0))
        bars[s_idx] = k + 1
        done |= s_idx
        t_idx = hit_tgt & ~s_idx
        ret[t_idx] = np.where(op[t_idx] >= (target or 0), op[t_idx], (target or 0))
        bars[t_idx] = k + 1
        done |= t_idx
    rest = ~done & np.isfinite(paths.cl[:, hold - 1])
    ret[rest] = paths.cl[rest, hold - 1]
    return ret, bars


def build_paths(events: pd.DataFrame, get_frame: Callable[[str], pd.DataFrame], hmax: int = max(HOLDS),
                random_draws: int = 10, window: int = LOCAL_WINDOW, seed: int = 7) -> Tuple[Paths, Paths, np.ndarray]:
    """Paths for the events and for ``random_draws`` local random entries per event."""
    ev = events.reset_index(drop=True)
    N = len(ev)
    parts_e: List[Paths] = []
    parts_r: List[Paths] = []
    order = np.zeros(N, dtype=int)
    pos = 0
    for symbol, idx in ev.groupby("symbol", sort=False).groups.items():
        idx = np.asarray(list(idx))
        df = get_frame(symbol)
        o, h, l, c = (df[x].to_numpy(dtype=float) for x in ("Open", "High", "Low", "Close"))
        n = len(c)
        entries = ev.loc[idx, "entry_idx"].to_numpy(dtype=int)
        dirs = ev.loc[idx, "dir"].to_numpy(dtype=int)
        parts_e.append(_paths(o, h, l, c, entries, dirs, hmax))
        rng = np.random.default_rng(seed + (zlib.crc32(symbol.encode()) % 100000))
        r_entries = np.empty(len(idx) * random_draws, dtype=int)
        r_dirs = np.repeat(dirs, random_draws)
        for j, e in enumerate(entries):
            lo_, hi_ = max(1, e - window), min(n - hmax, e + window)
            cand = np.arange(lo_, hi_ + 1)
            cand = cand[(cand < e - hmax) | (cand > e + hmax)]
            if len(cand) == 0:
                cand = np.array([e])
            r_entries[j * random_draws:(j + 1) * random_draws] = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
        parts_r.append(_paths(o, h, l, c, r_entries, r_dirs, hmax))
        order[pos:pos + len(idx)] = idx
        pos += len(idx)
    cat = lambda att, parts: np.concatenate([getattr(p, att) for p in parts])  # noqa: E731
    pe = Paths(*(cat(a, parts_e) for a in ("op", "hi", "lo", "cl", "valid")))
    pr = Paths(*(cat(a, parts_r) for a in ("op", "hi", "lo", "cl", "valid")))
    return pe, pr, order


def strategy_grid(ev: pd.DataFrame, pe: Paths, pr: Paths, order: np.ndarray, holds=HOLDS, targets=TARGETS,
                  stops=STOPS, cost: float = 0.0005, random_draws: int = 10, group: Optional[str] = None,
                  min_n: int = 30) -> pd.DataFrame:
    """One row per (hold, target, stop[, group]) with net expectancy and excess over random."""
    ev = ev.reset_index(drop=True).loc[order].reset_index(drop=True)
    rows = []
    groups = [(None, np.ones(len(ev), dtype=bool))] if group is None else \
        [(g, (ev[group] == g).to_numpy()) for g in sorted(ev[group].dropna().unique())]
    for hold in holds:
        for target in targets:
            for stop in stops:
                r_e, b_e = evaluate(pe, hold, target, stop)
                r_r, _ = evaluate(pr, hold, target, stop)
                r_r = r_r.reshape(len(ev), random_draws)
                for gname, mask in groups:
                    m = mask & np.isfinite(r_e) & np.isfinite(r_r).all(axis=1)
                    if m.sum() < min_n:
                        continue
                    net = r_e[m] - cost
                    rnet = r_r[m] - cost
                    excess = net - rnet.mean(axis=1)
                    lo_ci, hi_ci = bootstrap_mean_ci(excess, reps=500)
                    # permutation: one random draw per event
                    rng = np.random.default_rng(0)
                    picks = rng.integers(0, random_draws, size=(500, m.sum()))
                    null = rnet[np.arange(m.sum())[None, :], picks].mean(axis=1)
                    p = float((null >= net.mean()).mean())
                    wins, losses = net[net > 0].sum(), -net[net < 0].sum()
                    rows.append({
                        "group": gname, "hold": hold, "target": target, "stop": stop, "n": int(m.sum()),
                        "net_ret": float(net.mean()), "hit": float((net > 0).mean()),
                        "hit_lo": wilson(int((net > 0).sum()), int(m.sum()))[0],
                        "rand_net": float(rnet.mean()), "rand_hit": float((rnet > 0).mean()),
                        "excess": float(excess.mean()), "excess_lo": lo_ci, "excess_hi": hi_ci, "p": p,
                        "profit_factor": float(wins / losses) if losses > 0 else np.inf,
                        "target_rate": float((r_e[m] >= (target or np.inf) - 1e-12).mean()) if target else np.nan,
                        "stop_rate": float((r_e[m] <= -(stop or np.inf) + 1e-12).mean()) if stop else np.nan,
                        "avg_bars": float(b_e[m].mean()),
                    })
    return pd.DataFrame(rows)


def cost_sensitivity(ev: pd.DataFrame, pe: Paths, pr: Paths, order: np.ndarray, hold: int, target: Optional[float],
                     stop: Optional[float], costs=COSTS, random_draws: int = 10) -> pd.DataFrame:
    rows = []
    for c in costs:
        g = strategy_grid(ev, pe, pr, order, holds=(hold,), targets=(target,), stops=(stop,), cost=c,
                          random_draws=random_draws)
        if len(g):
            r = g.iloc[0]
            rows.append({"cost_bps": c * 1e4, "net_ret": r["net_ret"], "hit": r["hit"], "excess": r["excess"],
                         "profit_factor": r["profit_factor"]})
    return pd.DataFrame(rows).set_index("cost_bps")


def _pct(v) -> str:
    return "" if v is None or (isinstance(v, float) and not np.isfinite(v)) else f"{v * 100:+.2f}%"


def grid_markdown(g: pd.DataFrame, title: str) -> str:
    d = g.copy()
    d["target"] = d["target"].map(lambda v: "none" if pd.isna(v) else f"{v * 100:.0f}%")
    d["stop"] = d["stop"].map(lambda v: "none" if pd.isna(v) else f"{v * 100:.0f}%")
    for c in ("net_ret", "rand_net", "excess", "excess_lo", "excess_hi"):
        d[c] = d[c].map(_pct)
    for c in ("hit", "rand_hit", "target_rate", "stop_rate"):
        d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v * 100:.1f}%")
    d["p"] = d["p"].map(lambda v: f"{v:.3f}")
    d["profit_factor"] = d["profit_factor"].map(lambda v: f"{v:.2f}")
    d["avg_bars"] = d["avg_bars"].map(lambda v: f"{v:.1f}")
    cols = [c for c in ("group", "hold", "target", "stop", "n", "net_ret", "hit", "rand_net", "rand_hit", "excess",
                        "excess_lo", "excess_hi", "p", "profit_factor", "target_rate", "stop_rate", "avg_bars") if c in d.columns]
    if "group" in cols and d["group"].isna().all():
        cols.remove("group")
    return f"### {title}\n\n" + d[cols].to_markdown(index=False) + "\n"


def write_shortterm_report(out_dir, events: pd.DataFrame, wf: Optional[pd.DataFrame], get_frame,
                           cost: float = 0.0005) -> "Path":
    from pathlib import Path
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md = ["# Short-horizon exit study\n",
          "Hold a few bars after the signal, take a few percent when offered. Entry at the next open; a round-trip "
          f"cost of {cost * 1e4:.0f} bps is subtracted from every trade; random = the same exit rules applied to random "
          "dates within +-6 months in the same stock and direction (10 draws per event).\n"]
    for name, ev in (("Hindsight events", events), ("Walk-forward events", wf)):
        if ev is None or not len(ev):
            continue
        pe, pr, order = build_paths(ev, get_frame)
        g = strategy_grid(ev, pe, pr, order, cost=cost)
        g.to_csv(out_dir / f"shortterm_{name.split()[0].lower()}_grid.csv", index=False)
        md.append(grid_markdown(g, f"{name}: strategy grid (all patterns)"))
        gp = strategy_grid(ev, pe, pr, order, holds=(2,), targets=(0.02,), stops=(None,), cost=cost, group="pattern")
        md.append(grid_markdown(gp, f"{name}: hold 2 bars, take 2%, per pattern"))
        cs = cost_sensitivity(ev, pe, pr, order, 2, 0.02, None)
        md.append(f"### {name}: cost sensitivity (hold 2, take 2%)\n\n" + cs.to_markdown() + "\n")
    path = out_dir / "shortterm.md"
    path.write_text("\n".join(md), encoding="utf-8")
    return path
