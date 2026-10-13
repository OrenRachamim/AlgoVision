"""Volume around the turn, backtested (docs/research_volume.md).

The hypothesis: when a decline starts to stop and the turn comes on relatively high volume, the odds of a reversal
are better than on a quiet turn. Tested on the three rules with ten-year event tables (the beaten-down falling-wedge
breakout, the news-day rule, the early-rally rule), train / test as in ``algovision.research.filters``, with the same
verdict rule (yes minus no in excess return over local random entries, both periods, usable samples).

Volume features, all point-in-time at the signal bar ``t`` (the average windows end the bar before, so the signal day
is never compared with itself):

* **signal-day volume ratio** = volume[t] / mean(volume[t-20..t-1]);
* **5-day volume ratio** = mean(volume[t-4..t]) / mean(volume[t-20..t-1]) (volume expanding into the turn);
* **climax within 10 bars** = max over t-9..t of volume / mean(volume of the prior 60 bars) (a selling climax before
  or at the turn);
* **volume on the low day** = the signal-day-style ratio on the day of the lowest close of the last 20 bars
  (capitulation at the low itself);
* **up-volume share** = volume on up days / total volume over the last 10 bars (accumulation into the turn).

The news-day rule already requires >= 3x volume on the gap day, so its signal-day buckets start at 3x and the
"very high" condition is 5x.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence

import numpy as np
import pandas as pd

from algovision.research.filters import MIN_DIFF, MIN_SIDE, _fmt_buckets, _fmt_findings, _h, _p, bucket_table, condition_study

VOL_NAMES = {
    "c_vol_day_1_5": "signal-day volume >= 1.5x the prior 20-day average",
    "c_vol_day_2_5": "signal-day volume >= 2.5x the prior 20-day average",
    "c_vol_day_5": "signal-day volume >= 5x the prior 20-day average",
    "c_vol_5d_up": "5-day volume >= 1.3x the prior 20-day average (expanding into the turn)",
    "c_vol_climax10": "a >= 3x (60-day average) volume day within the last 10 bars (climax)",
    "c_vol_lowday_2": "volume on the 20-bar low-close day >= 2x its prior 20-day average (capitulation at the low)",
    "c_vol_upshare": ">= 60% of the last 10 bars' volume on up days (accumulation)",
    "c_base_vol_up": "in a base (15-bar close range <= 8%, the 40-bar low made > 10 bars ago) with base volume >= 1.3x the 40 bars before it",
    "c_base_vol_quiet": "in a base (same definition) with base volume <= 0.8x the 40 bars before it",
}
BASE_BARS, BASE_RANGE, PRE_BARS = 15, 0.08, 40
BASE_BINS = [0, 0.8, 1.0, 1.3, 1.6, np.inf]
BASE_LABELS = ["< 0.8x", "0.8-1x", "1-1.3x", "1.3-1.6x", "> 1.6x"]

DAY_BINS = [0, 0.8, 1.2, 2.0, 3.0, np.inf]
DAY_LABELS = ["< 0.8x", "0.8-1.2x", "1.2-2x", "2-3x", "> 3x"]
NEWS_BINS = [0, 5.0, 8.0, np.inf]
NEWS_LABELS = ["3-5x", "5-8x", "> 8x"]
CLIMAX_BINS = [0, 1.5, 3.0, 5.0, np.inf]
CLIMAX_LABELS = ["< 1.5x", "1.5-3x", "3-5x", "> 5x"]


# ----------------------------------------------------------------------------
# features on the wide panel
# ----------------------------------------------------------------------------
def _lowday_ratio(close: np.ndarray, ratio: np.ndarray, window: int = 20) -> np.ndarray:
    """For every bar, the volume ratio on the day of the lowest close of the last ``window`` bars (NaN before)."""
    n = len(close)
    out = np.full(n, np.nan)
    if n < window:
        return out
    c = np.where(np.isfinite(close), close, np.inf)
    from numpy.lib.stride_tricks import sliding_window_view
    w = sliding_window_view(c, window)                  # (n - window + 1, window)
    am = np.argmin(w, axis=1)
    pos = np.arange(window - 1, n) - (window - 1) + am  # absolute index of the low day
    out[window - 1:] = ratio[pos]
    return out


def volume_context(panel: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Per-stock, per-date volume features (wide frames aligned with the panel)."""
    v = panel["Volume"].astype(float)
    close = panel["Close"].astype(float)
    avg20 = v.rolling(20, min_periods=15).mean().shift(1)
    avg60 = v.rolling(60, min_periods=40).mean().shift(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        day = v / avg20
        five = v.rolling(5, min_periods=5).mean() / avg20
        climax = (v / avg60).rolling(10, min_periods=5).max()
        up = (close > close.shift(1)).astype(float)
        upshare = (v * up).rolling(10, min_periods=8).sum() / v.rolling(10, min_periods=8).sum()
    lowday = pd.DataFrame({s: _lowday_ratio(close[s].to_numpy(dtype=float), day[s].to_numpy(dtype=float)) for s in close.columns},
                          index=close.index)
    # the base: a beaten-down stock whose price stopped falling and holds a tight range; volume in the base vs before it
    ma200 = close.rolling(200, min_periods=200).mean()
    r126 = close / close.shift(126) - 1.0
    beaten = (close < ma200) & (r126 < -0.08)
    hi15, lo15, mean15 = close.rolling(BASE_BARS).max(), close.rolling(BASE_BARS).min(), close.rolling(BASE_BARS).mean()
    with np.errstate(invalid="ignore", divide="ignore"):
        base_range = (hi15 - lo15) / mean15
        low_before = close.rolling(10).min() > close.shift(10).rolling(30).min()       # the 40-bar low was made more than 10 bars ago
        base = beaten & (base_range <= BASE_RANGE) & low_before
        base_vol = v.rolling(BASE_BARS, min_periods=BASE_BARS).mean() / v.shift(BASE_BARS).rolling(PRE_BARS, min_periods=30).mean()
    return {"day": day.replace([np.inf, -np.inf], np.nan), "five": five.replace([np.inf, -np.inf], np.nan),
            "climax": climax.replace([np.inf, -np.inf], np.nan), "lowday": lowday.replace([np.inf, -np.inf], np.nan),
            "upshare": upshare, "close": close, "open": panel["Open"].astype(float), "base": base.fillna(False),
            "base_vol": base_vol.replace([np.inf, -np.inf], np.nan), "base_hi": hi15, "base_lo": lo15, "base_range": base_range}


def attach_volume(ev: pd.DataFrame, vctx: Dict[str, pd.DataFrame], date_col: str = "date") -> pd.DataFrame:
    """Volume condition columns (``c_vol_*``) and raw features (``x_vol_*``) for every event (symbol, date)."""
    out = ev.copy()
    d = pd.to_datetime(out[date_col])
    idx = vctx["close"].index
    pos = idx.searchsorted(d, side="right") - 1
    ok = (pos >= 0) & (pos < len(idx))
    cols = list(vctx["close"].columns)
    col_pos = pd.Series(range(len(cols)), index=cols)
    cp = out["symbol"].map(col_pos)
    ok &= cp.notna().to_numpy()
    cp = cp.fillna(0).astype(int).to_numpy()
    pos = np.where(ok, pos, 0)

    def per_stock(frame: pd.DataFrame) -> np.ndarray:
        x = frame.to_numpy(dtype=float)[pos, cp]
        return np.where(ok, x, np.nan)

    day, five, climax, lowday, upshare, bvol = (per_stock(vctx[k]) for k in ("day", "five", "climax", "lowday", "upshare", "base_vol"))
    base = np.where(ok, vctx["base"].to_numpy()[pos, cp], False)
    out["vol_ok"] = ok & np.isfinite(day)
    out["c_vol_day_1_5"] = np.nan_to_num(day >= 1.5, nan=False)
    out["c_vol_day_2_5"] = np.nan_to_num(day >= 2.5, nan=False)
    out["c_vol_day_5"] = np.nan_to_num(day >= 5.0, nan=False)
    out["c_vol_5d_up"] = np.nan_to_num(five >= 1.3, nan=False)
    out["c_vol_climax10"] = np.nan_to_num(climax >= 3.0, nan=False)
    out["c_vol_lowday_2"] = np.nan_to_num(lowday >= 2.0, nan=False)
    out["c_vol_upshare"] = np.nan_to_num(upshare >= 0.60, nan=False)
    out["c_base_vol_up"] = base & np.nan_to_num(bvol >= 1.3, nan=False)
    out["c_base_vol_quiet"] = base & np.nan_to_num(bvol <= 0.8, nan=False)
    out["x_vol_day"], out["x_vol_5d"], out["x_vol_climax10"], out["x_vol_lowday"], out["x_vol_upshare"] = day, five, climax, lowday, upshare
    out["in_base"], out["x_base_vol"] = base, bvol
    return out


def volume_buckets(ev: pd.DataFrame, newsday: bool = False) -> pd.DataFrame:
    out = ev.copy()
    if newsday:
        out["vol_day_bucket"] = pd.cut(out["x_vol_day"], NEWS_BINS, labels=NEWS_LABELS)
    else:
        out["vol_day_bucket"] = pd.cut(out["x_vol_day"], DAY_BINS, labels=DAY_LABELS)
    out["vol_climax_bucket"] = pd.cut(out["x_vol_climax10"], CLIMAX_BINS, labels=CLIMAX_LABELS)
    return out


def volume_at(df: pd.DataFrame, t: Optional[int] = None) -> Dict[str, float]:
    """The two context numbers the report shows for one stock at bar ``t`` (default: the last bar): the day's volume vs the
    prior 20-day average and the largest volume day of the last 10 bars vs the prior 60-day average (NaN when too short)."""
    v = np.nan_to_num(df["Volume"].to_numpy(dtype=float))
    n = len(v)
    t = n - 1 if t is None else int(t)
    out = {"day": np.nan, "climax10": np.nan}
    if t < 0 or t >= n:
        return out
    a20 = v[max(0, t - 20):t]
    if len(a20) >= 15 and a20.mean() > 0:
        out["day"] = float(v[t] / a20.mean())
    best = np.nan
    for j in range(max(0, t - 9), t + 1):
        a60 = v[max(0, j - 60):j]
        if len(a60) >= 40 and a60.mean() > 0:
            r = v[j] / a60.mean()
            best = r if not np.isfinite(best) or r > best else best
    out["climax10"] = float(best) if np.isfinite(best) else np.nan
    return out


# ----------------------------------------------------------------------------
# the base study: every tight base after a decline is an event; rising volume vs quiet
# ----------------------------------------------------------------------------
def base_events(vctx: Dict[str, pd.DataFrame], spy_close: pd.Series, horizons: Sequence[int] = (20, 60), min_gap: int = 30,
                local_window: int = 126, random_draws: int = 10, seed: int = 7) -> pd.DataFrame:
    """One row per (symbol, first base day in a 30-bar window): forward returns from the next open, SPY and local-random
    excess, and whether the stock left the base upward (close above the base high) or downward (below the base low)."""
    import zlib
    close, open_ = vctx["close"], vctx["open"]
    base, bvol, hi, lo = (vctx[k] for k in ("base", "base_vol", "base_hi", "base_lo"))
    idx = close.index
    spy = spy_close.reindex(idx).ffill().to_numpy(dtype=float)
    hmax = max(horizons)
    rows: List[Dict] = []
    for s in close.columns:
        b = base[s].to_numpy()
        hits = np.where(b)[0]
        if not len(hits):
            continue
        c, o = close[s].to_numpy(dtype=float), open_[s].to_numpy(dtype=float)
        bv, bh, bl = bvol[s].to_numpy(dtype=float), hi[s].to_numpy(dtype=float), lo[s].to_numpy(dtype=float)
        n = len(c)
        rng = np.random.default_rng(seed + zlib.crc32(s.encode()) % 100000)
        last = -10 ** 6
        for t in hits:
            if t - last < min_gap or t + hmax + 1 >= n or t < 260 or not np.isfinite(bv[t]):
                continue
            last = t
            entry = o[t + 1]
            if not np.isfinite(entry) or entry <= 0:
                continue
            row = {"symbol": s, "date": idx[t], "entry": float(entry), "base_vol": float(bv[t]), "base_hi": float(bh[t]), "base_lo": float(bl[t]),
                   "ret_126": float(c[t] / c[t - 126] - 1.0)}
            for h in horizons:
                r = c[t + h] / entry - 1.0
                row[f"ret_{h}"] = float(r)
                row[f"xspy_{h}"] = float(r - (spy[t + h] / spy[t + 1] - 1.0)) if np.isfinite(spy[t + 1]) else np.nan
                row[f"up_{h}"] = bool(c[t + h] > bh[t])          # left the base upward
                row[f"down_{h}"] = bool(c[t + h] < bl[t])        # broke the base
                lo_, hi_ = max(1, t - local_window), min(n - h - 3, t + local_window)
                cand = np.arange(lo_, hi_ + 1)
                cand = cand[np.abs(cand - t) > h]
                if len(cand) >= 5:
                    pick = rng.choice(cand, size=random_draws, replace=len(cand) < random_draws)
                    row[f"xloc_{h}"] = float(r - np.mean(c[pick + h] / o[pick + 1] - 1.0))
                else:
                    row[f"xloc_{h}"] = np.nan
            rows.append(row)
    ev = pd.DataFrame(rows)
    if len(ev):
        ev["vol_ok"] = True
        ev["c_base_vol_up"] = ev["base_vol"] >= 1.3
        ev["c_base_vol_quiet"] = ev["base_vol"] <= 0.8
        ev["base_vol_bucket"] = pd.cut(ev["base_vol"], BASE_BINS, labels=BASE_LABELS)
    return ev


def base_direction_table(ev: pd.DataFrame, split: str, horizons: Sequence[int] = (20, 60)) -> pd.DataFrame:
    """Per volume bucket and period: how often the stock left the base upward vs broke it, and the mean return."""
    d = pd.to_datetime(ev["date"])
    rows = []
    for period, mask in (("train", d < split), ("test", d >= split)):
        for key, g in ev[mask].groupby("base_vol_bucket", observed=True):
            rec = {"bucket": str(key), "period": period, "n": int(len(g))}
            for h in horizons:
                rec[f"up_{h}"] = float(g[f"up_{h}"].mean()) if len(g) else np.nan
                rec[f"down_{h}"] = float(g[f"down_{h}"].mean()) if len(g) else np.nan
                rec[f"net_{h}"] = float(g[f"ret_{h}"].mean() - 0.001) if len(g) else np.nan
                rec[f"xloc_{h}"] = float(g[f"xloc_{h}"].dropna().mean()) if len(g) else np.nan
            rows.append(rec)
    return pd.DataFrame(rows)


def _fmt_direction(t: pd.DataFrame, horizons=(20, 60)) -> str:
    head = " | ".join(f"{h} bars: left upward / broke down / net / excess over local random" for h in horizons)
    lines = [f"| base volume vs the 40 bars before | period | n | {head} |", "|" + "---|" * (3 + len(horizons))]
    for r in t.itertuples():
        cells = [f"{_h(getattr(r, f'up_{h}'))} / {_h(getattr(r, f'down_{h}'))} / {_p(getattr(r, f'net_{h}'))} / {_p(getattr(r, f'xloc_{h}'))}" for h in horizons]
        lines.append(f"| {r.bucket} | {r.period} | {r.n} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# the report
# ----------------------------------------------------------------------------
def write_volume_report(out_dir: Path, split: str, families: Dict[str, Dict], doc_path: Optional[Path] = None,
                        base: Optional[pd.DataFrame] = None) -> Path:
    """``families`` = {name: {"events": ev with volume columns, "ret_col", "x_col", "date_col", "slug", "newsday": bool}};
    ``base`` = the standalone base events from ``base_events`` (optional)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    md = ["# Volume around the turn, backtested (2016-2026)", "",
          "Hypothesis: when a decline starts to stop and the turn comes on relatively high volume, the odds of a reversal are "
          "better than on a quiet turn. Tested on the three rules with ten-year event tables, train (before "
          f"{split}) and test (from {split}) separately. Entry at the next open, 10 bps cost, excess measured over random entries "
          "in the same stock within half a year of the signal (``xloc``), which cancels the stock's drift and the regime around the signal.", "",
          "Volume features are point-in-time at the signal bar and the averages end the bar before, so the signal day is never "
          "compared with itself: the signal-day ratio (volume / prior 20-day average), the 5-day ratio (last five bars / prior 20-day "
          "average), a climax day (>= 3x the prior 60-day average) within the last 10 bars, the ratio on the day of the lowest close "
          "of the last 20 bars, and the share of the last 10 bars' volume that came on up days. Two more look at the base before the signal: "
          f"a beaten-down stock whose last {BASE_BARS} closes span at most {BASE_RANGE * 100:.0f}% and whose 40-bar low was made more than 10 bars "
          f"ago (the decline stopped), with the base's average volume at least 1.3x (or at most 0.8x) the {PRE_BARS} bars before it.", "",
          f"A condition **helps** when the yes rows beat the no rows in excess return in **both** periods by at least {MIN_DIFF * 100:.1f}% over "
          f"20 bars with at least {MIN_SIDE} events on each side; it **hurts** when the no rows beat the yes rows by the same margin in both "
          "periods; everything else is noise however good one period looks. Survivorship bias applies (today's index members).", ""]
    verdicts: List[str] = []
    for name, fam in families.items():
        ev = fam["events"]
        md += [f"## {name}", "", f"{len(ev)} events, {ev['symbol'].nunique()} stocks, {pd.to_datetime(ev[fam['date_col']]).min().date()} to "
               f"{pd.to_datetime(ev[fam['date_col']]).max().date()}; volume context available for {int(ev['vol_ok'].sum())} of them.", ""]
        conds = [c for c in VOL_NAMES if c in ev and not (fam.get("newsday") and c in ("c_vol_day_1_5", "c_vol_day_2_5"))]
        detail, find = condition_study(ev, split, conds, 20, 60, fam["ret_col"], fam["x_col"], fam["date_col"], names=VOL_NAMES)
        detail.to_csv(out / f"{fam['slug']}_volume_conditions.csv", index=False)
        find.to_csv(out / f"{fam['slug']}_volume_findings.csv", index=False)
        md += ["### Conditions", "", _fmt_findings(find, 20, 60), ""]
        for r in find.itertuples():
            if r.consistent:
                verdicts.append(f"- **{name}**: *{r.condition}* helps ({_p(getattr(r, 'train_diff_20'))} train, {_p(getattr(r, 'test_diff_20'))} test at 20 bars; "
                                f"{_p(getattr(r, 'train_diff_60'))} / {_p(getattr(r, 'test_diff_60'))} at 60).")
            elif r.consistent_negative:
                verdicts.append(f"- **{name}**: *{r.condition}* hurts ({_p(getattr(r, 'train_diff_20'))} train, {_p(getattr(r, 'test_diff_20'))} test at 20 bars; "
                                f"{_p(getattr(r, 'train_diff_60'))} / {_p(getattr(r, 'test_diff_60'))} at 60).")
        evb = volume_buckets(ev, newsday=bool(fam.get("newsday")))
        for label, col in (("Signal-day volume (vs the prior 20-day average)", "vol_day_bucket"), ("Largest volume day of the last 10 bars (vs the prior 60-day average)", "vol_climax_bucket")):
            t = bucket_table(evb, col, split, 20, fam["ret_col"], fam["x_col"], fam["date_col"])
            t.to_csv(out / f"{fam['slug']}_{col}.csv", index=False)
            md += [f"### {label}", "", _fmt_buckets(t, 20), ""]
    if base is not None and len(base):
        md += ["## Rising volume while the price stabilizes (every tight base after a decline, no rule)", "",
               f"Every beaten-down stock whose last {BASE_BARS} closes span at most {BASE_RANGE * 100:.0f}% and whose 40-bar low was made more than "
               f"10 bars ago is an event (first such day in a 30-bar window), {len(base)} events in {base['symbol'].nunique()} stocks, "
               f"{pd.to_datetime(base['date']).min().date()} to {pd.to_datetime(base['date']).max().date()}. Entry at the next open. "
               "*Left upward* = the close 20 / 60 bars later is above the base's high; *broke down* = below the base's low; the rest are still inside.", ""]
        bd = base_direction_table(base, split)
        bd.to_csv(out / "base_direction.csv", index=False)
        md += [_fmt_direction(bd), ""]
        detail, find = condition_study(base, split, ["c_base_vol_up", "c_base_vol_quiet"], 20, 60, "ret", "xloc", "date", names=VOL_NAMES)
        find.to_csv(out / "base_findings.csv", index=False)
        md += ["### Conditions (base volume >= 1.3x vs the rest; <= 0.8x vs the rest)", "", _fmt_findings(find, 20, 60), ""]
        for r in find.itertuples():
            if r.consistent:
                verdicts.append(f"- **Bases after a decline**: *{r.condition}* helps ({_p(getattr(r, 'train_diff_20'))} train, {_p(getattr(r, 'test_diff_20'))} test at 20 bars; "
                                f"{_p(getattr(r, 'train_diff_60'))} / {_p(getattr(r, 'test_diff_60'))} at 60).")
            elif r.consistent_negative:
                verdicts.append(f"- **Bases after a decline**: *{r.condition}* hurts ({_p(getattr(r, 'train_diff_20'))} train, {_p(getattr(r, 'test_diff_20'))} test at 20 bars; "
                                f"{_p(getattr(r, 'train_diff_60'))} / {_p(getattr(r, 'test_diff_60'))} at 60).")
    md += ["## Verdicts", ""] + (verdicts or ["- No volume condition passed in both periods; volume should not change a rule or a ranking."]) + [""]
    md += ["## Reading", "",
           "Only a condition marked **helps** or **hurts** in a family is a candidate for that family's rule, and only as stated. The "
           "bucket tables show whether the effect is monotonic (more volume, more edge) or a threshold; a condition that passes while "
           "its buckets wander is weaker than one whose buckets line up. A volume feature that passes in one family and fails in another "
           "stays confined to the family where it passed.", "",
           "Systematic screens and an event study on today's index members (survivorship bias), not investment advice.", ""]
    text = "\n".join(md)
    (out / "README.md").write_text(text, encoding="utf-8")
    if doc_path:
        Path(doc_path).write_text(text, encoding="utf-8")
    return out / "README.md"
