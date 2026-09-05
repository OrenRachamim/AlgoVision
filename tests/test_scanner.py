from pathlib import Path

import pandas as pd
import pytest

from algovision.data.provider import DataProvider, normalise_ohlcv
from algovision.data.synthetic import GENERATORS, random_walk
from algovision.data.universe import get_universe, load_snapshot
from algovision.scanner import Scanner


@pytest.fixture
def csv_dir(tmp_path):
    for name, gen in GENERATORS.items():
        df, _ = gen()
        sym = name.upper().replace(" ", "")[:8]
        df.to_csv(tmp_path / f"{sym}.csv")
    (tmp_path / "RW.csv").write_text(random_walk(300).to_csv())
    return tmp_path


def test_provider_reads_csv_dir(csv_dir):
    p = DataProvider(cache_dir=None, csv_dir=csv_dir)
    df = p.get("RW")
    assert list(df.columns) == ["Open", "High", "Low", "Close", "Volume"]
    assert isinstance(df.index, pd.DatetimeIndex)
    with pytest.raises(FileNotFoundError):
        p.get("NOPE")


def test_provider_offline_without_cache_raises(tmp_path):
    p = DataProvider(cache_dir=tmp_path, offline=True)
    with pytest.raises(RuntimeError):
        p.get("AAPL")


def test_normalise_handles_lowercase_and_adj():
    df = random_walk(50)
    raw = df.reset_index().rename(columns={"Date": "date", "Open": "open", "High": "high", "Low": "low",
                                           "Close": "close", "Volume": "volume"})
    out = normalise_ohlcv(raw)
    assert len(out) == 50 and out.index.is_monotonic_increasing


def test_scanner_history_and_current(csv_dir):
    provider = DataProvider(cache_dir=None, csv_dir=csv_dir)
    symbols = [p.stem for p in csv_dir.glob("*.csv")]
    sc = Scanner(provider)
    hist = sc.scan(symbols, mode="history")
    assert hist.matches and not hist.errors
    confirmed = [m for m in hist.matches if m.status == "confirmed"]
    assert confirmed
    for m in confirmed:
        assert "ret_5" in m.outcome and "bars_available" in m.outcome
        if m.outcome["bars_available"] > 0:
            assert "target_hit" in m.outcome
    frame = hist.to_frame()
    assert {"symbol", "pattern", "status", "score", "why"} <= set(frame.columns)
    cur = sc.scan(symbols, mode="current")
    for m in cur.matches:
        assert m.metrics["bars_since_end"] <= sc.cfg.recent_bars
        assert m.status in ("forming", "confirmed")


def test_scanner_skips_bad_symbol(csv_dir):
    provider = DataProvider(cache_dir=None, csv_dir=csv_dir)
    res = Scanner(provider).scan(["RW", "MISSING"], mode="all")
    assert "MISSING" in res.errors and "RW" in res.frames


def test_universe_snapshot():
    snap = load_snapshot()
    assert len(snap["sp500"]) > 480 and len(snap["nasdaq100"]) > 90
    sp = get_universe("sp500")
    assert "AAPL" in sp and len(sp) == len(set(sp))
    assert len(get_universe("all")) >= len(sp)
    with pytest.raises(ValueError):
        get_universe("ftse")


def test_plot_and_report(csv_dir, tmp_path):
    from algovision.plotting import plot_match
    from algovision.report import write_report
    provider = DataProvider(cache_dir=None, csv_dir=csv_dir)
    res = Scanner(provider).scan(["CUPANDHA"], mode="all")
    assert res.matches
    m = res.matches[0]
    out = tmp_path / "c.png"
    plot_match(res.frames["CUPANDHA"], m, out)
    assert out.exists() and out.stat().st_size > 1000
    rep = write_report(res.frames, res.matches[:2], tmp_path / "r.html")
    txt = rep.read_text()
    assert "CUPANDHA" in txt and "data:image/png;base64" in txt


def test_cli_demo(tmp_path, capsys):
    from algovision.cli import main
    assert main(["demo", "--out", str(tmp_path)]) == 0
    assert (tmp_path / "demo.html").exists()
    assert main(["patterns"]) == 0
    assert "Cup and Handle" in capsys.readouterr().out


def test_cli_analyze_csv_dir(csv_dir, tmp_path):
    from algovision.cli import main
    rc = main(["analyze", "RW", "HEADANDS", "--csv-dir", str(csv_dir), "--no-cache",
               "--csv", str(tmp_path / "out.csv"), "--json", str(tmp_path / "out.json"), "--explain"])
    assert rc == 0
    assert (tmp_path / "out.csv").exists() and (tmp_path / "out.json").exists()


def test_scanner_context_and_beaten_down_filter(csv_dir):
    from algovision.core.types import DetectorConfig
    provider = DataProvider(cache_dir=None, csv_dir=csv_dir)
    symbols = [p.stem for p in csv_dir.glob("*.csv")]
    res = Scanner(provider).scan(symbols, mode="all")
    assert res.matches
    for m in res.matches:
        ctx = m.metrics["context"]
        assert {"ret_126", "dist_ma200", "atr_pct", "beaten_down"} <= set(ctx)
        assert any(r.startswith("Context at signal") for r in m.reasons)
    frame = res.to_frame()
    assert {"ret_6m", "dist_ma200", "beaten_down"} <= set(frame.columns)
    strict = Scanner(provider, DetectorConfig(filter_max_ret_126=-0.08, filter_below_ma200=True)).scan(symbols, mode="all")
    assert len(strict.matches) <= len(res.matches)
    for m in strict.matches:
        assert m.metrics["context"]["ret_126"] < -0.08 and m.metrics["context"]["dist_ma200"] < 0
    # the filter never lets through a match that the unfiltered scan would not have produced
    keys = {(m.symbol, m.pattern, m.start_idx) for m in res.matches}
    assert all((m.symbol, m.pattern, m.start_idx) in keys for m in strict.matches)


def test_journal_logs_and_marks_to_market(tmp_path, monkeypatch):
    import algovision.journal as J
    from algovision.data.synthetic import random_walk, wedge
    frames = {"AAA": random_walk(700, seed=41), "BBB": random_walk(700, seed=42)}
    monkeypatch.setattr(J, "get_universe", lambda u: list(frames))

    class P:
        def __init__(self, *a, **k):
            pass

        def get_many(self, symbols, period, interval):
            return {s: frames[s] for s in symbols if s in frames}

    monkeypatch.setattr(J, "DataProvider", P)
    monkeypatch.setattr(J, "collect_growth", lambda *a, **k: [])
    monkeypatch.setattr(J, "collect_insiders", lambda *a, **k: [])
    p = J.run(tmp_path, today="2026-01-01")
    assert p.exists() and (tmp_path / "signals.csv").exists()
    # inject a past signal and check mark-to-market fills entry and result
    sig = pd.read_csv(tmp_path / "signals.csv", dtype=str)
    row = {"logged": "2025-01-01", "rule": "newsday", "symbol": "AAA", "signal_date": str(frames["AAA"].index[100].date()),
           "status": "open", "ref_price": "100", "entry_date": "", "entry_price": "", "hold_bars": "60", "note": "test"}
    sig = pd.concat([sig, pd.DataFrame([row])], ignore_index=True)
    sig.to_csv(tmp_path / "signals.csv", index=False)
    J.run(tmp_path, today="2026-01-02")
    m = pd.read_csv(tmp_path / "mark_to_market.csv")
    r = m[(m.symbol == "AAA") & (m.rule == "newsday")].iloc[0]
    assert r["done"] == True and r["bars_elapsed"] == 60  # noqa: E712
    assert abs(float(r["entry_price"]) - float(frames["AAA"]["Open"].iloc[101])) < 1e-3   # stored with 4 decimals
    assert "closed trades" in (tmp_path / "latest.md").read_text()


def test_fundamentals_features_and_growth_score():
    from algovision.data.fundamentals import features
    from algovision.growth import diversified_top, price_features, score
    from algovision.data.synthetic import random_walk

    def series(vals, start=2022):
        return [{"date": f"{start + i}-12-31", "value": v} for i, v in enumerate(vals)]

    raw = {"annualTotalRevenue": series([100, 130, 170, 220]), "quarterlyTotalRevenue": series([50, 55, 60, 65, 70], 2025),
           "quarterlyNetIncome": series([10, 11, 12, 13, 14], 2025), "quarterlyDilutedEPS": series([1, 1.1, 1.2, 1.3, 1.4], 2025),
           "quarterlyGrossProfit": series([30, 33, 36, 39, 42], 2025), "quarterlyOperatingIncome": series([12, 14, 15, 16, 18], 2025),
           "quarterlyFreeCashFlow": series([9, 10, 11, 12, 13], 2025), "quarterlyTotalDebt": series([20] * 5, 2025),
           "quarterlyStockholdersEquity": series([100] * 5, 2025), "quarterlyBasicAverageShares": series([10, 10, 9.9, 9.8, 9.7], 2025),
           "trailingMarketCap": series([1000.0]), "trailingPegRatio": series([1.2]), "trailingPeRatio": series([25.0]),
           "trailingForwardPeRatio": series([20.0]), "annualDilutedEPS": series([3, 3.6, 4.2, 5.0])}
    f = features(raw)
    assert abs(f["rev_cagr_3y"] - ((220 / 100) ** (1 / 3) - 1)) < 1e-9
    assert abs(f["rev_yoy_q"] - 0.4) < 1e-9 and abs(f["share_change_1y"] - (-0.03)) < 1e-9
    assert f["op_margin"] > 0.2 and f["fcf_margin"] > 0.1 and f["roe"] > 0.4
    frames = {f"S{i}": random_walk(400, seed=500 + i, drift=0.0005 * (i % 3)) for i in range(6)}
    fund = pd.DataFrame([{**features(raw), "symbol": s} for s in frames]).set_index("symbol")
    fund.loc["S0", "rev_yoy_q"] = -0.1     # fails the growth filter
    sc = score(fund, price_features(frames), {s: ("Tech" if i < 4 else "Health") for i, s in enumerate(frames)})
    assert "S0" not in sc.index and sc["score"].between(0, 1).all() and (sc["why"].str.len() > 20).all()
    d = diversified_top(sc, n=4, max_per_sector=2)
    assert len(d) <= 4 and d["sector"].value_counts().max() <= 2


def test_insider_cluster_and_single_events():
    from algovision.data.insiders import cluster_events, single_events
    rows = []
    for owner, day in (("A", 1), ("B", 10), ("C", 40), ("D", 100), ("E", 105)):
        rows.append({"symbol": "XYZ", "owner_cik": owner, "filing_date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=day),
                     "value": 200_000.0, "code": "P", "is_ceo_cfo": owner == "A"})
    rows.append({"symbol": "XYZ", "owner_cik": "F", "filing_date": pd.Timestamp("2024-02-01"), "value": 50_000.0, "code": "S", "is_ceo_cfo": False})
    tx = pd.DataFrame(rows)
    ev = cluster_events(tx, window_days=30, min_insiders=2)
    # A+B complete a cluster on day 10; C is alone in its window; D+E complete another on day 105
    assert list(ev["date"]) == [pd.Timestamp("2024-01-11"), pd.Timestamp("2024-04-15")]
    assert ev.iloc[0]["n_insiders"] == 2 and bool(ev.iloc[0]["ceo_cfo"]) is True
    sg = single_events(tx, min_value=100_000)
    assert len(sg) == 3      # A, C, D (B is within 30 days of A, E within 30 days of D)


def test_daily_report_helpers_and_parallel_fetch_signature():
    import inspect
    from algovision.daily_report import _pct, build_report
    from algovision.data.insiders_live import recent_transactions, parse_form4
    assert _pct(0.1234) == "+12%" and _pct(-0.05, 1) == "-5.0%" and _pct(float("nan")) == ""
    assert "workers" in inspect.signature(recent_transactions).parameters
    assert "insider_days" in inspect.signature(build_report).parameters
    xml = """<ownershipDocument><issuer><issuerTradingSymbol>xyz</issuerTradingSymbol></issuer>
    <reportingOwner><reportingOwnerId><rptOwnerCik>1</rptOwnerCik><rptOwnerName>Doe Jane</rptOwnerName></reportingOwnerId>
    <reportingOwnerRelationship><isDirector>1</isDirector><isOfficer>1</isOfficer><officerTitle>Chief Executive Officer</officerTitle></reportingOwnerRelationship></reportingOwner>
    <nonDerivativeTable><nonDerivativeTransaction><transactionDate><value>2026-09-01</value></transactionDate>
    <transactionCoding><transactionCode>P</transactionCode></transactionCoding>
    <transactionAmounts><transactionShares><value>1000</value></transactionShares><transactionPricePerShare><value>50.5</value></transactionPricePerShare></transactionAmounts>
    </nonDerivativeTransaction><nonDerivativeTransaction><transactionCoding><transactionCode>M</transactionCode></transactionCoding></nonDerivativeTransaction>
    </nonDerivativeTable></ownershipDocument>"""
    rows = parse_form4("junk before " + xml + " junk after")
    assert len(rows) == 1 and rows[0]["symbol"] == "XYZ" and rows[0]["code"] == "P" and rows[0]["value"] == 50500.0
    assert rows[0]["is_ceo_cfo"] and rows[0]["is_officer"] and rows[0]["is_director"]


def test_notify_chunks_and_skips_without_config(tmp_path, monkeypatch):
    from algovision.notify import _chunks, deliver, markdown_to_html
    text = "\n".join(f"line {i} " + "x" * 100 for i in range(100))
    parts = _chunks(text, limit=1000)
    assert all(len(p) <= 1000 for p in parts) and "".join(parts) == text
    for v in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID", "SMTP_USER", "SMTP_PASSWORD"):
        monkeypatch.delenv(v, raising=False)
    f = tmp_path / "r.md"
    f.write_text("# Report\n\n| a | b |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
    st = deliver(f)
    assert st["telegram"].startswith("skipped") and st["email"].startswith("skipped")
    assert "<table" in markdown_to_html(f.read_text())


def test_tradingview_links_and_relay(monkeypatch, tmp_path):
    from algovision.links import tradingview_url, tv
    from algovision import notify

    assert tradingview_url("brk.b") == "https://www.tradingview.com/chart/?symbol=BRK.B"
    assert tv("VST") == "[VST](https://www.tradingview.com/chart/?symbol=VST)"

    calls = []

    class _Resp:
        ok = True
        status_code = 200
        headers = {"content-type": "application/json"}
        text = ""

        def json(self):
            return {"ok": True, "sent": 2}

    def fake_post(url, json=None, timeout=None):
        calls.append((url, json))
        return _Resp()

    import requests
    monkeypatch.setattr(requests, "post", fake_post)
    for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("TELEGRAM_RELAY_URL", "https://relay.example/")
    monkeypatch.setenv("TELEGRAM_RELAY_SECRET", "s3cret")
    assert notify.send_telegram("hello") == 2
    assert calls[0][0] == "https://relay.example/" and calls[0][1] == {"text": "hello", "secret": "s3cret"}
    f = tmp_path / "r.md"
    f.write_text("# t\nbody", encoding="utf-8")
    notify.send_telegram_document(f, caption="cap")
    assert calls[1][1]["filename"] == "r.md" and calls[1][1]["content"] == "# t\nbody" and calls[1][1]["caption"] == "cap"
