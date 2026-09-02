"""Ticker universes: S&P 500 and NASDAQ-100.

A snapshot of both lists ships with the package so scans work offline.  Pass
``refresh=True`` to pull the live lists (Wikipedia / api.nasdaq.com).
"""

from __future__ import annotations

import io
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger(__name__)

_SNAPSHOT = Path(__file__).with_name("universe_snapshot.json")
_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
       "Accept": "application/json, text/html"}

UNIVERSES = ("sp500", "nasdaq100", "all")


def load_snapshot() -> Dict:
    with open(_SNAPSHOT, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _fetch_sp500() -> List[Dict]:
    import pandas as pd
    import requests

    r = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies", headers=_UA, timeout=60)
    r.raise_for_status()
    t = pd.read_html(io.StringIO(r.text))[0]
    return [{"symbol": str(s).replace(".", "-"), "name": str(n), "sector": str(sec)}
            for s, n, sec in zip(t["Symbol"], t["Security"], t["GICS Sector"])]


def _fetch_nasdaq100() -> List[Dict]:
    import requests

    r = requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100", headers=_UA, timeout=60)
    r.raise_for_status()
    rows = r.json()["data"]["data"]["rows"]
    return [{"symbol": str(x["symbol"]).replace(".", "-").strip(), "name": str(x.get("companyName", ""))}
            for x in rows]


def refresh_snapshot(path: Optional[Path] = None) -> Dict:
    """Download fresh constituent lists and overwrite the bundled snapshot."""
    import datetime as dt

    snap = {"as_of": str(dt.date.today()),
            "sources": {"sp500": "Wikipedia", "nasdaq100": "api.nasdaq.com"},
            "sp500": _fetch_sp500(), "nasdaq100": _fetch_nasdaq100()}
    with open(path or _SNAPSHOT, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=1)
    return snap


def get_universe(name: str = "sp500", refresh: bool = False) -> List[str]:
    """Return the list of symbols for ``sp500``, ``nasdaq100`` or ``all``."""
    name = name.lower()
    if name not in UNIVERSES:
        raise ValueError(f"unknown universe {name!r}; choose from {UNIVERSES}")
    snap = None
    if refresh:
        try:
            snap = refresh_snapshot()
        except Exception as exc:  # network problems -> fall back to the bundled list
            log.warning("could not refresh universe lists (%s); using bundled snapshot", exc)
    if snap is None:
        snap = load_snapshot()
    if name == "sp500":
        syms = [x["symbol"] for x in snap["sp500"]]
    elif name == "nasdaq100":
        syms = [x["symbol"] for x in snap["nasdaq100"]]
    else:
        syms = [x["symbol"] for x in snap["sp500"]] + [x["symbol"] for x in snap["nasdaq100"]]
    seen, out = set(), []
    for s in syms:
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


def symbol_names() -> Dict[str, str]:
    snap = load_snapshot()
    names = {}
    for x in snap["nasdaq100"]:
        names[x["symbol"]] = x["name"]
    for x in snap["sp500"]:
        names[x["symbol"]] = x["name"]
    return names
