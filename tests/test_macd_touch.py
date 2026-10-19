import numpy as np
import pandas as pd

from algovision import macd_touch as M


def _close(seed=1, n=400, drift=0.0):
    r = np.random.default_rng(seed)
    c = 100 * np.cumprod(1 + r.normal(drift, 0.012, n))
    return pd.Series(c, index=pd.bdate_range("2024-01-01", periods=n))


def _hist_after(close, nxt):
    """The MACD histogram once ``nxt`` is appended as tomorrow's close."""
    c = pd.concat([close, pd.Series([nxt], index=[close.index[-1] + pd.Timedelta(days=1)])])
    ef = c.ewm(span=M.FAST, adjust=False).mean()
    es = c.ewm(span=M.SLOW, adjust=False).mean()
    macd = ef - es
    sig = macd.ewm(span=M.SIGNAL, adjust=False).mean()
    return float(macd.iloc[-1] - sig.iloc[-1]), float(sig.iloc[-1])


def test_touch_and_cross_prices_are_exact():
    # a decline into the last bar so that MACD sits well below its signal line
    close = _close(3)
    close.iloc[-30:] = close.iloc[-30] * np.cumprod(1 - 0.01 * np.ones(30))
    fc = M.macd_touch_forecast(close)
    assert fc["status"] == "apart" and fc["gap_pct_of_signal"] > 5
    h_cross, _ = _hist_after(close, fc["cross_price"])
    assert abs(h_cross) < 1e-4                                   # MACD == signal at the cross price (prices are rounded to 4 dp)
    h_touch, _ = _hist_after(close, fc["touch_price"])
    assert abs(h_touch + M.TOLERANCE * abs(fc["signal"])) < 1e-4   # signal - MACD == 5% of today's |signal| at the touch price (the spec's eps)
    assert fc["touch_price"] < fc["cross_price"]
    assert 0 <= fc["touch_prob"] <= 1 and fc["signal_70"] == (fc["touch_prob"] >= 0.70)
    assert abs(fc["required_change_pct"] - (fc["touch_price"] / fc["close"] - 1) * 100) < 0.01   # both rounded for display


def test_statuses():
    up = _close(5)
    up.iloc[-30:] = up.iloc[-30] * np.cumprod(1 + 0.01 * np.ones(30))
    assert M.macd_touch_forecast(up)["status"] == "above_signal"
    assert M.macd_touch_forecast(_close(7).iloc[:100])["status"] == "insufficient_data"
    flat = pd.Series(100.0, index=pd.bdate_range("2024-01-01", periods=300))
    fc = M.macd_touch_forecast(flat)             # MACD == signal == 0: hist >= 0, nothing to forecast
    assert fc["status"] == "above_signal"


def test_probability_is_monotone_in_the_required_move():
    assert np.interp(-2.0, M._Z, M._P) > np.interp(0.0, M._Z, M._P) > np.interp(2.0, M._Z, M._P)
    assert abs(np.interp(0.0, M._Z, M._P) - 0.505) < 1e-9


def test_cells_and_fallback(tmp_path):
    fc = {"status": "apart", "touch_price": 79.9557, "required_change_pct": -2.64, "gap_pct_of_signal": 5.93, "touch_prob": 0.926, "signal_70": True,
          "source": "raw"}
    en, he = M.macd_cell(fc, "en"), M.macd_cell(fc, "he")
    assert en == "**93%** · touch >= 79.96 (-2.6%) · gap 5.9%"
    assert he.startswith("**93%** · נגיעה מ-79.96 (-2.6%)")
    assert M.macd_cell({**fc, "touch_prob": 0.4, "signal_70": False, "source": "adjusted"}) == "~40% · touch >= 79.96 (-2.6%) · gap 5.9%"
    assert M.macd_cell({"status": "touching", "source": "raw"}) == "touching" and M.macd_cell({"status": "above_signal", "source": "raw"}, "he") == "מעל הסיגנל"
    assert M.macd_cell({"status": "insufficient_data"}) == "" and M.macd_cell(None) == ""
    # offline with no raw cache: the forecast falls back to the adjusted frame and says so
    df = pd.DataFrame({"Close": _close(9)})
    mt = M.MacdTouch({"AAA": df}, tmp_path, offline=True)
    assert mt.get("AAA")["source"] == "adjusted" and mt.get("ZZZ")["status"] == "insufficient_data"
    # a raw cache that is fresh enough is used without the network
    raw = _close(11)
    (tmp_path / "macd_raw").mkdir()
    raw.rename("Close").to_frame().to_csv(tmp_path / "macd_raw" / "BBB.csv")
    mt = M.MacdTouch({"BBB": df}, tmp_path, offline=True)
    assert mt.get("BBB")["source"] == "raw"


def test_summary_tables_carry_the_cell():
    from algovision.briefs import summary_table
    from algovision.daily_he import summary_table_he

    fc = {"status": "apart", "touch_price": 50.0, "required_change_pct": -1.0, "gap_pct_of_signal": 7.0, "touch_prob": 0.8, "signal_70": True, "source": "raw"}
    base = {"tables": "early rally", "read": "undecided", "score": 1.0, "why fell": "", "concerns": "", "sentiment": "", "vs peers 20d": "", "last": 51.0,
            "from 52w high": -0.2, "vs MA50": 0.01, "vs MA200": -0.1, "consensus": "buy", "analysts": 5, "target upside": 0.2, "up/down 90d": "0/0",
            "EPS est 30d": 0.0, "last surprise": 0.0, "next report": "", "flags": {}}
    rows = [{"symbol": "AAA", "_macd": fc, **base}, {"symbol": "BBB", "_macd": {"status": "touching", "source": "raw"}, **base}]
    en = summary_table(rows)
    assert "MACD pre-touch" in en and "**80%** · touch >= 50.00 (-1.0%) · gap 7.0%" in en and "touching" in en
    he = "\n".join(summary_table_he(rows))
    assert "MACD נגיעה צפויה" in he and "נגיעה מ-50.00" in he and "נוגעים" in he
    assert "MACD" not in summary_table([{"symbol": "AAA", **base}])      # rows without the forecast: no column
