"""What has worked so far: every name the daily reports listed, measured forward.

Reads the dated reports (``journal/report_<date>.md``), takes the first day each (table, symbol) pair appeared, enters at
the next open and measures the return 5, 10 and 20 bars later and to the latest close, against SPY and against the
beaten-down basket of the same day (:mod:`algovision.regime`). The scorecard groups the results by table and by the
attributes the tables carried (wedge status, the flags, the rule-based read, the cause of the decline, how many days the
name stayed listed, the model's action). It is the honest ledger of the reports themselves, not a backtest: a few weeks,
one regime, overlapping windows. It runs in every daily report so the learning accumulates on its own.
"""

from __future__ import annotations

import glob
import re
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.regime import basket_return, beaten_mask, build_panels

_LINK = re.compile(r"\[([A-Z][A-Z0-9.\-]*)\]\(https://www\.tradingview\.com")
HORIZONS = (5, 10, 20)
SECTION_EN = {"insider_beaten": "insider buys, beaten-down", "insider_other": "insider buys, other", "newsday": "news-day",
              "wedge": "falling wedge (confirmed)", "wedge_watch": "falling wedge, forming (watch list)", "early_rally": "early rally",
              "briefs": "every name with a brief", "jev": "Jev decision", "growth": "growth screen (retired)"}
SECTION_HE = {"insider_beaten": "אינסיידרים, מוכות", "insider_other": "אינסיידרים, אחרות", "newsday": "יום חדשות",
              "wedge": "טריז יורד (מאושר)", "wedge_watch": "טריז יורד בהתהוות (רשימת מעקב)", "early_rally": "ראלי מוקדם",
              "briefs": "כל שם עם תקציר", "jev": "החלטת Jev", "growth": "סינון צמיחה (הופסק)"}


def _section_of(h2: Optional[str], h3: Optional[str]) -> Optional[str]:
    h = (h3 or "").lower()
    if h.startswith("beaten-down stocks"):
        return "insider_beaten"
    if h.startswith("other stocks with insider"):
        return "insider_other"
    if h.startswith("news-day"):
        return "newsday"
    if h.startswith("watch list"):
        return "wedge_watch"
    if h.startswith("falling wedge"):
        return "wedge"
    if h.startswith("early rally"):
        return "early_rally"
    if h.startswith("ai decisions") or h.startswith("model decisions"):
        return "jev"
    if h.startswith("checklist"):
        return None
    g = (h2 or "").lower()
    if g.startswith("3. growth screen"):
        return "growth"
    if g.startswith("3. stock briefs"):
        return "briefs"
    return None


def parse_report(path: Path) -> List[Dict]:
    """Every table row of a dated report as a dict (header -> cell), with ``symbol``, ``section`` and ``date``."""
    date = re.search(r"report_(\d{4}-\d{2}-\d{2})", str(path)).group(1)
    h2 = h3 = None
    header = None
    rows: List[Dict] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            h2, h3, header = line[3:].strip(), None, None
            continue
        if line.startswith("### "):
            h3, header = line[4:].strip(), None
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "symbol":
            header = cells
            continue
        if header is None or set(line) <= set("|:- "):
            continue
        sec = _section_of(h2, h3)
        if sec is None:
            continue
        m = _LINK.search(cells[0])
        if not m:
            continue
        row = dict(zip(header, cells))
        if sec == "wedge" and str(row.get("status", "")).startswith("forming"):
            sec = "wedge_watch"          # before the watch list existed, forming wedges sat in the signal table
        row.update(symbol=m.group(1), section=sec, date=date)
        rows.append(row)
    return rows


def _num(s) -> float:
    try:
        return float(str(s).replace("%", "").replace("$", "").replace("M", "").replace("x", "").replace(",", ""))
    except (TypeError, ValueError):
        return np.nan


def _flags_from_row(r: Dict) -> List[str]:
    """The flags (see :mod:`algovision.briefs`) reconstructed from a historical summary-table row."""
    out = []
    if "flags" in r and str(r.get("flags", "")).strip():
        return [c for c in str(r["flags"]).replace("*", "").split() if c in ("Z", "D", "S", "T")]
    z = re.search(r"z ([+-]?\d+\.\d+)", str(r.get("vs peers 20d", "")))
    if z and float(z.group(1)) <= -1:
        out.append("Z")
    if _num(r.get("from 52w high")) <= -40:
        out.append("D")
    if str(r.get("sentiment", "")).strip() == "negative":
        out.append("S")
    if _num(r.get("target upside")) >= 50:
        out.append("T")
    return out


def events(out_dir: Path) -> pd.DataFrame:
    """First appearance of every (section, symbol) in the dated reports, with that day's attributes and the day count."""
    rows: List[Dict] = []
    for p in sorted(glob.glob(str(Path(out_dir) / "report_????-??-??.md"))):
        rows += parse_report(Path(p))
    if not rows:
        return pd.DataFrame()
    R = pd.DataFrame(rows)
    first = R.sort_values("date").groupby(["section", "symbol"], as_index=False).first()
    cnt = R.groupby(["section", "symbol"]).size().rename("n_days").reset_index()
    first = first.merge(cnt, on=["section", "symbol"])
    first["flags"] = first.apply(lambda r: " ".join(_flags_from_row(r.to_dict())), axis=1)
    # the warning flags only (Z, S, T); D is a plus in the ten-year backtests and gets its own split
    first["n_flags"] = first["flags"].str.split().map(lambda f: sum(1 for x in (f or []) if x in ("Z", "S", "T"))).astype(int)
    first["market_wide"] = first.get("why fell", pd.Series("", index=first.index)).fillna("").str.contains("market-wide")
    return first


def forward(ev: pd.DataFrame, frames: Dict[str, pd.DataFrame], bench: pd.DataFrame) -> pd.DataFrame:
    """Attach forward returns from the next open after the report date: raw, vs SPY, vs the beaten-down basket of that day."""
    if not len(ev):
        return ev
    open_, close = build_panels({s: df for s, df in frames.items() if s != "SPY"})
    idx = close.index
    spy = bench.reindex(idx).ffill()
    members_cache: Dict[int, List[str]] = {}
    out = []
    for r in ev.to_dict("records"):
        s = r["symbol"]
        if s not in close.columns:
            continue
        d0 = pd.Timestamp(r["date"])
        pos0 = idx.searchsorted(d0, side="right") - 1      # the last bar on or before the report date
        e = pos0 + 1
        if pos0 < 0 or e >= len(idx):
            continue
        entry = open_[s].iloc[e]
        if not np.isfinite(entry) or entry <= 0:
            continue
        if pos0 not in members_cache:
            bm = beaten_mask(close, pos0)
            members_cache[pos0] = bm[bm].index.tolist()
        mem = members_cache[pos0]
        rec = dict(r)
        rec["entry_date"] = str(idx[e].date())
        for h in HORIZONS:
            j = e + h
            if j < len(idx):
                rec[f"ret_{h}"] = close[s].iloc[j] / entry - 1.0
                rec[f"spy_{h}"] = spy["Close"].iloc[j] / spy["Open"].iloc[e] - 1.0
                rec[f"bk_{h}"] = basket_return(open_, close, mem, e, j)
            else:
                rec[f"ret_{h}"] = rec[f"spy_{h}"] = rec[f"bk_{h}"] = np.nan
        j = len(idx) - 1
        rec["ret_latest"] = close[s].iloc[j] / entry - 1.0
        rec["spy_latest"] = spy["Close"].iloc[j] / spy["Open"].iloc[e] - 1.0
        rec["bk_latest"] = basket_return(open_, close, mem, e, j)
        rec["bars"] = j - e + 1
        out.append(rec)
    F = pd.DataFrame(out)
    for h in list(HORIZONS) + ["latest"]:
        F[f"xspy_{h}"] = F[f"ret_{h}"] - F[f"spy_{h}"]
        F[f"xbk_{h}"] = F[f"ret_{h}"] - F[f"bk_{h}"]
    return F


def _stats(g: pd.DataFrame) -> Dict:
    d: Dict = {"n": len(g)}
    for h in list(HORIZONS) + ["latest"]:
        r = g[f"ret_{h}"].dropna()
        d[f"n_{h}"] = len(r)
        d[f"mean_{h}"] = r.mean() if len(r) else np.nan
        d[f"hit_{h}"] = (r > 0).mean() if len(r) else np.nan
        d[f"xspy_{h}"] = g[f"xspy_{h}"].dropna().mean() if len(r) else np.nan
        d[f"xbk_{h}"] = g[f"xbk_{h}"].dropna().mean() if len(r) else np.nan
    return d


def scorecard(F: pd.DataFrame, min_n: int = 4) -> List[Dict]:
    """Rows of (group, label, stats) for the markdown; only groups with ``min_n`` names."""
    if not len(F):
        return []
    rows: List[Dict] = []

    def add(group: str, label_en: str, label_he: str, g: pd.DataFrame):
        if len(g) >= min_n:
            rows.append({"group": group, "en": label_en, "he": label_he, **_stats(g)})

    sig = F[F["section"].isin(["insider_beaten", "insider_other", "newsday", "wedge", "wedge_watch", "early_rally", "growth"])]
    for sec in ["newsday", "wedge", "wedge_watch", "insider_beaten", "insider_other", "early_rally", "growth"]:
        add("table", SECTION_EN[sec], SECTION_HE[sec], F[F["section"] == sec])
    B = F[F["section"] == "briefs"]
    add("briefs", "all briefs", "כל התקצירים", B)
    for nf, en, he in ((0, "no warning flag", "בלי דגלי אזהרה"), (1, "one warning flag", "דגל אזהרה אחד"), (2, "two or more warning flags", "שני דגלי אזהרה ומעלה")):
        g = B[B["n_flags"] == nf] if nf < 2 else B[B["n_flags"] >= 2]
        add("flags", en, he, g)
    for code, en, he in (("Z", "Z: z vs peers below -1", "Z: z מול עמיתים מתחת ל-1-"), ("D", "D: more than 40% below the 52-week high (a plus over ten years)", "D: יותר מ-40% מתחת לשיא 52 השבועות (פלוס על עשר שנים)"),
                         ("S", "S: negative sentiment", "S: סנטימנט שלילי"), ("T", "T: target upside above 50%", "T: אפסייד ליעד מעל 50%")):
        has = B["flags"].str.split().map(lambda f: code in (f or []))
        add("flag", en + " (yes)", he + " (כן)", B[has])
        add("flag", en + " (no)", he + " (לא)", B[~has])
    if "read" in B:
        for r, en, he in (("signs of a bottom", "read: signs of a bottom", "קריאה: סימני תחתית"), ("undecided", "read: undecided", "קריאה: לא מוכרע"),
                          ("still falling", "read: still falling", "קריאה: עדיין יורדת")):
            add("read", en, he, B[B["read"] == r])
    add("cause", "'market-wide' among the causes (yes)", "\"כלל-שוק\" בין הסיבות (כן)", B[B["market_wide"]])
    add("cause", "'market-wide' among the causes (no)", "\"כלל-שוק\" בין הסיבות (לא)", B[~B["market_wide"]])
    for lo, hi, en, he in ((1, 1, "listed 1 day", "יום אחד ברשימה"), (2, 3, "listed 2-3 days", "2-3 ימים"), (4, 7, "listed 4-7 days", "4-7 ימים"), (8, 10_000, "listed 8+ days", "8+ ימים")):
        add("days", en, he, sig[(sig["n_days"] >= lo) & (sig["n_days"] <= hi)])
    J = F[F["section"] == "jev"]
    if len(J) and "action" in J:
        for a, en, he in (("buy", "Jev: buy", "Jev: קנייה"), ("watch", "Jev: watch", "Jev: מעקב"), ("skip", "Jev: skip", "Jev: דילוג")):
            add("jev", en, he, J[J["action"] == a])
        if "P(buy)" in J:
            pb = J["P(buy)"].map(_num)
            add("jev", "Jev: P(buy) >= 0.6 (logged as jev_pick)", "Jev: P(קנייה) 0.6 ומעלה (נרשם כ-jev_pick)", J[pb >= 0.6])
            add("jev", "Jev: P(buy) < 0.2", "Jev: P(קנייה) מתחת ל-0.2", J[pb < 0.2])
    return rows


def _p(v, d=1) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def _h(v) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:.0f}%"


def lookback_markdown(rows: List[Dict], F: pd.DataFrame, lang: str = "en") -> List[str]:
    he = lang == "he"
    if not rows:
        return [("אין עדיין מספיק דוחות למאזן." if he else "Not enough dated reports yet for a ledger."), ""]
    first, last = F["date"].min(), F["date"].max()
    n_rep = F["date"].nunique()
    head = ("## 4. מה עבד עד עכשיו (כל שם שהדוחות הציגו)" if he else "## 4. What has worked so far (every name the reports listed)")
    intro = ((f"כל זוג (טבלה, מניה) נמדד מיום ההופעה הראשון שלו בדוחות ({first} עד {last}, {n_rep} דוחות): כניסה בפתיחה של היום הבא, תשואה אחרי "
              f"5, 10 ו-20 נרות ועד הסגירה האחרונה, מול SPY ומול סל המניות המוכות של אותו יום (ההשוואה ההוגנת לכלל שקונה רק מניות מוכות: \"מול הסל\" "
              f"חיובי פירושו שהפילטר בחר טוב מממוצע המניות המוכות). הדגלים: Z = z מול עמיתים מתחת ל-1-, S = סנטימנט שלילי, T = אפסייד ליעד מעל 50% "
              f"(אזהרות), D = יותר מ-40% מתחת לשיא 52 השבועות (פלוס בבדיקות עשר השנים, docs/research_filters.md). מאזן של הדוחות עצמם, לא בדיקה "
              f"לאחור: שבועות ספורים, משטר אחד, חלונות חופפים; n קטן בחתכים. \"פגיעה\" = חלק השמות עם תשואה חיובית.") if he else
             (f"Every (table, symbol) pair measured from its first appearance in the dated reports ({first} to {last}, {n_rep} reports): entry at the "
              f"next open, return after 5, 10 and 20 bars and to the latest close, against SPY and against the beaten-down basket of the same day "
              f"(the fair benchmark for a rule that only buys beaten-down stocks: a positive 'vs basket' means the filter picked better than the "
              f"average beaten-down stock). Flags: Z = z vs peers below -1, S = negative sentiment, T = target upside above 50% (warnings), "
              f"D = more than 40% below the 52-week high (a plus in the ten-year backtests, docs/research_filters.md). A ledger of the reports "
              f"themselves, not a backtest: a few weeks, one regime, overlapping windows; small n in the cuts. 'Hit' = share of names with a positive return."))
    cols_he = ["קבוצה", "n", "10 נרות", "פגיעה 10", "מול הסל 10", "n20", "20 נרות", "פגיעה 20", "מול SPY 20", "מול הסל 20", "עד היום", "פגיעה", "מול SPY", "מול הסל"]
    cols_en = ["group", "n", "10 bars", "hit 10", "vs basket 10", "n20", "20 bars", "hit 20", "vs SPY 20", "vs basket 20", "to date", "hit", "vs SPY", "vs basket"]
    lines = ["| " + " | ".join(cols_he if he else cols_en) + " |", "|" + "|".join([":--"] + ["--:"] * 13) + "|"]
    group_he = {"table": "לפי טבלה", "briefs": "תקצירים", "flags": "לפי מספר דגלים", "flag": "לפי דגל", "read": "לפי קריאה", "cause": "לפי סיבת הירידה",
                "days": "לפי ימים ברשימה", "jev": "לפי Jev"}
    group_en = {"table": "by table", "briefs": "briefs", "flags": "by number of flags", "flag": "by flag", "read": "by read", "cause": "by cause of the decline",
                "days": "by days listed", "jev": "by Jev"}
    cur = None
    for r in rows:
        if r["group"] != cur:
            cur = r["group"]
            lines.append(f"| **{group_he[cur] if he else group_en[cur]}** |" + " |" * 13)
        lines.append("| " + " | ".join([r["he"] if he else r["en"], str(r["n"]), _p(r["mean_10"]), _h(r["hit_10"]), _p(r["xbk_10"]), str(r["n_20"]),
                                        _p(r["mean_20"]), _h(r["hit_20"]), _p(r["xspy_20"]), _p(r["xbk_20"]), _p(r["mean_latest"]), _h(r["hit_latest"]),
                                        _p(r["xspy_latest"]), _p(r["xbk_latest"])]) + " |")
    return [head, "", intro, "", *lines, ""]


def run_lookback(out_dir: Path, frames: Dict[str, pd.DataFrame], bench: Optional[pd.DataFrame]) -> Dict:
    """Events, forward returns and the scorecard rows; also writes ``lookback.csv`` next to the reports."""
    ev = events(out_dir)
    if not len(ev) or bench is None:
        return {"events": ev, "forward": pd.DataFrame(), "rows": []}
    F = forward(ev, frames, bench)
    keep = [c for c in F.columns if not c.startswith("_")]
    F[keep].to_csv(Path(out_dir) / "lookback.csv", index=False)
    return {"events": ev, "forward": F, "rows": scorecard(F)}
