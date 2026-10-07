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

### Context filters

The research (`docs/research_falling_wedge.md`) found that bottom-reversal patterns only carry an edge in
*beaten-down* stocks. Every match now reports its context (6-month return, distance from the 200-day MA,
ATR %) and the scanner can filter on it:

```bash
# only stocks down >8% over 6 months and below their 200-day MA
python -m algovision scan -u all -p falling-wedge,ihs --mode current --beaten-down --explain
# fine-grained: --max-6m-return -0.15 --below-ma200 --min-atr-pct 0.02
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
[`docs/research_shortterm.md`](docs/research_shortterm.md) (`--short-term`); exit rules on the tested entries (time vs take-profit, rising target, per-day threshold, trailing stop) in [`docs/research_exits.md`](docs/research_exits.md) (`python -m algovision.research.exits`); the single-pattern deep dive
(features, filters, exits, entries, portfolio, train/test split) in
[`docs/research_falling_wedge.md`](docs/research_falling_wedge.md) (`python -m algovision deepdive --pattern falling-wedge`); momentum and short-term reversal on the same universe in
[`docs/research_factors.md`](docs/research_factors.md) (`python -m algovision factors`); five further anomalies in
[`docs/research_anomalies.md`](docs/research_anomalies.md), of which one survived and has a live scan:
`python -m algovision newsday`; insider buying from SEC Form 4 data in
[`docs/research_insiders.md`](docs/research_insiders.md).

## Growth screen (`growth` command)

```bash
python -m algovision growth --top 20 --explain --max-per-sector 3
```

Long-horizon selection: revenue / EPS growth and margin trend (40 %), quality (20 %), price momentum (25 %,
the one backtested block), valuation sanity (15 %), with a one-line "why" per name and a cyclical-peak flag.
Fundamentals come from Yahoo's time-series endpoint (`algovision/data/fundamentals.py`). See
[`docs/growth_screen.md`](docs/growth_screen.md). It is a standalone command only: the daily report and the journal
no longer include it (the fundamental blocks are untested).

## Insider buying (`insiders` command)

```bash
python -m algovision insiders --days 45            # beaten-down stocks with officer/director purchases >= $100k
python -m algovision insiders --days 45 --any-regime
```

Reads Form 4 filings from EDGAR's daily index (last N days), parses open-market trades by officers and
directors, and lists purchases in beaten-down stocks, the rule that tested at +10 % vs random over 60 bars
and +15 % over 120 in both halves of 2016-2026 ([`docs/research_insiders.md`](docs/research_insiders.md)).
The daily journal logs these as `insider_buy_beaten_down` (hold 120 bars).

## Daily report (`daily-report` command)

```bash
python -m algovision journal --out journal        # refresh data, log signals, mark to market
python -m algovision daily-report --out journal   # journal/report_<date>.md from cache
```

One file with the day's insider purchases (beaten-down first), news-day and wedge signals, a summary of one
research brief per listed stock, and the running forward-test results against SPY. A scheduled routine runs both
after every US close and commits the result to `journal/`.

The briefs themselves go to `journal/briefs_<date>.md` (`algovision/briefs.py`): for every stock in the report tables,
where it is (drawdown, moving averages, RSI), why it fell (the largest down days of the last year plus every
earnings reaction that closed down, each with the evidence found: headlines that name the company and state a cause,
an 8-K filed that day or the evening before with what it was about, rating or target cuts right after, abnormal
volume, a market-wide down day; when nothing is found the brief says "not found" rather than guessing), the latest
news with summaries, what worries investors (the themes of the negative headlines of the last year, counted, each
with the headlines behind it) and a sentiment read over listed signals (analysts, targets, estimate revisions, short
interest and its monthly change, the StockTwits crowd, headline tone), what analysts say (consensus, targets,
upgrades / downgrades, estimate revisions), the last report and the estimates, the fundamentals, and a rule-based
read (signs of a bottom / undecided / still falling) whose signals are listed. Data: Yahoo Finance's quoteSummary
and news feed plus the EDGAR submissions index for 8-Ks (`algovision/data/briefs_data.py`, cached for a day), and
two key-free extras (`algovision/data/newsfeed.py`): Google News RSS search (a year of headlines per company and the
window around every large down day; Google offers the feed for personal, non-commercial feed readers) and the
StockTwits public symbol stream (the last 30 posts' bullish / bearish tags). `--no-briefs` skips it.

## Peer groups (`peers` command)

```bash
python -m algovision peers NKE AEP FICO        # --he for Hebrew, --refresh to rebuild the groups
```

`algovision/peers.py` clusters the universe by market-neutral correlation (daily log returns minus beta times the
equal-weight market, Ward clustering of the correlation distance, about one group per eight stocks) and, for every
stock, lists its five closest peers, its group, the mean correlation to the group, beta and residual volatility,
plus the 20-day divergence from the group: the stock's return minus beta times the rest of the group, as a z-score
against its own last year. The grouping is cached for a week (`peers.json` in the cache directory); the divergence
is recomputed on every run. Every brief and every section of the Hebrew wedge file carries this block, the summary
tables a *vs peers 20d* column, and the rule-based read gains +0.5 when z <= -2: in the original full-universe
scan (`research/peers/`, 1,827 liquid US stocks, 2023-2026) such stocks regained +0.65% relative to their peers
over the next 20 days (t = 2.3), while stocks stretched above their peers showed nothing. Weak evidence, used as
context rather than as a rule.

### Groups as one stock (`research-groups` command)

`algovision/research/groups.py` aggregates every peer group into an equal-weight, daily-rebalanced OHLCV basket
and runs the same falling-wedge screen on the baskets, with groups built point-in-time (the three years before each
signal's year). `python -m algovision research-groups` writes [docs/research_groups.md](docs/research_groups.md):
does a stock's wedge signal do better when its group is in the same state, and is the basket itself a signal?
Result (2016-2026, train/test split 2023): wedge signals in stocks where **most of the group's other members were
beaten down too** earned +1.2% (train) / +1.9% (test) more over 20 bars, positive in all 6 years with enough signals;
a wedge breakout of the basket itself within 10 bars added +2.3% / +1.9% (smaller samples); neither holds at 60 bars.
The basket itself being beaten down (+0.4% / +1.9%), another member signalling, or the stock sitting above its group
did not hold up. So the group state is shown as context (the *group* column of the wedge table, the peers block of
every brief, the summary line of the Hebrew wedge file), not used as a filter. The basket as an instrument is not
supported out of sample (24 test signals, excess +0.7% with a wide interval).

## Early rally in beaten-down stocks (`research-rally` command)

```bash
python -m algovision research-rally --offline      # 518 symbols, 10 years, about a minute from cache
```

Is the *start* of an up-move a tradeable short-hold entry? `algovision/research/rally.py` tests six point-in-time
definitions on every stock (close back above the 50-day MA after a stint below it, 20/50-day MA cross, first close
above the 60-bar high in a stock still 10 % under its 52-week high, a Dow turn of higher low then higher high, a +8 %
thrust in 10 bars off the 60-bar low, RSI(14) back above 50 after < 35), entry at the next open, 10 bps cost, against
the SPY and against random entries in the same stock, train before 2023 and test after. Result
([docs/research_rally.md](docs/research_rally.md), 50,829 events): in stocks that are **not** beaten down the turn rules
add little or nothing (base breakouts fail outright); in **beaten-down** stocks (below the 200-day MA, 6-month return
< -8 %) all five turn rules pass the pre-registered bar in both periods. The deployable rule is their union, one entry
per stock per 30 days: over 20 bars +2.7 % (train) / +2.2 % (test) net, hit 61 % / 58 %, +4.0 % / +3.5 % over random
entries in the same stocks (t 19 / 13), positive in all 10 years, but only +0.6 % / 0.0 % over the SPY at 20 bars and
+0.8 % / -0.4 % at 60: the rule times the stock's own turn rather than beating the index. Only the deepest declines beat
the SPY (6-month return < -30 %: +6.1 % / +4.5 % net at 20 bars, +2.5 % / +2.1 % over the SPY); two rules within a week
helps a little, volume does not matter. The daily report shows the live table (*Early rally in beaten-down stocks*, rules fired in the last
3 bars, a brief for every name) and the journal logs day-0 rows as `early_rally_beaten_down`, hold 20 bars.

## The story along the time axis (`story` command)

```bash
python -m algovision story TJX NKE --he      # five chapters per stock, Hebrew; --json for the data
```

`algovision/story.py` tells each stock's last five years as five chapters (five to two years back, two to one, one
year to six months, six months to one, the last month), each at its own resolution: the closes are cut into legs
(zig-zag swings larger than the chapter's threshold, 20 % down to 3 %), and every leg is told with what the data
recorded inside it, in date order: earnings releases (8-K item 2.02) with the reaction, EPS vs the estimate (last
four quarters) and the quarter's revenue and EPS against the year before (SEC XBRL company facts, ten years, the
fourth quarter derived from the annual figure), material 8-K events (agreement, acquisition, officer change,
restructuring, impairment) with the reaction, the largest single days of the stretch with the headline that named
the company that day (Google News, any past date) or "no headline found", the leg's volume against normal, the
S&P 500 over the same leg and, in the last year, analyst upgrades and downgrades. The five-year chapter opens with
the annual arc of revenue and EPS. Nothing is inferred: a leg with no event is told as a move with no recorded cause.
The story leads every brief (English) and every section of the Hebrew wedge file; the data that follows it is
unchanged.

## Everything in one Hebrew file (`daily_<date>.md`)

The daily report also writes `journal/daily_<date>.md` / `daily_latest.md` (`algovision/daily_he.py`): one Hebrew
file that carries what the three files above carry separately, in order: the "what is new" note, the report tables
(insiders, news-day, the falling wedge with the wedge file's extra columns, early rally), the briefs summary table,
the Jev section and the stocks it prioritised, then one full section per listed stock (the five-line summary, the
time-axis story, the wedge's technical analysis for wedge stocks, where the stock is, why it fell with the latest
news, concerns and sentiment, peers and group, the AI decision, analysts, the last report and estimates, fundamentals,
the rule-based read), and the forward-test journal with every open position. Every table row links to the stock's
section. The Hebrew "what is new" note is `new_he_<date>.md`. The Telegram job sends the Hebrew note as the message
and this one file as the document; the English report, briefs and wedge files stay on GitHub (and are sent instead
only when the Hebrew file is missing for the day).

## AI decisions (`decide` command, Jev)

```bash
python -m algovision decide                 # every brief in journal/briefs_latest.md
python -m algovision decide NKE DECK --he   # a few symbols, Hebrew labels
```

`algovision/decide.py` sends each stock's brief (and only the brief) to **Jev 1.13**, TypeSafe's typed decision
model, through OpenRouter (`POST /api/alpha/decisions`, model `typesafe/jev-1.13`; the native
`api.typesafe.ai/v1/systemone` takes the same body). Jev writes no text: it answers a fixed set of typed questions in
one pass with calibrated probabilities: the action for a one-month hold (buy / watch / skip), the kind of decline
(transitory / structural / sector-wide / corporate action / unknown), whether the drop is a corporate action or a
data artefact rather than a real decline, whether a known event is due within four weeks, whether the evidence
supports or contradicts the setup, and the severity of the news (0-3). About 0.6 s and $0.00002 per stock.

The daily report runs it automatically when an API key is present (`OPENROUTER_API_KEY`, or a file
`~/.algovision/openrouter.key`): the decision block is appended to every brief and to every section of the Hebrew
wedge file, the summary tables get an *AI* column (`!` / `⚠` = likely corporate action or data problem), section 3
of the report lists all decisions, `journal/decisions.csv` keeps every answer, and 'buy' calls with P(buy) >= 0.6 are
logged in the journal as the rule `jev_pick` (hold 20 bars) so the model is forward-tested like every other rule.
Until that test has 20+ closed trades the column is context, not a recommendation. Without a key the step is skipped.

## Delivery (`notify` command)

```bash
python -m algovision notify --file journal/report_latest.md
```

Sends a report to Telegram and/or e-mail. Channels without variables are skipped; secrets live in environment
variables, never in the repository.

* Telegram, direct: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.
* Telegram, relay: `TELEGRAM_RELAY_URL`, `TELEGRAM_RELAY_SECRET` - an HTTPS endpoint that holds the bot credentials
  and accepts `POST {"text","secret"}` / `POST {"filename","content","caption","secret"}`. Used when the direct
  variables are absent. The text is sent in <=4000-character messages and the full report as a `.md` document.
* E-mail over SMTP: `SMTP_USER`, `SMTP_PASSWORD`, optional `SMTP_HOST`, `SMTP_PORT`, `REPORT_EMAIL_TO`.

Every ticker in the daily report and the journal tables is a link to its TradingView chart
(`https://www.tradingview.com/chart/?symbol=SYM`).

What is delivered: the message text is only the short "what is new" note (`journal/new_latest.md`, written by
`daily-report`: the signals the journal logged today and the tickers that entered or left each report table
since the previous report, with TradingView links); the full report travels as an attached `.md` file and is
never sent as text. Pass `--summary` to use a different note.

## Forward test (`journal` command)

```bash
python -m algovision journal --out journal
```

Downloads fresh prices, logs today's live signals from the two rules that survived the research
(news-day in a beaten-down stock, hold 60 bars; beaten-down Falling Wedge breakout, hold 20 bars) to
`journal/signals.csv`, marks every earlier signal to market (entry = next open after the signal) and writes
`journal/<date>.md` plus `journal/latest.md` with running hit rates and mean returns against the research
expectation. A scheduled routine runs it every trading day after the US close and commits the journal.

## Project layout

```
algovision/
  core/      types (PatternMatch, DetectorConfig), pivots, geometry helpers
  data/      universe lists (bundled snapshot + refresh), price provider + cache, synthetic generators
  patterns/  one module per pattern family + registry (detect_all)
  research/  event study: events, stats, walk-forward validation, report
  scanner.py universe scanning, current/history modes, forward outcomes
  peers.py   peer groups by market-neutral correlation, divergence from the group
  decide.py  typed decisions on every brief from the Jev model (OpenRouter), forward-tested as jev_pick
  briefs.py, sentiment.py, wedge_report.py, daily_report.py, journal.py, whatsnew.py
  plotting.py, report.py, cli.py
research/peers/  the original full-universe peer scan (reference for peers.py)
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
