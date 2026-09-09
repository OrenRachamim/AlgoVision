"""EDGAR daily-index caching: settled days come from the cache, recent days are always re-fetched."""

import pandas as pd

from algovision.data import insiders_live as il

CIK = "0000123456"
LINE = "4           ACME CORP                    {cik}   {date}  edgar/data/123456/{acc}.txt\n"


def _idx(date: str, *accs: str) -> str:
    return "Form Type   Company Name   CIK   Date Filed   File Name\n" + "".join(LINE.format(cik=CIK, date=date, acc=a) for a in accs)


def test_index_is_settled_window():
    today = pd.Timestamp("2026-09-09")                      # a Wednesday
    assert not il._index_is_settled(pd.Timestamp("2026-09-09"), today)   # today
    assert not il._index_is_settled(pd.Timestamp("2026-09-08"), today)   # previous business day
    assert il._index_is_settled(pd.Timestamp("2026-09-07"), today)
    monday = pd.Timestamp("2026-09-14")
    assert not il._index_is_settled(pd.Timestamp("2026-09-11"), monday)  # Friday before a Monday
    assert il._index_is_settled(pd.Timestamp("2026-09-10"), monday)


def test_settled_day_served_from_cache(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(il, "_get", lambda url, timeout=60: calls.append(url) or b"unused")
    day = pd.Timestamp.today().normalize() - pd.offsets.BDay(5)
    (tmp_path / f"form.{day:%Y%m%d}.idx").write_text(_idx(day.strftime("%Y%m%d"), "old"))
    out = il.daily_form4(day, [CIK], tmp_path)
    assert [e["path"] for e in out] == ["edgar/data/123456/old.txt"]
    assert calls == []


def test_recent_day_refetched_and_cache_refreshed(tmp_path, monkeypatch):
    day = pd.Timestamp.today().normalize()
    stale = tmp_path / f"form.{day:%Y%m%d}.idx"
    stale.write_text(_idx(day.strftime("%Y%m%d"), "early"))
    calls = []

    def fake_get(url, timeout=60):
        calls.append(url)
        return _idx(day.strftime("%Y%m%d"), "early", "late").encode("latin-1")

    monkeypatch.setattr(il, "_get", fake_get)
    out = il.daily_form4(day, [CIK], tmp_path)
    assert [e["path"] for e in out] == ["edgar/data/123456/early.txt", "edgar/data/123456/late.txt"]
    assert len(calls) == 1
    assert "late" in stale.read_text()                       # the fresh copy replaced the stale one


def test_recent_day_falls_back_to_cache_when_fetch_fails(tmp_path, monkeypatch):
    day = pd.Timestamp.today().normalize()
    (tmp_path / f"form.{day:%Y%m%d}.idx").write_text(_idx(day.strftime("%Y%m%d"), "cached"))
    monkeypatch.setattr(il, "_get", lambda url, timeout=60: None)
    out = il.daily_form4(day, [CIK], tmp_path)
    assert [e["path"] for e in out] == ["edgar/data/123456/cached.txt"]
    assert il.daily_form4(day, [CIK], tmp_path / "empty") == []
