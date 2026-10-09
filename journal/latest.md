# Forward-test journal - 2026-10-08

Data through 2026-10-08; 518 of 518 symbols loaded.

## New signals today (0)

none

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       27 |        0 | -0.32% | 54%   | -0.03%   | -1.47%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       19 |        2 | -1.70% | 28%   | -2.26%   | -1.61%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        3 |        0 | -1.29% | 33%   | -3.00%   | +1.06%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +0.37% | 61%   | +0.20%   | -1.39%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       13 |        0 | -0.39% | 46%   | -1.37%   | +0.31%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 27, closed: 0, open: 27
- open trades mark-to-market: mean -0.32%, hit 54%
- SPY over the same holding periods: mean -0.29% (excess -0.03%)
- beaten-down basket over the same holding periods: mean +1.15% (excess -1.47%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 19, closed: 2, open: 17
- closed trades: mean -5.72%, median -5.72%, hit 0%, best -3.5%, worst -8.0%
- open trades mark-to-market: mean -1.20%, hit 31%
- SPY over the same holding periods: mean +0.56% (excess -2.26%)
- beaten-down basket over the same holding periods: mean -0.09% (excess -1.61%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean -1.29%, hit 33%
- SPY over the same holding periods: mean +1.72% (excess -3.00%)
- beaten-down basket over the same holding periods: mean -2.35% (excess +1.06%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +0.37%, hit 61%
- SPY over the same holding periods: mean +0.16% (excess +0.20%)
- beaten-down basket over the same holding periods: mean +1.76% (excess -1.39%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 13, closed: 0, open: 13
- open trades mark-to-market: mean -0.39%, hit 46%
- SPY over the same holding periods: mean +0.98% (excess -1.37%)
- beaten-down basket over the same holding periods: mean -0.70% (excess +0.31%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |       100.58  |             23 |          60 | -7.85%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |       920.51  |             23 |          60 | -23.15% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |       232.71  |             22 |          60 | -4.36%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |       632     |             21 |          60 | +1.63%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |        52.32  |             22 |         120 | +0.04%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |        54.66  |             20 |          60 | -0.66%  |
| falling_wedge_beaten_down | [TXT](https://www.tradingview.com/chart/?symbol=TXT)   | 2026-09-11    | 2026-09-14   |        80.19  |             19 |          20 | -8.69%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |       441.33  |             17 |          60 | -5.44%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |        54.37  |             17 |         120 | -0.13%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |        72.99  |             20 |         120 | -3.77%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |        71.82  |             14 |          60 | -0.35%  |
| falling_wedge_beaten_down | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-09-18    | 2026-09-21   |       532.3   |             14 |          20 | -4.59%  |
| falling_wedge_beaten_down | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-09-18    | 2026-09-21   |      1091.3   |             14 |          20 | -0.18%  |
| falling_wedge_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-09-21    | 2026-09-22   |       519.27  |             13 |          20 | -1.18%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |       148.65  |             11 |          20 | -5.13%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |       107.7   |             11 |          20 | -5.30%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |        33.99  |             10 |          60 | -11.71% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |       366.7   |             10 |          20 | -1.41%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |        14.45  |              9 |          20 | +7.20%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |        36.34  |              8 |          20 | -4.40%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |       602.02  |              7 |          60 | +17.51% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |        12.385 |              5 |          60 | +11.02% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |       614     |              5 |          60 | +15.22% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              5 |          20 | +3.85%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |       238.11  |              5 |          20 | -4.33%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |       273.31  |              5 |          20 | +3.07%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |       162.22  |              5 |          20 | +2.78%  |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |        30.98  |              5 |          20 | +0.90%  |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              5 |          20 | +3.85%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |       222.597 |              5 |          20 | +1.77%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |       121.94  |              5 |          20 | -2.23%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |       119.24  |              5 |          20 | -2.87%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |       101.99  |              5 |          20 | -0.00%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |       142.09  |              5 |          20 | -4.50%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |        33.82  |              4 |          60 | +2.72%  |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |        47.64  |              4 |          20 | +2.69%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |       163.81  |              4 |          20 | +7.13%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              3 |          60 | +0.36%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | 2026-10-06   |        84.2   |              3 |          20 | +2.32%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | 2026-10-06   |        77.73  |              3 |          20 | +0.68%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | 2026-10-06   |        83.45  |              3 |          20 | +3.07%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    | 2026-10-06   |       134.94  |              3 |          20 | +2.82%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              3 |          20 | -6.46%  |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              3 |          20 | -3.02%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              3 |          20 | +0.36%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              3 |          20 | -6.46%  |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              3 |          20 | -3.02%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV) | 2026-10-06    | 2026-10-07   |        44.35  |              2 |          20 | -0.32%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-06    | 2026-10-07   |       103.16  |              2 |          20 | +0.44%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-06    | 2026-10-07   |       103.39  |              2 |          20 | -1.35%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-10-06    | 2026-10-07   |        15.15  |              2 |          20 | +2.24%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)     | 2026-10-06    | 2026-10-07   |        40.61  |              2 |          20 | -0.20%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)   | 2026-10-06    | 2026-10-07   |        52.59  |              2 |          20 | +0.67%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)   | 2026-10-06    | 2026-10-07   |       128.11  |              2 |          20 | -0.79%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)   | 2026-10-06    | 2026-10-07   |        33.7   |              2 |          20 | +1.19%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)   | 2026-10-06    | 2026-10-07   |        38.17  |              2 |          20 | +0.65%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)   | 2026-10-06    | 2026-10-07   |        71.68  |              2 |          20 | +0.22%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)   | 2026-10-06    | 2026-10-07   |       102.99  |              2 |          20 | -0.49%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST) | 2026-10-06    | 2026-10-07   |       940.84  |              2 |          20 | +0.75%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              1 |          20 | -1.10%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              1 |          20 | -1.10%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-10-07    | 2026-10-08   |       642     |              1 |          20 | +0.04%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-07    | 2026-10-08   |       126.47  |              1 |          20 | +3.65%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP) | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU) | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)     | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)   | 2026-10-08    | nan          |       nan     |            nan |          20 |         |