"""The checklist: the few names that pass the most checks today, shown as pass/fail columns.

Not a new composite score. Every column is one condition that can be checked on its own, and the look-back section says
what each one did so far. The checks:

* **signal**: listed today in a tested signal table (news-day, confirmed falling wedge, insider buys in a beaten-down
  stock, early rally), not only on the watch list or the insider context line;
* **no flags**: none of Z / D / S / T (:data:`algovision.briefs.FLAGS`);
* **read**: the rule-based read says "signs of a bottom";
* **market-driven**: "market-wide" is among the causes found for the decline (declines the market dragged recovered
  better in the first five weeks than company-specific ones).

Rows need the first two checks; the table shows up to ``TOP`` names by the number of checks passed, then by read score.
The regime line above the table says whether the beaten-down basket itself is falling, which is the same for every name.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd

from algovision.links import tv

TOP = 10
SIGNAL_TABLES = ("news-day", "falling wedge", "insider buys (beaten-down)", "early rally")


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
        if not signal or flags:
            continue
        read = r.get("read") == "signs of a bottom"
        market = "market-wide" in str(r.get("why fell") or "")
        out.append({"symbol": r["symbol"], "tables": ", ".join(tables), "read": read, "market": market, "score": float(r.get("score") or 0),
                    "sentiment": r.get("sentiment") or "", "passes": 2 + int(read) + int(market)})
    out.sort(key=lambda d: (-d["passes"], -d["score"]))
    return out[:TOP]


def checklist_markdown(rows: List[Dict], lang: str = "en", regime_warning: Optional[bool] = None, anchor=None) -> List[str]:
    he = lang == "he"
    ck = checklist_rows(rows)
    head = "### רשימת הבדיקות: השמות שעוברים הכי הרבה בדיקות היום" if he else "### Checklist: the names passing the most checks today"
    intro = (("לא ציון מורכב חדש: כל עמודה היא תנאי אחד שאפשר לבדוק לבד, ו\"מה עבד עד עכשיו\" אומר מה כל אחד עשה. "
              "שורה נכנסת רק אם המניה בטבלת איתותים שנבדקה (יום חדשות, טריז מאושר, אינסיידרים במניה מוכה, ראלי מוקדם) ובלי אף דגל; "
              "אחר כך: קריאה \"סימני תחתית\", ו\"כלל-שוק\" בין סיבות הירידה. ממוינות לפי מספר הבדיקות שעברו ואז לפי ציון הקריאה; עד 10 שמות.") if he else
             ("Not a new composite score: every column is one condition that can be checked on its own, and 'What has worked so far' says what "
              "each one did. A row needs a tested signal table today (news-day, confirmed wedge, insider buys in a beaten-down stock, early rally) "
              "and no flag; then: the read says 'signs of a bottom', and 'market-wide' is among the causes of the decline. Sorted by checks passed, "
              "then by read score; at most 10 names."))
    md = [head, "", intro, ""]
    if regime_warning:
        md += [("**המשטר נגד:** סל המניות המוכות יורד (ראו שורת המשטר בראש הדוח); זה חל על כל השמות כאן." if he else
                "**Regime against:** the beaten-down basket is falling (see the regime line at the top); this applies to every name here."), ""]
    if not ck:
        return md + [("אין היום שם שעובר את שתי הבדיקות הראשונות (טבלת איתותים ובלי דגלים)." if he else
                      "No name passes the first two checks today (a signal table and no flag)."), ""]
    yes, no = ("✓", "✗")
    if he:
        from algovision.daily_he import TABLE_HE, READ_HE  # noqa: F401  (Hebrew names of the tables)
        t = pd.DataFrame({
            "סימול": [tv(d["symbol"]) for d in ck],
            **({"פירוט": [f"[פירוט](#{anchor(d['symbol'])})" for d in ck]} if anchor else {}),
            "בטבלאות": [", ".join(TABLE_HE.get(x.strip(), x.strip()) for x in d["tables"].split(",")) for d in ck],
            "בלי דגלים": [yes for _ in ck], "סימני תחתית": [yes if d["read"] else no for d in ck],
            "ירידה שהשוק גרר": [yes if d["market"] else no for d in ck], "בדיקות שעברו": [f"{d['passes']}/4" for d in ck],
            "ציון קריאה": [f"{d['score']:+g}" for d in ck], "סנטימנט": [{"positive": "חיובי", "mixed": "מעורב", "negative": "שלילי"}.get(d["sentiment"], d["sentiment"]) for d in ck],
        })
    else:
        t = pd.DataFrame({
            "symbol": [tv(d["symbol"]) for d in ck], "in tables": [d["tables"] for d in ck],
            "no flags": [yes for _ in ck], "signs of a bottom": [yes if d["read"] else no for d in ck],
            "market-driven decline": [yes if d["market"] else no for d in ck], "checks passed": [f"{d['passes']}/4" for d in ck],
            "read score": [f"{d['score']:+g}" for d in ck], "sentiment": [d["sentiment"] for d in ck],
        })
    return md + [t.to_markdown(index=False), ""]
