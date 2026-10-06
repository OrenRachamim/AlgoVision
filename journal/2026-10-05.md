# Forward-test journal - 2026-10-05

Data through 2026-10-05; 518 of 518 symbols loaded.

## New signals today (3)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                                |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:--------------------------------------------------------------------|
| early_rally_beaten_down | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    |      134.41 |          20 | higher_high, rsi_turn; day +1.3%, 10d +2.6%, 6m -16%, vs MA200 -11% |
| early_rally_beaten_down | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    |       98.21 |          20 | higher_high; day +4.2%, 10d +3.0%, 6m -23%, vs MA200 -10%           |
| early_rally_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    |      527.07 |          20 | rsi_turn; day +1.7%, 10d +2.3%, 6m -9%, vs MA200 -10%               |

## Running results

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 3, closed: 0, open: 3

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 14, closed: 1, open: 13
- closed trades: mean -3.46%, median -3.46%, hit 0%, best -3.5%, worst -3.5%
- open trades mark-to-market: mean -2.53%, hit 36%
- SPY over the same holding periods: mean +1.08% (excess -3.69%)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 3, closed: 0, open: 3
- open trades mark-to-market: mean -0.52%, hit 33%
- SPY over the same holding periods: mean +1.83% (excess -2.35%)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 13, closed: 0, open: 13
- open trades mark-to-market: mean -0.41%, hit 50%
- SPY over the same holding periods: mean +0.57% (excess -0.98%)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 13, closed: 0, open: 13
- open trades mark-to-market: mean -2.41%, hit 42%
- SPY over the same holding periods: mean +1.23% (excess -3.64%)


## Open positions

| rule                      | symbol                                                 | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:-------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU) | 2026-09-04    | 2026-09-08   |      100.58   |             20 |          60 | -7.40%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-04    | 2026-09-08   |      920.51   |             20 |          60 | -25.08% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)   | 2026-09-08    | 2026-09-09   |      232.71   |             19 |          60 | -1.35%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY) | 2026-09-09    | 2026-09-10   |      632      |             18 |          60 | -2.32%  |
| falling_wedge_beaten_down | [TXT](https://www.tradingview.com/chart/?symbol=TXT)   | 2026-09-09    | 2026-09-10   |       79.3599 |             18 |          20 | -4.55%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)   | 2026-09-08    | 2026-09-09   |       52.32   |             19 |         120 | -1.17%  |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-10    | 2026-09-11   |       54.66   |             17 |          60 | +3.86%  |
| falling_wedge_beaten_down | [TXT](https://www.tradingview.com/chart/?symbol=TXT)   | 2026-09-11    | 2026-09-14   |       80.19   |             16 |          20 | -5.54%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-09-15    | 2026-09-16   |      441.33   |             14 |          60 | -6.69%  |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)   | 2026-09-15    | 2026-09-16   |       54.37   |             14 |         120 | +4.41%  |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER) | 2026-09-10    | 2026-09-11   |       72.99   |             17 |         120 | -4.81%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX) | 2026-09-18    | 2026-09-21   |       71.82   |             11 |          60 | -6.02%  |
| falling_wedge_beaten_down | [LMT](https://www.tradingview.com/chart/?symbol=LMT)   | 2026-09-18    | 2026-09-21   |      532.3    |             11 |          20 | -4.82%  |
| falling_wedge_beaten_down | [TDG](https://www.tradingview.com/chart/?symbol=TDG)   | 2026-09-18    | 2026-09-21   |     1091.3    |             11 |          20 | +0.12%  |
| falling_wedge_beaten_down | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-09-21    | 2026-09-22   |      519.27   |             10 |          20 | +1.50%  |
| falling_wedge_beaten_down | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN) | 2026-09-23    | 2026-09-24   |      148.65   |              8 |          20 | -5.38%  |
| falling_wedge_beaten_down | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-09-23    | 2026-09-24   |      107.7    |              8 |          20 | -4.90%  |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)   | 2026-09-24    | 2026-09-25   |       33.99   |              7 |          60 | -11.24% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)   | 2026-09-24    | 2026-09-25   |      366.7    |              7 |          20 | -1.51%  |
| falling_wedge_beaten_down | [NCLH](https://www.tradingview.com/chart/?symbol=NCLH) | 2026-09-25    | 2026-09-28   |       14.45   |              6 |          20 | +2.91%  |
| falling_wedge_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-09-28    | 2026-09-29   |       36.34   |              5 |          20 | -6.55%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-09-29    | 2026-09-30   |      602.02   |              4 |          60 | +14.55% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA) | 2026-10-01    | 2026-10-02   |       12.385  |              2 |          60 | +0.04%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO) | 2026-10-01    | 2026-10-02   |      614      |              2 |          60 | +12.31% |
| falling_wedge_beaten_down | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |       79.5    |              2 |          20 | +0.89%  |
| jev_pick                  | [CRM](https://www.tradingview.com/chart/?symbol=CRM)   | 2026-10-01    | 2026-10-02   |      238.11   |              2 |          20 | -3.49%  |
| jev_pick                  | [ECL](https://www.tradingview.com/chart/?symbol=ECL)   | 2026-10-01    | 2026-10-02   |      273.31   |              2 |          20 | +1.38%  |
| jev_pick                  | [AMT](https://www.tradingview.com/chart/?symbol=AMT)   | 2026-10-01    | 2026-10-02   |      162.22   |              2 |          20 | +0.02%  |
| jev_pick                  | [KDP](https://www.tradingview.com/chart/?symbol=KDP)   | 2026-10-01    | 2026-10-02   |       30.98   |              2 |          20 | -0.29%  |
| jev_pick                  | [DECK](https://www.tradingview.com/chart/?symbol=DECK) | 2026-10-01    | 2026-10-02   |       79.5    |              2 |          20 | +0.89%  |
| jev_pick                  | [ERIE](https://www.tradingview.com/chart/?symbol=ERIE) | 2026-10-01    | 2026-10-02   |      222.597  |              2 |          20 | -0.51%  |
| jev_pick                  | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS) | 2026-10-01    | 2026-10-02   |      121.94   |              2 |          20 | -2.04%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)   | 2026-10-01    | 2026-10-02   |      119.24   |              2 |          20 | -1.92%  |
| jev_pick                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)   | 2026-10-01    | 2026-10-02   |      101.99   |              2 |          20 | +0.42%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL) | 2026-10-01    | 2026-10-02   |      142.09   |              2 |          20 | +0.27%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-10-02    | 2026-10-05   |       33.82   |              1 |          60 | +0.41%  |
| jev_pick                  | [DVN](https://www.tradingview.com/chart/?symbol=DVN)   | 2026-10-02    | 2026-10-05   |       47.64   |              1 |          20 | +0.71%  |
| jev_pick                  | [VRSK](https://www.tradingview.com/chart/?symbol=VRSK) | 2026-10-02    | 2026-10-05   |      163.81   |              1 |          20 | -0.32%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW) | 2026-10-05    | nan          |      nan      |            nan |          60 |         |
| falling_wedge_beaten_down | [SO](https://www.tradingview.com/chart/?symbol=SO)     | 2026-10-05    | nan          |      nan      |            nan |          20 |         |
| falling_wedge_beaten_down | [PDD](https://www.tradingview.com/chart/?symbol=PDD)   | 2026-10-05    | nan          |      nan      |            nan |          20 |         |
| jev_pick                  | [ORLY](https://www.tradingview.com/chart/?symbol=ORLY) | 2026-10-05    | nan          |      nan      |            nan |          20 |         |
| early_rally_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)   | 2026-10-05    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO) | 2026-10-05    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX) | 2026-10-05    |              |               |            nan |          20 |         |