"""One line of forward-test evidence under each signal table, from the look-back ledger.

The daily report quotes the ten-year backtest in every table heading ("tested +3% vs random"). This module adds, under
the heading, what the forward test of the reports themselves has shown so far for that table: the 20-bar return, the
excess over the SPY and over the beaten-down basket of the same day (the fair benchmark for a rule that only buys
beaten-down stocks), the number of names, and the review's own verdict for the table (:mod:`algovision.review`, the
same thresholds and the same t-statistic), so the daily report and the periodic review never disagree.

Display only: nothing here changes a rule, a flag, a weight or what enters the journal. The line is computed from
``run_lookback``'s forward frame; without one (no dated reports yet, no benchmark) it is omitted.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.review import MIN_SPLIT, VERDICT_EN, VERDICT_HE, group_stats, split_stats, split_verdict, table_verdict


def _p(v, d=1) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def table_note(forward: Optional[pd.DataFrame], section: str, lang: str = "en") -> str:
    """The forward-test line for one signal table (``section`` as in :data:`algovision.lookback.SECTION_EN`), or ''."""
    if forward is None or not len(forward) or "section" not in forward:
        return ""
    g = forward[forward["section"] == section]
    if not len(g):
        return ""
    s = group_stats(g)
    he = lang == "he"
    v20, vlat = table_verdict(s), table_verdict(s, latest=True)
    V = VERDICT_HE if he else VERDICT_EN
    parts: List[str] = []
    if s["n_h"]:
        parts.append((f"ב-20 נרות: {_p(s['mean'])} ({s['n_h']} שמות, פגיעה {s['hit'] * 100:.0f}%), {_p(s['xspy'])} מול SPY, {_p(s['xbk'])} מול סל המוכות; פסיקה: {V[v20]}"
                      if he else
                      f"at 20 bars {_p(s['mean'])} ({s['n_h']} names, hit {s['hit'] * 100:.0f}%), {_p(s['xspy'])} vs SPY, {_p(s['xbk'])} vs the beaten-down basket; verdict: {V[v20]}"))
    if s["n_latest"]:
        parts.append((f"עד היום: {_p(s['mean_latest'])} ({s['n_latest']} שמות), {_p(s['xspy_latest'])} מול SPY, {_p(s['xbk_latest'])} מול הסל; פסיקה: {V[vlat]}"
                      if he else
                      f"to date {_p(s['mean_latest'])} ({s['n_latest']} names), {_p(s['xspy_latest'])} vs SPY, {_p(s['xbk_latest'])} vs the basket; verdict: {V[vlat]}"))
    if not parts:
        return ""
    below = section in TESTED and _below_expectation(s, v20, vlat)
    head = ("**מבחן קדימה עד כה** (רישום הדוחות עצמם; המדד ההוגן הוא סל המוכות): " if he else
            "**Forward test so far** (the ledger of the reports themselves; the fair benchmark is the beaten-down basket): ")
    tail = ""
    if below:
        tail = ((" **מתחת לציפיית המחקר עד כה**: שלילי מול סל המוכות בשני האופקים. הכלל נשאר בדוח: בדיקת עשר השנים קובעת, "
                 "וזהו משטר אחד של שבועות ספורים.") if he else
                (" **Below the research expectation so far**: negative against the beaten-down basket at both horizons. The rule "
                 "stays in the report: the ten-year backtest decides, and this is a few weeks in one regime."))
    return head + "; ".join(parts) + "." + tail


# the tables with a tested edge to fall below; the context tables (watch list, other insiders, MA200 cross) expect none
TESTED = ("newsday", "wedge", "insider_beaten", "early_rally")


def _below_expectation(s: Dict, v20: str, vlat: str) -> bool:
    """The review's own bar: 'not working so far' at either horizon (negative with t <= -2 on 20+ names), and negative at both."""
    both_negative = np.isfinite(s["xbk"]) and np.isfinite(s["xbk_latest"]) and s["xbk"] < 0 and s["xbk_latest"] < 0
    return bool(("fails" in (v20, vlat)) and both_negative)


def read_note(forward: Optional[pd.DataFrame], lang: str = "en") -> str:
    """The forward-test line for the rule-based read 'signs of a bottom' (the briefs population split by the read), or ''."""
    if forward is None or not len(forward) or "section" not in forward:
        return ""
    B = forward[forward["section"] == "briefs"]
    if not len(B) or "read" not in B:
        return ""
    mask = B["read"].fillna("").astype(str) == "signs of a bottom"
    yes, no = B[mask], B[~mask]
    if len(yes) < MIN_SPLIT or len(no) < MIN_SPLIT:
        return ""
    he = lang == "he"
    V = VERDICT_HE if he else VERDICT_EN
    s20, slat = split_stats(yes, no, "20"), split_stats(yes, no, "latest")
    v20, vlat = split_verdict(s20), split_verdict(slat)
    worse = (np.isfinite(s20["diff"]) and s20["diff"] < 0) and (np.isfinite(slat["diff"]) and slat["diff"] < 0)
    if he:
        line = (f"**הקריאה 'סימני תחתית' במבחן קדימה**: מול שאר הקריאות, {_p(s20['diff'])} מול סל המוכות ב-20 נרות (n {s20['n_yes']}/{s20['n_no']}; "
                f"פסיקה: {V[v20]}), {_p(slat['diff'])} עד היום (n {slat['n_yes']}/{slat['n_no']}; פסיקה: {V[vlat]}).")
        if worse:
            line += " השמות שסומנו 'סימני תחתית' עשו עד כה פחות טוב מהאחרים; הקריאה נשארת הקשר, לא פילטר."
    else:
        line = (f"**The read 'signs of a bottom' in the forward test**: against the other reads, {_p(s20['diff'])} vs the beaten-down basket at 20 bars "
                f"(n {s20['n_yes']}/{s20['n_no']}; verdict: {V[v20]}), {_p(slat['diff'])} to date (n {slat['n_yes']}/{slat['n_no']}; verdict: {V[vlat]}).")
        if worse:
            line += " The names read as 'signs of a bottom' have done worse than the rest so far; the read stays context, not a filter."
    return line


def group_first(order: List[str], peers: Dict[str, Dict]) -> List[str]:
    """Stable re-order: the names whose peer group is beaten down too first, then the others in their existing order."""
    def beaten(s):
        return bool((peers.get(s) or {}).get("g_beaten"))
    return [s for s in order if beaten(s)] + [s for s in order if not beaten(s)]


def group_first_frame(df: pd.DataFrame, peers: Dict[str, Dict]) -> pd.DataFrame:
    """The same re-order for a signal frame with a ``symbol`` column (a stable sort, duplicates and all)."""
    if not len(df):
        return df
    rank = {s: i for i, s in enumerate(group_first(list(dict.fromkeys(df["symbol"])), peers))}
    return df.assign(_k=df["symbol"].map(rank)).sort_values("_k", kind="stable").drop(columns="_k").reset_index(drop=True)


GROUP_FIRST_EN = ("Order: names whose peer group is beaten down too first (the one condition that separated in the ten-year backtest and in every "
                  "review of the forward test so far, docs/research_groups.md), then the table's usual order. A display order, not a filter.")
GROUP_FIRST_HE = ("סדר: קודם השמות שגם קבוצת העמיתים שלהם מוכה (התנאי היחיד שהפריד גם בבדיקת עשר השנים וגם בכל סקירה של מבחן הקדימה עד כה, "
                  "docs/research_groups.md), אחר כך הסדר הרגיל של הטבלה. סדר תצוגה, לא פילטר.")
