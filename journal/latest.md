# Forward-test journal - 2026-10-20

Data through 2026-10-20; 518 of 518 symbols loaded.

## New signals today (9)

| rule                      | symbol                                                   | signal_date   |   ref_price |   hold_bars | note                                                   |
|:--------------------------|:---------------------------------------------------------|:--------------|------------:|------------:|:-------------------------------------------------------|
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    |      110.34 |          20 | score 0.77, stop 101.10, level 107.75                  |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    |       55.38 |          20 | score 0.74, stop 49.63, level 55.12                    |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    |       99.94 |          20 | rsi_turn; day +2.2%, 10d +6.8%, 6m -40%, vs MA200 -28% |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    |       85.22 |          20 | rsi_turn; day +2.5%, 10d +1.9%, 6m -27%, vs MA200 -19% |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    |       22.36 |          20 | rsi_turn; day +2.1%, 10d +5.3%, 6m -21%, vs MA200 -13% |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    |       78.65 |          20 | rsi_turn; day +3.7%, 10d +2.3%, 6m -16%, vs MA200 -14% |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    |      536.22 |          20 | rsi_turn; day +2.7%, 10d +0.2%, 6m -16%, vs MA200 -11% |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    |       77.15 |          20 | rsi_turn; day +1.2%, 10d +2.1%, 6m -15%, vs MA200 -13% |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    |       56.17 |          20 | rsi_turn; day +1.7%, 10d +0.1%, 6m -8%, vs MA200 -9%   |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       93 |        0 | +2.30% | 83%   | +2.93%   | +0.03%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       33 |        6 | +2.02% | 74%   | +2.31%   | -0.25%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        4 |        0 | +2.86% | 75%   | +1.99%   | +1.92%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +4.74% | 78%   | +5.21%   | -0.87%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       17 |        0 | +2.91% | 53%   | +2.80%   | +0.15%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 93, closed: 0, open: 93
- open trades mark-to-market: mean +2.30%, hit 83%
- SPY over the same holding periods: mean -0.63% (excess +2.93%)
- beaten-down basket over the same holding periods: mean +2.27% (excess +0.03%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 33, closed: 6, open: 27
- closed trades: mean -0.63%, median +0.13%, hit 50%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +2.65%, hit 80%
- SPY over the same holding periods: mean -0.29% (excess +2.31%)
- beaten-down basket over the same holding periods: mean +2.26% (excess -0.25%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 4, closed: 0, open: 4
- open trades mark-to-market: mean +2.86%, hit 75%
- SPY over the same holding periods: mean +0.87% (excess +1.99%)
- beaten-down basket over the same holding periods: mean +0.94% (excess +1.92%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +4.74%, hit 78%
- SPY over the same holding periods: mean -0.47% (excess +5.21%)
- beaten-down basket over the same holding periods: mean +5.60% (excess -0.87%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 17, closed: 0, open: 17
- open trades mark-to-market: mean +2.91%, hit 53%
- SPY over the same holding periods: mean +0.11% (excess +2.80%)
- beaten-down basket over the same holding periods: mean +2.75% (excess +0.15%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |       100.58  |             31 |          60 | -0.64%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |       920.51  |             31 |          60 | -13.12% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |       232.71  |             30 |          60 | -9.06%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |       632     |             29 |          60 | +8.31%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |        52.32  |             30 |         120 | +5.85%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |        54.66  |             28 |          60 | +8.16%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |       441.33  |             25 |          60 | -11.03% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |        54.37  |             25 |         120 | +8.74%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |        72.99  |             28 |         120 | -5.55%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |        71.82  |             22 |          60 | -4.36%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-09-23    | 2026-09-24   |       148.65  |             19 |          20 | +1.24%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-09-23    | 2026-09-24   |       107.7   |             19 |          20 | -2.49%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |        33.99  |             18 |          60 | -14.97% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-09-24    | 2026-09-25   |       366.7   |             18 |          20 | -0.80%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-09-25    | 2026-09-28   |        14.45  |             17 |          20 | +8.30%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-09-28    | 2026-09-29   |        36.34  |             16 |          20 | +4.24%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |       602.02  |             15 |          60 | +32.84% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |        12.385 |             13 |          60 | +4.16%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |       614     |             13 |          60 | +30.25% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |        79.5   |             13 |          20 | +9.90%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)     | 2026-10-01    | 2026-10-02   |       238.11  |             13 |          20 | +1.81%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)     | 2026-10-01    | 2026-10-02   |       273.31  |             13 |          20 | +5.43%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)     | 2026-10-01    | 2026-10-02   |       162.22  |             13 |          20 | +13.15% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)     | 2026-10-01    | 2026-10-02   |        30.98  |             13 |          20 | +11.78% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-01    | 2026-10-02   |        79.5   |             13 |          20 | +9.90%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE)   | 2026-10-01    | 2026-10-02   |       222.597 |             13 |          20 | +10.48% |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-01    | 2026-10-02   |       121.94  |             13 |          20 | +4.69%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-01    | 2026-10-02   |       119.24  |             13 |          20 | -1.42%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-01    | 2026-10-02   |       101.99  |             13 |          20 | +2.97%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-01    | 2026-10-02   |       141.566 |             13 |          20 | -7.37%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |        33.82  |             12 |          60 | +12.00% |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)     | 2026-10-02    | 2026-10-05   |        47.64  |             12 |          20 | +5.75%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK)   | 2026-10-02    | 2026-10-05   |       163.81  |             12 |          20 | +16.52% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |       140.83  |             11 |          60 | -0.18%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-05    | 2026-10-06   |        84.2   |             11 |          20 | +7.73%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-05    | 2026-10-06   |        77.73  |             11 |          20 | +5.02%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-05    | 2026-10-06   |        83.45  |             11 |          20 | +7.87%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-10-05    | 2026-10-06   |       134.94  |             11 |          20 | +8.93%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |        99.81  |             11 |          20 | -13.45% |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |       529.14  |             11 |          20 | +5.44%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |       140.83  |             11 |          20 | -0.18%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-10-05    | 2026-10-06   |        99.81  |             11 |          20 | -13.45% |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-10-05    | 2026-10-06   |       529.14  |             11 |          20 | +5.44%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV)   | 2026-10-06    | 2026-10-07   |        44.35  |             10 |          20 | +1.60%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-06    | 2026-10-07   |       103.16  |             10 |          20 | +5.42%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-06    | 2026-10-07   |       103.39  |             10 |          20 | +1.58%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH)   | 2026-10-06    | 2026-10-07   |        15.15  |             10 |          20 | +3.30%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)       | 2026-10-06    | 2026-10-07   |        40.61  |             10 |          20 | +5.29%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)     | 2026-10-06    | 2026-10-07   |        52.59  |             10 |          20 | +4.24%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)     | 2026-10-06    | 2026-10-07   |       128.11  |             10 |          20 | +0.94%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)     | 2026-10-06    | 2026-10-07   |        33.7   |             10 |          20 | +2.70%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)     | 2026-10-06    | 2026-10-07   |        38.17  |             10 |          20 | +5.42%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-06    | 2026-10-07   |        71.68  |             10 |          20 | -1.14%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)     | 2026-10-06    | 2026-10-07   |       102.99  |             10 |          20 | +2.11%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST)   | 2026-10-06    | 2026-10-07   |       940.84  |             10 |          20 | +5.72%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |       107.5   |              9 |          20 | -8.99%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-10-07    | 2026-10-08   |       107.5   |              9 |          20 | -8.99%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-07    | 2026-10-08   |       642     |              9 |          20 | +6.62%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-07    | 2026-10-08   |       126.47  |              9 |          20 | +6.14%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY)   | 2026-10-08    | 2026-10-09   |        85.58  |              8 |          20 | +5.19%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)     | 2026-10-08    | 2026-10-09   |       123.25  |              8 |          20 | +7.70%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)     | 2026-10-08    | 2026-10-09   |        73.04  |              8 |          20 | +9.58%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK)   | 2026-10-08    | 2026-10-09   |        82.91  |              8 |          20 | +5.38%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-08    | 2026-10-09   |        30.02  |              8 |          20 | +10.09% |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-10-08    | 2026-10-09   |       309.25  |              8 |          20 | +2.28%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-10-08    | 2026-10-09   |       305.05  |              8 |          20 | +9.91%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)     | 2026-10-08    | 2026-10-09   |       110     |              8 |          20 | +7.14%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)     | 2026-10-08    | 2026-10-09   |        37.61  |              8 |          20 | +6.89%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-08    | 2026-10-09   |       155.51  |              8 |          20 | +1.44%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)       | 2026-10-08    | 2026-10-09   |        44.83  |              8 |          20 | +1.99%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)     | 2026-10-08    | 2026-10-09   |       116.26  |              8 |          20 | +4.36%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)       | 2026-10-08    | 2026-10-09   |        85.94  |              8 |          20 | +5.55%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-08    | 2026-10-09   |       144     |              8 |          20 | +5.28%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)     | 2026-10-08    | 2026-10-09   |        73.17  |              8 |          20 | +4.80%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |       149.6   |              7 |          60 | +5.45%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |        22.26  |              7 |          60 | +5.21%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-09    | 2026-10-12   |       143.23  |              7 |          20 | +5.07%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |        81.45  |              7 |          20 | +1.67%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC)   | 2026-10-09    | 2026-10-12   |       181.77  |              7 |          20 | -0.44%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-10-09    | 2026-10-12   |        33.62  |              7 |          20 | -2.11%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-10-09    | 2026-10-12   |        81.41  |              7 |          20 | +0.27%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-09    | 2026-10-12   |        53.56  |              7 |          20 | +3.40%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)     | 2026-10-09    | 2026-10-12   |        81.45  |              7 |          20 | +1.67%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)     | 2026-10-09    | 2026-10-12   |       161.66  |              7 |          20 | +3.38%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-09    | 2026-10-12   |       366.01  |              7 |          20 | -6.51%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)     | 2026-10-09    | 2026-10-12   |       103.99  |              7 |          20 | +4.58%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)     | 2026-10-09    | 2026-10-12   |        65.9   |              7 |          20 | +3.60%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)     | 2026-10-09    | 2026-10-12   |       123.2   |              7 |          20 | +3.26%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-12    | 2026-10-13   |       486.79  |              6 |          20 | +9.70%  |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)     | 2026-10-12    | 2026-10-13   |       147.47  |              6 |          20 | +2.80%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD)   | 2026-10-12    | 2026-10-13   |       140.79  |              6 |          20 | +1.31%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-10-12    | 2026-10-13   |        13.21  |              6 |          20 | -0.23%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)     | 2026-10-12    | 2026-10-13   |        56.04  |              6 |          20 | +0.87%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)     | 2026-10-12    | 2026-10-13   |        66.28  |              6 |          20 | +3.23%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)     | 2026-10-12    | 2026-10-13   |        42.6   |              6 |          20 | +1.01%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)     | 2026-10-12    | 2026-10-13   |      1113.01  |              6 |          20 | +2.70%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC)   | 2026-10-12    | 2026-10-13   |        67.74  |              6 |          20 | +3.68%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |        32.85  |              5 |          20 | +2.25%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |       182.6   |              5 |          20 | +3.14%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |        67.9   |              5 |          20 | +6.14%  |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |       220.63  |              5 |          20 | +2.92%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |        57.66  |              5 |          20 | +3.26%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |       191.79  |              5 |          20 | +2.79%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |        61.43  |              4 |          60 | +1.14%  |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |        33.27  |              4 |          20 | +0.21%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |       342.5   |              4 |          20 | -0.16%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |       153.24  |              4 |          20 | +15.20% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |        61.37  |              4 |          20 | +4.22%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |       531     |              4 |          20 | +3.34%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |        65.195 |              3 |          60 | -4.70%  |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |       136.02  |              3 |          20 | -1.32%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |        27.96  |              3 |          20 | -0.46%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |        83.4   |              3 |          20 | +2.18%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |       529.98  |              3 |          20 | +1.18%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |       357.38  |              3 |          20 | +1.79%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |      3091     |              3 |          20 | +2.24%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |        13.29  |              3 |          20 | -4.82%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |        36.42  |              3 |          20 | +0.03%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |       120.66  |              3 |          20 | -2.58%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |       295.89  |              3 |          20 | +2.88%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |        69.87  |              3 |          20 | -1.69%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |        44.45  |              3 |          20 | +2.54%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |        29.93  |              3 |          20 | +2.54%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |       125.05  |              3 |          20 | +2.09%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |       244.31  |              3 |          20 | +0.90%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |       150.37  |              3 |          20 | +0.08%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |       505.78  |              3 |          20 | +0.36%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |       197.06  |              3 |          20 | +0.75%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |        37.67  |              3 |          20 | +0.56%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |        86.69  |              3 |          20 | +0.88%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |        79.6   |              3 |          20 | -0.93%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |       255.41  |              3 |          20 | +2.55%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |       170.42  |              3 |          20 | -0.49%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |       136.02  |              3 |          20 | -1.32%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |       169.41  |              2 |          20 | +0.10%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |        45.99  |              2 |          20 | +3.39%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |       511     |              2 |          20 | +4.50%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |        57.29  |              2 |          20 | +3.19%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |       289.03  |              2 |          20 | +2.66%  |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |       268.28  |              2 |          20 | +1.47%  |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |       245.16  |              2 |          20 | +1.47%  |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |        47.42  |              2 |          20 | +1.75%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |        23.48  |              2 |          20 | -0.47%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |       130.88  |              2 |          20 | +2.40%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |       104.16  |              2 |          20 | +0.83%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |        55.8   |              2 |          20 | +0.97%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |       306.55  |              2 |          20 | +2.79%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |        33.45  |              2 |          20 | +0.42%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |       130.88  |              2 |         120 | +2.40%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |       454.74  |              1 |          20 | +1.01%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    |              |               |            nan |          20 |         |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    |              |               |            nan |          20 |         |