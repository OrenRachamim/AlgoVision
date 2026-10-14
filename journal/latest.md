# Forward-test journal - 2026-10-14

Data through 2026-10-14; 518 of 518 symbols loaded.

## New signals today (6)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                                        |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:----------------------------------------------------------------------------|
| newsday                 | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV) | 2026-10-14    |       65.78 |          60 | gap -7.7%, vol 3.5x, 6m -45%, vs MA200 -29%                                 |
| early_rally_beaten_down | [ROL](https://www.tradingview.com/chart/?symbol=ROL)   | 2026-10-14    |       32.63 |          20 | higher_high, rsi_turn, thrust; day +1.5%, 10d +8.3%, 6m -39%, vs MA200 -32% |
| early_rally_beaten_down | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN) | 2026-10-14    |      359.6  |          20 | golden_20_50; day -10.2%, 10d +2.2%, 6m -24%, vs MA200 -10%                 |
| early_rally_beaten_down | [EFX](https://www.tradingview.com/chart/?symbol=EFX)   | 2026-10-14    |      150.36 |          20 | thrust; day +0.9%, 10d +9.6%, 6m -19%, vs MA200 -16%                        |
| early_rally_beaten_down | [LYB](https://www.tradingview.com/chart/?symbol=LYB)   | 2026-10-14    |       61.17 |          20 | rsi_turn; day +1.9%, 10d +6.4%, 6m -15%, vs MA200 -1%                       |
| early_rally_beaten_down | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-10-14    |      522.23 |          20 | rsi_turn; day +3.6%, 10d +2.5%, 6m -13%, vs MA200 -6%                       |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       54 |        0 | +0.58% | 69%   | +1.50%   | +0.05%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       24 |        3 | -0.62% | 46%   | -0.47%   | -0.83%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        3 |        0 | -0.17% | 67%   | -1.31%   | +1.91%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +1.66% | 61%   | +2.06%   | -0.60%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       16 |        0 | +0.16% | 53%   | -0.05%   | +0.41%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 54, closed: 0, open: 54
- open trades mark-to-market: mean +0.58%, hit 69%
- SPY over the same holding periods: mean -0.92% (excess +1.50%)
- beaten-down basket over the same holding periods: mean +0.52% (excess +0.05%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 24, closed: 3, open: 21
- closed trades: mean -6.32%, median -7.52%, hit 0%, best -3.5%, worst -8.0%
- open trades mark-to-market: mean +0.19%, hit 52%
- SPY over the same holding periods: mean -0.15% (excess -0.47%)
- beaten-down basket over the same holding periods: mean +0.21% (excess -0.83%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean -0.17%, hit 67%
- SPY over the same holding periods: mean +1.15% (excess -1.31%)
- beaten-down basket over the same holding periods: mean -2.08% (excess +1.91%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +1.66%, hit 61%
- SPY over the same holding periods: mean -0.40% (excess +2.06%)
- beaten-down basket over the same holding periods: mean +2.27% (excess -0.60%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 16, closed: 0, open: 16
- open trades mark-to-market: mean +0.16%, hit 53%
- SPY over the same holding periods: mean +0.21% (excess -0.05%)
- beaten-down basket over the same holding periods: mean -0.25% (excess +0.41%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |       100.58  |             27 |          60 | -6.45%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |       920.51  |             27 |          60 | -21.82% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |       232.71  |             26 |          60 | -6.52%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |       632     |             25 |          60 | +3.42%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |        52.32  |             26 |         120 | +3.63%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |        54.66  |             24 |          60 | +0.40%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |       441.33  |             21 |          60 | -7.46%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |        54.37  |             21 |         120 | +0.94%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |        72.99  |             24 |         120 | -5.07%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |        71.82  |             18 |          60 | -1.74%  |
| falling_wedge_beaten_down | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-09-18    | 2026-09-21   |       532.3   |             18 |          20 | -1.89%  |
| falling_wedge_beaten_down | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-09-18    | 2026-09-21   |      1091.3   |             18 |          20 | +1.69%  |
| falling_wedge_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-09-21    | 2026-09-22   |       519.27  |             17 |          20 | +1.88%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |       148.65  |             15 |          20 | -2.83%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |       107.7   |             15 |          20 | -4.61%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |        33.99  |             14 |          60 | -14.80% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |       366.7   |             14 |          20 | -4.87%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |        14.45  |             13 |          20 | +2.91%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |        36.34  |             12 |          20 | -2.86%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |       602.02  |             11 |          60 | +19.54% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |        12.385 |              9 |          60 | +8.20%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |       614     |              9 |          60 | +17.20% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              9 |          20 | +4.18%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |       238.11  |              9 |          20 | -0.91%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |       273.31  |              9 |          20 | +5.27%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |       162.22  |              9 |          20 | +10.59% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |        30.98  |              9 |          20 | +6.91%  |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |              9 |          20 | +4.18%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |       222.597 |              9 |          20 | +3.38%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |       121.94  |              9 |          20 | -1.11%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |       119.24  |              9 |          20 | -3.53%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |       101.99  |              9 |          20 | +0.74%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |       141.566 |              9 |          20 | -7.78%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |        33.82  |              8 |          60 | +4.38%  |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |        47.64  |              8 |          20 | +4.79%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |       163.81  |              8 |          20 | +10.24% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              7 |          60 | -0.98%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | 2026-10-06   |        84.2   |              7 |          20 | +6.15%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | 2026-10-06   |        77.73  |              7 |          20 | +4.79%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | 2026-10-06   |        83.45  |              7 |          20 | +3.88%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    | 2026-10-06   |       134.94  |              7 |          20 | +5.85%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              7 |          20 | -11.97% |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              7 |          20 | -0.02%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |              7 |          20 | -0.98%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |              7 |          20 | -11.97% |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |              7 |          20 | -0.02%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV) | 2026-10-06    | 2026-10-07   |        44.35  |              6 |          20 | -1.17%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-06    | 2026-10-07   |       103.16  |              6 |          20 | +3.48%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-06    | 2026-10-07   |       103.39  |              6 |          20 | -0.63%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-10-06    | 2026-10-07   |        15.15  |              6 |          20 | -1.85%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)     | 2026-10-06    | 2026-10-07   |        40.61  |              6 |          20 | +1.60%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)   | 2026-10-06    | 2026-10-07   |        52.59  |              6 |          20 | +0.30%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)   | 2026-10-06    | 2026-10-07   |       128.11  |              6 |          20 | +0.16%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)   | 2026-10-06    | 2026-10-07   |        33.7   |              6 |          20 | +3.12%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)   | 2026-10-06    | 2026-10-07   |        38.17  |              6 |          20 | +3.96%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)   | 2026-10-06    | 2026-10-07   |        71.68  |              6 |          20 | -1.56%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)   | 2026-10-06    | 2026-10-07   |       102.99  |              6 |          20 | +1.47%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST) | 2026-10-06    | 2026-10-07   |       940.84  |              6 |          20 | +4.37%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              5 |          20 | -6.19%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              5 |          20 | -6.19%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-10-07    | 2026-10-08   |       642     |              5 |          20 | +1.81%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-07    | 2026-10-08   |       126.47  |              5 |          20 | +1.90%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-08    | 2026-10-09   |        85.58  |              4 |          20 | +1.30%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)   | 2026-10-08    | 2026-10-09   |       123.25  |              4 |          20 | +3.38%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)   | 2026-10-08    | 2026-10-09   |        73.04  |              4 |          20 | +3.08%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-08    | 2026-10-09   |        82.91  |              4 |          20 | -0.11%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP) | 2026-10-08    | 2026-10-09   |        30.02  |              4 |          20 | +0.30%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)   | 2026-10-08    | 2026-10-09   |       309.25  |              4 |          20 | -4.32%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU) | 2026-10-08    | 2026-10-09   |       305.05  |              4 |          20 | +1.77%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)   | 2026-10-08    | 2026-10-09   |       110     |              4 |          20 | +5.60%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)   | 2026-10-08    | 2026-10-09   |        37.61  |              4 |          20 | +2.71%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-08    | 2026-10-09   |       155.51  |              4 |          20 | +1.47%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)     | 2026-10-08    | 2026-10-09   |        44.83  |              4 |          20 | +1.29%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)   | 2026-10-08    | 2026-10-09   |       116.26  |              4 |          20 | +2.91%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-08    | 2026-10-09   |        85.94  |              4 |          20 | +4.00%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-08    | 2026-10-09   |       144     |              4 |          20 | +1.87%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)   | 2026-10-08    | 2026-10-09   |        73.17  |              4 |          20 | +2.99%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-09    | 2026-10-12   |       149.6   |              3 |          60 | +5.47%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)       | 2026-10-09    | 2026-10-12   |        22.26  |              3 |          60 | +3.55%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-09    | 2026-10-12   |       143.23  |              3 |          20 | +0.84%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              3 |          20 | +0.66%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC) | 2026-10-09    | 2026-10-12   |       181.77  |              3 |          20 | -0.58%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO) | 2026-10-09    | 2026-10-12   |        33.62  |              3 |          20 | -2.62%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-09    | 2026-10-12   |        81.41  |              3 |          20 | +0.05%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-10-09    | 2026-10-12   |        53.56  |              3 |          20 | +1.23%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              3 |          20 | +0.66%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)   | 2026-10-09    | 2026-10-12   |       161.66  |              3 |          20 | +1.41%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)   | 2026-10-09    | 2026-10-12   |       366.01  |              3 |          20 | -3.13%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-09    | 2026-10-12   |       103.99  |              3 |          20 | +2.65%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)   | 2026-10-09    | 2026-10-12   |        65.9   |              3 |          20 | +2.44%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)   | 2026-10-09    | 2026-10-12   |       123.2   |              3 |          20 | +2.38%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-12    | 2026-10-13   |       486.79  |              2 |          20 | +1.83%  |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-12    | 2026-10-13   |       147.47  |              2 |          20 | -0.53%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD) | 2026-10-12    | 2026-10-13   |       140.79  |              2 |          20 | -4.87%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)   | 2026-10-12    | 2026-10-13   |        13.21  |              2 |          20 | -0.45%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)   | 2026-10-12    | 2026-10-13   |        56.04  |              2 |          20 | -1.07%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)   | 2026-10-12    | 2026-10-13   |        66.28  |              2 |          20 | +0.81%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)   | 2026-10-12    | 2026-10-13   |        42.6   |              2 |          20 | -0.00%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-10-12    | 2026-10-13   |      1113.01  |              2 |          20 | -0.29%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC) | 2026-10-12    | 2026-10-13   |        67.74  |              2 |          20 | +1.08%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-13    | 2026-10-14   |        32.85  |              1 |          20 | -0.06%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-10-13    | 2026-10-14   |       182.6   |              1 |          20 | +0.97%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS) | 2026-10-13    | 2026-10-14   |        67.9   |              1 |          20 | +1.78%  |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG) | 2026-10-13    | 2026-10-14   |       220.63  |              1 |          20 | +1.05%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)   | 2026-10-13    | 2026-10-14   |        57.66  |              1 |          20 | +0.29%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)   | 2026-10-13    | 2026-10-14   |       191.79  |              1 |          20 | +0.80%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV) | 2026-10-14    |              |               |            nan |          60 |         |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)   | 2026-10-14    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN) | 2026-10-14    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)   | 2026-10-14    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)   | 2026-10-14    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-10-14    |              |               |            nan |          20 |         |