"""Minimal end-to-end example: scan the NASDAQ-100 for live setups and plot the best ones.

    python examples/quick_scan.py
"""

from pathlib import Path

from algovision import DetectorConfig, Scanner
from algovision.data.provider import DataProvider
from algovision.data.universe import get_universe
from algovision.plotting import plot_match
from algovision.report import write_report

out = Path("out/example")
out.mkdir(parents=True, exist_ok=True)

scanner = Scanner(DataProvider(), DetectorConfig(min_score=0.7), period="1y")
result = scanner.scan(get_universe("nasdaq100"), mode="current")

print(result.to_frame().drop(columns=["why"]).head(25).to_string(index=False))
for m in result.matches[:10]:
    print()
    print(m.explanation())
    plot_match(result.frames[m.symbol], m, out / f"{m.symbol}_{m.pattern.replace(' ', '_')}.png")

write_report(result.frames, result.matches, out / "nasdaq100_current.html", title="NASDAQ-100 live setups")
print(f"\nreport: {out / 'nasdaq100_current.html'}")
