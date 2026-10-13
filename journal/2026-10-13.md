# Forward-test journal - 2026-10-13

Data through 2026-10-13; 518 of 518 symbols loaded.

## New signals today (6)

| rule                      | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                               |
|:--------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:-------------------------------------------------------------------|
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-13    |       32.79 |          20 | score 0.62, stop 31.00, level 32.49                                |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-10-13    |      183.17 |          20 | higher_high, rsi_turn; day +0.7%, 10d +3.2%, 6m -13%, vs MA200 -8% |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS) | 2026-10-13    |       67.68 |          20 | rsi_turn; day +1.4%, 10d +3.1%, 6m -16%, vs MA200 -12%             |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG) | 2026-10-13    |      222.86 |          20 | rsi_turn; day +1.0%, 10d -0.5%, 6m -13%, vs MA200 -6%              |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)   | 2026-10-13    |       57.89 |          20 | rsi_turn; day +2.3%, 10d -0.2%, 6m -12%, vs MA200 -9%              |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)   | 2026-10-13    |      192.48 |          20 | rsi_turn; day +0.8%, 10d +1.5%, 6m -11%, vs MA200 -8%              |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       49 |        0 | +0.66% | 70%   | +0.53%   | -0.05%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       24 |        3 | -0.61% | 43%   | -1.43%   | -0.95%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        3 |        0 | +0.31% | 67%   | -1.94%   | +2.13%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +1.93% | 67%   | +1.24%   | -0.35%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       15 |        0 | -0.08% | 47%   | -1.38%   | +0.03%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 49, closed: 0, open: 49
- open trades mark-to-market: mean +0.66%, hit 70%
- SPY over the same holding periods: mean +0.13% (excess +0.53%)
- beaten-down basket over the same holding periods: mean +0.72% (excess -0.05%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 24, closed: 3, open: 21
- closed trades: mean -6.32%, median -7.52%, hit 0%, best -3.5%, worst -8.0%
- open trades mark-to-market: mean +0.24%, hit 50%
- SPY over the same holding periods: mean +0.82% (excess -1.43%)
- beaten-down basket over the same holding periods: mean +0.34% (excess -0.95%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean +0.31%, hit 67%
- SPY over the same holding periods: mean +2.25% (excess -1.94%)
- beaten-down basket over the same holding periods: mean -1.82% (excess +2.13%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +1.93%, hit 67%
- SPY over the same holding periods: mean +0.69% (excess +1.24%)
- beaten-down basket over the same holding periods: mean +2.28% (excess -0.35%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 15, closed: 0, open: 15
- open trades mark-to-market: mean -0.08%, hit 47%
- SPY over the same holding periods: mean +1.30% (excess -1.38%)
- beaten-down basket over the same holding periods: mean -0.11% (excess +0.03%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |       100.58  |             26 |          60 | -6.20%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |       920.51  |             26 |          60 | -21.45% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |       232.71  |             25 |          60 | -6.82%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |       632     |             24 |          60 | +1.54%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |        52.32  |             25 |         120 | +2.81%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |        54.66  |             23 |          60 | -0.13%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |       441.33  |             20 |          60 | -6.34%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |        54.37  |             20 |         120 | +0.40%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |        72.99  |             23 |         120 | -2.29%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |        71.82  |             17 |          60 | -1.89%  |
| falling_wedge_beaten_down | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-09-18    | 2026-09-21   |       532.3   |             17 |          20 | -5.31%  |
| falling_wedge_beaten_down | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-09-18    | 2026-09-21   |      1091.3   |             17 |          20 | +1.93%  |
| falling_wedge_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-09-21    | 2026-09-22   |       519.27  |             16 |          20 | +0.20%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |       148.65  |             14 |          20 | -3.44%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |       107.7   |             14 |          20 | -4.79%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |        33.99  |             13 |          60 | -13.50% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |       366.7   |             13 |          20 | -4.52%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |        14.45  |             12 |          20 | +6.02%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |        36.34  |             11 |          20 | -2.78%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |       602.02  |             10 |          60 | +20.10% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |        12.385 |              8 |          60 | +7.87%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |       614     |              8 |          60 | +17.76% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              8 |          20 | +5.69%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |       238.11  |              8 |          20 | -0.04%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |       273.31  |              8 |          20 | +4.52%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |       162.22  |              8 |          20 | +10.61% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |        30.98  |              8 |          20 | +5.42%  |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              8 |          20 | +5.69%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |       222.597 |              8 |          20 | +3.70%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |       121.94  |              8 |          20 | -1.84%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |       119.24  |              8 |          20 | -3.36%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |       101.99  |              8 |          20 | +0.54%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |       141.566 |              8 |          20 | +1.15%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |        33.82  |              7 |          60 | +4.46%  |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |        47.64  |              7 |          20 | +5.39%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |       163.81  |              7 |          20 | +7.84%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              6 |          60 | -2.03%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | 2026-10-06   |        84.2   |              6 |          20 | +4.64%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | 2026-10-06   |        77.73  |              6 |          20 | +5.44%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | 2026-10-06   |        83.45  |              6 |          20 | +3.09%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    | 2026-10-06   |       134.94  |              6 |          20 | +4.85%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              6 |          20 | -8.27%  |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              6 |          20 | -1.67%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              6 |          20 | -2.03%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              6 |          20 | -8.27%  |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              6 |          20 | -1.67%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV) | 2026-10-06    | 2026-10-07   |        44.35  |              5 |          20 | -0.20%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-06    | 2026-10-07   |       103.16  |              5 |          20 | +2.63%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-06    | 2026-10-07   |       103.39  |              5 |          20 | -0.82%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-10-06    | 2026-10-07   |        15.15  |              5 |          20 | +1.12%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)     | 2026-10-06    | 2026-10-07   |        40.61  |              5 |          20 | +2.17%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)   | 2026-10-06    | 2026-10-07   |        52.59  |              5 |          20 | +3.50%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)   | 2026-10-06    | 2026-10-07   |       128.11  |              5 |          20 | +0.17%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)   | 2026-10-06    | 2026-10-07   |        33.7   |              5 |          20 | +2.76%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)   | 2026-10-06    | 2026-10-07   |        38.17  |              5 |          20 | +3.12%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)   | 2026-10-06    | 2026-10-07   |        71.68  |              5 |          20 | -1.69%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)   | 2026-10-06    | 2026-10-07   |       102.99  |              5 |          20 | +1.94%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST) | 2026-10-06    | 2026-10-07   |       940.84  |              5 |          20 | +1.47%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              4 |          20 | -0.30%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              4 |          20 | -0.30%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-10-07    | 2026-10-08   |       642     |              4 |          20 | -0.04%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-07    | 2026-10-08   |       126.47  |              4 |          20 | +2.53%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-08    | 2026-10-09   |        85.58  |              3 |          20 | +0.53%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)   | 2026-10-08    | 2026-10-09   |       123.25  |              3 |          20 | +3.09%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)   | 2026-10-08    | 2026-10-09   |        73.04  |              3 |          20 | +1.73%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-08    | 2026-10-09   |        82.91  |              3 |          20 | +1.34%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP) | 2026-10-08    | 2026-10-09   |        30.02  |              3 |          20 | -0.07%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)   | 2026-10-08    | 2026-10-09   |       309.25  |              3 |          20 | -4.25%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU) | 2026-10-08    | 2026-10-09   |       305.05  |              3 |          20 | -1.18%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)   | 2026-10-08    | 2026-10-09   |       110     |              3 |          20 | +2.07%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)   | 2026-10-08    | 2026-10-09   |        37.61  |              3 |          20 | +2.42%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-08    | 2026-10-09   |       155.51  |              3 |          20 | -1.14%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)     | 2026-10-08    | 2026-10-09   |        44.83  |              3 |          20 | +0.85%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)   | 2026-10-08    | 2026-10-09   |       116.26  |              3 |          20 | +1.66%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-08    | 2026-10-09   |        85.94  |              3 |          20 | +2.53%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-08    | 2026-10-09   |       144     |              3 |          20 | +2.12%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)   | 2026-10-08    | 2026-10-09   |        73.17  |              3 |          20 | +2.01%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-09    | 2026-10-12   |       149.6   |              2 |          60 | +2.76%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)       | 2026-10-09    | 2026-10-12   |        22.26  |              2 |          60 | +2.65%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-09    | 2026-10-12   |       143.23  |              2 |          20 | +0.22%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              2 |          20 | +1.13%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC) | 2026-10-09    | 2026-10-12   |       181.77  |              2 |          20 | +0.03%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO) | 2026-10-09    | 2026-10-12   |        33.62  |              2 |          20 | +0.22%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-09    | 2026-10-12   |        81.41  |              2 |          20 | +0.68%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-10-09    | 2026-10-12   |        53.56  |              2 |          20 | +0.43%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              2 |          20 | +1.13%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)   | 2026-10-09    | 2026-10-12   |       161.66  |              2 |          20 | +1.12%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)   | 2026-10-09    | 2026-10-12   |       366.01  |              2 |          20 | +0.85%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-09    | 2026-10-12   |       103.99  |              2 |          20 | +1.81%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)   | 2026-10-09    | 2026-10-12   |        65.9   |              2 |          20 | +1.61%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)   | 2026-10-09    | 2026-10-12   |       123.2   |              2 |          20 | +1.99%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-12    | 2026-10-13   |       486.79  |              1 |          20 | -1.11%  |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-12    | 2026-10-13   |       147.47  |              1 |          20 | -0.28%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD) | 2026-10-12    | 2026-10-13   |       140.99  |              1 |          20 | -2.03%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)   | 2026-10-12    | 2026-10-13   |        13.21  |              1 |          20 | +0.91%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)   | 2026-10-12    | 2026-10-13   |        56.04  |              1 |          20 | -1.00%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)   | 2026-10-12    | 2026-10-13   |        66.28  |              1 |          20 | +0.03%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)   | 2026-10-12    | 2026-10-13   |        42.71  |              1 |          20 | -0.87%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-10-12    | 2026-10-13   |      1113.01  |              1 |          20 | -0.06%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC) | 2026-10-12    | 2026-10-13   |        67.74  |              1 |          20 | +1.55%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-13    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-10-13    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS) | 2026-10-13    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG) | 2026-10-13    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)   | 2026-10-13    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)   | 2026-10-13    |              |               |            nan |          20 |         |