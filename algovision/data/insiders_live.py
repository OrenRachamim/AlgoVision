"""Live insider trades from EDGAR's daily index (Form 4 filings of the last N business days).

The quarterly structured data sets lag by months; this reads the daily form
index, keeps Form 4 filings whose issuer CIK is in the universe, fetches each
filing once (cached) and parses the embedded XML.  SEC asks for a descriptive
User-Agent and <= 10 requests/second.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional
import xml.etree.ElementTree as ET

import pandas as pd

from algovision.data.provider import _DEFAULT_CACHE

log = logging.getLogger(__name__)
_CIK_MAP = Path(__file__).with_name("cik_map.json")
UA = "AlgoVision research orenrachamim@gmail.com"


def cik_map() -> Dict[str, str]:
    return json.loads(_CIK_MAP.read_text())


def _get(url: str, timeout: int = 60) -> Optional[bytes]:
    import requests

    for attempt in range(3):
        r = requests.get(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"}, timeout=timeout)
        if r.status_code == 200:
            time.sleep(0.12)
            return r.content
        if r.status_code in (403, 429):
            time.sleep(2 + 2 * attempt)
            continue
        return None
    return None


def daily_form4(day: pd.Timestamp, ciks: Iterable[str], cache_dir: Path) -> List[Dict]:
    """Form 4 entries (issuer CIK, path) for one day, restricted to ``ciks``."""
    q = (day.month - 1) // 3 + 1
    p = cache_dir / f"form.{day:%Y%m%d}.idx"
    if p.exists():
        text = p.read_text(errors="ignore")
    else:
        raw = _get(f"https://www.sec.gov/Archives/edgar/daily-index/{day.year}/QTR{q}/form.{day:%Y%m%d}.idx")
        if raw is None:
            return []
        text = raw.decode("latin-1")
        p.write_text(text)
    ciks = set(ciks)
    out = []
    for line in text.splitlines():
        if not line.startswith("4 "):
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) < 5:
            continue
        cik = parts[2].strip()
        if cik in ciks:
            out.append({"cik": cik, "path": parts[4].strip(), "date": day})
    return out


def parse_form4(text: str) -> List[Dict]:
    """Non-derivative open-market transactions (codes P and S) from a Form 4 filing text."""
    m = re.search(r"<ownershipDocument>.*?</ownershipDocument>", text, re.S)
    if not m:
        return []
    try:
        root = ET.fromstring(m.group(0))
    except ET.ParseError:
        return []
    g = lambda el, path: (el.findtext(path) or "").strip()  # noqa: E731
    symbol = g(root, "issuer/issuerTradingSymbol").upper().replace(".", "-")
    owners = root.findall("reportingOwner")
    rel_officer = any(g(o, "reportingOwnerRelationship/isOfficer") in ("1", "true") for o in owners)
    rel_director = any(g(o, "reportingOwnerRelationship/isDirector") in ("1", "true") for o in owners)
    rel_ten = any(g(o, "reportingOwnerRelationship/isTenPercentOwner") in ("1", "true") for o in owners)
    title = " ".join(g(o, "reportingOwnerRelationship/officerTitle") for o in owners).upper()
    names = "; ".join(g(o, "reportingOwnerId/rptOwnerName") for o in owners)
    owner_cik = g(owners[0], "reportingOwnerId/rptOwnerCik") if owners else ""
    rows = []
    for t in root.findall("nonDerivativeTable/nonDerivativeTransaction"):
        code = g(t, "transactionCoding/transactionCode")
        if code not in ("P", "S"):
            continue
        try:
            shares = float(g(t, "transactionAmounts/transactionShares/value") or "nan")
            price = float(g(t, "transactionAmounts/transactionPricePerShare/value") or "nan")
        except ValueError:
            continue
        rows.append({"symbol": symbol, "owner_cik": owner_cik, "owner_name": names, "is_officer": rel_officer,
                     "is_director": rel_director, "is_ten_pct": rel_ten,
                     "is_ceo_cfo": bool(re.search(r"CHIEF EXECUTIVE|CEO|CHIEF FINANCIAL|CFO", title)),
                     "trans_date": pd.to_datetime(g(t, "transactionDate/value"), errors="coerce"), "code": code,
                     "shares": shares, "price": price, "value": shares * price})
    return rows


def recent_transactions(days: int = 45, cache_dir: Optional[Path] = None, symbols: Optional[Iterable[str]] = None,
                        progress=None, workers: int = 4) -> pd.DataFrame:
    """Officer / director open-market trades filed in the last ``days`` calendar days."""
    cache = Path(cache_dir or _DEFAULT_CACHE) / "edgar"
    cache.mkdir(parents=True, exist_ok=True)
    cm = cik_map()
    if symbols is not None:
        want = set(symbols)
        cm = {k: v for k, v in cm.items() if v in want}
    ciks = set(cm)
    today = pd.Timestamp.today().normalize()
    rows: List[Dict] = []
    bdays = pd.bdate_range(today - pd.Timedelta(days=days), today)
    from concurrent.futures import ThreadPoolExecutor

    def fetch_one(e):
        fp = cache / e["path"].replace("/", "_")
        if fp.exists():
            return e, fp.read_text(errors="ignore")
        raw = _get(f"https://www.sec.gov/Archives/{e['path']}")
        if raw is None:
            return e, None
        text = raw.decode("latin-1", errors="ignore")
        fp.write_text(text)
        return e, text

    for i, day in enumerate(bdays):
        entries = daily_form4(day, ciks, cache)
        with ThreadPoolExecutor(max_workers=workers) as ex:      # SEC allows 10 req/s; 4 workers x 0.12 s sleep stays well under
            results = list(ex.map(fetch_one, entries))
        for e, text in results:
            if text is None:
                continue
            for r in parse_form4(text):
                r["filing_date"] = day
                r["issuer_cik"] = e["cik"]
                if not r["symbol"]:
                    r["symbol"] = cm.get(e["cik"], "")
                rows.append(r)
        if progress:
            progress(i + 1, len(bdays), len(rows))
    df = pd.DataFrame(rows)
    if not len(df):
        return df
    df = df[(df["is_officer"] | df["is_director"]) & df["value"].notna() & (df["value"] > 0)]
    return df.drop_duplicates(subset=["symbol", "owner_cik", "trans_date", "code", "shares", "price"]).reset_index(drop=True)
