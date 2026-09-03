# Can the setups be trusted? Findings (S&P 500 + NASDAQ-100, 2016-2026)

Full tables: [`research/full_report.md`](research/full_report.md) · per-pattern CSV:
[`research/summary_by_pattern.csv`](research/summary_by_pattern.csv) · reproduce with
`python -m algovision research --universe all --period 10y --wf-symbols 80`.

## Setup

* 518 symbols (today's S&P 500 and NASDAQ-100 members), daily bars, 2016-09 to 2026-09.
* 48,426 **confirmed** pattern events at the scanner's default `min_score = 0.6`; 16 pattern types.
* Signal bar = the later of the breakout bar and the bar at which the pattern's last swing point became
  knowable; entry at the **next open**; returns signed by the pattern's direction.
* Baselines: raw · minus SPY · minus random dates in the same stock (whole decade) · minus **local** random
  dates in the same stock within ±6 months of the signal, same direction and holding period. The local baseline
  cancels drift, survivorship *and* regime, so the verdicts use it.
* Trade simulation: exit at the measured-move target or the pattern stop (first touched), else after 60 bars.
* Look-ahead check: bar-by-bar walk-forward on 80 random symbols × last 1000 bars (4,106 events).

## Headline: pooled, the setups have no edge

| 20-bar horizon, all 48,426 events | value |
|---|---|
| hit rate (return positive in the pattern's direction) | 49.7 % |
| hit rate of local random entries | 49.8 % |
| mean return in pattern direction | −0.20 % |
| excess over SPY | −0.12 % |
| excess over local random entries (95 % CI) | **−0.31 %** (−0.40 to −0.21) |
| target hit first / stop hit first | 29 % / 56 % |
| average R, profit factor | +0.02, 1.03 |

A coin flip. The confidence interval excludes zero on the *negative* side: on average, buying breakouts and
shorting breakdowns did slightly worse than entering the same stocks on random nearby days. The gap widens with
the horizon (−0.10 % at 5 bars, −1.01 % at 60 bars): breakouts tend to **mean-revert**.

The walk-forward sample agrees: hindsight −0.12 % vs point-in-time +0.04 % mean 20-bar return, hit rate 49.0 %
vs 49.7 %, so the fast hindsight method is not flattering the results, and 84 % of hindsight events were also
found in real time within 3 bars.

## Per pattern: two groups

Excess 20-bar return over local random entries, hindsight (n) and walk-forward (n), with permutation p-values:

| pattern | hindsight xloc (n) | p | walk-forward xloc (n) | p | verdict |
|---|---|---|---|---|---|
| Falling Wedge | **+1.63 %** (3183) | 0.000 | **+1.90 %** (336) | 0.000 | edge, replicates, positive in 9 of 11 years |
| Inverse Head & Shoulders | **+0.92 %** (1728) | 0.000 | **+2.60 %** (128) | 0.000 | edge, replicates, positive in 9 of 10 years |
| Double Bottom | +0.35 % (5597) | 0.002 | +0.06 % (407) | 0.44 | small, does not replicate cleanly |
| Rising Wedge (bearish) | +0.92 % (5611) | 0.000 | +0.74 % (489) | 0.03 | "less bad than a random short"; raw return still negative, avg R −0.15 |
| Triple Bottom / Triple Top | +1.4 % / +1.2 % | 0.01 | n = 11 / 15 | – | too few events |
| Head & Shoulders | +0.05 % (1782) | 0.41 | −0.01 % (173) | 0.54 | nothing |
| Double Top | −0.20 % (6109) | 0.96 | −0.27 % (450) | 0.73 | nothing |
| Symmetrical Triangle, Rectangle | −0.15 %, −0.47 % | – | +0.17 %, +0.61 % | – | nothing |
| Ascending Triangle | −0.59 % (3163) | 1.00 | −0.05 % (244) | 0.55 | nothing |
| Descending Triangle | −1.15 % (1644) | 1.00 | −0.68 % (154) | 0.80 | worse than random |
| Bull Flag | −1.01 % (7707) | 1.00 | −0.48 % (657) | 0.85 | worse than random |
| Cup and Handle | −1.32 % (1224) | 1.00 | −1.12 % (88) | 0.91 | worse than random |
| Bear Flag | **−2.85 %** (4742) | 1.00 | −1.31 % (461) | 0.98 | clearly worse than random; stop hit 84 % of the time |

The pattern is consistent: **bottom-reversal shapes after a decline** (falling wedge, inverse head & shoulders,
to a lesser degree double bottom) carry a real, modest edge; **continuation / breakout shapes** (flags, cup &
handle, triangles) do worse than random because large-cap breakouts on daily bars mean-revert. Fading a
confirmed bear flag earned +2.9 % over 20 bars and +5.2 % over 60 bars relative to random, which is the largest
effect in the whole study.

## The score does not predict outcomes

Spearman ρ between score and excess return is −0.014. Raising the scanner threshold makes things *worse*:

| min_score | n | hit | excess over local random |
|---|---|---|---|
| 0.6 | 48,057 | 49.7 % | −0.31 % |
| 0.7 | 23,603 | 49.5 % | −0.43 % |
| 0.8 | 6,595 | 49.3 % | −0.58 % |
| 0.9 | 852 | 46.1 % | −0.76 % |

The score measures how textbook the shape looks. The most textbook shapes are the ones everybody sees, and they
resolve no better. Use the score to rank charts for reading, not to size positions.

## What helps a little

* **Breakout volume**: ≥ 1.5× the 20-bar average moves the pooled result from about −0.6 % to about −0.1 %
  and lifts the target-first rate from 19 % to 47 % (partly because those breakouts already travelled). It
  turns bear flags from −3.2 % to −0.6 %, but nothing becomes positive except the wedges, which were already positive.
* **Stops**: the median stop sits 4-6 % away on flags/triangles and 11-13 % on double tops/bottoms. With a
  reward:risk of ~3.5 the average trade still nets ~0 R, so the geometry of the measured move is not the problem;
  the direction is.
* **Forming setups**: once a shape is complete, 70-96 % of shapes that *have* a failure rule (head & shoulders
  90 %, double top 83 %, ascending triangle 70 %, descending triangle 56 %) go on to break in the expected
  direction. But the break itself does not predict what follows, so "it confirmed" is not a reason to trade.

## Caveats

* Survivorship (today's members) is controlled by the same-stock baselines but the raw numbers are inflated by it.
* No costs or slippage; the overnight gap to the next open is included in returns.
* Events overlap in time and across correlated stocks; effective sample sizes are smaller than n and p-values
  optimistic. 16 patterns × 5 horizons is a lot of comparisons; only effects that replicate in the walk-forward
  sample and are stable across years (the two wedges, inverse H&S) should be believed.
* Daily bars, US large caps, 2016-2026 (mostly a bull market with two drawdowns). Other timeframes and
  universes may behave differently and would need the same test.

## Short-horizon variant

Holding 1-5 bars and taking 1-3 % when offered does not change the conclusion: the pattern adds 2-3 bps per trade
over the same rule on random dates, which is below transaction costs. Details in [`research_shortterm.md`](research_shortterm.md).

## Falling Wedge deep dive

What makes the best pattern work and how to trade it, with a train/test split:
[`research_falling_wedge.md`](research_falling_wedge.md).

## Bottom line

Do not trust a setup because the scanner found it. As a class, the classic patterns on daily large-cap charts
have zero forecasting power at the 5-60 day horizon, and breakout-continuation patterns have negative power.
The only setups with evidence behind them are **falling wedges and inverse head & shoulders**, worth about
+1 to +2 % over a month relative to random entries, stable across years and replicated point-in-time. Treat the
rest as chart descriptions, or as candidates for the opposite trade.
