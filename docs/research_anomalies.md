# Beyond patterns: five pre-registered anomalies, one survivor

Tables: [`research/anomalies/`](research/anomalies/). Same universe (518 S&P 500 / NASDAQ-100 members,
2016-09 to 2026-09), same discipline: train before 2023-01-01, test after; local random baselines; costs.
The bar was set before looking: **|t| > 2 in both periods, positive net of 10 bps per side, economically
meaningful.**

| # | hypothesis | result | verdict |
|---|---|---|---|
| 1 | drift after a big news gap (PEAD proxy) | pooled: nothing (t < 1.5). **In beaten-down stocks: +6.6 % / +6.6 % over 60 days vs random, t = 7.9 / 5.7** | **passes** |
| 2 | overnight vs intraday return | overnight 13.5 %/yr (Sharpe 1.12) vs intraday 4.4 % (0.38), both periods | real but not tradeable after costs |
| 3 | turn of the month | +3 bp/day in-window vs out (t = 0.65), reversed in test | fails |
| 4a | low-volatility decile | low-vol decile 11 %/yr vs high-vol 40 %; opposite sign in both periods | fails |
| 4b | vol-managed SPY (target 15 %) | Sharpe 0.88 → 1.06, drawdown −34 % → −19 %; test 1.42 → 1.31 | drawdown tool, not alpha |
| 5 | sector-residual reversal (weekly, monthly) | weekly winners-underperform t = −4.8 train, 0.0 test; monthly nothing | fails |

## The survivor: a big news day in a beaten-down stock

Event: a stock **below its 200-day MA** opens with a **gap of at least 4 %** (either direction) on **volume of at
least 3× its 20-day average**. Trade: buy at the **next open**, hold **60 bars**. One event per stock per 5 days.
The gap and the volume are known at the close, so the signal is exactly point-in-time; no detector, no fitting.

| | n | net 60-bar return (10 bps) | hit | median | excess over SPY | excess over local random (95 % CI) | t |
|---|---|---|---|---|---|---|---|
| train 2016-22 | 921 | **+6.6 %** | 63.4 % | +5.1 % | +3.8 % | **+6.7 %** (+4.9 to +8.3) | 7.9 |
| test 2023-26 | 713 | **+7.2 %** | 62.4 % | +4.8 % | +1.2 % | **+6.6 %** (+4.4 to +8.8) | 5.7 |

* **Direction of the news does not matter.** Gap down: +7.1 % / +6.0 % (train / test); gap up: +4.7 % / +13.5 %
  (n = 196 / 116). The event is a capitulation or an inflection in a stock everyone has given up on.
* **Positive in every one of the 10 years** (worst 2018: +2.2 %, t = 1.5; 2025: +7.4 %, t = 3.8; 2026 to date:
  +6.5 %, t = 3.9). The recent years matter: survivorship has had little time to act on them.
* **It lives entirely in deeply beaten-down stocks.** With the pattern-study filter (6-month return < −8 %):
  +8.1 % / +8.3 % net, excess +9.7 % / +10.6 % (t = 8.4 / 6.6, n = 610 / 472). Without it (below the MA but not
  down 8 %): excess ≈ 0 in both periods. Bigger gaps are better (> 10 %: excess +10.8 % / +9.9 %).
* **Control**: the same trade in stocks *above* their 200-day MA is worse than random in both periods (excess
  −1.5 to −10 %). News in an uptrending stock is not an inflection.
* Horizon: the excess builds slowly (+0.2 % at 5 bars, +2.1 % at 20, +6.7 % at 60): this is a two-to-three
  month drift, not a bounce.

Equal-weight portfolio of every such event (about 160 a year, ~39 open positions with a 60-bar hold, 5 bps per trade):

| | CAGR | vol | Sharpe | max drawdown |
|---|---|---|---|---|
| news-day long, 2016-26 | 29.1 % | 26.9 % | 1.08 | −45 % |
| same trades at random nearby dates | 3.2 % | 24.0 % | 0.25 | −50 % |
| news-day long, test 2023-26 | 38.3 % | 27.9 % | 1.29 | −18 % |
| random nearby dates, test | 6.9 % | 20.2 % | 0.43 | −22 % |
| SPY, test 2023-26 | ~22 % | | 1.42 | −19 % |

The test-period portfolio returned 3.3× against 2.1× for SPY, with the same drawdown.

### Why to still be careful

* **Survivorship is at its worst exactly here.** Stocks that gapped down while already beaten-down and then
  kept falling out of the index are missing; those that survived are, by construction, the ones that recovered.
  The same-stock random baseline and the 2025-26 results (where removals have not happened yet) argue the effect
  is not only survivorship, but the absolute size (+7 %) is certainly inflated. Reproducing this on a
  point-in-time constituent list (or on all listed stocks including delistings) is the first thing to do before
  trading it at size.
* Events cluster in stressed periods (2018, 2020, 2022), so the effective sample is smaller than 1,634 and the
  drawdown of an equal-weight book is −45 %. Position sizing has to assume that.
* No stop was used; the 60-bar hold is a time exit. Expect fat tails: the median (+5 %) is below the mean.

### Use it

`python -m algovision newsday` lists today's candidates (below the 200-day MA, down > 8 % over six months, a
≥ 4 % gap on ≥ 3× volume within the last 5 bars) with entry level and bars left in the 60-bar window.

## The rest, briefly

* **Overnight vs intraday**: essentially all of the equity premium accrued overnight (close to open): universe
  13.5 %/yr overnight vs 4.4 % intraday, SPY 10.9 % vs 4.0 %, in both periods. Capturing it means two trades a
  day; at 5 bps a side that is −25 %/yr. Lesson: never be *out* overnight to avoid risk, that is where the return is.
* **Turn of the month**: 8.3 bp/day inside the window vs 5.2 outside on SPY, t = 0.65, sign flips in the test
  period. Not there in this decade.
* **Low volatility**: the opposite of the textbook anomaly in this sample. The high-vol decile made 40 %/yr
  (tech), the low-vol decile 11 %. Not tradeable in either direction with any confidence.
* **Vol-managed SPY**: scaling exposure by 15 % / realized vol cut the max drawdown from −34 % to −19 % with a
  similar return; Sharpe better in train, slightly worse in test. A risk-management tool, not an edge.
* **Sector-residual reversal**: a stock's week versus its sector. The "sector winners underperform next week"
  leg was strong until 2022 (t = −4.8) and vanished afterwards (t = 0.0). Dead, like the plain weekly reversal.

## Where this leaves the whole project

Every effect that survived has the same shape: **a stock that has already fallen a lot, and something that
marks the turn** (a slow wedge bottom, a big news day). Everything fast, everything based on the shape of the
price alone, and everything in stocks that are doing fine, has no edge. The news-day rule is the strongest
version of that one idea: +6-7 % per event over two to three months, both periods, every year, with the
survivorship caveat above.
