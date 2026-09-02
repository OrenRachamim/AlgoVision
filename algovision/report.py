"""Self-contained HTML report with embedded charts and explanations."""

from __future__ import annotations

import base64
import datetime as dt
import html
from pathlib import Path
from typing import Dict, Optional, Sequence, Union

import pandas as pd

from algovision.core.types import PatternMatch
from algovision.plotting import plot_match

_CSS = """
body{font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;margin:0;background:#f5f6f8;color:#222}
header{background:#1d2b3a;color:#fff;padding:18px 28px}header h1{margin:0;font-size:20px}header p{margin:4px 0 0;opacity:.8;font-size:13px}
main{padding:20px 28px;max-width:1400px;margin:auto}
table.summary{border-collapse:collapse;width:100%;font-size:13px;background:#fff;margin-bottom:28px}
table.summary th,table.summary td{border-bottom:1px solid #e4e6ea;padding:6px 8px;text-align:left}
table.summary th{background:#eef1f5;position:sticky;top:0}
.bullish{color:#1f9d55;font-weight:600}.bearish{color:#d64545;font-weight:600}.neutral{color:#4a6fa5;font-weight:600}
.card{background:#fff;border:1px solid #e4e6ea;border-radius:8px;padding:16px;margin-bottom:22px}
.card h2{margin:0 0 6px;font-size:17px}.card .meta{font-size:13px;color:#555;margin-bottom:10px}
.card img{max-width:100%;border:1px solid #eee}
.why{font-size:13px;margin:10px 0 0;padding-left:18px}.why li{margin:3px 0}
.badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;background:#eef1f5;margin-left:6px}
.outcome{font-size:12.5px;color:#444;margin-top:8px}
"""


def _pct(v) -> str:
    return "" if v is None else f"{v * 100:+.1f}%"


def _img_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def write_report(frames: Dict[str, pd.DataFrame], matches: Sequence[PatternMatch], out_path: Union[str, Path],
                 title: str = "AlgoVision pattern scan", charts: bool = True, context: int = 25,
                 chart_dir: Optional[Path] = None, max_charts: int = 200) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    chart_dir = Path(chart_dir) if chart_dir else out_path.parent / "charts"
    rows = []
    for m in matches:
        cls = m.direction
        rows.append(
            f"<tr><td><b>{html.escape(m.symbol)}</b></td><td>{html.escape(m.pattern)}</td>"
            f"<td class='{cls}'>{m.direction}</td><td>{m.status}</td><td>{m.score:.2f}</td>"
            f"<td>{m.start_date or m.start_idx}</td><td>{m.end_date or m.end_idx}</td>"
            f"<td>{m.breakout_date or ''}</td><td>{'' if m.level is None else f'{m.level:.2f}'}</td>"
            f"<td>{'' if m.target is None else f'{m.target:.2f}'}</td>"
            f"<td>{'' if m.last_close is None else f'{m.last_close:.2f}'}</td>"
            f"<td>{_pct(m.outcome.get('ret_20'))}</td></tr>"
        )
    cards = []
    for i, m in enumerate(matches):
        img = ""
        df = frames.get(m.symbol)
        if charts and df is not None and i < max_charts:
            p = chart_dir / f"{i:04d}_{m.symbol}_{m.pattern.replace(' ', '_')}.png"
            plot_match(df, m, p, context=context)
            img = f"<img src='data:image/png;base64,{_img_b64(p)}' alt='chart'>"
        why = "".join(f"<li>{html.escape(r)}</li>" for r in m.reasons)
        outcome = ""
        if m.outcome:
            bits = []
            for k in ("ret_5", "ret_10", "ret_20", "ret_40"):
                if m.outcome.get(k) is not None:
                    bits.append(f"+{k[4:]} bars: {m.outcome[k] * 100:+.1f}%")
            if "target_hit" in m.outcome:
                bits.append("target hit" if m.outcome["target_hit"] else "target not hit")
            if "max_favorable" in m.outcome:
                bits.append(f"best {m.outcome['max_favorable'] * 100:+.1f}% / worst {m.outcome['max_adverse'] * 100:+.1f}%")
            if bits:
                outcome = "<div class='outcome'><b>What happened next:</b> " + ", ".join(bits) + "</div>"
        cards.append(
            f"<div class='card'><h2>{html.escape(m.symbol)} - {html.escape(m.pattern)}"
            f"<span class='badge {m.direction}'>{m.direction}</span><span class='badge'>{m.status}</span>"
            f"<span class='badge'>score {m.score:.2f}</span></h2>"
            f"<div class='meta'>{m.start_date or m.start_idx} to {m.end_date or m.end_idx}"
            + (f", breakout {m.breakout_date} @ {m.breakout_price:.2f}" if m.breakout_date else "")
            + (f", level {m.level:.2f}" if m.level is not None else "")
            + (f", target {m.target:.2f}" if m.target is not None else "")
            + (f", stop {m.stop:.2f}" if m.stop is not None else "")
            + f"</div>{img}<ul class='why'>{why}</ul>{outcome}</div>"
        )
    doc = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title><style>{_CSS}</style></head><body>"
        f"<header><h1>{html.escape(title)}</h1><p>{len(matches)} matches across {len(frames)} symbols - generated "
        f"{dt.datetime.now():%Y-%m-%d %H:%M}</p></header><main>"
        "<table class='summary'><thead><tr><th>Symbol</th><th>Pattern</th><th>Bias</th><th>Status</th><th>Score</th>"
        "<th>Start</th><th>End</th><th>Breakout</th><th>Level</th><th>Target</th><th>Last</th><th>+20b</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table>{''.join(cards)}</main></body></html>"
    )
    out_path.write_text(doc, encoding="utf-8")
    return out_path
