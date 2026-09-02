"""Render a PatternMatch on a candlestick chart (matplotlib, no extra deps)."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Union

import numpy as np
import pandas as pd

from algovision.core.types import PatternMatch

_COLORS = {
    "bullish": "#1f9d55",
    "bearish": "#d64545",
    "neutral": "#4a6fa5",
}


def _candles(ax, df: pd.DataFrame, x: np.ndarray) -> None:
    o = df["Open"].to_numpy(dtype=float)
    h = df["High"].to_numpy(dtype=float)
    l = df["Low"].to_numpy(dtype=float)
    c = df["Close"].to_numpy(dtype=float)
    up = c >= o
    ax.vlines(x, l, h, color=np.where(up, "#2e7d32", "#b71c1c"), linewidth=0.7, alpha=0.9)
    body_lo = np.minimum(o, c)
    body_h = np.abs(c - o)
    body_h = np.where(body_h == 0, (h - l) * 0.02 + 1e-9, body_h)
    ax.bar(x, body_h, bottom=body_lo, width=0.7, color=np.where(up, "#43a047", "#e53935"), alpha=0.9, linewidth=0)


def plot_match(df: pd.DataFrame, match: PatternMatch, path: Optional[Union[str, Path]] = None,
               context: int = 25, show: bool = False, figsize=(13, 7.5), dpi: int = 110):
    """Draw the chart window around ``match``.  Returns the matplotlib Figure.

    ``context`` extra bars are drawn on each side of the pattern so the prior
    trend and the aftermath are visible.
    """
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    n = len(df)
    lo = max(0, match.start_idx - context)
    hi = min(n - 1, match.end_idx + context)
    win = df.iloc[lo:hi + 1]
    x = np.arange(lo, hi + 1)
    color = _COLORS.get(match.direction, "#4a6fa5")

    has_vol = "Volume" in df.columns and np.isfinite(win["Volume"].to_numpy(dtype=float)).any()
    fig, axes = plt.subplots(2 if has_vol else 1, 1, figsize=figsize, dpi=dpi, sharex=True,
                             gridspec_kw={"height_ratios": [4, 1]} if has_vol else None)
    ax = axes[0] if has_vol else axes
    _candles(ax, win, x)

    # pattern span shading
    ax.axvspan(match.start_idx, match.end_idx, color=color, alpha=0.06, lw=0)

    # lines (necklines, trendlines, levels)
    for ln in match.lines:
        ls = {"solid": "-", "dashed": "--", "dotted": ":"}.get(ln.style, "-")
        ax.plot([ln.x0, ln.x1], [ln.y0, ln.y1], ls, color=color, lw=1.6, alpha=0.95)
        ax.annotate(ln.label, (ln.x1, ln.y1), fontsize=7.5, color=color, xytext=(3, 0), textcoords="offset points", va="center")

    # key points
    for kp in match.key_points:
        ax.plot(kp.idx, kp.price, "o", ms=6, mfc="white", mec=color, mew=1.6, zorder=5)
        dy = 10 if kp.price >= float(df["Close"].iloc[kp.idx]) else -14
        ax.annotate(kp.label, (kp.idx, kp.price), fontsize=8, ha="center", xytext=(0, dy), textcoords="offset points",
                    color="#222", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color, lw=0.6, alpha=0.9))

    # breakout / target / stop
    if match.breakout_idx is not None and match.breakout_price is not None:
        ax.plot(match.breakout_idx, match.breakout_price, marker="^" if match.direction == "bullish" else "v",
                color=color, ms=11, zorder=6)
        ax.annotate("breakout", (match.breakout_idx, match.breakout_price), fontsize=8, color=color,
                    xytext=(6, -12 if match.direction == "bullish" else 8), textcoords="offset points")
    if match.target is not None:
        ax.axhline(match.target, color=color, lw=1, ls="-.", alpha=0.7)
        ax.annotate(f"target {match.target:.2f}", (hi, match.target), fontsize=8, color=color, ha="right",
                    xytext=(0, 3), textcoords="offset points")
    if match.stop is not None:
        ax.axhline(match.stop, color="#888", lw=0.8, ls=":", alpha=0.8)
        ax.annotate(f"stop {match.stop:.2f}", (lo, match.stop), fontsize=7.5, color="#666", xytext=(0, 3), textcoords="offset points")

    # cosmetics
    ax.set_ylabel("Price")
    ax.grid(True, alpha=0.25)
    title = f"{match.symbol} - {match.pattern} ({match.direction}, {match.status}, score {match.score:.2f})"
    sub = f"{match.start_date or match.start_idx} to {match.end_date or match.end_idx}"
    if match.breakout_date:
        sub += f", breakout {match.breakout_date}"
    ax.set_title(f"{title}\n{sub}", fontsize=11, loc="left")
    ymin, ymax = win["Low"].min(), win["High"].max()
    extra = [v for v in (match.target, match.stop) if v is not None]
    ymin = min([ymin] + extra)
    ymax = max([ymax] + extra)
    pad = (ymax - ymin) * 0.06
    ax.set_ylim(ymin - pad, ymax + pad)
    ax.legend(handles=[Line2D([], [], color=color, lw=1.6, label="pattern geometry")], loc="upper left", fontsize=8, frameon=False)

    # date ticks
    ticks = np.linspace(lo, hi, min(8, hi - lo + 1)).astype(int)
    labels = []
    for t in ticks:
        v = df.index[t]
        labels.append(pd.Timestamp(v).strftime("%Y-%m-%d") if isinstance(v, (pd.Timestamp,)) or hasattr(v, "strftime") else str(v))
    (axes[-1] if has_vol else ax).set_xticks(ticks)
    (axes[-1] if has_vol else ax).set_xticklabels(labels, rotation=30, ha="right", fontsize=8)

    if has_vol:
        v = win["Volume"].to_numpy(dtype=float)
        c = win["Close"].to_numpy(dtype=float)
        o = win["Open"].to_numpy(dtype=float)
        axes[1].bar(x, v, width=0.7, color=np.where(c >= o, "#43a047", "#e53935"), alpha=0.6, linewidth=0)
        axes[1].set_ylabel("Volume")
        axes[1].grid(True, alpha=0.25)
        if match.breakout_idx is not None:
            axes[1].axvline(match.breakout_idx, color=color, lw=0.8, ls="--")

    # the "why" box
    why = "\n".join(f"- {r}" for r in match.reasons[:7])
    fig.text(0.01, 0.005, why, fontsize=7.2, va="bottom", ha="left", family="monospace",
             bbox=dict(boxstyle="round", fc="#fafafa", ec="#ccc", alpha=0.95))
    fig.subplots_adjust(bottom=0.27 if len(match.reasons) > 4 else 0.2, top=0.92, left=0.06, right=0.98)

    if path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def safe_filename(match: PatternMatch) -> str:
    pat = match.pattern.lower().replace(" ", "_")
    when = (match.end_date or str(match.end_idx)).replace("-", "")
    return f"{match.symbol}_{pat}_{when}_{match.status}.png"


def plot_matches(frames, matches: Sequence[PatternMatch], out_dir: Union[str, Path], context: int = 25) -> list:
    """Save one PNG per match into ``out_dir``; returns the list of paths."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for m in matches:
        df = frames.get(m.symbol) if isinstance(frames, dict) else frames
        if df is None:
            continue
        p = out_dir / safe_filename(m)
        plot_match(df, m, p, context=context)
        paths.append(p)
    return paths
