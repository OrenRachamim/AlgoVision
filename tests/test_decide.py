import json

import pandas as pd
import pytest

from algovision import decide as D

ANSWERS = {
    "corporate_action": {"type": "noul", "noul": 0.07},
    "cause_type": {"type": "choice", "choice": "transitory", "confidence": 0.8,
                   "probabilities": {"transitory": 0.85, "structural": 0.1, "sector_wide": 0.03, "corporate_action": 0.0, "unknown": 0.02}},
    "event_ahead": {"type": "noul", "noul": 0.9},
    "evidence_vs_setup": {"type": "choice", "choice": "supports", "confidence": 0.6,
                          "probabilities": {"supports": 0.7, "contradicts": 0.1, "neutral": 0.2}},
    "severity": {"type": "score", "score": 1.2, "confidence": 0.4, "legend": {}, "probabilities": {}},
    "action": {"type": "choice", "choice": "buy", "confidence": 0.5, "probabilities": {"buy": 0.66, "watch": 0.24, "skip": 0.10}},
}


class _Resp:
    def __init__(self, status, payload):
        self.status_code = status
        self._p = payload
        self.text = json.dumps(payload)

    def json(self):
        return self._p


def _fake_post(calls, statuses=None):
    statuses = list(statuses or [])

    def post(url, headers=None, json=None, timeout=None):
        calls.append({"url": url, "auth": headers.get("Authorization", ""), "body": json})
        st = statuses.pop(0) if statuses else 200
        if st != 200:
            return _Resp(st, {"error": {"message": "nope"}})
        return _Resp(200, {"model": "typesafe/jev-1.13-test", "answers": ANSWERS, "usage": {"input_tokens": 500, "output_tokens": 90, "cost": 2.1e-05}})
    return post


def test_questions_are_well_formed():
    for k, q in D.QUESTIONS.items():
        assert q["type"] in ("noul", "choice", "score") and q["instructions"]
        if q["type"] == "choice":
            assert isinstance(q["criteria"], dict) and len(q["criteria"]) >= 2
        if q["type"] == "score":
            assert isinstance(q["criteria"], list) and 2 <= len(q["criteria"]) <= 10
    assert set(D.QUESTIONS["action"]["criteria"]) == {"buy", "watch", "skip"}


def test_ask_flatten_and_retry(monkeypatch):
    calls = []
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    monkeypatch.setattr("requests.post", _fake_post(calls, statuses=[503, 200]))
    monkeypatch.setattr(D.time, "sleep", lambda s: None)
    res = D.ask("some brief")
    assert len(calls) == 2 and calls[0]["auth"] == "Bearer sk-test" and calls[0]["body"]["model"] == D.MODEL
    assert set(calls[0]["body"]["questions"]) == set(D.QUESTIONS) and calls[0]["body"]["state"] == "some brief"
    d = D.flatten(res["answers"])
    assert d["action"] == "buy" and d["p_buy"] == 0.66 and d["cause_type"] == "transitory" and d["corporate_action"] == 0.07
    assert d["evidence"] == "supports" and d["severity"] == 1.2 and d["event_ahead"] == 0.9
    monkeypatch.setattr("requests.post", _fake_post([], statuses=[400]))
    with pytest.raises(RuntimeError):
        D.ask("x")
    monkeypatch.delenv("OPENROUTER_API_KEY")
    monkeypatch.setattr(D, "KEY_FILE", D.Path("/nonexistent/key"))
    assert not D.available()


def test_decide_write_log_and_render(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    monkeypatch.setattr("requests.post", _fake_post([]))
    dec = D.decide_briefs({"AAA": "brief a", "BBB": "brief b"}, "2026-01-05")
    assert set(dec) == {"AAA", "BBB"} and dec["AAA"]["date"] == "2026-01-05" and dec["AAA"]["cost"] == 2.1e-05
    p = D.write_decisions(tmp_path, "2026-01-05", dec)
    again = D.write_decisions(tmp_path, "2026-01-05", dec)            # a rerun replaces the day's rows
    t = pd.read_csv(again)
    assert len(t) == 2 and list(t.columns[:3]) == ["date", "symbol", "action"]
    idx = pd.bdate_range("2025-01-01", periods=300)
    frames = {s: pd.DataFrame({"Close": [10.0] * 300}, index=idx) for s in ("AAA", "BBB")}
    picks = D.log_picks(tmp_path, "2026-01-05", dec, frames)
    assert picks == ["AAA", "BBB"]
    j = pd.read_csv(tmp_path / "signals.csv")
    assert (j["rule"] == "jev_pick").sum() == 2 and j["hold_bars"].iloc[0] == 20 and "P(buy) 0.66" in j["note"].iloc[0]
    assert D.log_picks(tmp_path, "2026-01-06", dec, frames) == []     # already open: not logged twice
    low = {"CCC": {**dec["AAA"], "symbol": "CCC", "p_buy": 0.4}}
    assert D.log_picks(tmp_path, "2026-01-06", low, {"CCC": frames["AAA"]}) == []
    assert D.decision_cell(dec["AAA"]) == "buy 0.66" and D.decision_cell(dec["AAA"], "he") == "קנייה 0.66" and D.decision_cell(None) == ""
    flagged = {**dec["AAA"], "corporate_action": 0.9}
    assert D.decision_cell(flagged).endswith("!") and D.decision_cell(flagged, "he").endswith("⚠")
    en = "\n".join(D.decision_markdown(dec["AAA"], "en"))
    he = "\n".join(D.decision_markdown(dec["AAA"], "he"))
    assert en.startswith("**AI decision (Jev).** **Action: buy**") and "modest damage" in en and "jev_pick" in en
    assert he.startswith("### החלטת AI (Jev)") and "**פעולה: קנייה**" in he and "נזק מתון" in he
    table = D.decisions_table(dec)
    assert "| symbol" in table and "AAA" in table and "P(buy)" in table
    assert json.loads(D.summary_json(dec))["AAA"]["action"] == "buy"


def test_split_briefs_and_decide_file(tmp_path, monkeypatch):
    text = ("# AlgoVision stock briefs - 2026-02-02\n\nintro\n\n## Summary\n\n| x |\n\n"
            "## [AAA](https://www.tradingview.com/chart/?symbol=AAA) Alpha Inc\n\nbody a\n\n"
            "## [BB.B](https://www.tradingview.com/chart/?symbol=BB.B) Beta\n\nbody b\n")
    parts = D.split_briefs(text)
    assert set(parts) == {"AAA", "BB.B"} and parts["AAA"].startswith("## [AAA]") and "body a" in parts["AAA"] and "body b" not in parts["AAA"]
    f = tmp_path / "briefs_2026-02-02.md"
    f.write_text(text, encoding="utf-8")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test")
    calls = []
    monkeypatch.setattr("requests.post", _fake_post(calls))
    out = D.decide_file(f, symbols=["aaa"])
    assert set(out) == {"AAA"} and out["AAA"]["date"] == "2026-02-02" and calls[0]["body"]["state"].startswith("## [AAA]")
