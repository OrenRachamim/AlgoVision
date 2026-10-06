"""The stock's story along the time axis: five chapters (5y, 2y, 1y, 6m, 1m), each told from the chart.

Each chapter covers its own stretch of time (five to two years back, two to one, one year to six months, six
months to one, the last month) at its own resolution: the closes are cut into legs (zig-zag swings larger than
the chapter's threshold), and every leg is told with what is known to have happened inside it, in date order:

* earnings releases (8-K item 2.02) with the market's reaction, EPS vs the estimate (Yahoo, last four quarters)
  and the quarter's revenue / EPS against the year before (SEC XBRL company facts, ten years);
* material 8-K events (agreement, acquisition completed, officer change, restructuring, impairment...) with the
  reaction;
* the largest single days of the stretch with the headline that named the company that day (Google News,
  any past date) or "no headline found";
* the volume of the leg against the stretch's normal volume, the S&P 500 over the same leg, and (last year)
  analyst upgrades / downgrades.

Nothing is inferred: a leg with no event inside it is told as a move with no recorded cause.  The annual arc of
revenue and EPS (XBRL) opens the five-year chapter.  Rendered in English (briefs) and Hebrew (wedge file).
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

log = logging.getLogger(__name__)

# (key, bars back where the chapter starts, bars back where it ends, swing threshold, big-day threshold, max big days)
CHAPTERS = [("5y", 1260, 504, 0.20, 0.06, 3), ("2y", 504, 252, 0.15, 0.05, 3), ("1y", 252, 126, 0.10, 0.04, 3),
            ("6m", 126, 22, 0.07, 0.035, 3), ("1m", 22, 0, 0.03, 0.025, 3)]
MAX_LEGS = 6
CORPORATE_ITEMS = {"1.01": "material agreement", "1.02": "agreement terminated", "1.03": "bankruptcy", "2.01": "acquisition or disposal completed",
                   "2.03": "new debt", "2.05": "restructuring", "2.06": "impairment", "4.02": "restatement", "5.01": "change in control",
                   "5.02": "officer or director change"}
CORPORATE_HE = {"1.01": "הסכם מהותי", "1.02": "ביטול הסכם", "1.03": "פשיטת רגל", "2.01": "השלמת רכישה או מכירה", "2.03": "חוב חדש",
                "2.05": "ארגון מחדש", "2.06": "ירידת ערך", "4.02": "הצגה מחדש של דוחות", "5.01": "שינוי שליטה", "5.02": "חילופי נושא משרה או דירקטור"}
_FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:0>10}.json"
_REV_TAGS = ("Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RevenueFromContractWithCustomerIncludingAssessedTax",
             "SalesRevenueNet", "RevenuesNetOfInterestExpense", "TotalRevenuesAndOtherIncome", "InterestAndDividendIncomeOperating")
# generic words of company names that must not match a headline on their own
_GENERIC = {"companies", "company", "international", "group", "holdings", "technologies", "technology", "industries", "systems", "services",
            "solutions", "brands", "global", "financial", "energy", "capital", "health", "american", "national", "united", "general", "first",
            "corporation", "resources", "partners", "entertainment", "communications", "the"}
_EPS_TAGS = ("EarningsPerShareDiluted", "EarningsPerShareBasic")


# ----------------------------------------------------------------------------
# data
# ----------------------------------------------------------------------------
def long_frame(symbol: str, df: pd.DataFrame, cache_dir: Optional[Path] = None) -> pd.DataFrame:
    """The cached ten-year daily frame spliced with the newer bars of ``df`` (the daily two-year frame)."""
    try:
        from algovision.data.provider import DataProvider
        p = DataProvider(cache_dir=cache_dir, offline=True) if cache_dir else DataProvider(offline=True)
        old = p.get(symbol, "10y", "1d")
    except Exception:  # noqa: BLE001
        return df
    if old is None or not len(old):
        return df
    new = df[df.index > old.index[-1]]
    out = pd.concat([old, new]) if len(new) else old
    return out[~out.index.duplicated(keep="last")].sort_index()


def edgar_facts(symbol: str, cache_dir: Optional[Path] = None, max_age_days: float = 7.0, offline: bool = False,
                timeout: int = 60) -> Dict:
    """Quarterly and annual revenue / EPS / net income from SEC XBRL company facts (deduplicated by XBRL frame).
    Returns {"quarters": [{"frame", "end", "revenue", "eps", "net_income"}...], "years": [...]} (ascending)."""
    from algovision.data.briefs_data import _EDGAR_UA, sec_cik
    from algovision.data.provider import _DEFAULT_CACHE

    root = Path(cache_dir) if cache_dir else _DEFAULT_CACHE
    p = root / "facts" / f"{symbol}.json" if root else None
    if p and p.exists() and (offline or time.time() - p.stat().st_mtime < max_age_days * 86400):
        return json.loads(p.read_text())
    if offline:
        return {"quarters": [], "years": []}
    cik = sec_cik(symbol, root)
    if not cik:
        return {"quarters": [], "years": []}
    import requests
    try:
        r = requests.get(_FACTS_URL.format(cik=cik), headers={"User-Agent": _EDGAR_UA, "Accept-Encoding": "gzip, deflate"}, timeout=timeout)
        r.raise_for_status()
        facts = (r.json().get("facts") or {}).get("us-gaap") or {}
    except Exception as exc:  # noqa: BLE001
        log.warning("%s: company facts failed (%s)", symbol, exc)
        return json.loads(p.read_text()) if p and p.exists() else {"quarters": [], "years": []}
    time.sleep(0.12)

    def frames(tags, unit_pref):
        out: Dict[str, Tuple[str, float]] = {}
        for tag in tags:                                   # first tag wins for a frame; later tags fill the gaps
            units = (facts.get(tag) or {}).get("units") or {}
            vals = next((units[u] for u in unit_pref if u in units), None)
            if not vals:
                continue
            for v in vals:
                fr = v.get("frame")
                if fr and fr not in out and v.get("val") is not None:
                    out[fr] = (v.get("end"), float(v["val"]))
        return out

    rev, eps, ni = frames(_REV_TAGS, ("USD",)), frames(_EPS_TAGS, ("USD/shares",)), frames(("NetIncomeLoss",), ("USD",))
    keys = sorted(set(rev) | set(eps) | set(ni))
    rows = [{"frame": k, "end": (rev.get(k) or eps.get(k) or ni.get(k))[0], "revenue": (rev.get(k) or (None, None))[1],
             "eps": (eps.get(k) or (None, None))[1], "net_income": (ni.get(k) or (None, None))[1]} for k in keys]
    quarters = sorted([r for r in rows if "Q" in r["frame"]], key=lambda r: r["end"])
    years = sorted([r for r in rows if "Q" not in r["frame"]], key=lambda r: r["end"])
    # the fourth quarter is usually reported only inside the annual figure: derive it as annual minus Q1..Q3
    by_frame = {q["frame"]: q for q in quarters}
    for y in years:
        yr = y["frame"]
        if f"{yr}Q4" in by_frame or any(q["end"] == y["end"] for q in quarters):
            continue
        q123 = [by_frame.get(f"{yr}Q{k}") for k in (1, 2, 3)]
        if any(q is None for q in q123):
            continue
        q4 = {"frame": f"{yr}Q4", "end": y["end"], "derived": True}
        for key in ("revenue", "eps", "net_income"):
            vals = [q.get(key) for q in q123]
            q4[key] = (y[key] - sum(vals)) if y.get(key) is not None and all(v is not None for v in vals) else None
        if any(q4[k] is not None for k in ("revenue", "eps", "net_income")):
            quarters.append(q4)
    quarters.sort(key=lambda r: r["end"])
    data = {"quarters": quarters, "years": years, "fetched": time.strftime("%Y-%m-%d")}
    if p:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data))
    return data


def _yoy(rows: List[Dict], frame: str, key: str) -> Optional[float]:
    """Change against the same frame a year earlier (CY2024Q3 -> CY2023Q3, CY2024 -> CY2023)."""
    cur = next((r for r in rows if r["frame"] == frame), None)
    if not cur or cur.get(key) is None:
        return None
    y = int(frame[2:6])
    prev_frame = f"CY{y - 1}{frame[6:]}"
    prev = next((r for r in rows if r["frame"] == prev_frame), None)
    if not prev or prev.get(key) is None:
        return None
    base = prev[key]
    if key == "eps":
        return (cur[key] - base) / abs(base) if base else None
    return cur[key] / base - 1 if base else None


def quarter_before(facts: Dict, day: str, max_days: int = 100) -> Optional[Dict]:
    """The latest quarter whose period ended at most ``max_days`` before ``day`` (the one a filing on ``day`` reports)."""
    d0 = pd.Timestamp(day)
    best = None
    for q in facts.get("quarters") or []:
        end = pd.Timestamp(q["end"])
        if end <= d0 and (d0 - end).days <= max_days:
            best = q
    if best is None:
        return None
    return {**best, "revenue_yoy": _yoy(facts["quarters"], best["frame"], "revenue"), "eps_yoy": _yoy(facts["quarters"], best["frame"], "eps")}


# ----------------------------------------------------------------------------
# chart legs
# ----------------------------------------------------------------------------
def zigzag(close: np.ndarray, threshold: float) -> List[int]:
    """Pivot indices (first and last bar included) of swings larger than ``threshold``."""
    n = len(close)
    if n < 3:
        return list(range(n))
    pivots = [0]
    direction = 0                      # +1 rising from the last pivot, -1 falling, 0 unknown
    ext_i = 0
    for i in range(1, n):
        p = close[i]
        if direction >= 0 and p >= close[ext_i] and direction == 1:
            ext_i = i
        elif direction <= 0 and p <= close[ext_i] and direction == -1:
            ext_i = i
        elif direction == 0:
            if p / close[0] - 1 >= threshold:
                direction, ext_i = 1, i
            elif p / close[0] - 1 <= -threshold:
                direction, ext_i = -1, i
            continue
        if direction == 1 and p / close[ext_i] - 1 <= -threshold:
            pivots.append(ext_i)
            direction, ext_i = -1, i
        elif direction == -1 and p / close[ext_i] - 1 >= threshold:
            pivots.append(ext_i)
            direction, ext_i = 1, i
    if pivots[-1] != n - 1:
        if ext_i != pivots[-1] and ext_i != n - 1 and direction != 0:
            pivots.append(ext_i)
        pivots.append(n - 1)
    return pivots


def legs_for(close: np.ndarray, threshold: float, max_legs: int = MAX_LEGS) -> List[Tuple[int, int]]:
    """(start, end) index pairs; the threshold is raised until the stretch has at most ``max_legs`` legs."""
    thr = threshold
    for _ in range(5):
        piv = zigzag(close, thr)
        if len(piv) - 1 <= max_legs:
            break
        thr *= 1.4
    # a trailing stub smaller than half the threshold is the end of the previous leg, not a leg of its own
    if len(piv) >= 3 and abs(close[piv[-1]] / close[piv[-2]] - 1) < thr / 2:
        piv = piv[:-2] + [piv[-1]]
    return [(piv[k], piv[k + 1]) for k in range(len(piv) - 1)]


# ----------------------------------------------------------------------------
# events
# ----------------------------------------------------------------------------
def _reaction(ldf: pd.DataFrame, day: str, vol_ratio: pd.Series) -> Optional[Dict]:
    """The session on ``day`` or the next one, whichever moved more (a release after the close hits the next session)."""
    idx = ldf.index
    pos = idx.searchsorted(pd.Timestamp(day))
    cands = [k for k in (pos, pos + 1) if 0 < k < len(idx) and (idx[k] - pd.Timestamp(day)).days <= 4]
    if not cands:
        return None
    c = ldf["Close"].to_numpy(dtype=float)
    k = max(cands, key=lambda j: abs(c[j] / c[j - 1] - 1))
    return {"day": idx[k].strftime("%Y-%m-%d"), "ret": float(c[k] / c[k - 1] - 1), "vol": (None if pd.isna(vol_ratio.iloc[k]) else float(vol_ratio.iloc[k]))}


def _pick_headline(symbol: str, name: str, items: List[Dict], day: str, up: bool) -> Optional[Dict]:
    from algovision.briefs import _CAUSE_RE, _MARKET_RE, NOISE_TITLES, RISE_WORDS, _company_tokens
    toks = [t for t in _company_tokens(symbol, name) if t.lower() not in _GENERIC and len(t) > 2]
    best, best_score = None, 1                                   # a headline must state a cause or describe the stock's move
    for x in items:
        title = (x.get("title") or "").strip()
        tl = title.lower()
        if not title or not x.get("date") or not any(t.lower() in tl for t in toks) or any(n in tl for n in NOISE_TITLES):
            continue
        if not -1 <= (pd.Timestamp(x["date"]) - pd.Timestamp(day)).days <= 2:
            continue
        causes = [k for k, rx in _CAUSE_RE.items() if rx.search(tl) and k != "price move"]
        score = 2 * len(causes) + (1 if _MARKET_RE.search(title) else 0)
        rises, falls = any(w in tl for w in RISE_WORDS), bool(_CAUSE_RE["price move"].search(tl))
        score += 2 if (up and rises) or (not up and falls) else 0
        score -= 3 if (up and falls and not rises) or (not up and rises and not falls) else 0
        if score > best_score:
            best, best_score = {"date": x["date"], "title": title, "publisher": x.get("publisher") or "", "causes": causes}, score
    return best


def collect_events(symbol: str, name: str, ldf: pd.DataFrame, data: Dict, facts: Dict, bench: Optional[pd.DataFrame],
                   headlines_around: Optional[Callable[[str], List[Dict]]], first_day: str, big_thr: float, max_big: int,
                   window_start: int, window_end: int) -> List[Dict]:
    """Dated events inside [window_start, window_end) of ``ldf``: earnings, corporate 8-Ks, the largest single days."""
    profile = data.get("profile") or {}
    earn_hist = (profile.get("earningsHistory") or {}).get("history") or []
    vol = ldf["Volume"].astype(float)
    vol_ratio = vol / vol.rolling(20).median().shift(1)
    c = ldf["Close"].to_numpy(dtype=float)
    idx = ldf.index
    d_start, d_end = idx[window_start].strftime("%Y-%m-%d"), idx[window_end - 1].strftime("%Y-%m-%d")
    spy_ret = bench["Close"].astype(float).pct_change() if bench is not None and len(bench) else None
    events: List[Dict] = []
    taken_days = set()
    for f in data.get("filings") or []:
        fd = f.get("date")
        if not fd or not (d_start <= fd <= d_end):
            continue
        items = f.get("items") or []
        rx = _reaction(ldf, fd, vol_ratio)
        if rx is None:
            continue
        if "2.02" in items:
            ev = {"kind": "earnings", "date": fd, **rx}
            fdate = pd.Timestamp(fd)
            q = [h for h in earn_hist if h.get("quarter") and h.get("epsActual") is not None
                 and 0 <= (fdate - pd.Timestamp(int(h["quarter"]), unit="s")).days <= 75]
            if q:
                h = max(q, key=lambda h: h["quarter"])
                ev.update({"eps": h["epsActual"], "eps_est": h.get("epsEstimate"), "surprise": h.get("surprisePercent")})
            qb = quarter_before(facts, fd)
            if qb:
                ev.update({"revenue": qb.get("revenue"), "revenue_yoy": qb.get("revenue_yoy"), "eps_yoy": qb.get("eps_yoy"), "frame": qb["frame"]})
            events.append(ev)
            taken_days.add(rx["day"])
        codes = [k for k in items if k in CORPORATE_ITEMS]
        # an officer change or new debt is told only when the market reacted; the heavy items always
        if codes and (abs(rx["ret"]) >= 0.02 or any(k not in ("5.02", "2.03") for k in codes)):
            events.append({"kind": "corporate", "date": fd, "codes": codes, **rx})
            taken_days.add(rx["day"])
    # the largest single days of the stretch that no filing explains
    rets = pd.Series(c, index=idx).pct_change()
    seg = rets.iloc[window_start:window_end]
    big = seg[seg.abs() >= big_thr].abs().sort_values(ascending=False)
    n_fetch = 0
    for day, _ in big.items():
        ds = day.strftime("%Y-%m-%d")
        if ds in taken_days:          # the session after a release can be a second big day of its own (continued selling)
            continue
        if n_fetch >= max_big:
            break
        n_fetch += 1
        r = float(rets.loc[day])
        ev = {"kind": "bigday", "date": ds, "day": ds, "ret": r, "vol": (None if pd.isna(vol_ratio.loc[day]) else float(vol_ratio.loc[day])),
              "spy": (float(spy_ret.loc[day]) if spy_ret is not None and day in spy_ret.index and pd.notna(spy_ret.loc[day]) else None)}
        if headlines_around is not None and ds >= first_day:
            try:
                ev["headline"] = _pick_headline(symbol, name, headlines_around(ds) or [], ds, r > 0)
            except Exception:  # noqa: BLE001
                ev["headline"] = None
        events.append(ev)
        taken_days.add(ds)
    # two filings that hit the same session (earnings release plus an officer change) are one event
    merged: Dict[str, Dict] = {}
    for ev in sorted(events, key=lambda e: (e["day"], e["kind"] != "earnings")):
        prev = merged.get(ev["day"])
        if prev is None:
            merged[ev["day"]] = ev
        elif prev["kind"] == "earnings" and ev["kind"] == "corporate":
            prev["codes"] = ev["codes"]
    events = list(merged.values())
    if spy_ret is not None:
        for ev in events:
            if ev.get("spy") is None:
                d = pd.Timestamp(ev["day"])
                ev["spy"] = float(spy_ret.loc[d]) if d in spy_ret.index and pd.notna(spy_ret.loc[d]) else None
    events.sort(key=lambda e: e["date"])
    return events


# ----------------------------------------------------------------------------
# the story
# ----------------------------------------------------------------------------
def build_story(symbol: str, df: pd.DataFrame, data: Dict, bench: Optional[pd.DataFrame] = None, cache_dir: Optional[Path] = None,
                offline: bool = False, headlines_around: Optional[Callable[[str], List[Dict]]] = None) -> Dict:
    """The chapters, each with its legs and the events inside them, plus the annual arc. Pure data; see the renderers."""
    ldf = long_frame(symbol, df, cache_dir)
    ldf = ldf[ldf["Close"].notna()]
    name = ((data.get("profile") or {}).get("price") or {}).get("longName") or ""
    try:
        facts = edgar_facts(symbol, cache_dir, offline=offline)
    except Exception:  # noqa: BLE001
        facts = {"quarters": [], "years": []}
    n = len(ldf)
    c = ldf["Close"].to_numpy(dtype=float)
    vol = ldf["Volume"].astype(float).to_numpy()
    idx = ldf.index
    first_day = idx[0].strftime("%Y-%m-%d")
    spy = bench["Close"].astype(float).reindex(idx).ffill() if bench is not None and len(bench) else None
    an_actions = []
    try:
        from algovision.briefs import analyst_view
        an_actions = analyst_view(data.get("profile") or {}).get("actions_1y") or []
    except Exception:  # noqa: BLE001
        pass
    chapters = []
    for key, back0, back1, thr, big_thr, max_big in CHAPTERS:
        s, e = max(0, n - 1 - back0), n - back1            # [s, e) bars of this chapter; the last chapter ends at the last bar
        if e - s < 5 or n - 1 - back0 < -back0 * 0.75:     # less than a quarter of the chapter has data: skip it
            chapters.append({"key": key, "missing": True, "first_day": first_day})
            continue
        seg = c[s:e]
        legs = legs_for(seg, thr)
        vol_norm = float(np.nanmedian(vol[s:e])) if np.isfinite(vol[s:e]).any() else np.nan
        events = collect_events(symbol, name, ldf, data, facts, bench, headlines_around, first_day, big_thr, max_big, s, e)
        out_legs = []
        for a, b in legs:
            i0, i1 = s + a, s + b
            d0, d1 = idx[i0].strftime("%Y-%m-%d"), idx[i1].strftime("%Y-%m-%d")
            leg_vol = float(np.nanmean(vol[i0 + 1:i1 + 1]) / vol_norm) if vol_norm and i1 > i0 else np.nan
            inside = [ev for ev in events if d0 < ev["day"] <= d1] if a > 0 else [ev for ev in events if d0 <= ev["day"] <= d1]
            if len(inside) > 5:                                  # keep the five that moved the stock most, in date order
                inside = sorted(sorted(inside, key=lambda ev: -abs(ev.get("ret") or 0))[:5], key=lambda ev: ev["date"])
            ups = sum(1 for x in an_actions if x.get("date") and d0 < x["date"] <= d1 and x.get("action") == "up")
            downs = sum(1 for x in an_actions if x.get("date") and d0 < x["date"] <= d1 and x.get("action") == "down")
            out_legs.append({"start": d0, "end": d1, "p0": float(c[i0]), "p1": float(c[i1]), "ret": float(c[i1] / c[i0] - 1), "bars": i1 - i0,
                             "vol_ratio": leg_vol, "spy": (float(spy.iloc[i1] / spy.iloc[i0] - 1) if spy is not None and pd.notna(spy.iloc[i0]) and spy.iloc[i0] else None),
                             "events": inside[:5], "upgrades": ups, "downgrades": downs})
        chapters.append({"key": key, "start": idx[s].strftime("%Y-%m-%d"), "end": idx[e - 1].strftime("%Y-%m-%d"), "p_start": float(c[s]),
                         "p_end": float(c[e - 1]), "ret": float(c[e - 1] / c[s] - 1), "legs": out_legs, "threshold": thr,
                         "spy": (float(spy.iloc[e - 1] / spy.iloc[s] - 1) if spy is not None and pd.notna(spy.iloc[s]) and spy.iloc[s] else None)})
    hi_i, lo_i = int(np.nanargmax(c[-min(n, 1260):])) + max(0, n - 1260), int(np.nanargmin(c[-min(n, 1260):])) + max(0, n - 1260)
    years = [y for y in (facts.get("years") or []) if y.get("revenue") is not None or y.get("eps") is not None]
    arc = None
    if len(years) >= 2:
        span = [y for y in years if y["end"] >= (pd.Timestamp(idx[-1]) - pd.DateOffset(years=5, months=3)).strftime("%Y-%m-%d")] or years[-5:]
        if len(span) >= 2:
            arc = {"first": span[0], "last": span[-1], "n": len(span),
                   "rev_growth": (span[-1]["revenue"] / span[0]["revenue"] - 1) if span[0].get("revenue") and span[-1].get("revenue") else None,
                   "eps_first": span[0].get("eps"), "eps_last": span[-1].get("eps"),
                   "years": [{"frame": y["frame"], "end": y["end"], "revenue": y.get("revenue"), "eps": y.get("eps"),
                              "revenue_yoy": _yoy(years, y["frame"], "revenue")} for y in span]}
    return {"symbol": symbol, "name": name, "first_day": first_day, "last_day": idx[-1].strftime("%Y-%m-%d"), "last": float(c[-1]),
            "high": {"date": idx[hi_i].strftime("%Y-%m-%d"), "price": float(c[hi_i])}, "low": {"date": idx[lo_i].strftime("%Y-%m-%d"), "price": float(c[lo_i])},
            "chapters": chapters, "arc": arc}


# ----------------------------------------------------------------------------
# rendering
# ----------------------------------------------------------------------------
def _pct(v, d=0) -> str:
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return ""
    x = round(v * 100, d)
    return f"{x:+.{d}f}%" if x != 0 else f"{0:.{d}f}%"


def _abs_pct(v, d=0) -> str:
    return _pct(abs(v), d).lstrip("+")


def _money(v) -> str:
    if v is None:
        return ""
    a = abs(v)
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
        if a >= div:
            return f"${v / div:.1f}{unit}"
    return f"${v:,.0f}"


def _vol_phrase(vr, lang) -> str:
    if vr is None or not np.isfinite(vr):
        return ""
    if vr >= 1.5:
        return f" on {vr:.1f}x the usual volume" if lang == "en" else f" במחזור של פי {vr:.1f} מהרגיל"
    if vr <= 0.7:
        return " on thin volume" if lang == "en" else " במחזורים דלילים"
    return ""


CHAPTER_TITLE = {"en": {"5y": "Five years back (to two years ago)", "2y": "Two years back (to one year ago)", "1y": "One year back (to six months ago)",
                        "6m": "Six months back (to one month ago)", "1m": "The last month"},
                 "he": {"5y": "חמש שנים אחורה (עד לפני שנתיים)", "2y": "שנתיים אחורה (עד לפני שנה)", "1y": "שנה אחורה (עד לפני חצי שנה)",
                        "6m": "חצי שנה אחורה (עד לפני חודש)", "1m": "החודש האחרון"}}


def _event_text(ev: Dict, lang: str) -> str:
    r, v = ev.get("ret"), ev.get("vol")
    move = (f"the stock {_pct(r, 1)}" if lang == "en" else f"המניה {_pct(r, 1)}") + (f" ({v:.1f}x volume)" if v and v >= 1.5 and lang == "en" else
                                                                                   (f" (מחזור פי {v:.1f})" if v and v >= 1.5 else ""))
    spy = ev.get("spy")
    if spy is not None and abs(spy) >= 0.015 and ev["kind"] != "bigday":
        move += f" (S&P {_pct(spy, 1)} that day)" if lang == "en" else f" (S&P {_pct(spy, 1)} באותו יום)"
    if ev["kind"] == "earnings":
        codes = ev.get("codes") or []
        extra = ("; " + "; ".join((CORPORATE_ITEMS if lang == "en" else CORPORATE_HE).get(k, k) for k in codes)) if codes else ""
        parts = []
        if ev.get("eps") is not None:
            parts.append((f"EPS {ev['eps']:.2f} vs {ev['eps_est']:.2f} expected ({_pct(ev.get('surprise'), 1)})" if ev.get("eps_est") is not None else f"EPS {ev['eps']:.2f}")
                         if lang == "en" else
                         (f"רווח למניה {ev['eps']:.2f} מול {ev['eps_est']:.2f} צפוי ({_pct(ev.get('surprise'), 1)})" if ev.get("eps_est") is not None else f"רווח למניה {ev['eps']:.2f}"))
        if ev.get("revenue_yoy") is not None:
            parts.append(f"revenue {_pct(ev['revenue_yoy'])} y/y" if lang == "en" else f"הכנסות {_pct(ev['revenue_yoy'])} לעומת אשתקד")
        if ev.get("eps_yoy") is not None and ev.get("eps") is None:
            parts.append(f"EPS {_pct(ev['eps_yoy'])} y/y" if lang == "en" else f"רווח למניה {_pct(ev['eps_yoy'])} לעומת אשתקד")
        detail = ((", ".join(parts)) if parts else ("no figures on file" if lang == "en" else "ללא נתונים")) + extra
        return (f"{ev['date']} earnings release ({detail}): {move}" if lang == "en" else f"{ev['date']} דוח רבעוני ({detail}): {move}")
    if ev["kind"] == "corporate":
        what = "; ".join((CORPORATE_ITEMS if lang == "en" else CORPORATE_HE).get(k, k) for k in ev["codes"])
        return f"{ev['date']} 8-K {what}: {move}" if lang == "en" else f"{ev['date']} דיווח 8-K ({what}): {move}"
    h = ev.get("headline")
    spy = ev.get("spy")
    mkt = ""
    if spy is not None and abs(spy) >= 0.015:
        mkt = f" (S&P {_pct(spy, 1)} that day)" if lang == "en" else f" (S&P {_pct(spy, 1)} באותו יום)"
    if h:
        src = f" ({h['publisher']})" if h.get("publisher") else ""
        return f"{ev['date']} {move}{mkt}: \"{h['title']}\"{src}" if lang == "en" else f"{ev['date']} {move}{mkt}: \"{h['title']}\"{src}"
    return (f"{ev['date']} {move}{mkt}, no headline found" if lang == "en" else f"{ev['date']} {move}{mkt}, לא נמצאה כותרת")


def _leg_text(leg: Dict, lang: str, first: bool) -> str:
    r = leg["ret"]
    up = r >= 0
    if lang == "en":
        verb = ("Rose" if up else "Fell") if first else ("then rose" if up else "then fell")
        head = (f"{verb} {_abs_pct(r)} from {leg['start']} ({leg['p0']:.2f}) to {leg['end']} ({leg['p1']:.2f}) over {leg['bars']} sessions"
                if first else f"{verb} {_abs_pct(r)} to {leg['end']} ({leg['p1']:.2f}) over {leg['bars']} sessions")
        head += _vol_phrase(leg.get("vol_ratio"), lang)
        if leg.get("spy") is not None:
            head += f", S&P {_pct(leg['spy'])} meanwhile"
        if leg.get("upgrades") or leg.get("downgrades"):
            head += f", {leg['upgrades']} upgrades / {leg['downgrades']} downgrades"
    else:
        verb = ("עלייה" if up else "ירידה")
        head = (f"{verb} של {_abs_pct(r)} מ-{leg['start']} ({leg['p0']:.2f}) עד {leg['end']} ({leg['p1']:.2f}) ב-{leg['bars']} ימי מסחר"
                if first else f"אחר כך {verb} של {_abs_pct(r)} עד {leg['end']} ({leg['p1']:.2f}) ב-{leg['bars']} ימי מסחר")
        head += _vol_phrase(leg.get("vol_ratio"), lang)
        if leg.get("spy") is not None:
            head += f", ה-S&P {_pct(leg['spy'])} באותה תקופה"
        if leg.get("upgrades") or leg.get("downgrades"):
            head += f", {leg['upgrades']} העלאות דירוג / {leg['downgrades']} הורדות"
    evs = leg.get("events") or []
    if not evs:
        return head + ("; no earnings, filing or big day recorded inside this move." if lang == "en" else "; בלי דוח, דיווח או יום חריג בתוך המהלך הזה.")
    return head + (". Inside it: " if lang == "en" else ". בתוכה: ") + "; ".join(_event_text(e, lang) for e in evs) + "."


def story_markdown(story: Dict, lang: str = "en") -> List[str]:
    if not story or not story.get("chapters"):
        return []
    en = lang == "en"
    md = ["**The story, along the time axis.** " + (
        "Each chapter covers its own stretch at its own resolution; the legs are the chart's swings, and inside every leg only what the "
        "data recorded: earnings releases (8-K, EPS vs estimate, revenue vs the year before from SEC XBRL), material 8-K events, the "
        "largest days with the headline that named the company (Google News) or \"no headline found\", volume vs normal, the S&P over the same leg."
        if en else
        "כל פרק מכסה קטע זמן משלו ברזולוציה משלו; הרגליים הן התנודות של הגרף, ובתוך כל רגל רק מה שהנתונים תיעדו: דוחות רבעוניים "
        "(8-K, רווח למניה מול התחזית, הכנסות מול השנה הקודמת מ-XBRL של ה-SEC), אירועי 8-K מהותיים, הימים הגדולים עם הכותרת שהזכירה את החברה "
        "(Google News) או \"לא נמצאה כותרת\", מחזור מול הרגיל, וה-S&P באותה רגל.")]
    arc = story.get("arc")
    if arc:
        f, l = arc["first"], arc["last"]
        yrs = ", ".join(f"FY{y['end'][:7]}: {_money(y['revenue'])}" + (f" ({_pct(y['revenue_yoy'])})" if y.get("revenue_yoy") is not None else "")
                        for y in arc["years"] if y.get("revenue") is not None)
        parts = []
        if yrs:
            parts.append((f"revenue {yrs}" if en else f"הכנסות {yrs}"))
        if arc.get("eps_first") is not None and arc.get("eps_last") is not None:
            parts.append(f"diluted EPS {arc['eps_first']:.2f} -> {arc['eps_last']:.2f}" if en else f"רווח מדולל למניה {arc['eps_first']:.2f} ← {arc['eps_last']:.2f}")
        if parts:
            md.append((f"*Annual arc (SEC filings, fiscal years ending {f['end'][:4]}-{l['end'][:4]}):* " if en else
                       f"*הקשת השנתית (דיווחי SEC, שנות כספים המסתיימות {f['end'][:4]}-{l['end'][:4]}):* ") + "; ".join(parts) + ".")
    for ch in story["chapters"]:
        title = CHAPTER_TITLE[lang][ch["key"]]
        if ch.get("missing"):
            md.append(f"- **{title}.** " + (f"No price data before {ch['first_day']}." if en else f"אין נתוני מחיר לפני {ch['first_day']}."))
            continue
        intro = (f"From {ch['start']} ({ch['p_start']:.2f}) to {ch['end']} ({ch['p_end']:.2f}): {_pct(ch['ret'])}"
                 + (f" (S&P {_pct(ch['spy'])})" if ch.get("spy") is not None else "") + ". "
                 if en else
                 f"מ-{ch['start']} ({ch['p_start']:.2f}) עד {ch['end']} ({ch['p_end']:.2f}): {_pct(ch['ret'])}"
                 + (f" (S&P {_pct(ch['spy'])})" if ch.get("spy") is not None else "") + ". ")
        body = " ".join(_leg_text(leg, lang, k == 0) for k, leg in enumerate(ch["legs"]))
        md.append(f"- **{title}.** {intro}{body}")
    hi, lo = story["high"], story["low"]
    md.append((f"*Today {story['last']:.2f}: {_pct(story['last'] / hi['price'] - 1)} from the five-year high ({hi['price']:.2f} on {hi['date']}), "
               f"{_pct(story['last'] / lo['price'] - 1)} from the five-year low ({lo['price']:.2f} on {lo['date']}).*"
               if en else
               f"*היום {story['last']:.2f}: {_pct(story['last'] / hi['price'] - 1)} מהשיא של חמש השנים ({hi['price']:.2f} ב-{hi['date']}), "
               f"{_pct(story['last'] / lo['price'] - 1)} מהשפל של חמש השנים ({lo['price']:.2f} ב-{lo['date']}).*"))
    md.append("")
    return md
