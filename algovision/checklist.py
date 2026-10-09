"""The checklist: the few names that pass the most checks today, shown as pass/fail columns.

Not a new composite score. Every column is one condition that can be checked on its own, and the look-back section and
docs/research_filters.md say what each one did. The checks:

* **signal**: listed today in a tested signal table (news-day, confirmed falling wedge, insider buys in a beaten-down
  stock, early rally), not only on the watch list or the insider context line;
* **no warning flag**: none of Z / S / T (:data:`algovision.briefs.WARNING_FLAGS`; five-week evidence only);
* **deep decline (D)**: more than 40% below the 52-week high, the strongest positive condition in the ten-year backtests
  of all three rules (+4-6% excess over random entries at 20 bars);
* **market-driven**: "market-wide" is among the causes found for the decline; its backtestable analogue (the sector
  explains at least half of the 60-bar fall) helped the wedge and rally rules in both halves of the decade;
* **read**: the rule-based read says "signs of a bottom" (five-week evidence only).

Rows need the first two checks; the table shows up to ``TOP`` names by the number of checks passed, then by read score.
The regime line above the table describes the beaten-down basket; the ten-year backtests found no regime gate worth
having (the rules earned more over random entries when the basket was falling), so it stays a description.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd

from algovision.briefs import WARNING_FLAGS
from algovision.links import tv

TOP = 10
SIGNAL_TABLES = ("news-day", "falling wedge", "insider buys (beaten-down)", "early rally")
N_CHECKS = 5


def _tables(row: Dict) -> List[str]:
    t = row.get("tables")
    if isinstance(t, str):
        return [x.strip() for x in t.split(",") if x.strip()]
    return list(t or [])


def checklist_rows(rows: List[Dict]) -> List[Dict]:
    out = []
    for r in rows:
        tables = _tables(r)
        signal = any(t in SIGNAL_TABLES for t in tables)
        flags = list(r.get("flags") or [])
        if not signal or any(f in WARNING_FLAGS for f in flags):
            continue
        deep = "D" in flags
        read = r.get("read") == "signs of a bottom"
        market = "market-wide" in str(r.get("why fell") or "")
        out.append({"symbol": r["symbol"], "tables": ", ".join(tables), "deep": deep, "read": read, "market": market,
                    "score": float(r.get("score") or 0), "sentiment": r.get("sentiment") or "", "passes": 2 + int(deep) + int(market) + int(read)})
    out.sort(key=lambda d: (-d["passes"], -d["score"]))
    return out[:TOP]


def checklist_markdown(rows: List[Dict], lang: str = "en", regime_warning: Optional[bool] = None, anchor=None) -> List[str]:
    he = lang == "he"
    ck = checklist_rows(rows)
    head = "### רשימת הבדיקות: השמות שעוברים הכי הרבה בדיקות היום" if he else "### Checklist: the names passing the most checks today"
    intro = (("לא ציון מורכב חדש: כל עמודה היא תנאי אחד שאפשר לבדוק לבד, ו\"מה עבד עד עכשיו\" ו-docs/research_filters.md אומרים מה כל אחד עשה. "
              "שורה נכנסת רק אם המניה בטבלת איתותים שנבדקה (יום חדשות, טריז מאושר, אינסיידרים במניה מוכה, ראלי מוקדם) ובלי אף דגל אזהרה (Z, S, T); "
              "אחר כך: ירידה עמוקה (D, יותר מ-40% מהשיא: התנאי החיובי החזק ביותר בבדיקות עשר השנים), \"כלל-שוק\" בין סיבות הירידה (התחליף שלו "
              "עזר לטריז ולראלי בשני חצאי העשור), וקריאה \"סימני תחתית\" (חמישה שבועות בלבד). ממוינות לפי מספר הבדיקות שעברו ואז לפי ציון הקריאה; עד 10 שמות.") if he else
             ("Not a new composite score: every column is one condition that can be checked on its own, and 'What has worked so far' and "
              "docs/research_filters.md say what each one did. A row needs a tested signal table today (news-day, confirmed wedge, insider buys in a "
              "beaten-down stock, early rally) and no warning flag (Z, S, T); then: a deep decline (D, more than 40% below the 52-week high: the strongest "
              "positive condition in the ten-year backtests), 'market-wide' among the causes of the decline (its analogue helped the wedge and rally rules in "
              "both halves of the decade), and the read 'signs of a bottom' (five weeks only). Sorted by checks passed, then by read score; at most 10 names."))
    md = [head, "", intro, ""]
    if regime_warning:
        md += [("**הסל יורד:** סל המניות המוכות ירד ב-20 הנרות האחרונים (ראו שורת המשטר בראש הדוח); זה חל על כל השמות כאן. בבדיקות עשר השנים "
                "הכללים הרוויחו יותר מעל כניסות אקראיות דווקא כשהסל ירד, ולכן זה תיאור ולא שער." if he else
                "**Basket falling:** the beaten-down basket fell over the last 20 bars (see the regime line at the top); this applies to every name here. "
                "In the ten-year backtests the rules earned more over random entries when the basket was falling, so this is a description, not a gate."), ""]
    if not ck:
        return md + [("אין היום שם שעובר את שתי הבדיקות הראשונות (טבלת איתותים ובלי דגלי אזהרה)." if he else
                      "No name passes the first two checks today (a signal table and no warning flag)."), ""]
    yes, no = ("✓", "✗")
    if he:
        from algovision.daily_he import TABLE_HE  # noqa: F401  (Hebrew names of the tables)
        t = pd.DataFrame({
            "סימול": [tv(d["symbol"]) for d in ck],
            **({"פירוט": [f"[פירוט](#{anchor(d['symbol'])})" for d in ck]} if anchor else {}),
            "בטבלאות": [", ".join(TABLE_HE.get(x.strip(), x.strip()) for x in d["tables"].split(",")) for d in ck],
            "בלי דגלי אזהרה": [yes for _ in ck], "ירידה עמוקה (D)": [yes if d["deep"] else no for d in ck],
            "ירידה שהשוק גרר": [yes if d["market"] else no for d in ck], "סימני תחתית": [yes if d["read"] else no for d in ck],
            "בדיקות שעברו": [f"{d['passes']}/{N_CHECKS}" for d in ck],
            "ציון קריאה": [f"{d['score']:+g}" for d in ck], "סנטימנט": [{"positive": "חיובי", "mixed": "מעורב", "negative": "שלילי"}.get(d["sentiment"], d["sentiment"]) for d in ck],
        })
    else:
        t = pd.DataFrame({
            "symbol": [tv(d["symbol"]) for d in ck], "in tables": [d["tables"] for d in ck],
            "no warning flag": [yes for _ in ck], "deep decline (D)": [yes if d["deep"] else no for d in ck],
            "market-driven decline": [yes if d["market"] else no for d in ck], "signs of a bottom": [yes if d["read"] else no for d in ck],
            "checks passed": [f"{d['passes']}/{N_CHECKS}" for d in ck],
            "read score": [f"{d['score']:+g}" for d in ck], "sentiment": [d["sentiment"] for d in ck],
        })
    return md + [t.to_markdown(index=False), ""]
