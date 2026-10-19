# Forward-test journal - 2026-10-19

Data through 2026-10-19; 518 of 518 symbols loaded.

## New signals today (2)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                              |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:------------------------------------------------------------------|
| insider_buy_beaten_down | [PEP](https://www.tradingview.com/chart/?symbol=PEP)   | 2026-10-16    |      133.57 |         120 | 3 buy(s) $17.90M @ 128.28, 6m -13%, vs MA200 -7%; POHLAD ROBERT C |
| early_rally_beaten_down | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB) | 2026-10-19    |      464.92 |          20 | golden_20_50; day +0.8%, 10d -3.3%, 6m -14%, vs MA200 -5%         |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |       86 |        0 | +0.96% | 64%   | +1.93%   | -0.04%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       31 |        6 | +0.66% | 58%   | +1.22%   | -0.54%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |        4 |        0 | +2.02% | 75%   | +1.49%   | +2.38%             |
| jev_pick                  | untested (forward test only)                     |       18 |        0 | +4.03% | 78%   | +4.83%   | -0.14%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       17 |        0 | +1.77% | 47%   | +2.00%   | +0.37%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 86, closed: 0, open: 86
- open trades mark-to-market: mean +0.96%, hit 64%
- SPY over the same holding periods: mean -0.97% (excess +1.93%)
- beaten-down basket over the same holding periods: mean +1.00% (excess -0.04%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 31, closed: 6, open: 25
- closed trades: mean -0.63%, median +0.13%, hit 50%, best +7.0%, worst -8.0%
- open trades mark-to-market: mean +0.97%, hit 60%
- SPY over the same holding periods: mean -0.56% (excess +1.22%)
- beaten-down basket over the same holding periods: mean +1.21% (excess -0.54%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 4, closed: 0, open: 4
- open trades mark-to-market: mean +2.02%, hit 75%
- SPY over the same holding periods: mean +0.53% (excess +1.49%)
- beaten-down basket over the same holding periods: mean -0.36% (excess +2.38%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 18, closed: 0, open: 18
- open trades mark-to-market: mean +4.03%, hit 78%
- SPY over the same holding periods: mean -0.80% (excess +4.83%)
- beaten-down basket over the same holding periods: mean +4.17% (excess -0.14%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 17, closed: 0, open: 17
- open trades mark-to-market: mean +1.77%, hit 47%
- SPY over the same holding periods: mean -0.23% (excess +2.00%)
- beaten-down basket over the same holding periods: mean +1.40% (excess +0.37%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |       100.58  |             30 |          60 | -2.80%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |       920.51  |             30 |          60 | -15.15% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |       232.71  |             29 |          60 | -5.45%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |       632     |             28 |          60 | +9.77%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |        52.32  |             29 |         120 | +3.21%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |        54.66  |             27 |          60 | +6.40%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |       441.33  |             24 |          60 | -13.20% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |        54.37  |             24 |         120 | +6.97%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |        72.99  |             27 |         120 | -4.15%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |        71.82  |             21 |          60 | -2.74%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |       148.65  |             18 |          20 | +0.24%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |       107.7   |             18 |          20 | -3.87%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |        33.99  |             17 |          60 | -16.24% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |       366.7   |             17 |          20 | -2.98%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |        14.45  |             16 |          20 | +5.47%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |        36.34  |             15 |          20 | +2.39%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |       602.02  |             14 |          60 | +29.74% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |        12.385 |             12 |          60 | +2.14%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |       614     |             12 |          60 | +27.21% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |             12 |          20 | +9.74%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |       238.11  |             12 |          20 | +1.82%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |       273.31  |             12 |          20 | +4.62%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |       162.22  |             12 |          20 | +12.83% |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |        30.98  |             12 |          20 | +11.23% |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |        79.5   |             12 |          20 | +9.74%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |       222.597 |             12 |          20 | +8.83%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |       121.94  |             12 |          20 | +3.37%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |       119.24  |             12 |          20 | -1.28%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |       101.99  |             12 |          20 | +1.51%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |       141.566 |             12 |          20 | -8.46%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |        33.82  |             11 |          60 | +10.02% |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |        47.64  |             11 |          20 | +6.88%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |       163.81  |             11 |          20 | +15.51% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |             10 |          60 | -1.41%  |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | 2026-10-06   |        84.2   |             10 |          20 | +6.02%  |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | 2026-10-06   |        77.73  |             10 |          20 | +4.71%  |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | 2026-10-06   |        83.45  |             10 |          20 | +6.73%  |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    | 2026-10-06   |       134.94  |             10 |          20 | +9.20%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |             10 |          20 | -13.64% |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |             10 |          20 | +5.04%  |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | 2026-10-06   |       140.83  |             10 |          20 | -1.41%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    | 2026-10-06   |        99.81  |             10 |          20 | -13.64% |
| jev_pick                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    | 2026-10-06   |       529.14  |             10 |          20 | +5.04%  |
| falling_wedge_beaten_down | [APTV](https://www.tradingview.com/chart/?symbol=APTV) | 2026-10-06    | 2026-10-07   |        44.35  |              9 |          20 | +0.29%  |
| falling_wedge_beaten_down | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-06    | 2026-10-07   |       103.16  |              9 |          20 | +3.72%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-06    | 2026-10-07   |       103.39  |              9 |          20 | +0.14%  |
| early_rally_beaten_down   | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-10-06    | 2026-10-07   |        15.15  |              9 |          20 | +0.59%  |
| early_rally_beaten_down   | [NI](https://www.tradingview.com/chart/?symbol=NI)     | 2026-10-06    | 2026-10-07   |        40.61  |              9 |          20 | +3.30%  |
| early_rally_beaten_down   | [EQT](https://www.tradingview.com/chart/?symbol=EQT)   | 2026-10-06    | 2026-10-07   |        52.59  |              9 |          20 | +3.48%  |
| early_rally_beaten_down   | [DTE](https://www.tradingview.com/chart/?symbol=DTE)   | 2026-10-06    | 2026-10-07   |       128.11  |              9 |          20 | -0.92%  |
| early_rally_beaten_down   | [PPL](https://www.tradingview.com/chart/?symbol=PPL)   | 2026-10-06    | 2026-10-07   |        33.7   |              9 |          20 | +1.81%  |
| early_rally_beaten_down   | [CNP](https://www.tradingview.com/chart/?symbol=CNP)   | 2026-10-06    | 2026-10-07   |        38.17  |              9 |          20 | +3.64%  |
| early_rally_beaten_down   | [PEG](https://www.tradingview.com/chart/?symbol=PEG)   | 2026-10-06    | 2026-10-07   |        71.68  |              9 |          20 | -1.90%  |
| early_rally_beaten_down   | [ETR](https://www.tradingview.com/chart/?symbol=ETR)   | 2026-10-06    | 2026-10-07   |       102.99  |              9 |          20 | +0.79%  |
| jev_pick                  | [COST](https://www.tradingview.com/chart/?symbol=COST) | 2026-10-06    | 2026-10-07   |       940.84  |              9 |          20 | +5.81%  |
| falling_wedge_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              8 |          20 | -7.55%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-10-07    | 2026-10-08   |       107.5   |              8 |          20 | -7.55%  |
| early_rally_beaten_down   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-10-07    | 2026-10-08   |       642     |              8 |          20 | +8.06%  |
| jev_pick                  | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-07    | 2026-10-08   |       126.47  |              8 |          20 | +3.40%  |
| falling_wedge_beaten_down | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-08    | 2026-10-09   |        85.58  |              7 |          20 | +4.08%  |
| early_rally_beaten_down   | [STZ](https://www.tradingview.com/chart/?symbol=STZ)   | 2026-10-08    | 2026-10-09   |       123.25  |              7 |          20 | +6.34%  |
| early_rally_beaten_down   | [ZTS](https://www.tradingview.com/chart/?symbol=ZTS)   | 2026-10-08    | 2026-10-09   |        73.04  |              7 |          20 | +8.97%  |
| early_rally_beaten_down   | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-08    | 2026-10-09   |        82.91  |              7 |          20 | +5.22%  |
| early_rally_beaten_down   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP) | 2026-10-08    | 2026-10-09   |        30.02  |              7 |          20 | +5.96%  |
| early_rally_beaten_down   | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)   | 2026-10-08    | 2026-10-09   |       309.25  |              7 |          20 | -1.24%  |
| early_rally_beaten_down   | [INTU](https://www.tradingview.com/chart/?symbol=INTU) | 2026-10-08    | 2026-10-09   |       305.05  |              7 |          20 | +6.74%  |
| early_rally_beaten_down   | [WMT](https://www.tradingview.com/chart/?symbol=WMT)   | 2026-10-08    | 2026-10-09   |       110     |              7 |          20 | +7.91%  |
| early_rally_beaten_down   | [TAP](https://www.tradingview.com/chart/?symbol=TAP)   | 2026-10-08    | 2026-10-09   |        37.61  |              7 |          20 | +4.57%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-08    | 2026-10-09   |       155.51  |              7 |          20 | +0.37%  |
| early_rally_beaten_down   | [FE](https://www.tradingview.com/chart/?symbol=FE)     | 2026-10-08    | 2026-10-09   |        44.83  |              7 |          20 | +0.94%  |
| early_rally_beaten_down   | [DUK](https://www.tradingview.com/chart/?symbol=DUK)   | 2026-10-08    | 2026-10-09   |       116.26  |              7 |          20 | +2.59%  |
| early_rally_beaten_down   | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-08    | 2026-10-09   |        85.94  |              7 |          20 | +3.87%  |
| early_rally_beaten_down   | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-08    | 2026-10-09   |       144     |              7 |          20 | +4.05%  |
| early_rally_beaten_down   | [XEL](https://www.tradingview.com/chart/?symbol=XEL)   | 2026-10-08    | 2026-10-09   |        73.17  |              7 |          20 | +2.69%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS) | 2026-10-09    | 2026-10-12   |       149.6   |              6 |          60 | +4.34%  |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)       | 2026-10-09    | 2026-10-12   |        22.26  |              6 |          60 | +4.22%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-09    | 2026-10-12   |       143.23  |              6 |          20 | +4.03%  |
| falling_wedge_beaten_down | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              6 |          20 | +0.36%  |
| early_rally_beaten_down   | [SBAC](https://www.tradingview.com/chart/?symbol=SBAC) | 2026-10-09    | 2026-10-12   |       181.77  |              6 |          20 | +0.73%  |
| early_rally_beaten_down   | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO) | 2026-10-09    | 2026-10-12   |        33.62  |              6 |          20 | -2.41%  |
| early_rally_beaten_down   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-09    | 2026-10-12   |        81.41  |              6 |          20 | -0.02%  |
| early_rally_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-10-09    | 2026-10-12   |        53.56  |              6 |          20 | +0.82%  |
| early_rally_beaten_down   | [SRE](https://www.tradingview.com/chart/?symbol=SRE)   | 2026-10-09    | 2026-10-12   |        81.45  |              6 |          20 | +0.36%  |
| early_rally_beaten_down   | [ATO](https://www.tradingview.com/chart/?symbol=ATO)   | 2026-10-09    | 2026-10-12   |       161.66  |              6 |          20 | +1.91%  |
| early_rally_beaten_down   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)   | 2026-10-09    | 2026-10-12   |       366.01  |              6 |          20 | -5.85%  |
| early_rally_beaten_down   | [WEC](https://www.tradingview.com/chart/?symbol=WEC)   | 2026-10-09    | 2026-10-12   |       103.99  |              6 |          20 | +2.89%  |
| early_rally_beaten_down   | [LNT](https://www.tradingview.com/chart/?symbol=LNT)   | 2026-10-09    | 2026-10-12   |        65.9   |              6 |          20 | +1.44%  |
| early_rally_beaten_down   | [AEP](https://www.tradingview.com/chart/?symbol=AEP)   | 2026-10-09    | 2026-10-12   |       123.2   |              6 |          20 | +1.23%  |
| falling_wedge_beaten_down | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-12    | 2026-10-13   |       486.79  |              5 |          20 | +4.90%  |
| falling_wedge_beaten_down | [YUM](https://www.tradingview.com/chart/?symbol=YUM)   | 2026-10-12    | 2026-10-13   |       147.47  |              5 |          20 | +1.60%  |
| early_rally_beaten_down   | [PODD](https://www.tradingview.com/chart/?symbol=PODD) | 2026-10-12    | 2026-10-13   |       140.79  |              5 |          20 | +0.83%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)   | 2026-10-12    | 2026-10-13   |        13.21  |              5 |          20 | -0.61%  |
| early_rally_beaten_down   | [EIX](https://www.tradingview.com/chart/?symbol=EIX)   | 2026-10-12    | 2026-10-13   |        56.04  |              5 |          20 | -0.64%  |
| early_rally_beaten_down   | [CMS](https://www.tradingview.com/chart/?symbol=CMS)   | 2026-10-12    | 2026-10-13   |        66.28  |              5 |          20 | +1.64%  |
| early_rally_beaten_down   | [EXC](https://www.tradingview.com/chart/?symbol=EXC)   | 2026-10-12    | 2026-10-13   |        42.6   |              5 |          20 | -0.45%  |
| early_rally_beaten_down   | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-10-12    | 2026-10-13   |      1113.01  |              5 |          20 | +2.65%  |
| early_rally_beaten_down   | [GEHC](https://www.tradingview.com/chart/?symbol=GEHC) | 2026-10-12    | 2026-10-13   |        67.74  |              5 |          20 | +2.98%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-13    | 2026-10-14   |        32.85  |              4 |          20 | +0.40%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-10-13    | 2026-10-14   |       182.6   |              4 |          20 | +2.33%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS) | 2026-10-13    | 2026-10-14   |        67.9   |              4 |          20 | +4.62%  |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG) | 2026-10-13    | 2026-10-14   |       220.63  |              4 |          20 | +2.60%  |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)   | 2026-10-13    | 2026-10-14   |        57.66  |              4 |          20 | +1.77%  |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)   | 2026-10-13    | 2026-10-14   |       191.79  |              4 |          20 | +1.87%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV) | 2026-10-14    | 2026-10-15   |        61.43  |              3 |          60 | -0.50%  |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)   | 2026-10-14    | 2026-10-15   |        33.27  |              3 |          20 | -1.83%  |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN) | 2026-10-14    | 2026-10-15   |       342.5   |              3 |          20 | +0.50%  |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)   | 2026-10-14    | 2026-10-15   |       153.24  |              3 |          20 | +3.48%  |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)   | 2026-10-14    | 2026-10-15   |        61.37  |              3 |          20 | +3.81%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-10-14    | 2026-10-15   |       531     |              3 |          20 | +3.24%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV) | 2026-10-15    | 2026-10-16   |        65.195 |              2 |          60 | -6.25%  |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-15    | 2026-10-16   |       136.02  |              2 |          20 | -3.86%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT) | 2026-10-15    | 2026-10-16   |        27.96  |              2 |          20 | -1.61%  |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)   | 2026-10-15    | 2026-10-16   |        83.4   |              2 |          20 | -0.26%  |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)   | 2026-10-15    | 2026-10-16   |       529.98  |              2 |          20 | -1.48%  |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-10-15    | 2026-10-16   |       357.38  |              2 |          20 | -0.45%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)   | 2026-10-15    | 2026-10-16   |      3091     |              2 |          20 | +0.22%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)   | 2026-10-15    | 2026-10-16   |        13.29  |              2 |          20 | -7.75%  |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)   | 2026-10-15    | 2026-10-16   |        36.42  |              2 |          20 | -1.21%  |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-15    | 2026-10-16   |       120.66  |              2 |          20 | -2.44%  |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)   | 2026-10-15    | 2026-10-16   |       295.89  |              2 |          20 | +0.69%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-10-15    | 2026-10-16   |        69.87  |              2 |          20 | -0.03%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)   | 2026-10-15    | 2026-10-16   |        44.45  |              2 |          20 | +1.35%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)   | 2026-10-15    | 2026-10-16   |        29.93  |              2 |          20 | +0.50%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-15    | 2026-10-16   |       125.05  |              2 |          20 | +0.80%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)   | 2026-10-15    | 2026-10-16   |       244.31  |              2 |          20 | -0.67%  |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-10-15    | 2026-10-16   |       150.37  |              2 |          20 | -0.91%  |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)   | 2026-10-15    | 2026-10-16   |       505.78  |              2 |          20 | -0.82%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)   | 2026-10-15    | 2026-10-16   |       197.06  |              2 |          20 | -0.58%  |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-15    | 2026-10-16   |        37.67  |              2 |          20 | -1.22%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)   | 2026-10-15    | 2026-10-16   |        86.69  |              2 |          20 | -1.30%  |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)   | 2026-10-15    | 2026-10-16   |        79.6   |              2 |          20 | -1.80%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)   | 2026-10-15    | 2026-10-16   |       255.41  |              2 |          20 | +0.80%  |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)   | 2026-10-15    | 2026-10-16   |       170.42  |              2 |          20 | -2.01%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE) | 2026-10-15    | 2026-10-16   |       136.02  |              2 |          20 | -3.86%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)   | 2026-10-16    | 2026-10-19   |       169.41  |              1 |          20 | -1.42%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)   | 2026-10-16    | 2026-10-19   |        45.99  |              1 |          20 | -0.28%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)   | 2026-10-16    | 2026-10-19   |       511     |              1 |          20 | -0.07%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-10-16    | 2026-10-19   |        57.29  |              1 |          20 | +1.52%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)   | 2026-10-16    | 2026-10-19   |       289.03  |              1 |          20 | +0.25%  |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)   | 2026-10-16    | 2026-10-19   |       268.28  |              1 |          20 | +0.51%  |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)   | 2026-10-16    | 2026-10-19   |       245.16  |              1 |          20 | -0.54%  |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV) | 2026-10-16    | 2026-10-19   |        47.39  |              1 |          20 | +0.63%  |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI) | 2026-10-16    | 2026-10-19   |        23.48  |              1 |          20 | -1.62%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)   | 2026-10-16    | 2026-10-19   |       130.875 |              1 |          20 | +2.06%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-16    | 2026-10-19   |       104.155 |              1 |          20 | -0.60%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)       | 2026-10-16    | 2026-10-19   |        55.8   |              1 |          20 | -0.52%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)     | 2026-10-16    | 2026-10-19   |       306.55  |              1 |          20 | +1.09%  |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)   | 2026-10-16    | 2026-10-19   |        33.45  |              1 |          20 | -1.41%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)   | 2026-10-16    | 2026-10-19   |       130.875 |              1 |         120 | +2.06%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB) | 2026-10-19    |              |               |            nan |          20 |         |