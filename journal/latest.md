# Forward-test journal - 2026-10-16

Data through 2026-10-16; 518 of 518 symbols loaded.

## New signals today (14)

| rule                      | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                                |
|:--------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:--------------------------------------------------------------------|
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)   | 2026-10-16    |      170.83 |          20 | score 0.75, stop 157.86, level 170.32                               |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)   | 2026-10-16    |       46.35 |          20 | score 0.68, stop 42.86, level 45.33                                 |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-16    |      519.86 |          20 | rsi_turn, thrust; day +4.0%, 10d +8.8%, 6m -21%, vs MA200 -12%      |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-10-16    |       57.94 |          20 | higher_high, rsi_turn; day +0.9%, 10d +1.8%, 6m -17%, vs MA200 -17% |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)   | 2026-10-16    |      292.55 |          20 | rsi_turn, thrust; day +2.0%, 10d +8.6%, 6m -11%, vs MA200 -11%      |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)   | 2026-10-16    |      272    |          20 | rsi_turn; day +1.8%, 10d +1.3%, 6m -30%, vs MA200 -19%              |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)   | 2026-10-16    |      248.51 |          20 | rsi_turn; day +3.3%, 10d +5.0%, 6m -28%, vs MA200 -19%              |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV) | 2026-10-16    |       47.55 |          20 | rsi_turn; day +0.7%, 10d +7.2%, 6m -26%, vs MA200 -15%              |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI) | 2026-10-16    |       23.6  |          20 | rsi_turn; day +0.6%, 10d +4.2%, 6m -16%, vs MA200 -10%              |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)   | 2026-10-16    |      131.49 |          20 | rsi_turn; day +2.4%, 10d +4.4%, 6m -15%, vs MA200 -9%               |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-16    |      104.05 |          20 | higher_high; day +0.7%, 10d +2.2%, 6m -13%, vs MA200 -12%           |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)       | 2026-10-16    |       56.08 |          20 | rsi_turn; day +1.0%, 10d +3.6%, 6m -12%, vs MA200 -7%               |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)     | 2026-10-16    |      309.63 |          20 | thrust; day +0.5%, 10d +9.5%, 6m -10%, vs MA200 -7%                 |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-16    |       33.5  |          20 | rsi_turn; day +1.9%, 10d +5.2%, 6m -9%, vs MA200 -5%                |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       85 |        0 | +1.90% | 70%   | +3.43%   | -0.07%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       31 |        5 | +1.35% | 69%   | +2.29%   | -0.55%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        3 |        0 | +2.63% | 67%   | +2.31%   | +2.48%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +4.26% | 83%   | +5.48%   | -0.66%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       17 |        0 | +1.96% | 47%   | +2.61%   | -0.03%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 85, closed: 0, open: 85
- open trades mark-to-market: mean +1.90%, hit 70%
- SPY over the same holding periods: mean -1.53% (excess +3.43%)
- beaten-down basket over the same holding periods: mean +1.96% (excess -0.07%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 31, closed: 5, open: 26
- closed trades: mean -2.17%, median -3.46%, hit 40%, best +4.4%, worst -8.0%
- open trades mark-to-market: mean +2.08%, hit 75%
- SPY over the same holding periods: mean -0.94% (excess +2.29%)
- beaten-down basket over the same holding periods: mean +1.90% (excess -0.55%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean +2.63%, hit 67%
- SPY over the same holding periods: mean +0.31% (excess +2.31%)
- beaten-down basket over the same holding periods: mean +0.15% (excess +2.48%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +4.26%, hit 83%
- SPY over the same holding periods: mean -1.22% (excess +5.48%)
- beaten-down basket over the same holding periods: mean +4.92% (excess -0.66%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 17, closed: 0, open: 17
- open trades mark-to-market: mean +1.96%, hit 47%
- SPY over the same holding periods: mean -0.65% (excess +2.61%)
- beaten-down basket over the same holding periods: mean +1.99% (excess -0.03%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |       100.58  |             29 |          60 | -3.46%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |       920.51  |             29 |          60 | -16.22% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |       232.71  |             28 |          60 | -5.05%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |       632     |             27 |          60 | +9.05%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |        52.32  |             28 |         120 | +4.93%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |        54.66  |             26 |          60 | +6.00%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |       441.33  |             23 |          60 | -11.57% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |        54.37  |             23 |         120 | +6.57%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |        72.99  |             26 |         120 | -3.62%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |        71.82  |             20 |          60 | -1.80%  |
| falling_wedge_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-09-21    | 2026-09-22   |       519.27  |             19 |          20 | +7.91%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |       148.65  |             17 |          20 | -0.90%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |       107.7   |             17 |          20 | -3.39%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |        33.99  |             16 |          60 | -15.86% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |       366.7   |             16 |          20 | -2.45%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |        14.45  |             15 |          20 | +4.15%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |        36.34  |             14 |          20 | +2.17%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |       602.02  |             13 |          60 | +28.10% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |        12.385 |             11 |          60 | +4.00%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |       614     |             11 |          60 | +25.60% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |             11 |          20 | +7.81%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |       238.11  |             11 |          20 | +1.09%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |       273.31  |             11 |          20 | +5.70%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |       162.22  |             11 |          20 | +14.21% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |        30.98  |             11 |          20 | +11.75% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |             11 |          20 | +7.81%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |       222.597 |             11 |          20 | +9.48%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |       121.94  |             11 |          20 | +2.39%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |       119.24  |             11 |          20 | +0.79%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |       101.99  |             11 |          20 | +2.02%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |       141.566 |             11 |          20 | -9.42%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |        33.82  |             10 |          60 | +9.79%  |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |        47.64  |             10 |          20 | +6.49%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |       163.81  |             10 |          20 | +16.54% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              9 |          60 | -0.95%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | 2026-10-06   |        84.2   |              9 |          20 | +8.29%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | 2026-10-06   |        77.73  |              9 |          20 | +4.17%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | 2026-10-06   |        83.45  |              9 |          20 | +6.97%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    | 2026-10-06   |       134.94  |              9 |          20 | +9.18%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              9 |          20 | -14.47% |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              9 |          20 | +5.90%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              9 |          20 | -0.95%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              9 |          20 | -14.47% |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              9 |          20 | +5.90%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV) | 2026-10-06    | 2026-10-07   |        44.35  |              8 |          20 | +1.15%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-06    | 2026-10-07   |       103.16  |              8 |          20 | +5.38%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-06    | 2026-10-07   |       103.39  |              8 |          20 | +0.64%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-10-06    | 2026-10-07   |        15.15  |              8 |          20 | -0.66%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)     | 2026-10-06    | 2026-10-07   |        40.61  |              8 |          20 | +5.10%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)   | 2026-10-06    | 2026-10-07   |        52.59  |              8 |          20 | +3.25%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)   | 2026-10-06    | 2026-10-07   |       128.11  |              8 |          20 | +1.26%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)   | 2026-10-06    | 2026-10-07   |        33.7   |              8 |          20 | +4.36%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)   | 2026-10-06    | 2026-10-07   |        38.17  |              8 |          20 | +6.24%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)   | 2026-10-06    | 2026-10-07   |        71.68  |              8 |          20 | -0.27%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)   | 2026-10-06    | 2026-10-07   |       102.99  |              8 |          20 | +2.06%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST) | 2026-10-06    | 2026-10-07   |       940.84  |              8 |          20 | +5.13%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              7 |          20 | -3.49%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              7 |          20 | -3.49%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-10-07    | 2026-10-08   |       642     |              7 |          20 | +7.36%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-07    | 2026-10-08   |       126.47  |              7 |          20 | +5.23%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-08    | 2026-10-09   |        85.58  |              6 |          20 | +4.31%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)   | 2026-10-08    | 2026-10-09   |       123.25  |              6 |          20 | +6.57%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)   | 2026-10-08    | 2026-10-09   |        73.04  |              6 |          20 | +8.68%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-08    | 2026-10-09   |        82.91  |              6 |          20 | +3.38%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP) | 2026-10-08    | 2026-10-09   |        30.02  |              6 |          20 | +7.63%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)   | 2026-10-08    | 2026-10-09   |       309.25  |              6 |          20 | -0.20%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU) | 2026-10-08    | 2026-10-09   |       305.05  |              6 |          20 | +6.59%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)   | 2026-10-08    | 2026-10-09   |       110     |              6 |          20 | +8.01%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)   | 2026-10-08    | 2026-10-09   |        37.61  |              6 |          20 | +5.08%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-08    | 2026-10-09   |       155.51  |              6 |          20 | +2.31%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)     | 2026-10-08    | 2026-10-09   |        44.83  |              6 |          20 | +3.03%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)   | 2026-10-08    | 2026-10-09   |       116.26  |              6 |          20 | +4.48%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-08    | 2026-10-09   |        85.94  |              6 |          20 | +6.10%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-08    | 2026-10-09   |       144     |              6 |          20 | +4.52%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)   | 2026-10-08    | 2026-10-09   |        73.17  |              6 |          20 | +4.29%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-09    | 2026-10-12   |       149.6   |              5 |          60 | +6.35%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)       | 2026-10-09    | 2026-10-12   |        22.26  |              5 |          60 | +5.30%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-09    | 2026-10-12   |       143.23  |              5 |          20 | +2.85%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              5 |          20 | +2.41%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC) | 2026-10-09    | 2026-10-12   |       181.77  |              5 |          20 | +2.91%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO) | 2026-10-09    | 2026-10-12   |        33.62  |              5 |          20 | -1.37%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-09    | 2026-10-12   |        81.41  |              5 |          20 | -0.54%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-10-09    | 2026-10-12   |        53.56  |              5 |          20 | +2.50%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              5 |          20 | +2.41%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)   | 2026-10-09    | 2026-10-12   |       161.66  |              5 |          20 | +3.51%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)   | 2026-10-09    | 2026-10-12   |       366.01  |              5 |          20 | -4.12%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-09    | 2026-10-12   |       103.99  |              5 |          20 | +4.54%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)   | 2026-10-09    | 2026-10-12   |        65.9   |              5 |          20 | +3.67%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)   | 2026-10-09    | 2026-10-12   |       123.2   |              5 |          20 | +3.20%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-12    | 2026-10-13   |       486.79  |              4 |          20 | +6.79%  |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-12    | 2026-10-13   |       147.47  |              4 |          20 | +2.06%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD) | 2026-10-12    | 2026-10-13   |       140.79  |              4 |          20 | +0.22%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)   | 2026-10-12    | 2026-10-13   |        13.21  |              4 |          20 | -0.91%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)   | 2026-10-12    | 2026-10-13   |        56.04  |              4 |          20 | -0.20%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)   | 2026-10-12    | 2026-10-13   |        66.28  |              4 |          20 | +3.65%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)   | 2026-10-12    | 2026-10-13   |        42.6   |              4 |          20 | +2.11%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-10-12    | 2026-10-13   |      1113.01  |              4 |          20 | +2.37%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC) | 2026-10-12    | 2026-10-13   |        67.74  |              4 |          20 | +2.70%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-13    | 2026-10-14   |        32.85  |              3 |          20 | +1.98%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-10-13    | 2026-10-14   |       182.6   |              3 |          20 | +2.80%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS) | 2026-10-13    | 2026-10-14   |        67.9   |              3 |          20 | +5.05%  |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG) | 2026-10-13    | 2026-10-14   |       220.63  |              3 |          20 | +4.98%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)   | 2026-10-13    | 2026-10-14   |        57.66  |              3 |          20 | +2.71%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)   | 2026-10-13    | 2026-10-14   |       191.79  |              3 |          20 | +2.09%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV) | 2026-10-14    | 2026-10-15   |        61.43  |              2 |          60 | -0.07%  |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)   | 2026-10-14    | 2026-10-15   |        33.27  |              2 |          20 | +0.54%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN) | 2026-10-14    | 2026-10-15   |       342.5   |              2 |          20 | -2.85%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)   | 2026-10-14    | 2026-10-15   |       153.24  |              2 |          20 | +5.23%  |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)   | 2026-10-14    | 2026-10-15   |        61.37  |              2 |          20 | +4.30%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-10-14    | 2026-10-15   |       531     |              2 |          20 | +3.97%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV) | 2026-10-15    | 2026-10-16   |        65.195 |              1 |          60 | -5.84%  |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-15    | 2026-10-16   |       136.02  |              1 |          20 | -2.16%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT) | 2026-10-15    | 2026-10-16   |        27.96  |              1 |          20 | -0.32%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)   | 2026-10-15    | 2026-10-16   |        83.4   |              1 |          20 | +0.28%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)   | 2026-10-15    | 2026-10-16   |       529.98  |              1 |          20 | +0.25%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-10-15    | 2026-10-16   |       357.38  |              1 |          20 | +0.10%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)   | 2026-10-15    | 2026-10-16   |      3091     |              1 |          20 | +0.96%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)   | 2026-10-15    | 2026-10-16   |        13.285 |              1 |          20 | -7.94%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)   | 2026-10-15    | 2026-10-16   |        36.42  |              1 |          20 | -1.13%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-15    | 2026-10-16   |       120.66  |              1 |          20 | -0.40%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)   | 2026-10-15    | 2026-10-16   |       295.89  |              1 |          20 | -0.42%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-10-15    | 2026-10-16   |        69.82  |              1 |          20 | +1.02%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)   | 2026-10-15    | 2026-10-16   |        44.45  |              1 |          20 | -0.13%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)   | 2026-10-15    | 2026-10-16   |        29.93  |              1 |          20 | +0.00%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-15    | 2026-10-16   |       125.05  |              1 |          20 | -0.16%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)   | 2026-10-15    | 2026-10-16   |       244.31  |              1 |          20 | -0.55%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-15    | 2026-10-16   |       150.37  |              1 |          20 | -2.03%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)   | 2026-10-15    | 2026-10-16   |       505.78  |              1 |          20 | -0.98%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)   | 2026-10-15    | 2026-10-16   |       197.06  |              1 |          20 | +0.16%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-15    | 2026-10-16   |        37.67  |              1 |          20 | -1.43%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)   | 2026-10-15    | 2026-10-16   |        86.69  |              1 |          20 | +0.46%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)   | 2026-10-15    | 2026-10-16   |        79.595 |              1 |          20 | +0.26%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)   | 2026-10-15    | 2026-10-16   |       255.41  |              1 |          20 | +0.87%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)   | 2026-10-15    | 2026-10-16   |       170.42  |              1 |          20 | +0.24%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-15    | 2026-10-16   |       136.02  |              1 |          20 | -2.16%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)   | 2026-10-16    |              |               |            nan |          20 |         |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV) | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI) | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)       | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)     | 2026-10-16    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-16    |              |               |            nan |          20 |         |