"""``python -m algovision research`` implementation."""

from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig
from algovision.data.provider import DataProvider
from algovision.data.universe import get_universe
from algovision.research.events import add_local_baseline
from algovision.research.run import hindsight_subset, run_hindsight, run_walkforward, save_outputs


def cmd_research(args) -> int:
    from algovision.cli import _config  # reuse config handling
    cfg = _config(args)
    if args.symbols:
        symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    else:
        symbols = get_universe(args.universe)
    if args.limit:
        symbols = symbols[: args.limit]
    provider_kwargs = dict(cache_dir=None if args.no_cache else (Path(args.cache_dir) if args.cache_dir else DataProvider.__init__.__defaults__[0]),
                           csv_dir=Path(args.csv_dir) if args.csv_dir else None, max_age_hours=args.max_age,
                           offline=args.offline, workers=1)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    def prog(i, n, ne, el):
        print(f"  hindsight [{i}/{n}] events={ne} {el:.0f}s", file=sys.stderr)

    print(f"research: {len(symbols)} symbols, period={args.period}, min_score={cfg.min_score}", file=sys.stderr)
    events, structures, errors = run_hindsight(symbols, provider_kwargs, cfg, args.period, args.interval,
                                               args.benchmark, args.workers, progress=prog)
    print(f"hindsight done: {len(events)} events, {len(structures)} structures, {len(errors)} errors, "
          f"{time.time() - t0:.0f}s", file=sys.stderr)

    wf = None
    wf_meta = {}
    if args.wf_symbols and len(events):
        rng = np.random.default_rng(args.seed)
        pool = sorted(set(events["symbol"]))
        wf_syms = sorted(rng.choice(pool, size=min(args.wf_symbols, len(pool)), replace=False).tolist())

        def wprog(i, n, ne, el):
            if i % 5 == 0 or i == n:
                print(f"  walk-forward [{i}/{n}] events={ne} {el:.0f}s", file=sys.stderr)

        wf, wf_err = run_walkforward(wf_syms, provider_kwargs, cfg, args.period, args.interval, args.benchmark,
                                     args.workers, args.wf_window, args.wf_bars, args.wf_step, progress=wprog)
        wf_meta = {"symbols": wf_syms, "window": args.wf_window, "last_bars": args.wf_bars, "step": args.wf_step,
                   "errors": wf_err}
        print(f"walk-forward done: {len(wf)} events, {time.time() - t0:.0f}s", file=sys.stderr)

    provider = DataProvider(**{**provider_kwargs, "offline": True})
    if len(events):
        print("computing local random baselines...", file=sys.stderr)
        events = add_local_baseline(events, lambda s: provider.get(s, args.period, args.interval))
    if wf is not None and len(wf):
        wf = add_local_baseline(wf, lambda s: provider.get(s, args.period, args.interval))
    meta = {"generated": dt.datetime.now().isoformat(timespec="seconds"), "universe": args.universe,
            "n_symbols": len(symbols), "period": args.period, "interval": args.interval, "benchmark": args.benchmark,
            "config": cfg.to_dict(), "errors": errors, "walkforward": wf_meta, "elapsed_s": time.time() - t0}
    save_outputs(out, events, structures, wf, meta)

    from algovision.research.report import write_research_report
    p = write_research_report(out, events, structures, wf, meta)
    print(f"wrote {p}", file=sys.stderr)
    if getattr(args, "short_term", False) and len(events):
        from algovision.research.shortterm import write_shortterm_report
        q = write_shortterm_report(out, events, wf, lambda s: provider.get(s, args.period, args.interval))
        print(f"wrote {q}", file=sys.stderr)
    return 0


def cmd_deepdive(args) -> int:
    from algovision.cli import _config
    from algovision.patterns import resolve_patterns
    from algovision.research.deepdive import collect_pattern_events, write_deepdive_report

    cfg = _config(args)
    pattern = resolve_patterns([args.pattern])[0]
    symbols = [s.strip().upper() for s in args.symbols.split(",")] if args.symbols else get_universe(args.universe)
    if args.limit:
        symbols = symbols[: args.limit]
    provider_kwargs = dict(cache_dir=None if args.no_cache else (Path(args.cache_dir) if args.cache_dir else DataProvider.__init__.__defaults__[0]),
                           csv_dir=Path(args.csv_dir) if args.csv_dir else None, max_age_hours=args.max_age,
                           offline=args.offline, workers=1)
    if not args.offline:   # warm the cache once, concurrently
        DataProvider(**{**provider_kwargs, "workers": args.workers}).get_many(list(symbols) + ["SPY"], args.period, args.interval)
    t0 = time.time()
    print(f"deep dive: {pattern} over {len(symbols)} symbols", file=sys.stderr)
    events, errors = collect_pattern_events(symbols, {**provider_kwargs, "offline": True}, pattern, cfg, args.period,
                                            args.interval, args.workers,
                                            progress=lambda i, n, ne: print(f"  [{i}/{n}] events={ne}", file=sys.stderr))
    if not len(events):
        print("no events", file=sys.stderr)
        return 1
    provider = DataProvider(**{**provider_kwargs, "offline": True})
    cache = {}

    def gf(s):
        if s not in cache:
            cache[s] = provider.get(s, args.period, args.interval)
        return cache[s]

    events = add_local_baseline(events, gf)
    out = Path(args.out) if args.out else Path("out/deepdive") / pattern.replace(" ", "_").lower()
    p = write_deepdive_report(out, pattern, events, gf, args.split)
    print(f"wrote {p} ({time.time() - t0:.0f}s, {len(errors)} symbol errors)", file=sys.stderr)
    return 0
