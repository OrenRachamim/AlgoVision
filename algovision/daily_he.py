"""One file, in Hebrew, with everything the daily run produces: ``daily_<date>.md`` / ``daily_latest.md``.

It carries, in this order, what the three English/Hebrew files carried separately:

1. the "what is new" note (``new_latest.md``);
2. the report tables (``report_latest.md``): insider buying, news-day, falling wedge (with the wedge file's extra
   columns: target, distance from the stop, ATR, wedge height, peers, AI, group, why it fell, concerns, sentiment,
   read), early rally;
3. the briefs summary table (``briefs_latest.md`` / report section 3), the Jev section (explanation, high-priority
   picks, the full decisions table, what was logged) and the stocks Jev prioritised (``wedge_latest.md``);
4. one section per stock in the tables (``briefs_latest.md`` in English, ``wedge_latest.md`` for the wedges): the
   five-line summary, the time-axis story, the wedge's technical analysis (wedge stocks), where the stock is, why it
   fell with the latest news, investor concerns and sentiment, peers and group, the AI decision, analysts, the last
   report and estimates, fundamentals, the rule-based read;
5. the forward-test journal (``report_latest.md`` section 4): running results per rule and every open position.

Everything the program says is in Hebrew; tickers, company names, analyst firms and headlines stay as published.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.briefs import _money, _num, _pct
from algovision.decide import LABEL_HE as DEC_HE, SEVERITY_HE, decision_cell, decision_markdown, top_picks, top_picks_he
from algovision.journal import RULES
from algovision.links import tradingview_url
from algovision.peers import peers_markdown, peers_short
from algovision.sentiment import LABEL_HE as SENT_HE, sentiment_markdown
from algovision.story import story_markdown
from algovision.wedge_report import (LABEL_HE, LABEL_SHORT_HE, STATUS_HE, _he_cause, _he_consensus, _he_sector, _spy_below_ma200, analysts_he,
                                     fundamentals_he, read_he, report_he, summary_he, wedge_geometry, wedge_section_he, why_fell_he)
from algovision.whatsnew import RULE_HE

TABLE_HE = {"insider buys (beaten-down)": "אינסיידרים (מוכות)", "insider buys (other)": "אינסיידרים (אחרות)", "news-day": "יום חדשות",
            "falling wedge": "טריז יורד", "falling wedge (forming)": "טריז בהתהוות (מעקב)", "early rally": "ראלי מוקדם"}
DAYS_LABEL = {"insider_beaten": "Insider buys, beaten-down (tested setup)", "newsday": "News-day", "wedge": "Falling wedge, beaten-down",
              "rally": "Early rally, beaten-down", "watch": "Wedge watch list (forming, not a signal)"}


def _days(days: Optional[Dict[str, Dict[str, int]]], key: str, symbol: str) -> str:
    if not days:
        return ""
    n = days.get(DAYS_LABEL[key], {}).get(symbol, 0)
    if key == "watch":
        n = max(n, days.get(DAYS_LABEL["wedge"], {}).get(symbol, 0))
    return str(n + 1)
READ_HE = {"signs of a bottom": "סימני תחתית", "undecided": "לא מוכרע", "still falling": "עדיין יורדת"}
RULE_TEXT_HE = {"ma50_cross": "חזרה מעל ממוצע 50", "golden_20_50": "ממוצע 20 חוצה את 50", "higher_high": "שיא גבוה יותר (תפנית דאו)",
                "thrust": "זינוק +8% ב-10 נרות", "rsi_turn": "RSI חוזר מעל 50"}
RULE_EXPECT_HE = {
    "newsday": "+6-7% מול אקראי, הצלחה ~62% (docs/research_anomalies.md)",
    "falling_wedge_beaten_down": "+3% מול אקראי, הצלחה ~60% (docs/research_falling_wedge.md)",
    "insider_buy_beaten_down": "+10% מול אקראי ב-60 נרות, +15% ב-120, הצלחה ~68% (docs/research_insiders.md)",
    "jev_pick": "לא נבדק: ה\"קנייה\" של מודל ההחלטות Jev (P של 0.6 ומעלה) על מניה מהרשימה, נרשם על ידי הדוח היומי (algovision/decide.py)",
    "jev_skip": "לא נבדק: ה\"דילוג\" של המודל (P(דילוג) 0.5 ומעלה); הקריאה נכונה כשהמניה יורדת, ולכן תשואה שלילית היא ההצלחה",
    "early_rally_beaten_down": "+2-3% נטו, הצלחה ~58-61%, +3.5-4% מול כניסה אקראית באותה מניה, ~0 מול SPY ב-20 נרות (docs/research_rally.md)",
}


def _tv(s: str) -> str:
    return f"[{s}]({tradingview_url(s)})"


def _anchor(symbol: str) -> str:
    return "s-" + "".join(ch if ch.isalnum() else "-" for ch in symbol.lower())


def _tables_he(tables) -> str:
    return ", ".join(TABLE_HE.get(t, t) for t in (tables or []))


def _group_cell_he(p: Optional[Dict]) -> str:
    if not p or p.get("g_beaten") is None:
        return ""
    return (("מוכה" if p["g_beaten"] else "לא מוכה") + (f" ({p['share_beaten'] * 100:.0f}%)" if p.get("share_beaten") == p.get("share_beaten") else "")
            + (f" + טריז {'מאושר' if p['g_wedge'] == 'confirmed' else 'בהתהוות'}" if p.get("g_wedge") else ""))


# ----------------------------------------------------------------------------
# tables
# ----------------------------------------------------------------------------
def insiders_he(sig: pd.DataFrame, tx: pd.DataFrame, sectors: Dict[str, str], insider_days: int, days: Optional[Dict] = None) -> List[str]:
    md = [f"## 1. קניות אינסיידרים (טופס 4 של ה-SEC, נושאי משרה ודירקטורים, {insider_days} הימים האחרונים)", "",
          "הכלל נבדק 2016-2026: רכישה של 100 אלף דולר ומעלה במניה **מוכה** (מתחת לממוצע הנע של 200 יום, תשואת 6 חודשים מתחת ל-8%-): "
          "+10% מול כניסה אקראית על פני 60 נרות, +15% על פני 120, שיעור הצלחה ~68%, בשני חצאי העשור. רכישות במניות במגמת עלייה "
          "לא הראו יתרון ומוצגות בשורה אחת להקשר בלבד.", ""]
    if not len(sig):
        md += ["אין רכישות אינסיידרים בחלון.", ""]
        return md
    bd, rest = sig[sig["beaten_down"]], sig[~sig["beaten_down"]]
    for title, d in (("### מניות מוכות (התבנית שנבדקה)", bd),):
        md += [title, ""]
        if not len(d):
            md += ["אין", ""]
            continue
        t = pd.DataFrame({
            "סימול": d["symbol"].map(_tv), "פירוט": d["symbol"].map(lambda s: f"[פירוט](#{_anchor(s)})"),
            "ימים ברשימה": d["symbol"].map(lambda s: _days(days, "insider_beaten", s)),
            "סקטור": d["symbol"].map(lambda s: _he_sector(sectors.get(s, ""))), "דיווח אחרון": d["last_filing"],
            "אשכול (2+ אינסיידרים/30 יום)": np.where(d["cluster"], "כן", "לא"), "אינסיידרים 30 יום": d["n_insiders_30d"],
            "קניות": d["n_buys"], "סה\"כ": d["total_value"].map(lambda v: f"${v / 1e6:.2f}M"),
            "מחיר ממוצע": d["avg_price"].map(lambda v: f"{v:.2f}"), "אחרון": d["last_close"].map(lambda v: f"{v:.2f}"),
            "6 חודשים": d["ret_6m"].map(_pct), "מול ממוצע 200": d["dist_ma200"].map(_pct), "מנכ\"ל/סמנכ\"ל כספים": np.where(d["ceo_cfo"], "כן", ""),
            "קונים": d["buyers"].str.slice(0, 70)})
        md += [t.to_markdown(index=False), ""]
    md += ["### מניות אחרות עם רכישות אינסיידרים (הקשר)", ""]
    if len(rest):
        officer = ' מנכ"ל/סמנכ"ל כספים'
        md += ["אין יתרון שנבדק (מניות במגמת עלייה), שורה אחת בלבד: " + ", ".join(
            f"{_tv(r.symbol)} {r.last_filing} ${r.total_value / 1e6:.2f}M{officer if r.ceo_cfo else ''}{' אשכול' if r.cluster else ''}"
            for r in rest.itertuples()) + ".", ""]
    else:
        md += ["אין", ""]
    md += [f"נסרקו {len(tx)} עסקאות שוק פתוח של נושאי משרה/דירקטורים.", ""]
    return md


def newsday_he(nd: pd.DataFrame, sectors: Dict[str, str], days: Optional[Dict] = None) -> List[str]:
    md = ["### כלל יום החדשות (פער של 4%+ על מחזור של פי 3+ במניה מוכה, 5 הנרות האחרונים; החזקה ~60 נרות; נבדק +6-7% מול אקראי)", ""]
    if not len(nd):
        return md + ["אין", ""]
    t = nd[["symbol", "news_date", "bars_ago", "gap", "volume_ratio", "ret_6m", "dist_ma200", "last_close", "since_news", "bars_left"]].copy()
    for c in ("gap", "ret_6m", "dist_ma200", "since_news"):
        t[c] = t[c].map(lambda v: _pct(v, 1))
    t["volume_ratio"] = t["volume_ratio"].map(lambda v: f"{v:.1f}x")
    out = pd.DataFrame({"סימול": t["symbol"].map(_tv), "פירוט": t["symbol"].map(lambda s: f"[פירוט](#{_anchor(s)})"),
                        "ימים ברשימה": t["symbol"].map(lambda s: _days(days, "newsday", s)), "תאריך החדשות": t["news_date"],
                        "נרות מאז": t["bars_ago"], "פער": t["gap"], "יחס מחזור": t["volume_ratio"], "6 חודשים": t["ret_6m"],
                        "מול ממוצע 200": t["dist_ma200"], "סגירה אחרונה": t["last_close"], "מאז החדשות": t["since_news"], "נרות שנותרו": t["bars_left"],
                        "סקטור": t["symbol"].map(lambda s: _he_sector(sectors.get(s, "")))})
    return md + [out.to_markdown(index=False), ""]


def wedge_table_he(wedges: Dict, frames: Dict[str, pd.DataFrame], data: Dict[str, Dict], peers: Dict[str, Dict], decisions: Dict[str, Dict],
                   sectors: Dict[str, str], days: Optional[Dict] = None, watch: bool = False) -> List[str]:
    """The confirmed wedges (the signal) or, with ``watch=True``, the forming ones as the watch list."""
    if watch:
        md = ["### רשימת מעקב: טריזים יורדים שעדיין בהתהוות (לא איתות; האיתות הוא הסגירה מעל הקו העליון)", ""]
        wedges = {s: m for s, m in wedges.items() if m.status != "confirmed"}
        if not wedges:
            return md + ["אין", ""]
    else:
        md = ["### טריז יורד במניות מוכות (מאושר = סגר מעל הקו העליון ב-5 הנרות האחרונים; החזקה ~20 נרות; נבדק +3% מול אקראי). "
              "טריזים שעדיין בהתהוות נמצאים ברשימת המעקב בסוף הסעיף, לא כאן.", ""]
        wedges = {s: m for s, m in wedges.items() if m.status == "confirmed"}
        if not wedges:
            return md + ["אין פריצות מאושרות היום.", ""]
    rows = []
    order = sorted(wedges, key=lambda s: wedges[s].metrics.get("context", {}).get("ret_126", 0))      # deepest decline first
    for s in order:
        m, df = wedges[s], frames[s]
        d = data.get(s) or {}
        geo = wedge_geometry(m, df)
        last = float(df["Close"].iloc[-1])
        pr, dec = peers.get(s), decisions.get(s)
        why, sent, fu = d.get("why") or {}, d.get("sent"), d.get("fu") or {}
        rows.append({
            "סימול": _tv(s), "פירוט": f"[פירוט](#{_anchor(s)})", "ימים ברשימה": _days(days, "watch" if watch else "wedge", s),
            "ציון": f"{m.score:.2f}", "התחלה": m.start_date,
            **({} if watch else {"פריצה": m.breakout_date or "", "נרות מאז הפריצה": (len(df) - 1 - int(m.breakout_idx)) if m.breakout_idx is not None else ""}),
            "רמה": f"{m.level:.2f}", "סטופ": f"{m.stop:.2f}", "יעד": f"{m.target:.2f}",
            "אחרון": f"{last:.2f}", "מהסטופ": _pct(m.stop / last - 1 if last else np.nan),
            "6 חודשים": _pct(m.metrics.get("context", {}).get("ret_126")), "מול ממוצע 200": _pct(m.metrics.get("context", {}).get("dist_ma200")),
            "ATR%": f"{m.metrics.get('context', {}).get('atr_pct', 0) * 100:.1f}%", "גובה הטריז": f"{geo['h0_pct'] * 100:.0f}%",
            "מול עמיתים 20 יום": peers_short(pr), "AI": decision_cell(dec, "he"), "הקבוצה": _group_cell_he(pr),
            "למה ירדה": _he_cause(why.get("cause", "")) if why else "", "חששות": (", ".join(t["he"] for t in sent["concerns"]["themes"][:2]) or "לא נמצאו") if sent else "",
            "סנטימנט": SENT_HE[sent["label"]] if sent else "", "קריאה": LABEL_SHORT_HE.get(d.get("label"), "") if d else "",
            "ציון קריאה": f"{d['score']:+g}" if d.get("score") is not None else "", "סקטור": _he_sector(fu.get("sector") or sectors.get(s)),
        })
    if watch:
        return md + [pd.DataFrame(rows).to_markdown(index=False), "",
                     "בחמשת השבועות הראשונים של מבחן הקדימה הטריזים בהתהוות ירדו כ-6% ב-20 נרות (פגיעה 11%), המאושרים לא; מניה בתוך טריז יורד היא "
                     "מניה שעדיין יורדת. היומן רושם טריז רק ביום הפריצה שלו.", ""]
    md += [pd.DataFrame(rows).to_markdown(index=False), "",
           "הירידה העמוקה ביותר קודם: בבדיקות עשר השנים ירידה של יותר מ-40% משיא 52 השבועות הוסיפה +5-6% מעל כניסות אקראיות ב-20 נרות, וציון הדטקטור "
           "לא ניבא דבר (השליש הגבוה היה הגרוע ביותר בשני חצאי העשור), ולכן הציון מוצג אבל לא קובע את הסדר (docs/research_filters.md).", "",
           "*הקבוצה*: קבוצת העמיתים של המניה כסל אחד במשקל שווה, מוכה או לא (בסוגריים חלקן של שאר החברות שמוכות), ו-\"+ טריז\" כאשר הסל "
           "עצמו בטריז יורד. איתותים שבהם רוב הקבוצה הייתה מוכה גם כן הרוויחו +1.2% (אימון) / +1.9% (מבחן) יותר על פני 20 נרות, חיובי בכל 6 "
           "השנים שנבדקו, לא אושר ב-60 נרות (docs/research_groups.md); ראיות בינוניות, הקשר ולא מסנן.", "",
           "**הכלל בקצרה.** טריז יורד: שני קווי מגמה יורדים ומתכנסים, המחיר נסחר בתוכם ונשאר בפנים, ופריצה בסגירה מעל הקו העליון היא האיתות. "
           "נבדק על S&P 500 + NASDAQ-100 ב-2016-2026 עם חלוקה לאימון (עד 2022) ומבחן (2023-2026): היתרון קיים רק במניות **מוכות**, כלומר תשואת 6 "
           "חודשים מתחת ל-8%- ומחיר מתחת לממוצע הנע של 200 יום. בתת-הקבוצה הזו: כ-3%+ לעסקה מעל כניסה אקראית באותה מניה, שיעור פגיעה ~60%, מקדם "
           "רווח ~1.8, חיובי בכל אחת מ-11 השנים, כ-100 איתותים בשנה. במניות במגמת עלייה הטריז הוא רק תיקון ואין לו יתרון. עזרו: כמה המניה מוכה, "
           "תנודתיות גבוהה (ATR), טריז גדול, ירידה תלולה לתוך התבנית ושוק חלש (SPY מתחת לממוצע 200: שיעור פגיעה 70%). לא עזרו: ציון הדטקטור, נפח "
           "הפריצה, התכווצות הנפח, מספר הנגיעות ו\"איכות\" הצורה. הכלל שהחזיק מעמד מחוץ למדגם: כניסה בסגירת הפריצה או בפתיחה למחרת, סטופ בתחתית "
           "הטריז (או 2 ATR), ללא יעד רווח, יציאה אחרי ~20 נרות; לצפות ל-2-3%+ עודף לעסקה ולירידה של 25-35% בתיק שווה-משקל של האיתותים האלה "
           "(docs/research_falling_wedge.md).", ""]
    return md


def rally_table_he(rally: pd.DataFrame, peers: Dict[str, Dict], sectors: Dict[str, str], days: Optional[Dict] = None) -> List[str]:
    md = ["### ראלי מוקדם במניות מוכות (כלל תפנית ירה ב-3 הנרות האחרונים; החזקה ~20 נרות; נבדק +2-3% נטו, הצלחה ~58-61%, +3.5-4% מול כניסה אקראית, כ-0 מול SPY ב-20 נרות)", ""]
    if not len(rally):
        return md + ["אין", ""]
    t = rally.copy()
    out = pd.DataFrame({
        "סימול": t["symbol"].map(_tv), "פירוט": t["symbol"].map(lambda s: f"[פירוט](#{_anchor(s)})"),
        "ימים ברשימה": t["symbol"].map(lambda s: _days(days, "rally", s)),
        "כללים": t["rules"].map(lambda r: ", ".join(RULE_TEXT_HE.get(x.strip(), x.strip()) for x in str(r).split(","))), "כללים שירו": t["n_rules"],
        "תאריך האיתות": t["signal_date"], "נרות מאז": t["bars_ago"], "יום האיתות": t["day_ret"].map(lambda v: _pct(v, 1)), "10 ימים": t["ret_10"].map(lambda v: _pct(v, 1)),
        "6 חודשים": t["ret_6m"].map(lambda v: _pct(v, 1)), "משיא 52 שבועות": t["from_52w_high"].map(lambda v: _pct(v, 1)),
        "מול ממוצע 50": t["dist_ma50"].map(lambda v: _pct(v, 1)), "מול ממוצע 200": t["dist_ma200"].map(lambda v: _pct(v, 1)),
        "מחזור": t["volume_ratio"].map(lambda v: "" if pd.isna(v) else f"{v:.1f}x"), "אחרון": t["last"].map(lambda v: f"{v:.2f}"),
        "הקבוצה": t["symbol"].map(lambda s: _group_cell_he(peers.get(s))), "סקטור": t["symbol"].map(lambda s: _he_sector(sectors.get(s, "")))})
    md += [out.to_markdown(index=False), "",
           "*כללים*: חזרה מעל ממוצע 50 = הסגירה חוזרת מעל הממוצע הנע של 50 יום אחרי 15+ מתוך 20 נרות מתחתיו; ממוצע 20 חוצה את 50 = הממוצע של 20 יום "
           "חוצה מעלה את זה של 50; שיא גבוה יותר (תפנית דאו) = סגירה ראשונה מעל שיא הביניים אחרי שפל גבוה יותר; זינוק = +8% ב-10 נרות מתוך שפל 60 "
           "הנרות אחרי חצי שנה שטוחה או שלילית; RSI חוזר מעל 50 = RSI(14) חוזר מעל 50 אחרי שהיה מתחת ל-35. נבדק 2016-2026 על מניות מוכות בלבד "
           "(מתחת לממוצע 200, תשואת 6 חודשים מתחת ל-8%-), כניסה אחת למניה ל-30 יום, כניסה בפתיחה הבאה, עלות 10 נקודות בסיס: 20 נרות +2.7% (אימון) / "
           "+2.2% (מבחן), הצלחה 61% / 58%, +4.0% / +3.5% מעל כניסות אקראיות באותן מניות (t 19 / 13), חיובי בכל 10 השנים, אבל רק +0.6% / 0.0% מעל "
           "ה-SPY ב-20 נרות ו-+0.8% / -0.4% ב-60 (הכלל מתזמן את התפנית של המניה עצמה, הוא לא מכה את המדד). רק הירידות העמוקות ביותר מנצחות את "
           "ה-SPY (6 חודשים מתחת ל-30%-: +6.1% / +4.5% נטו ב-20 נרות, +2.5% / +2.1% מעל ה-SPY); שני כללים ומעלה בתוך שבוע עוזרים מעט. היומן רושם "
           "את שורות יום 0 ככלל early_rally_beaten_down (docs/research_rally.md).", ""]
    return md


def summary_table_he(rows: List[Dict], title: bool = True) -> List[str]:
    from algovision.briefs import flags_cell, flags_legend

    md = (["### טבלת התקציר", ""] if not title else []) + [
          "עמודת *קריאה* היא ציון מבוסס כללים על איתותים מתועדים (סימני תחתית / לא מוכרע / עדיין יורדת), לא תחזית. *למה ירדה* מציינת את הראיות "
          "שנמצאו סביב ימי הירידה הגדולים ביותר (כותרות המזכירות את החברה, הורדות דירוג, ימי שוק) או \"לא נמצא\"; שום דבר לא מוסק. *מול עמיתים 20 יום* "
          "הוא תשואת 20 הימים של המניה ביחס לקבוצת העמיתים שלה (המניות המתואמות איתה ביותר אחרי ניכוי השוק, מתוך מחירים) וציון ה-z שלה מול השנה "
          "האחרונה; מתחת ל-2- פירושו ירידה חריגה מול העמיתים. \"פירוט\" מקפיץ לסעיף המלא של המניה בקובץ הזה.", "", flags_legend("he"), ""]
    if title:
        md = ["## 3. תקציר לכל מניה (אחת לכל שם בטבלאות שלמעלה)", ""] + md
    if not rows:
        return md + ["אין", ""]
    d = pd.DataFrame(rows)
    order = {"signs of a bottom": 0, "undecided": 1, "still falling": 2}
    d = d.sort_values(["read", "score"], key=lambda s: s.map(order) if s.name == "read" else -s).reset_index(drop=True)
    out = pd.DataFrame({
        "סימול": d["symbol"].map(_tv), "פירוט": d["symbol"].map(lambda s: f"[פירוט](#{_anchor(s)})"),
        "בטבלאות": d["tables"].map(lambda t: ", ".join(TABLE_HE.get(x.strip(), x.strip()) for x in str(t).split(","))),
        "קריאה": d["read"].map(lambda r: READ_HE.get(r, r)), "ציון": d["score"].map(lambda v: f"{v:+g}"),
        "דגלים": d["flags"].map(flags_cell) if "flags" in d else "",
        "למה ירדה": d["why fell"].map(_he_cause) if "why fell" in d else "",
        "חששות": d["concerns"].map(lambda c: ", ".join(CONCERN_HE.get(x.strip(), x.strip()) for x in str(c).split(",")) if c else "") if "concerns" in d else "",
        "סנטימנט": d["sentiment"].map(lambda s: SENT_HE.get(s, s)) if "sentiment" in d else "",
        **({"AI": d["AI"].fillna("").map(_ai_he)} if "AI" in d else {}),
        "אחרון": d["last"].map(lambda v: f"{v:.2f}"), "משיא 52 שבועות": d["from 52w high"].map(_pct), "מול ממוצע 50": d["vs MA50"].map(_pct),
        "מול עמיתים 20 יום": d["vs peers 20d"] if "vs peers 20d" in d else "",
        "קונצנזוס": d["consensus"].map(_he_consensus), "אנליסטים": d["analysts"].map(lambda v: "" if v is None or pd.isna(v) else f"{int(v)}"),
        "אפסייד ליעד": d["target upside"].map(_pct), "העלאות/הורדות 90 יום": d["up/down 90d"],
        "תחזית EPS 30 יום": d["EPS est 30d"].map(lambda v: _pct(v, 1)), "הפתעה אחרונה": d["last surprise"].map(lambda v: _pct(v, 1)),
        "הדוח הבא": d["next report"],
    })
    return md + [out.to_markdown(index=False), ""]


# the concern themes as the sentiment module names them in English -> its own Hebrew names
from algovision.sentiment import THEMES as _THEMES  # noqa: E402

CONCERN_HE = {en: he for en, he, _ in _THEMES.values()}


def _ai_he(cell: str) -> str:
    for en, he in (("buy", "קנייה"), ("watch", "מעקב"), ("skip", "דילוג")):
        if cell.startswith(en):
            return he + cell[len(en):].replace("!", " ⚠")
    return cell


def decisions_table_he(decisions: Dict[str, Dict]) -> str:
    if not decisions:
        return "אין\n"
    rows = sorted(decisions.values(), key=lambda d: -(d.get("p_buy") or 0))
    f = lambda v, d=2: "" if v is None else f"{float(v):.{d}f}"  # noqa: E731
    t = pd.DataFrame({
        "סימול": [_tv(d["symbol"]) for d in rows], "פירוט": [f"[פירוט](#{_anchor(d['symbol'])})" for d in rows],
        "פעולה": [DEC_HE.get(d.get("action"), d.get("action")) for d in rows],
        "P(קנייה)": [f(d.get("p_buy")) for d in rows], "P(מעקב)": [f(d.get("p_watch")) for d in rows], "P(דילוג)": [f(d.get("p_skip")) for d in rows],
        "סוג הירידה": [DEC_HE.get(d.get("cause_type"), d.get("cause_type")) for d in rows],
        "הראיות מול התבנית": [DEC_HE.get(d.get("evidence"), d.get("evidence")) for d in rows],
        "P(פעולה תאגידית)": [f(d.get("corporate_action")) for d in rows], "P(אירוע ב-4 שבועות)": [f(d.get("event_ahead")) for d in rows],
        "חומרה 0-3": [(f"{f(d['severity'], 1)} ({SEVERITY_HE[min(3, max(0, int(round(d['severity']))))]})" if d.get("severity") is not None else "") for d in rows],
    })
    return t.to_markdown(index=False) + "\n"


def jev_he(decisions: Dict[str, Dict], picks: List[str], anchors: Dict[str, str], peers: Dict[str, Dict], skips: Optional[List[str]] = None) -> List[str]:
    md = ["### החלטות המודל (Jev), מבחן קדימה", ""]
    if not decisions:
        return md + ["דולג (אין מפתח OpenRouter, או שהמודל לא היה זמין).", ""]
    md += ["מודל החלטות מוקלד (TypeSafe Jev 1.13 דרך OpenRouter) קרא כל תקציר, ואת התקציר בלבד, וענה על שאלות קבועות בהסתברויות מכוילות: "
           "הפעולה להחזקה של חודש (קנייה / מעקב / דילוג), סוג הירידה, האם הירידה היא פעולה תאגידית או תקלת נתונים ולא ירידה אמיתית, האם אירוע ידוע "
           "צפוי בתוך ארבעה שבועות, האם הראיות תומכות בתבנית או סותרות אותה, וכמה החדשות רעות לעסק (0-3). הוא לא נותן נימוק. קריאות ה\"קנייה\" שלו "
           "עם P(קנייה) של 0.6 ומעלה נרשמות ביומן ככלל jev_pick, וקריאות ה\"דילוג\" עם P(דילוג) של 0.5 ומעלה ככלל jev_skip (החזקה 20 נרות; דילוג צודק "
           "כשהמניה יורדת), ושניהם משוערכים לשוק כמו כל כלל אחר. בשבוע הראשון שמות ה\"דילוג\" עשו טוב יותר משמות ה\"קנייה\", ולכן עד שלמבחן הקדימה "
           "יהיו 20+ עסקאות סגורות העמודה היא הקשר, לא המלצה. עמודת *AI* בטבלת התקצירים נושאת את אותה פעולה; ⚠ מסמן פעולה תאגידית או בעיית נתונים סבירה.", ""]
    md += [decisions_table_he(decisions),
           (("נרשמו היום ביומן כ-jev_pick: " + ", ".join(_tv(s) for s in picks)) if picks else "לא נרשם היום jev_pick חדש (אין \"קנייה\" עם P של 0.6 ומעלה ללא פוזיציה פתוחה).")
           + ((" נרשמו כ-jev_skip: " + ", ".join(_tv(s) for s in skips) + ".") if skips else ""), ""]
    md += top_picks_he(decisions, anchors, tradingview_url, None, peers)
    return md


# ----------------------------------------------------------------------------
# one section per stock
# ----------------------------------------------------------------------------
def where_he(ctx: Dict, fu: Dict) -> List[str]:
    return ["**איפה המניה.** "
            f"אחרון {ctx['last']:.2f}, {_pct(ctx['drawdown'])} משיא 52 השבועות ({ctx['high_52w']:.2f} ב-{ctx['high_date']}), "
            f"{_pct(ctx['off_low'])} מעל שפל 52 השבועות ({ctx['low_52w']:.2f} ב-{ctx['low_date']}). "
            f"חודש {_pct(ctx['ret_1m'])}, 3 חודשים {_pct(ctx['ret_3m'])}, 6 חודשים {_pct(ctx['ret_6m'])}, שנה {_pct(ctx['ret_1y'])}; "
            f"מול ממוצע 50 {_pct(ctx['dist_ma50'])}, מול ממוצע 200 {_pct(ctx['dist_ma200'])}; RSI(14) {ctx['rsi14']:.0f}."
            + (f" שינוי 52 שבועות {_pct(fu['chg_52w'])} מול S&P 500 {_pct(fu['spx_52w'])}." if fu.get("chg_52w") is not None else ""), ""]


def brief_summary_he(ctx: Dict, why: Dict, sent: Optional[Dict], an: Dict, ea: Dict, label: str, score: float, peers: Optional[Dict],
                     decision: Optional[Dict], tables: List[str]) -> List[str]:
    """The five-line summary for a stock that is not in the wedge table (the wedge stocks get the wedge file's own)."""
    md = ["**בקצרה:**",
          f"- **בטבלאות:** {_tables_he(tables)}. מחיר אחרון {ctx['last']:.2f}, {_pct(ctx['drawdown'])} משיא 52 השבועות ({ctx['high_date']}), "
          f"6 חודשים {_pct(ctx['ret_6m'])}, {_pct(ctx['dist_ma200'])} מול ממוצע 200, RSI(14) {ctx['rsi14']:.0f}."]
    quote = ""
    for d in why.get("days", []):
        if d.get("headlines"):
            h = d["headlines"][0]
            quote = f" למשל {d['day']} ({_pct(d['ret'], 1)}): \"{h['title']}\"" + (f" ({h['publisher']})" if h.get("publisher") else "") + "."
            break
    md.append(f"- **למה ירדה:** {_he_cause(why['cause'])}." + quote if why.get("found") else
              "- **למה ירדה:** לא נמצאה סיבה בנתונים (כותרות, דיווחי 8-K, הורדות דירוג, ימי שוק).")
    if sent:
        themes = ", ".join(t["he"] for t in sent["concerns"]["themes"][:3])
        neg = sum(1 for _, sg, _ in sent["signals"] if sg < 0)
        pos = sum(1 for _, sg, _ in sent["signals"] if sg > 0)
        md.append("- **חששות וסנטימנט:** " + (f"הכותרות השליליות עוסקות ב{themes}. " if themes else "לא נמצאו כותרות שליליות על החברה בשנה האחרונה. ")
                  + f"סנטימנט {SENT_HE[sent['label']]} ({neg} איתותים שליליים, {pos} חיוביים).")
    if peers and peers.get("ret20") is not None and peers.get("group_ret20") is not None:
        z = peers.get("z")
        md.append(f"- **מול העמיתים:** ב-20 יום המניה {_pct(peers['ret20'], 1)} מול {_pct(peers['group_ret20'], 1)} של קבוצת ההשוואה "
                  f"({peers['n_group']} מניות, למשל {', '.join(peers.get('top', [])[:3])}); יחסית לקבוצה {_pct(peers['rel20'], 1)}"
                  + (f", z={z:+.1f}" if z is not None else "") + ((" הקבוצה כסל **מוכה**" if peers["g_beaten"] else " הקבוצה כסל לא מוכה") if peers.get("g_beaten") is not None else "") + ".")
    if decision and decision.get("action"):
        md.append(f"- **AI (Jev):** {DEC_HE.get(decision['action'], decision['action'])} (קנייה {decision.get('p_buy', 0):.2f}, "
                  f"מעקב {decision.get('p_watch', 0):.2f}, דילוג {decision.get('p_skip', 0):.2f}); סוג הירידה {DEC_HE.get(decision.get('cause_type'), decision.get('cause_type'))}, "
                  f"הראיות {DEC_HE.get(decision.get('evidence'), decision.get('evidence'))} את התבנית"
                  + (f"; **הסתברות {decision['corporate_action']:.2f} שזו פעולה תאגידית/בעיית נתונים**" if (decision.get("corporate_action") or 0) >= 0.5 else "") + ".")
    an_txt = (f"קונצנזוס {_he_consensus(an.get('key'))} ({an.get('n') or '?'} אנליסטים), יעד ממוצע {_num(an.get('target'), 2)} "
              f"({_pct(an.get('upside'))} מהמחיר)" if an.get("key") else "אין קונצנזוס אנליסטים")
    md.append(f"- **אנליסטים וקריאה:** {an_txt}" + (f"; הדוח הבא {ea['next_date']}" if ea.get("next_date") else "")
              + f". קריאה מבוססת כללים: **{LABEL_SHORT_HE[label]}** (ציון {score:+g}).")
    md.append("")
    return md


def stock_section_he(symbol: str, row: Dict, df: pd.DataFrame, wedge, peers: Optional[Dict], decision: Optional[Dict], sectors: Dict[str, str],
                     spy_below: Optional[bool]) -> List[str]:
    d = row["_data"]
    ctx, an, ea, fu, why, sent, news = d["ctx"], d["an"], d["ea"], d["fu"], d["why"], d["sent"], d["news"]
    label, score, fired = d["label"], d["score"], d["fired"]
    name = fu.get("name") or symbol
    sec = [f"<a id=\"{_anchor(symbol)}\" name=\"{_anchor(symbol)}\"></a>", f"## {symbol} - {name}", "",
           f"[גרף ב-TradingView]({tradingview_url(symbol)}) · [חזרה לטבלה](#summary)", "",
           f"*בטבלאות היום: {_tables_he(d['tables'])}. {_he_sector(fu.get('sector') or sectors.get(symbol))}"
           + (f" / {fu['industry']}" if fu.get("industry") else "") + ".*" + (f" *{fu['summary'].rstrip('.')}.*" if fu.get("summary") else ""), ""]
    if wedge is not None:
        geo = wedge_geometry(wedge, df)
        sec += summary_he(wedge, geo, ctx, why, sent, an, ea, label, score, peers, decision)
    else:
        sec += brief_summary_he(ctx, why, sent, an, ea, label, score, peers, decision, d["tables"])
    if row.get("_story"):
        sec += story_markdown(row["_story"], "he")
    if wedge is not None:
        sec += wedge_section_he(wedge, df, wedge_geometry(wedge, df), ctx, spy_below)
    sec += where_he(ctx, fu)
    sec += why_fell_he(why, news, n_news=6, summaries=True)
    if sent:
        sec += sentiment_markdown(sent, "he")
    if peers:
        sec += peers_markdown(peers, "he")
    if decision:
        sec += decision_markdown(decision, "he")
    sec += analysts_he(an)
    sec += report_he(ea)
    sec += fundamentals_he(fu)
    sec += read_he(label, score, fired)
    return sec


# ----------------------------------------------------------------------------
# the journal
# ----------------------------------------------------------------------------
def journal_he(out_dir: Path) -> List[str]:
    md = ["## 6. מבחן קדימה (היומן)", ""]
    p = Path(out_dir) / "mark_to_market.csv"
    if not p.exists():
        return md + ["אין יומן עדיין.", ""]
    mtm = pd.read_csv(p)
    from algovision.journal import RETIRED_RULES, expectation_table
    mtm = mtm[~mtm["rule"].isin(RETIRED_RULES)] if len(mtm) else mtm
    if not len(mtm):
        return md + ["אין איתותים רשומים עדיין.", ""]
    md += ["### תוצאות שוטפות", "",
           "ציפייה מול מציאות (כל העסקאות שנרשמו, סגורות ופתוחות לפי שווי שוק; \"מול סל המוכות\" = פחות התשואה שווה-המשקל של המניות שהיו מוכות "
           "ביום האיתות על פני אותו חלון, ההשוואה ההוגנת לכלל שקונה רק מניות מוכות):", "", expectation_table(mtm, "he")]
    for rule, g in mtm.groupby("rule"):
        closed = g[g["done"].astype(bool)]
        open_ = g[~g["done"].astype(bool)]
        md.append(f"**{RULE_HE.get(rule, rule)}** (`{rule}`; צפוי: {RULE_EXPECT_HE.get(rule, RULES.get(rule, {}).get('expect', ''))})")
        md.append(f"- נרשמו: {len(g)}, נסגרו: {len(closed)}, פתוחות: {len(open_)}")
        if len(closed):
            r = closed["ret"].astype(float)
            md.append(f"- עסקאות סגורות: ממוצע {r.mean() * 100:+.2f}%, חציון {r.median() * 100:+.2f}%, הצלחה {(r > 0).mean() * 100:.0f}%, "
                      f"הטובה {r.max() * 100:+.1f}%, הגרועה {r.min() * 100:+.1f}%")
        if len(open_):
            r = open_["ret"].astype(float).dropna()
            if len(r):
                md.append(f"- עסקאות פתוחות לפי שווי שוק: ממוצע {r.mean() * 100:+.2f}%, הצלחה {(r > 0).mean() * 100:.0f}%")
        sp = g["spy_ret"].astype(float).dropna() if "spy_ret" in g.columns else pd.Series(dtype=float)
        if len(sp):
            md.append(f"- SPY על פני אותן תקופות החזקה: ממוצע {sp.mean() * 100:+.2f}% (עודף {(g['ret'].astype(float).dropna().mean() - sp.mean()) * 100:+.2f}%)")
        bk = g["basket_ret"].astype(float).dropna() if "basket_ret" in g.columns else pd.Series(dtype=float)
        if len(bk):
            md.append(f"- סל המניות המוכות על פני אותן תקופות: ממוצע {bk.mean() * 100:+.2f}% (עודף {(g['ret'].astype(float).dropna().mean() - bk.mean()) * 100:+.2f}%)")
        md.append("")
    open_ = mtm[~mtm["done"].astype(bool)]
    if len(open_):
        t = pd.DataFrame({
            "כלל": open_["rule"].map(lambda r: RULE_HE.get(r, r)), "סימול": open_["symbol"].map(_tv), "תאריך האיתות": open_["signal_date"],
            "תאריך כניסה": open_["entry_date"].fillna(""), "מחיר כניסה": open_["entry_price"].map(lambda v: "" if pd.isna(v) else f"{float(v):.2f}"),
            "נרות שחלפו": open_["bars_elapsed"].map(lambda v: "" if pd.isna(v) else f"{int(v)}"), "נרות החזקה": open_["hold_bars"],
            "תשואה": open_["ret"].map(lambda v: "" if pd.isna(v) else f"{float(v) * 100:+.2f}%"),
            "SPY באותה תקופה": open_["spy_ret"].map(lambda v: "" if pd.isna(v) else f"{float(v) * 100:+.2f}%")})
        md += ["### פוזיציות פתוחות", "", t.to_markdown(index=False), ""]
    return md


# ----------------------------------------------------------------------------
# the file
# ----------------------------------------------------------------------------
def build_daily_he(out_dir: Path, today: str, last_bar: str, n_frames: int, n_symbols: int, insider_days: int, sig: pd.DataFrame, tx: pd.DataFrame,
                   nd: pd.DataFrame, wedges: Dict, rally: pd.DataFrame, rows: List[Dict], frames: Dict[str, pd.DataFrame], peers: Dict[str, Dict],
                   decisions: Dict[str, Dict], picks: List[str], sectors: Dict[str, str], bench: Optional[pd.DataFrame], note_he: str,
                   regime: Optional[Dict] = None, days: Optional[Dict] = None, lookback: Optional[Dict] = None,
                   skips: Optional[List[str]] = None) -> Path:
    """Write ``daily_<today>.md`` / ``daily_latest.md`` and return the dated path."""
    from algovision.checklist import checklist_markdown
    from algovision.lookback import lookback_markdown
    from algovision.regime import regime_markdown

    out_dir = Path(out_dir)
    peers = peers or {}
    decisions = decisions or {}
    regime = regime or {}
    by_sym = {r["symbol"]: r for r in rows if r.get("_data")}
    spy_below = _spy_below_ma200(bench)
    md = [f"# AlgoVision: הדוח היומי בעברית - {today}", "",
          f"מחירים עד {last_bar}; {n_frames} מתוך {n_symbols} סימולים. כל סימול מקושר לגרף TradingView שלו; \"פירוט\" מקפיץ לסעיף המניה בקובץ הזה.", ""]
    if regime:
        md += regime_markdown(regime, "he")
    md += ["**מה בקובץ.** (0) מה חדש מאז הדוח הקודם; (1) קניות אינסיידרים; (2) טבלאות האיתותים: יום חדשות, טריז יורד מאושר (עם הניתוח הטכני בסעיף כל מניה), "
          "ראלי מוקדם, ורשימת המעקב של הטריזים בהתהוות; (3) רשימת הבדיקות, טבלת תקציר לכל מניה עם דגלי האזהרה, והחלטות המודל (Jev); (4) סעיף מלא לכל מניה: "
          "סיכום בקצרה, הסיפור לאורך ציר הזמן (חמש שנים בחמישה פרקים), הניתוח הטכני של הטריז (למניות הטריז), איפה המניה, למה ירדה והחדשות האחרונות, "
          "חששות המשקיעים והסנטימנט, עמיתים וקבוצת ההשוואה, החלטת המודל, אנליסטים, הדוח האחרון והתחזיות, נתוני יסוד וקריאה מבוססת כללים; (5) מה עבד עד "
          "עכשיו: המאזן של כל שם שהדוחות הציגו; (6) יומן מבחן הקדימה: ציפייה מול מציאות, תוצאות כל כלל וכל פוזיציה פתוחה. \"למה ירדה\" ו\"הסיפור\" "
          "מציינים רק ראיות שנמצאו בנתונים (כותרות שמזכירות את החברה, דיווחי 8-K, דוחות ב-XBRL, הורדות דירוג, ימי שוק) או \"לא נמצא\"; שום דבר לא "
          "מומצא. הכותרות, שמות החברות ובתי ההשקעות מובאים כפי שפורסמו. סינון שיטתי ומבחן קדימה, לא ייעוץ השקעות.", "",
          "## 0. מה חדש", "", note_he.strip(), ""]
    md += insiders_he(sig, tx, sectors, insider_days, days)
    md += ["## 2. איתותים לטווח קצר", ""]
    md += newsday_he(nd, sectors, days)
    wedge_data = {s: by_sym[s]["_data"] for s in wedges if s in by_sym}
    md += wedge_table_he(wedges, frames, wedge_data, peers, decisions, sectors, days)
    md += rally_table_he(rally, peers, sectors, days)
    md += wedge_table_he(wedges, frames, wedge_data, peers, decisions, sectors, days, watch=True)
    md += ["*ימים ברשימה*: בכמה מהדוחות (מתוך 30 האחרונים) השם ישב בטבלה הזאת, כולל היום. בחמשת השבועות הראשונים השמות שהופיעו 4-7 ימים היו הגרועים; "
           "רישום טרי היה טוב מרישום ישן.", ""]
    md += ["<a id=\"summary\" name=\"summary\"></a>", "## 3. רשימת הבדיקות, תקציר לכל מניה והחלטות המודל", ""]
    md += checklist_markdown(rows, "he", regime.get("warning"), anchor=_anchor)
    md += summary_table_he(rows, title=False)
    anchors = {s: _anchor(s) for s in by_sym}
    md += jev_he(decisions, picks, anchors, peers, skips)
    md += ["## 4. פירוט לכל מניה", ""]
    order = sorted(by_sym, key=lambda s: ({"signs of a bottom": 0, "undecided": 1, "still falling": 2}.get(by_sym[s].get("read"), 3), -(by_sym[s].get("score") or 0)))
    for s in order:
        if s not in frames:
            continue
        md += stock_section_he(s, by_sym[s], frames[s], wedges.get(s), peers.get(s), decisions.get(s), sectors, spy_below)
        md.append("")
    if lookback and lookback.get("rows"):
        md += [line.replace("## 4. מה עבד", "## 5. מה עבד") for line in lookback_markdown(lookback["rows"], lookback["forward"], "he")]
    else:
        md += ["## 5. מה עבד עד עכשיו", "", "אין עדיין מספיק דוחות למאזן.", ""]
    md += journal_he(out_dir)
    md += ["---", "סינון שיטתי ומבחן קדימה, לא ייעוץ השקעות. הטיית שרידות חלה על כל הבדיקות לאחור (חברות המדד של היום); ראו docs/research*.md לשיטות ולהסתייגויות.", ""]
    text = "\n".join(md)
    path = out_dir / f"daily_{today}.md"
    path.write_text(text, encoding="utf-8")
    (out_dir / "daily_latest.md").write_text(text, encoding="utf-8")
    return path
