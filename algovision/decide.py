"""Typed decisions on every brief from Jev (TypeSafe's System One decision model), through OpenRouter.

Jev does not write text: it reads a block of state (here: the stock's brief, the same evidence the reader sees) and
answers a fixed set of typed questions in one pass, each with a calibrated probability. It is used as a judge over
evidence the code has already gathered, never as a source of facts, and its "action" is forward-tested in the
journal as its own rule (``jev_pick``) next to the systematic rules, so its value is measured, not assumed.

Questions (``QUESTIONS``): is the drop a corporate action (spin-off, split) rather than a real decline; what kind
of decline; is a known event due inside the holding window; does the evidence support or contradict the technical
setup; how bad is the news for the business; and the action (buy / watch / skip) with probabilities.

API: ``POST https://openrouter.ai/api/alpha/decisions`` with ``{model, state, questions}`` (the key from
``OPENROUTER_API_KEY`` or ``~/.algovision/openrouter.key``); the native endpoint ``api.typesafe.ai/v1/systemone``
takes the same body. Pricing at the time of writing: $0.042 per million input tokens, output free; a brief is about
2,500 tokens, so a day of 50 briefs costs well under a cent. Every call is best effort: on any error the stock
simply gets no decision.
"""

from __future__ import annotations

import datetime as dt
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd

log = logging.getLogger(__name__)

OPENROUTER_URL = "https://openrouter.ai/api/alpha/decisions"
MODEL = os.environ.get("ALGOVISION_JEV_MODEL", "typesafe/jev-1.13")
KEY_FILE = Path(os.environ.get("ALGOVISION_OPENROUTER_KEY_FILE", str(Path.home() / ".algovision" / "openrouter.key")))
MAX_STATE_CHARS = 60_000      # the model's context is 32K tokens; briefs are ~10K characters
RULE = "jev_pick"
HOLD_BARS = 20
BUY_THRESHOLD = 0.60          # the journal logs a pick when P(buy) is at least this

QUESTIONS: Dict[str, Dict] = {
    "corporate_action": {
        "type": "noul",
        "instructions": "Is the stock's large price drop explained by a corporate action (spin-off, separation, stock split, special "
                        "dividend, rights issue) or a data error, rather than a real fall in the value of the business?",
        "criteria": {"true": "the evidence mentions a separation, spin-off, split, distribution or an unadjusted price series",
                     "false": "the drop reflects news, results or market moves"},
    },
    "cause_type": {
        "type": "choice",
        "instructions": "Based only on the evidence in the brief, what kind of decline is this?",
        "criteria": {
            "transitory": "a one-off event (a missed quarter, a guidance cut, a lawsuit headline) the business can absorb",
            "structural": "a lasting problem: losing share, a broken business model, secular decline, heavy debt",
            "sector_wide": "the whole industry or market fell for the same reason, not this company",
            "corporate_action": "a spin-off, split or similar mechanical price change",
            "unknown": "the brief does not say why the stock fell",
        },
    },
    "event_ahead": {
        "type": "noul",
        "instructions": "Is a known scheduled event (earnings report, court ruling, regulatory decision, shareholder vote) due within "
                        "the next four weeks according to the brief?",
    },
    "evidence_vs_setup": {
        "type": "choice",
        "instructions": "The technical rule says the stock is beaten down and may be bottoming. Does the fundamental and news evidence "
                        "in the brief support that, contradict it, or say nothing either way?",
        "criteria": {
            "supports": "estimates stable or rising, analysts not cutting further, the cause looks transitory, sentiment improving",
            "contradicts": "estimates still being cut, targets falling, the cause looks structural, more bad news likely",
            "neutral": "mixed or insufficient evidence",
        },
    },
    "severity": {
        "type": "score",
        "instructions": "How bad is the news behind the decline for the company's business?",
        "criteria": ["no real damage", "modest damage", "serious damage", "existential"],
    },
    "action": {
        "type": "choice",
        "instructions": "Given everything in the brief, what should a systematic buyer of beaten-down stocks do with this one now, "
                        "for a hold of about one month?",
        "criteria": {
            "buy": "the setup and the evidence together favour a bounce over the next month",
            "watch": "interesting but something must resolve first (an event, a confirmation, clearer evidence)",
            "skip": "the evidence argues against a bounce, or the setup is an artefact",
        },
    },
}

LABEL_EN = {"buy": "buy", "watch": "watch", "skip": "skip", "transitory": "transitory", "structural": "structural",
            "sector_wide": "sector-wide", "corporate_action": "corporate action", "unknown": "unknown",
            "supports": "supports", "contradicts": "contradicts", "neutral": "neutral"}
LABEL_HE = {"buy": "קנייה", "watch": "מעקב", "skip": "דילוג", "transitory": "חולף", "structural": "מבני",
            "sector_wide": "סקטוריאלי", "corporate_action": "פעולה תאגידית", "unknown": "לא ידוע",
            "supports": "תומכות", "contradicts": "סותרות", "neutral": "ניטרליות"}
SEVERITY_HE = ["ללא נזק ממשי", "נזק מתון", "נזק רציני", "קיומי"]


def api_key() -> Optional[str]:
    k = os.environ.get("OPENROUTER_API_KEY")
    if k:
        return k.strip()
    try:
        if KEY_FILE.exists():
            return KEY_FILE.read_text().strip() or None
    except OSError:
        pass
    return None


def available() -> bool:
    return api_key() is not None


def ask(state: str, questions: Dict[str, Dict] = QUESTIONS, timeout: int = 30, retries: int = 2) -> Dict:
    """One call: {answers: {...}, usage: {...}, model}. Raises on a hard error; retries 429 / 5xx."""
    import requests

    key = api_key()
    if not key:
        raise RuntimeError("no OpenRouter API key (OPENROUTER_API_KEY or ~/.algovision/openrouter.key)")
    body = {"model": MODEL, "state": state[:MAX_STATE_CHARS], "questions": questions}
    last = None
    for attempt in range(retries + 1):
        r = requests.post(OPENROUTER_URL, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                          json=body, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        last = f"HTTP {r.status_code}: {r.text[:300]}"
        if r.status_code in (429, 500, 502, 503, 529) and attempt < retries:
            time.sleep(2 ** attempt)
            continue
        break
    raise RuntimeError(last or "decision request failed")


def flatten(answers: Dict) -> Dict:
    """The answers as one flat row: action, p_buy/p_watch/p_skip, cause_type (+confidence), corporate_action, event_ahead,
    evidence (+confidence), severity (0-3 weighted score)."""
    a = answers.get("action") or {}
    c = answers.get("cause_type") or {}
    e = answers.get("evidence_vs_setup") or {}
    s = answers.get("severity") or {}
    p = a.get("probabilities") or {}
    return {
        "action": a.get("choice"), "p_buy": p.get("buy"), "p_watch": p.get("watch"), "p_skip": p.get("skip"),
        "action_confidence": a.get("confidence"),
        "cause_type": c.get("choice"), "cause_confidence": c.get("confidence"),
        "corporate_action": (answers.get("corporate_action") or {}).get("noul"),
        "event_ahead": (answers.get("event_ahead") or {}).get("noul"),
        "evidence": e.get("choice"), "evidence_confidence": e.get("confidence"),
        "severity": s.get("score"), "severity_confidence": s.get("confidence"),
    }


def decide_briefs(briefs: Dict[str, str], today: str, progress=None) -> Dict[str, Dict]:
    """Ask Jev about every brief. {symbol: flat row + date, model, input_tokens, cost}; symbols that failed are absent."""
    out: Dict[str, Dict] = {}
    for i, (s, text) in enumerate(briefs.items(), 1):
        try:
            res = ask(text)
        except Exception as exc:  # noqa: BLE001
            log.warning("%s: decision failed (%s)", s, exc)
            continue
        row = flatten(res.get("answers") or {})
        usage = res.get("usage") or {}
        row.update({"symbol": s, "date": today, "model": res.get("model") or MODEL,
                    "input_tokens": usage.get("input_tokens"), "cost": usage.get("cost")})
        out[s] = row
        if progress and (i % 10 == 0 or i == len(briefs)):
            progress(i, len(briefs))
    return out


def write_decisions(out_dir: Path, today: str, decisions: Dict[str, Dict]) -> Path:
    """Append today's rows to ``decisions.csv`` (one row per symbol per day; a rerun replaces the day's rows)."""
    out_dir = Path(out_dir)
    p = out_dir / "decisions.csv"
    new = pd.DataFrame(list(decisions.values()))
    new["date"] = today
    if p.exists():
        old = pd.read_csv(p)
        old = old[old["date"].astype(str) != today]
        new = pd.concat([old, new], ignore_index=True)
    cols = ["date", "symbol", "action", "p_buy", "p_watch", "p_skip", "action_confidence", "cause_type", "cause_confidence",
            "corporate_action", "event_ahead", "evidence", "evidence_confidence", "severity", "severity_confidence", "model",
            "input_tokens", "cost"]
    new = new.reindex(columns=[c for c in cols if c in new.columns] + [c for c in new.columns if c not in cols])
    new.to_csv(p, index=False)
    return p


def log_picks(out_dir: Path, today: str, decisions: Dict[str, Dict], frames: Dict[str, pd.DataFrame],
              threshold: float = BUY_THRESHOLD) -> List[str]:
    """Log ``jev_pick`` signals in the journal (signals.csv) for the stocks the model says to buy with P(buy) >= threshold
    and no open jev_pick position; the journal marks them to market like every other rule."""
    from algovision.journal import COLS, _load

    out_dir = Path(out_dir)
    path = out_dir / "signals.csv"
    journal = _load(path)
    open_ = set(journal[(journal["rule"] == RULE) & (journal["status"] != "closed")]["symbol"]) if len(journal) else set()
    existing = set(zip(journal["rule"], journal["symbol"], journal["signal_date"])) if len(journal) else set()
    rows = []
    for s, d in decisions.items():
        pb = d.get("p_buy")
        if d.get("action") != "buy" or pb is None or pb < threshold or s in open_ or (RULE, s, today) in existing:
            continue
        df = frames.get(s)
        if df is None or not len(df):
            continue
        rows.append({"logged": today, "rule": RULE, "symbol": s, "signal_date": today, "status": "open",
                     "ref_price": f"{float(df['Close'].iloc[-1]):.4f}", "entry_date": "", "entry_price": "", "hold_bars": HOLD_BARS,
                     "note": f"P(buy) {pb:.2f}, cause {d.get('cause_type')}, evidence {d.get('evidence')}, severity {d.get('severity')}"})
    if rows:
        journal = pd.concat([journal, pd.DataFrame(rows)[COLS]], ignore_index=True)
        journal.to_csv(path, index=False)
    return [r["symbol"] for r in rows]


SKIP_RULE = "jev_skip"
SKIP_THRESHOLD = 0.50


def log_skips(out_dir: Path, today: str, decisions: Dict[str, Dict], frames: Dict[str, pd.DataFrame],
              threshold: float = SKIP_THRESHOLD) -> List[str]:
    """Log ``jev_skip`` signals for the stocks the model says to skip with P(skip) >= threshold (no open jev_skip position).
    The journal marks them to market like a long position; the model's call is right when the return is negative, which is
    why the rule's expectation says so. In the first week of the forward test the 'skip' names did better than the 'buy'
    names, so the call is tracked rather than trusted."""
    from algovision.journal import COLS, _load

    out_dir = Path(out_dir)
    path = out_dir / "signals.csv"
    journal = _load(path)
    open_ = set(journal[(journal["rule"] == SKIP_RULE) & (journal["status"] != "closed")]["symbol"]) if len(journal) else set()
    existing = set(zip(journal["rule"], journal["symbol"], journal["signal_date"])) if len(journal) else set()
    rows = []
    for s, d in decisions.items():
        ps = d.get("p_skip")
        if d.get("action") != "skip" or ps is None or ps < threshold or s in open_ or (SKIP_RULE, s, today) in existing:
            continue
        df = frames.get(s)
        if df is None or not len(df):
            continue
        rows.append({"logged": today, "rule": SKIP_RULE, "symbol": s, "signal_date": today, "status": "open",
                     "ref_price": f"{float(df['Close'].iloc[-1]):.4f}", "entry_date": "", "entry_price": "", "hold_bars": HOLD_BARS,
                     "note": f"P(skip) {ps:.2f}, cause {d.get('cause_type')}, evidence {d.get('evidence')}, severity {d.get('severity')}"})
    if rows:
        journal = pd.concat([journal, pd.DataFrame(rows)[COLS]], ignore_index=True)
        journal.to_csv(path, index=False)
    return [r["symbol"] for r in rows]


# ----------------------------------------------------------------------------
# rendering
# ----------------------------------------------------------------------------
def _f(v, d=2):
    return "" if v is None or (isinstance(v, float) and v != v) else f"{v:.{d}f}"


def decision_cell(d: Optional[Dict], lang: str = "en") -> str:
    """Compact cell for the summary tables: 'buy 0.71' / 'קנייה 0.71'."""
    if not d or not d.get("action"):
        return ""
    lab = (LABEL_HE if lang == "he" else LABEL_EN).get(d["action"], d["action"])
    p = {"buy": d.get("p_buy"), "watch": d.get("p_watch"), "skip": d.get("p_skip")}.get(d["action"])
    flag = ""
    if (d.get("corporate_action") or 0) >= 0.5:
        flag = " ⚠" if lang == "he" else " !"
    return f"{lab} {_f(p)}{flag}"


def decision_markdown(d: Dict, lang: str = "en") -> List[str]:
    """The decision block for a brief / the Hebrew wedge section."""
    he = lang == "he"
    lab = LABEL_HE if he else LABEL_EN
    sev = d.get("severity")
    sev_txt = ""
    if sev is not None:
        i = int(round(sev))
        name = SEVERITY_HE[min(3, max(0, i))] if he else QUESTIONS["severity"]["criteria"][min(3, max(0, i))]
        sev_txt = f"{_f(sev, 1)} ({name})"
    parts = [
        (f"**פעולה: {lab.get(d.get('action'), d.get('action'))}** (קנייה {_f(d.get('p_buy'))}, מעקב {_f(d.get('p_watch'))}, דילוג {_f(d.get('p_skip'))})" if he
         else f"**Action: {lab.get(d.get('action'), d.get('action'))}** (buy {_f(d.get('p_buy'))}, watch {_f(d.get('p_watch'))}, skip {_f(d.get('p_skip'))})"),
        (f"סוג הירידה: {lab.get(d.get('cause_type'), d.get('cause_type'))} (ביטחון {_f(d.get('cause_confidence'))})" if he
         else f"kind of decline: {lab.get(d.get('cause_type'), d.get('cause_type'))} (confidence {_f(d.get('cause_confidence'))})"),
        (f"הסתברות שזו פעולה תאגידית/בעיית נתונים ולא ירידה אמיתית: {_f(d.get('corporate_action'))}" if he
         else f"P(corporate action / data artefact, not a real decline): {_f(d.get('corporate_action'))}"),
        (f"אירוע ידוע ב-4 השבועות הקרובים: {_f(d.get('event_ahead'))}" if he else f"P(known event within 4 weeks): {_f(d.get('event_ahead'))}"),
        (f"הראיות מול התבנית: {lab.get(d.get('evidence'), d.get('evidence'))} (ביטחון {_f(d.get('evidence_confidence'))})" if he
         else f"evidence vs the setup: {lab.get(d.get('evidence'), d.get('evidence'))} (confidence {_f(d.get('evidence_confidence'))})"),
        (f"חומרת החדשות לעסק: {sev_txt}" if he else f"severity of the news for the business: {sev_txt}"),
    ]
    head = ("### החלטת AI (Jev)" if he else "**AI decision (Jev).** ")
    note = ("מודל החלטה טיפוסי (TypeSafe Jev דרך OpenRouter) שקרא את התקציר הזה בלבד וענה על שאלות קבועות עם הסתברויות מכוילות; "
            "אין לו נימוק. ההחלטה נמדדת ביומן ככלל נפרד (jev_pick) ואינה מחליפה את הכללים שנבדקו." if he else
            "A typed decision model (TypeSafe Jev via OpenRouter) that read only this brief and answered fixed questions with calibrated "
            "probabilities; it gives no rationale. Its action is forward-tested in the journal as its own rule (jev_pick) and does not "
            "replace the tested rules.")
    if he:
        return [head, "", "; ".join(parts) + ".", "", f"*{note}*", ""]
    return [head + "; ".join(parts) + ".", "", f"*{note}*", ""]


# ----------------------------------------------------------------------------
# briefs file helpers (for the CLI and backfills)
# ----------------------------------------------------------------------------
_HEAD = re.compile(r"^## \[([A-Z.\-]+)\]\(", re.M)


def split_briefs(text: str) -> Dict[str, str]:
    """{symbol: section markdown} from a briefs_<date>.md file."""
    out: Dict[str, str] = {}
    heads = list(_HEAD.finditer(text))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out[m.group(1)] = text[m.start():end].strip()
    return out


def decide_file(path: Path, today: Optional[str] = None, symbols: Optional[Iterable[str]] = None, progress=None) -> Dict[str, Dict]:
    text = Path(path).read_text(encoding="utf-8")
    m = re.search(r"^# AlgoVision stock briefs - (\d{4}-\d{2}-\d{2})", text, re.M)
    today = today or (m.group(1) if m else dt.date.today().isoformat())
    briefs = split_briefs(text)
    if symbols:
        want = {s.upper() for s in symbols}
        briefs = {s: t for s, t in briefs.items() if s in want}
    return decide_briefs(briefs, today, progress=progress)


def decisions_table(decisions: Dict[str, Dict], tv=None) -> str:
    """Markdown table of today's decisions, most bullish first."""
    if not decisions:
        return "none\n"
    rows = sorted(decisions.values(), key=lambda d: -(d.get("p_buy") or 0))
    t = pd.DataFrame({
        "symbol": [tv(d["symbol"]) if tv else d["symbol"] for d in rows],
        "action": [d.get("action") for d in rows], "P(buy)": [_f(d.get("p_buy")) for d in rows],
        "P(watch)": [_f(d.get("p_watch")) for d in rows], "P(skip)": [_f(d.get("p_skip")) for d in rows],
        "kind of decline": [d.get("cause_type") for d in rows], "evidence vs setup": [d.get("evidence") for d in rows],
        "P(corporate action)": [_f(d.get("corporate_action")) for d in rows], "P(event in 4w)": [_f(d.get("event_ahead")) for d in rows],
        "severity 0-3": [_f(d.get("severity"), 1) for d in rows],
    })
    return t.to_markdown(index=False) + "\n"


def summary_json(decisions: Dict[str, Dict]) -> str:
    return json.dumps({s: {k: v for k, v in d.items() if k in ("action", "p_buy", "cause_type", "evidence", "corporate_action")}
                       for s, d in decisions.items()}, ensure_ascii=False)


def load_decisions(out_dir: Path, today: str) -> Dict[str, Dict]:
    """Today's rows of ``decisions.csv`` as {symbol: row} (empty when the file or the day is missing)."""
    p = Path(out_dir) / "decisions.csv"
    if not p.exists():
        return {}
    t = pd.read_csv(p)
    t = t[t["date"].astype(str) == today]
    out = {}
    for r in t.to_dict("records"):
        out[str(r["symbol"])] = {k: (None if isinstance(v, float) and v != v else v) for k, v in r.items()}
    return out


def top_picks(decisions: Dict[str, Dict], threshold: float = BUY_THRESHOLD) -> List[Dict]:
    """The stocks the model rates 'buy' with P(buy) >= threshold, most confident first."""
    picks = [d for d in decisions.values() if d.get("action") == "buy" and (d.get("p_buy") or 0) >= threshold]
    return sorted(picks, key=lambda d: -(d.get("p_buy") or 0))


def top_picks_he(decisions: Dict[str, Dict], anchors: Dict[str, str], tv_url, briefs_url: Optional[str] = None,
                 peers: Optional[Dict[str, Dict]] = None, threshold: float = BUY_THRESHOLD) -> List[str]:
    """Hebrew section: the stocks Jev prioritised (P(buy) >= threshold), with links to their details."""
    from algovision.peers import peers_short

    md = ["<a id=\"ai-picks\" name=\"ai-picks\"></a>", "## המניות שהמודל סימן \"קנייה\" (נרשמות ליומן כ-jev_pick)", "",
          f"כל המניות שבטבלאות הדוח היום שמודל ההחלטה סימן \"קנייה\" בהסתברות {threshold:.2f} ומעלה, מהבטוחה ביותר למטה. זה מבחן קדימה של המודל, "
          "לא רשימת עדיפות: בשבוע הראשון שמות ה\"דילוג\" שלו עשו טוב יותר משמות ה\"קנייה\". המודל קרא רק את התקציר של כל מניה; אין לו נימוק, "
          "וההחלטות נמדדות ביומן ככלל jev_pick. \"פירוט\" מקפיץ לסעיף המניה בקובץ הזה (לטריזים) או לתקציר באנגלית ב-GitHub (לשאר).", ""]
    picks = top_picks(decisions, threshold)
    if not picks:
        md += [f"אין היום מניות עם הסתברות קנייה של {threshold:.2f} ומעלה.", ""]
        return md
    rows = []
    for d in picks:
        s = d["symbol"]
        if s in anchors:
            detail = f"[פירוט](#{anchors[s]})"
        elif briefs_url:
            detail = f"[תקציר]({briefs_url})"
        else:
            detail = ""
        tables = str(d.get("tables") or "").replace("falling wedge", "טריז יורד").replace("news-day", "יום חדשות") \
            .replace("insider buys (beaten-down)", "אינסיידרים (מוכות)").replace("insider buys (other)", "אינסיידרים (אחרות)")
        read = {"signs of a bottom": "סימני תחתית", "undecided": "לא מוכרע", "still falling": "עדיין יורדת"}.get(d.get("read") or "", d.get("read") or "")
        sev = d.get("severity")
        rows.append({
            "סימול": f"[{s}]({tv_url(s)})", "פירוט": detail, "בטבלאות": tables,
            "P(קנייה)": _f(d.get("p_buy")), "P(מעקב)": _f(d.get("p_watch")), "P(דילוג)": _f(d.get("p_skip")),
            "סוג הירידה": LABEL_HE.get(d.get("cause_type"), d.get("cause_type") or ""),
            "הראיות מול התבנית": LABEL_HE.get(d.get("evidence"), d.get("evidence") or ""),
            "אירוע ב-4 שבועות": _f(d.get("event_ahead")),
            "חומרה 0-3": (f"{_f(sev, 1)} ({SEVERITY_HE[min(3, max(0, int(round(sev))))]})" if sev is not None else ""),
            "פעולה תאגידית?": ("⚠ " + _f(d.get("corporate_action"))) if (d.get("corporate_action") or 0) >= 0.5 else _f(d.get("corporate_action")),
            "קריאה מבוססת כללים": read + (f" ({float(d['score']):+g})" if d.get("score") is not None else ""),
            "מול עמיתים 20 יום": peers_short((peers or {}).get(s)),
        })
    md += [pd.DataFrame(rows).to_markdown(index=False), ""]
    return md
