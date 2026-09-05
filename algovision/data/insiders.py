"""Insider transactions from the SEC's quarterly Form 3/4/5 structured data sets.

https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
Each quarter ships NONDERIV_TRANS (open-market trades), SUBMISSION (filing date,
issuer, ticker) and REPORTINGOWNER (who, and their relationship).  The filing
date is the moment the market could know, so it is the signal date.
"""

from __future__ import annotations

import io
import logging
import time
import zipfile
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

log = logging.getLogger(__name__)

_URL = "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{tag}_form345.zip"
_FILES = ("NONDERIV_TRANS.tsv", "SUBMISSION.tsv", "REPORTINGOWNER.tsv")


def quarters(start: str = "2016q3", end: Optional[str] = None) -> List[str]:
    end = end or f"{pd.Timestamp.today().year}q{(pd.Timestamp.today().month - 1) // 3 + 1}"
    out = []
    y, q = int(start[:4]), int(start[-1])
    while f"{y}q{q}" <= end:
        out.append(f"{y}q{q}")
        q += 1
        if q == 5:
            y, q = y + 1, 1
    return out


def download_quarter(tag: str, dest: Path, user_agent: str, timeout: int = 120) -> bool:
    import requests

    d = dest / tag
    if all((d / f).exists() for f in _FILES):
        return True
    r = requests.get(_URL.format(tag=tag), headers={"User-Agent": user_agent}, timeout=timeout)
    if r.status_code != 200 or not r.content[:2] == b"PK":
        log.warning("%s: not available (%s)", tag, r.status_code)
        return False
    d.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        for f in _FILES:
            z.extract(f, d)
    time.sleep(0.5)
    return True


def load_transactions(dest: Path, tags: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Open-market purchases and sales by officers / directors, one row per transaction.

    Columns: symbol, issuer_cik, owner_cik, owner_name, relationship, is_officer, is_director,
    is_ceo_cfo, trans_date, filing_date, code (P / S), shares, price, value, accession.
    """
    tags = list(tags) if tags else sorted(p.name for p in dest.iterdir() if p.is_dir())
    parts = []
    for tag in tags:
        d = dest / tag
        if not all((d / f).exists() for f in _FILES):
            continue
        tr = pd.read_csv(d / "NONDERIV_TRANS.tsv", sep="\t", low_memory=False,
                         usecols=["ACCESSION_NUMBER", "TRANS_DATE", "TRANS_CODE", "TRANS_SHARES", "TRANS_PRICEPERSHARE",
                                  "TRANS_ACQUIRED_DISP_CD", "SECURITY_TITLE"])
        tr = tr[tr["TRANS_CODE"].isin(["P", "S"])]
        sub = pd.read_csv(d / "SUBMISSION.tsv", sep="\t", low_memory=False,
                          usecols=["ACCESSION_NUMBER", "FILING_DATE", "ISSUERCIK", "ISSUERTRADINGSYMBOL", "DOCUMENT_TYPE"])
        own = pd.read_csv(d / "REPORTINGOWNER.tsv", sep="\t", low_memory=False,
                          usecols=["ACCESSION_NUMBER", "RPTOWNERCIK", "RPTOWNERNAME", "RPTOWNER_RELATIONSHIP", "RPTOWNER_TITLE"])
        m = tr.merge(sub, on="ACCESSION_NUMBER").merge(own, on="ACCESSION_NUMBER")
        parts.append(m)
    if not parts:
        return pd.DataFrame()
    m = pd.concat(parts, ignore_index=True)
    rel = m["RPTOWNER_RELATIONSHIP"].fillna("").astype(str)
    title = m["RPTOWNER_TITLE"].fillna("").astype(str).str.upper()
    out = pd.DataFrame({
        "symbol": m["ISSUERTRADINGSYMBOL"].astype(str).str.upper().str.strip().str.replace(".", "-", regex=False),
        "issuer_cik": m["ISSUERCIK"], "owner_cik": m["RPTOWNERCIK"], "owner_name": m["RPTOWNERNAME"],
        "relationship": rel, "is_officer": rel.str.contains("Officer"), "is_director": rel.str.contains("Director"),
        "is_ten_pct": rel.str.contains("TenPercentOwner"),
        "is_ceo_cfo": title.str.contains("CHIEF EXECUTIVE|CEO|CHIEF FINANCIAL|CFO", regex=True),
        "trans_date": pd.to_datetime(m["TRANS_DATE"], format="%d-%b-%Y", errors="coerce"),
        "filing_date": pd.to_datetime(m["FILING_DATE"], format="%d-%b-%Y", errors="coerce"),
        "code": m["TRANS_CODE"], "shares": pd.to_numeric(m["TRANS_SHARES"], errors="coerce"),
        "price": pd.to_numeric(m["TRANS_PRICEPERSHARE"], errors="coerce"), "accession": m["ACCESSION_NUMBER"],
        "form": m["DOCUMENT_TYPE"].astype(str),
    })
    out["value"] = out["shares"] * out["price"]
    out = out[(out["is_officer"] | out["is_director"]) & out["filing_date"].notna() & out["trans_date"].notna()]
    out = out[out["value"].notna() & (out["value"] > 0)]
    # a filing may report the same trade in several rows (footnotes); keep one row per (accession, owner, date, code, shares)
    out = out.drop_duplicates(subset=["accession", "owner_cik", "trans_date", "code", "shares", "price"])
    return out.reset_index(drop=True)


def cluster_events(tx: pd.DataFrame, window_days: int = 30, min_insiders: int = 2, min_value: float = 0.0,
                   code: str = "P") -> pd.DataFrame:
    """One event per issuer when >= ``min_insiders`` distinct insiders traded (``code``) within ``window_days``.

    Signal date = filing date of the trade that completes the cluster; the next
    event for the same issuer can only start after that window.
    """
    t = tx[(tx["code"] == code) & (tx["value"] >= min_value)].sort_values("filing_date")
    rows = []
    for sym, g in t.groupby("symbol", sort=False):
        g = g.sort_values("filing_date")
        dates = g["filing_date"].to_numpy()
        owners = g["owner_cik"].to_numpy()
        values = g["value"].to_numpy()
        ceo = g["is_ceo_cfo"].to_numpy()
        last_event = None
        for i in range(len(g)):
            if last_event is not None and (dates[i] - last_event) < pd.Timedelta(days=window_days):
                continue
            lo = dates[i] - pd.Timedelta(days=window_days)
            mask = (dates <= dates[i]) & (dates > lo)
            if len(set(owners[mask])) >= min_insiders:
                rows.append({"symbol": sym, "date": pd.Timestamp(dates[i]), "n_insiders": len(set(owners[mask])),
                             "n_trades": int(mask.sum()), "total_value": float(values[mask].sum()),
                             "ceo_cfo": bool(ceo[mask].any()), "code": code})
                last_event = dates[i]
    return pd.DataFrame(rows)


def single_events(tx: pd.DataFrame, min_value: float = 100_000.0, code: str = "P", gap_days: int = 30) -> pd.DataFrame:
    """Any single open-market trade above ``min_value`` (one event per issuer per ``gap_days``)."""
    t = tx[(tx["code"] == code) & (tx["value"] >= min_value)].sort_values("filing_date")
    rows = []
    for sym, g in t.groupby("symbol", sort=False):
        last = None
        for r in g.itertuples():
            if last is not None and (r.filing_date - last) < pd.Timedelta(days=gap_days):
                continue
            rows.append({"symbol": sym, "date": r.filing_date, "n_insiders": 1, "n_trades": 1, "total_value": r.value,
                         "ceo_cfo": bool(r.is_ceo_cfo), "code": code})
            last = r.filing_date
    return pd.DataFrame(rows)
