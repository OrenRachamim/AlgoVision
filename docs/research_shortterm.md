# Short-horizon exits: hold 2-3 days, take a few percent, repeat

Question: instead of waiting for the measured move, hold each setup for 1-5 bars and take 1-3 % when offered.
Does taking many small profits turn the setups into an edge?

Tables: [`research/shortterm/`](research/shortterm/) (pooled grid at 0 and 5 bps, per pattern, per direction,
per year, cost sensitivity, hindsight and walk-forward). Reproduce with
`python -m algovision research --universe all --period 10y --short-term`.

## Setup

* Same 48,426 confirmed-pattern events (518 symbols, 2016-2026) and the 4,106 point-in-time walk-forward events.
* Entry at the next open. Grid: hold 1 / 2 / 3 / 5 bars × take-profit 1 % / 2 % / 3 % / none × stop none / 2 % / 3 %.
* Fills: take-profit at the target (or at the open when the bar gaps through it, which is better); stop at the
  stop (or at the open when the bar gaps through it, which is worse); stop wins when both are touched in one bar.
* Round-trip cost 5 bps subtracted from every trade (0 and 10 bps also reported).
* Control: the **same exit rules on random dates within ±6 months in the same stock and direction** (10 per
  event). This is essential here, because a take-profit rule by itself manufactures a high hit rate.

## Answer: no

Pooled, no-stop rows, 5 bps cost (hindsight; walk-forward in brackets):

| hold | take | hit rate | random hit rate | net / trade | random net / trade | excess | profit factor |
|---|---|---|---|---|---|---|---|
| 1 | 1 % | 60.5 % | 58.2 % | −0.02 % | −0.05 % | +0.03 % (+0.05 %) | 0.97 |
| 2 | 1 % | 68.7 % | 66.5 % | −0.01 % | −0.04 % | +0.03 % (+0.05 %) | 0.99 |
| 2 | 2 % | 55.9 % | 54.3 % | −0.01 % | −0.04 % | +0.03 % (+0.02 %) | 0.99 |
| 3 | 1 % | 73.0 % | 71.4 % | −0.02 % | −0.04 % | +0.02 % (+0.06 %) | 0.97 |
| 3 | 2 % | 58.8 % | 57.6 % | −0.04 % | −0.04 % | −0.00 % (+0.02 %) | 0.97 |
| 5 | 1 % | 78.2 % | 77.2 % | −0.04 % | −0.02 % | −0.01 % (+0.05 %) | 0.95 |
| 5 | 2 % | 63.9 % | 63.0 % | −0.05 % | −0.02 % | −0.03 % (+0.00 %) | 0.96 |

Three things to read off this table:

1. **The high hit rate is the exit rule, not the pattern.** "Take 1 % within 3 days" wins 73 % of the time on
   pattern signals and 71 % of the time on random days in the same stocks. A tight take-profit converts a
   zero-mean process into many small wins and fewer, larger losses; the expectancy does not change.
2. **The pattern adds 2-3 basis points per trade** (statistically significant with n = 48k, and the same
   magnitude in the walk-forward sample). That is real but tiny: the first day or two after a confirmed
   breakout carries a little continuation, and it is gone by day 3-5 (at 5 bars with no target the excess is
   −0.09 %, i.e. the mean reversion from the main study begins).
3. **Costs decide the sign.** Hold 2 / take 2 %: +0.04 % per trade at 0 bps, −0.01 % at 5 bps, −0.06 % at 10 bps.
   Five basis points round trip is optimistic for a retail account (spread + slippage + commission); at
   realistic costs every cell of the grid is negative and the profit factor is below 1.

Adding a stop makes it worse in every cell (a 2 % stop is hit on 20-45 % of trades and costs 5-15 bps per trade
of expectancy), because stops at this horizon mostly get hit by noise.

## Per pattern (hold 2, take 2 %, no stop, 5 bps)

| pattern | n | net / trade | excess over random | p | walk-forward excess (n) |
|---|---|---|---|---|---|
| Falling Wedge | 3182 | **+0.20 %** | +0.21 % | 0.000 | +0.14 % (335) |
| Rising Wedge (short) | 5609 | +0.01 % | +0.15 % | 0.000 | +0.10 % (488) |
| Symmetrical Triangle | 3677 | +0.06 % | +0.08 % | 0.010 | +0.14 % (358) |
| Head & Shoulders | 1780 | −0.04 % | +0.08 % | 0.054 | +0.08 % (173) |
| Double Top | 6105 | −0.08 % | +0.05 % | 0.026 | +0.10 % (449) |
| Double Bottom, Inverse H&S, Rectangle, Cup & Handle, Ascending Triangle | | ≈ 0 | ≈ 0 | n.s. | ≈ 0 |
| Bull Flag | 7705 | −0.06 % | −0.10 % | 1.000 | +0.06 % (657) |
| Bear Flag | 4740 | −0.14 % | −0.07 % | 0.974 | −0.11 % (461) |

Only the Falling Wedge earns anything after costs at this horizon (+0.20 % per trade, profit factor 1.28, hit
59 %, and +0.14 % in the walk-forward sample with a CI that includes zero). Per year the pooled strategy is
positive in 2018, 2020, 2022 (high-volatility years) and flat or negative otherwise: what little short-term
continuation exists is a volatility effect.

## Practical reading

* Taking small profits quickly does not create an edge; it changes the *shape* of the P&L (many small wins,
  occasional larger losses) without changing its mean, and it multiplies the number of times you pay the spread.
* The 2-3 bps of genuine day-one continuation is smaller than any realistic transaction cost, so it can only be
  harvested by someone trading at near-zero cost, and even then it is ~+0.04 % per trade.
* If you want the short horizon anyway: Falling Wedge only, hold 1-2 bars, 1-2 % target, no stop, and expect
  about +0.1-0.2 % per trade before slippage.

## Caveats

Same as the main study (survivorship controlled by the same-stock baseline; overlapping events; many
comparisons), plus: daily bars cannot show intraday sequencing inside a bar, so "target before stop" within one
bar is resolved conservatively in favour of the stop, and gap-through fills are approximated by the open.
