"""Run the full study: hindsight events over a universe + walk-forward validation."""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

from algovision.core.types import DetectorConfig
from algovision.data.provider import DataProvider
from algovision.research.events import HORIZONS, MAX_HOLD, RANDOM_DRAWS, build_events
from algovision.research.walkforward import walk_forward_events

log = logging.getLogger(__name__)

_PROVIDER: Optional[DataProvider] = None
_BENCH: Optional[pd.DataFrame] = None


def _init_worker(provider_kwargs: Dict, bench_symbol: Optional[str], period: str, interval: str) -> None:
    global _PROVIDER, _BENCH
    import warnings
    warnings.filterwarnings("ignore")
    _PROVIDER = DataProvider(**provider_kwargs)
    _BENCH = _PROVIDER.get(bench_symbol, period, interval) if bench_symbol else None


def _hindsight_task(args) -> Tuple[str, List[Dict], List[Dict], Optional[str]]:
    symbol, period, interval, cfg_dict, min_bars = args
    try:
        df = _PROVIDER.get(symbol, period, interval)
        if len(df) < min_bars:
            return symbol, [], [], f"only {len(df)} bars"
        cfg = DetectorConfig(**cfg_dict)
        ev, st = build_events(symbol, df, _BENCH, cfg)
        for e in ev:
            e["method"] = "hindsight"
        return symbol, ev, st, None
    except Exception as exc:  # noqa: BLE001
        return symbol, [], [], str(exc)


def _walkforward_task(args) -> Tuple[str, List[Dict], Optional[str]]:
    symbol, period, interval, cfg_dict, window, last_bars, step = args
    try:
        df = _PROVIDER.get(symbol, period, interval)
        cfg = DetectorConfig(**cfg_dict)
        n = len(df)
        start = max(window, n - last_bars)
        ev = walk_forward_events(symbol, df, _BENCH, cfg, window=window, start=start, step=step)
        return symbol, ev, None
    except Exception as exc:  # noqa: BLE001
        return symbol, [], str(exc)


def _cfg_dict(cfg: DetectorConfig) -> Dict:
    return cfg.to_dict()


def run_hindsight(symbols: Sequence[str], provider_kwargs: Dict, config: Optional[DetectorConfig] = None,
                  period: str = "10y", interval: str = "1d", bench_symbol: Optional[str] = "SPY",
                  workers: int = 4, min_bars: int = 300, progress=None) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, str]]:
    cfg = config or DetectorConfig()
    events: List[Dict] = []
    structures: List[Dict] = []
    errors: Dict[str, str] = {}
    tasks = [(s, period, interval, _cfg_dict(cfg), min_bars) for s in symbols]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker,
                             initargs=(provider_kwargs, bench_symbol, period, interval)) as ex:
        futs = [ex.submit(_hindsight_task, t) for t in tasks]
        for i, f in enumerate(as_completed(futs), 1):
            sym, ev, st, err = f.result()
            events.extend(ev)
            structures.extend(st)
            if err:
                errors[sym] = err
            if progress and (i % 25 == 0 or i == len(futs)):
                progress(i, len(futs), len(events), time.time() - t0)
    return pd.DataFrame(events), pd.DataFrame(structures), errors


def run_walkforward(symbols: Sequence[str], provider_kwargs: Dict, config: Optional[DetectorConfig] = None,
                    period: str = "10y", interval: str = "1d", bench_symbol: Optional[str] = "SPY",
                    workers: int = 4, window: int = 400, last_bars: int = 1250, step: int = 1,
                    progress=None) -> Tuple[pd.DataFrame, Dict[str, str]]:
    cfg = config or DetectorConfig()
    events: List[Dict] = []
    errors: Dict[str, str] = {}
    tasks = [(s, period, interval, _cfg_dict(cfg), window, last_bars, step) for s in symbols]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker,
                             initargs=(provider_kwargs, bench_symbol, period, interval)) as ex:
        futs = [ex.submit(_walkforward_task, t) for t in tasks]
        for i, f in enumerate(as_completed(futs), 1):
            sym, ev, err = f.result()
            events.extend(ev)
            if err:
                errors[sym] = err
            if progress:
                progress(i, len(futs), len(events), time.time() - t0)
    return pd.DataFrame(events), errors


def hindsight_subset(events: pd.DataFrame, symbols: Sequence[str], last_bars: int, window: int,
                     frames_len: Dict[str, int]) -> pd.DataFrame:
    """Hindsight events restricted to the bars the walk-forward actually covered."""
    parts = []
    for s in symbols:
        n = frames_len.get(s)
        if n is None:
            continue
        start = max(window, n - last_bars)
        g = events[(events["symbol"] == s) & (events["signal_idx"] >= start)]
        parts.append(g)
    return pd.concat(parts) if parts else events.iloc[0:0]


def save_outputs(out_dir: Path, events: pd.DataFrame, structures: pd.DataFrame, wf: Optional[pd.DataFrame],
                 meta: Dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    events.to_csv(out_dir / "events.csv", index=False)
    structures.to_csv(out_dir / "structures.csv", index=False)
    if wf is not None:
        wf.to_csv(out_dir / "walkforward_events.csv", index=False)
    with open(out_dir / "meta.json", "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, default=str)
