"""Short "what changed since the previous report" note that travels with the daily report.

The full report is delivered as an attached .md file; this note is the only text the reader sees in the
message body, so it lists exactly the tickers that entered (or left) each report table since the previous
report, plus the signals the journal logged today.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from algovision.links import tv

_LINK = re.compile(r"\[([A-Z][A-Z0-9.\-]*)\]\(https://www\.tradingview\.com/chart/\?symbol=[A-Z0-9.\-]+\)")
_HEADER = re.compile(r"^# AlgoVision daily report - (\d{4}-\d{2}-\d{2})", re.M)

# (label, heading line prefix that starts the section)
SECTIONS: List[Tuple[str, str]] = [
    ("Insider buys, beaten-down (tested setup)", "### Beaten-down stocks"),
    ("Insider buys, other stocks", "### Other stocks with insider purchases"),
    ("News-day", "### News-day rule"),
    ("Falling wedge, beaten-down", "### Falling Wedge in beaten-down stocks"),
    ("Early rally, beaten-down", "### Early rally in beaten-down stocks"),
]


def report_date(text: str) -> Optional[str]:
    m = _HEADER.search(text)
    return m.group(1) if m else None


def section_tickers(text: str) -> Dict[str, List[str]]:
    """Ordered, de-duplicated tickers of every report table, keyed by section label."""
    lines = text.splitlines()
    starts = []
    for label, prefix in SECTIONS:
        for i, line in enumerate(lines):
            if line.startswith(prefix):
                starts.append((i, label))
                break
    starts.sort()
    out: Dict[str, List[str]] = {label: [] for label, _ in SECTIONS}
    for k, (i, label) in enumerate(starts):
        end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
        # a section ends at the next heading of the same or higher level as well
        for j in range(i + 1, end):
            if lines[j].startswith("## ") or lines[j].startswith("### "):
                end = j
                break
        seen: List[str] = []
        for line in lines[i:end]:
            for s in _LINK.findall(line):
                if s not in seen:
                    seen.append(s)
        out[label] = seen
    return out


def previous_report(out_dir: Path, today: str) -> Optional[Path]:
    dated = sorted(p for p in Path(out_dir).glob("report_????-??-??.md") if p.stem[7:] < today)
    return dated[-1] if dated else None


def journal_new_signals(out_dir: Path) -> List[str]:
    """Rows of the journal's 'New signals today' table as '- rule: [SYM](url) date @ price - note' lines."""
    latest = Path(out_dir) / "latest.md"
    if not latest.exists():
        return []
    lines = latest.read_text(encoding="utf-8").splitlines()
    out: List[str] = []
    inside = False
    for line in lines:
        if line.startswith("## New signals today"):
            inside = True
            continue
        if inside and line.startswith("## "):
            break
        if inside and line.startswith("|") and not line.startswith("|:") and "rule" not in line.split("|")[1]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 6:
                rule, sym, date, price, hold, note = cells[:6]
                out.append(f"- {rule}: {sym} {date} @ {price}, hold {hold} bars. {note}")
    return out


LABEL_HE = {"Insider buys, beaten-down (tested setup)": "קניות אינסיידרים, מניות מוכות (התבנית שנבדקה)", "Insider buys, other stocks": "קניות אינסיידרים, מניות אחרות",
            "News-day": "יום חדשות", "Falling wedge, beaten-down": "טריז יורד, מניות מוכות", "Early rally, beaten-down": "ראלי מוקדם, מניות מוכות"}
SHORT_EN = {"Insider buys, beaten-down (tested setup)": "insider buys (beaten-down)", "Insider buys, other stocks": "insider buys (other)",
            "News-day": "news-day", "Falling wedge, beaten-down": "falling wedge", "Early rally, beaten-down": "early rally"}
SHORT_HE = {"Insider buys, beaten-down (tested setup)": "אינסיידרים (מוכות)", "Insider buys, other stocks": "אינסיידרים (אחרות)",
            "News-day": "יום חדשות", "Falling wedge, beaten-down": "טריז יורד", "Early rally, beaten-down": "ראלי מוקדם"}
RULE_HE = {"newsday": "יום חדשות", "falling_wedge_beaten_down": "טריז יורד במניה מוכה", "insider_buy_beaten_down": "קניית אינסיידר במניה מוכה",
           "jev_pick": "בחירת Jev", "early_rally_beaten_down": "ראלי מוקדם במניה מוכה"}
# the journal notes are short English key-value strings; these are their Hebrew readings
_NOTE_HE = [("hold ", "החזקה "), (" bars", " נרות"), ("gap ", "פער "), ("vol ", "מחזור פי "), ("6m ", "6 חודשים "), ("vs MA200 ", "מול ממוצע 200 "),
            ("score ", "ציון "), ("stop ", "סטופ "), ("level ", "רמה "), ("day ", "יום "), ("10d ", "10 ימים "), ("P(buy) ", "P(קנייה) ")]


def _note_he(line: str) -> str:
    out = line
    for en, he in _NOTE_HE:
        out = out.replace(en, he)
    for en, he in RULE_HE.items():
        out = out.replace(f"- {en}:", f"- {he}:")
    return out


def build_whatsnew(out_dir: Path, today: str, report_text: Optional[str] = None, briefs_url: Optional[str] = None,
                   wedge_url: Optional[str] = None, report_url: Optional[str] = None, lang: str = "en",
                   daily_url: Optional[str] = None) -> str:
    """The note in English (``lang="en"``) or Hebrew (``"he"``); the Hebrew one names the single Hebrew daily file."""
    out_dir = Path(out_dir)
    he = lang == "he"
    text = report_text if report_text is not None else (out_dir / "report_latest.md").read_text(encoding="utf-8")
    cur = section_tickers(text)
    prev_path = previous_report(out_dir, today)
    prev = section_tickers(prev_path.read_text(encoding="utf-8")) if prev_path else {k: [] for k in cur}
    prev_date = report_date(prev_path.read_text(encoding="utf-8")) if prev_path else None
    if he:
        md: List[str] = [f"# AlgoVision {today}: מה חדש" + (f" מאז {prev_date}" if prev_date else "") + "\n"]
    else:
        md = [f"# AlgoVision {today}: what is new" + (f" since {prev_date}" if prev_date else "") + "\n"]
    sig = journal_new_signals(out_dir)
    md.append(f"סיגנלים חדשים שנרשמו ביומן היום ({len(sig)}):" if he else f"New signals logged in the journal today ({len(sig)}):")
    md.extend(([_note_he(s) for s in sig] if he else sig) or (["- אין"] if he else ["- none"]))
    md.append("")
    md.append("נכנסו לטבלאות הדוח:" if he else "Entered the report tables:")
    any_add = False
    for label, _ in SECTIONS:
        added = [s for s in cur.get(label, []) if s not in prev.get(label, [])]
        if added:
            any_add = True
            md.append(f"- {LABEL_HE[label] if he else label}: " + ", ".join(tv(s) for s in added))
    if not any_add:
        md.append("- אין" if he else "- none")
    md.append("")
    md.append("יצאו מטבלאות הדוח:" if he else "Left the report tables:")
    any_rm = False
    for label, _ in SECTIONS:
        removed = [s for s in prev.get(label, []) if s not in cur.get(label, [])]
        if removed:
            any_rm = True
            md.append(f"- {LABEL_HE[label] if he else label}: " + ", ".join(removed))
    if not any_rm:
        md.append("- אין" if he else "- none")
    md.append("")
    short = SHORT_HE if he else SHORT_EN
    counts = ", ".join(f"{short.get(label, label)} {len(v)}" for label, v in cur.items())
    if he:
        md.append(f"הטבלאות כעת: {counts}. הקובץ המלא בעברית מצורף. לא ייעוץ השקעות.")
        if daily_url:
            md.append(f"הקובץ היומי המלא בעברית (כל הטבלאות, סיפור ציר הזמן, ניתוח הטריזים, תקציר לכל מניה, החלטות Jev ויומן המעקב): {daily_url}")
        if report_url:
            md.append(f"הדוח באנגלית: {report_url}")
        if briefs_url:
            md.append(f"התקצירים באנגלית: {briefs_url}")
        if wedge_url:
            md.append(f"קובץ הטריז היורד: {wedge_url}")
    else:
        md.append(f"Tables now: {counts}. Full report attached. Not investment advice.")
        if daily_url:
            md.append(f"Everything in one Hebrew file (all tables, the time-axis story, the wedge analyses, a brief per stock, Jev, the journal): {daily_url}")
        if report_url:
            md.append(f"Today's report on GitHub: {report_url}")
        if briefs_url:
            md.append(f"One research brief per listed stock (price context, what moved it, analysts, last report, fundamentals, rule-based read): {briefs_url}")
        if wedge_url:
            md.append(f"Falling wedge only, in Hebrew (technical analysis of each wedge, why it fell, brief; table rows link to the details): {wedge_url}")
    return "\n".join(md) + "\n"


def write_whatsnew(out_dir: Path, today: str, report_text: Optional[str] = None, briefs_url: Optional[str] = None,
                   wedge_url: Optional[str] = None, report_url: Optional[str] = None, daily_url: Optional[str] = None) -> Path:
    """Writes the English note (``new_<date>.md`` / ``new_latest.md``) and the Hebrew one (``new_he_<date>.md`` / ``new_he_latest.md``)."""
    out_dir = Path(out_dir)
    text = build_whatsnew(out_dir, today, report_text, briefs_url, wedge_url, report_url, "en", daily_url)
    (out_dir / f"new_{today}.md").write_text(text, encoding="utf-8")
    p = out_dir / "new_latest.md"
    p.write_text(text, encoding="utf-8")
    text_he = build_whatsnew(out_dir, today, report_text, briefs_url, wedge_url, report_url, "he", daily_url)
    (out_dir / f"new_he_{today}.md").write_text(text_he, encoding="utf-8")
    (out_dir / "new_he_latest.md").write_text(text_he, encoding="utf-8")
    return p
