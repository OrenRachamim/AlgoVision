"""Markdown + HTML research report."""

from __future__ import annotations

import base64
import html
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from algovision.research.events import HORIZONS
from algovision.research.stats import (breakdown, calibration, compare_walkforward, conditional_table,
                                       score_threshold_table, structure_table, summary_table, volume_buckets)

# validated default palette (light surface)
C = {"s1": "#2a78d6", "s2": "#eb6834", "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
     "grid": "#e1e0d9", "axis": "#c3c2b7", "surface": "#fcfcfb"}

MIN_N_VERDICT = 100


def _style(ax, title: str, xlabel: str = "", ylabel: str = "") -> None:
    ax.set_facecolor(C["surface"])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(C["axis"])
    ax.tick_params(colors=C["muted"], labelsize=8)
    ax.grid(True, axis="x" if ax.get_xscale() else "both", color=C["grid"], lw=0.6)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=10, loc="left", color=C["ink"])
    ax.set_xlabel(xlabel, fontsize=8, color=C["ink2"])
    ax.set_ylabel(ylabel, fontsize=8, color=C["ink2"])


def _fig(w=8, h=4.5):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    fig.patch.set_facecolor(C["surface"])
    return fig, ax, plt


def _save(fig, plt, path: Path) -> str:
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return base64.b64encode(path.read_bytes()).decode("ascii")


def chart_excess(t: pd.DataFrame, h: int, path: Path) -> str:
    pre = "xloc" if f"xloc_{h}" in t.columns and np.isfinite(t[f"xloc_{h}"]).any() else "xrand"
    d = t.drop(index="ALL", errors="ignore").sort_values(f"{pre}_{h}")
    fig, ax, plt = _fig(8, 0.35 * len(d) + 1.5)
    y = np.arange(len(d))
    lo = d[f"{pre}_{h}"] - d[f"{pre}_lo_{h}"]
    hi = d[f"{pre}_hi_{h}"] - d[f"{pre}_{h}"]
    ax.errorbar(d[f"{pre}_{h}"] * 100, y, xerr=[lo * 100, hi * 100], fmt="o", color=C["s1"], ecolor=C["s1"],
                elinewidth=1.5, capsize=3, ms=6)
    ax.axvline(0, color=C["axis"], lw=1)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{p}  (n={int(n)})" for p, n in zip(d.index, d["n"])], fontsize=8, color=C["ink"])
    what = "local random entries (same stock, +-6 months)" if pre == "xloc" else "random-date entries"
    _style(ax, f"Mean {h}-bar return in excess of {what}, 95% bootstrap CI", "excess return, %")
    ax.grid(True, axis="y", color=C["grid"], lw=0.4)
    return _save(fig, plt, path)


def chart_hit(t: pd.DataFrame, h: int, path: Path) -> str:
    d = t.drop(index="ALL", errors="ignore").sort_values(f"hit_{h}")
    fig, ax, plt = _fig(8, 0.35 * len(d) + 1.5)
    y = np.arange(len(d))
    for yi, (a, b) in enumerate(zip(d[f"rand_hit_{h}"], d[f"hit_{h}"])):
        ax.plot([a * 100, b * 100], [yi, yi], color=C["grid"], lw=2, zorder=1)
    ax.scatter(d[f"rand_hit_{h}"] * 100, y, color=C["s2"], s=36, zorder=2, label="random-date entries")
    ax.scatter(d[f"hit_{h}"] * 100, y, color=C["s1"], s=36, zorder=3, label="pattern signals")
    ax.set_yticks(y)
    ax.set_yticklabels(list(d.index), fontsize=8, color=C["ink"])
    _style(ax, f"Share of signals with a positive {h}-bar return (in the pattern's direction)", "hit rate, %")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.grid(True, axis="y", color=C["grid"], lw=0.4)
    return _save(fig, plt, path)


def chart_calibration(cal: pd.DataFrame, h: int, path: Path) -> str:
    fig, ax, plt = _fig(7, 3.6)
    x = np.arange(len(cal))
    ax.bar(x, cal["xloc" if "xloc" in cal.columns else "xrand"] * 100, color=C["s1"], width=0.6)
    ax.axhline(0, color=C["axis"], lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{a:.2f}-{b:.2f}\n(n={int(n)})" for a, b, n in zip(cal["score_min"], cal["score_max"], cal["n"])],
                       fontsize=8, color=C["ink"])
    rho = cal.attrs.get("spearman_rho", np.nan)
    _style(ax, f"Score calibration: excess {h}-bar return by score quintile (Spearman rho={rho:.2f})", "score bin",
           "excess return, %")
    ax.grid(True, axis="y", color=C["grid"], lw=0.6)
    ax.grid(False, axis="x")
    return _save(fig, plt, path)


def chart_year(by: pd.DataFrame, h: int, path: Path) -> str:
    fig, ax, plt = _fig(7, 3.4)
    x = np.arange(len(by))
    ax.bar(x, by["xloc" if "xloc" in by.columns else "xrand"] * 100, color=C["s1"], width=0.6)
    ax.axhline(0, color=C["axis"], lw=1)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{i}\n(n={int(n)})" for i, n in zip(by.index, by["n"])], fontsize=8, color=C["ink"])
    _style(ax, f"Stability over time: excess {h}-bar return by signal year", "", "excess return, %")
    ax.grid(True, axis="y", color=C["grid"], lw=0.6)
    ax.grid(False, axis="x")
    return _save(fig, plt, path)


def chart_trade(t: pd.DataFrame, path: Path) -> str:
    d = t.drop(index="ALL", errors="ignore").sort_values("target_rate")
    fig, ax, plt = _fig(8, 0.35 * len(d) + 1.5)
    y = np.arange(len(d))
    ax.barh(y - 0.18, d["target_rate"] * 100, height=0.34, color=C["s1"], label="target hit first")
    ax.barh(y + 0.18, d["stop_rate"] * 100, height=0.34, color=C["s2"], label="stop hit first")
    ax.set_yticks(y)
    ax.set_yticklabels(list(d.index), fontsize=8, color=C["ink"])
    _style(ax, "Trade simulation within 60 bars: measured-move target vs. pattern stop", "% of signals")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.grid(True, axis="x", color=C["grid"], lw=0.6)
    ax.grid(False, axis="y")
    return _save(fig, plt, path)


def verdict(row: pd.Series, h: int = 20) -> str:
    n = row.get("n", 0)
    if n < MIN_N_VERDICT:
        return "insufficient data"
    if f"xloc_lo_{h}" in row.index and np.isfinite(row.get(f"xloc_lo_{h}", np.nan)):
        lo, hi, p = row.get(f"xloc_lo_{h}"), row.get(f"xloc_hi_{h}"), row.get(f"ploc_{h}")
    else:
        lo, hi, p = row.get(f"xrand_lo_{h}"), row.get(f"xrand_hi_{h}"), row.get(f"p_{h}")
    pf = row.get("profit_factor", np.nan)
    if np.isfinite(lo) and lo > 0 and p < 0.05:
        return "edge vs random (statistically significant)"
    if np.isfinite(hi) and hi < 0:
        return "worse than random"
    if np.isfinite(pf) and pf > 1.1 and row.get("avg_r", 0) > 0.05:
        return "weak / unproven (positive R but not significant)"
    return "no detectable edge"


def _fmt_table(df: pd.DataFrame, cols: List[str], pct_cols: List[str] = (), float_cols: Dict[str, int] = None) -> str:
    float_cols = float_cols or {}
    d = df[cols].copy()
    for c in pct_cols:
        if c in d:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v * 100:+.2f}%" if "x" in c or "ret" in c else f"{v * 100:.1f}%")
    for c, k in float_cols.items():
        if c in d:
            d[c] = d[c].map(lambda v: "" if pd.isna(v) else f"{v:.{k}f}")
    return d.to_markdown()


def build_markdown(events: pd.DataFrame, structures: pd.DataFrame, wf: Optional[pd.DataFrame], meta: Dict,
                   h: int = 20) -> Dict:
    out: Dict = {}
    t = summary_table(events)
    t["verdict"] = [verdict(t.loc[i], h) for i in t.index]
    out["summary"] = t
    md: List[str] = []
    md.append("# Can the setups be trusted? - AlgoVision research report\n")
    md.append(f"Generated {meta.get('generated', '')}. Universe: **{meta.get('universe')}** "
              f"({meta.get('n_symbols')} symbols, {events['symbol'].nunique()} with events), period {meta.get('period')}, "
              f"daily bars, benchmark {meta.get('benchmark')}. Detector config: min_score={meta.get('config', {}).get('min_score')}.\n")
    md.append("## Method\n")
    md.append("""
* Every **confirmed** pattern is one event. The signal bar is the later of the breakout bar and the bar at which
  the last swing point of the structure became knowable (`pivot + order`), so nothing from the future is used to
  decide the shape. Entry is the **next bar's open**.
* Returns are **signed by the pattern's direction** (a bearish pattern "wins" when price falls) and measured over
  5/10/20/40/60 bars, close-to-entry.
* Three baselines: raw, **minus SPY** over the same window, and **minus random-date entries in the same stock and
  direction** (20 draws per event). The random-date baseline cancels each stock's drift and the survivorship bias
  of using today's index members, so it is the number to trust.
* A fourth, stricter baseline, **local random entries** (`xloc`): random dates within +-126 bars of the signal in the
  same stock and direction. This also cancels the *regime* around the signal (bear patterns cluster in bear phases),
  so it is the number the verdicts are based on.
* `p` / `p_loc` are one-sided permutation p-values: the share of "no-skill" replicates (one random date per event)
  whose mean return is at least as good as the pattern's. CIs are 95% bootstrap intervals of the mean excess return.
* Trade simulation: enter at next open, exit at the measured-move **target** or the pattern **stop** (whichever is
  touched first; stop wins ties) or after 60 bars. R = result / initial risk. Profit factor = gross wins / gross losses in R.
* **Walk-forward validation**: on a random subsample the detectors were re-run bar by bar seeing only past data;
  its events are compared with the fast hindsight method to quantify look-ahead bias.
""")
    md.append(f"## Headline numbers ({h}-bar horizon)\n")
    a = t.loc["ALL"]
    md.append(f"* Events: **{int(a['n'])}** across {int(a['n_symbols'])} symbols; {len(t) - 1} pattern types.")
    md.append(f"* Mean {h}-bar return in the pattern's direction: **{a[f'ret_{h}'] * 100:+.2f}%** "
              f"(hit rate {a[f'hit_{h}'] * 100:.1f}%, random-date hit rate {a[f'rand_hit_{h}'] * 100:.1f}%).")
    md.append(f"* Excess over SPY: **{a[f'xspy_{h}'] * 100:+.2f}%**; excess over random-date entries: "
              f"**{a[f'xrand_{h}'] * 100:+.2f}%** (95% CI {a[f'xrand_lo_{h}'] * 100:+.2f}% to {a[f'xrand_hi_{h}'] * 100:+.2f}%, "
              f"permutation p = {a[f'p_{h}']:.3f}).")
    if f"xloc_{h}" in a.index and np.isfinite(a[f"xloc_{h}"]):
        md.append(f"* Excess over **local** random entries (same stock, +-6 months): **{a[f'xloc_{h}'] * 100:+.2f}%** "
                  f"(95% CI {a[f'xloc_lo_{h}'] * 100:+.2f}% to {a[f'xloc_hi_{h}'] * 100:+.2f}%, p = {a[f'ploc_{h}']:.3f}; "
                  f"local random hit rate {a[f'loc_hit_{h}'] * 100:.1f}%).")
    md.append(f"* Trade simulation: target hit first {a['target_rate'] * 100:.1f}%, stop hit first {a['stop_rate'] * 100:.1f}%, "
              f"average R = {a.get('avg_r', np.nan):+.2f}, profit factor {a.get('profit_factor', np.nan):.2f}, "
              f"average reward:risk {a.get('avg_reward_risk', np.nan):.2f}.\n")
    md.append("## Per-pattern results\n")
    has_loc = f"xloc_{h}" in t.columns
    cols = ["n", "n_symbols", f"hit_{h}", f"rand_hit_{h}", f"ret_{h}", f"xspy_{h}", f"xrand_{h}", f"p_{h}"]
    if has_loc:
        cols += [f"xloc_{h}", f"xloc_lo_{h}", f"xloc_hi_{h}", f"ploc_{h}"]
    cols += ["target_rate", "stop_rate", "avg_r", "profit_factor", "verdict"]
    md.append(_fmt_table(t, cols, [f"hit_{h}", f"rand_hit_{h}", f"ret_{h}", f"xspy_{h}", f"xrand_{h}", f"xloc_{h}",
                                   f"xloc_lo_{h}", f"xloc_hi_{h}", "target_rate", "stop_rate"],
                         {f"p_{h}": 3, f"ploc_{h}": 3, "avg_r": 2, "profit_factor": 2}))
    md.append("\n## Across horizons (all patterns pooled)\n")
    rows = []
    for hh in HORIZONS:
        if not a.get(f"n_{hh}", 0):
            continue
        rows.append({"horizon": hh, "n": int(a[f"n_{hh}"]), "hit": a.get(f"hit_{hh}"), "rand_hit": a.get(f"rand_hit_{hh}"),
                     "ret": a.get(f"ret_{hh}"), "xspy": a.get(f"xspy_{hh}"), "xrand": a.get(f"xrand_{hh}"),
                     "ci_lo": a.get(f"xrand_lo_{hh}"), "ci_hi": a.get(f"xrand_hi_{hh}"), "p": a.get(f"p_{hh}"),
                     "xloc": a.get(f"xloc_{hh}", np.nan), "p_loc": a.get(f"ploc_{hh}", np.nan)})
    hz = pd.DataFrame(rows).set_index("horizon")
    out["horizons"] = hz
    md.append(_fmt_table(hz, list(hz.columns), ["hit", "rand_hit", "ret", "xspy", "xrand", "ci_lo", "ci_hi", "xloc"], {"p": 3, "p_loc": 3}))
    md.append("\n## By direction\n")
    bd = breakdown(events, "direction", h)
    out["by_direction"] = bd
    md.append(_fmt_table(bd, list(bd.columns), ["ret", "xspy", "xrand", "xloc", "hit", "target_rate", "stop_rate"], {"avg_r": 2}))
    cal = calibration(events, h)
    out["calibration"] = cal
    if len(cal):
        md.append(f"\n## Score calibration (Spearman rho between score and excess return = {cal.attrs['spearman_rho']:.3f}, "
                  f"p = {cal.attrs['spearman_p']:.3f})\n")
        md.append(_fmt_table(cal.reset_index().drop(columns=["score_bin"]).set_index("score_min"),
                             ["n", "score_max", "ret", "xrand", "hit", "target_rate", "avg_r"],
                             ["ret", "xrand", "hit", "target_rate"], {"score_max": 2, "avg_r": 2}))
    st_ = score_threshold_table(events, h)
    out["score_threshold"] = st_
    if len(st_):
        md.append("\n## Raising the scanner threshold\n")
        md.append(_fmt_table(st_, list(st_.columns), ["hit", "ret", "xrand", "xloc", "target_rate"], {"avg_r": 2}))
    ct = conditional_table(events, h)
    out["conditional"] = ct
    if len(ct):
        md.append(f"\n## Conditional view per pattern (excess {h}-bar return over local random entries; blank = fewer than 100 events)\n")
        ccols = [c for c in ct.columns if c.startswith("xrand")] + ["n", "years", "years_positive"]
        md.append(_fmt_table(ct, ccols, [c for c in ccols if c.startswith("xrand")]))
    md.append("\n## Breakout volume\n")
    ev2 = events.copy()
    ev2["volume_bucket"] = volume_buckets(ev2)
    bv = breakdown(ev2.dropna(subset=["volume_bucket"]), "volume_bucket", h)
    out["by_volume"] = bv
    md.append(_fmt_table(bv, list(bv.columns), ["ret", "xspy", "xrand", "xloc", "hit", "target_rate", "stop_rate"], {"avg_r": 2}))
    md.append("\n## By year\n")
    by = breakdown(events, "year", h)
    out["by_year"] = by
    md.append(_fmt_table(by, list(by.columns), ["ret", "xspy", "xrand", "xloc", "hit", "target_rate", "stop_rate"], {"avg_r": 2}))
    md.append("\n## By pivot scale\n")
    bs = breakdown(events, "scale", h)
    out["by_scale"] = bs
    md.append(_fmt_table(bs, list(bs.columns), ["ret", "xspy", "xrand", "xloc", "hit", "target_rate", "stop_rate"], {"avg_r": 2}))
    if len(structures):
        st = structure_table(structures)
        out["structures"] = st
        md.append("\n## Forming setups: once the shape is complete, does it confirm?\n")
        md.append("`failed` means price broke the *opposite* way (or invalidated the shape) before confirming. "
                  "Flags, cups, rectangles and symmetrical triangles have no failure rule in the detectors - they are only "
                  "recorded once they break out - so their 100% is by construction, not evidence.\n")
        md.append(_fmt_table(st, list(st.columns), ["confirm_rate", "fail_rate", "expire_rate"]))
    if wf is not None and len(wf):
        wmeta = meta.get("walkforward", {})
        syms = wmeta.get("symbols", [])
        sub = events[events["symbol"].isin(syms)]
        # restrict hindsight to the walk-forward's bar range per symbol
        parts = []
        for s in syms:
            g = sub[sub["symbol"] == s]
            wg = wf[wf["symbol"] == s]
            if len(wg):
                parts.append(g[g["signal_idx"] >= wg["signal_idx"].min() - 5])
            else:
                parts.append(g.iloc[0:0])
        hind = pd.concat(parts) if parts else sub
        cmp_ = compare_walkforward(hind, wf, h)
        out["walkforward"] = cmp_
        md.append("\n## Look-ahead check: walk-forward vs hindsight\n")
        md.append(f"Sample: {len(syms)} symbols, last {wmeta.get('last_bars')} bars each, detection window "
                  f"{wmeta.get('window')} bars, step {wmeta.get('step')}.\n")
        md.append(f"* Hindsight events in that range: {cmp_['hindsight_events']}; walk-forward events: "
                  f"{cmp_['walkforward_events']}; hindsight events also found point-in-time (within 3 bars): "
                  f"{cmp_['hindsight_matched_in_wf']} ({cmp_['match_rate'] * 100:.0f}%).")
        md.append(f"* {h}-bar mean return: hindsight {cmp_[f'hindsight_ret_{h}'] * 100:+.2f}% vs walk-forward "
                  f"{cmp_[f'walkforward_ret_{h}'] * 100:+.2f}%; hit rate {cmp_[f'hindsight_hit_{h}'] * 100:.1f}% vs "
                  f"{cmp_[f'walkforward_hit_{h}'] * 100:.1f}%; excess over random {cmp_[f'hindsight_xrand_{h}'] * 100:+.2f}% vs "
                  f"{cmp_[f'walkforward_xrand_{h}'] * 100:+.2f}%; excess over local random {cmp_[f'hindsight_xloc_{h}'] * 100:+.2f}% vs "
                  f"{cmp_[f'walkforward_xloc_{h}'] * 100:+.2f}%.")
        md.append(f"* Target-first rate: {cmp_['hindsight_target_rate'] * 100:.1f}% vs {cmp_['walkforward_target_rate'] * 100:.1f}%; "
                  f"average R: {cmp_['hindsight_avg_r']:+.2f} vs {cmp_['walkforward_avg_r']:+.2f}.\n")
        tw = summary_table(wf)
        out["walkforward_table"] = tw
        md.append("Walk-forward per pattern:\n")
        md.append(_fmt_table(tw, ["n", f"hit_{h}", f"rand_hit_{h}", f"ret_{h}", f"xrand_{h}", f"p_{h}", "target_rate", "stop_rate", "avg_r"],
                             [f"hit_{h}", f"rand_hit_{h}", f"ret_{h}", f"xrand_{h}", "target_rate", "stop_rate"], {f"p_{h}": 3, "avg_r": 2}))
    md.append("\n## Caveats\n")
    md.append("""
* Universe = today's index members (survivorship bias). The random-date baseline in the same stock is the control
  for this; the raw and SPY-adjusted numbers are inflated by it.
* No transaction costs, slippage or position sizing; overnight gap from signal close to next open is included.
* Events overlap in time and across correlated stocks, so effective sample sizes are smaller than `n` and
  p-values are optimistic. Treat borderline significance as noise.
* Many comparisons are made (patterns x horizons); with ~16 patterns, expect roughly one spurious "significant"
  result at p<0.05 by chance.
* Score is a geometric-fit measure. Calibration tells you whether it also predicts outcomes.
""")
    out["markdown"] = "\n".join(md)
    return out


def write_research_report(out_dir: Path, events: pd.DataFrame, structures: pd.DataFrame, wf: Optional[pd.DataFrame],
                          meta: Dict, h: int = 20) -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if len(events) == 0:
        (out_dir / "report.md").write_text("No events.\n")
        return out_dir / "report.md"
    parts = build_markdown(events, structures, wf, meta, h)
    (out_dir / "report.md").write_text(parts["markdown"], encoding="utf-8")
    parts["summary"].to_csv(out_dir / "summary_by_pattern.csv")
    imgs = {}
    charts = out_dir / "charts"
    charts.mkdir(exist_ok=True)
    imgs["excess"] = chart_excess(parts["summary"], h, charts / "excess.png")
    imgs["hit"] = chart_hit(parts["summary"], h, charts / "hit.png")
    if len(parts.get("calibration", [])):
        imgs["calibration"] = chart_calibration(parts["calibration"], h, charts / "calibration.png")
    imgs["year"] = chart_year(parts["by_year"], h, charts / "year.png")
    imgs["trade"] = chart_trade(parts["summary"], charts / "trade.png")
    try:
        import markdown as _md  # optional
        body = _md.markdown(parts["markdown"], extensions=["tables"])
    except Exception:
        body = "<pre style='white-space:pre-wrap'>" + html.escape(parts["markdown"]) + "</pre>"
    figs = "".join(f"<figure><img src='data:image/png;base64,{v}' alt='{k}'></figure>" for k, v in imgs.items())
    doc = ("<!doctype html><html><head><meta charset='utf-8'><title>AlgoVision research</title><style>"
           "body{font-family:system-ui,-apple-system,'Segoe UI',sans-serif;max-width:1200px;margin:24px auto;padding:0 20px;color:#0b0b0b;background:#f9f9f7}"
           "table{border-collapse:collapse;font-size:12px;margin:12px 0}td,th{border-bottom:1px solid #e1e0d9;padding:4px 8px;text-align:right}"
           "th:first-child,td:first-child{text-align:left}figure{margin:16px 0}img{max-width:100%;border:1px solid #e1e0d9}"
           "pre{font-size:12px}</style></head><body>" + body + "<h2>Charts</h2>" + figs + "</body></html>")
    (out_dir / "report.html").write_text(doc, encoding="utf-8")
    return out_dir / "report.html"
