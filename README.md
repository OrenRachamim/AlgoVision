# AlgoVision

**Visual chart-pattern detection and scanning for US stocks (S&P 500 / NASDAQ-100).**

AlgoVision reads a price chart the way a technical analyst does: it finds the
swing highs and lows, checks their geometry against the textbook definition
of each setup, and reports **which pattern**, **where** (start, end, breakout),
**how confident** it is, and **why** in plain English. It scans whole index
universes for setups that are forming *right now* and for every historical
occurrence, annotated with what happened afterwards.

<div dir="rtl">

## בקצרה (עברית)

מערכת בפייתון שסורקת מניות בארה"ב (S&P 500 ו-NASDAQ-100), מזהה תבניות גרפיות
מקובלות במסחר טכני (ראש וכתפיים, כוס וידית, דאבל טופ/בוטום, משולשים, טריזים,
דגלים, מלבן) ומסבירה לכל התאמה: איזו תבנית, איפה על הגרף (תאריכים, נקודות
מפתח, קו צוואר/קו מגמה, פריצה), ציון ביטחון, יעד וסטופ, ו**למה** המניה מתאימה
לתבנית. עובדת גם על ההווה (סטאפים שנבנים או שנפרצו לאחרונה) וגם על העבר
(כל המופעים ההיסטוריים, כולל מה קרה אחרי הפריצה). הפלט: טבלה, CSV/JSON,
גרפים מסומנים (PNG) ודוח HTML.

</div>

---

## Supported patterns

| Pattern | Bias | Confirmation |
|---|---|---|
| Head and Shoulders | bearish | close below the neckline |
| Inverse Head and Shoulders | bullish | close above the neckline |
| Double Top / Triple Top | bearish | close below the trough(s) |
| Double Bottom / Triple Bottom | bullish | close above the peak(s) |
| Cup and Handle | bullish | close above the rim after the handle |
| Inverted Cup and Handle | bearish | close below the rim |
| Ascending Triangle | bullish | close above the flat top |
| Descending Triangle | bearish | close below the flat bottom |
| Symmetrical Triangle | breakout direction | close outside either line |
| Rising Wedge | bearish | close below the lower line |
| Falling Wedge | bullish | close above the upper line |
| Bull Flag / Bear Flag | continuation | close outside the flag channel |
| Rectangle | breakout direction | close outside the range |

Every match carries a `status`:

* `forming` – the structure is complete but the confirming break has not happened yet (a live setup),
* `confirmed` – the break happened (with the breakout bar, price and volume),
* `failed` – price invalidated the setup before confirming,
* `expired` – the setup went stale without a break.

## Installation

```bash
git clone https://github.com/OrenRachamim/AlgoVision.git
cd AlgoVision
pip install -e .          # or: pip install -r requirements.txt
```

Python 3.9+; depends on numpy, pandas, scipy, matplotlib, requests. Price
data comes from Yahoo Finance's public chart endpoint (queried directly, so
it works behind most proxies); `yfinance` is used as a fallback if installed.
Downloads are cached in `~/.algovision/cache` (override with `ALGOVISION_CACHE`).

## Quick start

```bash
# what does the system detect?
python -m algovision patterns

# run all detectors on synthetic textbook charts (no network) -> out/demo/demo.html
python -m algovision demo --out out/demo --explain

# analyse specific symbols: every pattern in the last 2 years + live setups,
# with one annotated PNG per match and a self-contained HTML report
python -m algovision analyze AAPL NVDA MSFT --period 2y --mode all \
    --charts out/charts --report out/report.html --explain

# scan the S&P 500 for setups forming now / confirmed in the last 15 bars
python -m algovision scan --universe sp500 --mode current --min-score 0.7 \
    --csv out/sp500_current.csv --report out/sp500_current.html

# scan NASDAQ-100 for cup & handle and head & shoulders only
python -m algovision scan -u nasdaq100 -p cup,hs,ihs --mode current --explain

# history: every past occurrence with forward returns / target hit
python -m algovision history TSLA --period 5y --patterns bull-flag,double-bottom --csv out/tsla_hist.csv
```

Example console output (columns trimmed):

```
symbol            pattern direction    status  score      start        end   breakout   level  target  ret_20  target_hit
  TSLA Ascending Triangle   bullish confirmed  0.815 2025-05-29 2025-08-22 2025-08-22  338.58  431.85  +27.7%        True
  NVDA      Double Bottom   bullish confirmed  0.900 2026-06-29 2026-08-05 2026-08-05  214.39  238.88   +2.4%       False
  NVDA         Double Top   bearish   forming  0.741 2026-08-17 2026-09-02        NaN  207.25  185.31     NaN        None
```

With `--explain` each match prints its reasoning, e.g.

```
NVDA: Double Bottom (bullish, confirmed, score 0.90) 2026-06-29 -> 2026-08-05, breakout 2026-08-05 @ 219.22, target 238.88
  - 2 troughs at 189.80, 190.01 within 0.1% of each other (tolerance 3.5%)
  - Pullback between the troughs is 12.9% deep (minimum 3%)
  - Troughs are 21+ bars apart (minimum 8)
  - Price fell 8.9% into the pattern (prior trend present)
  - Confirmed: close 219.22 broke the resistance at 214.39 at bar 481
  - breakout volume 1.2x the 20-bar average
  - Measured move: 24.49 projected from 214.39 -> target 238.88 (+9.0%)
  outcome after breakout: +5b: +1.9%, +10b: -0.8%, +20b: +2.4%, target not hit
```

### Scan modes

* `--mode current` – setups whose structure ended within `--recent-bars`
  (default 15) bars: still `forming`, or `confirmed` by a fresh breakout.
* `--mode history` – every occurrence in the window; confirmed ones get an
  `outcome` (returns 5/10/20/40 bars after the breakout, max favourable/adverse
  excursion, whether the measured-move target or the stop was hit).
* `--mode all` – both.

### Outputs

* console table, `--explain` for the full reasoning,
* `--csv` flat table (one row per match, `why` column with all reasons),
* `--json` full match objects (key points, lines, metrics, component scores),
* `--charts DIR` one annotated candlestick PNG per match,
* `--report FILE.html` self-contained HTML report with embedded charts.

### Using your own data

```bash
python -m algovision analyze XYZ --csv-dir ./my_prices     # reads ./my_prices/XYZ.csv
```

CSV needs `Date, Open, High, Low, Close[, Volume]` columns (case-insensitive).
`--offline` uses the cache only.

## Python API

```python
from algovision import detect_all, Scanner, DetectorConfig
from algovision.data.provider import DataProvider
from algovision.data.universe import get_universe
from algovision.plotting import plot_match

provider = DataProvider()
df = provider.get("AAPL", period="3y")
for m in detect_all(df, symbol="AAPL", patterns=["cup", "hs", "ihs"]):
    print(m.explanation())
    plot_match(df, m, f"out/{m.symbol}_{m.pattern}_{m.end_date}.png")

# universe scan
scanner = Scanner(provider, DetectorConfig(min_score=0.7), period="1y")
result = scanner.scan(get_universe("nasdaq100"), mode="current")
print(result.to_frame().head(20))
```

`PatternMatch` fields: `symbol, pattern, direction, status, score, start/end
(idx + date), breakout (idx/date/price), level, target, stop, key_points,
lines, reasons, metrics, outcome`.

## How detection works

1. **Swing points.** `core/pivots.py` finds alternating swing highs/lows
   (`scipy.signal.argrelextrema` with a window `order`), then removes swings
   smaller than `max(1 ATR, 1% of price)` zig-zag style. Detection runs at
   several scales (`pivot_orders = 3, 5, 8, 13`) so small and large
   structures are both seen; duplicates across scales are merged.
2. **Geometry rules.** Each detector expresses the textbook definition as
   checks on the pivot sequence: e.g. head & shoulders = `H L H L H` with the
   middle high the most prominent, shoulders within 6 %, a near-flat neckline,
   time symmetry and a prior uptrend. Triangles/wedges/rectangles fit lines to
   the highs and to the lows and classify by normalised slopes and
   convergence. Cups fit a parabola to the price path between two level rims
   and look for a shallow handle. Flags look for a sharp pole and a tight,
   near-parallel counter-trend channel.
3. **Confirmation.** The detector then searches forward for the confirming
   close (neckline / trendline / rim / range break), or marks the setup
   `forming`, `failed` or `expired`.
4. **Scoring.** Each check contributes a 0-1 component (how close to ideal),
   combined with fixed weights plus volume behaviour (contracting during the
   pattern, expanding on the breakout). `score` is the weighted mean;
   `metrics["components"]` exposes the parts.
5. **Explanation.** Every check also emits a sentence with the concrete
   numbers, which becomes the `reasons` list, the `--explain` text, the chart
   annotation and the HTML report.
6. **De-duplication.** Same-pattern matches on the same bars keep the best
   score; different patterns with a high intersection-over-union are reduced
   to the most specific interpretation (a cup with level rims is also a
   "double top"; the cup wins).

All tolerances live in `DetectorConfig` (`algovision/core/types.py`) and can be
overridden from a JSON file with `--config`.

## Can the setups be trusted? (`research` command)

The scanner tells you *what* it sees; the research module tells you whether
that has predicted anything. It runs an event study over a whole universe and
writes a report (`report.md`, `report.html`, charts, `events.csv`):

```bash
python -m algovision research --universe all --period 10y --out out/research --wf-symbols 80
```

Method, in short:

* every **confirmed** pattern is an event; the signal bar is the later of the
  breakout and the bar at which the last swing point became knowable, entry is
  the **next open** (no look-ahead);
* forward returns at 5/10/20/40/60 bars, **signed by the pattern's direction**,
  compared with three baselines: raw, minus SPY, and minus **random-date
  entries in the same stock and direction** (this cancels drift and the
  survivorship bias of using today's index members);
* permutation p-values and bootstrap CIs for the excess return, Wilson CIs for
  hit rates, a target/stop trade simulation in R-multiples, score calibration,
  stability by year, breakout-volume and other conditional views;
* a **walk-forward** re-run (bar-by-bar, past data only) on a random subsample,
  compared with the fast hindsight method to quantify any remaining look-ahead
  bias;
* the "forming" question: once a shape is complete, how often does it confirm,
  fail or expire?

The findings of the study run on 2016-2026 data are summarised in
[`docs/research.md`](docs/research.md); the short-horizon variant (hold 1-5 bars, take-profit) in
[`docs/research_shortterm.md`](docs/research_shortterm.md) (`--short-term`); the single-pattern deep dive
(features, filters, exits, entries, portfolio, train/test split) in
[`docs/research_falling_wedge.md`](docs/research_falling_wedge.md) (`python -m algovision deepdive --pattern falling-wedge`).

## Project layout

```
algovision/
  core/      types (PatternMatch, DetectorConfig), pivots, geometry helpers
  data/      universe lists (bundled snapshot + refresh), price provider + cache, synthetic generators
  patterns/  one module per pattern family + registry (detect_all)
  research/  event study: events, stats, walk-forward validation, report
  scanner.py universe scanning, current/history modes, forward outcomes
  plotting.py, report.py, cli.py
tests/       pytest suite (synthetic textbook patterns, scanner, provider, CLI)
```

## Tests

```bash
pytest -q
```

## Disclaimer

This is analysis tooling, not investment advice. Pattern recognition is
heuristic; scores express geometric fit, not probability of profit. Always
validate on the `history` mode outcomes before trading any setup.
