import numpy as np
import pandas as pd

from algovision import story as S


def _frame(close, start="2021-01-04"):
    n = len(close)
    idx = pd.bdate_range(start, periods=n)
    o = np.r_[close[0], close[:-1]]
    v = np.full(n, 1_000_000.0)
    return pd.DataFrame({"Open": o, "High": np.maximum(o, close) * 1.004, "Low": np.minimum(o, close) * 0.996, "Close": close, "Volume": v}, index=idx)


def test_zigzag_finds_the_swings_and_drops_the_trailing_stub():
    c = np.r_[np.linspace(100, 150, 100), np.linspace(150, 90, 80), np.linspace(90, 130, 60), np.linspace(130, 129, 5)]
    legs = S.legs_for(c, 0.15)
    assert len(legs) == 3 and legs[0] == (0, 100) and legs[1][1] == 180 and legs[2][1] == len(c) - 1  # the -1% stub joins the last leg
    assert S.legs_for(np.linspace(100, 101, 50), 0.10) == [(0, 49)]                                    # a flat stretch is one leg
    many = np.r_[[100 + 20 * (k % 2) for k in range(40)]]                                              # 39 swings of 20%: threshold raised
    assert len(S.legs_for(many.astype(float), 0.10)) <= S.MAX_LEGS


def test_q4_is_derived_and_quarter_before_matches_the_filing(monkeypatch, tmp_path):
    facts = {"quarters": [{"frame": "CY2023Q1", "end": "2023-03-31", "revenue": 10.0, "eps": 1.0, "net_income": None},
                          {"frame": "CY2023Q2", "end": "2023-06-30", "revenue": 11.0, "eps": 1.1, "net_income": None},
                          {"frame": "CY2023Q3", "end": "2023-09-30", "revenue": 12.0, "eps": 1.2, "net_income": None},
                          {"frame": "CY2024Q3", "end": "2024-09-30", "revenue": 15.0, "eps": 1.5, "net_income": None}],
             "years": [{"frame": "CY2023", "end": "2023-12-31", "revenue": 46.0, "eps": 4.5, "net_income": None}]}
    # the derivation lives in edgar_facts; replay it on the parsed rows through the public helper used there
    q = S.quarter_before({"quarters": facts["quarters"]}, "2024-11-05")
    assert q["frame"] == "CY2024Q3" and q["revenue_yoy"] == 15.0 / 12.0 - 1 and abs(q["eps_yoy"] - 0.25) < 1e-9
    assert S.quarter_before(facts, "2025-06-01") is None                                               # nothing within 100 days
    assert S._yoy(facts["years"], "CY2023", "revenue") is None                                         # no prior year on file


def test_headline_pick_needs_a_distinctive_company_token_and_a_cause():
    items = [{"date": "2025-04-09", "title": "Revenue of the leading retail companies worldwide", "publisher": "Statista"},
             {"date": "2025-04-09", "title": "TJX shares jump as tariff pause lifts retailers", "publisher": "Wire"},
             {"date": "2025-04-10", "title": "TJX stock falls 1% as guidance rises", "publisher": "AdHoc"}]
    h = S._pick_headline("TJX", "The TJX Companies, Inc.", items, "2025-04-09", up=True)
    assert h["title"].startswith("TJX shares jump")
    assert S._pick_headline("TJX", "The TJX Companies, Inc.", items[:1], "2025-04-09", up=True) is None   # "companies" alone is not the company


def test_build_story_and_render(monkeypatch, tmp_path):
    c = np.r_[np.linspace(100, 160, 700), np.linspace(160, 80, 500), np.linspace(80, 120, 150)]
    df = _frame(c)
    df.iloc[705, df.columns.get_loc("Volume")] = 5_000_000.0
    df.iloc[705:, df.columns.get_loc("Close")] *= 0.93                                                   # a -7% gap that stays, on heavy volume
    day = pd.Timestamp(df.index[705]).strftime("%Y-%m-%d")
    spy = _frame(np.linspace(300, 420, len(c)))
    monkeypatch.setattr(S, "long_frame", lambda symbol, d, cache_dir=None: d)
    monkeypatch.setattr(S, "edgar_facts", lambda *a, **k: {"quarters": [{"frame": "CY2023Q2", "end": "2023-06-30", "revenue": 9.0, "eps": 0.9, "net_income": None},
                                                                          {"frame": "CY2024Q2", "end": "2024-06-30", "revenue": 10.0, "eps": 1.0, "net_income": None}],
                                                            "years": [{"frame": "CY2022", "end": "2022-12-31", "revenue": 30.0, "eps": 3.0, "net_income": None},
                                                                      {"frame": "CY2024", "end": "2024-12-31", "revenue": 40.0, "eps": 4.0, "net_income": None}]})
    data = {"profile": {"price": {"longName": "Test Corp"}, "earningsHistory": {"history": []}},
            "filings": [{"date": "2024-08-01", "form": "8-K", "items": ["2.02"], "what": ["results"]},
                        {"date": "2023-05-10", "form": "8-K", "items": ["1.01"], "what": ["material agreement"]}]}
    calls = []

    def around(d):
        calls.append(d)
        return [{"date": d, "title": "Test Corp shares plunge after guidance cut", "publisher": "Wire"}]

    st = S.build_story("TST", df, data, spy, tmp_path, offline=True, headlines_around=around)
    keys = [ch["key"] for ch in st["chapters"]]
    assert keys == ["5y", "2y", "1y", "6m", "1m"] and all(not ch.get("missing") for ch in st["chapters"])
    assert st["arc"]["rev_growth"] == 40.0 / 30.0 - 1 and st["high"]["price"] >= st["low"]["price"]
    kinds = {ev["kind"] for ch in st["chapters"] for leg in ch["legs"] for ev in leg["events"]}
    assert {"earnings", "corporate", "bigday"} <= kinds
    big = [ev for ch in st["chapters"] for leg in ch["legs"] for ev in leg["events"] if ev["kind"] == "bigday" and ev["date"] == day]
    assert big and big[0]["headline"]["title"].startswith("Test Corp shares plunge") and day in calls
    earn = [ev for ch in st["chapters"] for leg in ch["legs"] for ev in leg["events"] if ev["kind"] == "earnings"][0]
    assert earn["frame"] == "CY2024Q2" and abs(earn["revenue_yoy"] - (10 / 9 - 1)) < 1e-9
    en = "\n".join(S.story_markdown(st, "en"))
    he = "\n".join(S.story_markdown(st, "he"))
    assert "Five years back" in en and "earnings release" in en and "material agreement" in en and "Annual arc" in en and "plunge after guidance cut" in en
    assert "חמש שנים אחורה" in he and "דוח רבעוני" in he and "הסכם מהותי" in he and "הקשת השנתית" in he
    assert "Fell +" not in en and "+0%" not in en
    # a short history: the old chapters are reported as missing, nothing crashes
    short = S.build_story("TST", df.iloc[-300:], data, spy, tmp_path, offline=True, headlines_around=None)
    assert short["chapters"][0]["missing"] and not short["chapters"][-1].get("missing")
    assert "No price data before" in "\n".join(S.story_markdown(short, "en"))
