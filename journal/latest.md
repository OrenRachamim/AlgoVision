# Forward-test journal - 2026-11-23

Data through 2026-11-23; 518 of 518 symbols loaded.

## New signals today (4)

| rule                      | symbol                                               | signal_date   |   ref_price |   hold_bars | note                                                                |
|:--------------------------|:-----------------------------------------------------|:--------------|------------:|------------:|:--------------------------------------------------------------------|
| newsday                   | [TPL](https://www.tradingview.com/chart/?symbol=TPL) | 2026-11-23    |      258.07 |          60 | gap +4.8%, vol 3.7x, 6m -35%, vs MA200 -35%                         |
| falling_wedge_beaten_down | [ARM](https://www.tradingview.com/chart/?symbol=ARM) | 2026-11-23    |      176.67 |          20 | score 0.63, stop 142.06, level 171.43                               |
| insider_buy_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX) | 2026-11-20    |      139.25 |         120 | 1 buy(s) $0.20M @ 140.03, 6m -12%, vs MA200 -7%; PINTOFF CRAIG ADAM |
| early_rally_beaten_down   | [APO](https://www.tradingview.com/chart/?symbol=APO) | 2026-11-23    |      116.94 |          20 | golden_20_50; day +5.2%, 10d -3.8%, 6m -9%, vs MA200 -3%            |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      137 |      101 | +3.74% | 71%   | +7.31%   | +0.14%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       39 |       33 | +1.81% | 61%   | +4.05%   | -2.09%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       21 |        0 | -0.23% | 38%   | +3.49%   | +1.61%             |
| jev_pick                  | untested (forward test only)                     |       76 |       33 | -0.77% | 47%   | +2.33%   | -1.34%             |
| jev_skip                  | untested; a fall is the success case             |       16 |        6 | +0.50% | 38%   | +5.35%   | +2.45%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       54 |        0 | -3.69% | 42%   | +0.91%   | -4.03%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 137, closed: 101, open: 36
- closed trades: mean +6.25%, median +6.76%, hit 81%, best +34.5%, worst -25.6%
- open trades mark-to-market: mean -3.53%, hit 43%
- SPY over the same holding periods: mean -3.58% (excess +7.31%)
- beaten-down basket over the same holding periods: mean +3.59% (excess +0.14%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 39, closed: 33, open: 6
- closed trades: mean +2.28%, median +3.72%, hit 64%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean -1.32%, hit 40%
- SPY over the same holding periods: mean -2.25% (excess +4.05%)
- beaten-down basket over the same holding periods: mean +3.89% (excess -2.09%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 21, closed: 0, open: 21
- open trades mark-to-market: mean -0.23%, hit 38%
- SPY over the same holding periods: mean -3.72% (excess +3.49%)
- beaten-down basket over the same holding periods: mean -1.83% (excess +1.61%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 76, closed: 33, open: 43
- closed trades: mean +2.47%, median +1.06%, hit 55%, best +26.9%, worst -13.9%
- open trades mark-to-market: mean -3.25%, hit 42%
- SPY over the same holding periods: mean -3.10% (excess +2.33%)
- beaten-down basket over the same holding periods: mean +0.57% (excess -1.34%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 16, closed: 6, open: 10
- closed trades: mean +6.82%, median +5.51%, hit 67%, best +28.5%, worst -8.4%
- open trades mark-to-market: mean -3.30%, hit 20%
- SPY over the same holding periods: mean -4.85% (excess +5.35%)
- beaten-down basket over the same holding periods: mean -1.95% (excess +2.45%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 54, closed: 0, open: 54
- open trades mark-to-market: mean -3.69%, hit 42%
- SPY over the same holding periods: mean -4.60% (excess +0.91%)
- beaten-down basket over the same holding periods: mean +0.34% (excess -4.03%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             55 |          60 | +4.03%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             55 |          60 | -21.42% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             54 |          60 | -6.57%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             53 |          60 | +8.65%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             54 |         120 | +20.32% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             52 |          60 | +10.17% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             49 |          60 | -30.30% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             49 |         120 | +10.76% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             52 |         120 | -12.22% |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             46 |          60 | -19.10% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             42 |          60 | -0.88%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             39 |          60 | +20.15% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             37 |          60 | -34.60% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             37 |          60 | +17.81% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             36 |          60 | -0.18%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             35 |          60 | -2.60%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             31 |          60 | +11.20% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             31 |          60 | +0.18%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             28 |          60 | -21.33% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             27 |          60 | -25.87% |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             26 |         120 | +7.13%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1174      |             21 |          60 | -1.32%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             20 |          60 | -16.33% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       91      |             19 |          60 | +6.32%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |             19 |          60 | -2.24%  |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-27    | 2026-10-28   |       58.64   |             19 |          20 | +15.64% |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-10-27    | 2026-10-28   |       56.5204 |             19 |          20 | -18.54% |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-27    | 2026-10-28   |       53.3582 |             19 |          20 | +11.72% |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |             18 |          60 | +5.02%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |             18 |          60 | +1.24%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |             18 |          60 | -21.69% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |             18 |          60 | +9.06%  |
| falling_wedge_beaten_down | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-10-28    | 2026-10-29   |       94.96   |             18 |          20 | -13.04% |
| early_rally_beaten_down   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |             18 |          20 | -21.69% |
| early_rally_beaten_down   | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-28    | 2026-10-29   |      342      |             18 |          20 | -8.32%  |
| early_rally_beaten_down   | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-28    | 2026-10-29   |      144.14   |             18 |          20 | -21.13% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |             17 |          60 | -9.68%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |             17 |          60 | +0.35%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |             17 |          60 | -0.06%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |             17 |          60 | -9.60%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |             17 |          20 | -0.18%  |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      259.604  |             17 |          20 | -3.04%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |             17 |          20 | -0.18%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |             16 |          60 | -3.74%  |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |             16 |          60 | -8.78%  |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       92.11   |             17 |         120 | +5.04%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |             16 |          20 | -3.99%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.73   |             16 |          20 | -20.95% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |             16 |          20 | +4.56%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |             16 |          20 | +5.38%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      263.777  |             16 |          20 | -4.57%  |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |             16 |          20 | +3.19%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |             16 |          20 | -21.44% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       93      |             16 |          20 | +4.03%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |             16 |          20 | -0.95%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |             16 |          20 | -13.44% |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |             15 |          20 | +12.22% |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |             15 |          20 | +2.60%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.3719 |             15 |          20 | +7.71%  |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      159.6    |             15 |          20 | +4.24%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      378.388  |             15 |          20 | -11.11% |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |             15 |          20 | +2.36%  |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |             15 |          20 | +3.74%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |             15 |          20 | -0.06%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             14 |          20 | +4.47%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             14 |          20 | -11.52% |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             14 |          20 | -10.54% |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |             14 |          20 | -6.65%  |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             14 |          20 | -11.52% |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             14 |          20 | -10.54% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |             14 |          20 | +2.94%  |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |             14 |          20 | -12.59% |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |             13 |          60 | +19.29% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |             13 |          60 | -10.60% |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |             13 |          60 | +6.00%  |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |             13 |          60 | +0.06%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             13 |          60 | -27.76% |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |             14 |         120 | -8.25%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             14 |         120 | +4.47%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |             14 |         120 | -10.24% |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             13 |          20 | -27.76% |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |             13 |          20 | +6.89%  |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |             13 |          20 | -9.47%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |             13 |          20 | -8.47%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |             13 |          20 | -6.65%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |             13 |          20 | -8.43%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |             13 |          20 | -1.64%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          60 | -21.89% |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             12 |          60 | +12.88% |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |             12 |          60 | +5.05%  |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |             12 |          60 | +2.54%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |             12 |          60 | -7.61%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |             12 |          60 | +1.19%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      385.935  |             12 |          60 | -0.90%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             12 |          60 | +1.05%  |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |             13 |         120 | +5.57%  |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          20 | -21.89% |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             12 |          20 | +12.88% |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             12 |          20 | +1.05%  |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |             12 |          20 | -25.26% |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |             12 |          20 | +4.99%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      319.28   |             11 |          60 | -3.66%  |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.2594 |             12 |         120 | -0.47%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.4744 |             12 |         120 | -0.22%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |             11 |          20 | -15.27% |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             11 |          20 | +3.36%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      162.81   |             11 |          20 | +2.18%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48.1006 |             11 |          20 | -4.28%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       96.896  |             11 |          20 | -4.77%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             11 |          20 | +3.36%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.99   |             11 |          20 | +7.59%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |             11 |          20 | +6.27%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.71   |             11 |          20 | -3.56%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    | 2026-11-10   |       14.52   |             10 |          60 | -3.17%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    | 2026-11-10   |      173.97   |             10 |          60 | -5.13%  |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    | 2026-11-10   |       54.99   |             10 |          20 | -9.75%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    | 2026-11-10   |       94.89   |             10 |          20 | +2.98%  |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    | 2026-11-10   |       84.538  |             10 |          20 | -4.43%  |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    | 2026-11-10   |      129.79   |             10 |          20 | -3.58%  |
| jev_skip                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-09    | 2026-11-10   |       28.44   |             10 |          20 | -6.01%  |
| insider_buy_beaten_down   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-09    | 2026-11-10   |      390.578  |             10 |         120 | -2.08%  |
| insider_buy_beaten_down   | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-09    | 2026-11-10   |       69.218  |             10 |         120 | -2.53%  |
| jev_pick                  | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-10    | 2026-11-11   |       69.1584 |              9 |          20 | -2.44%  |
| falling_wedge_beaten_down | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-11    | 2026-11-12   |      659.81   |              8 |          20 | -1.56%  |
| early_rally_beaten_down   | [ON](https://www.tradingview.com/chart/?symbol=ON)       | 2026-11-11    | 2026-11-12   |       71.43   |              8 |          20 | -6.52%  |
| early_rally_beaten_down   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-11    | 2026-11-12   |      598.63   |              8 |          20 | +1.73%  |
| jev_pick                  | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-11-11    | 2026-11-12   |       37.07   |              8 |          20 | +1.35%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-12    | 2026-11-13   |      169.91   |              7 |          60 | -2.86%  |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-12    | 2026-11-13   |        9.11   |              7 |          60 | -11.09% |
| falling_wedge_beaten_down | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-12    | 2026-11-13   |      356.54   |              7 |          20 | -12.06% |
| jev_pick                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-12    | 2026-11-13   |       15.63   |              7 |          20 | -10.04% |
| insider_buy_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-12    | 2026-11-13   |      229.75   |              7 |         120 | -6.07%  |
| insider_buy_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-12    | 2026-11-13   |      159.17   |              7 |         120 | -2.00%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-11-13    | 2026-11-16   |       13.37   |              6 |          20 | +5.31%  |
| jev_pick                  | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-13    | 2026-11-16   |      201.36   |              6 |          20 | +7.18%  |
| insider_buy_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-13    | 2026-11-16   |       85.14   |              6 |         120 | +4.79%  |
| early_rally_beaten_down   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              5 |          20 | -2.93%  |
| jev_pick                  | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              5 |          20 | -2.93%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-11-17    | 2026-11-18   |       35.54   |              4 |          60 | -5.01%  |
| falling_wedge_beaten_down | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-17    | 2026-11-18   |       85.44   |              4 |          20 | +4.42%  |
| insider_buy_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-11-13    | 2026-11-16   |       21.02   |              6 |         120 | -6.04%  |
| insider_buy_beaten_down   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-16    | 2026-11-17   |        9.25   |              5 |         120 | -12.43% |
| early_rally_beaten_down   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              4 |          20 | +0.06%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-17    | 2026-11-18   |      348.71   |              4 |          20 | -10.08% |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              4 |          20 | +0.06%  |
| newsday                   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-18    | 2026-11-19   |      214.73   |              3 |          60 | -2.50%  |
| insider_buy_beaten_down   | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-17    | 2026-11-18   |      337.63   |              4 |         120 | -0.38%  |
| early_rally_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-18    | 2026-11-19   |      230.5    |              3 |          20 | -6.37%  |
| early_rally_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-18    | 2026-11-19   |       93.34   |              3 |          20 | -4.41%  |
| early_rally_beaten_down   | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              3 |          20 | -2.98%  |
| jev_pick                  | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              3 |          20 | -2.98%  |
| newsday                   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-19    | 2026-11-20   |       87.09   |              2 |          60 | +0.06%  |
| early_rally_beaten_down   | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-19    | 2026-11-20   |      287.01   |              2 |          20 | +3.57%  |
| early_rally_beaten_down   | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-19    | 2026-11-20   |      505.18   |              2 |          20 | +2.95%  |
| jev_pick                  | [SNPS](https://www.tradingview.com/chart/?symbol=SNPS)   | 2026-11-19    | 2026-11-20   |      425      |              2 |          20 | +0.47%  |
| newsday                   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-11-20    | 2026-11-23   |      274.5    |              1 |          60 | +0.35%  |
| insider_buy_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-19    | 2026-11-20   |      123.65   |              2 |         120 | +1.21%  |
| early_rally_beaten_down   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-11-20    | 2026-11-23   |       22.06   |              1 |          20 | +1.09%  |
| jev_pick                  | [KMI](https://www.tradingview.com/chart/?symbol=KMI)     | 2026-11-20    | 2026-11-23   |       30.71   |              1 |          20 | -0.46%  |
| jev_pick                  | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-20    | 2026-11-23   |      387.33   |              1 |          20 | -1.25%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-20    | 2026-11-23   |      125      |              1 |          20 | +0.11%  |
| jev_pick                  | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-20    | 2026-11-23   |      303.45   |              1 |          20 | -2.04%  |
| jev_pick                  | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-20    | 2026-11-23   |      553      |              1 |          20 | -5.95%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-11-20    | 2026-11-23   |      246.81   |              1 |          20 | -1.85%  |
| jev_pick                  | [TT](https://www.tradingview.com/chart/?symbol=TT)       | 2026-11-20    | 2026-11-23   |      408.02   |              1 |          20 | +0.09%  |
| jev_pick                  | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-20    | 2026-11-23   |      183.15   |              1 |          20 | -3.54%  |
| newsday                   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-11-23    |              |               |            nan |          60 |         |
| falling_wedge_beaten_down | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-23    |              |               |            nan |          20 |         |
| insider_buy_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-20    | 2026-11-23   |      140.78   |              1 |         120 | -1.09%  |
| early_rally_beaten_down   | [APO](https://www.tradingview.com/chart/?symbol=APO)     | 2026-11-23    |              |               |            nan |          20 |         |