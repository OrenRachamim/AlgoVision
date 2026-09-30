"""The one-rule Hebrew falling-wedge file: geometry, translations and the writer on a synthetic wedge."""

import pandas as pd

from algovision import wedge_report as W
from algovision.data.synthetic import wedge
from algovision.patterns import detect_all
from tests.test_briefs import _profile


def _match():
    df, meta = wedge("falling", with_breakout=True)
    hits = [m for m in detect_all(df, symbol="SYN") if m.pattern == "Falling Wedge"]
    m = max(hits, key=lambda m: m.score)
    m.metrics["context"] = {"ret_126": -0.2, "dist_ma200": -0.15, "atr_pct": 0.03, "ma200_bars": 200, "beaten_down": True}
    return df, m


def test_translations():
    assert W._he_cause("heavy volume, cause not found") == "נפח כבד, סיבה לא נמצאה"
    assert W._he_cause("earnings, rating cut") == "דוח רבעוני, הורדת דירוג"
    assert W._he_cause("") == "לא נמצא" and W._he_consensus("strong_buy") == "קנייה חזקה" and W._he_sector("Health Care") == "בריאות"
    assert W._anchor("BRK.B") == "wedge-brk-b"


def test_geometry_and_section():
    df, m = _match()
    geo = W.wedge_geometry(m, df)
    assert geo["width"] > 10 and geo["h0"] > geo["h1"] > 0 and 0 < geo["h0_pct"] < 1
    assert len(geo["highs"]) >= 2 and len(geo["lows"]) >= 2 and geo["breakout_volume"] is not None
    from algovision.briefs import price_context
    md = "\n".join(W.wedge_section_he(m, df, geo, price_context(df), spy_below_ma200=False))
    for piece in ("הניתוח הטכני", "מבנה", "פריצה", "רמות", "מניה מוכה: כן", "SPY מעל"):
        assert piece in md


def test_writer(tmp_path):
    df, m = _match()
    day = pd.Timestamp(df.index[-10]).strftime("%Y-%m-%d")
    data = {"SYN": {"profile": _profile(), "news": [{"title": "Test Corp cuts guidance", "summary": "Weak demand.", "publisher": "Wire",
                                                      "date": day, "link": ""}], "filings": []}}
    path = W.build_wedge_report(tmp_path, "2026-01-01", {"SYN": df}, {"SYN": m}, {"SYN": "Industrials"}, briefs_data=data)
    text = path.read_text(encoding="utf-8")
    assert (tmp_path / "wedge_latest.md").exists()
    assert "טבלה מסכמת" in text and "[פירוט](#wedge-syn)" in text and '<a id="wedge-syn"' in text
    assert "[SYN](https://www.tradingview.com/chart/?symbol=SYN)" in text and "[חזרה לטבלה](#summary)" in text
    assert "מאושר" in text and "למה המניה ירדה" in text and "מה אומרים האנליסטים" in text and "קריאה מבוססת כללים" in text
    assert "קונצנזוס אנליסטים קנייה" in text          # the signal text is rendered in Hebrew, including the consensus key
    assert "Test Corp cuts guidance" in text        # headlines stay as published
