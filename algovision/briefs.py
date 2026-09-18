"""One research brief per stock in the daily report.

Every name in the report tables is a stock that has fallen or just had news. The brief answers, from data:
what the stock has done (price context), why it fell (the largest down days with the evidence found around
each: headlines naming the company that state a cause, 8-K filings, rating cuts, market-wide days; otherwise
"not found", nothing is inferred), the latest news with one-paragraph summaries, what analysts say (consensus, targets, recent
upgrades / downgrades, estimate revisions), what the last report showed (EPS vs estimate, revenue growth,
next report date), the fundamentals (valuation, margins, cash flow, balance sheet), and a **rule-based
read**: signs of a bottom / undecided / still falling. The read is a transparent score over listed
signals, not a forecast; the signals are printed with it so the reader can disagree.
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

from algovision.links import tv

LABELS = {"up": "signs of a bottom (more likely up than down)", "flat": "undecided (no clear base yet)",
          "down": "still falling (more likely down)"}


# ----------------------------------------------------------------------------
# building blocks
# ----------------------------------------------------------------------------
def _pct(v, d=0) -> str:
    return "" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v * 100:+.{d}f}%"


def _num(v, d=1, prefix="") -> str:
    return "" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{prefix}{v:,.{d}f}"


def _money(v) -> str:
    if v is None:
        return ""
    a = abs(v)
    for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
        if a >= div:
            return f"${v / div:,.1f}{unit}"
    return f"${v:,.0f}"


def _date(ts) -> str:
    if ts is None:
        return ""
    if isinstance(ts, (int, float)):
        return dt.datetime.fromtimestamp(int(ts), tz=dt.timezone.utc).strftime("%Y-%m-%d")
    return str(ts)[:10]


def _sentences(text: str, limit: int) -> str:
    """The first sentences of ``text`` that fit in ``limit`` characters (at least one)."""
    out = ""
    for part in text.replace("\n", " ").split(". "):
        cand = (out + ". " if out else "") + part.strip()
        if out and len(cand) > limit:
            break
        out = cand
    return (out[:limit].rstrip(".") + ".") if out else ""


def price_context(df: pd.DataFrame) -> Dict:
    c = df["Close"].astype(float)
    n = len(c)
    last = float(c.iloc[-1])
    ma50 = float(c.tail(50).mean()) if n >= 50 else np.nan
    ma200 = float(c.tail(200).mean()) if n >= 200 else np.nan
    ma50_prev = float(c.iloc[-70:-20].mean()) if n >= 70 else np.nan
    win = c.tail(252)
    hi_i, lo_i = win.idxmax(), win.idxmin()
    ret = c.pct_change()
    drops = ret.tail(90).nsmallest(3)
    vol = df["Volume"].astype(float) if "Volume" in df.columns else pd.Series(np.nan, index=df.index)
    vol_ratio = {}
    for i in drops.index:
        pos = df.index.get_loc(i)
        base = vol.iloc[max(0, pos - 20):pos].median()
        vol_ratio[pd.Timestamp(i).strftime("%Y-%m-%d")] = float(vol.iloc[pos] / base) if base and base == base else None
    delta = c.diff().tail(15)
    up, down = delta.clip(lower=0).mean(), -delta.clip(upper=0).mean()
    rsi = 100 - 100 / (1 + up / down) if down > 0 else 100.0
    low20, low_prev = float(c.tail(20).min()), (float(c.iloc[-40:-20].min()) if n >= 40 else np.nan)
    return {
        "last": last, "ma50": ma50, "ma200": ma200,
        "dist_ma50": last / ma50 - 1 if ma50 == ma50 else np.nan, "dist_ma200": last / ma200 - 1 if ma200 == ma200 else np.nan,
        "ma50_rising": bool(ma50 > ma50_prev) if ma50 == ma50 and ma50_prev == ma50_prev else None,
        "ret_1m": last / float(c.iloc[-22]) - 1 if n > 22 else np.nan, "ret_3m": last / float(c.iloc[-64]) - 1 if n > 64 else np.nan,
        "ret_6m": last / float(c.iloc[-127]) - 1 if n > 127 else np.nan, "ret_1y": last / float(c.iloc[-253]) - 1 if n > 253 else np.nan,
        "high_52w": float(win.max()), "high_date": pd.Timestamp(hi_i).strftime("%Y-%m-%d"), "drawdown": last / float(win.max()) - 1,
        "low_52w": float(win.min()), "low_date": pd.Timestamp(lo_i).strftime("%Y-%m-%d"), "off_low": last / float(win.min()) - 1,
        "new_low_5d": bool(win.tail(5).min() <= float(win.min())),
        "higher_low": bool(low20 > low_prev) if low_prev == low_prev else None, "rsi14": float(rsi),
        "biggest_drops": [(pd.Timestamp(i).strftime("%Y-%m-%d"), float(v)) for i, v in drops.items()],
        "drop_volume": vol_ratio,
    }


# words that make a headline near a down day a plausible stated cause, and what to call it (matched on word boundaries)
CAUSE_WORDS = {
    "earnings": ("earnings", "results", "quarter", "quarterly", "q1", "q2", "q3", "q4", "eps", "revenue", "revenues", "profit", "profits"),
    "guidance": ("guidance", "outlook", "forecast", "warns", "warning", "lowers", "cuts forecast", "cut its", "trims"),
    "rating cut": ("downgrade", "downgrades", "downgraded", "price target", "target cut", "cuts target", "lowers target"),
    "legal/regulatory": ("lawsuit", "probe", "investigation", "sec", "doj", "ftc", "fda", "recall", "antitrust", "regulator", "regulators",
                         "fined", "tariff", "tariffs", "subpoena"),
    "deal/financing": ("acquisition", "acquire", "acquires", "merger", "offering", "convertible", "dilution", "notes", "buyout", "spin-off", "spinoff"),
    "management": ("ceo", "cfo", "resigns", "resignation", "steps down", "departure"),
    "demand/competition": ("demand", "competition", "competitor", "loses", "lost", "contract", "delay", "delays", "slowdown", "weak", "weakness"),
    "price move": ("falls", "fall", "fell", "drops", "drop", "dropped", "plunge", "plunges", "plunged", "tumble", "tumbles", "tumbled", "sinks", "sank",
                   "slides", "slid", "slump", "slumps", "sell-off", "selloff", "52-week low", "why", "down today", "shares down", "slammed"),
}
_CAUSE_RE = {k: re.compile(r"\b(?:" + "|".join(re.escape(w) for w in words) + r")\b") for k, words in CAUSE_WORDS.items()}
RISE_WORDS = ("jump", "jumps", "soars", "soar", "rally", "rallies", "gains", "climbs", "surges", "strength seen", "up today", "rises", "rebound")
# boilerplate that names the company but never states a cause
NOISE_TITLES = ("trending stock", "should you buy", "what to know beyond", "which is the better", "better value stock", "dips more than",
                "outpaces stock market", "settling at", "zacks rank", "moving average", "investors heavily search", "vs.", "here's why you should",
                "is a great choice", "stock is up today", "stock is down today", "buy the dip")


def _company_tokens(symbol: str, name: str) -> List[str]:
    stop = {"the", "inc", "inc.", "corp", "corp.", "corporation", "co", "co.", "company", "plc", "ltd", "holdings", "group", "&", "and", "of"}
    toks = [t.strip(",.") for t in (name or "").split()]
    toks = [t for t in toks if t.lower() not in stop and len(t) > 2]
    return [symbol.upper()] + toks[:2]


_8K_TAGS = {"2.02": "earnings", "5.02": "management", "2.05": "restructuring", "2.06": "impairment", "1.01": "deal/financing",
            "1.02": "deal/financing", "2.01": "deal/financing", "2.03": "deal/financing", "3.02": "deal/financing", "4.02": "restatement",
            "1.03": "bankruptcy", "4.01": "auditor change", "7.01": "company disclosure (8-K)", "8.01": "company disclosure (8-K)"}


def _filings_near(filings: List[Dict], day: str, earn_hist: List[Dict]) -> Tuple[List[str], List[str]]:
    """8-K filings on the drop day or the evening before (release after the close -> drop next session)."""
    d0 = pd.Timestamp(day)
    ev, tags = [], []
    for f in filings or []:
        if not f.get("date"):
            continue
        lag = (d0 - pd.Timestamp(f["date"])).days
        if not 0 <= lag <= 1:
            continue
        codes = [c for c in f.get("items", []) if c in _8K_TAGS]
        if not codes:
            continue
        tags += [_8K_TAGS[c] for c in codes]
        text = f"8-K filed {f['date']}: " + "; ".join(f.get("what") or codes)
        if "2.02" in codes:
            fdate = pd.Timestamp(f["date"])
            q = [h for h in earn_hist or [] if h.get("quarter") and h.get("epsActual") is not None
                 and 0 <= (fdate - pd.Timestamp(int(h["quarter"]), unit="s")).days <= 75]
            if q:
                h = max(q, key=lambda h: h["quarter"])
                text += (f" (quarter to {_date(h['quarter'])}: EPS {_num(h['epsActual'], 2)} vs {_num(h.get('epsEstimate'), 2)} expected"
                         + (f", {_pct(h['surprisePercent'], 1)}" if h.get("surprisePercent") is not None else "") + ")")
        ev.append(text)
    return ev, tags


def decline_reason(symbol: str, name: str, ctx: Dict, news: List[Dict], an: Dict, ea: Dict, bench: Optional[pd.DataFrame] = None,
                   filings: Optional[List[Dict]] = None, earn_hist: Optional[List[Dict]] = None) -> Dict:
    """Evidence for why the stock fell on its largest down days: headlines that name the company and state a cause,
    8-K filings on the day (earnings release, officer change, deal...), rating or target cuts right after, abnormal
    volume, or a market-wide down day. Nothing is inferred beyond that."""
    toks = _company_tokens(symbol, name)
    bench_ret = bench["Close"].astype(float).pct_change() if bench is not None and len(bench) else None
    dated = [x["date"] for x in news if x.get("date")]
    oldest = min(dated) if dated else None
    days, tags = [], []
    for day, r in ctx["biggest_drops"]:
        ev, day_tags = [], []
        scored = []
        for x in [x for x in news if x.get("date") and -1 <= (pd.Timestamp(x["date"]) - pd.Timestamp(day)).days <= 2]:
            title, summ = (x.get("title") or "").lower(), (x.get("summary") or "").lower()
            if not any(t.lower() in f"{title} {summ}" for t in toks) or any(n in title for n in NOISE_TITLES):
                continue
            in_title = [k for k, rx in _CAUSE_RE.items() if rx.search(title)]
            in_summ = [k for k, rx in _CAUSE_RE.items() if rx.search(summ) and k not in in_title]
            causes = [k for k in in_title + in_summ if k != "price move"]
            score = 2 * len([k for k in in_title if k != "price move"]) + len([k for k in in_summ if k != "price move"])
            score += 2 if "price move" in in_title else (1 if "price move" in in_summ else 0)
            if any(w in title for w in RISE_WORDS):
                score -= 3
            if score <= 0 or not in_title:  # the title itself must state a cause or describe the fall
                continue
            scored.append((score, x, causes or ["news"]))
        scored.sort(key=lambda t: (-t[0], abs((pd.Timestamp(t[1]["date"]) - pd.Timestamp(day)).days)))
        fev, ftags = _filings_near(filings or [], day, earn_hist or [])
        ev += fev
        day_tags += ftags
        for _, x, causes in scored[:3]:
            day_tags += causes
            ev.append(f"{x['date']} {x['title']}" + (f" ({x['publisher']})" if x.get("publisher") else "")
                      + (f": {_sentences(x['summary'], 200)}" if x.get("summary") else ""))
        d0 = pd.Timestamp(day)
        cuts = [a for a in an.get("actions", [])
                if a.get("date") and -1 <= (pd.Timestamp(a["date"]) - d0).days <= 3
                and (a.get("action") == "down" or a.get("target_action") == "Lowers")]
        if cuts:
            day_tags.append("rating cut")
            ev.append("rating/target cuts right after: " + "; ".join(
                f"{a['firm']} {'downgrade' if a.get('action') == 'down' else 'target cut'}"
                + (f" {_num(a.get('prior_target'), 0)} -> {_num(a.get('target'), 0)}" if a.get("target") and a.get("prior_target") else "")
                for a in cuts[:3]))
        spy = None
        if bench_ret is not None and d0 in bench_ret.index:
            spy = float(bench_ret.loc[d0])
            if spy <= -0.015:
                day_tags.append("market-wide")
                ev.append(f"market-wide day: SPY {_pct(spy, 1)}")
        vr = ctx.get("drop_volume", {}).get(day)
        volume = f"{vr:.1f}x normal volume" if vr else ""
        if vr and vr >= 2.5 and not day_tags:
            day_tags.append("company event (heavy volume, cause not found)")
        days.append({"day": day, "ret": r, "volume": volume, "spy": spy, "evidence": ev, "tags": list(dict.fromkeys(day_tags)),
                     "before_feed": bool(oldest and (pd.Timestamp(oldest) - d0).days > 2)})
        tags += day_tags
    found = any(d["evidence"] for d in days)
    tags = [t for t in dict.fromkeys(tags) if not t.startswith("company event")]
    return {"found": found, "days": days, "oldest_news": oldest, "cause": ", ".join(tags) if tags else ("heavy volume, cause not found" if any(
        t.startswith("company event") for d in days for t in d["tags"]) else "not found")}


def analyst_view(profile: Dict) -> Dict:
    fd = profile.get("financialData") or {}
    trend = (profile.get("recommendationTrend") or {}).get("trend") or []
    now = next((t for t in trend if t.get("period") == "0m"), {})
    ago = next((t for t in trend if t.get("period") == "-3m"), {})

    def bullish_share(t):
        tot = sum(int(t.get(k) or 0) for k in ("strongBuy", "buy", "hold", "sell", "strongSell"))
        return (int(t.get("strongBuy") or 0) + int(t.get("buy") or 0)) / tot if tot else None

    price = fd.get("currentPrice")
    target = fd.get("targetMeanPrice")
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=90)
    actions = []
    for h in (profile.get("upgradeDowngradeHistory") or {}).get("history") or []:
        when = h.get("epochGradeDate")
        if not when or dt.datetime.fromtimestamp(int(when), tz=dt.timezone.utc) < cutoff:
            continue
        actions.append({"date": _date(when), "firm": h.get("firm", ""), "action": h.get("action", ""),
                        "from": h.get("fromGrade", ""), "to": h.get("toGrade", ""),
                        "target_action": h.get("priceTargetAction", ""), "target": h.get("currentPriceTarget"),
                        "prior_target": h.get("priorPriceTarget")})
    actions.sort(key=lambda a: a["date"], reverse=True)
    key, mean = fd.get("recommendationKey"), fd.get("recommendationMean")
    if (not key or key == "none") and mean is not None:  # Yahoo sometimes ships the mean without the key
        key = "strong_buy" if mean < 1.5 else "buy" if mean < 2.5 else "hold" if mean < 3.5 else "sell" if mean < 4.5 else "strong_sell"
    elif key == "none":
        key = None
    tot = sum(int(now.get(k) or 0) for k in ("strongBuy", "buy", "hold", "sell", "strongSell")) if now else 0
    if tot and mean is None:  # derive the 1-5 mean from the rating counts
        mean = sum(w * int(now.get(k) or 0) for w, k in ((1, "strongBuy"), (2, "buy"), (3, "hold"), (4, "sell"), (5, "strongSell"))) / tot
        if key is None:
            key = "strong_buy" if mean < 1.5 else "buy" if mean < 2.5 else "hold" if mean < 3.5 else "sell" if mean < 4.5 else "strong_sell"
    n = fd.get("numberOfAnalystOpinions") or (tot or None)
    return {
        "key": key, "mean": mean, "n": n,
        "target": target, "target_low": fd.get("targetLowPrice"), "target_high": fd.get("targetHighPrice"),
        "upside": (target / price - 1) if target and price else None,
        "bullish_now": bullish_share(now), "bullish_3m": bullish_share(ago), "counts_now": now,
        "actions": actions[:8],
        "n_up": sum(a["action"] == "up" for a in actions), "n_down": sum(a["action"] == "down" for a in actions),
        "n_target_cuts": sum(a["target_action"] == "Lowers" for a in actions),
        "n_target_raises": sum(a["target_action"] == "Raises" for a in actions),
    }


def earnings_view(profile: Dict) -> Dict:
    hist = (profile.get("earningsHistory") or {}).get("history") or []
    hist = [h for h in hist if h.get("epsActual") is not None]
    hist.sort(key=lambda h: h.get("quarter") or 0)
    last = hist[-1] if hist else {}
    trend = (profile.get("earningsTrend") or {}).get("trend") or []
    q0 = next((t for t in trend if t.get("period") == "0q"), {})
    y0 = next((t for t in trend if t.get("period") == "0y"), {})
    y1 = next((t for t in trend if t.get("period") == "+1y"), {})

    def revision(t, days="30daysAgo"):
        et = t.get("epsTrend") or {}
        cur, ago = et.get("current"), et.get(days)
        return (cur / ago - 1) if cur is not None and ago else None

    def revs(t):
        r = t.get("epsRevisions") or {}
        return int(r.get("upLast30days") or 0), int(r.get("downLast30days") or 0)

    cal = (profile.get("calendarEvents") or {}).get("earnings") or {}
    nxt = (cal.get("earningsDate") or [None])[0]
    fd = profile.get("financialData") or {}
    next_date = _date(nxt)
    if next_date and next_date < dt.date.today().isoformat():
        next_date = ""                                   # Yahoo shows the last date until the next one is announced
    return {
        "last_quarter": _date(last.get("quarter")), "eps_actual": last.get("epsActual"), "eps_est": last.get("epsEstimate"),
        "surprise": last.get("surprisePercent"),
        "beats_4q": sum((h.get("surprisePercent") or 0) > 0 for h in hist[-4:]), "n_4q": len(hist[-4:]),
        "next_date": next_date, "next_is_estimate": bool(cal.get("isEarningsDateEstimate")),
        "q0_eps_est": (q0.get("earningsEstimate") or {}).get("avg"), "q0_growth": (q0.get("earningsEstimate") or {}).get("growth"),
        "q0_rev_growth": (q0.get("revenueEstimate") or {}).get("growth"),
        "y0_growth": (y0.get("earningsEstimate") or {}).get("growth"), "y1_growth": (y1.get("earningsEstimate") or {}).get("growth"),
        "y0_rev_30d": revision(y0), "y0_rev_90d": revision(y0, "90daysAgo"), "q0_rev_30d": revision(q0),
        "y0_up_down_30d": revs(y0), "revenue_growth": fd.get("revenueGrowth"), "earnings_growth": fd.get("earningsGrowth"),
    }


def fundamentals_view(profile: Dict) -> Dict:
    fd, ks, sd = (profile.get(k) or {} for k in ("financialData", "defaultKeyStatistics", "summaryDetail"))
    ap = profile.get("assetProfile") or {}
    fcf = fd.get("freeCashflow")
    mcap = sd.get("marketCap") or (profile.get("price") or {}).get("marketCap")
    return {
        "name": (profile.get("price") or {}).get("longName") or "", "sector": ap.get("sector"), "industry": ap.get("industry"),
        "summary": _sentences(ap.get("longBusinessSummary") or "", 320), "market_cap": mcap,
        "pe": sd.get("trailingPE"), "forward_pe": sd.get("forwardPE") or ks.get("forwardPE"), "peg": ks.get("pegRatio"),
        "ev_rev": ks.get("enterpriseToRevenue"), "ev_ebitda": ks.get("enterpriseToEbitda"), "pb": ks.get("priceToBook"),
        "gross_margin": fd.get("grossMargins"), "op_margin": fd.get("operatingMargins"), "net_margin": fd.get("profitMargins"),
        "fcf": fcf, "fcf_yield": (fcf / mcap) if fcf is not None and mcap else None,
        "debt_to_equity": (fd.get("debtToEquity") / 100) if fd.get("debtToEquity") is not None else None,
        "cash": fd.get("totalCash"), "debt": fd.get("totalDebt"), "current_ratio": fd.get("currentRatio"), "roe": fd.get("returnOnEquity"),
        "dividend_yield": sd.get("dividendYield"), "short_pct": ks.get("shortPercentOfFloat"), "beta": ks.get("beta"),
        "chg_52w": ks.get("52WeekChange"), "spx_52w": ks.get("SandP52WeekChange"),
    }


def verdict(ctx: Dict, an: Dict, ea: Dict, fu: Dict, insider_buying: bool = False) -> Tuple[str, float, List[str]]:
    """Transparent score: each signal adds or subtracts, the list says which fired."""
    score, why = 0.0, []

    def add(cond, pts, text):
        nonlocal score
        if cond:
            score += pts
            why.append(f"{'+' if pts > 0 else ''}{pts:g} {text}")

    d50 = ctx.get("dist_ma50")
    add(d50 == d50 and d50 > 0, 1, "price above its 50-day average")
    add(d50 == d50 and d50 <= 0, -1, "price below its 50-day average")
    add(ctx.get("ma50_rising") is True, 1, "50-day average turning up")
    add(ctx.get("higher_low") is True, 1, "higher low over the last 20 bars than the 20 before")
    add(ctx.get("new_low_5d"), -1, "new 52-week low within the last 5 bars")
    key = (an.get("key") or "").lower()
    add(key in ("strong_buy", "buy"), 1, f"analyst consensus {key.replace('_', ' ')} ({an.get('n') or '?'} analysts)")
    add(key in ("sell", "underperform", "strong_sell"), -1, f"analyst consensus {key.replace('_', ' ')}")
    up = an.get("upside")
    add(up is not None and up > 0.20, 1, f"mean price target {_pct(up)} above the price")
    add(up is not None and up < 0.05, -1, f"mean price target only {_pct(up)} from the price")
    add(an.get("n_up", 0) > an.get("n_down", 0), 1, f"more upgrades than downgrades in 90 days ({an.get('n_up')} vs {an.get('n_down')})")
    add(an.get("n_down", 0) > an.get("n_up", 0), -1, f"more downgrades than upgrades in 90 days ({an.get('n_down')} vs {an.get('n_up')})")
    cuts, raises = an.get("n_target_cuts", 0), an.get("n_target_raises", 0)
    add(cuts >= raises + 3, -1, f"analysts cutting price targets ({cuts} cuts vs {raises} raises in 90 days)")
    add(raises >= cuts + 3, 1, f"analysts raising price targets ({raises} raises vs {cuts} cuts in 90 days)")
    ud = ea.get("y0_up_down_30d") or (0, 0)
    add(ud[1] >= ud[0] + 3, -0.5, f"estimate revisions mostly down ({ud[0]} up / {ud[1]} down in 30 days)")
    add(ud[0] >= ud[1] + 3, 0.5, f"estimate revisions mostly up ({ud[0]} up / {ud[1]} down in 30 days)")
    r30 = ea.get("y0_rev_30d")
    add(r30 is not None and r30 > 0.01, 1, f"current-year EPS estimate raised {_pct(r30, 1)} in 30 days")
    add(r30 is not None and r30 < -0.01, -1, f"current-year EPS estimate cut {_pct(r30, 1)} in 30 days")
    sp = ea.get("surprise")
    add(sp is not None and sp > 0, 0.5, f"last quarter beat estimates ({_pct(sp, 1)})")
    add(sp is not None and sp < 0, -1, f"last quarter missed estimates ({_pct(sp, 1)})")
    rg = ea.get("revenue_growth")
    add(rg is not None and rg > 0, 0.5, f"revenue growing ({_pct(rg)} yoy)")
    add(rg is not None and rg < 0, -0.5, f"revenue shrinking ({_pct(rg)} yoy)")
    fcf = fu.get("fcf")
    add(fcf is not None and fcf > 0, 0.5, "positive free cash flow")
    add(fcf is not None and fcf < 0, -0.5, "negative free cash flow")
    de = fu.get("debt_to_equity")
    add(de is not None and de > 2, -0.5, f"high leverage (debt/equity {_num(de)})")
    pe, fpe = fu.get("pe"), fu.get("forward_pe")
    add(bool(pe and fpe and fpe < pe), 0.5, f"forward P/E {_num(fpe, 0)} below trailing {_num(pe, 0)} (earnings expected to grow)")
    add(insider_buying, 1, "insiders bought (in today's insider table)")
    label = "up" if score >= 3 else "down" if score <= -2 else "flat"
    return label, score, why


def _news_near(news: List[Dict], day: str, window: int = 3) -> List[Dict]:
    d0 = pd.Timestamp(day)
    out = []
    for x in news:
        if not x.get("date"):
            continue
        if abs((pd.Timestamp(x["date"]) - d0).days) <= window:
            out.append(x)
    return out


# ----------------------------------------------------------------------------
# markdown
# ----------------------------------------------------------------------------
def brief_markdown(symbol: str, tables: List[str], ctx: Dict, an: Dict, ea: Dict, fu: Dict, news: List[Dict],
                   label: str, score: float, why: List[str], why_fell: Optional[Dict] = None) -> str:
    md = [f"## {tv(symbol)} {fu.get('name') or ''}".rstrip(), ""]
    md.append(f"*In today's tables: {', '.join(tables) if tables else '-'}. {fu.get('sector') or ''} / {fu.get('industry') or ''}.*")
    if fu.get("summary"):
        md.append(f"*{fu['summary'].rstrip('.')}.*")
    md.append("")
    md.append(f"**Read: {LABELS[label]}** (score {score:+g}). Signals: " + ("; ".join(why) if why else "none") + ".")
    md.append("")
    md.append("**Where the stock is.** "
              f"Last {ctx['last']:.2f}, {_pct(ctx['drawdown'])} from the 52-week high ({ctx['high_52w']:.2f} on {ctx['high_date']}), "
              f"{_pct(ctx['off_low'])} above the 52-week low ({ctx['low_52w']:.2f} on {ctx['low_date']}). "
              f"1m {_pct(ctx['ret_1m'])}, 3m {_pct(ctx['ret_3m'])}, 6m {_pct(ctx['ret_6m'])}, 1y {_pct(ctx['ret_1y'])}; "
              f"vs 50-day {_pct(ctx['dist_ma50'])}, vs 200-day {_pct(ctx['dist_ma200'])}; RSI(14) {ctx['rsi14']:.0f}."
              + (f" 52-week change {_pct(fu['chg_52w'])} vs S&P 500 {_pct(fu['spx_52w'])}." if fu.get("chg_52w") is not None else ""))
    md.append("")
    why = why_fell or {"found": False, "days": [], "cause": "not found"}
    md.append("**Why it fell.** " + (
        f"Cause found in the data ({why['cause']}). Largest down days in the last 90 bars and the evidence around each:" if why["found"]
        else "No cause found in the data: no headline naming the company with a stated reason within 2 days of the largest down days, "
             "no 8-K filing (earnings release, officer change, deal) on those days, no rating or target cut right after, and no "
             "market-wide sell-off. Largest down days in the last 90 bars:"))
    for d in why["days"]:
        extra = ", ".join(x for x in (d["volume"], f"SPY {_pct(d['spy'], 1)}" if d.get("spy") is not None else "") if x)
        line = f"- {d['day']}: {_pct(d['ret'], 1)}" + (f" ({extra})" if extra else "")
        if d["evidence"]:
            md.append(line + ":")
            md += [f"  - {e}" for e in d["evidence"]]
        elif d.get("before_feed"):
            md.append(line + f". No cause found for this day (before the news feed starts on {why['oldest_news']}; "
                      "only 8-K filings, rating changes and the market were checked).")
        else:
            md.append(line + ". No cause found for this day.")
    if news:
        md.append("")
        md.append("Latest news:")
        for x in news[:6]:
            line = f"- {x['date']} {x['title']}" + (f" ({x['publisher']})" if x.get("publisher") else "")
            if x.get("summary"):
                line += f": {x['summary'][:280]}"
            md.append(line)
    md.append("")
    cn = an.get("counts_now") or {}
    md.append("**What analysts say.** "
              + (f"Consensus **{str(an['key']).replace('_', ' ')}** ({an.get('n') or '?'} analysts"
                 + (f", mean rating {_num(an['mean'])} on a 1-5 scale" if an.get("mean") is not None else "") + "); "
                 if an.get("key") else "No consensus data; ")
              + (f"strong buy {cn.get('strongBuy', 0)}, buy {cn.get('buy', 0)}, hold {cn.get('hold', 0)}, sell {cn.get('sell', 0)}, strong sell {cn.get('strongSell', 0)}"
                 + (f" (bullish share {an['bullish_now'] * 100:.0f}% now vs {an['bullish_3m'] * 100:.0f}% three months ago)"
                    if an.get("bullish_now") is not None and an.get("bullish_3m") is not None else "") + ". " if cn else "")
              + (f"Mean target {_num(an['target'], 2)} ({_pct(an['upside'])} from the price"
                 + (f"; range {_num(an['target_low'], 2)}-{_num(an['target_high'], 2)}"
                    if an.get("target_low") is not None and an.get("target_high") is not None else "") + "). "
                 if an.get("target") else ""))
    if an.get("actions"):
        md.append(f"Last 90 days: {an.get('n_up', 0)} upgrades, {an.get('n_down', 0)} downgrades, "
                  f"{an.get('n_target_raises', 0)} target raises, {an.get('n_target_cuts', 0)} target cuts.")
        for a in an["actions"][:6]:
            t, pt = a.get("target"), a.get("prior_target")
            tgt = f", target {_num(pt, 0)} -> {_num(t, 0)}" if t and pt and t != pt else (f", target {_num(t, 0)}" if t else "")
            verb = {"up": "upgrades", "down": "downgrades", "main": "maintains", "reit": "reiterates", "init": "initiates"}.get(a.get("action"), a.get("action") or "")
            frm, to = a.get("from") or "", a.get("to") or ""
            grade = f"{frm} -> {to}" if frm and frm != to else to
            md.append(f"- {a.get('date') or ''} {a.get('firm') or ''}: {verb} {grade}{tgt}")
    md.append("")
    md.append("**Last report and estimates.** "
              + (f"Quarter to {ea.get('last_quarter') or '?'}: EPS {_num(ea['eps_actual'], 2)}"
                 + (f" vs {_num(ea['eps_est'], 2)} expected ({_pct(ea.get('surprise'), 1)})" if ea.get("eps_est") is not None else "")
                 + f"; beat in {ea.get('beats_4q', 0)} of the last {ea.get('n_4q', 0)} quarters. "
                 if ea.get("eps_actual") is not None else "No earnings history. ")
              + (f"Revenue {_pct(ea.get('revenue_growth'))} yoy, earnings {_pct(ea.get('earnings_growth'))} yoy (latest quarter). "
                 if ea.get("revenue_growth") is not None else "")
              + (f"Next report {ea.get('next_date') or '(date not yet announced)'}"
                 f"{' (estimated date)' if ea.get('next_is_estimate') and ea.get('next_date') else ''}: EPS {_num(ea['q0_eps_est'], 2)} expected "
                 f"({_pct(ea.get('q0_growth'))} yoy), revenue {_pct(ea.get('q0_rev_growth'))} yoy. " if ea.get("q0_eps_est") is not None else "")
              + (f"Current-year EPS estimate {_pct(ea.get('y0_rev_30d'), 1)} in 30 days, {_pct(ea.get('y0_rev_90d'), 1)} in 90 days "
                 f"({(ea.get('y0_up_down_30d') or (0, 0))[0]} up / {(ea.get('y0_up_down_30d') or (0, 0))[1]} down revisions); "
                 f"growth expected {_pct(ea.get('y0_growth'))} this year, {_pct(ea.get('y1_growth'))} next. "
                 if ea.get("y0_rev_30d") is not None else ""))
    md.append("")
    md.append("**Fundamentals.** "
              f"Market cap {_money(fu.get('market_cap'))}; P/E {_num(fu.get('pe'))} trailing, {_num(fu.get('forward_pe'))} forward, PEG {_num(fu.get('peg'), 2)}; "
              f"EV/revenue {_num(fu.get('ev_rev'))}, EV/EBITDA {_num(fu.get('ev_ebitda'))}, P/B {_num(fu.get('pb'))}. "
              f"Margins: gross {_pct(fu.get('gross_margin'))}, operating {_pct(fu.get('op_margin'))}, net {_pct(fu.get('net_margin'))}; ROE {_pct(fu.get('roe'))}. "
              f"Free cash flow {_money(fu.get('fcf'))} (yield {_pct(fu.get('fcf_yield'), 1)}); cash {_money(fu.get('cash'))}, debt {_money(fu.get('debt'))}, "
              f"debt/equity {_num(fu.get('debt_to_equity'), 2)}, current ratio {_num(fu.get('current_ratio'), 2)}. "
              + (f"Dividend yield {_pct(fu['dividend_yield'], 1)}. " if fu.get("dividend_yield") else "")
              + (f"Short interest {_pct(fu['short_pct'], 1)} of float. " if fu.get("short_pct") is not None else "")
              + (f"Beta {_num(fu['beta'], 2)}." if fu.get("beta") is not None else ""))
    md.append("")
    return "\n".join(md)


def build_brief(symbol: str, df: pd.DataFrame, data: Dict, tables: List[str], insider_buying: bool = False,
                bench: Optional[pd.DataFrame] = None) -> Tuple[Dict, str]:
    profile, news = data.get("profile") or {}, data.get("news") or []
    ctx = price_context(df)
    an, ea, fu = analyst_view(profile), earnings_view(profile), fundamentals_view(profile)
    label, score, why = verdict(ctx, an, ea, fu, insider_buying)
    why_fell = decline_reason(symbol, fu.get("name") or "", ctx, news, an, ea, bench, filings=data.get("filings") or [],
                              earn_hist=(profile.get("earningsHistory") or {}).get("history") or [])
    row = {"symbol": symbol, "tables": ", ".join(tables), "read": LABELS[label].split(" (")[0], "score": score, "why fell": why_fell["cause"],
           "last": ctx["last"], "from 52w high": ctx["drawdown"], "vs MA50": ctx["dist_ma50"], "vs MA200": ctx["dist_ma200"],
           "consensus": (an.get("key") or "").replace("_", " "), "analysts": an.get("n"), "target upside": an.get("upside"),
           "up/down 90d": f"{an.get('n_up', 0)}/{an.get('n_down', 0)}", "EPS est 30d": ea.get("y0_rev_30d"),
           "last surprise": ea.get("surprise"), "next report": ea.get("next_date")}
    return row, brief_markdown(symbol, tables, ctx, an, ea, fu, news, label, score, why, why_fell)


def summary_table(rows: List[Dict]) -> str:
    if not rows:
        return "none\n"
    d = pd.DataFrame(rows)
    order = {"signs of a bottom": 0, "undecided": 1, "still falling": 2}
    d = d.sort_values(["read", "score"], key=lambda s: s.map(order) if s.name == "read" else -s).reset_index(drop=True)
    out = pd.DataFrame({
        "symbol": d["symbol"].map(tv), "in tables": d["tables"], "read": d["read"], "score": d["score"].map(lambda v: f"{v:+g}"),
        "why fell": d["why fell"] if "why fell" in d else "",
        "last": d["last"].map(lambda v: f"{v:.2f}"), "from 52w high": d["from 52w high"].map(_pct), "vs MA50": d["vs MA50"].map(_pct),
        "consensus": d["consensus"], "analysts": d["analysts"].map(lambda v: "" if v is None or pd.isna(v) else f"{int(v)}"),
        "target upside": d["target upside"].map(_pct), "up/down 90d": d["up/down 90d"],
        "EPS est 30d": d["EPS est 30d"].map(lambda v: _pct(v, 1)), "last surprise": d["last surprise"].map(lambda v: _pct(v, 1)),
        "next report": d["next report"],
    })
    return out.to_markdown(index=False) + "\n"


def write_briefs(out_dir: Path, today: str, symbols: Iterable[str], frames: Dict[str, pd.DataFrame], tables: Dict[str, List[str]],
                 insider_symbols: Iterable[str] = (), cache_dir: Optional[Path] = None, workers: int = 4, offline: bool = False,
                 progress=None, bench: Optional[pd.DataFrame] = None) -> Tuple[Path, List[Dict]]:
    """Write ``briefs_<today>.md`` / ``briefs_latest.md`` for every symbol and return the summary rows."""
    from algovision.data.briefs_data import BriefsProvider
    from algovision.data.provider import _DEFAULT_CACHE

    out_dir = Path(out_dir)
    symbols = [s for s in dict.fromkeys(symbols) if s in frames]
    provider = BriefsProvider(cache_dir=cache_dir or _DEFAULT_CACHE, workers=workers, offline=offline)
    data = provider.get_many(symbols, progress=progress)
    insiders = set(insider_symbols)
    rows, parts = [], []
    for s in symbols:
        if s not in data:
            parts.append(f"## {tv(s)}\n\nno data\n")
            continue
        try:
            row, md = build_brief(s, frames[s], data[s], tables.get(s, []), insider_buying=s in insiders, bench=bench)
        except Exception as exc:  # one bad profile must not sink the whole file
            parts.append(f"## {tv(s)}\n\nbrief unavailable: {exc}\n")
            continue
        rows.append(row)
        parts.append(md)
    head = [f"# AlgoVision stock briefs - {today}\n",
            f"One brief per name in today's report tables ({len(symbols)} stocks): where the stock is, why it fell (only evidence "
            "found in the data: headlines naming the company near the largest down days, rating cuts, market-wide days; otherwise "
            "\"not found\"), what analysts "
            "say, the last report and the estimates, the fundamentals, and a rule-based read (signs of a bottom / undecided / "
            "still falling) whose signals are listed so it can be checked. Data: Yahoo Finance (analysts, estimates, "
            "statistics, news). Systematic screens, not investment advice.\n",
            "## Summary\n", summary_table(rows)]
    text = "\n".join(head + parts)
    path = out_dir / f"briefs_{today}.md"
    path.write_text(text, encoding="utf-8")
    (out_dir / "briefs_latest.md").write_text(text, encoding="utf-8")
    return path, rows
