"""Per-stock briefs: the rule-based read, the markdown and the file writer on synthetic data."""

import pandas as pd

from algovision import briefs as B
from algovision.data.synthetic import random_walk


def _profile(key="buy", target=1.3, surprise=0.05, rev30=0.02, n_down=0, fcf=1e8):
    now = 1_800_000_000
    return {
        "price": {"longName": "Test Corp", "marketCap": 5e9}, "assetProfile": {"sector": "Tech", "industry": "Widgets", "longBusinessSummary": "Makes widgets."},
        "financialData": {"currentPrice": 100.0, "targetMeanPrice": 100.0 * target, "targetLowPrice": 90.0, "targetHighPrice": 150.0,
                          "recommendationKey": key, "recommendationMean": 2.0, "numberOfAnalystOpinions": 12, "revenueGrowth": 0.08,
                          "earningsGrowth": 0.1, "freeCashflow": fcf, "debtToEquity": 50.0, "grossMargins": 0.5, "operatingMargins": 0.2,
                          "profitMargins": 0.1, "returnOnEquity": 0.15, "totalCash": 1e9, "totalDebt": 5e8, "currentRatio": 1.5},
        "recommendationTrend": {"trend": [{"period": "0m", "strongBuy": 3, "buy": 5, "hold": 4, "sell": 0, "strongSell": 0},
                                          {"period": "-3m", "strongBuy": 4, "buy": 6, "hold": 2, "sell": 0, "strongSell": 0}]},
        "upgradeDowngradeHistory": {"history": [{"epochGradeDate": now, "firm": "Bank", "action": "down", "fromGrade": "Buy", "toGrade": "Hold",
                                                 "priceTargetAction": "Lowers", "currentPriceTarget": 110.0, "priorPriceTarget": 130.0}] * n_down},
        "earningsHistory": {"history": [{"quarter": now - 86400 * 40, "epsActual": 1.05, "epsEstimate": 1.0, "surprisePercent": surprise, "period": "-1q"}]},
        "earningsTrend": {"trend": [{"period": "0q", "earningsEstimate": {"avg": 1.1, "growth": 0.05}, "revenueEstimate": {"growth": 0.04},
                                     "epsTrend": {"current": 1.1, "30daysAgo": 1.1}},
                                    {"period": "0y", "earningsEstimate": {"avg": 4.4, "growth": 0.1},
                                     "epsTrend": {"current": 4.4 * (1 + rev30), "30daysAgo": 4.4, "90daysAgo": 4.5},
                                     "epsRevisions": {"upLast30days": 2, "downLast30days": 0}},
                                    {"period": "+1y", "earningsEstimate": {"avg": 5.0, "growth": 0.14}}]},
        "calendarEvents": {"earnings": {"earningsDate": [now + 86400 * 30], "isEarningsDateEstimate": False}},
        "defaultKeyStatistics": {"forwardPE": 18.0, "pegRatio": 1.2, "enterpriseToRevenue": 3.0, "enterpriseToEbitda": 12.0, "priceToBook": 2.0,
                                 "shortPercentOfFloat": 0.03, "beta": 1.1, "52WeekChange": -0.2, "SandP52WeekChange": 0.1},
        "summaryDetail": {"marketCap": 5e9, "trailingPE": 22.0, "forwardPE": 18.0, "dividendYield": 0.01},
    }


def _news(day):
    return [{"title": "Test Corp cuts guidance", "summary": "Weak demand.", "publisher": "Wire", "date": day, "link": "https://x"},
            {"title": "Analyst day recap", "summary": "", "publisher": "Wire", "date": "2020-01-01", "link": ""}]


def test_price_context_fields():
    df = random_walk(400, seed=3)
    ctx = B.price_context(df)
    assert ctx["last"] == float(df["Close"].iloc[-1]) and -1 <= ctx["drawdown"] <= 0 and ctx["off_low"] >= 0
    assert 0 <= ctx["rsi14"] <= 100 and len(ctx["biggest_drops"]) == 3 and ctx["biggest_drops"][0][1] <= ctx["biggest_drops"][1][1]


def test_verdict_moves_with_signals():
    up_ctx = {"dist_ma50": 0.05, "ma50_rising": True, "higher_low": True, "new_low_5d": False}
    down_ctx = {"dist_ma50": -0.1, "ma50_rising": False, "higher_low": False, "new_low_5d": True}
    good = _profile(key="buy", target=1.3, surprise=0.05, rev30=0.03)
    bad = _profile(key="sell", target=1.0, surprise=-0.1, rev30=-0.05, n_down=2, fcf=-1e7)
    lab_up, s_up, why_up = B.verdict(up_ctx, B.analyst_view(good), B.earnings_view(good), B.fundamentals_view(good), insider_buying=True)
    lab_dn, s_dn, why_dn = B.verdict(down_ctx, B.analyst_view(bad), B.earnings_view(bad), B.fundamentals_view(bad))
    assert lab_up == "up" and s_up >= 3 and any("insiders bought" in w for w in why_up)
    assert lab_dn == "down" and s_dn <= -2 and any("missed" in w for w in why_dn)


def test_analyst_and_earnings_views():
    an = B.analyst_view(_profile(n_down=1))
    assert an["key"] == "buy" and an["n"] == 12 and abs(an["upside"] - 0.3) < 1e-9 and an["n_down"] == 1 and an["n_target_cuts"] == 1
    ea = B.earnings_view(_profile(rev30=0.02))
    assert abs(ea["surprise"] - 0.05) < 1e-9 and abs(ea["y0_rev_30d"] - 0.02) < 1e-9 and ea["next_date"] and ea["beats_4q"] == 1


def test_markdown_and_writer(tmp_path, monkeypatch):
    df = random_walk(400, seed=5)
    day = pd.Timestamp(df.index[-10]).strftime("%Y-%m-%d")
    data = {"profile": _profile(), "news": _news(day)}
    row, md = B.build_brief("TST", df, data, ["news-day"], insider_buying=False)
    for piece in ("**Read:", "Where the stock is", "Why it fell", "What analysts say", "Last report and estimates", "Fundamentals", "Test Corp cuts guidance"):
        assert piece in md
    assert row["symbol"] == "TST" and row["consensus"] == "buy" and "why fell" in row

    class FakeProvider:
        def __init__(self, *a, **k):
            pass

        def get_many(self, symbols, progress=None):
            return {s: data for s in symbols if s != "MISSING"}

    monkeypatch.setattr("algovision.data.briefs_data.BriefsProvider", FakeProvider)
    frames = {"TST": df, "MISSING": df}
    path, rows = B.write_briefs(tmp_path, "2026-01-01", ["TST", "MISSING"], frames, {"TST": ["news-day"]}, cache_dir=tmp_path)
    text = path.read_text()
    assert (tmp_path / "briefs_latest.md").exists() and len(rows) == 1
    assert "## Summary" in text and "no data" in text and "[TST]" in text


def _drop_frame():
    df = random_walk(400, seed=7).copy()
    pos = len(df) - 30
    df.iloc[pos:, df.columns.get_loc("Close")] *= 0.85  # -15% gap that stays: the largest down day of the window
    df["Volume"] = 1_000_000.0
    df.iloc[pos, df.columns.get_loc("Volume")] = 4_000_000.0
    return df, pd.Timestamp(df.index[pos]).strftime("%Y-%m-%d")


def test_decline_reason_found_only_with_evidence():
    df, day = _drop_frame()
    ctx = B.price_context(df)
    assert ctx["biggest_drops"][0][0] == day and ctx["drop_volume"][day] > 3
    an, ea = B.analyst_view(_profile()), B.earnings_view(_profile())
    # a headline that names the company and states a cause on the drop day
    why = B.decline_reason("TST", "Test Corp", ctx, _news(day), an, ea)
    assert why["found"] and "guidance" in why["cause"] and any(day in d["day"] and d["evidence"] for d in why["days"])
    # a headline that does not name the company is not evidence
    other = [{"title": "Widgets sector cuts guidance", "summary": "", "publisher": "Wire", "date": day, "link": ""}]
    why = B.decline_reason("TST", "Test Corp", ctx, other, an, ea)
    assert not why["found"] and why["cause"] == "heavy volume, cause not found"
    # nothing near the day: not found, and the markdown says so instead of guessing
    why = B.decline_reason("TST", "Test Corp", ctx, [], an, ea)
    assert not why["found"]
    md = B.brief_markdown("TST", [], ctx, an, ea, B.fundamentals_view(_profile()), [], "flat", 0.0, [], why)
    assert "No cause found in the data" in md and "No cause found for this day" in md
    # a market-wide down day counts as evidence
    bench = df.copy()
    bench["Close"] = 100.0
    bench.iloc[df.index.get_loc(pd.Timestamp(day)):, bench.columns.get_loc("Close")] = 97.0
    why = B.decline_reason("TST", "Test Corp", ctx, [], an, ea, bench=bench)
    assert why["found"] and why["cause"] == "market-wide"


def test_decline_reason_uses_8k_filings():
    df, day = _drop_frame()
    ctx = B.price_context(df)
    prof = _profile()
    q_end = int(pd.Timestamp(day).timestamp()) - 86400 * 35
    hist = [{"quarter": q_end, "epsActual": 0.9, "epsEstimate": 1.0, "surprisePercent": -0.1}]
    prev = (pd.Timestamp(day) - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    filings = [{"date": prev, "form": "8-K", "items": ["2.02"], "what": ["results of operations (earnings release)"]},
               {"date": "2020-01-01", "form": "8-K", "items": ["5.02"], "what": ["officer or director change"]}]
    why = B.decline_reason("TST", "Test Corp", ctx, [], B.analyst_view(prof), B.earnings_view(prof), filings=filings, earn_hist=hist)
    assert why["found"] and why["cause"] == "earnings"
    top = next(d for d in why["days"] if d["day"] == day)
    assert any("8-K filed" in e and "EPS 0.90 vs 1.00" in e and "-10.0%" in e for e in top["evidence"])
