"""One small file, in Hebrew, for one rule: the Falling Wedge in beaten-down stocks.

``wedge_<date>.md`` / ``wedge_latest.md`` next to the daily report: a summary table whose every row links to the
TradingView chart and, inside the file, to a per-stock section with the full technical analysis of the wedge
(structure, slopes, convergence, containment, breakout, levels, the context features the research found to matter),
why the stock fell (only evidence found in the data), analysts, the last report, fundamentals and the rule-based
read. Everything the program says is in Hebrew; headlines, company names and analyst firms stay as published.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

from algovision.briefs import (_company_tokens, _money, _num, _pct, analyst_view, decline_reason, earnings_view, fetch_sources, fundamentals_view,
                               price_context, render_signals, verdict_signals)
from algovision.core.geometry import volume_ratio
from algovision.core.types import PatternMatch
from algovision.links import tradingview_url
from algovision.sentiment import LABEL_HE as SENT_HE, sentiment_markdown, sentiment_view

# ----------------------------------------------------------------------------
# Hebrew vocabulary
# ----------------------------------------------------------------------------
SECTOR_HE = {
    # Yahoo Finance sectors
    "Consumer Cyclical": "צריכה מחזורית", "Consumer Defensive": "צריכה בסיסית", "Technology": "טכנולוגיה",
    "Financial Services": "שירותים פיננסיים", "Healthcare": "בריאות", "Industrials": "תעשייה", "Utilities": "תשתיות",
    "Basic Materials": "חומרי גלם", "Communication Services": "שירותי תקשורת", "Energy": "אנרגיה", "Real Estate": "נדל\"ן",
    # GICS sectors (the universe snapshot)
    "Consumer Discretionary": "צריכה מחזורית", "Consumer Staples": "צריכה בסיסית", "Information Technology": "טכנולוגיית מידע",
    "Financials": "פיננסים", "Health Care": "בריאות", "Materials": "חומרים",
}
STATUS_HE = {"confirmed": "מאושר", "forming": "בהתהוות", "failed": "נכשל", "expired": "פג"}
LABEL_HE = {"up": "סימני תחתית (סביר יותר למעלה מאשר למטה)", "flat": "לא מוכרע (אין עדיין בסיס ברור)", "down": "עדיין יורדת (סביר יותר למטה)"}
LABEL_SHORT_HE = {"up": "סימני תחתית", "flat": "לא מוכרע", "down": "עדיין יורדת"}
CONSENSUS_HE = {"strong_buy": "קנייה חזקה", "buy": "קנייה", "hold": "החזקה", "underperform": "ביצועי חסר", "sell": "מכירה",
                "strong_sell": "מכירה חזקה"}
ACTION_HE = {"up": "מעלה דירוג", "down": "מוריד דירוג", "main": "מותיר", "reit": "מאשר מחדש", "init": "מתחיל כיסוי"}
CAUSE_HE = {"earnings": "דוח רבעוני", "guidance": "תחזית", "rating cut": "הורדת דירוג", "legal/regulatory": "משפטי/רגולטורי",
            "deal/financing": "עסקה/מימון", "management": "הנהלה", "demand/competition": "ביקוש/תחרות", "news": "חדשות",
            "market-wide": "יום שוק", "restructuring": "ארגון מחדש", "impairment": "הפחתת ערך", "restatement": "הצגה מחדש",
            "bankruptcy": "פשיטת רגל", "auditor change": "החלפת רואה חשבון", "company disclosure (8-K)": "דיווח חברה (8-K)",
            "heavy volume, cause not found": "נפח כבד, סיבה לא נמצאה", "not found": "לא נמצא"}
ITEM_HE = {"2.02": "פרסום תוצאות", "5.02": "שינוי בהנהלה או בדירקטוריון", "2.05": "ארגון מחדש", "2.06": "הפחתת ערך",
           "1.01": "הסכם מהותי", "1.02": "סיום הסכם מהותי", "2.01": "השלמת רכישה או מכירה", "2.03": "יצירת התחייבות כספית",
           "3.02": "הנפקת ניירות ערך", "4.02": "הצגה מחדש של דוחות", "1.03": "פשיטת רגל", "4.01": "החלפת רואה חשבון",
           "7.01": "גילוי לפי Regulation FD", "8.01": "אירועים אחרים"}
SIGNAL_HE = {
    "above_ma50": "המחיר מעל הממוצע הנע של 50 יום", "below_ma50": "המחיר מתחת לממוצע הנע של 50 יום",
    "ma50_up": "הממוצע הנע של 50 יום מתחיל לעלות", "higher_low": "שפל גבוה יותר ב-20 הנרות האחרונים מאשר ב-20 שלפניהם",
    "new_low": "שפל 52 שבועות חדש ב-5 הנרות האחרונים",
    "consensus_buy": "קונצנזוס אנליסטים {key} ({n} אנליסטים)", "consensus_sell": "קונצנזוס אנליסטים {key}",
    "target_far": "יעד המחיר הממוצע {up} מעל המחיר", "target_near": "יעד המחיר הממוצע רק {up} מהמחיר",
    "more_upgrades": "יותר העלאות דירוג מהורדות ב-90 יום ({n_up} מול {n_down})",
    "more_downgrades": "יותר הורדות דירוג מהעלאות ב-90 יום ({n_down} מול {n_up})",
    "target_cuts": "אנליסטים מורידים יעדי מחיר ({cuts} הורדות מול {raises} העלאות ב-90 יום)",
    "target_raises": "אנליסטים מעלים יעדי מחיר ({raises} העלאות מול {cuts} הורדות ב-90 יום)",
    "revisions_down": "עדכוני תחזית בעיקר כלפי מטה ({up} למעלה / {down} למטה ב-30 יום)",
    "revisions_up": "עדכוני תחזית בעיקר כלפי מעלה ({up} למעלה / {down} למטה ב-30 יום)",
    "eps_raised": "תחזית הרווח למניה לשנה הנוכחית הועלתה {r30} ב-30 יום",
    "eps_cut": "תחזית הרווח למניה לשנה הנוכחית הורדה {r30} ב-30 יום",
    "beat": "הרבעון האחרון היכה את התחזיות ({sp})", "miss": "הרבעון האחרון פספס את התחזיות ({sp})",
    "revenue_up": "ההכנסות צומחות ({rg} שנה מול שנה)", "revenue_down": "ההכנסות מתכווצות ({rg} שנה מול שנה)",
    "fcf_positive": "תזרים מזומנים חופשי חיובי", "fcf_negative": "תזרים מזומנים חופשי שלילי",
    "leverage": "מינוף גבוה (חוב/הון {de})",
    "forward_pe_lower": "מכפיל רווח עתידי {fpe} נמוך מהמכפיל הנוכחי {pe} (צפי לצמיחת רווחים)",
    "insiders": "אינסיידרים קנו (מופיעה בטבלת האינסיידרים של היום)",
}


def _he_consensus(key: Optional[str]) -> str:
    k = (key or "").lower().replace(" ", "_")
    return CONSENSUS_HE.get(k, key or "")


def _he_cause(cause: str) -> str:
    if not cause:
        return CAUSE_HE["not found"]
    if cause in CAUSE_HE:
        return CAUSE_HE[cause]
    return ", ".join(CAUSE_HE.get(part.strip(), part.strip()) for part in cause.split(","))


def _he_sector(name: Optional[str]) -> str:
    return SECTOR_HE.get(name or "", name or "")


def _anchor(symbol: str) -> str:
    return "wedge-" + "".join(ch if ch.isalnum() else "-" for ch in symbol.lower())


def _yesno(v) -> str:
    return "" if v is None else ("כן" if v else "לא")


# ----------------------------------------------------------------------------
# the wedge itself
# ----------------------------------------------------------------------------
def wedge_geometry(m: PatternMatch, df: pd.DataFrame) -> Dict:
    """Numbers about the wedge that the detector does not store directly: heights, touches, breakout volume, apex distance."""
    close = df["Close"].to_numpy(dtype=float)
    vol = df["Volume"].to_numpy(dtype=float) if "Volume" in df.columns else None
    upper = next((ln for ln in m.lines if ln.label == "Upper line"), None)
    lower = next((ln for ln in m.lines if ln.label == "Lower line"), None)
    x0 = m.start_idx
    x1 = max((kp.idx for kp in m.key_points), default=m.end_idx)      # last touch
    h0 = (upper.value_at(x0) - lower.value_at(x0)) if upper and lower else np.nan
    h1 = (upper.value_at(x1) - lower.value_at(x1)) if upper and lower else np.nan
    price = float(np.mean(close[x0:x1 + 1])) if x1 >= x0 else float(close[-1])
    n = len(close)
    highs = [kp for kp in m.key_points if kp.label == "H"]
    lows = [kp for kp in m.key_points if kp.label == "L"]
    apex = m.metrics.get("apex")
    bo = m.breakout_idx
    bo_vol = volume_ratio(vol, bo, 20) if (bo is not None and vol is not None) else None
    return {
        "x0": x0, "x1": x1, "width": x1 - x0, "h0": h0, "h1": h1, "h0_pct": h0 / price if price else np.nan,
        "highs": highs, "lows": lows,
        "upper_now": upper.value_at(n - 1) if upper else np.nan, "lower_now": lower.value_at(n - 1) if lower else np.nan,
        "apex_bars": (int(apex) - x1) if apex is not None else None,
        "breakout_volume": bo_vol, "breakout_line": upper.value_at(bo) if (bo is not None and upper) else np.nan,
        "bars_since_breakout": (n - 1 - bo) if bo is not None else None,
    }


def _components_he(comp: Dict[str, float]) -> str:
    names = {"touches": "נגיעות", "fit": "התאמה לקווים", "convergence": "התכנסות", "containment": "הכלה", "volume": "נפח",
             "trend": "מגמה קודמת", "breakout_volume": "נפח הפריצה"}
    return ", ".join(f"{names.get(k, k)} {v:.2f}" for k, v in comp.items())


def wedge_section_he(m: PatternMatch, df: pd.DataFrame, geo: Dict, ctx: Dict, spy_below_ma200: Optional[bool]) -> List[str]:
    """The technical analysis of one wedge, as Hebrew bullet points."""
    mt = m.metrics
    cx = mt.get("context", {})
    last = float(df["Close"].iloc[-1])
    md = ["### הניתוח הטכני של הטריז", ""]
    md.append(f"- **מבנה:** הטריז נמשך {geo['width']} נרות, מ-{m.start_date} עד {df.index[geo['x1']].strftime('%Y-%m-%d')} (הנגיעה האחרונה). "
              f"{len(geo['highs'])} שיאים נוגעים בקו העליון היורד ו-{len(geo['lows'])} שפלים נוגעים בקו התחתון היורד; "
              f"הסטייה המקסימלית מהקווים {mt.get('max_residual', 0) * 100:.0f}% מגובה התבנית.")
    md.append(f"- **שיפועים והתכנסות:** הקו העליון יורד ב-{abs(mt.get('upper_slope', 0)) * 100:.0f}% מהגובה ההתחלתי לאורך התבנית "
              f"והקו התחתון ב-{abs(mt.get('lower_slope', 0)) * 100:.0f}%, כלומר הקו העליון תלול יותר והטווח נסגר. "
              f"הגובה מתכווץ {mt.get('convergence', 0) * 100:.0f}%, מ-{geo['h0']:.2f} ל-{geo['h1']:.2f} "
              f"(גובה התחלתי {geo['h0_pct'] * 100:.1f}% מהמחיר)"
              + (f"; הקודקוד צפוי {geo['apex_bars']} נרות אחרי הנגיעה האחרונה." if geo["apex_bars"] is not None else "."))
    md.append(f"- **הכלה:** המחיר נשאר בתוך הגבולות {100 - mt.get('violations', 0) * 100:.0f}% מהזמן.")
    vt = mt.get("volume_trend")
    if vt is not None:
        md.append(f"- **נפח:** {'התכווץ' if vt < 0 else 'התרחב'} {abs(vt) * 100:.0f}% במהלך התבנית"
                  + (" (התכווצות היא הצורה הקלאסית של דשדוש)" if vt < 0 else "")
                  + "; המחקר מצא שהנפח לא משנה את התוצאה.")
    pt = mt.get("prior_trend")
    if pt is not None and abs(pt) > 0.03:
        md.append(f"- **התנועה לפני התבנית:** {_pct(pt, 1)} ב-{max(geo['width'], 20)} הנרות שלפני תחילת הטריז"
                  + (" (עלייה לתוך הטריז: התבנית היא מנוחה בתוך התאוששות)." if pt > 0 else " (ירידה לתוך הטריז: המחקר מצא שירידה תלולה יותר לפני התבנית עדיפה)."))
    if m.status == "confirmed" and m.breakout_idx is not None:
        bv = geo["breakout_volume"]
        bv_txt = ("" if bv is None else f"; נפח הפריצה {bv:.1f}x הממוצע של 20 נרות ("
                  + ("אישור חזק" if bv >= 1.5 else "אישור סביר" if bv >= 1.1 else "אישור חלש") + ")")
        md.append(f"- **פריצה:** ב-{m.breakout_date} סגירה {m.breakout_price:.2f} מעל הקו העליון ({geo['breakout_line']:.2f}), "
                  f"לפני {geo['bars_since_breakout']} נרות{bv_txt}. "
                  f"מאז הפריצה: {_pct(last / m.breakout_price - 1, 1)}"
                  + (f"; הטוב ביותר {_pct(m.outcome.get('max_favorable'), 1)}, הגרוע ביותר {_pct(m.outcome.get('max_adverse'), 1)}"
                     if m.outcome and m.outcome.get("max_favorable") is not None else "") + ".")
    else:
        md.append(f"- **מצב:** עדיין בתוך הטריז, אין איתות. הקו העליון כעת ~{geo['upper_now']:.2f} ({_pct(geo['upper_now'] / last - 1, 1)} מהמחיר), "
                  f"הקו התחתון ~{geo['lower_now']:.2f} ({_pct(geo['lower_now'] / last - 1, 1)}), סגירה אחרונה {last:.2f}. "
                  f"איתות = סגירה מעל הקו העליון.")
    stop_pct = (m.stop / last - 1) if m.stop else np.nan
    tgt_pct = (m.target / last - 1) if m.target else np.nan
    md.append(f"- **רמות:** רמת הפריצה {m.level:.2f}, סטופ בתחתית הטריז {m.stop:.2f} ({_pct(stop_pct, 1)} מהמחיר האחרון), "
              f"יעד מדוד (ראש הטריז) {m.target:.2f} ({_pct(tgt_pct, 1)}; במחקר היעד מושג רק בכ-32% מהמקרים).")
    beaten = cx.get("beaten_down")
    md.append(f"- **הקשר (מה שניבא תוצאות במחקר):** תשואת 6 חודשים {_pct(cx.get('ret_126'), 1)}, "
              f"{abs(cx.get('dist_ma200', 0)) * 100:.1f}% {'מתחת ל' if cx.get('dist_ma200', 0) < 0 else 'מעל ה'}ממוצע הנע של 200 יום "
              f"(מניה מוכה: {_yesno(beaten)}); ATR {cx.get('atr_pct', 0) * 100:.1f}% מהמחיר; גובה הטריז {geo['h0_pct'] * 100:.1f}% מהמחיר"
              + (f"; SPY {'מתחת ל' if spy_below_ma200 else 'מעל ה'}ממוצע הנע של 200 יום שלו "
                 f"({'שוק חלש' if spy_below_ma200 else 'שוק חזק'})." if spy_below_ma200 is not None else "."))
    md.append(f"- **מיקום המחיר:** אחרון {ctx['last']:.2f}, {_pct(ctx['drawdown'])} משיא 52 שבועות ({ctx['high_52w']:.2f} ב-{ctx['high_date']}), "
              f"{_pct(ctx['off_low'])} מעל שפל 52 שבועות ({ctx['low_52w']:.2f} ב-{ctx['low_date']}). "
              f"חודש {_pct(ctx['ret_1m'])}, 3 חודשים {_pct(ctx['ret_3m'])}, 6 חודשים {_pct(ctx['ret_6m'])}, שנה {_pct(ctx['ret_1y'])}; "
              f"מול ממוצע 50 {_pct(ctx['dist_ma50'])}, מול ממוצע 200 {_pct(ctx['dist_ma200'])}; RSI(14) {ctx['rsi14']:.0f}; "
              f"שפל עולה ב-20 הנרות האחרונים: {_yesno(ctx.get('higher_low')) or 'אין נתון'}; "
              f"שפל 52 שבועות חדש ב-5 הנרות האחרונים: {_yesno(ctx.get('new_low_5d'))}.")
    md.append(f"- **ציון הדטקטור {m.score:.2f}** (רכיבים: {_components_he(mt.get('components', {}))}).")
    md.append("")
    return md


# ----------------------------------------------------------------------------
# why it fell, analysts, report, fundamentals, read: Hebrew renderings of the brief building blocks
# ----------------------------------------------------------------------------
def why_fell_he(why: Dict, news: List[Dict]) -> List[str]:
    md = ["### למה המניה ירדה", ""]
    big = ""
    if why.get("high_date"):
        big = (f"מהשיא של 52 השבועות ({why['high_52w']:.2f} ב-{why['high_date']}) המניה ירדה {abs(why['drawdown']) * 100:.0f}%"
               + (f"; {why['n_earnings_days']} ימי התגובה לדוחות שלהלן הורידו אותה יחד {abs(why['earnings_days_ret']) * 100:.1f}%. "
                  if why.get("n_earnings_days") else ". "))
    if why["found"]:
        md.append(big + f"סיבות שנמצאו בנתונים: **{_he_cause(why['cause'])}**. ימי הירידה הגדולים בשנה האחרונה, וכל יום תגובה לדוח שנסגר "
                  "בירידה, עם הראיות סביב כל אחד:")
    else:
        md.append(big + "לא נמצאה סיבה בנתונים: אין כותרת שמזכירה את החברה עם סיבה מוצהרת בטווח יומיים מימי הירידה הגדולים, אין דיווח 8-K "
                  "(פרסום תוצאות, שינוי בהנהלה, עסקה) באותם ימים, אין הורדת דירוג או יעד מיד אחרי, ואין יום ירידה כלל-שוקי. "
                  "ימי הירידה הגדולים בשנה האחרונה:")
    for d in why["days"]:
        extra = ", ".join(x for x in (("יום תגובה לדוח" if d.get("kind") == "earnings" else ""),
                                      (f"נפח {d['volume_ratio']:.1f}x מהרגיל" if d.get("volume_ratio") else ""),
                                      (f"SPY {_pct(d['spy'], 1)}" if d.get("spy") is not None else "")) if x)
        line = f"- {d['day']}: {_pct(d['ret'], 1)}" + (f" ({extra})" if extra else "")
        items: List[str] = []
        for f in d.get("filings", []):
            what = "; ".join(ITEM_HE.get(c, w) for c, w in zip(f["codes"], f["what"]))
            eps = f.get("eps")
            if eps:
                what += (f" (רבעון עד {eps['quarter']}: רווח למניה {_num(eps['actual'], 2)} מול {_num(eps.get('estimate'), 2)} צפוי"
                         + (f", {_pct(eps['surprise'], 1)}" if eps.get("surprise") is not None else "") + ")")
            items.append(f"דיווח 8-K מ-{f['date']}: {what}")
        for h in d.get("headlines", []):
            items.append(f"כותרת ({', '.join(CAUSE_HE.get(c, c) for c in h.get('causes', []))}): {h['date']} \"{h['title']}\""
                         + (f" ({h['publisher']})" if h.get("publisher") else "") + (f": {h['summary']}" if h.get("summary") else ""))
        if d.get("cuts"):
            items.append("הורדות דירוג/יעד מיד אחרי: " + "; ".join(
                f"{c['firm']} {'הורדת דירוג' if c['kind'] == 'downgrade' else 'הורדת יעד'}"
                + (f" {_num(c['prior_target'], 0)} -> {_num(c['target'], 0)}" if c.get("target") and c.get("prior_target") else "")
                for c in d["cuts"]))
        if d.get("spy") is not None and d["spy"] <= -0.015:
            items.append(f"יום ירידה כלל-שוקי: SPY {_pct(d['spy'], 1)}")
        if items:
            md.append(line + ":")
            md += [f"  - {x}" for x in items]
        elif d.get("before_feed"):
            md.append(line + f". לא נמצאה סיבה ליום זה (לפני תחילת פיד החדשות ב-{why['oldest_news']}; נבדקו רק דיווחי 8-K, שינויי דירוג והשוק).")
        else:
            md.append(line + ". לא נמצאה סיבה ליום זה.")
    if news:
        md.append("")
        md.append("חדשות אחרונות (הכותרות כפי שפורסמו): " + "; ".join(
            f"{x['date']} \"{x['title']}\"" + (f" ({x['publisher']})" if x.get("publisher") else "") for x in news[:3]) + ".")
    md.append("")
    return md


def summary_he(m: PatternMatch, geo: Dict, ctx: Dict, why: Dict, sent: Dict, an: Dict, ea: Dict, label: str, score: float) -> List[str]:
    """Five short lines at the top of a stock's section: the wedge and its levels, how beaten the stock is, why it fell,
    what worries investors and the sentiment, what analysts expect and the rule-based read. Data only."""
    last = ctx["last"]
    if m.status == "confirmed" and m.breakout_date:
        state = f"פרץ מעל הקו העליון ב-{m.breakout_date} (רמת הפריצה {m.level:.2f})"
    else:
        state = f"המחיר עדיין בתוך הטריז, הקו העליון עכשיו ב-{geo['upper_now']:.2f}" if geo.get("upper_now") == geo.get("upper_now") else "המחיר עדיין בתוך הטריז"
    stop_pct = m.stop / last - 1 if last else float("nan")
    md = ["**בקצרה:**",
          f"- **הטריז:** {STATUS_HE.get(m.status, m.status)}, {geo['width']} נרות מ-{m.start_date}; {state}. מחיר אחרון {last:.2f}, "
          f"סטופ {m.stop:.2f} ({_pct(stop_pct, 1)} מהמחיר), יעד {m.target:.2f}."]
    cx = m.metrics.get("context", {})
    md.append(f"- **כמה מוכה:** {abs(ctx['drawdown']) * 100:.0f}% מתחת לשיא של 52 השבועות ({ctx['high_date']}), "
              f"6 חודשים {_pct(cx.get('ret_126'))}, {_pct(cx.get('dist_ma200'))} מול ממוצע 200, ATR {cx.get('atr_pct', 0) * 100:.1f}% ליום.")
    # the strongest evidence: the first headline of the largest day that has one, else the largest day's filing
    quote = ""
    for d in why.get("days", []):
        if d.get("headlines"):
            h = d["headlines"][0]
            quote = f" למשל {d['day']} ({_pct(d['ret'], 1)}): \"{h['title']}\"" + (f" ({h['publisher']})" if h.get("publisher") else "") + "."
            break
    md.append(f"- **למה ירדה:** {_he_cause(why['cause'])}." + quote if why.get("found") else
              "- **למה ירדה:** לא נמצאה סיבה בנתונים (כותרות, דיווחי 8-K, הורדות דירוג, ימי שוק).")
    themes = ", ".join(t["he"] for t in sent["concerns"]["themes"][:3])
    neg = sum(1 for _, sg, _ in sent["signals"] if sg < 0)
    pos = sum(1 for _, sg, _ in sent["signals"] if sg > 0)
    md.append("- **חששות וסנטימנט:** " + (f"הכותרות השליליות עוסקות ב{themes}. " if themes else "לא נמצאו כותרות שליליות על החברה בשנה האחרונה. ")
              + f"סנטימנט {SENT_HE[sent['label']]} ({neg} איתותים שליליים, {pos} חיוביים).")
    an_txt = (f"קונצנזוס {_he_consensus(an.get('key'))} ({an.get('n') or '?'} אנליסטים), יעד ממוצע {_num(an.get('target'), 2)} "
              f"({_pct(an.get('upside'))} מהמחיר)" if an.get("key") else "אין קונצנזוס אנליסטים")
    md.append(f"- **אנליסטים וקריאה:** {an_txt}"
              + (f"; הדוח הבא {ea['next_date']}" if ea.get("next_date") else "")
              + f". קריאה מבוססת כללים: **{LABEL_SHORT_HE[label]}** (ציון {score:+g}).")
    md.append("")
    return md


def analysts_he(an: Dict) -> List[str]:
    md = ["### מה אומרים האנליסטים", ""]
    cn = an.get("counts_now") or {}
    if an.get("key"):
        md.append(f"קונצנזוס **{_he_consensus(an['key'])}** ({an.get('n') or '?'} אנליסטים"
                  + (f", דירוג ממוצע {_num(an['mean'])} בסולם 1-5" if an.get("mean") is not None else "") + ")"
                  + (f"; קנייה חזקה {cn.get('strongBuy', 0)}, קנייה {cn.get('buy', 0)}, החזקה {cn.get('hold', 0)}, מכירה {cn.get('sell', 0)}, "
                     f"מכירה חזקה {cn.get('strongSell', 0)}"
                     + (f" (חלק שורי {an['bullish_now'] * 100:.0f}% היום מול {an['bullish_3m'] * 100:.0f}% לפני שלושה חודשים)"
                        if an.get("bullish_now") is not None and an.get("bullish_3m") is not None else "") if cn else "") + ". "
                  + (f"יעד ממוצע {_num(an['target'], 2)} ({_pct(an['upside'])} מהמחיר"
                     + (f"; טווח {_num(an['target_low'], 2)}-{_num(an['target_high'], 2)}"
                        if an.get("target_low") is not None and an.get("target_high") is not None else "") + ")." if an.get("target") else ""))
    else:
        md.append("אין נתוני קונצנזוס.")
    if an.get("actions"):
        md.append(f"90 הימים האחרונים: {an.get('n_up', 0)} העלאות דירוג, {an.get('n_down', 0)} הורדות דירוג, "
                  f"{an.get('n_target_raises', 0)} העלאות יעד, {an.get('n_target_cuts', 0)} הורדות יעד.")
        for a in an["actions"][:4]:
            t, pt = a.get("target"), a.get("prior_target")
            tgt = f", יעד {_num(pt, 0)} -> {_num(t, 0)}" if t and pt and t != pt else (f", יעד {_num(t, 0)}" if t else "")
            frm, to = a.get("from") or "", a.get("to") or ""
            grade = f"{frm} -> {to}" if frm and frm != to else to
            md.append(f"- {a.get('date') or ''} {a.get('firm') or ''}: {ACTION_HE.get(a.get('action'), a.get('action') or '')} {grade}{tgt}")
    md.append("")
    return md


def report_he(ea: Dict) -> List[str]:
    md = ["### הדוח האחרון והתחזיות", ""]
    parts = []
    if ea.get("eps_actual") is not None:
        parts.append(f"רבעון עד {ea.get('last_quarter') or '?'}: רווח למניה {_num(ea['eps_actual'], 2)}"
                     + (f" מול {_num(ea['eps_est'], 2)} צפוי ({_pct(ea.get('surprise'), 1)})" if ea.get("eps_est") is not None else "")
                     + f"; היכתה את התחזית ב-{ea.get('beats_4q', 0)} מתוך {ea.get('n_4q', 0)} הרבעונים האחרונים.")
    else:
        parts.append("אין היסטוריית דוחות.")
    if ea.get("revenue_growth") is not None:
        parts.append(f"הכנסות {_pct(ea.get('revenue_growth'))} שנה מול שנה, רווח {_pct(ea.get('earnings_growth'))} שנה מול שנה (הרבעון האחרון).")
    if ea.get("q0_eps_est") is not None:
        parts.append(f"הדוח הבא {ea.get('next_date') or '(תאריך טרם פורסם)'}"
                     f"{' (תאריך משוער)' if ea.get('next_is_estimate') and ea.get('next_date') else ''}: "
                     f"רווח למניה צפוי {_num(ea['q0_eps_est'], 2)} ({_pct(ea.get('q0_growth'))} שנה מול שנה), הכנסות {_pct(ea.get('q0_rev_growth'))} שנה מול שנה.")
    if ea.get("y0_rev_30d") is not None:
        ud = ea.get("y0_up_down_30d") or (0, 0)
        parts.append(f"תחזית הרווח למניה לשנה הנוכחית {_pct(ea.get('y0_rev_30d'), 1)} ב-30 יום, {_pct(ea.get('y0_rev_90d'), 1)} ב-90 יום "
                     f"({ud[0]} עדכונים למעלה / {ud[1]} למטה); צמיחה צפויה {_pct(ea.get('y0_growth'))} השנה, {_pct(ea.get('y1_growth'))} בשנה הבאה.")
    md.append(" ".join(parts))
    md.append("")
    return md


def fundamentals_he(fu: Dict) -> List[str]:
    md = ["### נתוני יסוד", ""]
    md.append(f"שווי שוק {_money(fu.get('market_cap'))}; מכפיל רווח {_num(fu.get('pe'))} נוכחי, {_num(fu.get('forward_pe'))} עתידי, PEG {_num(fu.get('peg'), 2)}; "
              f"EV/הכנסות {_num(fu.get('ev_rev'))}, EV/EBITDA {_num(fu.get('ev_ebitda'))}, מחיר/הון {_num(fu.get('pb'))}. "
              f"שולי רווח: גולמי {_pct(fu.get('gross_margin'))}, תפעולי {_pct(fu.get('op_margin'))}, נקי {_pct(fu.get('net_margin'))}; תשואה על ההון {_pct(fu.get('roe'))}. "
              f"תזרים מזומנים חופשי {_money(fu.get('fcf'))} (תשואה {_pct(fu.get('fcf_yield'), 1)}); מזומן {_money(fu.get('cash'))}, חוב {_money(fu.get('debt'))}, "
              f"חוב/הון {_num(fu.get('debt_to_equity'), 2)}, יחס שוטף {_num(fu.get('current_ratio'), 2)}. "
              + (f"תשואת דיבידנד {_pct(fu['dividend_yield'], 1)}. " if fu.get("dividend_yield") else "")
              + (f"שורט {_pct(fu['short_pct'], 1)} מהמניות הצפות. " if fu.get("short_pct") is not None else "")
              + (f"בטא {_num(fu['beta'], 2)}." if fu.get("beta") is not None else ""))
    md.append("")
    return md


def read_he(label: str, score: float, fired) -> List[str]:
    md = ["### קריאה מבוססת כללים", ""]
    fired = [(code, pts, {**kw, "key": _he_consensus(kw["key"])} if "key" in kw else kw) for code, pts, kw in fired]
    md.append(f"**{LABEL_HE[label]}** (ציון {score:+g}). ניקוד שקוף על איתותים מפורטים, לא תחזית; האיתותים שנדלקו: "
              + ("; ".join(render_signals(fired, SIGNAL_HE)) if fired else "אין") + ".")
    md.append("")
    return md


# ----------------------------------------------------------------------------
# the file
# ----------------------------------------------------------------------------
def _spy_below_ma200(bench: Optional[pd.DataFrame]) -> Optional[bool]:
    if bench is None or len(bench) < 200:
        return None
    c = bench["Close"].astype(float)
    return bool(c.iloc[-1] < c.tail(200).mean())


def _open_positions_he(journal_dir: Path) -> List[str]:
    """The rule's open positions from the forward-test journal, if any."""
    p = journal_dir / "mark_to_market.csv"
    if not p.exists():
        return []
    try:
        mtm = pd.read_csv(p)
    except Exception:  # noqa: BLE001
        return []
    d = mtm[(mtm["rule"] == "falling_wedge_beaten_down") & (~mtm["done"].astype(bool))] if "rule" in mtm else mtm.iloc[0:0]
    if not len(d):
        return []
    t = pd.DataFrame({
        "סימול": d["symbol"].map(lambda s: f"[{s}]({tradingview_url(s)})"), "תאריך איתות": d["signal_date"], "תאריך כניסה": d["entry_date"].fillna(""),
        "מחיר כניסה": d["entry_price"].map(lambda v: "" if pd.isna(v) else f"{v:.2f}"), "נרות שחלפו": d["bars_elapsed"].map(lambda v: "" if pd.isna(v) else f"{int(v)}"),
        "נרות החזקה": d["hold_bars"], "תשואה": d["ret"].map(lambda v: "" if pd.isna(v) else f"{v * 100:+.2f}%"),
        "SPY באותה תקופה": d["spy_ret"].map(lambda v: "" if pd.isna(v) else f"{v * 100:+.2f}%")})
    return ["## פוזיציות פתוחות של הכלל ביומן (מבחן קדימה)", "", t.to_markdown(index=False), ""]


def build_wedge_report(out_dir: Path, today: str, frames: Dict[str, pd.DataFrame], matches: Dict[str, PatternMatch],
                       sectors: Optional[Dict[str, str]] = None, cache_dir: Optional[Path] = None, workers: int = 4,
                       bench: Optional[pd.DataFrame] = None, offline: bool = False, briefs_data: Optional[Dict[str, Dict]] = None) -> Path:
    """Write ``wedge_<today>.md`` / ``wedge_latest.md`` for the given falling-wedge matches (one per symbol)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    sectors = sectors or {}
    symbols = [s for s in matches if s in frames]
    if briefs_data is None:
        from algovision.data.briefs_data import BriefsProvider
        from algovision.data.provider import _DEFAULT_CACHE
        briefs_data = BriefsProvider(cache_dir=cache_dir or _DEFAULT_CACHE, workers=workers, offline=offline).get_many(symbols) if symbols else {}
    spy_below = _spy_below_ma200(bench)
    last_bar = max((pd.Timestamp(frames[s].index[-1]) for s in symbols), default=pd.Timestamp(today)).strftime("%Y-%m-%d")

    rows, sections = [], []
    order = sorted(symbols, key=lambda s: (matches[s].status != "confirmed", -matches[s].score))
    for s in order:
        m, df = matches[s], frames[s]
        data = briefs_data.get(s) or {}
        profile, news = data.get("profile") or {}, data.get("news") or []
        ctx = price_context(df)
        an, ea, fu = analyst_view(profile), earnings_view(profile), fundamentals_view(profile)
        label, score, fired = verdict_signals(ctx, an, ea, fu)
        name = fu.get("name") or ""
        src = fetch_sources(s, name, cache_dir, offline)
        why = decline_reason(s, name, ctx, news, an, ea, bench, filings=data.get("filings") or [],
                             earn_hist=(profile.get("earningsHistory") or {}).get("history") or [], extra_headlines=src["around"])
        sent = sentiment_view(src["year"], why["window_headlines"], _company_tokens(s, name), profile, src["twits"], an, ea)
        geo = wedge_geometry(m, df)
        last = ctx["last"]
        rows.append({
            "סימול": f"[{s}]({tradingview_url(s)})", "פירוט": f"[פירוט](#{_anchor(s)})", "סטטוס": STATUS_HE.get(m.status, m.status),
            "ציון": f"{m.score:.2f}", "התחלה": m.start_date, "פריצה": m.breakout_date or "",
            "רמה": f"{m.level:.2f}", "סטופ": f"{m.stop:.2f}", "יעד": f"{m.target:.2f}", "אחרון": f"{last:.2f}",
            "מהסטופ": _pct(m.stop / last - 1 if last else np.nan),
            "6 חודשים": _pct(m.metrics.get("context", {}).get("ret_126")), "מול ממוצע 200": _pct(m.metrics.get("context", {}).get("dist_ma200")),
            "ATR%": f"{m.metrics.get('context', {}).get('atr_pct', 0) * 100:.1f}%", "גובה הטריז": f"{geo['h0_pct'] * 100:.0f}%",
            "למה ירדה": _he_cause(why["cause"]), "חששות": ", ".join(t["he"] for t in sent["concerns"]["themes"][:2]) or "לא נמצאו",
            "סנטימנט": SENT_HE[sent["label"]], "קריאה": LABEL_SHORT_HE[label], "ציון קריאה": f"{score:+g}",
            "סקטור": _he_sector(fu.get("sector") or sectors.get(s)),
        })
        sec = [f"<a id=\"{_anchor(s)}\" name=\"{_anchor(s)}\"></a>", f"## {s} - {fu.get('name') or s}", "",
               f"[גרף ב-TradingView]({tradingview_url(s)}) · [חזרה לטבלה](#summary)", "",
               f"*{_he_sector(fu.get('sector') or sectors.get(s))}" + (f" / {fu['industry']}" if fu.get("industry") else "") + ".*"
               + (f" *{fu['summary'].rstrip('.')}.*" if fu.get("summary") else ""), ""]
        sec += summary_he(m, geo, ctx, why, sent, an, ea, label, score)
        sec += wedge_section_he(m, df, geo, ctx, spy_below)
        sec += why_fell_he(why, news)
        sec += sentiment_markdown(sent, "he")
        sec += analysts_he(an)
        sec += report_he(ea)
        sec += fundamentals_he(fu)
        sec += read_he(label, score, fired)
        sections.append("\n".join(sec))

    n_conf = sum(matches[s].status == "confirmed" for s in symbols)
    head = [
        f"# AlgoVision: טריז יורד במניות מוכות - {today}", "",
        f"מחירים עד {last_bar}. {len(symbols)} מניות בטבלה: {n_conf} מאושרות (פרצו ב-5 הנרות האחרונים) ו-{len(symbols) - n_conf} בהתהוות (עדיין בתוך הטריז).", "",
        "**הכלל בקצרה.** טריז יורד: שני קווי מגמה יורדים ומתכנסים, המחיר נסחר בתוכם ונשאר בפנים, ופריצה בסגירה מעל הקו העליון "
        "היא האיתות. נבדק על S&P 500 + NASDAQ-100 ב-2016-2026 עם חלוקה לאימון (עד 2022) ומבחן (2023-2026): היתרון קיים רק במניות **מוכות**, "
        "כלומר תשואת 6 חודשים מתחת ל-8%- ומחיר מתחת לממוצע הנע של 200 יום. בתת-הקבוצה הזו: כ-3%+ לעסקה מעל כניסה אקראית באותה מניה, "
        "שיעור פגיעה ~60%, מקדם רווח ~1.8, חיובי בכל אחת מ-11 השנים, כ-100 איתותים בשנה. במניות במגמת עלייה הטריז הוא רק תיקון ואין לו יתרון.", "",
        "**מה ניבא תוצאות ומה לא.** עזרו: כמה המניה מוכה (ככל שיותר, טוב יותר), תנודתיות גבוהה (ATR), טריז גדול (לא צר), ירידה תלולה לתוך התבנית, "
        "ושוק חלש (SPY מתחת לממוצע 200: שיעור פגיעה 70%). לא עזרו: ציון הדטקטור, נפח הפריצה, התכווצות הנפח, מספר הנגיעות ו\"איכות\" הצורה.", "",
        "**הכלל שהחזיק מעמד מחוץ למדגם.** כניסה בסגירת הפריצה או בפתיחה למחרת, סטופ בתחתית הטריז (או 2 ATR), ללא יעד רווח, יציאה אחרי ~20 נרות. "
        "לצפות ל-2-3%+ עודף לעסקה, לא ל-5%, ולירידה של 25-35% בתיק שווה-משקל של האיתותים האלה. פירוט: docs/research_falling_wedge.md.", "",
        "**איך לקרוא את הקובץ.** לחיצה על הסימול פותחת את הגרף ב-TradingView; לחיצה על \"פירוט\" מקפיצה להסבר המלא על המניה בתוך הקובץ "
        "(סיכום קצר בחמש שורות, ואז ניתוח טכני של הטריז, למה המניה ירדה, חששות וסנטימנט, אנליסטים, הדוח האחרון, נתוני יסוד וקריאה מבוססת כללים). \"מאושר\" = המחיר סגר מעל הקו העליון "
        "ב-5 הנרות האחרונים (זה האיתות); \"בהתהוות\" = עדיין בתוך הטריז, אין איתות עדיין. \"למה ירדה\" מציין רק ראיות שנמצאו בנתונים "
        "(כותרות שמזכירות את החברה סביב ימי הירידה הגדולים, דיווחי 8-K, הורדות דירוג, ימי שוק) או \"לא נמצא\"; שום דבר לא מומצא. "
        "\"חששות\" = נושאי הכותרות השליליות על החברה בשנה האחרונה (Google News), ספורים, עם הכותרות עצמן בפירוט; \"סנטימנט\" = "
        "קריאה שקופה על איתותים רשומים: אנליסטים, יעדי מחיר, עדכוני תחזיות, שורט, הקהל ב-StockTwits וטון הכותרות. "
        "הכותרות, שמות החברות ובתי ההשקעות מובאים כפי שפורסמו.", "",
        "<a id=\"summary\" name=\"summary\"></a>", "## טבלה מסכמת", "",
        pd.DataFrame(rows).to_markdown(index=False) if rows else "אין טריזים יורדים במניות מוכות היום.", "",
    ]
    tail = _open_positions_he(out_dir)
    tail += ["---", "סינון שיטתי ומבחן קדימה, לא ייעוץ השקעות. הטיית שרידות חלה על כל הבדיקות לאחור (חברי המדד של היום)."]
    text = "\n".join(head + sections + tail) + "\n"
    path = out_dir / f"wedge_{today}.md"
    path.write_text(text, encoding="utf-8")
    (out_dir / "wedge_latest.md").write_text(text, encoding="utf-8")
    return path


def wedge_matches(frames: Dict[str, pd.DataFrame], symbols: Iterable[str]) -> Dict[str, PatternMatch]:
    """Current falling wedges in beaten-down stocks, the best-scored match per symbol (the daily report's filter)."""
    from algovision.core.types import DetectorConfig
    from algovision.data.provider import DataProvider
    from algovision.scanner import Scanner

    cfg = DetectorConfig(filter_max_ret_126=-0.08, filter_below_ma200=True, recent_bars=5)
    sc = Scanner(DataProvider(cache_dir=None, offline=True), cfg, ["Falling Wedge"])
    out: Dict[str, PatternMatch] = {}
    for s in symbols:
        df = frames.get(s)
        if df is None or len(df) < 260:
            continue
        for m in sc.analyse_frame(s, df, mode="current"):
            if s not in out or (m.status == "confirmed", m.score) > (out[s].status == "confirmed", out[s].score):
                out[s] = m
    return out
