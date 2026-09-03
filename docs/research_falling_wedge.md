# Deep dive: Falling Wedge. Is it worth focusing on, and what around it pays?

Tables and charts: [`research/falling_wedge/`](research/falling_wedge/) (comparison set for Inverse Head &
Shoulders in [`research/inverse_head_and_shoulders/`](research/inverse_head_and_shoulders/)). Reproduce with
`python -m algovision deepdive --pattern falling-wedge`.

## Discipline

The Falling Wedge was picked because it was the best of 16 patterns. Tuning it further on the same data would
produce an edge by construction (winner's curse). So everything below is done as follows:

* **Train** = signals before 2023-01-01 (1,792 events), **test** = 2023-01 to 2026-09 (1,373 events).
* A fixed, small list of hypotheses (19 features, 8 filters, 11 exit rules, 3 entries), thresholds set on
  train, results reported for both periods. A finding counts only if it has the same sign and a meaningful size
  in both.
* `xloc` = mean 20-bar return in excess of random entries within ±6 months in the same stock and direction.

## 1. The base edge shrank out of sample, but survived

| | n | hit | 20-bar return | excess over local random (95 % CI) | avg R | profit factor |
|---|---|---|---|---|---|---|
| train (2016-22) | 1,792 | 64.6 % | +2.73 % | **+2.31 %** (+1.90 to +2.77) | +0.44 | 1.91 |
| test (2023-26) | 1,373 | 57.5 % | +1.58 % | **+0.70 %** (+0.15 to +1.19) | +0.33 | 1.64 |

Per year the excess was positive in 9 of 11 years (negative in 2018 and 2024). The edge is real but a third of
what the full-sample number suggested.

## 2. What makes it work: the wedge is an oversold-bounce detector

Seven features moved outcomes the same way in both periods (tercile T3 minus T1, thresholds from train):

| feature | train T1 → T3 | test T1 → T3 | reading |
|---|---|---|---|
| 6-month return before the signal | +4.9 % → +0.3 % | +3.2 % → −0.9 % | **the more beaten-down the stock, the better** (ρ = −0.22 / −0.19) |
| distance from 200-day MA | +4.3 % → +0.6 % | +2.7 % → −0.6 % | below the 200-day MA works, above it does not |
| ATR as % of price (volatility) | +1.2 % → +3.6 % | +0.2 % → +1.9 % | high-volatility names |
| wedge height (% of price) | +1.4 % → +3.6 % | +0.4 % → +2.5 % | big wedges, not tight ones |
| decline into the wedge | +3.3 % → +2.0 % | +1.2 % → +0.1 % | steeper preceding fall is better |
| breakout-bar close strength | +3.0 % → +1.8 % | +1.1 % → +0.1 % | a strong breakout close does *not* help |
| detector score | +2.9 % → +1.5 % | +1.1 % → +0.3 % | textbook-looking wedges do *worse* |
| SPY below its 200-day MA (binary) | +4.7 % vs +1.4 % | +5.0 % vs +0.2 % | best in weak markets (hit 70-72 %) |

Not consistent: breakout volume, volume contraction, convergence, number of touches, width, pivot scale,
apex distance, delay, gap from the line. The classical "quality" criteria of the pattern carry no information.

The same four features (6-month return, distance from 200-day MA, volatility, decline into the pattern) are
the consistent ones for the Inverse Head & Shoulders as well. Both patterns are therefore proxies for one
effect: **a bottoming structure in a stock that has already fallen a lot**. In stocks in uptrends the falling
wedge is just a pullback, and it has no edge, exactly like the flags in the main study.

## 3. Pre-registered filters (thresholds from train)

| filter | train n / yr | train excess | test n / yr | test excess (95 % CI) | test hit | test PF |
|---|---|---|---|---|---|---|
| all signals | 284 | +2.3 % | 379 | +0.7 % (+0.2 to +1.2) | 57.5 % | 1.64 |
| **6-month return < −8 %** | 95 | +4.9 % | 100 | **+3.2 % (+2.1 to +4.4)** | 60.3 % | 1.77 |
| below 200-day MA | 164 | +3.4 % | 200 | +1.7 % (+0.9 to +2.5) | 57.9 % | 1.71 |
| beaten down AND below 200-day MA | 94 | +4.9 % | 99 | +3.2 % (+2.1 to +4.3) | 60.5 % | 1.77 |
| beaten down AND high volatility | 67 | +5.4 % | 57 | +4.1 % (+2.6 to +5.8) | 59.4 % | 1.80 |
| SPY below 200-day MA | 77 | +4.7 % | 40 | +5.0 % (+3.1 to +6.9) | 70.3 % | 2.52 |
| 6-month return > +4 % (uptrend) | 95 | +0.3 % | 152 | −0.9 % (−1.7 to +0.1) | 55.4 % | 1.55 |
| above 200-day MA | 121 | +0.9 % | 179 | −0.4 % (−1.2 to +0.4) | 57.2 % | 1.56 |

The beaten-down subset was positive in **every one of the 11 years** (worst: 2018 and 2024 at +1.0 %). It keeps
~100 signals a year across the universe, about 8 open positions at any time with a 20-bar hold.

## 4. Exits and entries

* **Time exits**: return per bar is highest early (train 16 bps/bar at 10 bars, 14 at 20, 8 at 40, 7 at 60; test
  9 / 8 / 8 / 8). 20 bars is a sensible compromise; 60 bars earns more in total (+4.4 %) but slowly.
* **Targets do not help**: the pattern's measured target is reached 32 % of the time; using a target lowers the
  average R (0.39 vs 0.37-0.41) without raising it anywhere. A tight 2-ATR target lifts the hit rate to 61 % and
  lowers expectancy (R 0.23).
* **Stops**: "no target, stop at the wedge low, exit after 20 bars" has the best profit factor (train 2.30, test
  1.67, all 1.99) with 34 % of trades stopped. A 2-ATR stop is equivalent; a 3-ATR stop with 40 bars is close.
  Stops help here mostly by cutting the tail, not by improving the mean.
* **Entry**: signal-bar close is marginally better than next open (+0.1 %); waiting for a retest of the broken
  line happens in 69 % of cases and earns slightly less. No reason to wait.

## 5. Portfolio reality check (equal weight across open positions, hold 20 bars, 5 bps per trade)

| | CAGR | vol | Sharpe | max drawdown |
|---|---|---|---|---|
| all wedges, 2016-22 (train) | 28.3 % | 20.9 % | 1.31 | −33 % |
| all wedges, 2023-26 (test) | 16.1 % | 16.2 % | 1.00 | −17 % |
| same trades at random nearby dates, test | 13.8 % | 14.3 % | 0.98 | −16 % |
| SPY buy & hold, 2023-26 | ~22 % | | | |
| beaten-down subset, test | 15.2 % | 21.9 % | 0.77 | −28 % |
| beaten-down subset at random dates, test | −3.4 % | 19.4 % | −0.08 | −34 % |

The unfiltered wedge portfolio had no edge over random dates out of sample (Sharpe 1.00 vs 0.98): in the
2023-26 bull market almost any long entry in these stocks did fine. The beaten-down subset kept a large edge
over its own random baseline (+15 % vs −3 % CAGR) but still trailed SPY, because the filter concentrates in
laggards during a period when leaders led.

## Bottom line

* Focus on the Falling Wedge *as a way of finding oversold bounces*, not as a chart shape. Trade it only when
  the stock is down more than ~8 % over six months and below its 200-day MA; prefer volatile names and large
  wedges; expect it to be best in weak markets. Ignore the detector score, volume and "textbook quality".
* Rule that held out of sample: enter at the breakout close or next open, stop at the wedge low (or 2 ATR), no
  profit target, exit after ~20 bars. About +3 % per trade over a same-stock random entry, hit rate ~60 %,
  profit factor ~1.8, roughly 100 trades a year on the S&P 500 + NASDAQ-100.
* Expect ~+2-3 % excess per trade, not the +5 % the training period shows, and a 25-35 % drawdown for an
  equal-weight portfolio of these. It beats random entries in the same stocks in every year; it does not
  reliably beat holding the index in a strong bull market.
