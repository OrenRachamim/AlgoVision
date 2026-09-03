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
