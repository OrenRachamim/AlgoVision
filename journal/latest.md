# Forward-test journal - 2026-10-22

Data through 2026-10-22; 518 of 518 symbols loaded.

## New signals today (7)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                    |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:--------------------------------------------------------|
| early_rally_beaten_down | [PNR](https://www.tradingview.com/chart/?symbol=PNR)   | 2026-10-22    |       55.44 |          20 | rsi_turn; day +4.9%, 10d +6.0%, 6m -38%, vs MA200 -28%  |
| early_rally_beaten_down | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR) | 2026-10-22    |       57.54 |          20 | rsi_turn; day +7.5%, 10d +6.9%, 6m -36%, vs MA200 -30%  |
| early_rally_beaten_down | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-22    |      823.27 |          20 | rsi_turn; day +3.5%, 10d +16.4%, 6m -16%, vs MA200 -28% |
| early_rally_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT) | 2026-10-22    |       29.09 |          20 | rsi_turn; day +5.4%, 10d +5.9%, 6m -14%, vs MA200 -11%  |
| early_rally_beaten_down | [NVR](https://www.tradingview.com/chart/?symbol=NVR)   | 2026-10-22    |     6110.63 |          20 | rsi_turn; day +3.6%, 10d +1.8%, 6m -8%, vs MA200 -7%    |
| early_rally_beaten_down | [PHM](https://www.tradingview.com/chart/?symbol=PHM)   | 2026-10-22    |      119.48 |          20 | rsi_turn; day +5.8%, 10d +5.2%, 6m -8%, vs MA200 -3%    |
| early_rally_beaten_down | [KKR](https://www.tradingview.com/chart/?symbol=KKR)   | 2026-10-22    |       93.09 |          20 | rsi_turn; day +3.6%, 10d +3.9%, 6m -8%, vs MA200 -7%    |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      101 |        0 | +4.32% | 85%   | +5.56%   | +0.96%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       33 |        9 | +3.15% | 76%   | +3.95%   | -0.15%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        4 |        0 | +5.79% | 75%   | +5.60%   | +3.25%             |
| jev_pick                  | untested (forward test only)                     |       27 |        0 | +3.86% | 72%   | +4.88%   | -1.82%             |
| jev_skip                  | untested; a fall is the success case             |        3 |        0 | +5.50% | 100%  | +6.02%   | +4.67%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       17 |        0 | +2.87% | 59%   | +3.43%   | -1.83%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 101, closed: 0, open: 101
- open trades mark-to-market: mean +4.32%, hit 85%
- SPY over the same holding periods: mean -1.24% (excess +5.56%)
- beaten-down basket over the same holding periods: mean +3.36% (excess +0.96%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 33, closed: 9, open: 24
- closed trades: mean +0.32%, median +3.28%, hit 56%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +4.22%, hit 83%
- SPY over the same holding periods: mean -0.80% (excess +3.95%)
- beaten-down basket over the same holding periods: mean +3.30% (excess -0.15%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 4, closed: 0, open: 4
- open trades mark-to-market: mean +5.79%, hit 75%
- SPY over the same holding periods: mean +0.20% (excess +5.60%)
- beaten-down basket over the same holding periods: mean +2.54% (excess +3.25%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 27, closed: 0, open: 27
- open trades mark-to-market: mean +3.86%, hit 72%
- SPY over the same holding periods: mean -1.02% (excess +4.88%)
- beaten-down basket over the same holding periods: mean +5.68% (excess -1.82%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean +5.50%, hit 100%
- SPY over the same holding periods: mean -0.52% (excess +6.02%)
- beaten-down basket over the same holding periods: mean +0.83% (excess +4.67%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 17, closed: 0, open: 17
- open trades mark-to-market: mean +2.87%, hit 59%
- SPY over the same holding periods: mean -0.55% (excess +3.43%)
- beaten-down basket over the same holding periods: mean +4.70% (excess -1.83%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |       100.58  |             33 |          60 | +3.46%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |       920.51  |             33 |          60 | -10.56% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |       232.71  |             32 |          60 | -16.94% |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |       632     |             31 |          60 | +12.92% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |        52.32  |             32 |         120 | +9.08%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |        54.66  |             30 |          60 | +12.79% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |       441.33  |             27 |          60 | -6.06%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |        54.37  |             27 |         120 | +13.39% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |        72.99  |             30 |         120 | -5.37%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |        71.82  |             24 |          60 | -6.64%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |        33.99  |             20 |          60 | -13.21% |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-09-25    | 2026-09-28   |        14.45  |             18 |          20 | +7.54%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-09-28    | 2026-09-29   |        36.34  |             18 |          20 | +5.45%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |       602.02  |             17 |          60 | +36.75% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |        12.385 |             15 |          60 | +3.84%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |       614     |             15 |          60 | +34.08% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |        79.5   |             15 |          20 | +7.27%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)     | 2026-10-01    | 2026-10-02   |       238.11  |             14 |          20 | +5.12%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)     | 2026-10-01    | 2026-10-02   |       273.31  |             14 |          20 | +6.95%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)     | 2026-10-01    | 2026-10-02   |       162.22  |             15 |          20 | +11.93% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)     | 2026-10-01    | 2026-10-02   |        30.98  |             15 |          20 | +13.59% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |        79.5   |             15 |          20 | +7.27%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE)   | 2026-10-01    | 2026-10-02   |       222.597 |             15 |          20 | +15.37% |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-01    | 2026-10-02   |       121.94  |             15 |          20 | +10.49% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-01    | 2026-10-02   |       119.24  |             15 |          20 | -4.46%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-01    | 2026-10-02   |       101.99  |             15 |          20 | +7.13%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-01    | 2026-10-02   |       141.566 |             15 |          20 | -11.32% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |        33.82  |             14 |          60 | +13.31% |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)     | 2026-10-02    | 2026-10-05   |        47.64  |             14 |          20 | +3.23%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK)   | 2026-10-02    | 2026-10-05   |       163.81  |             14 |          20 | +24.13% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |       140.83  |             13 |          60 | +1.05%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-05    | 2026-10-06   |        84.2   |             13 |          20 | +11.43% |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-05    | 2026-10-06   |        77.73  |             13 |          20 | +1.85%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-05    | 2026-10-06   |        83.45  |             13 |          20 | +10.25% |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-10-05    | 2026-10-06   |       134.94  |             13 |          20 | +9.22%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |        99.81  |             13 |          20 | -14.05% |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |       529.14  |             13 |          20 | +7.11%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |       140.83  |             13 |          20 | +1.05%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |        99.81  |             13 |          20 | -14.05% |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |       529.14  |             13 |          20 | +7.11%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV)   | 2026-10-06    | 2026-10-07   |        44.35  |             12 |          20 | -1.22%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-06    | 2026-10-07   |       103.16  |             12 |          20 | +8.71%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-06    | 2026-10-07   |       103.39  |             12 |          20 | +5.68%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-10-06    | 2026-10-07   |        15.15  |             11 |          20 | +2.57%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)       | 2026-10-06    | 2026-10-07   |        40.61  |             12 |          20 | +7.58%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)     | 2026-10-06    | 2026-10-07   |        52.59  |             12 |          20 | +3.96%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)     | 2026-10-06    | 2026-10-07   |       128.11  |             11 |          20 | +3.86%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)     | 2026-10-06    | 2026-10-07   |        33.7   |             11 |          20 | +4.90%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)     | 2026-10-06    | 2026-10-07   |        38.17  |             12 |          20 | +7.94%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-06    | 2026-10-07   |        71.68  |             12 |          20 | +1.45%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)     | 2026-10-06    | 2026-10-07   |       102.99  |             12 |          20 | +5.05%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST)   | 2026-10-06    | 2026-10-07   |       940.84  |             12 |          20 | +8.22%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |       107.5   |             11 |          20 | -12.20% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |       107.5   |             11 |          20 | -12.20% |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-07    | 2026-10-08   |       642     |             11 |          20 | +11.16% |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-07    | 2026-10-08   |       126.47  |             11 |          20 | +3.77%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-08    | 2026-10-09   |        85.58  |             10 |          20 | +7.50%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)     | 2026-10-08    | 2026-10-09   |       123.25  |             10 |          20 | +12.76% |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)     | 2026-10-08    | 2026-10-09   |        73.04  |             10 |          20 | +12.27% |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-08    | 2026-10-09   |        82.91  |             10 |          20 | +2.86%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-08    | 2026-10-09   |        30.02  |             10 |          20 | +18.09% |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-10-08    | 2026-10-09   |       309.25  |             10 |          20 | +2.73%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-10-08    | 2026-10-09   |       305.05  |             10 |          20 | +16.34% |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)     | 2026-10-08    | 2026-10-09   |       110     |             10 |          20 | +10.11% |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)     | 2026-10-08    | 2026-10-09   |        37.61  |             10 |          20 | +10.79% |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-08    | 2026-10-09   |       155.51  |             10 |          20 | +2.11%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)       | 2026-10-08    | 2026-10-09   |        44.83  |             10 |          20 | +3.70%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)     | 2026-10-08    | 2026-10-09   |       116.26  |             10 |          20 | +7.86%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-08    | 2026-10-09   |        85.94  |             10 |          20 | +9.17%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-08    | 2026-10-09   |       144     |             10 |          20 | +7.26%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)     | 2026-10-08    | 2026-10-09   |        73.17  |             10 |          20 | +7.83%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |       149.6   |              9 |          60 | +6.14%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |        22.26  |              9 |          60 | +2.16%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-09    | 2026-10-12   |       143.23  |              8 |          20 | +8.57%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |        81.45  |              9 |          20 | +4.08%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC)   | 2026-10-09    | 2026-10-12   |       181.77  |              9 |          20 | -1.86%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-10-09    | 2026-10-12   |        33.62  |              9 |          20 | +3.30%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-09    | 2026-10-12   |        81.41  |              9 |          20 | -2.75%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-09    | 2026-10-12   |        53.56  |              9 |          20 | +6.55%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |        81.45  |              9 |          20 | +4.08%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)     | 2026-10-09    | 2026-10-12   |       161.66  |              9 |          20 | +7.58%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-09    | 2026-10-12   |       366.01  |              9 |          20 | -8.84%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-09    | 2026-10-12   |       103.99  |              9 |          20 | +7.85%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)     | 2026-10-09    | 2026-10-12   |        65.9   |              9 |          20 | +6.68%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)     | 2026-10-09    | 2026-10-12   |       123.2   |              9 |          20 | +6.04%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-12    | 2026-10-13   |       486.79  |              8 |          20 | +13.47% |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-12    | 2026-10-13   |       147.47  |              8 |          20 | +4.73%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD)   | 2026-10-12    | 2026-10-13   |       140.79  |              8 |          20 | +5.21%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-10-12    | 2026-10-13   |        13.21  |              8 |          20 | -1.74%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)     | 2026-10-12    | 2026-10-13   |        56.04  |              8 |          20 | +3.32%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)     | 2026-10-12    | 2026-10-13   |        66.28  |              8 |          20 | +6.07%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)     | 2026-10-12    | 2026-10-13   |        42.6   |              8 |          20 | +5.28%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)     | 2026-10-12    | 2026-10-13   |      1113.01  |              8 |          20 | +2.58%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC)   | 2026-10-12    | 2026-10-13   |        67.74  |              7 |          20 | +5.43%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |        32.85  |              7 |          20 | +1.04%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |       182.6   |              7 |          20 | +3.99%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |        67.9   |              7 |          20 | +11.34% |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |       220.63  |              6 |          20 | +3.03%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |        57.66  |              7 |          20 | +8.34%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |       191.79  |              6 |          20 | +1.93%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |        61.43  |              6 |          60 | -9.49%  |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |        33.27  |              6 |          20 | +6.13%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |       342.5   |              6 |          20 | -5.80%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |       153.24  |              6 |          20 | +22.12% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |        61.37  |              5 |          20 | +6.52%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |       531     |              6 |          20 | +11.09% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |        65.195 |              5 |          60 | -14.72% |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |       136.02  |              5 |          20 | -3.51%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |        27.96  |              5 |          20 | +4.04%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |        83.4   |              5 |          20 | +3.63%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |       529.98  |              5 |          20 | -1.97%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |       357.38  |              5 |          20 | +5.97%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |      3091     |              5 |          20 | +5.81%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |        13.29  |              5 |          20 | -0.98%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |        36.42  |              5 |          20 | +5.13%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |       120.66  |              5 |          20 | -5.59%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |       295.89  |              5 |          20 | +3.78%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |        69.87  |              5 |          20 | -4.04%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |        44.45  |              5 |          20 | +3.51%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |        29.93  |              5 |          20 | +6.28%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |       125.05  |              5 |          20 | +7.74%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |       244.31  |              5 |          20 | +3.41%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |       150.37  |              4 |          20 | +3.42%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |       505.78  |              4 |          20 | +2.35%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |       195.819 |              5 |          20 | +4.37%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |        37.67  |              5 |          20 | +1.73%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |        86.69  |              5 |          20 | +2.27%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |        79.6   |              5 |          20 | +2.89%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |       255.41  |              4 |          20 | +5.21%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |       170.42  |              5 |          20 | +3.06%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |       136.02  |              5 |          20 | -3.51%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |       169.41  |              4 |          20 | +3.68%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |        45.99  |              4 |          20 | +5.91%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |       511     |              4 |          20 | +8.09%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |        57.29  |              4 |          20 | +7.61%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |       289.03  |              4 |          20 | +6.15%  |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |       268.28  |              4 |          20 | +3.94%  |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |       245.16  |              4 |          20 | +3.70%  |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |        47.42  |              4 |          20 | +7.17%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |        23.48  |              3 |          20 | +2.30%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |       130.88  |              4 |          20 | +6.07%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |       104.16  |              4 |          20 | +4.90%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |        55.8   |              4 |          20 | +2.26%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |       306.55  |              4 |          20 | +6.91%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |        33.45  |              4 |          20 | -0.78%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |       130.88  |              4 |         120 | +6.07%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |       454.74  |              3 |          20 | -1.97%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |       111.74  |              2 |          20 | +6.27%  |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |        55.27  |              2 |          20 | +3.26%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |       100     |              2 |          20 | +4.06%  |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |        86.03  |              2 |          20 | +0.46%  |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |        21.94  |              2 |          20 | +4.10%  |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |        78.84  |              2 |          20 | +7.12%  |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |       545     |              2 |          20 | -4.67%  |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |        77.73  |              2 |          20 | +0.40%  |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-22   |        55.69  |              1 |          20 | +1.42%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |       189.29  |              2 |          20 | +0.32%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-22   |       227.31  |              1 |          20 | -0.00%  |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |       465.97  |              2 |          20 | -4.33%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |        62.31  |              2 |          20 | +2.73%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |       338.03  |              2 |          20 | -4.38%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |       281.5   |              2 |          20 | -5.01%  |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |       100     |              2 |          20 | +4.06%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |       363.84  |              1 |          20 | +4.09%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | nan          |       nan     |            nan |          20 |         |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | nan          |       nan     |            nan |          20 |         |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |       544.7   |              1 |          20 | +1.40%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |        77.57  |              1 |          20 | +8.87%  |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |        85.6   |              1 |          20 | +3.57%  |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    |              |               |            nan |          20 |         |