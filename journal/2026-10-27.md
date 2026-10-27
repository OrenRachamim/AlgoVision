# Forward-test journal - 2026-10-27

Data through 2026-10-27; 518 of 518 symbols loaded.

## New signals today (5)

| rule                      | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                              |
|:--------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:------------------------------------------------------------------|
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-27    |       92.86 |          60 | gap -5.8%, vol 4.6x, 6m -21%, vs MA200 -21%                       |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB) | 2026-10-27    |      434.28 |          60 | gap -6.3%, vol 3.4x, 6m -20%, vs MA200 -11%                       |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA) | 2026-10-27    |       59.23 |          20 | score 0.75, stop 55.36, level 58.45                               |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)   | 2026-10-27    |       59    |          20 | ma50_cross, rsi_turn; day +5.3%, 10d +4.5%, 6m -12%, vs MA200 -1% |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)   | 2026-10-27    |       54.02 |          20 | rsi_turn; day +7.3%, 10d +6.8%, 6m -20%, vs MA200 -16%            |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      103 |        0 | +2.60% | 75%   | +2.99%   | +0.35%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       34 |       11 | +1.52% | 73%   | +1.79%   | -0.88%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        4 |        0 | +2.20% | 75%   | +1.26%   | +0.76%             |
| jev_pick                  | untested (forward test only)                     |       33 |        0 | +2.20% | 67%   | +2.23%   | -1.41%             |
| jev_skip                  | untested; a fall is the success case             |        6 |        0 | +1.70% | 67%   | +0.94%   | +0.69%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       21 |        0 | -1.54% | 42%   | -1.78%   | -4.61%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 103, closed: 0, open: 103
- open trades mark-to-market: mean +2.60%, hit 75%
- SPY over the same holding periods: mean -0.39% (excess +2.99%)
- beaten-down basket over the same holding periods: mean +2.25% (excess +0.35%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 34, closed: 11, open: 23
- closed trades: mean +0.81%, median +3.28%, hit 64%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +1.87%, hit 77%
- SPY over the same holding periods: mean -0.28% (excess +1.79%)
- beaten-down basket over the same holding periods: mean +2.39% (excess -0.88%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 4, closed: 0, open: 4
- open trades mark-to-market: mean +2.20%, hit 75%
- SPY over the same holding periods: mean +0.95% (excess +1.26%)
- beaten-down basket over the same holding periods: mean +1.44% (excess +0.76%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 33, closed: 0, open: 33
- open trades mark-to-market: mean +2.20%, hit 67%
- SPY over the same holding periods: mean -0.02% (excess +2.23%)
- beaten-down basket over the same holding periods: mean +3.62% (excess -1.41%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 6, closed: 0, open: 6
- open trades mark-to-market: mean +1.70%, hit 67%
- SPY over the same holding periods: mean +0.75% (excess +0.94%)
- beaten-down basket over the same holding periods: mean +1.00% (excess +0.69%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 21, closed: 0, open: 21
- open trades mark-to-market: mean -1.54%, hit 42%
- SPY over the same holding periods: mean +0.23% (excess -1.78%)
- beaten-down basket over the same holding periods: mean +3.07% (excess -4.61%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             36 |          60 | +3.99%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             36 |          60 | -24.85% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.71   |             35 |          60 | -17.50% |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      632      |             34 |          60 | +10.37% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             35 |         120 | +6.56%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             33 |          60 | +9.55%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             30 |          60 | -3.50%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             30 |         120 | +10.13% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             33 |         120 | -9.88%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             27 |          60 | -12.95% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             23 |          60 | -17.65% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             20 |          60 | +14.90% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             18 |          60 | -6.10%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             18 |          60 | +12.66% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |       79.5    |             18 |          20 | +1.31%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)     | 2026-10-01    | 2026-10-02   |      238.11   |             18 |          20 | +1.17%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)     | 2026-10-01    | 2026-10-02   |      273.31   |             18 |          20 | +6.57%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)     | 2026-10-01    | 2026-10-02   |      162.22   |             18 |          20 | +13.32% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)     | 2026-10-01    | 2026-10-02   |       30.98   |             18 |          20 | +12.52% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |       79.5    |             18 |          20 | +1.31%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE)   | 2026-10-01    | 2026-10-02   |      222.597  |             18 |          20 | +10.91% |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-01    | 2026-10-02   |      121.94   |             18 |          20 | +14.52% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-01    | 2026-10-02   |      119.24   |             18 |          20 | -6.58%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-01    | 2026-10-02   |      101.99   |             18 |          20 | -8.95%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-01    | 2026-10-02   |      141.566  |             18 |          20 | -7.80%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             17 |          60 | +11.06% |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)     | 2026-10-02    | 2026-10-05   |       47.64   |             17 |          20 | +7.54%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK)   | 2026-10-02    | 2026-10-05   |      163.81   |             17 |          20 | +14.60% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             16 |          60 | +1.96%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-05    | 2026-10-06   |       84.2    |             16 |          20 | +10.04% |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-05    | 2026-10-06   |       77.73   |             16 |          20 | +0.86%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-05    | 2026-10-06   |       83.45   |             16 |          20 | +7.63%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-10-05    | 2026-10-06   |      134.94   |             16 |          20 | +3.90%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |       99.81   |             16 |          20 | -9.44%  |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |      529.14   |             16 |          20 | +6.07%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             16 |          20 | +1.96%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |       99.81   |             16 |          20 | -9.44%  |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |      529.14   |             16 |          20 | +6.07%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV)   | 2026-10-06    | 2026-10-07   |       44.35   |             15 |          20 | -1.58%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-06    | 2026-10-07   |      103.16   |             15 |          20 | +8.02%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-06    | 2026-10-07   |      103.39   |             15 |          20 | -10.18% |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-10-06    | 2026-10-07   |       15.15   |             15 |          20 | +3.96%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)       | 2026-10-06    | 2026-10-07   |       40.61   |             15 |          20 | +7.36%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)     | 2026-10-06    | 2026-10-07   |       52.59   |             15 |          20 | +7.00%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)     | 2026-10-06    | 2026-10-07   |      128.11   |             15 |          20 | +3.56%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)     | 2026-10-06    | 2026-10-07   |       33.7    |             15 |          20 | +4.39%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)     | 2026-10-06    | 2026-10-07   |       38.17   |             15 |          20 | +9.96%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-06    | 2026-10-07   |       71.68   |             15 |          20 | +1.59%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)     | 2026-10-06    | 2026-10-07   |      102.99   |             15 |          20 | +5.28%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST)   | 2026-10-06    | 2026-10-07   |      940.84   |             15 |          20 | +5.45%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |      107.5    |             14 |          20 | -11.38% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |      107.5    |             14 |          20 | -11.38% |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-07    | 2026-10-08   |      642      |             14 |          20 | +8.65%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-07    | 2026-10-08   |      126.47   |             14 |          20 | -3.81%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-08    | 2026-10-09   |       85.58   |             13 |          20 | +4.95%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)     | 2026-10-08    | 2026-10-09   |      123.25   |             13 |          20 | +5.99%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)     | 2026-10-08    | 2026-10-09   |       73.04   |             13 |          20 | +7.11%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-08    | 2026-10-09   |       82.91   |             13 |          20 | -2.86%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-08    | 2026-10-09   |       30.02   |             13 |          20 | +6.63%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-10-08    | 2026-10-09   |      309.25   |             13 |          20 | +0.90%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-10-08    | 2026-10-09   |      305.05   |             13 |          20 | +7.67%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)     | 2026-10-08    | 2026-10-09   |      110      |             13 |          20 | +8.47%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)     | 2026-10-08    | 2026-10-09   |       37.61   |             13 |          20 | +4.89%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-08    | 2026-10-09   |      155.51   |             13 |          20 | -5.58%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)       | 2026-10-08    | 2026-10-09   |       44.83   |             13 |          20 | +3.21%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)     | 2026-10-08    | 2026-10-09   |      116.26   |             13 |          20 | +7.35%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-08    | 2026-10-09   |       85.94   |             13 |          20 | +7.81%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-08    | 2026-10-09   |      144      |             13 |          20 | +3.85%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)     | 2026-10-08    | 2026-10-09   |       73.17   |             13 |          20 | +6.79%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             12 |          60 | -1.85%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             12 |          60 | -5.93%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-09    | 2026-10-12   |      143.23   |             12 |          20 | +6.09%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |       81.45   |             12 |          20 | +4.37%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC)   | 2026-10-09    | 2026-10-12   |      181.77   |             12 |          20 | +1.36%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-10-09    | 2026-10-12   |       33.62   |             12 |          20 | -4.10%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-09    | 2026-10-12   |       81.41   |             12 |          20 | -3.70%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-09    | 2026-10-12   |       53.56   |             12 |          20 | +4.09%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |       81.45   |             12 |          20 | +4.37%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)     | 2026-10-09    | 2026-10-12   |      161.66   |             12 |          20 | +6.01%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-09    | 2026-10-12   |      366.01   |             12 |          20 | -9.72%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-09    | 2026-10-12   |      103.99   |             12 |          20 | +7.15%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)     | 2026-10-09    | 2026-10-12   |       65.9    |             12 |          20 | +6.28%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)     | 2026-10-09    | 2026-10-12   |      123.2    |             12 |          20 | +5.76%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-12    | 2026-10-13   |      486.79   |             11 |          20 | +13.24% |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-12    | 2026-10-13   |      147.47   |             11 |          20 | +1.40%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD)   | 2026-10-12    | 2026-10-13   |      140.79   |             11 |          20 | +6.42%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-10-12    | 2026-10-13   |       13.21   |             11 |          20 | -1.89%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)     | 2026-10-12    | 2026-10-13   |       56.04   |             11 |          20 | +3.84%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)     | 2026-10-12    | 2026-10-13   |       66.28   |             11 |          20 | +4.10%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)     | 2026-10-12    | 2026-10-13   |       42.6    |             11 |          20 | +4.93%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)     | 2026-10-12    | 2026-10-13   |     1113.01   |             11 |          20 | +1.55%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC)   | 2026-10-12    | 2026-10-13   |       67.7021 |             11 |          20 | +5.03%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |       32.85   |             10 |          20 | +8.43%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |      182.6    |             10 |          20 | +2.43%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |       67.9    |             10 |          20 | +9.26%  |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |      220.63   |             10 |          20 | +4.05%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |       57.66   |             10 |          20 | +7.63%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |      191.79   |             10 |          20 | +7.50%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |              9 |          60 | -3.03%  |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |       33.27   |              9 |          20 | +2.22%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |      342.5    |              9 |          20 | +2.53%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |      153.24   |              9 |          20 | +14.66% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |       61.37   |              9 |          20 | +9.87%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |      531      |              9 |          20 | +17.32% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |              8 |          60 | -8.63%  |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |              8 |          20 | -10.56% |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |       27.96   |              8 |          20 | +3.43%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |       83.4    |              8 |          20 | +2.84%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |      529.98   |              8 |          20 | +0.12%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |      357.38   |              8 |          20 | +4.10%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |     3091      |              8 |          20 | +1.69%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |       13.29   |              8 |          20 | -4.44%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |       36.42   |              8 |          20 | -2.22%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |      120.66   |              8 |          20 | -7.68%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |      295.89   |              8 |          20 | +1.87%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |       69.87   |              8 |          20 | -10.52% |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |       44.45   |              8 |          20 | +1.37%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |       29.93   |              8 |          20 | +12.86% |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |      125.05   |              8 |          20 | +11.67% |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |      244.31   |              8 |          20 | +2.11%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |      150.37   |              8 |          20 | +1.05%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |      505.78   |              8 |          20 | -0.41%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |      195.819  |              8 |          20 | +1.21%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |       37.67   |              8 |          20 | -0.29%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |       86.69   |              8 |          20 | +0.77%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |       79.6    |              8 |          20 | +3.54%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |      255.41   |              8 |          20 | +2.78%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |      170.42   |              8 |          20 | -3.47%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |              8 |          20 | -10.56% |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |      169.41   |              7 |          20 | -2.89%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |       45.99   |              7 |          20 | +3.24%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |      511      |              7 |          20 | +7.87%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |       57.29   |              7 |          20 | +4.52%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |      289.03   |              7 |          20 | +4.66%  |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |      268.28   |              7 |          20 | +4.86%  |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |      245.16   |              7 |          20 | +5.81%  |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |       47.42   |              7 |          20 | -0.04%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |       23.48   |              7 |          20 | +0.94%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |              7 |          20 | +2.00%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |      104.16   |              7 |          20 | -10.85% |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |       55.8    |              7 |          20 | +1.83%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |      306.55   |              7 |          20 | +3.90%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |       33.45   |              7 |          20 | +6.49%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |              7 |         120 | +2.00%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |      454.74   |              6 |          20 | -4.50%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |      111.74   |              5 |          20 | +4.44%  |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |       55.27   |              5 |          20 | +0.87%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |              5 |          20 | +4.59%  |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |       86.03   |              5 |          20 | -0.30%  |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |       21.94   |              5 |          20 | -0.46%  |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |       78.84   |              5 |          20 | +7.28%  |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |      545      |              5 |          20 | -2.64%  |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |       77.73   |              5 |          20 | +0.58%  |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |       56.51   |              5 |          20 | +2.34%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |      189.29   |              5 |          20 | -1.19%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |      227.11   |              5 |          20 | +1.08%  |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |      465.97   |              5 |          20 | -6.80%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |       62.31   |              5 |          20 | +1.36%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |      338.03   |              5 |          20 | +1.27%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |      281.5    |              5 |          20 | +0.64%  |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |              5 |          20 | +4.59%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |      363.84   |              4 |          20 | +2.26%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | 2026-10-22   |      264.64   |              4 |          20 | -0.81%  |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | 2026-10-22   |      509.34   |              4 |          20 | -1.11%  |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |      544.7    |              4 |          20 | +1.20%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |       77.57   |              4 |          20 | +9.04%  |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |       85.6    |              4 |          20 | +2.06%  |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    | 2026-10-23   |       54.61   |              3 |          20 | +14.06% |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |              3 |          20 | +0.04%  |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    | 2026-10-23   |      818.29   |              3 |          20 | -15.47% |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    | 2026-10-23   |       28.89   |              3 |          20 | +0.10%  |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |              3 |          20 | -3.23%  |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    | 2026-10-23   |      117.97   |              3 |          20 | +3.10%  |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |              3 |          20 | -0.25%  |
| jev_pick                  | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |              3 |          20 | -0.25%  |
| jev_pick                  | [ISRG](https://www.tradingview.com/chart/?symbol=ISRG)   | 2026-10-22    | 2026-10-23   |      443.65   |              3 |          20 | +0.50%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-10-22    | 2026-10-23   |      126.05   |              3 |          20 | +0.33%  |
| jev_skip                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-22    | 2026-10-23   |       13      |              3 |          20 | -2.31%  |
| jev_skip                  | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |              3 |          20 | +0.04%  |
| jev_skip                  | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |              3 |          20 | -3.23%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |              2 |          60 | +9.67%  |
| jev_pick                  | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |              2 |          20 | +9.67%  |
| jev_pick                  | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-23    | 2026-10-26   |      699.26   |              2 |          20 | -0.25%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1706.46   |              1 |          60 | -1.52%  |
| jev_pick                  | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-26    | 2026-10-27   |      280.98   |              1 |          20 | +0.12%  |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    |              |               |            nan |          60 |         |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    |              |               |            nan |          60 |         |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-27    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-10-27    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-27    |              |               |            nan |          20 |         |