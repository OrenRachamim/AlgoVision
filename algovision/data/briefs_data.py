"""Per-stock research data for the daily briefs.

Two public Yahoo Finance sources, no API key:

* ``quoteSummary`` (needs a session crumb): price, profile, analyst consensus and price targets,
  recommendation trend, upgrade / downgrade history, earnings history (EPS vs estimate), estimate trend
  and revisions, next earnings date, key statistics.
* the Yahoo Finance news feed for the ticker: RSS (headline, one-paragraph summary, date, link) merged with
  the search endpoint's headlines.

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


class BriefsProvider:
    def __init__(self, cache_dir: Optional[Path] = _DEFAULT_CACHE, max_age_hours: float = 20.0, workers: int = 4,
                 offline: bool = False):
        self.cache_dir = Path(cache_dir) / "briefs" if cache_dir else None
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
            return json.loads(p.read_text())
        if self.offline:
            raise RuntimeError(f"{symbol}: no cached brief data")
        data = {"symbol": symbol, "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "profile": self.session.quote_summary(symbol), "news": self.session.news(symbol)}
        time.sleep(0.2)
        if p:
            p.write_text(json.dumps(data))
        return data

    def get_many(self, symbols: Iterable[str], progress=None) -> Dict[str, Dict]:
        out: Dict[str, Dict] = {}
        symbols = list(symbols)
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
