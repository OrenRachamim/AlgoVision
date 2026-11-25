# Forward-test journal - 2026-11-25

Data through 2026-11-25; 518 of 518 symbols loaded.

## New signals today (5)

| rule                      | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                        |
|:--------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:------------------------------------------------------------|
| falling_wedge_beaten_down | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-11-25    |      174.66 |          20 | score 0.64, stop 161.53, level 172.87                       |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-11-25    |      349.97 |          20 | rsi_turn; day +2.4%, 10d -0.2%, 6m -29%, vs MA200 -23%      |
| early_rally_beaten_down   | [JBHT](https://www.tradingview.com/chart/?symbol=JBHT) | 2026-11-25    |      227.92 |          20 | ma50_cross; day +2.0%, 10d +0.1%, 6m -16%, vs MA200 -7%     |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR) | 2026-11-25    |       53.9  |          20 | rsi_turn; day +2.2%, 10d -1.2%, 6m -15%, vs MA200 -11%      |
| early_rally_beaten_down   | [MOS](https://www.tradingview.com/chart/?symbol=MOS)   | 2026-11-25    |       20.35 |          20 | golden_20_50; day +3.4%, 10d -10.7%, 6m -15%, vs MA200 -11% |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      143 |      106 | +3.52% | 71%   | +7.18%   | +0.18%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       40 |       35 | +1.35% | 59%   | +3.62%   | -2.35%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       23 |        0 | +0.29% | 52%   | +4.35%   | +2.47%             |
| jev_pick                  | untested (forward test only)                     |       78 |       33 | -1.71% | 46%   | +1.72%   | -1.75%             |
| jev_skip                  | untested; a fall is the success case             |       16 |        6 | +2.37% | 56%   | +7.69%   | +4.91%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       54 |        0 | -3.62% | 46%   | +1.62%   | -4.36%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 143, closed: 106, open: 37
- closed trades: mean +5.25%, median +6.46%, hit 78%, best +34.5%, worst -27.9%
- open trades mark-to-market: mean -2.04%, hit 45%
- SPY over the same holding periods: mean -3.66% (excess +7.18%)
- beaten-down basket over the same holding periods: mean +3.34% (excess +0.18%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 40, closed: 35, open: 5
- closed trades: mean +2.10%, median +3.72%, hit 63%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean -5.26%, hit 25%
- SPY over the same holding periods: mean -2.27% (excess +3.62%)
- beaten-down basket over the same holding periods: mean +3.70% (excess -2.35%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 23, closed: 0, open: 23
- open trades mark-to-market: mean +0.29%, hit 52%
- SPY over the same holding periods: mean -4.06% (excess +4.35%)
- beaten-down basket over the same holding periods: mean -2.18% (excess +2.47%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 78, closed: 33, open: 45
- closed trades: mean +2.47%, median +1.06%, hit 55%, best +26.9%, worst -13.9%
- open trades mark-to-market: mean -4.77%, hit 40%
- SPY over the same holding periods: mean -3.43% (excess +1.72%)
- beaten-down basket over the same holding periods: mean +0.04% (excess -1.75%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 16, closed: 6, open: 10
- closed trades: mean +6.82%, median +5.51%, hit 67%, best +28.5%, worst -8.4%
- open trades mark-to-market: mean -0.30%, hit 50%
- SPY over the same holding periods: mean -5.31% (excess +7.69%)
- beaten-down basket over the same holding periods: mean -2.54% (excess +4.91%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 54, closed: 0, open: 54
- open trades mark-to-market: mean -3.62%, hit 46%
- SPY over the same holding periods: mean -5.24% (excess +1.62%)
- beaten-down basket over the same holding periods: mean +0.74% (excess -4.36%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             57 |          60 | +6.82%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             57 |          60 | -23.98% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             56 |          60 | -9.24%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             55 |          60 | +10.59% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             56 |         120 | +21.41% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             54 |          60 | +13.96% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             51 |          60 | -22.27% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             51 |         120 | +14.57% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             54 |         120 | -9.10%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             48 |          60 | -17.28% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             44 |          60 | +1.94%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             41 |          60 | +16.24% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             39 |          60 | -33.55% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             39 |          60 | +13.98% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             38 |          60 | +8.40%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             37 |          60 | +2.83%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             33 |          60 | +11.13% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             33 |          60 | +3.19%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             30 |          60 | -30.70% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             29 |          60 | -34.70% |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             28 |         120 | +9.97%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1174      |             23 |          60 | -6.34%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             22 |          60 | -13.85% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       90.5956 |             21 |          60 | +6.43%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |             21 |          60 | -3.58%  |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |             20 |          60 | +7.68%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |             20 |          60 | +7.92%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.832  |             20 |          60 | -27.10% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |             20 |          60 | +22.86% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |             19 |          60 | -4.61%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |             19 |          60 | -2.85%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |             19 |          60 | -3.11%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |             19 |          60 | -5.57%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |             19 |          20 | -0.13%  |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      259.604  |             19 |          20 | -9.37%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |             19 |          20 | -0.13%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |             18 |          60 | -0.76%  |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |             18 |          60 | -16.71% |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       91.7006 |             19 |         120 | +5.15%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |             18 |          20 | -0.24%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.603  |             18 |          20 | -26.41% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |             18 |          20 | +9.67%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |             18 |          20 | +4.51%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      263.777  |             18 |          20 | -10.80% |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |             18 |          20 | +4.13%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |             18 |          20 | -20.43% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       92.5867 |             18 |          20 | +4.14%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |             18 |          20 | +1.56%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |             18 |          20 | -6.00%  |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |             17 |          20 | +29.20% |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |             17 |          20 | +4.22%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.3719 |             17 |          20 | +11.25% |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      159.6    |             17 |          20 | +4.17%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      378.388  |             17 |          20 | -16.01% |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |             17 |          20 | -8.33%  |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |             17 |          20 | +7.13%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |             17 |          20 | +3.44%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             16 |          20 | +7.44%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             16 |          20 | -16.40% |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             16 |          20 | -13.09% |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |             16 |          20 | -14.70% |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             16 |          20 | -16.40% |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             16 |          20 | -13.09% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |             16 |          20 | +5.36%  |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |             16 |          20 | -9.61%  |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |             15 |          60 | +12.23% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |             15 |          60 | -7.56%  |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |             15 |          60 | +3.82%  |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |             15 |          60 | +3.08%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             15 |          60 | -27.10% |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |             16 |         120 | -7.05%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             16 |         120 | +7.44%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |             16 |         120 | -10.79% |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             15 |          20 | -27.10% |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |             15 |          20 | +8.32%  |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |             15 |          20 | -6.25%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |             15 |          20 | -5.36%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |             15 |          20 | -5.05%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |             15 |          20 | -4.00%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |             15 |          20 | +0.89%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          60 | -34.44% |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             14 |          60 | +4.81%  |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |             14 |          60 | +6.46%  |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |             14 |          60 | +4.58%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |             14 |          60 | -4.88%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |             14 |          60 | -1.86%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      385.935  |             14 |          60 | -0.27%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             14 |          60 | -11.13% |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |             15 |         120 | -3.61%  |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          20 | -34.44% |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             14 |          20 | +4.81%  |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             14 |          20 | -11.13% |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |             14 |          20 | -24.57% |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |             14 |          20 | +1.63%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      319.28   |             13 |          60 | +7.44%  |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.2594 |             14 |         120 | +0.22%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.4744 |             14 |         120 | +5.22%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |             13 |          20 | -16.38% |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             13 |          20 | +0.41%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      162.81   |             13 |          20 | +2.11%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48.1006 |             13 |          20 | -3.62%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       96.896  |             13 |          20 | +0.42%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             13 |          20 | +0.41%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.99   |             13 |          20 | +7.94%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |             13 |          20 | +8.15%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.71   |             13 |          20 | -2.26%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    | 2026-11-10   |       14.52   |             12 |          60 | -2.96%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    | 2026-11-10   |      173.97   |             12 |          60 | -14.18% |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    | 2026-11-10   |       54.99   |             12 |          20 | -14.49% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    | 2026-11-10   |       94.89   |             12 |          20 | -3.11%  |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    | 2026-11-10   |       84.538  |             12 |          20 | +2.64%  |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    | 2026-11-10   |      129.79   |             12 |          20 | -2.13%  |
| jev_skip                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-09    | 2026-11-10   |       28.44   |             12 |          20 | -2.81%  |
| insider_buy_beaten_down   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-09    | 2026-11-10   |      390.578  |             12 |         120 | -1.45%  |
| insider_buy_beaten_down   | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-09    | 2026-11-10   |       69.218  |             12 |         120 | -3.70%  |
| jev_pick                  | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-10    | 2026-11-11   |       69.1584 |             11 |          20 | -3.61%  |
| falling_wedge_beaten_down | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-11    | 2026-11-12   |      659.81   |             10 |          20 | -4.71%  |
| early_rally_beaten_down   | [ON](https://www.tradingview.com/chart/?symbol=ON)       | 2026-11-11    | 2026-11-12   |       71.43   |             10 |          20 | -12.53% |
| early_rally_beaten_down   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-11    | 2026-11-12   |      598.63   |             10 |          20 | -5.54%  |
| jev_pick                  | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-11-11    | 2026-11-12   |       36.8386 |             10 |          20 | +9.59%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-12    | 2026-11-13   |      169.91   |              9 |          60 | -12.13% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-12    | 2026-11-13   |        9.11   |              9 |          60 | -9.66%  |
| falling_wedge_beaten_down | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-12    | 2026-11-13   |      356.54   |              9 |          20 | -15.62% |
| jev_pick                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-12    | 2026-11-13   |       15.63   |              9 |          20 | -9.85%  |
| insider_buy_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-12    | 2026-11-13   |      229.75   |              9 |         120 | -14.61% |
| insider_buy_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-12    | 2026-11-13   |      159.17   |              9 |         120 | +3.49%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-11-13    | 2026-11-16   |       13.37   |              8 |          20 | +6.66%  |
| jev_pick                  | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-13    | 2026-11-16   |      201.36   |              8 |          20 | -2.57%  |
| insider_buy_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-13    | 2026-11-16   |       85.14   |              8 |         120 | +4.13%  |
| early_rally_beaten_down   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              7 |          20 | +5.40%  |
| jev_pick                  | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              7 |          20 | +5.40%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-11-17    | 2026-11-18   |       35.54   |              6 |          60 | +3.15%  |
| falling_wedge_beaten_down | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-17    | 2026-11-18   |       85.44   |              6 |          20 | +3.77%  |
| insider_buy_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-11-13    | 2026-11-16   |       21.02   |              8 |         120 | -2.38%  |
| insider_buy_beaten_down   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-16    | 2026-11-17   |        9.25   |              7 |         120 | -11.03% |
| early_rally_beaten_down   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              6 |          20 | +5.64%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-17    | 2026-11-18   |      348.71   |              6 |          20 | -13.72% |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              6 |          20 | +5.64%  |
| newsday                   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-18    | 2026-11-19   |      214.73   |              5 |          60 | +5.87%  |
| insider_buy_beaten_down   | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-17    | 2026-11-18   |      337.63   |              6 |         120 | -5.87%  |
| early_rally_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-18    | 2026-11-19   |      230.5    |              5 |          20 | -14.89% |
| early_rally_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-18    | 2026-11-19   |       93.34   |              5 |          20 | -5.01%  |
| early_rally_beaten_down   | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              5 |          20 | -3.34%  |
| jev_pick                  | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              5 |          20 | -3.34%  |
| newsday                   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-19    | 2026-11-20   |       87.09   |              4 |          60 | +0.38%  |
| early_rally_beaten_down   | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-19    | 2026-11-20   |      287.01   |              4 |          20 | -5.07%  |
| early_rally_beaten_down   | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-19    | 2026-11-20   |      505.18   |              4 |          20 | -6.50%  |
| jev_pick                  | [SNPS](https://www.tradingview.com/chart/?symbol=SNPS)   | 2026-11-19    | 2026-11-20   |      425      |              4 |          20 | -4.68%  |
| newsday                   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-11-20    | 2026-11-23   |      274.02   |              3 |          60 | -0.84%  |
| insider_buy_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-19    | 2026-11-20   |      123.65   |              4 |         120 | +2.73%  |
| early_rally_beaten_down   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-11-20    | 2026-11-23   |       22.06   |              3 |          20 | +4.13%  |
| jev_pick                  | [KMI](https://www.tradingview.com/chart/?symbol=KMI)     | 2026-11-20    | 2026-11-23   |       30.71   |              3 |          20 | +3.19%  |
| jev_pick                  | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-20    | 2026-11-23   |      387.33   |              3 |          20 | -0.62%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-20    | 2026-11-23   |      125      |              3 |          20 | +1.62%  |
| jev_pick                  | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-20    | 2026-11-23   |      303.58   |              3 |          20 | -10.25% |
| jev_pick                  | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-20    | 2026-11-23   |      553      |              3 |          20 | -14.59% |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-11-20    | 2026-11-23   |      246.81   |              3 |          20 | -7.56%  |
| jev_pick                  | [TT](https://www.tradingview.com/chart/?symbol=TT)       | 2026-11-20    | 2026-11-23   |      408.02   |              3 |          20 | -1.11%  |
| jev_pick                  | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-20    | 2026-11-23   |      183.02   |              3 |          20 | -11.75% |
| newsday                   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-11-23    | 2026-11-24   |      256.5    |              2 |          60 | +1.90%  |
| falling_wedge_beaten_down | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-23    | 2026-11-24   |      169.09   |              2 |          20 | -4.48%  |
| insider_buy_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-20    | 2026-11-23   |      140.78   |              3 |         120 | +3.77%  |
| early_rally_beaten_down   | [APO](https://www.tradingview.com/chart/?symbol=APO)     | 2026-11-23    | 2026-11-24   |      116.18   |              2 |          20 | +3.70%  |
| jev_pick                  | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-23    | 2026-11-24   |      139.38   |              2 |          20 | +4.81%  |
| jev_pick                  | [STLD](https://www.tradingview.com/chart/?symbol=STLD)   | 2026-11-23    | 2026-11-24   |      211.71   |              2 |          20 | +2.43%  |
| insider_buy_beaten_down   | [BG](https://www.tradingview.com/chart/?symbol=BG)       | 2026-11-23    | 2026-11-24   |       91.8    |              2 |         120 | -3.98%  |
| insider_buy_beaten_down   | [WMB](https://www.tradingview.com/chart/?symbol=WMB)     | 2026-11-23    | 2026-11-24   |       65.05   |              2 |         120 | +2.15%  |
| early_rally_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-24    | 2026-11-25   |      163      |              1 |          20 | +1.06%  |
| early_rally_beaten_down   | [F](https://www.tradingview.com/chart/?symbol=F)         | 2026-11-24    | 2026-11-25   |       11.91   |              1 |          20 | +2.18%  |
| falling_wedge_beaten_down | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-11-25    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-11-25    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [JBHT](https://www.tradingview.com/chart/?symbol=JBHT)   | 2026-11-25    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-11-25    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [MOS](https://www.tradingview.com/chart/?symbol=MOS)     | 2026-11-25    |              |               |            nan |          20 |         |