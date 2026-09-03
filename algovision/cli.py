"""Command-line interface.

    python -m algovision scan     --universe sp500 --mode current --report out/scan.html
    python -m algovision analyze  AAPL MSFT --period 3y --mode all --charts out/charts
    python -m algovision history  NVDA --period 5y --patterns cup,hs
    python -m algovision demo     --out out/demo
    python -m algovision patterns
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

from algovision.core.types import DetectorConfig
from algovision.data.provider import DataProvider
from algovision.data.universe import UNIVERSES, get_universe
from algovision.patterns import ALIASES, ALL_PATTERNS, resolve_patterns
from algovision.scanner import Scanner, ScanResult


def _parse_patterns(value: Optional[str]) -> Optional[List[str]]:
    if not value:
        return None
    return resolve_patterns([p for p in value.replace(";", ",").split(",") if p.strip()])


def _provider(args) -> DataProvider:
    return DataProvider(cache_dir=None if args.no_cache else Path(args.cache_dir) if args.cache_dir else DataProvider.__init__.__defaults__[0],
                        csv_dir=Path(args.csv_dir) if args.csv_dir else None,
                        max_age_hours=args.max_age, offline=args.offline, workers=args.workers)


def _config(args) -> DetectorConfig:
    cfg = DetectorConfig()
    if getattr(args, "recent_bars", None) is not None:
        cfg.recent_bars = args.recent_bars
    if getattr(args, "min_score", None) is not None:
        cfg.min_score = args.min_score
    if getattr(args, "beaten_down", False):
        cfg.filter_max_ret_126 = -0.08
        cfg.filter_below_ma200 = True
    if getattr(args, "max_6m_return", None) is not None:
        cfg.filter_max_ret_126 = args.max_6m_return
    if getattr(args, "below_ma200", False):
        cfg.filter_below_ma200 = True
    if getattr(args, "min_atr_pct", None) is not None:
        cfg.filter_min_atr_pct = args.min_atr_pct
    if getattr(args, "config", None):
        with open(args.config, "r", encoding="utf-8") as fh:
            for k, v in json.load(fh).items():
                if not hasattr(cfg, k):
                    raise SystemExit(f"unknown config key {k!r}")
                setattr(cfg, k, tuple(v) if isinstance(getattr(cfg, k), tuple) else v)
    return cfg


def _emit(result: ScanResult, args, title: str) -> None:
    matches = result.matches
    if args.top:
        matches = matches[: args.top]
    if not matches:
        print("No patterns matched.")
    else:
        df = result.to_frame().head(len(matches))
        show = df.drop(columns=["why"])
        try:
            import pandas as pd
            with pd.option_context("display.max_rows", None, "display.width", 200, "display.max_columns", None):
                print(show.to_string(index=False))
        except Exception:  # pragma: no cover
            print(show)
        if args.explain:
            print()
            for m in matches:
                print(m.explanation())
                print()
    if args.csv:
        result.to_frame().to_csv(args.csv, index=False)
        print(f"wrote {args.csv}")
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump([m.to_dict() for m in result.matches], fh, indent=1, default=str)
        print(f"wrote {args.json}")
    if args.charts:
        from algovision.plotting import plot_matches
        paths = plot_matches(result.frames, matches, args.charts, context=args.context)
        print(f"wrote {len(paths)} chart(s) to {args.charts}")
    if args.report:
        from algovision.report import write_report
        p = write_report(result.frames, matches, args.report, title=title, context=args.context)
        print(f"wrote report {p}")
    if result.errors:
        print(f"{len(result.errors)} symbol(s) skipped: " + ", ".join(sorted(result.errors)[:15])
              + (" ..." if len(result.errors) > 15 else ""), file=sys.stderr)


def _add_common(p: argparse.ArgumentParser, default_mode: str) -> None:
    p.add_argument("--period", default="2y", help="history window: 6mo, 1y, 2y, 5y, 10y, max (default 2y)")
    p.add_argument("--interval", default="1d", help="bar interval: 1d, 1wk (default 1d)")
    p.add_argument("--mode", choices=("current", "history", "all"), default=default_mode,
                   help="current = forming / just-confirmed setups; history = past occurrences with outcomes")
    p.add_argument("--patterns", "-p", default=None, help="comma list, e.g. 'hs,cup,double-top' (default all)")
    p.add_argument("--min-score", type=float, default=None, help="minimum confidence 0-1 (default 0.60)")
    p.add_argument("--recent-bars", type=int, default=None, help="bars back that still count as 'current' (default 15)")
    p.add_argument("--config", default=None, help="JSON file overriding DetectorConfig fields")
    p.add_argument("--beaten-down", action="store_true",
                   help="only stocks down >8%% over 6 months AND below their 200-day MA (the regime where "
                        "bottom-reversal patterns showed an edge; see docs/research_falling_wedge.md)")
    p.add_argument("--max-6m-return", type=float, default=None, help="keep only matches with 6-month return below this fraction, e.g. -0.08")
    p.add_argument("--below-ma200", action="store_true", help="keep only matches with price below the 200-day MA")
    p.add_argument("--min-atr-pct", type=float, default=None, help="keep only matches with ATR/price above this, e.g. 0.02")
    p.add_argument("--top", type=int, default=0, help="only print/plot the N best matches")
    p.add_argument("--explain", action="store_true", help="print the full 'why' for every match")
    p.add_argument("--csv", default=None, help="write results table to CSV")
    p.add_argument("--json", default=None, help="write full match objects to JSON")
    p.add_argument("--charts", default=None, help="directory for one PNG per match")
    p.add_argument("--report", default=None, help="write a self-contained HTML report with charts")
    p.add_argument("--context", type=int, default=25, help="extra bars drawn around each pattern")
    # data
    p.add_argument("--csv-dir", default=None, help="read SYMBOL.csv files from this directory instead of the network")
    p.add_argument("--cache-dir", default=None, help="price cache directory (default ~/.algovision/cache)")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--max-age", type=float, default=12.0, help="hours before cached prices are refreshed")
    p.add_argument("--offline", action="store_true", help="use cached prices only")
    p.add_argument("--workers", type=int, default=4, help="parallel downloads")
    p.add_argument("-v", "--verbose", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="algovision", description="Visual chart-pattern scanner for US stocks.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan", help="scan an index universe")
    s.add_argument("--universe", "-u", default="sp500", choices=UNIVERSES)
    s.add_argument("--symbols", default=None, help="comma list overriding the universe")
    s.add_argument("--limit", type=int, default=0, help="only the first N symbols (testing)")
    s.add_argument("--refresh-universe", action="store_true", help="re-download constituent lists")
    _add_common(s, "current")

    a = sub.add_parser("analyze", help="analyse specific symbols")
    a.add_argument("symbols", nargs="+")
    _add_common(a, "all")

    h = sub.add_parser("history", help="all past occurrences for symbols, with outcomes")
    h.add_argument("symbols", nargs="+")
    _add_common(h, "history")

    d = sub.add_parser("demo", help="run the detectors on synthetic textbook patterns (no network)")
    d.add_argument("--out", default="out/demo", help="output directory for charts + report")
    d.add_argument("--explain", action="store_true")

    r = sub.add_parser("research", help="event study: can the setups be trusted? (hindsight + walk-forward)")
    r.add_argument("--universe", "-u", default="all", choices=UNIVERSES)
    r.add_argument("--symbols", default=None, help="comma list overriding the universe")
    r.add_argument("--limit", type=int, default=0)
    r.add_argument("--period", default="10y")
    r.add_argument("--interval", default="1d")
    r.add_argument("--benchmark", default="SPY")
    r.add_argument("--out", default="out/research")
    r.add_argument("--min-score", type=float, default=None)
    r.add_argument("--config", default=None)
    r.add_argument("--workers", type=int, default=4)
    r.add_argument("--wf-symbols", type=int, default=60, help="walk-forward validation sample size (0 = skip)")
    r.add_argument("--wf-bars", type=int, default=1000, help="walk-forward: last N bars per symbol")
    r.add_argument("--wf-window", type=int, default=400, help="walk-forward: detection window in bars")
    r.add_argument("--wf-step", type=int, default=1)
    r.add_argument("--seed", type=int, default=42)
    r.add_argument("--short-term", action="store_true", help="also run the short-horizon exit study (hold 1-5 bars, take-profit)")
    r.add_argument("--cache-dir", default=None)
    r.add_argument("--csv-dir", default=None)
    r.add_argument("--offline", action="store_true")
    r.add_argument("--no-cache", action="store_true")
    r.add_argument("--max-age", type=float, default=12.0)
    r.add_argument("-v", "--verbose", action="store_true")

    dd = sub.add_parser("deepdive", help="deep dive on one pattern: features, filters, exits, entries, portfolio (train/test split)")
    dd.add_argument("--pattern", required=True, help="e.g. 'Falling Wedge' or alias 'falling-wedge'")
    dd.add_argument("--universe", "-u", default="all", choices=UNIVERSES)
    dd.add_argument("--symbols", default=None)
    dd.add_argument("--limit", type=int, default=0)
    dd.add_argument("--period", default="10y")
    dd.add_argument("--interval", default="1d")
    dd.add_argument("--split", default="2023-01-01", help="test period starts here")
    dd.add_argument("--out", default=None, help="default out/deepdive/<pattern>")
    dd.add_argument("--min-score", type=float, default=None)
    dd.add_argument("--config", default=None)
    dd.add_argument("--workers", type=int, default=4)
    dd.add_argument("--cache-dir", default=None)
    dd.add_argument("--csv-dir", default=None)
    dd.add_argument("--offline", action="store_true")
    dd.add_argument("--no-cache", action="store_true")
    dd.add_argument("--max-age", type=float, default=12.0)
    dd.add_argument("-v", "--verbose", action="store_true")

    fa = sub.add_parser("factors", help="classic anomalies on the universe: cross-sectional momentum, trend filter, short-term reversal")
    fa.add_argument("--universe", "-u", default="all", choices=UNIVERSES)
    fa.add_argument("--symbols", default=None)
    fa.add_argument("--limit", type=int, default=0)
    fa.add_argument("--period", default="10y")
    fa.add_argument("--interval", default="1d")
    fa.add_argument("--split", default="2023-01-01")
    fa.add_argument("--out", default="out/factors")
    fa.add_argument("--cost-bps", type=float, default=10.0, help="per-side cost on turnover for ranked portfolios")
    fa.add_argument("--workers", type=int, default=4)
    fa.add_argument("--cache-dir", default=None)
    fa.add_argument("--csv-dir", default=None)
    fa.add_argument("--offline", action="store_true")
    fa.add_argument("--no-cache", action="store_true")
    fa.add_argument("--max-age", type=float, default=12.0)
    fa.add_argument("-v", "--verbose", action="store_true")

    nd = sub.add_parser("newsday", help="live scan: big news-gap days in beaten-down stocks (docs/research_anomalies.md)")
    nd.add_argument("--universe", "-u", default="all", choices=UNIVERSES)
    nd.add_argument("--symbols", default=None)
    nd.add_argument("--period", default="2y")
    nd.add_argument("--max-age", type=int, default=5, help="news day within the last N bars")
    nd.add_argument("--gap-min", type=float, default=0.04)
    nd.add_argument("--vol-mult", type=float, default=3.0)
    nd.add_argument("--any-below-ma200", action="store_true", help="drop the 'down >8%% over 6 months' requirement")
    nd.add_argument("--csv", default=None)
    nd.add_argument("--cache-dir", default=None)
    nd.add_argument("--csv-dir", default=None)
    nd.add_argument("--offline", action="store_true")
    nd.add_argument("--no-cache", action="store_true")
    nd.add_argument("--max-age-hours", type=float, default=12.0, dest="max_age_hours")
    nd.add_argument("--workers", type=int, default=4)
    nd.add_argument("-v", "--verbose", action="store_true")

    jo = sub.add_parser("journal", help="daily forward test: log live signals and mark previous ones to market")
    jo.add_argument("--out", default="journal")
    jo.add_argument("--universe", "-u", default="all", choices=UNIVERSES)
    jo.add_argument("--period", default="2y")
    jo.add_argument("--cache-dir", default=None)
    jo.add_argument("--max-age", type=float, default=0.5, help="hours; prices older than this are re-downloaded")
    jo.add_argument("--workers", type=int, default=4)
    jo.add_argument("--date", default=None, help="log date (default today)")

    sub.add_parser("patterns", help="list supported patterns")
    sub.add_parser("universe", help="print the bundled universes").add_argument("--name", default="sp500", choices=UNIVERSES)
    return ap


def cmd_scan(args) -> int:
    if args.symbols:
        symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    else:
        symbols = get_universe(args.universe, refresh=args.refresh_universe)
    if args.limit:
        symbols = symbols[: args.limit]
    scanner = Scanner(_provider(args), _config(args), _parse_patterns(args.patterns), args.period, args.interval,
                      min_score=args.min_score)
    print(f"scanning {len(symbols)} symbols ({args.universe if not args.symbols else 'custom'}), "
          f"mode={args.mode}, period={args.period}, patterns={len(scanner.patterns)}", file=sys.stderr)

    def progress(sym, done, total, found):
        if args.verbose or done % 25 == 0 or done == total:
            print(f"  [{done}/{total}] {sym}: {found} match(es)", file=sys.stderr)

    result = scanner.scan(symbols, mode=args.mode, progress=progress)
    _emit(result, args, f"AlgoVision {args.universe} scan - {args.mode}")
    return 0


def cmd_analyze(args) -> int:
    symbols = [s.upper() for s in args.symbols]
    scanner = Scanner(_provider(args), _config(args), _parse_patterns(args.patterns), args.period, args.interval,
                      min_score=args.min_score)
    result = scanner.scan(symbols, mode=args.mode)
    result.matches.sort(key=lambda m: (m.symbol, m.end_idx))
    _emit(result, args, f"AlgoVision analysis - {', '.join(symbols)}")
    return 0


def cmd_demo(args) -> int:
    import pandas as pd

    from algovision.data.synthetic import GENERATORS
    from algovision.report import write_report

    result = ScanResult()
    scanner = Scanner(provider=DataProvider(cache_dir=None, offline=True))
    for name, gen in GENERATORS.items():
        df, meta = gen()
        sym = "SYN-" + name.upper().replace(" ", "-")[:18]
        ms = scanner.analyse_frame(sym, df, mode="all")
        ms = [m for m in ms if m.pattern == name] or ms[:1]
        result.frames[sym] = df
        result.matches.extend(ms)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    frame = result.to_frame().drop(columns=["why"])
    with pd.option_context("display.max_rows", None, "display.width", 200, "display.max_columns", None):
        print(frame.to_string(index=False))
    if args.explain:
        for m in result.matches:
            print()
            print(m.explanation())
    p = write_report(result.frames, result.matches, out / "demo.html", title="AlgoVision demo - synthetic patterns")
    print(f"\nwrote {p} (charts in {out / 'charts'})")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if getattr(args, "verbose", False) else logging.WARNING,
                        format="%(levelname)s %(name)s: %(message)s")
    if args.cmd == "patterns":
        for p in ALL_PATTERNS:
            al = [k for k, v in ALIASES.items() if v == p]
            print(f"{p:28s} aliases: {', '.join(al)}")
        return 0
    if args.cmd == "universe":
        for s in get_universe(args.name):
            print(s)
        return 0
    if args.cmd == "demo":
        return cmd_demo(args)
    if args.cmd == "research":
        from algovision.research.cli import cmd_research
        return cmd_research(args)
    if args.cmd == "deepdive":
        from algovision.research.cli import cmd_deepdive
        return cmd_deepdive(args)
    if args.cmd == "factors":
        from algovision.research.cli import cmd_factors
        return cmd_factors(args)
    if args.cmd == "journal":
        from algovision.journal import run as run_journal
        p = run_journal(Path(args.out), args.universe, args.period, Path(args.cache_dir) if args.cache_dir else None,
                        args.max_age, args.workers, args.date)
        print(p.read_text())
        return 0
    if args.cmd == "newsday":
        from algovision.research.cli import cmd_newsday
        return cmd_newsday(args)
    if args.cmd == "scan":
        return cmd_scan(args)
    return cmd_analyze(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
