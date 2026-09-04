# "Enter any day above the 200-day MA, take +2 %, stop at −20 %"

Tested exactly as stated on 514 symbols, 2016-2026: entry at the next open on every 5th eligible day
(149,568 trades), take-profit filled at the target (or the open when the bar gaps through it), stop at the
stop (or the open when it gaps through), 250-bar time limit, 5 bps per trade. Code: `algovision/research/tpsl.py`;
grid: [`research/tpsl/grid.csv`](research/tpsl/grid.csv).

## What the rule does

| | value |
|---|---|
| trades | 149,568 |
| hit rate | **93.5 %** |
| stop hit | 5.8 % (average loss −19.0 %) |
| average win | +2.1 % |
| mean return per trade | **+0.73 %** (median +1.95 %) |
| mean holding time | **15.9 days** (median 5, 90th percentile 42; stopped trades average 56 days) |
| return per day of capital | **4.6 bp** (≈ 12 % a year) |
| buy-and-hold of the same stocks over the same days | 4.8 bp per day |
| profit factor | 1.58 |

The hit rate is real and the expectancy is real, but the two are unrelated to "1 % a day":

1. **A 93 % hit rate is bought with a −20 % loss on the other 7 %.** Ten wins of +2 % are wiped out by one stop.
   Net: +0.73 % per trade.
2. **Capital is tied up.** The average trade takes 16 days, and the losers take 56. The +0.73 % per trade over
   15.9 days is 4.6 bp a day, which is exactly the drift of the stocks themselves (4.8 bp a day for holding the
   same stocks over the same days). The exit rule moves returns between the "many small wins" bucket and the
   "rare big loss" bucket; it does not create any.
3. **Every cell of the take-profit / stop grid says the same.** From TP 1 % to 10 % and SL 5 % to none, the
   return per day of capital stays between 0 and 5.3 bp, and the best cells are the ones with *no stop* (5 bp),
   i.e. plain buy-and-hold. Tight stops only lower it (TP 1 % / SL 5 %: 0.1 bp a day).
4. **2018 and 2022 (down years) were flat or negative** (+0.01 % and −0.16 % per trade), because the stops
   cluster there: 9-10 % of trades stopped.
5. **The "above the 200-day MA" filter does not help**: the same rule below the MA earned 7.6 bp a day (the
   beaten-down bounce again), with no filter 5.2 bp.

Capital-constrained portfolio (20 slots, every free slot buys a random eligible stock, 2016-2026):

| | annual return | Sharpe | max drawdown | 2023-26 annual |
|---|---|---|---|---|
| TP 2 % / SL 20 % | 11.5 % | 0.79 | −28 % | 11.5 % |
| TP 2 % / no stop | 14.7 % | 0.82 | −35 % | 17.1 % |
| TP 5 % / SL 20 % | 15.0 % | 0.96 | −32 % | 12.9 % |
| SPY buy & hold | 15.1 % | 0.85 | −34 % | 22.4 % |

## The arithmetic of "1 % a day"

1 % a day compounds to ×12 a year. To earn it with +2 % exits, every unit of capital would have to complete a
winning trade every two days with no losers. In reality a winner takes 13 days on average and 5.8 % of trades
lose 19 %. The strategy earns what the market pays for holding stocks, about 5 bp a day, paid out in a
psychologically pleasant shape. There is no exit rule that changes that number; only the entry can, and this
project has measured which entries do (see the news-day and beaten-down findings): a few percent per trade,
not per day.

## By stock type and by parameters

Every 10th day of every stock is an entry (115,444 trades per cell, no filter), each trade tagged with the stock's
state at entry; 25 cells (take-profit 1/2/3/5/10 % × stop 5/10/20/50 %/none). Full table:
[`research/tpsl/groups_grid.csv`](research/tpsl/groups_grid.csv). Numbers are **return per day of capital (bp)**,
and in brackets the **edge over holding the same stock for the same days** (bp/day).

| stock type | TP 2 / SL 20 | TP 5 / SL 20 | TP 5 / no stop | TP 10 / no stop | B&H same days |
|---|---|---|---|---|---|
| all | 5.2 (−0.3) | 5.4 (−0.2) | 6.0 (−0.1) | 5.8 (0.0) | 5.6-6.0 |
| above 200-day MA | 4.3 (−0.2) | 4.7 (−0.1) | 5.3 (0.0) | 5.1 (0.0) | 5.1 |
| below 200-day MA | 6.0 (−0.5) | 5.8 (−0.2) | 6.4 (−0.1) | 6.0 (−0.1) | 6.5 |
| beaten-down (below MA, 6m < −8 %) | 9.2 (−0.6) | 8.9 (−0.3) | 9.0 (−0.1) | 8.5 (0.0) | 9.8 |
| high volatility tercile | 11.3 (−0.7) | 10.9 (−0.5) | 10.6 (−0.2) | 9.9 (−0.1) | 12.0 |
| low volatility tercile | 3.2 (−0.2) | 3.6 (0.0) | 4.2 (0.0) | 4.1 (0.0) | 3.4 |
| 6-month losers | 7.6 (−0.5) | 7.4 (−0.3) | 7.8 (−0.1) | 7.3 (0.0) | 8.1 |
| 6-month winners | 4.5 (−0.2) | 5.0 (−0.1) | 5.6 (0.0) | 5.6 (0.0) | 4.7 |
| NASDAQ-100 | 6.5 (−0.8) | 7.4 (−0.4) | 8.1 (−0.2) | 8.0 (−0.1) | 7.3 |
| S&P-only | 4.9 (−0.2) | 5.1 (−0.1) | 5.6 (−0.1) | 5.4 (0.0) | 5.1 |
| Information Technology | 6.3 | 7.5 | 8.6 | 8.6 | 8.9 |
| Consumer Staples | 4.2 | 3.7 | 4.1 | 3.6 | 3.9 |
| Energy | 3.2 | 4.6 | 4.1 | 4.5 | 4.3 |

Three facts hold in every row, every sector, every cell:

1. **The edge over buy-and-hold is never positive.** All 125 group × cell combinations sit between −7 and
   +0.1 bp/day. Tight stops are the most expensive (TP 1 % / SL 5 %: −2 bp/day overall, −7 bp/day in
   high-volatility stocks, where a 5 % stop is hit by noise 40 % of the time). "No stop" is always the best
   column, i.e. the closer the rule gets to plain holding, the better it does.
2. **Differences between stock types are differences in drift, not in the rule.** Beaten-down stocks earn
   9 bp/day under the rule because they earn 10 bp/day when simply held (the bounce found in the pattern
   study); high-volatility stocks 11 vs 12; low-volatility 3-4 vs 3. The rule tracks the stock's own drift
   minus a small toll.
3. **Hit rates are the same everywhere** (93-94 % for TP 2 / SL 20 in every group) and say nothing about
   profit: the low-volatility group has the same hit rate as the high-volatility group and a third of the return.

Out of sample: in 2023-26 the beaten-down group's edge over holding turned marginally positive (+0.2 to +0.4
bp/day, from −0.7 to −1.3 in 2016-22), which is noise around zero, not a finding.

**Conclusion:** there is no stock type and no take-profit / stop-loss pair for which the exit rule earns more than
holding the stock. Picking *which* stocks to hold (beaten-down, high volatility, tech) moves the return per day
from 3 to 11 bp; picking *how* to exit moves it by at most −2 bp. The only thing a stop does is cap the size of a
single loss, at a price of 0.2-2 bp a day, which is a reasonable insurance premium to pay but not a source of
return.
