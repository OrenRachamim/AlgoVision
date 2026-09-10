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
    ("Growth screen", "## 3. Growth screen"),
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


def build_whatsnew(out_dir: Path, today: str, report_text: Optional[str] = None) -> str:
    out_dir = Path(out_dir)
    text = report_text if report_text is not None else (out_dir / "report_latest.md").read_text(encoding="utf-8")
    cur = section_tickers(text)
    prev_path = previous_report(out_dir, today)
    prev = section_tickers(prev_path.read_text(encoding="utf-8")) if prev_path else {k: [] for k in cur}
    prev_date = report_date(prev_path.read_text(encoding="utf-8")) if prev_path else None
    md: List[str] = [f"# AlgoVision {today}: what is new" + (f" since {prev_date}" if prev_date else "") + "\n"]
    sig = journal_new_signals(out_dir)
    md.append(f"New signals logged in the journal today ({len(sig)}):")
    md.extend(sig or ["- none"])
    md.append("")
    md.append("Entered the report tables:")
    any_add = False
    for label, _ in SECTIONS:
        added = [s for s in cur.get(label, []) if s not in prev.get(label, [])]
        if added:
            any_add = True
            md.append(f"- {label}: " + ", ".join(tv(s) for s in added))
    if not any_add:
        md.append("- none")
    md.append("")
    md.append("Left the report tables:")
    any_rm = False
    for label, _ in SECTIONS:
        removed = [s for s in prev.get(label, []) if s not in cur.get(label, [])]
        if removed:
            any_rm = True
            md.append(f"- {label}: " + ", ".join(removed))
    if not any_rm:
        md.append("- none")
    md.append("")
    short = {"Insider buys, beaten-down (tested setup)": "insider buys (beaten-down)", "Insider buys, other stocks": "insider buys (other)",
             "News-day": "news-day", "Falling wedge, beaten-down": "falling wedge", "Growth screen": "growth screen"}
    counts = ", ".join(f"{short.get(label, label)} {len(v)}" for label, v in cur.items())
    md.append(f"Tables now: {counts}. Full report attached. Not investment advice.")
    return "\n".join(md) + "\n"


def write_whatsnew(out_dir: Path, today: str, report_text: Optional[str] = None) -> Path:
    out_dir = Path(out_dir)
    text = build_whatsnew(out_dir, today, report_text)
    (out_dir / f"new_{today}.md").write_text(text, encoding="utf-8")
    p = out_dir / "new_latest.md"
    p.write_text(text, encoding="utf-8")
    return p
