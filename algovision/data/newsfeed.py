"""Extra, key-free sources for what moved a stock and how investors feel about it.

* Google News RSS search (``news.google.com/rss/search``): headlines with date and publisher, for the last year and
  for a window around one day (``after:``/``before:``). Google offers the feed for personal, non-commercial feed
  readers; this is a personal research tool and the feed is fetched once per symbol and day, then cached.
* StockTwits public symbol stream: the last 30 messages, each tagged Bullish / Bearish by its author (or untagged).

Everything is cached under the AlgoVision cache directory: a year's headlines and the StockTwits stream for
``max_age_hours``, the headlines around a past day forever (the past does not change). Every fetch is best effort:
on any error the source returns nothing and the caller carries on.
"""

from __future__ import annotations

import html
import json
import logging
import re
import threading
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import quote_plus

from algovision.data.provider import _DEFAULT_CACHE

log = logging.getLogger(__name__)

_UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
_GOOGLE = "https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
_STOCKTWITS = "https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
_lock = threading.Lock()
_last_google = [0.0]
_SUFFIXES = {"inc", "inc.", "corp", "corp.", "corporation", "co", "co.", "company", "plc", "ltd", "ltd.", "holdings", "group",
             "the", "&", "and", "of", "n.v.", "nv", "sa", "s.a.", "ag", "se", "llc", "lp", "l.p.", "trust", "incorporated", "limited"}


def company_query(symbol: str, name: str) -> str:
    """The quoted company name Google News is asked for: the first two meaningful words of the name (``"Norwegian Cruise"``),
    the ticker when no name is known."""
    toks = [t.strip(",.") for t in (name or "").replace("(", " ").replace(")", " ").split()]
    toks = [t for t in toks if t.lower() not in _SUFFIXES and len(t) > 1]
    core = " ".join(toks[:2]) if toks else symbol
    return f'"{core}"'


def _cache_path(root: Optional[Path], kind: str, key: str) -> Optional[Path]:
    if not root:
        return None
    d = Path(root) / kind
    d.mkdir(parents=True, exist_ok=True)
    return d / (re.sub(r"[^A-Za-z0-9_.-]", "_", key) + ".json")


def _read_cache(p: Optional[Path], max_age: Optional[float]) -> Optional[list]:
    if p is None or not p.exists():
        return None
    if max_age is not None and time.time() - p.stat().st_mtime > max_age:
        return None
    try:
        return json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return None


def parse_google_rss(xml_text: str) -> List[Dict]:
    """RSS items -> [{date, title, publisher, summary, link, source}] (title without the trailing ' - Publisher')."""
    out: List[Dict] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return out
    for it in root.findall(".//item"):
        title = html.unescape(it.findtext("title") or "").strip()
        src = it.find("source")
        publisher = (src.text or "").strip() if src is not None else ""
        if publisher and title.endswith(" - " + publisher):
            title = title[: -len(publisher) - 3].rstrip()
        elif " - " in title and not publisher:
            title, publisher = title.rsplit(" - ", 1)
        when = it.findtext("pubDate") or ""
        try:
            date = parsedate_to_datetime(when).astimezone(timezone.utc).strftime("%Y-%m-%d")
        except Exception:  # noqa: BLE001
            date = ""
        if not title or not date:
            continue
        out.append({"date": date, "title": title, "publisher": publisher, "summary": "", "link": it.findtext("link") or "",
                    "source": "google"})
    return out


def google_news(query: str, cache_dir: Optional[Path] = _DEFAULT_CACHE, max_age_hours: Optional[float] = 20.0,
                timeout: int = 30, offline: bool = False) -> List[Dict]:
    """Headlines for a Google News search query (at most 100), newest first. ``max_age_hours=None`` caches forever."""
    import requests

    p = _cache_path(cache_dir, "news", query)
    cached = _read_cache(p, None if max_age_hours is None else max_age_hours * 3600)
    if cached is not None or offline:
        return cached or []
    with _lock:                                    # be gentle: one Google request every half second, process-wide
        wait = 0.5 - (time.time() - _last_google[0])
        if wait > 0:
            time.sleep(wait)
        try:
            r = requests.get(_GOOGLE.format(q=quote_plus(query)), headers={"User-Agent": _UA}, timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            log.warning("google news %s: %s", query, exc)
            return []
        finally:
            _last_google[0] = time.time()
    if r.status_code != 200:
        log.warning("google news %s: HTTP %s", query, r.status_code)
        return []
    items = parse_google_rss(r.text)
    items.sort(key=lambda x: x["date"], reverse=True)
    if p:
        p.write_text(json.dumps(items))
    return items


def headlines_year(symbol: str, name: str, cache_dir: Optional[Path] = _DEFAULT_CACHE, offline: bool = False) -> List[Dict]:
    """Up to 100 headlines about the company from the last year (Google's relevance ranking, so recent months dominate)."""
    return google_news(f"{company_query(symbol, name)} {symbol} stock when:1y", cache_dir, 20.0, offline=offline)


def headlines_around(symbol: str, name: str, day: str, window: int = 2, cache_dir: Optional[Path] = _DEFAULT_CACHE,
                     offline: bool = False) -> List[Dict]:
    """Headlines about the company from ``day - 1`` to ``day + window`` (cached forever once the window has passed)."""
    import datetime as dt

    d0 = dt.date.fromisoformat(day)
    after, before = (d0 - dt.timedelta(days=1)).isoformat(), (d0 + dt.timedelta(days=window + 1)).isoformat()
    settled = dt.date.today() > d0 + dt.timedelta(days=window + 2)
    return google_news(f"{company_query(symbol, name)} after:{after} before:{before}", cache_dir, None if settled else 6.0, offline=offline)


def stocktwits(symbol: str, cache_dir: Optional[Path] = _DEFAULT_CACHE, max_age_hours: float = 20.0, timeout: int = 20,
               offline: bool = False) -> Dict:
    """The last 30 StockTwits messages on the symbol, summarised: bullish / bearish / untagged counts, watchers."""
    import requests

    p = _cache_path(cache_dir, "stocktwits", symbol)
    cached = _read_cache(p, max_age_hours * 3600)
    if cached is not None:
        return cached[0] if isinstance(cached, list) else cached
    if offline:
        return {}
    try:
        r = requests.get(_STOCKTWITS.format(symbol=symbol), headers={"User-Agent": _UA}, timeout=timeout)
        if r.status_code != 200:
            log.warning("stocktwits %s: HTTP %s", symbol, r.status_code)
            return {}
        j = r.json()
    except Exception as exc:  # noqa: BLE001
        log.warning("stocktwits %s: %s", symbol, exc)
        return {}
    msgs = j.get("messages") or []
    bull = sum(1 for m in msgs if ((m.get("entities") or {}).get("sentiment") or {}).get("basic") == "Bullish")
    bear = sum(1 for m in msgs if ((m.get("entities") or {}).get("sentiment") or {}).get("basic") == "Bearish")
    dates = [m.get("created_at", "")[:10] for m in msgs if m.get("created_at")]
    out = {"n": len(msgs), "bullish": bull, "bearish": bear, "watchers": (j.get("symbol") or {}).get("watchlist_count"),
           "from": min(dates) if dates else None, "to": max(dates) if dates else None,
           "fetched": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if p:
        p.write_text(json.dumps(out))
    time.sleep(0.3)
    return out
