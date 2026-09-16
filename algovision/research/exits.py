"""Exit-rule study: does an adaptive exit beat a plain time exit on the entries the journal forward-tests?

Entries (the three tested setups, all long, all in beaten-down stocks: below the 200-day MA and down > 8 % over
six months): a confirmed Falling Wedge breakout, a news-day gap (>= 4 % on >= 3x volume) and a single insider
purchase >= $100k (officers / directors).  For each entry the same pre-registered list of exit rules is applied
to the signal trades and to random entries in the same stock within +-6 months (10 per event) under the *same*
exit rule, so "excess" isolates what the signal adds under that exit rather than what the exit does to any
price series (a take-profit rule raises the hit rate and the return per bar of random entries too).

Two yardsticks are reported side by side:

* return per trade      what one signal earns, net of a round-trip cost;
* return per bar of capital (bp)   what the money earns while it is tied up, i.e. the "2 % in one day is
  better than 2 % in five" view.

Exit families (thresholds fixed before looking at the data):

* time N                    exit at the close of bar N (baseline; 20 is the journal's wedge hold, 60 news-day)
* take X % / time N         exit at the first bar whose high reaches +X % (fill at the open if it gaps through)
* rising target a + b.k     the target grows with time: +a on bar 1, +a+b on bar 2, ... (the "2 % today, 6 %
                            in a week" idea); exit when the high reaches it, else time N
* per-day r %               exit at the close of bar k when the return so far is >= r % x k (return per day of
                            capital at least r %), else time N
* hybrid a / b              +a on the first bar, then +b for the rest of the hold (the rule as proposed:
                            2 % on day one, otherwise wait for 6 %), else time N
* trail x %                 exit at the close of the first bar that closes x % below the highest close since
                            entry, else time N (an adaptive stop that lets winners run)

Entry is the open of the bar after the signal; costs are subtracted per round trip; train = signals before the
split date, test = after.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from algovision.research.shortterm import Paths, build_paths
from algovision.research.stats import bootstrap_mean_ci

HMAX = 60
RANDOM_DRAWS = 10


@dataclass(frozen=True)
class Rule:
    name: str
    kind: str          # time | target | rising | perday | hybrid | trail
    hold: int
    a: float = 0.0
    b: float = 0.0


RULES: List[Rule] = [
    *[Rule(f"time {h}", "time", h) for h in (5, 10, 20, 40, 60)],
    *[Rule(f"take {int(x * 100)}% / time 20", "target", 20, x) for x in (0.02, 0.03, 0.05, 0.08)],
    *[Rule(f"take {int(x * 100)}% / time 60", "target", 60, x) for x in (0.05, 0.08)],
    Rule("rising 2% +0.25%/bar / time 20", "rising", 20, 0.02, 0.0025),
    Rule("rising 2% +0.5%/bar / time 20", "rising", 20, 0.02, 0.005),
    Rule("rising 3% +0.5%/bar / time 20", "rising", 20, 0.03, 0.005),
    Rule("rising 2% +0.5%/bar / time 60", "rising", 60, 0.02, 0.005),
    Rule("per-day 0.5% / time 20", "perday", 20, 0.005),
    Rule("per-day 1% / time 20", "perday", 20, 0.01),
    Rule("per-day 2% / time 20", "perday", 20, 0.02),
    Rule("per-day 0.5% / time 60", "perday", 60, 0.005),
    Rule("hybrid 2% day 1 then 6% / time 7", "hybrid", 7, 0.02, 0.06),
    Rule("hybrid 2% day 1 then 6% / time 10", "hybrid", 10, 0.02, 0.06),
    Rule("hybrid 2% day 1 then 6% / time 20", "hybrid", 20, 0.02, 0.06),
    Rule("trail 3% / time 60", "trail", 60, 0.03),
    Rule("trail 5% / time 60", "trail", 60, 0.05),
    Rule("trail 8% / time 60", "trail", 60, 0.08),
    Rule("trail 5% / time 20", "trail", 20, 0.05),
]


def evaluate(paths: Paths, rule: Rule):
    """(gross return per trade, bars held) under ``rule``; NaN where the path is incomplete."""
    N = paths.op.shape[0]
    hold = rule.hold
    ret = np.full(N, np.nan)
    bars = np.full(N, hold, dtype=int)
    done = np.zeros(N, dtype=bool)
    peak = np.full(N, -np.inf)
    for k in range(hold):
        op, hi, cl = paths.op[:, k], paths.hi[:, k], paths.cl[:, k]
        live = ~done & np.isfinite(cl)
        if rule.kind in ("target", "rising", "hybrid"):
            tgt = rule.a if rule.kind == "target" else rule.a + rule.b * k if rule.kind == "rising" else (rule.a if k == 0 else rule.b)
            hit = live & (hi >= tgt)
            ret[hit] = np.where(op[hit] >= tgt, op[hit], tgt)
        elif rule.kind == "perday":
            hit = live & (cl >= rule.a * (k + 1))
            ret[hit] = cl[hit]
        elif rule.kind == "trail":
            peak[live] = np.maximum(peak[live], cl[live])
            dd = (1.0 + cl) / (1.0 + peak) - 1.0
            hit = live & (k > 0) & (dd <= -rule.a)
            ret[hit] = cl[hit]
        else:
            hit = np.zeros(N, dtype=bool)
        bars[hit] = k + 1
        done |= hit
    rest = ~done & np.isfinite(paths.cl[:, hold - 1])
    ret[rest] = paths.cl[rest, hold - 1]
    return ret, bars


def _stats(net: np.ndarray, b_e: np.ndarray, rnet: np.ndarray, b_r: np.ndarray, hold: int) -> Dict:
    excess = net - rnet.mean(axis=1)
    lo, hi = bootstrap_mean_ci(excess, reps=500)
    per_bar = net.sum() / b_e.sum() * 1e4
    rand_per_bar = rnet.sum() / b_r.sum() * 1e4
    wins, losses = net[net > 0].sum(), -net[net < 0].sum()
    return {"n": int(len(net)), "net_ret": float(net.mean()), "hit": float((net > 0).mean()),
            "avg_bars": float(b_e.mean()), "early_exit": float((b_e < hold).mean()),
            "per_bar_bp": float(per_bar), "rand_net": float(rnet.mean()), "rand_hit": float((rnet > 0).mean()),
            "rand_avg_bars": float(b_r.mean()), "rand_per_bar_bp": float(rand_per_bar),
            "excess": float(excess.mean()), "excess_lo": lo, "excess_hi": hi,
            "excess_bar_bp": float(per_bar - rand_per_bar),
            "profit_factor": float(wins / losses) if losses > 0 else np.inf}


def exit_grid(ev: pd.DataFrame, pe: Paths, pr: Paths, order: np.ndarray, split: str, cost: float = 0.001,
              rules: Sequence[Rule] = RULES, random_draws: int = RANDOM_DRAWS, min_n: int = 30) -> pd.DataFrame:
    ev = ev.reset_index(drop=True).loc[order].reset_index(drop=True)
    is_train = (pd.to_datetime(ev["signal_date"]) < pd.Timestamp(split)).to_numpy()
    rows = []
    for rule in rules:
        r_e, b_e = evaluate(pe, rule)
        r_r, b_r = evaluate(pr, rule)
        r_r = r_r.reshape(len(ev), random_draws)
        b_r = b_r.reshape(len(ev), random_draws)
        ok = np.isfinite(r_e) & np.isfinite(r_r).all(axis=1)
        for period, m in (("train", ok & is_train), ("test", ok & ~is_train), ("all", ok)):
            if m.sum() < min_n:
                continue
            s = _stats(r_e[m] - cost, b_e[m], r_r[m] - cost, b_r[m], rule.hold)
            rows.append({"rule": rule.name, "kind": rule.kind, "hold": rule.hold, "period": period, **s})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# entry rules -> event tables (symbol, entry_idx, dir, signal_date)
# ----------------------------------------------------------------------------
def _beaten_down(c: np.ndarray, t: int) -> bool:
    """State at the close of bar ``t``: below the 200-day MA and down > 8 % over 126 bars."""
    if t < 200:
        return False
    return bool(c[t] < c[t - 199:t + 1].mean() and c[t] / c[t - 126] - 1.0 < -0.08)


def wedge_events(events: pd.DataFrame) -> pd.DataFrame:
    """Confirmed bullish Falling Wedge events (from ``deepdive.collect_pattern_events``) in beaten-down stocks."""
    ev = events[(events["dir"] == 1) & (events["ret_126"] < -0.08) & (events["dist_ma200"] < 0)]
    return ev[["symbol", "entry_idx", "dir", "signal_date"]].reset_index(drop=True)


def newsday_events(frames: Dict[str, pd.DataFrame], gap_min: float = 0.04, vol_mult: float = 3.0) -> pd.DataFrame:
    rows = []
    for s, df in frames.items():
        c, o, v = (df[x].to_numpy(dtype=float) for x in ("Close", "Open", "Volume"))
        n = len(c)
        if n < 300:
            continue
        gap = np.full(n, np.nan)
        gap[1:] = o[1:] / c[:-1] - 1.0
        avgv = pd.Series(v).rolling(20).mean().shift(1).to_numpy()
        hits = np.where(np.isfinite(gap) & (np.abs(gap) >= gap_min) & np.isfinite(avgv) & (v >= vol_mult * avgv))[0]
        last = -100
        for t in hits:
            if t - last < 5 or t < 260 or t + 1 >= n:
                continue
            last = t
            if not _beaten_down(c, t):
                continue
            rows.append({"symbol": s, "entry_idx": t + 1, "dir": 1, "signal_date": str(df.index[t].date())})
    return pd.DataFrame(rows)


def insider_events(frames: Dict[str, pd.DataFrame], tx: pd.DataFrame, min_value: float = 100_000.0) -> pd.DataFrame:
    from algovision.data.insiders import single_events
    ev = single_events(tx, min_value=min_value)
    rows = []
    for s, g in ev.groupby("symbol"):
        df = frames.get(s)
        if df is None or len(df) < 300:
            continue
        c = df["Close"].to_numpy(dtype=float)
        idx = df.index
        for r in g.itertuples():
            e = int(idx.searchsorted(pd.Timestamp(r.date), side="right"))   # first bar after the filing date
            if e < 210 or e >= len(c) or not _beaten_down(c, e - 1):
                continue
            rows.append({"symbol": s, "entry_idx": e, "dir": 1, "signal_date": str(pd.Timestamp(r.date).date())})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# report
# ----------------------------------------------------------------------------
def _pct(v) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.2f}%"


def grid_markdown(g: pd.DataFrame, period: str) -> str:
    d = g[g["period"] == period].copy()
    if not len(d):
        return ""
    out = pd.DataFrame({
        "exit rule": d["rule"], "n": d["n"], "net / trade": d["net_ret"].map(_pct),
        "hit": d["hit"].map(lambda v: f"{v * 100:.0f}%"), "bars": d["avg_bars"].map(lambda v: f"{v:.1f}"),
        "early exit": d["early_exit"].map(lambda v: f"{v * 100:.0f}%"),
        "bp / bar": d["per_bar_bp"].map(lambda v: f"{v:.1f}"),
        "random net / trade": d["rand_net"].map(_pct), "random bp / bar": d["rand_per_bar_bp"].map(lambda v: f"{v:.1f}"),
        "excess / trade (95% CI)": [f"{_pct(a)} ({_pct(b)} to {_pct(c)})" for a, b, c in zip(d["excess"], d["excess_lo"], d["excess_hi"])],
        "excess bp / bar": d["excess_bar_bp"].map(lambda v: f"{v:+.1f}"),
        "PF": d["profit_factor"].map(lambda v: f"{v:.2f}"),
    })
    return out.to_markdown(index=False) + "\n"


def write_exits_report(out_dir: Path, tables: Dict[str, pd.DataFrame], meta: Dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    md = ["# Exit rules on the tested entries: time exit vs take-profit, rising target, per-day threshold, trailing stop\n",
          f"Universe {meta['n_symbols']} symbols, {meta['period']} daily bars, entry at the next open, cost "
          f"{meta['cost'] * 1e4:.0f} bps per round trip, train before {meta['split']}, test from {meta['split']}. "
          "Random = the same exit rule on 10 random entries per event in the same stock within +-6 months. "
          "`bp / bar` = net return summed over trades divided by bars held (return per bar of capital). "
          "`excess` = signal minus random under the same exit rule.\n"]
    for name, g in tables.items():
        g.to_csv(out_dir / f"exits_{name}.csv", index=False)
        n_all = int(g[g["period"] == "all"]["n"].max()) if len(g) else 0
        md.append(f"## {meta['titles'][name]} ({n_all} events)\n")
        for period in ("train", "test", "all"):
            t = grid_markdown(g, period)
            if t:
                md.append(f"### {period}\n\n{t}")
    p = out_dir / "exits.md"
    p.write_text("\n".join(md), encoding="utf-8")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    from algovision.data.provider import DataProvider, _DEFAULT_CACHE
    from algovision.data.universe import get_universe

    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="docs/research/exits")
    ap.add_argument("--period", default="10y")
    ap.add_argument("--split", default="2023-01-01")
    ap.add_argument("--cost", type=float, default=0.001)
    ap.add_argument("--wedge-csv", default=None, help="events from deepdive.collect_pattern_events (Falling Wedge)")
    ap.add_argument("--insider-dir", default=None, help="directory with the SEC quarterly data sets")
    ap.add_argument("--cache-dir", default=None)
    args = ap.parse_args(argv)

    t0 = time.time()
    log = lambda m: print(f"  {m} ({time.time() - t0:.0f}s)", file=sys.stderr)  # noqa: E731
    provider = DataProvider(cache_dir=Path(args.cache_dir) if args.cache_dir else _DEFAULT_CACHE, offline=True)
    symbols = get_universe("all")
    frames = {}
    for s in symbols:
        try:
            frames[s] = provider.get(s, args.period, "1d")
        except Exception:  # noqa: BLE001
            pass
    log(f"{len(frames)} frames")
    get_frame = lambda s: frames[s]  # noqa: E731

    entries: Dict[str, pd.DataFrame] = {}
    if args.wedge_csv:
        entries["wedge"] = wedge_events(pd.read_csv(args.wedge_csv))
    entries["newsday"] = newsday_events(frames)
    if args.insider_dir:
        from algovision.data.insiders import load_transactions
        tx = load_transactions(Path(args.insider_dir))
        tx = tx[tx["symbol"].isin(frames)]
        entries["insider"] = insider_events(frames, tx)
    titles = {"wedge": "Falling Wedge, beaten-down (journal hold: 20 bars)",
              "newsday": "News day, beaten-down (journal hold: 60 bars)",
              "insider": "Insider purchase >= $100k, beaten-down (journal hold: 120 bars; study horizon 60)"}
    tables = {}
    for name, ev in entries.items():
        ev = ev[ev["symbol"].isin(frames)].reset_index(drop=True)
        log(f"{name}: {len(ev)} events")
        if len(ev) < 30:
            continue
        pe, pr, order = build_paths(ev, get_frame, hmax=HMAX, random_draws=RANDOM_DRAWS)
        tables[name] = exit_grid(ev, pe, pr, order, args.split, cost=args.cost)
        log(f"{name}: grid done")
    meta = {"n_symbols": len(frames), "period": args.period, "cost": args.cost, "split": args.split, "titles": titles}
    p = write_exits_report(Path(args.out), tables, meta)
    print(f"wrote {p}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
