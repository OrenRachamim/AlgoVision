"""Investor concerns and sentiment for one stock, from data only.

* Concerns: the themes of the negative headlines about the company over the last year (Google News), counted, with
  the headlines around the largest down days weighted double, and the headlines themselves as examples so the
  reader can check every theme. A theme is named only when headlines carry it; nothing is inferred.
* Sentiment: what analysts, short sellers, estimate revisions, the retail crowd (StockTwits) and the news tone say,
  each as a number, plus a transparent label (negative / mixed / positive) over listed signals.
"""

from __future__ import annotations

import datetime as dt
import re
from typing import Dict, List, Optional, Tuple

# theme -> (English label, Hebrew label, words matched on word boundaries in the headline)
THEMES: Dict[str, Tuple[str, str, Tuple[str, ...]]] = {
    "china": ("China / international markets", "סין ושווקים בינלאומיים",
              ("china", "chinese", "greater china", "asia", "europe", "international", "overseas", "japan", "emerging markets")),
    "tariffs": ("tariffs / trade", "מכסים וסחר", ("tariff", "tariffs", "trade war", "duties", "sanctions", "import")),
    "demand": ("weak demand / consumer", "ביקוש חלש וצרכן",
               ("demand", "sales drop", "sales fall", "sales decline", "weak sales", "consumer", "consumers", "spending", "traffic",
                "bookings", "volumes", "slowdown", "slump in sales", "orders")),
    "guidance": ("guidance / outlook cut", "הורדת תחזית", ("guidance", "outlook", "forecast", "forecasts", "warns", "warning", "trims", "cuts forecast",
                                                          "lowers", "expects", "expected to")),
    "margins": ("margins / costs", "שולי רווח ועלויות", ("margin", "margins", "costs", "cost", "inflation", "fuel", "oil", "freight", "wages",
                                                        "expenses", "pricing", "profitability")),
    "competition": ("competition / market share", "תחרות ואובדן נתח שוק",
                    ("competition", "competitor", "competitors", "rival", "rivals", "market share", "share loss", "losing share", "upstart")),
    "management": ("management / turnaround", "הנהלה ותפנית",
                   ("ceo", "cfo", "turnaround", "restructuring", "layoffs", "job cuts", "reorganization", "strategy", "reset", "leadership",
                    "resigns", "steps down", "shake-up", "overhaul")),
    "inventory": ("inventory / discounting", "מלאי והנחות", ("inventory", "inventories", "promotions", "promotional", "discounting", "discounts",
                                                            "markdowns", "clearance", "excess stock")),
    "debt": ("debt / financing", "חוב ומימון", ("debt", "leverage", "offering", "dilution", "convertible", "refinance", "refinancing", "liquidity",
                                               "cash burn", "bankruptcy", "credit rating", "junk")),
    "legal": ("legal / regulatory", "משפטי ורגולטורי", ("lawsuit", "probe", "investigation", "sec", "doj", "ftc", "fda", "recall", "antitrust",
                                                       "regulator", "regulators", "fined", "subpoena", "settlement", "class action")),
    "miss": ("earnings miss", "החמצת תחזיות", ("misses", "missed", "miss", "disappoints", "disappointing", "disappointed", "below estimates",
                                             "falls short", "worse than expected", "shortfall")),
    "downgrade": ("analyst downgrades", "הורדות דירוג", ("downgrade", "downgrades", "downgraded", "price target cut", "cuts price target",
                                                        "lowers price target", "slashes target", "slash price targets", "underperform", "sell rating")),
    "macro": ("macro / market", "מאקרו ושוק", ("recession", "interest rates", "rates", "fed", "macro", "selloff", "sell-off", "market rout",
                                              "tariff fears", "trade fears", "economy")),
    "geopolitics": ("geopolitics", "גיאופוליטיקה", ("war", "conflict", "middle east", "geopolitical", "ukraine", "israel", "iran", "red sea")),
    "technology": ("technology disruption / AI", "שיבוש טכנולוגי ו-AI", ("ai", "artificial intelligence", "disruption", "disrupt", "obsolete",
                                                                        "automation")),
    "product": ("product / delays", "מוצר ועיכובים", ("delay", "delays", "delayed", "defect", "safety", "quality", "supply chain", "shortage")),
}
_THEME_RE = {k: re.compile(r"\b(?:" + "|".join(re.escape(w) for w in v[2]) + r")\b", re.I) for k, v in THEMES.items()}
NEGATIVE = ("drop", "drops", "dropped", "fall", "falls", "fell", "plunge", "plunges", "plunged", "slump", "slumps", "slumped", "cut", "cuts",
            "weak", "weakness", "miss", "misses", "missed", "decline", "declines", "declined", "tumble", "tumbles", "tumbled", "sink", "sinks",
            "sank", "low", "lows", "warns", "warning", "hurt", "hurts", "worst", "hated", "sell", "downgrade", "downgrades", "downgraded",
            "slash", "slashes", "slashed", "struggle", "struggles", "struggling", "problem", "problems", "concern", "concerns", "fear",
            "fears", "risk", "risks", "worry", "worries", "pressure", "loses", "lost", "loss", "losses", "layoffs", "disappoint", "disappoints",
            "disappointing", "bearish", "trap", "crash", "crashes", "collapse", "tank", "tanks", "tanking", "lower", "lowers", "trims", "sinking",
            "sliding", "slides", "slid", "rout", "selloff", "sell-off", "bleak", "dismal", "trouble", "troubles", "woes", "pain", "exodus")
POSITIVE = ("jump", "jumps", "jumped", "surge", "surges", "surged", "rally", "rallies", "rallied", "gain", "gains", "gained", "beat", "beats",
            "record", "upgrade", "upgrades", "upgraded", "raises", "raised", "strong", "strength", "rebound", "rebounds", "soar", "soars",
            "soared", "climb", "climbs", "climbed", "buy", "bullish", "outperform", "opportunity", "recovery", "recovers", "momentum", "boost",
            "boosts", "wins", "win", "growth", "growing", "improves", "improving", "upside", "undervalued", "bargain", "cheap")
_NEG_RE = re.compile(r"\b(?:" + "|".join(NEGATIVE) + r")\b", re.I)
_POS_RE = re.compile(r"\b(?:" + "|".join(POSITIVE) + r")\b", re.I)
NOISE = ("should you buy", "vs.", "which is the better", "better value", "trending stock", "zacks", "moving average", "here's why you should",
         "is a great choice", "sale on", "sneakers", "colorway", "collab", "collaboration", "release date", "outfit", "style", "deal on")


def _tone(title: str) -> int:
    """-1 negative, +1 positive, 0 neutral, from the headline's words."""
    neg, pos = len(_NEG_RE.findall(title)), len(_POS_RE.findall(title))
    return -1 if neg > pos else (1 if pos > neg else 0)


def _relevant(title: str, tokens: List[str]) -> bool:
    t = title.lower()
    return any(tok.lower() in t for tok in tokens) and not any(n in t for n in NOISE)


def concerns(headlines_year: List[Dict], drop_headlines: List[Dict], tokens: List[str], top: int = 4) -> Dict:
    """Themes of the negative headlines: {themes: [{key, en, he, count, examples}], tone: {...}, n}."""
    seen, items = set(), []
    for weight, group in ((2, drop_headlines), (1, headlines_year)):
        for x in group:
            key = (x.get("title") or "").strip().lower()
            if not key or key in seen or not x.get("date") or not _relevant(x["title"], tokens):
                continue
            seen.add(key)
            items.append((weight, x))
    counts: Dict[str, float] = {}
    examples: Dict[str, List[Dict]] = {}
    neg = pos = neu = 0
    recent = (dt.date.today() - dt.timedelta(days=30)).isoformat()
    neg_30 = pos_30 = 0
    for weight, x in items:
        tone = _tone(x["title"])
        neg, pos, neu = neg + (tone < 0), pos + (tone > 0), neu + (tone == 0)
        if x["date"] >= recent:
            neg_30, pos_30 = neg_30 + (tone < 0), pos_30 + (tone > 0)
        if tone > 0:
            continue                                   # a concern is a theme of a negative (or neutral) headline
        for k, rx in _THEME_RE.items():
            if rx.search(x["title"]):
                counts[k] = counts.get(k, 0) + weight * (1 if tone < 0 else 0.5)
                ex = examples.setdefault(k, [])
                if len(ex) < 8 and all(e["title"] != x["title"] for e in ex):
                    ex.append({"date": x["date"], "title": x["title"], "publisher": x.get("publisher", ""), "weight": weight})
    themes = sorted(counts.items(), key=lambda kv: -kv[1])[:top]
    used, out = set(), []
    for k, c in themes:                                # each headline illustrates one theme only (drop-day headlines first)
        if c < 1:
            continue
        ex = [e for e in sorted(examples[k], key=lambda e: (-e["weight"], e["date"])) if e["title"] not in used][:2]
        used.update(e["title"] for e in ex)
        out.append({"key": k, "en": THEMES[k][0], "he": THEMES[k][1], "count": int(round(c)), "examples": ex})
    return {"n": len(items), "themes": out,
            "tone": {"neg": neg, "pos": pos, "neu": neu, "neg_30d": neg_30, "pos_30d": pos_30}}


def positioning(profile: Dict, twits: Optional[Dict]) -> Dict:
    ks = profile.get("defaultKeyStatistics") or {}
    ss, ssp = ks.get("sharesShort"), ks.get("sharesShortPriorMonth")
    date = ks.get("dateShortInterest")
    return {
        "short_pct": ks.get("shortPercentOfFloat"), "short_change": (ss / ssp - 1) if ss and ssp else None,
        "short_ratio": ks.get("shortRatio"),
        "short_date": dt.datetime.fromtimestamp(int(date), tz=dt.timezone.utc).strftime("%Y-%m-%d") if date else None,
        "institutions": ks.get("heldPercentInstitutions"), "insiders": ks.get("heldPercentInsiders"),
        "twits": twits or {},
    }


def sentiment_label(pos: Dict, an: Dict, ea: Dict, tone: Dict) -> Tuple[str, List[Tuple[str, int, Dict]]]:
    """(negative | mixed | positive, [(code, sign, args)]) over the listed signals; each signal counts +1 or -1."""
    sig: List[Tuple[str, int, Dict]] = []

    def add(cond, sign, code, **kw):
        if cond:
            sig.append((code, sign, kw))

    bn, b3 = an.get("bullish_now"), an.get("bullish_3m")
    add(bn is not None and b3 is not None and bn < b3 - 0.03, -1, "analysts_less_bullish", now=f"{bn * 100:.0f}%" if bn is not None else "",
        ago=f"{b3 * 100:.0f}%" if b3 is not None else "")
    add(bn is not None and b3 is not None and bn > b3 + 0.03, 1, "analysts_more_bullish", now=f"{bn * 100:.0f}%" if bn is not None else "",
        ago=f"{b3 * 100:.0f}%" if b3 is not None else "")
    cuts, raises = an.get("n_target_cuts", 0), an.get("n_target_raises", 0)
    add(cuts > raises, -1, "targets_cut", cuts=cuts, raises=raises)
    add(raises > cuts, 1, "targets_raised", cuts=cuts, raises=raises)
    ud = ea.get("y0_up_down_30d") or (0, 0)
    add(ud[1] > ud[0], -1, "revisions_down", up=ud[0], down=ud[1])
    add(ud[0] > ud[1], 1, "revisions_up", up=ud[0], down=ud[1])
    sc = pos.get("short_change")
    chg = f"{sc * 100:+.0f}%" if sc is not None else ""
    add(sc is not None and sc > 0.10, -1, "shorts_rising", chg=chg)
    add(sc is not None and sc < -0.10, 1, "shorts_falling", chg=chg)
    sp = pos.get("short_pct")
    add(sp is not None and sp > 0.10, -1, "short_heavy", pct=f"{sp * 100:.0f}%" if sp is not None else "")
    tw = pos.get("twits") or {}
    if tw.get("bullish", 0) + tw.get("bearish", 0) >= 5:
        add(tw["bearish"] > tw["bullish"], -1, "crowd_bearish", bull=tw["bullish"], bear=tw["bearish"], n=tw.get("n"))
        add(tw["bullish"] > tw["bearish"], 1, "crowd_bullish", bull=tw["bullish"], bear=tw["bearish"], n=tw.get("n"))
    n30 = tone.get("neg_30d", 0) + tone.get("pos_30d", 0)
    if n30 >= 4:
        add(tone["neg_30d"] > tone["pos_30d"], -1, "news_negative", neg=tone["neg_30d"], pos=tone["pos_30d"])
        add(tone["pos_30d"] > tone["neg_30d"], 1, "news_positive", neg=tone["neg_30d"], pos=tone["pos_30d"])
    score = sum(s for _, s, _ in sig)
    label = "negative" if score <= -2 else "positive" if score >= 2 else "mixed"
    return label, sig


SIGNAL_EN = {
    "analysts_less_bullish": "fewer analysts bullish than three months ago ({now} vs {ago})",
    "analysts_more_bullish": "more analysts bullish than three months ago ({now} vs {ago})",
    "targets_cut": "price targets mostly cut in 90 days ({cuts} cuts vs {raises} raises)",
    "targets_raised": "price targets mostly raised in 90 days ({raises} raises vs {cuts} cuts)",
    "revisions_down": "EPS estimates revised down ({up} up / {down} down in 30 days)",
    "revisions_up": "EPS estimates revised up ({up} up / {down} down in 30 days)",
    "shorts_rising": "short interest rising ({chg} in a month)", "shorts_falling": "short interest falling ({chg} in a month)",
    "short_heavy": "heavy short interest ({pct} of float)",
    "crowd_bearish": "StockTwits crowd bearish ({bear} bearish vs {bull} bullish of the last {n} posts)",
    "crowd_bullish": "StockTwits crowd bullish ({bull} bullish vs {bear} bearish of the last {n} posts)",
    "news_negative": "headlines mostly negative in the last 30 days ({neg} negative vs {pos} positive)",
    "news_positive": "headlines mostly positive in the last 30 days ({pos} positive vs {neg} negative)",
}
SIGNAL_HE = {
    "analysts_less_bullish": "פחות אנליסטים שוריים מאשר לפני שלושה חודשים ({now} מול {ago})",
    "analysts_more_bullish": "יותר אנליסטים שוריים מאשר לפני שלושה חודשים ({now} מול {ago})",
    "targets_cut": "יעדי המחיר בעיקר הורדו ב-90 יום ({cuts} הורדות מול {raises} העלאות)",
    "targets_raised": "יעדי המחיר בעיקר הועלו ב-90 יום ({raises} העלאות מול {cuts} הורדות)",
    "revisions_down": "תחזיות הרווח עודכנו כלפי מטה ({up} למעלה / {down} למטה ב-30 יום)",
    "revisions_up": "תחזיות הרווח עודכנו כלפי מעלה ({up} למעלה / {down} למטה ב-30 יום)",
    "shorts_rising": "השורט גדל ({chg} בחודש)", "shorts_falling": "השורט קטן ({chg} בחודש)",
    "short_heavy": "שורט כבד ({pct} מהמניות הצפות)",
    "crowd_bearish": "הקהל ב-StockTwits דובי ({bear} דוביים מול {bull} שוריים מתוך {n} ההודעות האחרונות)",
    "crowd_bullish": "הקהל ב-StockTwits שורי ({bull} שוריים מול {bear} דוביים מתוך {n} ההודעות האחרונות)",
    "news_negative": "הכותרות ב-30 הימים האחרונים בעיקר שליליות ({neg} שליליות מול {pos} חיוביות)",
    "news_positive": "הכותרות ב-30 הימים האחרונים בעיקר חיוביות ({pos} חיוביות מול {neg} שליליות)",
}
LABEL_EN = {"negative": "negative", "mixed": "mixed", "positive": "positive"}
LABEL_HE = {"negative": "שלילי", "mixed": "מעורב", "positive": "חיובי"}


def _pct(v, d=0):
    return "" if v is None else f"{v * 100:+.{d}f}%"


def sentiment_view(headlines_year: List[Dict], drop_headlines: List[Dict], tokens: List[str], profile: Dict,
                   twits: Optional[Dict], an: Dict, ea: Dict) -> Dict:
    """Everything the block needs: {concerns, positioning, label, signals}."""
    con = concerns(headlines_year, drop_headlines, tokens)
    pos = positioning(profile, twits)
    label, sig = sentiment_label(pos, an, ea, con["tone"])
    return {"concerns": con, "positioning": pos, "label": label, "signals": sig}


def sentiment_markdown(view: Dict, lang: str = "en") -> List[str]:
    """The 'investor concerns and sentiment' block, English or Hebrew, as markdown lines."""
    con, pos, label, sig = view["concerns"], view["positioning"], view["label"], view["signals"]
    he = lang == "he"
    texts = SIGNAL_HE if he else SIGNAL_EN
    md = ["### חששות המשקיעים וסנטימנט", ""] if he else ["**Investor concerns and sentiment.**", ""]
    # concerns
    if con["themes"]:
        head = (f"**מה מטריד את המשקיעים** (נושאי הכותרות השליליות בשנה האחרונה, {con['n']} כותרות שנבדקו; כותרות סביב ימי הירידה הגדולים נספרות כפולות):"
                if he else f"**What worries investors** (themes of the negative headlines of the last year, {con['n']} headlines checked; "
                           "headlines around the largest down days count double):")
        md.append(head)
        for t in con["themes"]:
            ex = "; ".join(f"{e['date']} \"{e['title']}\"" + (f" ({e['publisher']})" if e.get("publisher") else "") for e in t["examples"])
            md.append(f"- **{t['he'] if he else t['en']}** ({t['count']:g}): {ex}")
    else:
        md.append("**מה מטריד את המשקיעים:** לא נמצאו כותרות שליליות שמזכירות את החברה בשנה האחרונה." if he
                  else "**What worries investors:** no negative headlines naming the company were found in the last year.")
    tone = con["tone"]
    md.append((f"טון הכותרות בשנה האחרונה: {tone['neg']} שליליות, {tone['pos']} חיוביות, {tone['neu']} ניטרליות; "
               f"ב-30 הימים האחרונים {tone['neg_30d']} שליליות מול {tone['pos_30d']} חיוביות.") if he else
              (f"Headline tone over the year: {tone['neg']} negative, {tone['pos']} positive, {tone['neu']} neutral; "
               f"last 30 days {tone['neg_30d']} negative vs {tone['pos_30d']} positive."))
    md.append("")
    # positioning
    tw = pos.get("twits") or {}
    parts = []
    if pos.get("short_pct") is not None:
        parts.append((f"שורט {pos['short_pct'] * 100:.1f}% מהמניות הצפות" if he else f"Short interest {pos['short_pct'] * 100:.1f}% of float")
                      + (f" ({_pct(pos['short_change'])} {'מול החודש הקודם' if he else 'vs the prior month'}" if pos.get("short_change") is not None else "")
                      + (f", {pos['short_ratio']:.1f} {'ימי כיסוי' if he else 'days to cover'}" if pos.get("short_ratio") else "")
                      + (")" if pos.get("short_change") is not None else "")
                      + (f", {'נכון ל' if he else 'as of '}-{pos['short_date']}" if pos.get("short_date") else ""))
    if pos.get("institutions") is not None:
        parts.append((f"מוסדיים מחזיקים {pos['institutions'] * 100:.0f}%" if he else f"institutions hold {pos['institutions'] * 100:.0f}%")
                      + (f", {'אינסיידרים' if he else 'insiders'} {pos['insiders'] * 100:.1f}%" if pos.get("insiders") is not None else ""))
    if tw.get("n"):
        parts.append((f"StockTwits ({tw.get('watchers') or '?'} עוקבים): מתוך {tw['n']} ההודעות האחרונות {tw['bearish']} דוביות, {tw['bullish']} שוריות"
                      if he else f"StockTwits ({tw.get('watchers') or '?'} watchers): of the last {tw['n']} posts {tw['bearish']} bearish, {tw['bullish']} bullish"))
    if parts:
        md.append(("**פוזיציות:** " if he else "**Positioning:** ") + "; ".join(parts) + ".")
    md.append((f"**סנטימנט: {LABEL_HE[label]}**" if he else f"**Sentiment: {LABEL_EN[label]}**")
              + (" (איתותים: " if he else " (signals: ")
              + ("; ".join(f"{'+' if s > 0 else '-'} {texts[c].format(**kw)}" for c, s, kw in sig) if sig else ("אין" if he else "none")) + ").")
    md.append("")
    return md
