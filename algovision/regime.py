"""Market regime for the beaten-down rules, and the beaten-down basket as a benchmark.

Every rule in the report fires only in *beaten-down* stocks (below the 200-day MA, six-month return < -8%). In the first
five weeks of the forward test (2026-09-05 to 2026-10-08) the equal-weight basket of all such stocks lost about 4% over
20 bars while the index gained, and every table listed roughly average beaten-down stocks: the "beaten-down factor" was
the dominant driver of the results, not the filters. This module makes that visible:

* :func:`regime_stats` describes the regime at the last bar: the basket's 10- and 20-bar return (membership fixed at the
  start of the window, so nothing is known in advance), the share of the universe above its 50-day MA now and 20 bars
  ago, the share beaten down, SPY against its 50- and 200-day MAs, and a warning flag when the basket lost more than
  ``WARN_20`` over 20 bars ("the rules are against the wind");
* :func:`basket_return` gives the basket's return over any entry/exit window, the right benchmark for a rule that only
  trades beaten-down stocks (the journal and the look-back use it next to SPY).

Descriptive only: no claim that the regime predicts anything until docs/research_filters.md says so.
"""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

BEATEN_RET_126 = -0.08
WARN_20 = -0.03          # basket 20-bar return below this -> warning line


def build_panels(frames: Dict[str, pd.DataFrame], min_len: int = 210) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """(open, close) panels, one column per symbol, on the union of the dates (forward-filled)."""
    close = pd.DataFrame({s: df["Close"].astype(float) for s, df in frames.items() if len(df) >= min_len})
    open_ = pd.DataFrame({s: df["Open"].astype(float) for s, df in frames.items() if len(df) >= min_len})
    close = close.sort_index().ffill()
    open_ = open_.reindex(close.index).ffill()
    return open_, close


def beaten_mask(close: pd.DataFrame, pos: int) -> pd.Series:
    """Which symbols are beaten down at bar ``pos`` (close below the 200-day MA and 6-month return < -8%)."""
    if pos < 200:
        return pd.Series(False, index=close.columns)
    window = close.iloc[pos - 199: pos + 1]
    ma200 = window.mean()
    c = close.iloc[pos]
    r126 = c / close.iloc[pos - 126] - 1.0
    return (c < ma200) & (r126 < BEATEN_RET_126) & c.notna() & ma200.notna()


def basket_return(open_: pd.DataFrame, close: pd.DataFrame, members: Iterable[str], entry_pos: int, exit_pos: int) -> float:
    """Equal-weight return of ``members`` from the open at ``entry_pos`` to the close at ``exit_pos`` (NaN when empty)."""
    cols = [m for m in members if m in close.columns]
    if not cols or entry_pos < 0 or exit_pos >= len(close) or exit_pos < entry_pos:
        return float("nan")
    r = close[cols].iloc[exit_pos] / open_[cols].iloc[entry_pos] - 1.0
    r = r.replace([np.inf, -np.inf], np.nan).dropna()
    return float(r.mean()) if len(r) else float("nan")


def regime_stats(frames: Dict[str, pd.DataFrame], bench: Optional[pd.DataFrame]) -> Dict:
    open_, close = build_panels({s: df for s, df in frames.items() if s != "SPY"})
    n = len(close)
    last = n - 1
    out: Dict = {"date": str(pd.Timestamp(close.index[last]).date()), "n_symbols": int(close.shape[1])}
    for h in (10, 20):
        if last - h < 200:
            out[f"basket_{h}"] = np.nan
            out[f"universe_{h}"] = np.nan
            continue
        members = beaten_mask(close, last - h)
        m = members[members].index.tolist()
        out[f"n_beaten_{h}_ago"] = len(m)
        r = close[m].iloc[last] / close[m].iloc[last - h] - 1.0 if m else pd.Series(dtype=float)
        out[f"basket_{h}"] = float(r.mean()) if len(r) else np.nan
        u = close.iloc[last] / close.iloc[last - h] - 1.0
        out[f"universe_{h}"] = float(u.mean())
    now = beaten_mask(close, last)
    out["share_beaten"] = float(now.mean())
    out["n_beaten"] = int(now.sum())
    ago = beaten_mask(close, last - 20) if last >= 220 else None
    out["share_beaten_20_ago"] = float(ago.mean()) if ago is not None else np.nan
    ma50 = close.iloc[last - 49: last + 1].mean()
    out["share_above_ma50"] = float((close.iloc[last] > ma50).mean())
    if last >= 70:
        ma50_ago = close.iloc[last - 69: last - 19].mean()
        out["share_above_ma50_20_ago"] = float((close.iloc[last - 20] > ma50_ago).mean())
    else:
        out["share_above_ma50_20_ago"] = np.nan
    out["spy_20"] = out["spy_vs_ma50"] = out["spy_vs_ma200"] = np.nan
    if bench is not None and len(bench) >= 200:
        c = bench["Close"].astype(float)
        out["spy_20"] = float(c.iloc[-1] / c.iloc[-21] - 1.0)
        out["spy_vs_ma50"] = float(c.iloc[-1] / c.iloc[-50:].mean() - 1.0)
        out["spy_vs_ma200"] = float(c.iloc[-1] / c.iloc[-200:].mean() - 1.0)
    out["basket_vs_spy_20"] = out["basket_20"] - out["spy_20"] if np.isfinite(out.get("basket_20", np.nan)) and np.isfinite(out["spy_20"]) else np.nan
    out["warning"] = bool(np.isfinite(out.get("basket_20", np.nan)) and out["basket_20"] < WARN_20)
    return out


def _pct(v, d=1) -> str:
    return "" if v is None or not np.isfinite(v) else f"{v * 100:+.{d}f}%"


def regime_markdown(st: Dict, lang: str = "en") -> List[str]:
    """The regime line (two sentences) and, when the basket is falling, the warning line."""
    he = lang == "he"
    if he:
        line = (f"**משטר השוק.** סל המניות המוכות (שווה משקל, {st.get('n_beaten_20_ago', 0)} מניות שהיו מוכות לפני 20 נרות): "
                f"{_pct(st.get('basket_20'))} ב-20 נרות, {_pct(st.get('basket_10'))} ב-10, מול SPY {_pct(st.get('spy_20'))} ב-20 "
                f"(הפרש {_pct(st.get('basket_vs_spy_20'))}). רוחב: {st['share_above_ma50'] * 100:.0f}% מהיקום מעל ממוצע 50 "
                f"(לפני 20 נרות {st['share_above_ma50_20_ago'] * 100:.0f}%), {st['share_beaten'] * 100:.0f}% מוכות "
                f"(לפני 20 נרות {st['share_beaten_20_ago'] * 100:.0f}%). SPY מול ממוצע 50 {_pct(st.get('spy_vs_ma50'))}, מול ממוצע 200 {_pct(st.get('spy_vs_ma200'))}.")
        warn = (f"**אזהרה: הכללים נגד הרוח.** סל המניות המוכות ירד {_pct(st.get('basket_20'))} ב-20 הנרות האחרונים. כל הכללים בדוח קונים מניות "
                "מוכות; כשהסל עצמו יורד, גם הבחירות הטובות שבהן ירדו (ספטמבר 2026: כל הטבלאות הפסידו, בערך כמו ממוצע המניות המוכות). "
                "תיאור של המצב, לא תחזית; שער משטר ייכנס לכללים רק אחרי בדיקה לאחור (docs/research_filters.md).")
    else:
        line = (f"**Regime.** The beaten-down basket (equal weight, the {st.get('n_beaten_20_ago', 0)} stocks that were beaten down 20 bars ago): "
                f"{_pct(st.get('basket_20'))} over 20 bars, {_pct(st.get('basket_10'))} over 10, vs SPY {_pct(st.get('spy_20'))} over 20 "
                f"(difference {_pct(st.get('basket_vs_spy_20'))}). Breadth: {st['share_above_ma50'] * 100:.0f}% of the universe above the 50-day MA "
                f"({st['share_above_ma50_20_ago'] * 100:.0f}% 20 bars ago), {st['share_beaten'] * 100:.0f}% beaten down "
                f"({st['share_beaten_20_ago'] * 100:.0f}% 20 bars ago). SPY vs its 50-day MA {_pct(st.get('spy_vs_ma50'))}, vs its 200-day MA {_pct(st.get('spy_vs_ma200'))}.")
        warn = (f"**Warning: the rules are against the wind.** The beaten-down basket lost {_pct(st.get('basket_20'))} over the last 20 bars. Every rule "
                "in this report buys beaten-down stocks; when the basket itself is falling, even its better picks fell with it (September 2026: every "
                "table lost, about as much as the average beaten-down stock). A description of the state, not a forecast; a regime gate enters the "
                "rules only after a backtest (docs/research_filters.md).")
    md = [line, ""]
    if st.get("warning"):
        md += [warn, ""]
    return md
