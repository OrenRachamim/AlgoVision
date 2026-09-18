"""Per-stock research data for the daily briefs.

Two public Yahoo Finance sources, no API key:

* ``quoteSummary`` (needs a session crumb): price, profile, analyst consensus and price targets,
  recommendation trend, upgrade / downgrade history, earnings history (EPS vs estimate), estimate trend
  and revisions, next earnings date, key statistics.
* the Yahoo Finance news feed for the ticker: RSS (headline, one-paragraph summary, date, link) merged with
  the search endpoint's headlines.

plus SEC EDGAR (no key, User-Agent only): the company's recent 8-K filings with their item codes (earnings
release, officer change, material agreement...), the registrant CIK taken from the SEC's own ticker list.

Everything is cached as one JSON per symbol under ``<cache>/briefs`` and refreshed once a day.
"""

from __future__ import annotations

import html
import json
import logging
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from algovision.data.provider import _DEFAULT_CACHE, _UA

log = logging.getLogger(__name__)

MODULES = ("price,summaryDetail,financialData,recommendationTrend,earningsHistory,earningsTrend,"
           "calendarEvents,defaultKeyStatistics,assetProfile,upgradeDowngradeHistory")
_QS = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}"
_CRUMB = "https://query2.finance.yahoo.com/v1/test/getcrumb"
_RSS = "https://feeds.finance.yahoo.com/rss/2.0/headline"
_SEARCH = "https://query2.finance.yahoo.com/v1/finance/search"


def _unwrap(o):
    """Yahoo wraps numbers as {"raw": x, "fmt": "..."}; keep the raw value, drop empty {} placeholders."""
    if isinstance(o, dict):
        if "raw" in o and set(o) <= {"raw", "fmt", "longFmt"}:
            return o["raw"]
        if not o:
            return None
        return {k: _unwrap(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_unwrap(x) for x in o]
    return o


class YahooSession:
    """requests session with the cookie + crumb Yahoo's quoteSummary endpoint requires."""

    def __init__(self, timeout: int = 30):
        import requests

        self.s = requests.Session()
        self.s.headers.update(_UA)
        self.timeout = timeout
        self._crumb: Optional[str] = None
        self._lock = threading.Lock()

    def crumb(self, refresh: bool = False) -> str:
        with self._lock:
            if self._crumb is None or refresh:
                try:
                    self.s.get("https://fc.yahoo.com", timeout=self.timeout)      # sets the cookie (404 is expected)
                except Exception:  # noqa: BLE001
                    pass
                r = self.s.get(_CRUMB, timeout=self.timeout, headers={"Accept": "*/*"})   # text/plain; the JSON Accept header gets a 406
                r.raise_for_status()
                self._crumb = r.text.strip()
            return self._crumb

    def quote_summary(self, symbol: str) -> Dict:
        for attempt in range(3):
            r = self.s.get(_QS.format(symbol=symbol), params={"modules": MODULES, "crumb": self.crumb(refresh=attempt > 0)},
                           timeout=self.timeout)
            if r.status_code == 200:
                res = (r.json().get("quoteSummary") or {}).get("result") or []
                return _unwrap(res[0]) if res else {}
            if r.status_code in (401, 403, 429):
                time.sleep(1 + attempt)
                continue
            r.raise_for_status()
        return {}

    def news(self, symbol: str, n: int = 12) -> List[Dict]:
        items: Dict[str, Dict] = {}
        try:
            r = self.s.get(_RSS, params={"s": symbol, "region": "US", "lang": "en-US"}, timeout=self.timeout, headers={"Accept": "*/*"})
            if r.status_code == 200:
                for block in re.findall(r"<item>(.*?)</item>", r.text, re.S):
                    g = lambda tag: html.unescape(re.sub(r"<[^>]+>", "", (re.search(rf"<{tag}>(.*?)</{tag}>", block, re.S) or [None, ""])[1])).strip()  # noqa: E731
                    title = g("title")
                    if not title:
                        continue
                    try:
                        when = parsedate_to_datetime(g("pubDate")).astimezone(timezone.utc)
                    except Exception:  # noqa: BLE001
                        when = None
                    items[title] = {"title": title, "summary": re.sub(r"\s+", " ", g("description"))[:600], "publisher": "",
                                    "date": when.strftime("%Y-%m-%d") if when else "", "link": g("link")}
        except Exception as exc:  # noqa: BLE001
            log.warning("%s: rss failed (%s)", symbol, exc)
        try:
            r = self.s.get(_SEARCH, params={"q": symbol, "newsCount": n, "quotesCount": 0}, timeout=self.timeout)
            if r.status_code == 200:
                for x in r.json().get("news", []):
                    title = html.unescape(x.get("title", "")).strip()
                    if not title:
                        continue
                    when = datetime.fromtimestamp(int(x.get("providerPublishTime", 0)), tz=timezone.utc) if x.get("providerPublishTime") else None
                    rec = items.setdefault(title, {"title": title, "summary": "", "publisher": "", "date": "", "link": ""})
                    rec["publisher"] = rec["publisher"] or x.get("publisher", "")
                    rec["date"] = rec["date"] or (when.strftime("%Y-%m-%d") if when else "")
                    rec["link"] = rec["link"] or x.get("link", "")
                    rec["related"] = x.get("relatedTickers", [])
        except Exception as exc:  # noqa: BLE001
            log.warning("%s: news search failed (%s)", symbol, exc)
        out = sorted(items.values(), key=lambda d: d["date"], reverse=True)
        return out[:n]


# what the 8-K item numbers mean (SEC Form 8-K instructions), for the "why it fell" evidence
EIGHT_K_ITEMS = {
    "1.01": "material agreement", "1.02": "agreement terminated", "1.03": "bankruptcy", "2.01": "acquisition or disposal completed",
    "2.02": "results of operations (earnings release)", "2.03": "new debt obligation", "2.04": "debt acceleration",
    "2.05": "restructuring / exit costs", "2.06": "impairment", "3.01": "listing notice", "3.02": "unregistered share sale",
    "4.01": "auditor change", "4.02": "financials not to be relied on (restatement)", "5.01": "change in control",
    "5.02": "officer or director change", "5.03": "bylaw change", "5.07": "shareholder vote", "7.01": "Reg FD disclosure",
    "8.01": "other events",
}
_EDGAR_UA = "AlgoVision research orenrachamim@gmail.com"
_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik:0>10}.json"


_TICKERS = "https://www.sec.gov/files/company_tickers.json"


def sec_cik(symbol: str, cache_dir: Optional[Path] = _DEFAULT_CACHE, max_age_days: float = 7.0) -> Optional[str]:
    """The registrant CIK for ``symbol`` from the SEC's own ticker list (cached), falling back to the package map.
    The package map holds every CIK ever tied to a symbol (right for insider filtering, wrong for 8-K lookups)."""
    import requests

    from algovision.data.insiders_live import cik_map

    p = Path(cache_dir) / "company_tickers.json" if cache_dir else None
    table = None
    if p and p.exists() and time.time() - p.stat().st_mtime < max_age_days * 86400:
        table = json.loads(p.read_text())
    else:
        try:
            r = requests.get(_TICKERS, headers={"User-Agent": _EDGAR_UA, "Accept-Encoding": "gzip, deflate"}, timeout=30)
            if r.status_code == 200:
                table = {v["ticker"]: str(v["cik_str"]) for v in r.json().values()}
                if p:
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(json.dumps(table))
        except Exception as exc:  # noqa: BLE001
            log.warning("sec ticker list failed (%s)", exc)
        if table is None and p and p.exists():
            table = json.loads(p.read_text())
    if table and symbol.upper().replace(".", "-") in table:
        return table[symbol.upper().replace(".", "-")]
    return {v: k for k, v in cik_map().items()}.get(symbol)


def edgar_8k(symbol: str, timeout: int = 30, limit: int = 40, cache_dir: Optional[Path] = _DEFAULT_CACHE) -> List[Dict]:
    """Recent 8-K filings for ``symbol`` from EDGAR submissions: date, items and their meaning. [] when unknown."""
    import requests

    cik = sec_cik(symbol, cache_dir)
    if not cik:
        return []
    for attempt in range(3):
        r = requests.get(_SUBMISSIONS.format(cik=cik), headers={"User-Agent": _EDGAR_UA, "Accept-Encoding": "gzip, deflate"}, timeout=timeout)
        if r.status_code == 200:
            break
        if r.status_code in (403, 429):
            time.sleep(2 + 2 * attempt)
            continue
        return []
    else:
        return []
    f = (r.json().get("filings") or {}).get("recent") or {}
    out = []
    for date, form, items in zip(f.get("filingDate", []), f.get("form", []), f.get("items", [])):
        if form not in ("8-K", "8-K/A"):
            continue
        codes = [c.strip() for c in (items or "").split(",") if c.strip() and c.strip() != "9.01"]
        out.append({"date": date, "form": form, "items": codes, "what": [EIGHT_K_ITEMS.get(c, f"item {c}") for c in codes]})
        if len(out) >= limit:
            break
    time.sleep(0.12)
    return out


class BriefsProvider:
    def __init__(self, cache_dir: Optional[Path] = _DEFAULT_CACHE, max_age_hours: float = 20.0, workers: int = 4,
                 offline: bool = False):
        self._root = Path(cache_dir) if cache_dir else None
        self.cache_dir = self._root / "briefs" if self._root else None
        self.max_age = max_age_hours * 3600
        self.workers = workers
        self.offline = offline
        self._session: Optional[YahooSession] = None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def session(self) -> YahooSession:
        if self._session is None:
            self._session = YahooSession()
        return self._session

    def get(self, symbol: str) -> Dict:
        p = self.cache_dir / f"{symbol}.json" if self.cache_dir else None
        if p and p.exists() and (self.offline or time.time() - p.stat().st_mtime < self.max_age):
            cached = json.loads(p.read_text())
            if not self.offline and cached.get("filings_cik") != sec_cik(symbol, self._root):  # no 8-Ks yet, or fetched for the wrong registrant
                try:
                    cached["filings"] = edgar_8k(symbol, cache_dir=self._root)
                    cached["filings_cik"] = sec_cik(symbol, self._root)
                    p.write_text(json.dumps(cached))
                except Exception as exc:  # noqa: BLE001
                    log.warning("%s: edgar 8-K failed (%s)", symbol, exc)
            return cached
        if self.offline:
            raise RuntimeError(f"{symbol}: no cached brief data")
        data = {"symbol": symbol, "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "profile": self.session.quote_summary(symbol), "news": self.session.news(symbol)}
        try:
            data["filings"] = edgar_8k(symbol, cache_dir=self._root)
            data["filings_cik"] = sec_cik(symbol, self._root)
        except Exception as exc:  # noqa: BLE001
            log.warning("%s: edgar 8-K failed (%s)", symbol, exc)
            data["filings"] = []
        time.sleep(0.2)
        if p:
            p.write_text(json.dumps(data))
        return data

    def get_many(self, symbols: Iterable[str], progress=None) -> Dict[str, Dict]:
        out: Dict[str, Dict] = {}
        symbols = list(symbols)
        if symbols and not self.offline:
            sec_cik(symbols[0], self._root)  # warm the SEC ticker list once, not from every worker
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futs = {ex.submit(self.get, s): s for s in symbols}
            for i, f in enumerate(as_completed(futs), 1):
                s = futs[f]
                try:
                    out[s] = f.result()
                except Exception as exc:  # noqa: BLE001
                    log.warning("%s: %s", s, exc)
                if progress:
                    progress(i, len(symbols))
        return out
