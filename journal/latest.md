# Forward-test journal - 2026-10-21

Data through 2026-10-21; 518 of 518 symbols loaded.

## New signals today (1)

| rule                    | symbol                                               | signal_date   |   ref_price |   hold_bars | note                                                   |
|:------------------------|:-----------------------------------------------------|:--------------|------------:|------------:|:-------------------------------------------------------|
| early_rally_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII) | 2026-10-21    |      366.37 |          20 | rsi_turn; day +0.7%, 10d +2.2%, 6m -25%, vs MA200 -23% |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       94 |        0 | +1.84% | 71%   | +1.92%   | +0.12%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       33 |        8 | +1.78% | 67%   | +1.64%   | -0.04%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        4 |        0 | +2.72% | 75%   | +1.32%   | +1.95%             |
| jev_pick                  | untested (forward test only)                     |       24 |        0 | +3.39% | 71%   | +3.28%   | -0.34%             |
| jev_skip                  | untested; a fall is the success case             |        1 |        0 | -3.46% | 0%    | -3.71%   | -2.97%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       17 |        0 | +1.67% | 53%   | +1.04%   | -0.74%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 94, closed: 0, open: 94
- open trades mark-to-market: mean +1.84%, hit 71%
- SPY over the same holding periods: mean -0.08% (excess +1.92%)
- beaten-down basket over the same holding periods: mean +1.72% (excess +0.12%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 33, closed: 8, open: 25
- closed trades: mean -0.40%, median +0.29%, hit 50%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +2.48%, hit 72%
- SPY over the same holding periods: mean +0.13% (excess +1.64%)
- beaten-down basket over the same holding periods: mean +1.81% (excess -0.04%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 4, closed: 0, open: 4
- open trades mark-to-market: mean +2.72%, hit 75%
- SPY over the same holding periods: mean +1.40% (excess +1.32%)
- beaten-down basket over the same holding periods: mean +0.76% (excess +1.95%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 24, closed: 0, open: 24
- open trades mark-to-market: mean +3.39%, hit 71%
- SPY over the same holding periods: mean +0.10% (excess +3.28%)
- beaten-down basket over the same holding periods: mean +3.72% (excess -0.34%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 1, closed: 0, open: 1
- open trades mark-to-market: mean -3.46%, hit 0%
- SPY over the same holding periods: mean +0.25% (excess -3.71%)
- beaten-down basket over the same holding periods: mean -0.49% (excess -2.97%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 17, closed: 0, open: 17
- open trades mark-to-market: mean +1.67%, hit 53%
- SPY over the same holding periods: mean +0.63% (excess +1.04%)
- beaten-down basket over the same holding periods: mean +2.41% (excess -0.74%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |       100.58  |             32 |          60 | -4.03%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |       920.51  |             32 |          60 | -13.61% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |       232.71  |             31 |          60 | -10.55% |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |       632     |             30 |          60 | +10.00% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |        52.32  |             31 |         120 | +6.84%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |        54.66  |             29 |          60 | +7.89%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |       441.33  |             26 |          60 | -8.78%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |        54.37  |             26 |         120 | +8.46%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |        72.99  |             29 |         120 | -7.36%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |        71.82  |             23 |          60 | -9.44%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |        33.99  |             19 |          60 | -15.06% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-09-24    | 2026-09-25   |       366.7   |             19 |          20 | -0.09%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-09-25    | 2026-09-28   |        14.45  |             18 |          20 | +7.89%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-09-28    | 2026-09-29   |        36.34  |             17 |          20 | +3.27%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |       602.02  |             16 |          60 | +32.09% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |        12.385 |             14 |          60 | +2.70%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |       614     |             14 |          60 | +29.51% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |        79.5   |             14 |          20 | +7.53%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)     | 2026-10-01    | 2026-10-02   |       238.11  |             14 |          20 | +1.54%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)     | 2026-10-01    | 2026-10-02   |       273.31  |             14 |          20 | +5.41%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)     | 2026-10-01    | 2026-10-02   |       162.22  |             14 |          20 | +9.51%  |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)     | 2026-10-01    | 2026-10-02   |        30.98  |             14 |          20 | +11.27% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |        79.5   |             14 |          20 | +7.53%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE)   | 2026-10-01    | 2026-10-02   |       222.597 |             14 |          20 | +9.67%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-01    | 2026-10-02   |       121.94  |             14 |          20 | +5.98%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-01    | 2026-10-02   |       119.24  |             14 |          20 | -3.42%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-01    | 2026-10-02   |       101.99  |             14 |          20 | +4.27%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-01    | 2026-10-02   |       141.566 |             14 |          20 | -8.78%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |        33.82  |             13 |          60 | +10.97% |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)     | 2026-10-02    | 2026-10-05   |        47.64  |             13 |          20 | +4.68%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK)   | 2026-10-02    | 2026-10-05   |       163.81  |             13 |          20 | +17.42% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |       140.83  |             12 |          60 | +0.09%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-05    | 2026-10-06   |        84.2   |             12 |          20 | +7.35%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-05    | 2026-10-06   |        77.73  |             12 |          20 | +1.27%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-05    | 2026-10-06   |        83.45  |             12 |          20 | +6.89%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-10-05    | 2026-10-06   |       134.94  |             12 |          20 | +7.84%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |        99.81  |             12 |          20 | -7.18%  |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |       529.14  |             12 |          20 | +4.60%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |       140.83  |             12 |          20 | +0.09%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |        99.81  |             12 |          20 | -7.18%  |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |       529.14  |             12 |          20 | +4.60%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV)   | 2026-10-06    | 2026-10-07   |        44.35  |             11 |          20 | -0.02%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-06    | 2026-10-07   |       103.16  |             11 |          20 | +5.18%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-06    | 2026-10-07   |       103.39  |             11 |          20 | +2.86%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-10-06    | 2026-10-07   |        15.15  |             11 |          20 | +2.90%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)       | 2026-10-06    | 2026-10-07   |        40.61  |             11 |          20 | +5.86%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)     | 2026-10-06    | 2026-10-07   |        52.59  |             11 |          20 | +2.81%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)     | 2026-10-06    | 2026-10-07   |       128.11  |             11 |          20 | +1.20%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)     | 2026-10-06    | 2026-10-07   |        33.7   |             11 |          20 | +2.61%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)     | 2026-10-06    | 2026-10-07   |        38.17  |             11 |          20 | +5.63%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-06    | 2026-10-07   |        71.68  |             11 |          20 | -0.95%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)     | 2026-10-06    | 2026-10-07   |       102.99  |             11 |          20 | +3.00%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST)   | 2026-10-06    | 2026-10-07   |       940.84  |             11 |          20 | +6.11%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |       107.5   |             10 |          20 | -7.16%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |       107.5   |             10 |          20 | -7.16%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-07    | 2026-10-08   |       642     |             10 |          20 | +8.29%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-07    | 2026-10-08   |       126.47  |             10 |          20 | +6.47%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-08    | 2026-10-09   |        85.58  |              9 |          20 | +4.23%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)     | 2026-10-08    | 2026-10-09   |       123.25  |              9 |          20 | +7.12%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)     | 2026-10-08    | 2026-10-09   |        73.04  |              9 |          20 | +9.01%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-08    | 2026-10-09   |        82.91  |              9 |          20 | +3.11%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-08    | 2026-10-09   |        30.02  |              9 |          20 | +9.59%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-10-08    | 2026-10-09   |       309.25  |              9 |          20 | +0.61%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-10-08    | 2026-10-09   |       305.05  |              9 |          20 | +10.02% |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)     | 2026-10-08    | 2026-10-09   |       110     |              9 |          20 | +7.09%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)     | 2026-10-08    | 2026-10-09   |        37.61  |              9 |          20 | +4.95%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-08    | 2026-10-09   |       155.51  |              9 |          20 | -1.13%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)       | 2026-10-08    | 2026-10-09   |        44.83  |              9 |          20 | +1.52%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)     | 2026-10-08    | 2026-10-09   |       116.26  |              9 |          20 | +3.79%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-08    | 2026-10-09   |        85.94  |              9 |          20 | +5.18%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-08    | 2026-10-09   |       144     |              9 |          20 | +5.03%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)     | 2026-10-08    | 2026-10-09   |        73.17  |              9 |          20 | +4.93%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |       149.6   |              8 |          60 | +2.77%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |        22.26  |              8 |          60 | -1.57%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-09    | 2026-10-12   |       143.23  |              8 |          20 | +5.68%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |        81.45  |              8 |          20 | +2.52%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC)   | 2026-10-09    | 2026-10-12   |       181.77  |              8 |          20 | -4.60%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-10-09    | 2026-10-12   |        33.62  |              8 |          20 | -2.77%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-09    | 2026-10-12   |        81.41  |              8 |          20 | -3.30%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-09    | 2026-10-12   |        53.56  |              8 |          20 | +4.37%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |        81.45  |              8 |          20 | +2.52%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)     | 2026-10-09    | 2026-10-12   |       161.66  |              8 |          20 | +3.27%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-09    | 2026-10-12   |       366.01  |              8 |          20 | -5.93%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-09    | 2026-10-12   |       103.99  |              8 |          20 | +4.34%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)     | 2026-10-09    | 2026-10-12   |        65.9   |              8 |          20 | +3.78%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)     | 2026-10-09    | 2026-10-12   |       123.2   |              8 |          20 | +3.40%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-12    | 2026-10-13   |       486.79  |              7 |          20 | +10.79% |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-12    | 2026-10-13   |       147.47  |              7 |          20 | +2.56%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD)   | 2026-10-12    | 2026-10-13   |       140.79  |              7 |          20 | +0.79%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-10-12    | 2026-10-13   |        13.21  |              7 |          20 | -0.45%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)     | 2026-10-12    | 2026-10-13   |        56.04  |              7 |          20 | +2.05%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)     | 2026-10-12    | 2026-10-13   |        66.28  |              7 |          20 | +2.79%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)     | 2026-10-12    | 2026-10-13   |        42.6   |              7 |          20 | +1.06%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)     | 2026-10-12    | 2026-10-13   |      1113.01  |              7 |          20 | +1.47%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC)   | 2026-10-12    | 2026-10-13   |        67.74  |              7 |          20 | +1.87%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |        32.85  |              6 |          20 | +3.47%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |       182.6   |              6 |          20 | +3.45%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |        67.9   |              6 |          20 | +6.55%  |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |       220.63  |              6 |          20 | +3.32%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |        57.66  |              6 |          20 | +3.45%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |       191.79  |              6 |          20 | +4.20%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |        61.43  |              5 |          60 | +0.63%  |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |        33.27  |              5 |          20 | +0.54%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |       342.5   |              5 |          20 | +5.50%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |       153.24  |              5 |          20 | +14.57% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |        61.37  |              5 |          20 | +3.10%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |       531     |              5 |          20 | +3.86%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |        65.195 |              4 |          60 | -5.18%  |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |       136.02  |              4 |          20 | -1.01%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |        27.96  |              4 |          20 | -1.34%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |        83.4   |              4 |          20 | +3.15%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |       529.98  |              4 |          20 | +2.31%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |       357.38  |              4 |          20 | +2.52%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |      3091     |              4 |          20 | +2.13%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |        13.29  |              4 |          20 | -5.27%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |        36.42  |              4 |          20 | -0.00%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |       120.66  |              4 |          20 | -4.56%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |       295.89  |              4 |          20 | +0.58%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |        69.87  |              4 |          20 | -6.91%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |        44.45  |              4 |          20 | +0.13%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |        29.93  |              4 |          20 | +1.50%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |       125.05  |              4 |          20 | +3.34%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |       244.31  |              4 |          20 | +0.79%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |       150.37  |              4 |          20 | +0.67%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |       505.78  |              4 |          20 | +0.64%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |       197.06  |              4 |          20 | -0.25%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |        37.67  |              4 |          20 | -0.37%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |        86.69  |              4 |          20 | -2.21%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |        79.6   |              4 |          20 | -1.66%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |       255.41  |              4 |          20 | +3.61%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |       170.42  |              4 |          20 | -1.53%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |       136.02  |              4 |          20 | -1.01%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |       169.41  |              3 |          20 | -0.94%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |        45.99  |              3 |          20 | +0.72%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |       511     |              3 |          20 | +5.54%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |        57.29  |              3 |          20 | +2.93%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |       289.03  |              3 |          20 | +1.84%  |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |       268.28  |              3 |          20 | +2.11%  |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |       245.16  |              3 |          20 | +0.97%  |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |        47.42  |              3 |          20 | +1.67%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |        23.48  |              3 |          20 | -1.41%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |       130.88  |              3 |          20 | +2.92%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |       104.16  |              3 |          20 | +2.10%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |        55.8   |              3 |          20 | -0.81%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |       306.55  |              3 |          20 | +2.48%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |        33.45  |              3 |          20 | +1.61%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |       130.88  |              3 |         120 | +2.92%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |       454.74  |              2 |          20 | +1.32%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |       111.74  |              1 |          20 | -1.94%  |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |        55.27  |              1 |          20 | +1.14%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |        99.99  |              1 |          20 | -3.46%  |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |        86.03  |              1 |          20 | -0.00%  |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |        21.94  |              1 |          20 | +0.64%  |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |        78.84  |              1 |          20 | -1.45%  |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |       545     |              1 |          20 | -0.51%  |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |        77.73  |              1 |          20 | -0.58%  |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |        56.51  |              1 |          20 | -0.07%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |       189.29  |              1 |          20 | -0.21%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |       227.11  |              1 |          20 | +0.37%  |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |       465.97  |              1 |          20 | -1.12%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |        62.31  |              1 |          20 | +0.45%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |       338.025 |              1 |          20 | -0.07%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |       281.5   |              1 |          20 | -0.18%  |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |        99.99  |              1 |          20 | -3.46%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    |              |               |            nan |          20 |         |