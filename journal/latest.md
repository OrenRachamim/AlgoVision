# Forward-test journal - 2026-10-30

Data through 2026-10-30; 518 of 518 symbols loaded.

## New signals today (4)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                                |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:--------------------------------------------------------------------|
| newsday                 | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT) | 2026-10-30    |       91.73 |          60 | gap -22.6%, vol 6.7x, 6m -45%, vs MA200 -42%                        |
| newsday                 | [INTC](https://www.tradingview.com/chart/?symbol=INTC) | 2026-10-30    |       65.76 |          60 | gap -25.8%, vol 4.6x, 6m -34%, vs MA200 -24%                        |
| insider_buy_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-29    |       92.4  |         120 | 1 buy(s) $0.99M @ 89.60, 6m -19%, vs MA200 -21%; KOCH D CHRISTIAN   |
| early_rally_beaten_down | [WY](https://www.tradingview.com/chart/?symbol=WY)     | 2026-10-30    |       20.35 |          20 | higher_high, rsi_turn; day +3.0%, 10d +3.8%, 6m -14%, vs MA200 -13% |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      109 |        0 | +4.31% | 75%   | +6.46%   | +1.00%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       35 |       12 | +2.38% | 66%   | +3.83%   | -0.79%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        5 |        0 | +2.64% | 80%   | +3.49%   | +0.48%             |
| jev_pick                  | untested (forward test only)                     |       34 |       12 | +3.08% | 65%   | +4.36%   | -1.45%             |
| jev_skip                  | untested; a fall is the success case             |        6 |        0 | +5.33% | 67%   | +6.40%   | +3.85%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       31 |        0 | -1.14% | 41%   | +0.37%   | -4.09%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 109, closed: 0, open: 109
- open trades mark-to-market: mean +4.31%, hit 75%
- SPY over the same holding periods: mean -2.15% (excess +6.46%)
- beaten-down basket over the same holding periods: mean +3.32% (excess +1.00%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 35, closed: 12, open: 23
- closed trades: mean +1.08%, median +3.50%, hit 67%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +3.05%, hit 65%
- SPY over the same holding periods: mean -1.45% (excess +3.83%)
- beaten-down basket over the same holding periods: mean +3.16% (excess -0.79%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 5, closed: 0, open: 5
- open trades mark-to-market: mean +2.64%, hit 80%
- SPY over the same holding periods: mean -0.85% (excess +3.49%)
- beaten-down basket over the same holding periods: mean +2.16% (excess +0.48%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 34, closed: 12, open: 22
- closed trades: mean +6.97%, median +9.77%, hit 67%, best +19.8%, worst -11.0%
- open trades mark-to-market: mean +0.95%, hit 64%
- SPY over the same holding periods: mean -1.28% (excess +4.36%)
- beaten-down basket over the same holding periods: mean +4.53% (excess -1.45%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 6, closed: 0, open: 6
- open trades mark-to-market: mean +5.33%, hit 67%
- SPY over the same holding periods: mean -1.07% (excess +6.40%)
- beaten-down basket over the same holding periods: mean +1.48% (excess +3.85%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 31, closed: 0, open: 31
- open trades mark-to-market: mean -1.14%, hit 41%
- SPY over the same holding periods: mean -1.51% (excess +0.37%)
- beaten-down basket over the same holding periods: mean +2.95% (excess -4.09%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             39 |          60 | +6.62%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             39 |          60 | -22.74% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.71   |             38 |          60 | -14.39% |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      632      |             37 |          60 | +7.63%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             38 |         120 | +9.02%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             36 |          60 | +8.95%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             33 |          60 | -3.07%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             33 |         120 | +9.53%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             36 |         120 | -10.60% |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             30 |          60 | -13.56% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             26 |          60 | -11.86% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             23 |          60 | +18.14% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             21 |          60 | -6.02%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             21 |          60 | +15.84% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             20 |          60 | +14.34% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             19 |          60 | -11.52% |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-05    | 2026-10-06   |       84.2    |             19 |          20 | +11.29% |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-05    | 2026-10-06   |       77.73   |             19 |          20 | +1.13%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-05    | 2026-10-06   |       83.45   |             19 |          20 | +5.60%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-10-05    | 2026-10-06   |      134.94   |             19 |          20 | +3.98%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |       99.81   |             19 |          20 | -2.88%  |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |      529.14   |             19 |          20 | +4.17%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             19 |          20 | -11.52% |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |       99.81   |             19 |          20 | -2.88%  |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |      529.14   |             19 |          20 | +4.17%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV)   | 2026-10-06    | 2026-10-07   |       44.35   |             18 |          20 | -0.95%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-06    | 2026-10-07   |      103.16   |             18 |          20 | +12.51% |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-06    | 2026-10-07   |      103.39   |             18 |          20 | -10.63% |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-10-06    | 2026-10-07   |       15.15   |             18 |          20 | +15.97% |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)       | 2026-10-06    | 2026-10-07   |       40.61   |             18 |          20 | +9.75%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)     | 2026-10-06    | 2026-10-07   |       52.59   |             18 |          20 | +5.31%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)     | 2026-10-06    | 2026-10-07   |      128.11   |             18 |          20 | +5.76%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)     | 2026-10-06    | 2026-10-07   |       33.7    |             18 |          20 | +5.79%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)     | 2026-10-06    | 2026-10-07   |       38.17   |             18 |          20 | +11.19% |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-06    | 2026-10-07   |       71.68   |             18 |          20 | +3.64%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)     | 2026-10-06    | 2026-10-07   |      102.99   |             18 |          20 | +6.91%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST)   | 2026-10-06    | 2026-10-07   |      940.84   |             18 |          20 | +7.59%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |      107.5    |             17 |          20 | -10.64% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |      107.5    |             17 |          20 | -10.64% |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-07    | 2026-10-08   |      642      |             17 |          20 | +5.95%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-07    | 2026-10-08   |      126.47   |             17 |          20 | +1.88%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-08    | 2026-10-09   |       85.58   |             16 |          20 | +2.97%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)     | 2026-10-08    | 2026-10-09   |      123.25   |             16 |          20 | +9.80%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)     | 2026-10-08    | 2026-10-09   |       73.04   |             16 |          20 | +9.15%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-08    | 2026-10-09   |       82.91   |             16 |          20 | -1.11%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-08    | 2026-10-09   |       30.02   |             16 |          20 | +0.50%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-10-08    | 2026-10-09   |      309.25   |             16 |          20 | +1.44%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-10-08    | 2026-10-09   |      305.05   |             16 |          20 | +11.81% |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)     | 2026-10-08    | 2026-10-09   |      110      |             16 |          20 | +12.28% |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)     | 2026-10-08    | 2026-10-09   |       37.61   |             16 |          20 | +6.67%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-08    | 2026-10-09   |      155.51   |             16 |          20 | +0.60%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)       | 2026-10-08    | 2026-10-09   |       44.83   |             16 |          20 | +4.64%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)     | 2026-10-08    | 2026-10-09   |      116.26   |             16 |          20 | +9.57%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-08    | 2026-10-09   |       85.94   |             16 |          20 | +9.04%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-08    | 2026-10-09   |      144      |             16 |          20 | +7.92%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)     | 2026-10-08    | 2026-10-09   |       73.17   |             16 |          20 | +9.09%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             15 |          60 | +4.57%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             15 |          60 | -3.82%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-09    | 2026-10-12   |      143.23   |             15 |          20 | +4.65%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |       81.45   |             15 |          20 | +5.66%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC)   | 2026-10-09    | 2026-10-12   |      181.77   |             15 |          20 | +2.96%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-10-09    | 2026-10-12   |       33.62   |             15 |          20 | +0.95%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-09    | 2026-10-12   |       81.41   |             15 |          20 | -3.44%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-09    | 2026-10-12   |       53.56   |             15 |          20 | +6.50%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |       81.45   |             15 |          20 | +5.66%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)     | 2026-10-09    | 2026-10-12   |      161.66   |             15 |          20 | +6.65%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-09    | 2026-10-12   |      366.01   |             15 |          20 | -9.38%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-09    | 2026-10-12   |      103.99   |             15 |          20 | +11.62% |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)     | 2026-10-09    | 2026-10-12   |       65.9    |             15 |          20 | +8.73%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)     | 2026-10-09    | 2026-10-12   |      123.2    |             15 |          20 | +5.69%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-12    | 2026-10-13   |      486.79   |             14 |          20 | +14.53% |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-12    | 2026-10-13   |      147.47   |             14 |          20 | +5.38%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD)   | 2026-10-12    | 2026-10-13   |      140.79   |             14 |          20 | +6.31%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-10-12    | 2026-10-13   |       13.21   |             14 |          20 | -0.23%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)     | 2026-10-12    | 2026-10-13   |       56.04   |             14 |          20 | +4.91%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)     | 2026-10-12    | 2026-10-13   |       66.28   |             14 |          20 | +5.76%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)     | 2026-10-12    | 2026-10-13   |       42.6    |             14 |          20 | +8.36%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)     | 2026-10-12    | 2026-10-13   |     1113.01   |             14 |          20 | +3.04%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC)   | 2026-10-12    | 2026-10-13   |       67.7021 |             14 |          20 | +13.10% |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |       32.85   |             13 |          20 | +10.11% |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |      182.6    |             13 |          20 | -5.50%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |       67.9    |             13 |          20 | +11.56% |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |      220.63   |             13 |          20 | +8.18%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |       57.66   |             13 |          20 | +9.38%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |      191.79   |             13 |          20 | +8.32%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             12 |          60 | -10.68% |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |       33.27   |             12 |          20 | +4.18%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |      342.5    |             12 |          20 | -6.36%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |      153.24   |             12 |          20 | +20.46% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |       61.37   |             12 |          20 | +11.85% |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |      531      |             12 |          20 | +19.95% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             11 |          60 | -15.84% |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             11 |          20 | -5.27%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |       27.96   |             11 |          20 | +7.76%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |       83.4    |             11 |          20 | +8.88%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |      529.98   |             11 |          20 | -5.64%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |      357.38   |             11 |          20 | -3.72%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |     3091      |             11 |          20 | +2.55%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |       13.29   |             11 |          20 | -7.52%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |       36.42   |             11 |          20 | +5.85%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |      120.66   |             11 |          20 | -3.62%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |      295.89   |             11 |          20 | -1.36%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |       69.87   |             11 |          20 | -11.15% |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |       44.45   |             11 |          20 | -5.56%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |       29.93   |             11 |          20 | +15.94% |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |      125.05   |             11 |          20 | +14.34% |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |      244.31   |             11 |          20 | +5.65%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |      150.37   |             11 |          20 | -0.32%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |      505.78   |             11 |          20 | +6.85%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |      195.819  |             11 |          20 | +6.77%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |       37.67   |             11 |          20 | +2.65%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |       85.4496 |             11 |          20 | +2.98%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |       79.6    |             11 |          20 | +5.16%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |      255.41   |             11 |          20 | +10.12% |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |      170.42   |             11 |          20 | -2.82%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             11 |          20 | -5.27%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |      169.41   |             10 |          20 | -2.24%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |       45.99   |             10 |          20 | +2.83%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |      511      |             10 |          20 | +9.11%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |       57.29   |             10 |          20 | +3.94%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |      289.03   |             10 |          20 | +11.29% |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |      268.28   |             10 |          20 | +18.12% |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |      245.16   |             10 |          20 | +13.24% |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |       47.42   |             10 |          20 | +5.48%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |       23.48   |             10 |          20 | +4.17%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             10 |          20 | +4.94%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |      104.16   |             10 |          20 | -11.29% |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |       55.8    |             10 |          20 | +2.03%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |      306.55   |             10 |          20 | +7.39%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |       33.45   |             10 |          20 | +8.13%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             10 |         120 | +4.94%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |      454.74   |              9 |          20 | -7.10%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |      111.74   |              8 |          20 | +6.06%  |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |       55.27   |              8 |          20 | +3.20%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |              8 |          20 | +7.24%  |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |       86.03   |              8 |          20 | +5.56%  |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |       21.94   |              8 |          20 | +5.83%  |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |       78.84   |              8 |          20 | +10.27% |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |      545      |              8 |          20 | -8.24%  |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |       77.73   |              8 |          20 | +10.25% |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |       56.269  |              8 |          20 | -4.69%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |      189.29   |              8 |          20 | -8.84%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |      227.11   |              8 |          20 | +5.09%  |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |      465.97   |              8 |          20 | -9.34%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |       62.31   |              8 |          20 | +4.22%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |      338.03   |              8 |          20 | -3.54%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |      281.5    |              8 |          20 | -3.12%  |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |              8 |          20 | +7.24%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |      363.84   |              7 |          20 | -5.43%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | 2026-10-22   |      264.64   |              7 |          20 | +6.28%  |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | 2026-10-22   |      509.34   |              7 |          20 | +6.10%  |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |      544.7    |              7 |          20 | +2.36%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |       77.57   |              7 |          20 | +12.08% |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |       84.3752 |              7 |          20 | +4.30%  |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    | 2026-10-23   |       54.61   |              6 |          20 | +21.33% |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |              6 |          20 | +14.52% |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    | 2026-10-23   |      818.29   |              6 |          20 | -13.08% |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    | 2026-10-23   |       28.89   |              6 |          20 | +4.29%  |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |              6 |          20 | -0.69%  |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    | 2026-10-23   |      117.97   |              6 |          20 | +5.74%  |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |              6 |          20 | +2.43%  |
| jev_pick                  | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |              6 |          20 | +2.43%  |
| jev_pick                  | [ISRG](https://www.tradingview.com/chart/?symbol=ISRG)   | 2026-10-22    | 2026-10-23   |      443.65   |              6 |          20 | -2.62%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-10-22    | 2026-10-23   |      126.05   |              6 |          20 | +1.53%  |
| jev_skip                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-22    | 2026-10-23   |       13      |              6 |          20 | -5.46%  |
| jev_skip                  | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |              6 |          20 | +14.52% |
| jev_skip                  | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |              6 |          20 | -0.69%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |              5 |          60 | +4.91%  |
| jev_pick                  | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |              5 |          20 | +4.91%  |
| jev_pick                  | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-23    | 2026-10-26   |      699.26   |              5 |          20 | -2.73%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |              4 |          60 | -4.62%  |
| jev_pick                  | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-26    | 2026-10-27   |      280.98   |              4 |          20 | +12.78% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       91      |              3 |          60 | +1.54%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |              3 |          60 | -5.00%  |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-27    | 2026-10-28   |       58.64   |              3 |          20 | +16.46% |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-10-27    | 2026-10-28   |       56.79   |              3 |          20 | -2.75%  |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-27    | 2026-10-28   |       54.22   |              3 |          20 | +1.97%  |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |              2 |          60 | +5.87%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |              2 |          60 | +0.41%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |              2 |          60 | -2.29%  |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |              2 |          60 | +8.96%  |
| falling_wedge_beaten_down | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-10-28    | 2026-10-29   |       94.96   |              2 |          20 | -4.17%  |
| early_rally_beaten_down   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |              2 |          20 | -2.29%  |
| early_rally_beaten_down   | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-28    | 2026-10-29   |      342      |              2 |          20 | -4.65%  |
| early_rally_beaten_down   | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-28    | 2026-10-29   |      144.14   |              2 |          20 | -9.35%  |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.695  |              1 |          60 | -4.46%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.09   |              1 |          60 | -0.44%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.613  |              1 |          60 | -0.50%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |              1 |          60 | -0.04%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              1 |          20 | +0.53%  |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      260      |              1 |          20 | +0.92%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              1 |          20 | +0.53%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    |              |               |            nan |          60 |         |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    |              |               |            nan |          60 |         |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       92.11   |              1 |         120 | +0.31%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    |              |               |            nan |          20 |         |