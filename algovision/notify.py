"""Deliver a report file to Telegram and/or e-mail.

Configuration is by environment variables only (never stored in the repo):

* Telegram, direct: ``TELEGRAM_BOT_TOKEN`` (from @BotFather) and ``TELEGRAM_CHAT_ID`` (your chat with the bot).
* Telegram, relay: ``TELEGRAM_RELAY_URL`` and ``TELEGRAM_RELAY_SECRET`` - an HTTPS endpoint that holds the bot
  credentials itself and accepts ``POST {"text", "secret"}`` or ``POST {"filename", "content", "caption", "secret"}``
  (the existing Val Town relay used by the other routines). Used when the direct variables are absent.
* E-mail (SMTP): ``SMTP_HOST`` (default smtp.gmail.com), ``SMTP_PORT`` (default 587), ``SMTP_USER``,
  ``SMTP_PASSWORD`` (for Gmail: an app password), ``REPORT_EMAIL_TO`` (default = SMTP_USER).

Channels whose variables are missing are skipped with a note, so the same command works everywhere.
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, List, Optional

TELEGRAM_LIMIT = 4000


def _chunks(text: str, limit: int = TELEGRAM_LIMIT) -> List[str]:
    out, cur = [], ""
    for line in text.splitlines(keepends=True):
        if len(cur) + len(line) > limit and cur:
            out.append(cur)
            cur = ""
        while len(line) > limit:                       # a single over-long line
            out.append(line[:limit])
            line = line[limit:]
        cur += line
    if cur:
        out.append(cur)
    return out


def _relay() -> Optional[Dict[str, str]]:
    url, secret = os.environ.get("TELEGRAM_RELAY_URL"), os.environ.get("TELEGRAM_RELAY_SECRET")
    return {"url": url, "secret": secret} if url and secret else None


def _relay_post(payload: Dict[str, str], timeout: int) -> Dict:
    import requests

    relay = _relay()
    if not relay:
        raise RuntimeError("TELEGRAM_RELAY_URL / TELEGRAM_RELAY_SECRET not set")
    r = requests.post(relay["url"], json={**payload, "secret": relay["secret"]}, timeout=timeout)
    body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if not r.ok or not body.get("ok", False):
        raise RuntimeError(f"relay returned {r.status_code}: {body.get('error') or body.get('telegram') or r.text[:200]}")
    return body


def send_telegram(text: str, token: Optional[str] = None, chat_id: Optional[str] = None, timeout: int = 30) -> int:
    """Send ``text`` as one or more plain-text messages; returns the number of messages sent.

    Uses the bot API directly when ``TELEGRAM_BOT_TOKEN``/``TELEGRAM_CHAT_ID`` are set, otherwise the relay.
    """
    import requests

    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        if _relay():
            return int(_relay_post({"text": text}, timeout=max(timeout, 60)).get("sent", 1))
        raise RuntimeError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID (or TELEGRAM_RELAY_URL / TELEGRAM_RELAY_SECRET) not set")
    n = 0
    for part in _chunks(text):
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat_id, "text": part, "disable_web_page_preview": True}, timeout=timeout)
        r.raise_for_status()
        n += 1
    return n


def send_telegram_document(path: Path, token: Optional[str] = None, chat_id: Optional[str] = None, caption: str = "",
                           timeout: int = 60) -> None:
    import requests

    token = token or os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        if _relay():
            _relay_post({"filename": Path(path).name, "content": Path(path).read_text(encoding="utf-8"),
                         "caption": caption[:1000]}, timeout=timeout)
            return
        raise RuntimeError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID (or TELEGRAM_RELAY_URL / TELEGRAM_RELAY_SECRET) not set")
    with open(path, "rb") as fh:
        r = requests.post(f"https://api.telegram.org/bot{token}/sendDocument", data={"chat_id": chat_id, "caption": caption[:1000]},
                          files={"document": (Path(path).name, fh)}, timeout=timeout)
    r.raise_for_status()


def markdown_to_html(text: str) -> str:
    try:
        import markdown as _md
        body = _md.markdown(text, extensions=["tables"])
    except Exception:  # noqa: BLE001
        import html
        body = "<pre>" + html.escape(text) + "</pre>"
    return ("<html><body style='font-family:system-ui,Arial,sans-serif;font-size:14px'>"
            "<style>table{border-collapse:collapse;font-size:12px}td,th{border:1px solid #ddd;padding:3px 6px}</style>"
            + body + "</body></html>")


def send_email(subject: str, text: str, to: Optional[str] = None, html: Optional[str] = None) -> str:
    host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    port = int(os.environ.get("SMTP_PORT", "587"))
    user, password = os.environ.get("SMTP_USER"), os.environ.get("SMTP_PASSWORD")
    to = to or os.environ.get("REPORT_EMAIL_TO") or user
    if not user or not password or not to:
        raise RuntimeError("SMTP_USER / SMTP_PASSWORD (and optionally REPORT_EMAIL_TO) not set")
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, user, to
    msg.set_content(text)
    if html:
        msg.add_alternative(html, subtype="html")
    with smtplib.SMTP(host, port, timeout=60) as s:
        s.starttls()
        s.login(user, password)
        s.send_message(msg)
    return to


def deliver(path: Path, subject: Optional[str] = None, telegram: bool = True, email: bool = True,
            as_document: bool = True) -> Dict[str, str]:
    """Send a report file through every configured channel; returns {channel: status}."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    subject = subject or text.splitlines()[0].lstrip("# ").strip()
    status: Dict[str, str] = {}
    if telegram:
        try:
            n = send_telegram(text)
            if as_document:
                send_telegram_document(path, caption=subject)
            status["telegram"] = f"sent ({n} message(s) + file)"
        except Exception as exc:  # noqa: BLE001
            status["telegram"] = f"skipped: {exc}"
    if email:
        try:
            to = send_email(subject, text, html=markdown_to_html(text))
            status["email"] = f"sent to {to}"
        except Exception as exc:  # noqa: BLE001
            status["email"] = f"skipped: {exc}"
    return status
