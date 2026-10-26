# Forward-test journal - 2026-10-26

Data through 2026-10-26; 518 of 518 symbols loaded.

## New signals today (1)

| rule    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                       |
|:--------|:-------------------------------------------------------|:--------------|------------:|------------:|:-------------------------------------------|
| newsday | [MELI](https://www.tradingview.com/chart/?symbol=MELI) | 2026-10-26    |     1668.72 |          60 | gap -12.6%, vol 5.1x, 6m -9%, vs MA200 -8% |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      101 |        0 | +2.92% | 77%   | +3.86%   | +0.74%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       33 |       11 | +2.12% | 73%   | +2.76%   | -0.33%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        4 |        0 | +3.59% | 75%   | +3.20%   | +2.04%             |
| jev_pick                  | untested (forward test only)                     |       32 |        0 | +3.00% | 62%   | +3.60%   | -0.60%             |
| jev_skip                  | untested; a fall is the success case             |        6 |        0 | +0.90% | 50%   | +0.71%   | +0.71%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       19 |        0 | -1.75% | 39%   | -1.42%   | -5.16%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 101, closed: 0, open: 101
- open trades mark-to-market: mean +2.92%, hit 77%
- SPY over the same holding periods: mean -0.94% (excess +3.86%)
- beaten-down basket over the same holding periods: mean +2.18% (excess +0.74%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 33, closed: 11, open: 22
- closed trades: mean +0.81%, median +3.28%, hit 64%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +2.77%, hit 77%
- SPY over the same holding periods: mean -0.65% (excess +2.76%)
- beaten-down basket over the same holding periods: mean +2.44% (excess -0.33%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 4, closed: 0, open: 4
- open trades mark-to-market: mean +3.59%, hit 75%
- SPY over the same holding periods: mean +0.38% (excess +3.20%)
- beaten-down basket over the same holding periods: mean +1.54% (excess +2.04%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 32, closed: 0, open: 32
- open trades mark-to-market: mean +3.00%, hit 62%
- SPY over the same holding periods: mean -0.59% (excess +3.60%)
- beaten-down basket over the same holding periods: mean +3.60% (excess -0.60%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 6, closed: 0, open: 6
- open trades mark-to-market: mean +0.90%, hit 50%
- SPY over the same holding periods: mean +0.19% (excess +0.71%)
- beaten-down basket over the same holding periods: mean +0.19% (excess +0.71%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 19, closed: 0, open: 19
- open trades mark-to-market: mean -1.75%, hit 39%
- SPY over the same holding periods: mean -0.33% (excess -1.42%)
- beaten-down basket over the same holding periods: mean +3.41% (excess -5.16%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             35 |          60 | +2.32%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             35 |          60 | -23.08% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.71   |             34 |          60 | -16.48% |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      632      |             33 |          60 | +11.38% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             34 |         120 | +7.80%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             32 |          60 | +11.86% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             29 |          60 | -3.75%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             29 |         120 | +12.45% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             32 |         120 | -9.40%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             26 |          60 | -11.03% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             22 |          60 | -16.03% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             19 |          60 | +17.62% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             17 |          60 | -3.51%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             17 |          60 | +15.32% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |       79.5    |             17 |          20 | +1.09%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)     | 2026-10-01    | 2026-10-02   |      238.11   |             17 |          20 | +3.99%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)     | 2026-10-01    | 2026-10-02   |      273.31   |             17 |          20 | +5.70%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)     | 2026-10-01    | 2026-10-02   |      162.22   |             17 |          20 | +16.06% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)     | 2026-10-01    | 2026-10-02   |       30.98   |             17 |          20 | +12.94% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |       79.5    |             17 |          20 | +1.09%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE)   | 2026-10-01    | 2026-10-02   |      222.597  |             17 |          20 | +12.89% |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-01    | 2026-10-02   |      121.94   |             17 |          20 | +14.70% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-01    | 2026-10-02   |      119.24   |             17 |          20 | -6.99%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-01    | 2026-10-02   |      101.99   |             17 |          20 | +6.13%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-01    | 2026-10-02   |      141.566  |             17 |          20 | -10.95% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             16 |          60 | +12.09% |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)     | 2026-10-02    | 2026-10-05   |       47.64   |             16 |          20 | +8.40%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK)   | 2026-10-02    | 2026-10-05   |      163.81   |             16 |          20 | +19.77% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             15 |          60 | -0.48%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-05    | 2026-10-06   |       84.2    |             15 |          20 | +9.94%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-05    | 2026-10-06   |       77.73   |             15 |          20 | +0.51%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-05    | 2026-10-06   |       83.45   |             15 |          20 | +9.11%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-10-05    | 2026-10-06   |      134.94   |             15 |          20 | +6.49%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |       99.81   |             15 |          20 | -10.57% |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |      529.14   |             15 |          20 | +7.76%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             15 |          20 | -0.48%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |       99.81   |             15 |          20 | -10.57% |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |      529.14   |             15 |          20 | +7.76%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV)   | 2026-10-06    | 2026-10-07   |       44.35   |             14 |          20 | -1.67%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-06    | 2026-10-07   |      103.16   |             14 |          20 | +7.72%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-06    | 2026-10-07   |      103.39   |             14 |          20 | +4.69%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-10-06    | 2026-10-07   |       15.15   |             14 |          20 | +0.66%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)       | 2026-10-06    | 2026-10-07   |       40.61   |             14 |          20 | +6.97%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)     | 2026-10-06    | 2026-10-07   |       52.59   |             14 |          20 | +4.30%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)     | 2026-10-06    | 2026-10-07   |      128.11   |             14 |          20 | +2.83%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)     | 2026-10-06    | 2026-10-07   |       33.7    |             14 |          20 | +3.62%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)     | 2026-10-06    | 2026-10-07   |       38.17   |             14 |          20 | +7.94%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-06    | 2026-10-07   |       71.68   |             14 |          20 | +0.60%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)     | 2026-10-06    | 2026-10-07   |      102.99   |             14 |          20 | +4.38%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST)   | 2026-10-06    | 2026-10-07   |      940.84   |             14 |          20 | +6.84%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |      107.5    |             13 |          20 | -12.92% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |      107.5    |             13 |          20 | -12.92% |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-07    | 2026-10-08   |      642      |             13 |          20 | +9.65%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-07    | 2026-10-08   |      126.47   |             13 |          20 | -2.84%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-08    | 2026-10-09   |       85.58   |             12 |          20 | +6.39%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)     | 2026-10-08    | 2026-10-09   |      123.25   |             12 |          20 | +10.04% |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)     | 2026-10-08    | 2026-10-09   |       73.04   |             12 |          20 | +10.86% |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-08    | 2026-10-09   |       82.91   |             12 |          20 | -3.06%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-08    | 2026-10-09   |       30.02   |             12 |          20 | +12.26% |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-10-08    | 2026-10-09   |      309.25   |             12 |          20 | +1.32%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-10-08    | 2026-10-09   |      305.05   |             12 |          20 | +11.42% |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)     | 2026-10-08    | 2026-10-09   |      110      |             12 |          20 | +9.35%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)     | 2026-10-08    | 2026-10-09   |       37.61   |             12 |          20 | +6.35%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-08    | 2026-10-09   |      155.51   |             12 |          20 | -5.52%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)       | 2026-10-08    | 2026-10-09   |       44.83   |             12 |          20 | +3.01%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)     | 2026-10-08    | 2026-10-09   |      116.26   |             12 |          20 | +7.04%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-08    | 2026-10-09   |       85.94   |             12 |          20 | +7.71%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-08    | 2026-10-09   |      144      |             12 |          20 | +3.80%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)     | 2026-10-08    | 2026-10-09   |       73.17   |             12 |          20 | +6.41%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             11 |          60 | -1.78%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             11 |          60 | -6.33%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-09    | 2026-10-12   |      143.23   |             11 |          20 | +6.30%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |       81.45   |             11 |          20 | +3.43%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC)   | 2026-10-09    | 2026-10-12   |      181.77   |             11 |          20 | +2.28%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-10-09    | 2026-10-12   |       33.62   |             11 |          20 | -3.24%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-09    | 2026-10-12   |       81.41   |             11 |          20 | -4.03%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-09    | 2026-10-12   |       53.56   |             11 |          20 | +5.30%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |       81.45   |             11 |          20 | +3.43%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)     | 2026-10-09    | 2026-10-12   |      161.66   |             11 |          20 | +5.96%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-09    | 2026-10-12   |      366.01   |             11 |          20 | -8.89%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-09    | 2026-10-12   |      103.99   |             11 |          20 | +6.86%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)     | 2026-10-09    | 2026-10-12   |       65.9    |             11 |          20 | +5.46%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)     | 2026-10-09    | 2026-10-12   |      123.2    |             11 |          20 | +4.89%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-12    | 2026-10-13   |      486.79   |             10 |          20 | +16.15% |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-12    | 2026-10-13   |      147.47   |             10 |          20 | +1.36%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD)   | 2026-10-12    | 2026-10-13   |      140.79   |             10 |          20 | +6.02%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-10-12    | 2026-10-13   |       13.21   |             10 |          20 | -2.73%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)     | 2026-10-12    | 2026-10-13   |       56.04   |             10 |          20 | +3.10%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)     | 2026-10-12    | 2026-10-13   |       66.28   |             10 |          20 | +4.99%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)     | 2026-10-12    | 2026-10-13   |       42.6    |             10 |          20 | +4.55%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)     | 2026-10-12    | 2026-10-13   |     1113.01   |             10 |          20 | +1.50%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC)   | 2026-10-12    | 2026-10-13   |       67.7021 |             10 |          20 | +6.32%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |       32.85   |              9 |          20 | +7.88%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |      182.6    |              9 |          20 | -0.07%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |       67.9    |              9 |          20 | +10.85% |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |      220.63   |              9 |          20 | +4.03%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |       57.66   |              9 |          20 | +7.37%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |      191.79   |              9 |          20 | +5.59%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |              8 |          60 | -10.16% |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |       33.27   |              8 |          20 | +3.85%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |      342.5    |              8 |          20 | -1.92%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |      153.24   |              8 |          20 | +16.52% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |       61.37   |              8 |          20 | +9.74%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |      531      |              8 |          20 | +19.62% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |              7 |          60 | -15.35% |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |              7 |          20 | -9.66%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |       27.96   |              7 |          20 | +4.26%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |       83.4    |              7 |          20 | +2.43%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |      529.98   |              7 |          20 | -1.48%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |      357.38   |              7 |          20 | +2.31%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |     3091      |              7 |          20 | +3.21%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |       13.29   |              7 |          20 | -3.91%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |       36.42   |              7 |          20 | +1.24%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |      120.66   |              7 |          20 | -8.09%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |      295.89   |              7 |          20 | +3.46%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |       69.87   |              7 |          20 | -8.54%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |       44.45   |              7 |          20 | +2.54%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |       29.93   |              7 |          20 | +13.56% |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |      125.05   |              7 |          20 | +11.84% |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |      244.31   |              7 |          20 | +2.67%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |      150.37   |              7 |          20 | +1.26%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |      505.78   |              7 |          20 | -0.37%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |      195.819  |              7 |          20 | +1.23%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |       37.67   |              7 |          20 | +0.64%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |       86.69   |              7 |          20 | +0.08%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |       79.6    |              7 |          20 | +3.07%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |      255.41   |              7 |          20 | +2.38%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |      170.42   |              7 |          20 | -1.29%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |              7 |          20 | -9.66%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |      169.41   |              6 |          20 | -0.70%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |       45.99   |              6 |          20 | +4.31%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |      511      |              6 |          20 | +10.65% |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |       57.29   |              6 |          20 | +6.72%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |      289.03   |              6 |          20 | +4.51%  |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |      268.28   |              6 |          20 | +4.76%  |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |      245.16   |              6 |          20 | +6.15%  |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |       47.42   |              6 |          20 | +1.92%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |       23.48   |              6 |          20 | +2.30%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |              6 |          20 | +3.50%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |      104.16   |              6 |          20 | +3.92%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |       55.8    |              6 |          20 | +2.44%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |      306.55   |              6 |          20 | +4.19%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |       33.45   |              6 |          20 | +5.95%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |              6 |         120 | +3.50%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |      454.74   |              5 |          20 | +1.02%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |      111.74   |              4 |          20 | +6.55%  |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |       55.27   |              4 |          20 | +2.04%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |              4 |          20 | +2.91%  |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |       86.03   |              4 |          20 | -0.70%  |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |       21.94   |              4 |          20 | +0.50%  |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |       78.84   |              4 |          20 | +6.52%  |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |      545      |              4 |          20 | -4.20%  |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |       77.73   |              4 |          20 | +0.49%  |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |       56.51   |              4 |          20 | -0.12%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |      189.29   |              4 |          20 | -3.60%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |      227.11   |              4 |          20 | +1.06%  |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |      465.97   |              4 |          20 | -1.41%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |       62.31   |              4 |          20 | +1.70%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |      338.03   |              4 |          20 | -2.62%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |      281.5    |              4 |          20 | -2.07%  |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |              4 |          20 | +2.91%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |      363.84   |              3 |          20 | +0.49%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | 2026-10-22   |      264.64   |              3 |          20 | -1.19%  |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | 2026-10-22   |      509.34   |              3 |          20 | -1.06%  |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |      544.7    |              3 |          20 | +3.80%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |       77.57   |              3 |          20 | +8.26%  |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |       85.6    |              3 |          20 | +1.36%  |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    | 2026-10-23   |       54.61   |              2 |          20 | +1.12%  |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |              2 |          20 | -0.83%  |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    | 2026-10-23   |      818.29   |              2 |          20 | -13.47% |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    | 2026-10-23   |       28.89   |              2 |          20 | +0.90%  |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |              2 |          20 | -4.54%  |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    | 2026-10-23   |      117.97   |              2 |          20 | +2.83%  |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |              2 |          20 | -0.58%  |
| jev_pick                  | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |              2 |          20 | -0.58%  |
| jev_pick                  | [ISRG](https://www.tradingview.com/chart/?symbol=ISRG)   | 2026-10-22    | 2026-10-23   |      443.65   |              2 |          20 | +1.80%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-10-22    | 2026-10-23   |      126.05   |              2 |          20 | +0.21%  |
| jev_skip                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-22    | 2026-10-23   |       13      |              2 |          20 | -1.77%  |
| jev_skip                  | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |              2 |          20 | -0.83%  |
| jev_skip                  | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |              2 |          20 | -4.54%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |              1 |          60 | +5.89%  |
| jev_pick                  | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |              1 |          20 | +5.89%  |
| jev_pick                  | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-23    | 2026-10-26   |      699.26   |              1 |          20 | +0.67%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    |              |               |            nan |          60 |         |