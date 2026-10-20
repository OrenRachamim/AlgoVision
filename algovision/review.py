"""The periodic review: what in the daily report has actually worked so far, what has not, and what is still unknown.

Built on the look-back ledger (:mod:`algovision.lookback`: every (table, symbol) pair from its first appearance in the
dated reports, measured forward against the SPY and against the beaten-down basket of that day) and on the journal's
realised trades (``mark_to_market.csv``). Every verdict is a fixed rule applied to the numbers, written next to them:

* a **table** (signal list) *works so far* when at least ``MIN_N`` names have a 20-bar return, the mean excess over the
  beaten-down basket is positive and its t-statistic is at least ``T_STRONG``; *not working so far* when the excess
  is negative with t at or below ``-T_STRONG``; *noise so far* in between; *too early* below ``MIN_N`` names;
* a **condition** (a flag, a column, a cut) *separates* when both sides have at least ``MIN_SPLIT`` names and the
  difference of the 20-bar basket excess (yes minus no) has a Welch t of at least ``T_STRONG`` in absolute value;
  the sign says which side did better; otherwise *noise so far* or *too early*;
* a **journal rule** is compared with its research expectation on closed trades only: *on track* when the realised
  hit rate is within 10 points of the expectation and the mean is positive, *below expectation* otherwise, *too early*
  under ``MIN_CLOSED`` closed trades.

The windows overlap and the sample is a few weeks in one regime, so the t-statistics overstate the evidence; the
thresholds are deliberately strict and every verdict carries its n. Nothing here changes a rule, a flag or an
order: the review says what the evidence is, the ten-year backtests decide what enters the report.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from algovision.lookback import SECTION_EN, SECTION_HE, _num, events, forward

MIN_N = 20          # names with a 20-bar return before a table gets a verdict
MIN_SPLIT = 12      # names on each side of a condition
MIN_CLOSED = 10     # closed trades before a journal rule gets a verdict
T_STRONG = 2.0

VERDICT_HE = {"works": "עובד עד כה", "fails": "לא עובד עד כה", "noise": "רעש עד כה", "early": "מוקדם מדי",
              "better_yes": "עם התנאי טוב יותר", "better_no": "בלי התנאי טוב יותר", "on_track": "במסלול", "below": "מתחת לציפייה"}
VERDICT_EN = {"works": "works so far", "fails": "not working so far", "noise": "noise so far", "early": "too early",
              "better_yes": "better with the condition", "better_no": "better without it", "on_track": "on track", "below": "below expectation"}

# what the ten-year backtests said about each table (docs/research_*.md), for the "expected vs seen" column
EXPECTED = {
    "newsday": {"en": "+6-7% vs random at 60 bars", "he": "+6-7% מול אקראי ב-60 נרות"},
    "wedge": {"en": "+3% vs random at 20 bars", "he": "+3% מול אקראי ב-20 נרות"},
    "wedge_watch": {"en": "no edge (a stock still falling)", "he": "ללא יתרון (מניה שעדיין יורדת)"},
    "insider_beaten": {"en": "+10% vs random at 60 bars", "he": "+10% מול אקראי ב-60 נרות"},
    "insider_other": {"en": "no edge", "he": "ללא יתרון"},
    "early_rally": {"en": "+2-3% net, ~0 vs SPY at 20 bars", "he": "+2-3% נטו, ~0 מול SPY ב-20 נרות"},
    "ma200_cross": {"en": "no edge in both periods", "he": "ללא יתרון בשתי התקופות"},
    "growth": {"en": "retired", "he": "הופסק"},
    "jev": {"en": "untested (forward test only)", "he": "לא נבדק (מבחן קדימה בלבד)"},
}


# ----------------------------------------------------------------------------
# statistics
# ----------------------------------------------------------------------------
def _t(x: pd.Series) -> float:
    x = x.dropna()
    return float(x.mean() / x.std(ddof=1) * np.sqrt(len(x))) if len(x) > 2 and x.std(ddof=1) > 0 else np.nan


def _welch(a: pd.Series, b: pd.Series) -> float:
    a, b = a.dropna(), b.dropna()
    if len(a) < 3 or len(b) < 3:
        return np.nan
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float((a.mean() - b.mean()) / se) if se > 0 else np.nan


def group_stats(g: pd.DataFrame, h: str = "20") -> Dict:
    r = g[f"ret_{h}"].dropna()
    out = {"n": int(len(g)), "n_h": int(len(r)), "mean": float(r.mean()) if len(r) else np.nan, "hit": float((r > 0).mean()) if len(r) else np.nan,
           "xspy": float(g[f"xspy_{h}"].dropna().mean()) if len(r) else np.nan, "xbk": float(g[f"xbk_{h}"].dropna().mean()) if len(r) else np.nan,
           "t_xbk": _t(g[f"xbk_{h}"]) if len(r) else np.nan}
    rl = g["ret_latest"].dropna()
    out.update({"n_latest": int(len(rl)), "mean_latest": float(rl.mean()) if len(rl) else np.nan, "hit_latest": float((rl > 0).mean()) if len(rl) else np.nan,
                "xbk_latest": float(g["xbk_latest"].dropna().mean()) if len(rl) else np.nan,
                "xspy_latest": float(g["xspy_latest"].dropna().mean()) if len(rl) else np.nan, "t_xbk_latest": _t(g["xbk_latest"]) if len(rl) else np.nan})
    return out


def table_verdict(s: Dict, latest: bool = False) -> str:
    """The verdict at 20 bars, or (``latest``) at the current close over every name listed so far."""
    n, x, tt = (s["n_latest"], s["xbk_latest"], s["t_xbk_latest"]) if latest else (s["n_h"], s["xbk"], s["t_xbk"])
    if n < MIN_N or not np.isfinite(tt):
        return "early"
    if x > 0 and tt >= T_STRONG:
        return "works"
    if x < 0 and tt <= -T_STRONG:
        return "fails"
    return "noise"


def split_stats(yes: pd.DataFrame, no: pd.DataFrame, h: str = "20") -> Dict:
    a, b = yes[f"xbk_{h}"], no[f"xbk_{h}"]
    out = {"n_yes": int(a.notna().sum()), "n_no": int(b.notna().sum()), "xbk_yes": float(a.mean()) if a.notna().any() else np.nan,
           "xbk_no": float(b.mean()) if b.notna().any() else np.nan, "ret_yes": float(yes[f"ret_{h}"].mean()) if len(yes) else np.nan,
           "ret_no": float(no[f"ret_{h}"].mean()) if len(no) else np.nan, "hit_yes": float((yes[f"ret_{h}"].dropna() > 0).mean()) if yes[f"ret_{h}"].notna().any() else np.nan,
           "hit_no": float((no[f"ret_{h}"].dropna() > 0).mean()) if no[f"ret_{h}"].notna().any() else np.nan, "t": _welch(a, b)}
    out["diff"] = out["xbk_yes"] - out["xbk_no"] if np.isfinite(out["xbk_yes"]) and np.isfinite(out["xbk_no"]) else np.nan
    return out


def split_verdict(s: Dict) -> str:
    if s["n_yes"] < MIN_SPLIT or s["n_no"] < MIN_SPLIT or not np.isfinite(s["t"]):
        return "early"
    if s["t"] >= T_STRONG:
        return "better_yes"
    if s["t"] <= -T_STRONG:
        return "better_no"
    return "noise"


# ----------------------------------------------------------------------------
# the conditions tested, defined once
# ----------------------------------------------------------------------------
def _has_flag(F: pd.DataFrame, code: str) -> pd.Series:
    return F["flags"].fillna("").str.split().map(lambda f: code in (f or []))


def _cell(F: pd.DataFrame, col: str) -> pd.Series:
    return F[col].fillna("").astype(str) if col in F else pd.Series("", index=F.index)


def _macd_prob(F: pd.DataFrame) -> pd.Series:
    """The probability in a 'MACD pre-touch' cell (NaN for touching / above signal / empty)."""
    return _cell(F, "MACD pre-touch").str.extract(r"(\d+)%")[0].map(_num)


def conditions(F: pd.DataFrame) -> List[Dict]:
    """Every condition as (key, label en/he, population, mask); the review splits each population by its mask."""
    sig = F[F["section"].isin(["newsday", "wedge", "wedge_watch", "insider_beaten", "early_rally", "ma200_cross"])]
    B = F[F["section"] == "briefs"]
    J = F[F["section"] == "jev"]
    out: List[Dict] = []

    def add(key, en, he, pop, mask, note_en="", note_he=""):
        out.append({"key": key, "en": en, "he": he, "pop": pop, "mask": mask.fillna(False).astype(bool), "note_en": note_en, "note_he": note_he})

    if len(B):
        for code, en, he in (("Z", "Z: z vs peers below -1 (warning)", "Z: z מול עמיתים מתחת ל--1 (אזהרה)"), ("S", "S: negative sentiment (warning)", "S: סנטימנט שלילי (אזהרה)"),
                             ("T", "T: target upside above 50% (warning)", "T: אפסייד ליעד מעל 50% (אזהרה)"), ("D", "D: more than 40% below the 52-week high (a plus over ten years)", "D: יותר מ-40% מתחת לשיא השנתי (יתרון לאורך עשור)")):
            add(f"flag_{code}", en, he, B, _has_flag(B, code))
        add("no_warning", "no warning flag at all", "ללא דגל אזהרה בכלל", B, B["n_flags"] == 0)
        add("read_bottom", "read: signs of a bottom", "קריאה: סימני תחתית", B, _cell(B, "read") == "signs of a bottom")
        add("read_falling", "read: still falling", "קריאה: עדיין יורדת", B, _cell(B, "read") == "still falling")
        add("market_wide", "'market-wide' among the causes of the decline", "'כלל-שוקי' בין סיבות הירידה", B, B["market_wide"])
        add("sent_pos", "sentiment read positive", "קריאת סנטימנט חיובית", B, _cell(B, "sentiment") == "positive")
        add("consensus_buy", "analyst consensus buy / strong buy", "קונצנזוס אנליסטים קנייה / קנייה חזקה", B, _cell(B, "consensus").str.contains("buy"))
        add("deep_dd", "more than 30% below the 52-week high", "יותר מ-30% מתחת לשיא השנתי", B, B["from 52w high"].map(_num) <= -30)
        add("peers_up", "20-day return above the peer group (vs peers 20d > 0)", "תשואת 20 יום מעל קבוצת העמיתים", B, _cell(B, "vs peers 20d").str.extract(r"^([+-]?\d+\.\d+)%")[0].map(_num) > 0)
        pb = _cell(B, "P(buy)").map(_num) if "P(buy)" in B else pd.Series(np.nan, index=B.index)
        if pb.notna().sum() >= MIN_SPLIT:
            add("jev_buy_brief", "Jev P(buy) >= 0.6 on the brief", "Jev P(קנייה) >= 0.6 על התקציר", B[pb.notna()], pb[pb.notna()] >= 0.6)
        mp = _macd_prob(B)
        if mp.notna().sum() >= MIN_SPLIT:
            add("macd70_brief", "MACD pre-touch probability >= 70% (lines still apart)", "MACD נגיעה צפויה >= 70% (הקווים עדיין מופרדים)", B[mp.notna()], mp[mp.notna()] >= 70)
    C = F[F["section"] == "checklist"]
    if len(C):
        checks = _cell(C, "checks passed").str.extract(r"(\d+)/")[0].map(_num)
        if checks.notna().sum() >= 2 * MIN_SPLIT:
            add("checklist4", "checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist)", "צ'קליסט: 4 או 5 בדיקות עברו (לעומת 3 ומטה, מבין השמות בצ'קליסט)",
                C[checks.notna()], checks[checks.notna()] >= 4)
    if len(sig):
        add("fresh", "listed 1-3 days (fresh) vs 4+ days", "ברשימה 1-3 ימים (טרי) לעומת 4+ ימים", sig, sig["n_days"] <= 3)
        grp = _cell(sig, "group")
        if (grp != "").sum() >= 2 * MIN_SPLIT:
            add("group_beaten", "peer group beaten down too", "קבוצת העמיתים מוכה גם היא", sig[grp != ""], grp[grp != ""].str.startswith("beaten"))
        six = _cell(sig, "6m").map(_num)
        add("depth30", "6-month return below -30%", "תשואת 6 חודשים מתחת ל--30%", sig[six.notna()], six[six.notna()] <= -30)
        vol = _cell(sig, "volume").map(_num)
        if vol.notna().sum() >= 2 * MIN_SPLIT:
            add("vol15", "signal-day volume above 1.5x", "מחזור יום הסיגנל מעל 1.5x", sig[vol.notna()], vol[vol.notna()] > 1.5)
        mv = _cell(sig, "max vol 10d").map(_num)
        if mv.notna().sum() >= 2 * MIN_SPLIT:
            add("climax3", "a 3x+ volume day in the last 10 bars", "יום מחזור 3x+ ב-10 הנרות האחרונים", sig[mv.notna()], mv[mv.notna()] >= 3)
        mp = _macd_prob(sig)
        if mp.notna().sum() >= 2 * MIN_SPLIT:
            add("macd70", "MACD pre-touch probability >= 70% (lines still apart)", "MACD נגיעה צפויה >= 70% (הקווים עדיין מופרדים)", sig[mp.notna()], mp[mp.notna()] >= 70)
        R = sig[sig["section"] == "early_rally"]
        nr = _cell(R, "rules fired").map(_num)
        if nr.notna().sum() >= 2 * MIN_SPLIT:
            add("rules2", "early rally: two or more rules fired", "ראלי מוקדם: שני כללים או יותר נורו", R[nr.notna()], nr[nr.notna()] >= 2)
    if len(J) and "P(buy)" in J:
        pb = J["P(buy)"].map(_num)
        add("jev_pick", "Jev: P(buy) >= 0.6 (the jev_pick rule)", "Jev: P(קנייה) >= 0.6 (הכלל jev_pick)", J[pb.notna()], pb[pb.notna()] >= 0.6)
        add("jev_low", "Jev: P(buy) < 0.2", "Jev: P(קנייה) < 0.2", J[pb.notna()], pb[pb.notna()] < 0.2)
    return out


# ----------------------------------------------------------------------------
# the realised journal
# ----------------------------------------------------------------------------
EXPECT_HIT = {"newsday": 0.62, "falling_wedge_beaten_down": 0.60, "insider_buy_beaten_down": 0.68, "early_rally_beaten_down": 0.595, "jev_pick": np.nan, "jev_skip": np.nan}


def journal_verdicts(out_dir: Path) -> List[Dict]:
    p = Path(out_dir) / "mark_to_market.csv"
    if not p.exists():
        return []
    m = pd.read_csv(p)
    out = []
    for rule, g in m.groupby("rule"):
        c = g[g["status"] == "closed"]
        o = g[g["status"] == "open"]
        rec = {"rule": rule, "logged": int(len(g)), "closed": int(len(c)), "open": int(len(o)),
               "mean_closed": float(c["ret"].mean()) if len(c) else np.nan, "hit_closed": float((c["ret"] > 0).mean()) if len(c) else np.nan,
               "xspy_closed": float((c["ret"] - c["spy_ret"]).mean()) if len(c) else np.nan, "xbk_closed": float((c["ret"] - c["basket_ret"]).mean()) if len(c) else np.nan,
               "mean_open": float(o["ret"].mean()) if len(o) else np.nan, "hit_open": float((o["ret"] > 0).mean()) if len(o) else np.nan,
               "mean_all": float(g["ret"].mean()) if g["ret"].notna().any() else np.nan, "hit_all": float((g["ret"].dropna() > 0).mean()) if g["ret"].notna().any() else np.nan,
               "xbk_all": float((g["ret"] - g["basket_ret"]).mean()) if g["ret"].notna().any() else np.nan,
               "expect_hit": EXPECT_HIT.get(rule, np.nan)}
        if rec["closed"] < MIN_CLOSED:
            rec["verdict"] = "early"
        elif rule == "jev_skip":
            rec["verdict"] = "on_track" if rec["mean_closed"] < 0 else "below"
        elif np.isfinite(rec["expect_hit"]):
            rec["verdict"] = "on_track" if rec["mean_closed"] > 0 and rec["hit_closed"] >= rec["expect_hit"] - 0.10 else "below"
        else:
            rec["verdict"] = "on_track" if rec["mean_closed"] > 0 and rec["hit_closed"] >= 0.5 else "below"
        out.append(rec)
    return out


# ----------------------------------------------------------------------------
# the review
# ----------------------------------------------------------------------------
def build_review(out_dir: Path, frames: Dict[str, pd.DataFrame], bench: Optional[pd.DataFrame], today: Optional[str] = None) -> Dict:
    out_dir = Path(out_dir)
    today = today or dt.date.today().isoformat()
    ev = events(out_dir)
    F = forward(ev, frames, bench) if len(ev) and bench is not None else pd.DataFrame()
    res: Dict = {"date": today, "n_reports": int(F["date"].nunique()) if len(F) else 0,
                 "first": str(F["date"].min()) if len(F) else "", "last": str(F["date"].max()) if len(F) else "", "tables": [], "conditions": [], "stability": [],
                 "journal": journal_verdicts(out_dir)}
    if not len(F):
        return res
    for sec in ["newsday", "wedge", "insider_beaten", "early_rally", "ma200_cross", "wedge_watch", "insider_other", "jev", "growth"]:
        g = F[F["section"] == sec]
        if not len(g):
            continue
        s = group_stats(g)
        s.update({"section": sec, "en": SECTION_EN.get(sec, sec), "he": SECTION_HE.get(sec, sec), "verdict": table_verdict(s), "verdict_latest": table_verdict(s, latest=True),
                  "expected_en": EXPECTED.get(sec, {}).get("en", ""), "expected_he": EXPECTED.get(sec, {}).get("he", "")})
        # stability: the sign of the basket excess in the first and second half of the dates
        d = pd.to_datetime(g["date"])
        mid = d.min() + (d.max() - d.min()) / 2
        a, b = g[d <= mid], g[d > mid]
        sa, sb = group_stats(a), group_stats(b)
        s.update({"half1_xbk": sa["xbk"], "half1_n": sa["n_h"], "half2_xbk": sb["xbk"], "half2_n": sb["n_h"],
                  "stable": bool(sa["n_h"] >= 8 and sb["n_h"] >= 8 and np.sign(sa["xbk"]) == np.sign(sb["xbk"]))})
        res["tables"].append(s)
    for c in conditions(F):
        yes, no = c["pop"][c["mask"]], c["pop"][~c["mask"]]
        s = split_stats(yes, no)
        sl = split_stats(yes, no, "latest")
        s.update({"key": c["key"], "en": c["en"], "he": c["he"], "verdict": split_verdict(s), "note_en": c["note_en"], "note_he": c["note_he"],
                  "latest": sl, "verdict_latest": split_verdict(sl)})
        res["conditions"].append(s)
    return res


def _changes(res: Dict, prev: Optional[Dict]) -> List[Dict]:
    """Verdicts that differ from the previous review."""
    if not prev:
        return []
    out = []
    for kind, key in (("tables", "section"), ("conditions", "key"), ("journal", "rule")):
        for field, tag_en, tag_he in (("verdict", "20 bars", "20 נרות"), ("verdict_latest", "to date", "עד היום")):
            old = {r[key]: r.get(field) for r in prev.get(kind, []) if r.get(field)}
            for r in res.get(kind, []):
                if r.get(field) and r[key] in old and old[r[key]] != r[field]:
                    out.append({"kind": kind, "key": r[key], "en": f"{r.get('en', r[key])} ({tag_en})", "he": f"{r.get('he', r[key])} ({tag_he})",
                                "from": old[r[key]], "to": r[field]})
    return out


def _p(v, d=1) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def _h(v) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:.0f}%"


def _tt(v) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v:.1f}"


def review_markdown(res: Dict, prev: Optional[Dict] = None, lang: str = "en") -> List[str]:
    he = lang == "he"
    V = VERDICT_HE if he else VERDICT_EN
    L = (lambda r: r["he"]) if he else (lambda r: r["en"])
    md = [f"# {'AlgoVision: סקירת מסקנות' if he else 'AlgoVision review: what has worked so far'} - {res['date']}", ""]
    if not res["tables"]:
        return md + [("אין עדיין מספיק דוחות מתוארכים." if he else "Not enough dated reports yet."), ""]
    md += [(f"מה בדוח היומי באמת רלוונטי לפי הראיות עד כה: {res['n_reports']} דוחות מתוארכים, {res['first']} עד {res['last']}. כל שם נמדד מההופעה "
            f"הראשונה שלו בטבלה, כניסה בפתיחה הבאה, בשני אופקים: 20 נרות קדימה, ועד הסגירה הנוכחית (\"עד היום\": כל שם שנרשם אי פעם, כל אחד באורך "
            f"החזקה שלו), מול סל המניות המוכות של אותו יום (המדד ההוגן לכללים שקונים רק מניות מוכות) ומול SPY. לכל טבלה ולכל תנאי יש פסיקה "
            f"לכל אופק. הפסיקות הן כללים קבועים (בסוף הקובץ), לא שיקול דעת: טבלה \"עובדת\" רק עם {MIN_N}+ שמות ו-t של {T_STRONG:.0f} ומעלה על "
            f"העודף מול הסל; תנאי \"מפריד\" רק עם {MIN_SPLIT}+ שמות בכל צד ו-t של {T_STRONG:.0f} ומעלה על ההפרש. החלונות חופפים והמדגם הוא שבועות "
            f"ספורים במשטר אחד, אז ה-t מוגזם; הספים מחמירים בכוונה. הסקירה לא משנה שום כלל: הבדיקות של עשר שנים קובעות מה נכנס לדוח.") if he else
           (f"What in the daily report is actually relevant on the evidence so far: {res['n_reports']} dated reports, {res['first']} to {res['last']}. "
            f"Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current "
            f"close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair "
            f"benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), "
            f"not judgement: a table 'works' only with {MIN_N}+ names and a t of {T_STRONG:.0f} or more on the basket excess; a condition 'separates' "
            f"only with {MIN_SPLIT}+ names on each side and a t of {T_STRONG:.0f} or more on the difference. The windows overlap and the sample is a "
            f"few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year "
            f"backtests decide what enters the report."), ""]
    # bottom line
    md += [("## השורה התחתונה" if he else "## Bottom line"), ""]
    titles = {"works": ("עובד / מפריד עד כה", "Works or separates so far"), "fails": ("לא עובד / הצד השני טוב יותר", "Not working, or the other side did better"),
              "noise": ("רעש עד כה", "Noise so far"), "early": ("מוקדם מדי לומר", "Too early to say")}
    for latest in (False, True):
        md.append(("### עד היום (מול המחיר הנוכחי, כל שם שנרשם)" if he else "### To date (against the current price, every name listed)") if latest
                  else ("### 20 נרות אחרי הרישום" if he else "### 20 bars after the listing"))
        md.append("")
        buckets = {"works": [], "fails": [], "noise": [], "early": []}
        for t in res["tables"]:
            v = t["verdict_latest"] if latest else t["verdict"]
            n, x, tt = (t["n_latest"], t["xbk_latest"], t["t_xbk_latest"]) if latest else (t["n_h"], t["xbk"], t["t_xbk"])
            buckets[v].append(f"{L(t)} (n {n}, {'מול הסל' if he else 'vs basket'} {_p(x)}, t {_tt(tt)})")
        for c in res["conditions"]:
            s = c["latest"] if latest else c
            v = c["verdict_latest"] if latest else c["verdict"]
            key = {"better_yes": "works", "better_no": "fails", "noise": "noise", "early": "early"}[v]
            buckets[key].append(f"{L(c)} ({'הפרש' if he else 'diff'} {_p(s['diff'])}, n {s['n_yes']}/{s['n_no']}, t {_tt(s['t'])})")
        for k in ("works", "fails", "noise", "early"):
            md.append(f"**{titles[k][0] if he else titles[k][1]}:** " + ("; ".join(buckets[k]) if buckets[k] else ("אין" if he else "none")))
            md.append("")
    # tables
    md += [("## לפי טבלה (20 נרות)" if he else "## By table (20 bars)"), ""]
    hdr = (["טבלה", "n", "n20", "תשואה 20", "פגיעה 20", "מול SPY 20", "מול הסל 20", "t 20", "פסיקה 20", "עד היום", "פגיעה", "מול SPY", "מול הסל", "t", "פסיקה עד היום", "ציפיית המחקר", "יציב בשני החצאים"] if he else
           ["table", "n", "n20", "ret 20", "hit 20", "vs SPY 20", "vs basket 20", "t 20", "verdict 20", "to date", "hit", "vs SPY", "vs basket", "t", "verdict to date", "research expected", "same sign in both halves"])
    md += ["| " + " | ".join(hdr) + " |", "|:--|" + "--:|" * 7 + ":--|" + "--:|" * 5 + ":--|:--|:--|"]
    for t in res["tables"]:
        stable = ("" if t["half1_n"] < 8 or t["half2_n"] < 8 else (("כן" if he else "yes") if t["stable"] else ("לא" if he else "no")))
        md.append("| " + " | ".join([L(t), str(t["n"]), str(t["n_h"]), _p(t["mean"]), _h(t["hit"]), _p(t["xspy"]), _p(t["xbk"]), _tt(t["t_xbk"]), V[t["verdict"]],
                                     _p(t["mean_latest"]), _h(t["hit_latest"]), _p(t["xspy_latest"]), _p(t["xbk_latest"]), _tt(t["t_xbk_latest"]), V[t["verdict_latest"]],
                                     t["expected_he"] if he else t["expected_en"],
                                     stable + (f" ({_p(t['half1_xbk'])} / {_p(t['half2_xbk'])})" if stable else "")]) + " |")
    md.append("")
    # conditions
    md += [("## לפי תנאי (עודף מול הסל, עם התנאי לעומת בלי; 20 נרות ועד היום)" if he else "## By condition (basket excess, with vs without; 20 bars and to date)"), ""]
    hdr = (["תנאי", "n עם", "n בלי", "תשואה 20 עם", "תשואה 20 בלי", "פגיעה 20 עם", "פגיעה 20 בלי", "מול הסל 20 עם", "מול הסל 20 בלי", "הפרש 20", "t 20", "פסיקה 20",
            "n עם (עד היום)", "n בלי", "תשואה עם", "תשואה בלי", "מול הסל עם", "מול הסל בלי", "הפרש", "t", "פסיקה עד היום"] if he else
           ["condition", "n with", "n without", "ret 20 with", "ret 20 without", "hit 20 with", "hit 20 without", "vs basket 20 with", "vs basket 20 without", "diff 20", "t 20", "verdict 20",
            "n with (to date)", "n without", "ret with", "ret without", "vs basket with", "vs basket without", "diff", "t", "verdict to date"])
    md += ["| " + " | ".join(hdr) + " |", "|:--|" + "--:|" * 10 + ":--|" + "--:|" * 8 + ":--|"]
    for c in res["conditions"]:
        s = c["latest"]
        md.append("| " + " | ".join([L(c), str(c["n_yes"]), str(c["n_no"]), _p(c["ret_yes"]), _p(c["ret_no"]), _h(c["hit_yes"]), _h(c["hit_no"]), _p(c["xbk_yes"]),
                                     _p(c["xbk_no"]), _p(c["diff"]), _tt(c["t"]), V[c["verdict"]],
                                     str(s["n_yes"]), str(s["n_no"]), _p(s["ret_yes"]), _p(s["ret_no"]), _p(s["xbk_yes"]), _p(s["xbk_no"]), _p(s["diff"]), _tt(s["t"]), V[c["verdict_latest"]]]) + " |")
    md.append("")
    # journal
    if res["journal"]:
        md += [("## היומן: עסקאות סגורות מול ציפיית המחקר" if he else "## The journal: closed trades against the research expectation"), ""]
        hdr = (["כלל", "נרשמו", "נסגרו", "ממוצע סגורות", "פגיעה סגורות", "מול SPY", "מול הסל", "פגיעה צפויה", "פתוחות: ממוצע", "פתוחות: פגיעה", "הכול במחיר הנוכחי: ממוצע", "פגיעה", "מול הסל", "פסיקה (סגורות)"] if he else
               ["rule", "logged", "closed", "closed mean", "closed hit", "vs SPY", "vs basket", "expected hit", "open: mean", "open: hit", "all at the current price: mean", "hit", "vs basket", "verdict (closed)"])
        md += ["| " + " | ".join(hdr) + " |", "|:--|" + "--:|" * 12 + ":--|"]
        for j in res["journal"]:
            md.append("| " + " | ".join([j["rule"], str(j["logged"]), str(j["closed"]), _p(j["mean_closed"], 2), _h(j["hit_closed"]), _p(j["xspy_closed"], 2),
                                         _p(j["xbk_closed"], 2), _h(j["expect_hit"]), _p(j["mean_open"], 2), _h(j["hit_open"]), _p(j["mean_all"], 2), _h(j["hit_all"]),
                                         _p(j["xbk_all"], 2), V[j["verdict"]]]) + " |")
        md.append("")
    # changes
    ch = _changes(res, prev)
    md += [("## מה השתנה מאז הסקירה הקודמת" if he else "## What changed since the previous review"), ""]
    if prev is None:
        md.append("הסקירה הראשונה; אין השוואה." if he else "First review; nothing to compare with.")
    elif not ch:
        md.append(f"{'שום פסיקה לא השתנתה מאז' if he else 'No verdict changed since'} {prev.get('date', '')}.")
    else:
        for x in ch:
            md.append(f"- {x['he'] if he else x['en']}: {V[x['from']]} -> {V[x['to']]}")
    md.append("")
    md += [("## השיטה" if he else "## Method"), "",
           (f"מקור: הטבלאות של הדוחות המתוארכים (journal/report_<date>.md) ו-mark_to_market.csv של היומן. שני אופקים: 20 נרות אחרי הרישום, ועד הסגירה "
            f"הנוכחית (כל שם, באורך ההחזקה שלו; אופק לא אחיד, אז הוא מסכם את המצב עכשיו ולא תוצאה של כלל קבוע). פסיקה לטבלה: {MIN_N}+ שמות עם תשואה באופק; "
            f"\"עובד\" כשהעודף הממוצע מול סל המניות המוכות חיובי ו-t >= {T_STRONG:.0f}; \"לא עובד\" כשהוא שלילי ו-t <= -{T_STRONG:.0f}; אחרת \"רעש\". "
            f"פסיקה לתנאי: {MIN_SPLIT}+ שמות בכל צד, t של Welch על ההפרש בעודף מול הסל; |t| >= {T_STRONG:.0f} אומר איזה צד טוב יותר. כלל ביומן: "
            f"{MIN_CLOSED}+ עסקאות סגורות; \"במסלול\" כשהממוצע חיובי ושיעור הפגיעה בתוך 10 נקודות מהציפייה. הטיית שרידות, חלונות חופפים ומשטר אחד "
            f"חלים על הכול. סינונים שיטתיים ומבחן קדימה, לא ייעוץ השקעות.") if he else
           (f"Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, "
            f"and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather "
            f"than the result of a fixed rule). Table verdict: {MIN_N}+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= {T_STRONG:.0f}; 'not working' when negative with "
            f"t <= -{T_STRONG:.0f}; 'noise' otherwise. Condition verdict: {MIN_SPLIT}+ names on each side, Welch t on the difference in basket excess; "
            f"|t| >= {T_STRONG:.0f} names the better side. Journal rule: {MIN_CLOSED}+ closed trades; 'on track' when the mean is positive and the hit rate is "
            f"within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a "
            f"forward test, not investment advice."), ""]
    return md


def write_review(out_dir: Path, frames: Dict[str, pd.DataFrame], bench: Optional[pd.DataFrame], today: Optional[str] = None) -> Tuple[Path, Path, Dict]:
    """Write review_<date>.md / review_latest.md (English), review_he_<date>.md / review_he_latest.md (Hebrew) and
    review_latest.json (the verdicts, compared with on the next run). Returns the two dated paths and the result."""
    out_dir = Path(out_dir)
    res = build_review(out_dir, frames, bench, today)
    jpath = out_dir / "review_latest.json"
    prev = None
    if jpath.exists():
        try:
            prev = json.loads(jpath.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            prev = None
    en = out_dir / f"review_{res['date']}.md"
    he = out_dir / f"review_he_{res['date']}.md"
    en.write_text("\n".join(review_markdown(res, prev, "en")), encoding="utf-8")
    he.write_text("\n".join(review_markdown(res, prev, "he")), encoding="utf-8")
    (out_dir / "review_latest.md").write_text(en.read_text(encoding="utf-8"), encoding="utf-8")
    (out_dir / "review_he_latest.md").write_text(he.read_text(encoding="utf-8"), encoding="utf-8")
    res["changes"] = _changes(res, prev)
    jpath.write_text(json.dumps(res, default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else (o.item() if hasattr(o, "item") else str(o)),
                                ensure_ascii=False, indent=1), encoding="utf-8")
    return en, he, res
