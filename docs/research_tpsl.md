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
