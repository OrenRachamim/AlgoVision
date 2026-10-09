import numpy as np
import pandas as pd

from algovision import daily_he as D
from algovision import whatsnew as W


def _frame(n=320, seed=3):
    rng = np.random.default_rng(seed)
    close = 100 * np.cumprod(1 + rng.normal(0, 0.01, n))
    idx = pd.bdate_range("2025-06-02", periods=n)
    o = np.r_[close[0], close[:-1]]
    return pd.DataFrame({"Open": o, "High": np.maximum(o, close) * 1.004, "Low": np.minimum(o, close) * 0.996, "Close": close,
                         "Volume": np.full(n, 1e6)}, index=idx)


def _row(symbol, tables, read="undecided", score=1.0):
    ctx = {"last": 50.0, "drawdown": -0.2, "high_52w": 62.5, "high_date": "2026-01-05", "off_low": 0.05, "low_52w": 47.6, "low_date": "2026-09-01",
           "ret_1m": -0.02, "ret_3m": -0.1, "ret_6m": -0.15, "ret_1y": -0.2, "dist_ma50": -0.03, "dist_ma200": -0.12, "rsi14": 45.0}
    why = {"found": True, "cause": "earnings, guidance", "high_date": "2026-01-05", "high_52w": 62.5, "drawdown": -0.2, "n_earnings_days": 1,
           "earnings_days_ret": -0.08, "oldest_news": "2026-09-01",
           "days": [{"day": "2026-08-20", "kind": "earnings", "ret": -0.08, "volume": "4.0x normal volume", "volume_ratio": 4.0, "spy": -0.002,
                     "evidence": ["x"], "tags": ["earnings"], "before_feed": False,
                     "filings": [{"date": "2026-08-20", "codes": ["2.02"], "what": ["results"], "eps": None}],
                     "headlines": [{"date": "2026-08-20", "title": "Test Corp cuts guidance", "publisher": "Wire", "summary": "", "causes": ["guidance"]}],
                     "cuts": []}]}
    sent = {"label": "mixed", "signals": [("targets_cut", -1, {"cuts": 2, "raises": 1}), ("revisions_up", 1, {"up": 2, "down": 1})],
            "concerns": {"themes": [{"en": "guidance / outlook cut", "he": "הורדת תחזית", "count": 3,
                                     "examples": [{"date": "2026-08-20", "title": "Test Corp cuts guidance", "publisher": "Wire"}]}],
                         "n": 10, "tone": {"neg": 3, "pos": 2, "neu": 5, "neg_30d": 1, "pos_30d": 1}},
            "positioning": {"short_pct": 0.03, "short_change": 0.1, "short_ratio": 2.0, "short_date": "2026-09-15", "institutions": 0.8, "insiders": 0.01, "twits": {}}}
    an = {"key": "buy", "n": 10, "mean": 2.0, "target": 60.0, "upside": 0.2, "counts_now": {"strongBuy": 2, "buy": 5, "hold": 3, "sell": 0, "strongSell": 0},
          "actions": [], "actions_1y": [], "n_up": 1, "n_down": 0, "n_target_cuts": 0, "n_target_raises": 1}
    ea = {"last_quarter": "2026-06-30", "eps_actual": 1.0, "eps_est": 0.9, "surprise": 0.11, "beats_4q": 3, "n_4q": 4, "next_date": "2026-11-01",
          "q0_eps_est": 1.1, "q0_growth": 0.1, "q0_rev_growth": 0.05, "y0_rev_30d": 0.01, "y0_rev_90d": 0.02, "y0_up_down_30d": (2, 1), "y0_growth": 0.1,
          "y1_growth": 0.12, "revenue_growth": 0.05, "earnings_growth": 0.1}
    fu = {"name": f"{symbol} Corp", "sector": "Industrials", "industry": "Machinery", "summary": "Makes things.", "market_cap": 5e9, "pe": 20.0,
          "forward_pe": 15.0, "peg": 1.2, "ev_rev": 2.0, "ev_ebitda": 10.0, "pb": 3.0, "gross_margin": 0.4, "op_margin": 0.15, "net_margin": 0.1,
          "fcf": 3e8, "fcf_yield": 0.06, "debt_to_equity": 0.5, "cash": 1e9, "debt": 2e9, "current_ratio": 1.5, "roe": 0.2, "dividend_yield": 0.02,
          "short_pct": 0.03, "beta": 1.1, "chg_52w": -0.2, "spx_52w": 0.15}
    return {"symbol": symbol, "tables": ", ".join(tables), "read": read, "score": score, "why fell": "earnings, guidance", "concerns": "guidance / outlook cut",
            "sentiment": "mixed", "AI": "buy 0.70", "vs peers 20d": "+1.0% (z +0.3)", "last": 50.0, "from 52w high": -0.2, "vs MA50": -0.03, "vs MA200": -0.12,
            "consensus": "buy", "analysts": 10, "target upside": 0.2, "up/down 90d": "1/0", "EPS est 30d": 0.01, "last surprise": 0.11, "next report": "2026-11-01",
            "_story": None, "_decision": None,
            "_data": {"ctx": ctx, "an": an, "ea": ea, "fu": fu, "why": why, "sent": sent, "news": [{"date": "2026-10-01", "title": "Test Corp news", "publisher": "Wire", "summary": "A summary."}],
                      "label": "flat", "score": score, "fired": [("below_ma50", -1.0, {})], "name": f"{symbol} Corp", "tables": list(tables), "peers": None}}


def test_build_daily_he_carries_every_part(tmp_path):
    frames = {"AAA": _frame(), "BBB": _frame(seed=4)}
    rows = [_row("AAA", ["news-day"], "signs of a bottom", 4.0), _row("BBB", ["early rally", "insider buys (other)"])]
    sig = pd.DataFrame({"symbol": ["BBB"], "beaten_down": [False], "last_filing": ["2026-09-30"], "cluster": [False], "n_insiders_30d": [1], "n_buys": [1],
                        "total_value": [2.5e5], "avg_price": [48.0], "last_close": [50.0], "ret_6m": [-0.15], "dist_ma200": [-0.12], "ceo_cfo": [True], "buyers": ["Doe J"]})
    nd = pd.DataFrame({"symbol": ["AAA"], "news_date": ["2026-10-03"], "bars_ago": [1], "gap": [-0.06], "volume_ratio": [3.5], "ret_6m": [-0.15], "dist_ma200": [-0.12],
                       "last_close": [50.0], "since_news": [0.01], "bars_left": [59]})
    rally = pd.DataFrame({"symbol": ["BBB"], "rules": ["rsi_turn, thrust"], "n_rules": [2], "signal_date": ["2026-10-03"], "bars_ago": [0], "day_ret": [0.03],
                          "ret_10": [0.09], "ret_6m": [-0.15], "from_52w_high": [-0.2], "dist_ma50": [-0.01], "dist_ma200": [-0.1], "volume_ratio": [1.4], "last": [50.0]})
    decisions = {"AAA": {"symbol": "AAA", "action": "buy", "p_buy": 0.7, "p_watch": 0.2, "p_skip": 0.1, "cause_type": "transitory", "evidence": "supports",
                         "corporate_action": 0.03, "event_ahead": 0.8, "severity": 1.0, "tables": "news-day", "read": "signs of a bottom", "score": 4.0}}
    mtm = pd.DataFrame({"logged": ["2026-10-03"], "rule": ["newsday"], "symbol": ["AAA"], "signal_date": ["2026-10-03"], "status": ["open"], "ref_price": [50.0],
                        "entry_date": ["2026-10-06"], "entry_price": [50.5], "hold_bars": [60], "note": ["gap -6%"], "bars_elapsed": [1], "last_price": [51.0],
                        "ret": [0.0099], "done": [False], "spy_ret": [0.002]})
    mtm.to_csv(tmp_path / "mark_to_market.csv", index=False)
    rows[0]["flags"] = []
    rows[1]["flags"] = ["Z", "S"]
    regime = {"n_beaten_20_ago": 3, "basket_20": -0.05, "basket_10": -0.02, "spy_20": 0.01, "basket_vs_spy_20": -0.06, "share_above_ma50": 0.4,
              "share_above_ma50_20_ago": 0.5, "share_beaten": 0.2, "share_beaten_20_ago": 0.15, "spy_vs_ma50": 0.01, "spy_vs_ma200": 0.05, "warning": True}
    days = {"News-day": {"AAA": 2}, "Early rally, beaten-down": {}}
    path = D.build_daily_he(tmp_path, "2026-10-06", "2026-10-06", 2, 2, 45, sig, pd.DataFrame({"x": range(7)}), nd, {}, rally, rows, frames, {}, decisions, ["AAA"],
                            {"AAA": "Industrials", "BBB": "Utilities"}, None, "# AlgoVision 2026-10-06: מה חדש\n- בדיקה\n", regime=regime, days=days,
                            lookback=None, skips=["BBB"])
    text = path.read_text(encoding="utf-8")
    assert (tmp_path / "daily_latest.md").exists()
    for piece in ("**משטר השוק.**", "נגד הרוח", "## 0. מה חדש", "## 1. קניות אינסיידרים", "### מניות אחרות עם רכישות אינסיידרים", "שורה אחת בלבד",
                  "### כלל יום החדשות", "ימים ברשימה", "### טריז יורד", "### ראלי מוקדם", "### רשימת מעקב", "## 3. רשימת הבדיקות", "### רשימת הבדיקות",
                  "### טבלת התקציר", "דגלים", "**Z S**", "### החלטות המודל (Jev), מבחן קדימה", "נרשמו כ-jev_skip", "## המניות שהמודל סימן",
                  "## 4. פירוט לכל מניה", "## AAA - AAA Corp", "## BBB - BBB Corp", "**בקצרה:**", "**איפה המניה.**",
                  "### למה המניה ירדה", "חדשות אחרונות (הכותרות והתקצירים", "### חששות המשקיעים וסנטימנט", "### החלטת AI (Jev)", "### מה אומרים האנליסטים",
                  "### הדוח האחרון והתחזיות", "### נתוני יסוד", "### קריאה מבוססת כללים", "## 5. מה עבד עד עכשיו", "## 6. מבחן קדימה (היומן)",
                  "ציפייה מול מציאות", "### פוזיציות פתוחות", "[פירוט](#s-aaa)", "RSI חוזר מעל 50", "נרשמו היום ביומן כ-jev_pick"):
        assert piece in text, piece
    import re
    assert re.search(r"\|\s*3\s*\|", text.split("### כלל יום החדשות")[1].split("### טריז")[0])     # AAA listed on 2 earlier days + today
    assert "Test Corp cuts guidance" in text and "A summary." in text          # the evidence and the news summaries travel with the file
    assert text.index("## AAA - AAA Corp") < text.index("## BBB - BBB Corp")    # signs of a bottom first, like the summary table


def test_hebrew_whatsnew_note(tmp_path):
    report = ("# AlgoVision daily report - 2026-10-06\n\n### News-day rule\n\n| x |\n| [AAA](https://www.tradingview.com/chart/?symbol=AAA) |\n\n"
              "### Early rally in beaten-down stocks\n\n| [BBB](https://www.tradingview.com/chart/?symbol=BBB) |\n\n## 3. x\n")
    (tmp_path / "latest.md").write_text("# j\n\n## New signals today (1)\n\n| rule | symbol | signal_date | ref_price | hold_bars | note |\n|:--|:--|:--|--:|--:|:--|\n"
                                        "| newsday | [AAA](https://www.tradingview.com/chart/?symbol=AAA) | 2026-10-06 | 50 | 60 | gap -6.0%, vol 3.5x |\n\n## Running results\n", encoding="utf-8")
    W.write_whatsnew(tmp_path, "2026-10-06", report, "https://b", "https://w", "https://r", "https://d")
    he = (tmp_path / "new_he_latest.md").read_text(encoding="utf-8")
    en = (tmp_path / "new_latest.md").read_text(encoding="utf-8")
    assert he.startswith("# AlgoVision 2026-10-06: מה חדש") and "יום חדשות" in he and "ראלי מוקדם, מניות מוכות" in he and "https://d" in he
    assert "- יום חדשות:" in he and "פער -6.0%, מחזור פי 3.5x" in he
    assert en.startswith("# AlgoVision 2026-10-06: what is new") and "Everything in one Hebrew file" in en
