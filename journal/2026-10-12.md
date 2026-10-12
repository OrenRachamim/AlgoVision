# Forward-test journal - 2026-10-12

Data through 2026-10-12; 518 of 518 symbols loaded.

## New signals today (9)

| rule                      | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                   |
|:--------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:-------------------------------------------------------|
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-12    |      485    |          20 | score 0.69, stop 456.65, level 481.17                  |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-12    |      146.75 |          20 | score 0.70, stop 134.41, level 145.91                  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD) | 2026-10-12    |      139.81 |          20 | rsi_turn; day +3.3%, 10d +5.0%, 6m -29%, vs MA200 -26% |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)   | 2026-10-12    |       13.16 |          20 | thrust; day +0.2%, 10d +10.6%, 6m -25%, vs MA200 -19%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)   | 2026-10-12    |       55.64 |          20 | thrust; day +0.6%, 10d +9.9%, 6m -21%, vs MA200 -16%   |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)   | 2026-10-12    |       65.86 |          20 | rsi_turn; day +0.6%, 10d +5.2%, 6m -15%, vs MA200 -8%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)   | 2026-10-12    |       42.12 |          20 | rsi_turn; day +0.9%, 10d +4.5%, 6m -11%, vs MA200 -6%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-10-12    |     1119.94 |          20 | rsi_turn; day +1.1%, 10d +1.0%, 6m -9%, vs MA200 -10%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC) | 2026-10-12    |       67.74 |          20 | rsi_turn; day +3.0%, 10d +1.4%, 6m -8%, vs MA200 -4%   |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       44 |        0 | +0.68% | 73%   | +0.53%   | -0.04%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       23 |        3 | -0.83% | 43%   | -1.73%   | -1.10%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        3 |        0 | +0.84% | 67%   | -1.43%   | +2.58%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +2.06% | 61%   | +1.36%   | -0.03%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       15 |        0 | +0.59% | 53%   | -0.73%   | +0.76%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 44, closed: 0, open: 44
- open trades mark-to-market: mean +0.68%, hit 73%
- SPY over the same holding periods: mean +0.15% (excess +0.53%)
- beaten-down basket over the same holding periods: mean +0.72% (excess -0.04%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 23, closed: 3, open: 20
- closed trades: mean -6.32%, median -7.52%, hit 0%, best -3.5%, worst -8.0%
- open trades mark-to-market: mean +0.09%, hit 50%
- SPY over the same holding periods: mean +0.90% (excess -1.73%)
- beaten-down basket over the same holding periods: mean +0.27% (excess -1.10%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean +0.84%, hit 67%
- SPY over the same holding periods: mean +2.26% (excess -1.43%)
- beaten-down basket over the same holding periods: mean -1.75% (excess +2.58%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +2.06%, hit 61%
- SPY over the same holding periods: mean +0.70% (excess +1.36%)
- beaten-down basket over the same holding periods: mean +2.09% (excess -0.03%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 15, closed: 0, open: 15
- open trades mark-to-market: mean +0.59%, hit 53%
- SPY over the same holding periods: mean +1.31% (excess -0.73%)
- beaten-down basket over the same holding periods: mean -0.17% (excess +0.76%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |       100.58  |             25 |          60 | -5.89%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |       920.51  |             25 |          60 | -19.61% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |       232.71  |             24 |          60 | -5.11%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |       632     |             23 |          60 | +2.17%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |        52.32  |             24 |         120 | +2.39%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |        54.66  |             22 |          60 | +1.62%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |       441.33  |             19 |          60 | -6.10%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |        54.37  |             19 |         120 | +2.16%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |        72.99  |             22 |         120 | -2.04%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |        71.82  |             16 |          60 | -1.68%  |
| falling_wedge_beaten_down | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-09-18    | 2026-09-21   |       532.3   |             16 |          20 | -3.84%  |
| falling_wedge_beaten_down | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-09-18    | 2026-09-21   |      1091.3   |             16 |          20 | +2.62%  |
| falling_wedge_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-09-21    | 2026-09-22   |       519.27  |             15 |          20 | +0.90%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |       148.65  |             13 |          20 | -5.54%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |       107.7   |             13 |          20 | -4.74%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |        33.99  |             12 |          60 | -13.74% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |       366.7   |             12 |          20 | -2.72%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |        14.45  |             11 |          20 | +6.23%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |        36.34  |             10 |          20 | -2.72%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |       602.02  |              9 |          60 | +22.92% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |        12.385 |              7 |          60 | +7.39%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |       614     |              7 |          60 | +20.52% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              7 |          20 | +6.00%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |       238.11  |              7 |          20 | -1.76%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |       273.31  |              7 |          20 | +4.02%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |       162.22  |              7 |          20 | +12.54% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |        30.98  |              7 |          20 | +5.71%  |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              7 |          20 | +6.00%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |       222.597 |              7 |          20 | +1.11%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |       121.94  |              7 |          20 | -0.28%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |       119.24  |              7 |          20 | -1.69%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |       101.99  |              7 |          20 | +0.59%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |       141.566 |              7 |          20 | -2.95%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |        33.82  |              6 |          60 | +4.52%  |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |        47.64  |              6 |          20 | +2.77%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |       163.81  |              6 |          20 | +8.35%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              5 |          60 | -0.77%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | 2026-10-06   |        84.2   |              5 |          20 | +3.37%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | 2026-10-06   |        77.73  |              5 |          20 | +4.10%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | 2026-10-06   |        83.45  |              5 |          20 | +3.83%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    | 2026-10-06   |       134.94  |              5 |          20 | +5.17%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              5 |          20 | -4.72%  |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              5 |          20 | -0.98%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              5 |          20 | -0.77%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              5 |          20 | -4.72%  |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              5 |          20 | -0.98%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV) | 2026-10-06    | 2026-10-07   |        44.35  |              4 |          20 | -1.80%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-06    | 2026-10-07   |       103.16  |              4 |          20 | +1.70%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-06    | 2026-10-07   |       103.39  |              4 |          20 | -0.77%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-10-06    | 2026-10-07   |        15.15  |              4 |          20 | +1.32%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)     | 2026-10-06    | 2026-10-07   |        40.61  |              4 |          20 | +1.53%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)   | 2026-10-06    | 2026-10-07   |        52.59  |              4 |          20 | +1.20%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)   | 2026-10-06    | 2026-10-07   |       128.11  |              4 |          20 | -0.05%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)   | 2026-10-06    | 2026-10-07   |        33.7   |              4 |          20 | +1.90%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)   | 2026-10-06    | 2026-10-07   |        38.17  |              4 |          20 | +2.25%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)   | 2026-10-06    | 2026-10-07   |        71.68  |              4 |          20 | -1.28%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)   | 2026-10-06    | 2026-10-07   |       102.99  |              4 |          20 | +0.97%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST) | 2026-10-06    | 2026-10-07   |       940.84  |              4 |          20 | +1.98%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              3 |          20 | -1.05%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              3 |          20 | -1.05%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-10-07    | 2026-10-08   |       642     |              3 |          20 | +0.58%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-07    | 2026-10-08   |       126.47  |              3 |          20 | +3.35%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-08    | 2026-10-09   |        85.58  |              2 |          20 | +1.25%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)   | 2026-10-08    | 2026-10-09   |       123.25  |              2 |          20 | +2.56%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)   | 2026-10-08    | 2026-10-09   |        73.04  |              2 |          20 | +3.57%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-08    | 2026-10-09   |        82.91  |              2 |          20 | +1.64%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP) | 2026-10-08    | 2026-10-09   |        30.02  |              2 |          20 | -2.70%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)   | 2026-10-08    | 2026-10-09   |       309.25  |              2 |          20 | +0.53%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU) | 2026-10-08    | 2026-10-09   |       305.05  |              2 |          20 | +0.31%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)   | 2026-10-08    | 2026-10-09   |       110     |              2 |          20 | +2.80%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)   | 2026-10-08    | 2026-10-09   |        37.61  |              2 |          20 | +1.41%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-08    | 2026-10-09   |       155.51  |              2 |          20 | -2.34%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)     | 2026-10-08    | 2026-10-09   |        44.83  |              2 |          20 | +1.18%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)   | 2026-10-08    | 2026-10-09   |       116.26  |              2 |          20 | +1.23%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-08    | 2026-10-09   |        85.94  |              2 |          20 | +1.28%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-08    | 2026-10-09   |       144     |              2 |          20 | +1.91%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)   | 2026-10-08    | 2026-10-09   |        73.17  |              2 |          20 | +1.37%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-09    | 2026-10-12   |       149.58  |              1 |          60 | +1.53%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)       | 2026-10-09    | 2026-10-12   |        22.26  |              1 |          60 | +1.03%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-09    | 2026-10-12   |       143.23  |              1 |          20 | -1.96%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              1 |          20 | +0.53%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC) | 2026-10-09    | 2026-10-12   |       181.77  |              1 |          20 | +1.38%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO) | 2026-10-09    | 2026-10-12   |        33.62  |              1 |          20 | -0.51%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-09    | 2026-10-12   |        81.41  |              1 |          20 | -0.60%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-10-09    | 2026-10-12   |        53.56  |              1 |          20 | +0.02%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              1 |          20 | +0.53%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)   | 2026-10-09    | 2026-10-12   |       161.66  |              1 |          20 | +0.45%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)   | 2026-10-09    | 2026-10-12   |       366.01  |              1 |          20 | -0.19%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-09    | 2026-10-12   |       103.99  |              1 |          20 | +0.88%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)   | 2026-10-09    | 2026-10-12   |        65.9   |              1 |          20 | +0.85%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)   | 2026-10-09    | 2026-10-12   |       123.2   |              1 |          20 | +0.84%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-12    |              |               |            nan |          20 |         |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD) | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)   | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)   | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)   | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)   | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-10-12    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC) | 2026-10-12    |              |               |            nan |          20 |         |