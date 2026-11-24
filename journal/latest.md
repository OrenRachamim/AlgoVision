# Forward-test journal - 2026-11-24

Data through 2026-11-24; 518 of 518 symbols loaded.

## New signals today (4)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                                 |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:---------------------------------------------------------------------|
| insider_buy_beaten_down | [BG](https://www.tradingview.com/chart/?symbol=BG)     | 2026-11-23    |       84.06 |         120 | 2 buy(s) $1.16M @ 92.93, 6m -30%, vs MA200 -26%; Mahoney Christopher |
| insider_buy_beaten_down | [WMB](https://www.tradingview.com/chart/?symbol=WMB)   | 2026-11-23    |       66    |         120 | 1 buy(s) $0.65M @ 64.65, 6m -10%, vs MA200 -8%; Turner Robb E        |
| early_rally_beaten_down | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY) | 2026-11-24    |      164.61 |          20 | thrust; day +5.5%, 10d +8.6%, 6m -44%, vs MA200 -39%                 |
| early_rally_beaten_down | [F](https://www.tradingview.com/chart/?symbol=F)       | 2026-11-24    |       11.95 |          20 | rsi_turn; day +2.6%, 10d -2.7%, 6m -23%, vs MA200 -7%                |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      139 |      103 | +3.37% | 69%   | +7.04%   | +0.22%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       39 |       34 | +1.36% | 59%   | +3.59%   | -2.25%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       23 |        0 | -0.77% | 48%   | +3.01%   | +2.19%             |
| jev_pick                  | untested (forward test only)                     |       78 |       33 | -1.98% | 45%   | +1.28%   | -1.60%             |
| jev_skip                  | untested; a fall is the success case             |       16 |        6 | +1.55% | 44%   | +6.69%   | +4.57%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       54 |        0 | -4.38% | 46%   | +0.58%   | -4.10%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 139, closed: 103, open: 36
- closed trades: mean +6.05%, median +6.76%, hit 81%, best +34.5%, worst -25.6%
- open trades mark-to-market: mean -4.77%, hit 35%
- SPY over the same holding periods: mean -3.67% (excess +7.04%)
- beaten-down basket over the same holding periods: mean +3.15% (excess +0.22%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 39, closed: 34, open: 5
- closed trades: mean +2.58%, median +3.91%, hit 65%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean -6.97%, hit 20%
- SPY over the same holding periods: mean -2.23% (excess +3.59%)
- beaten-down basket over the same holding periods: mean +3.60% (excess -2.25%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 23, closed: 0, open: 23
- open trades mark-to-market: mean -0.77%, hit 48%
- SPY over the same holding periods: mean -3.78% (excess +3.01%)
- beaten-down basket over the same holding periods: mean -2.96% (excess +2.19%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 78, closed: 33, open: 45
- closed trades: mean +2.47%, median +1.06%, hit 55%, best +26.9%, worst -13.9%
- open trades mark-to-market: mean -5.25%, hit 38%
- SPY over the same holding periods: mean -3.26% (excess +1.28%)
- beaten-down basket over the same holding periods: mean -0.39% (excess -1.60%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 16, closed: 6, open: 10
- closed trades: mean +6.82%, median +5.51%, hit 67%, best +28.5%, worst -8.4%
- open trades mark-to-market: mean -1.61%, hit 30%
- SPY over the same holding periods: mean -5.14% (excess +6.69%)
- beaten-down basket over the same holding periods: mean -3.02% (excess +4.57%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 54, closed: 0, open: 54
- open trades mark-to-market: mean -4.38%, hit 46%
- SPY over the same holding periods: mean -4.96% (excess +0.58%)
- beaten-down basket over the same holding periods: mean -0.28% (excess -4.10%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             56 |          60 | +5.44%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             56 |          60 | -23.59% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             55 |          60 | -9.33%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             54 |          60 | +8.81%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             55 |         120 | +21.22% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             53 |          60 | +12.18% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             50 |          60 | -27.65% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             50 |         120 | +12.78% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             53 |         120 | -11.36% |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             47 |          60 | -18.03% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             43 |          60 | +0.97%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             40 |          60 | +16.83% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             38 |          60 | -34.11% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             38 |          60 | +14.55% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             37 |          60 | +5.71%  |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             36 |          60 | -0.21%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             32 |          60 | +11.83% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             32 |          60 | +2.79%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             29 |          60 | -30.64% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             28 |          60 | -34.65% |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             27 |         120 | +9.02%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1174      |             22 |          60 | -6.60%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             21 |          60 | -14.85% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       91      |             20 |          60 | +4.59%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |             20 |          60 | -5.08%  |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |             19 |          60 | +5.20%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |             19 |          60 | +5.57%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |             19 |          60 | -26.95% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |             19 |          60 | +17.88% |
| falling_wedge_beaten_down | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-10-28    | 2026-10-29   |       94.96   |             19 |          20 | -15.09% |
| early_rally_beaten_down   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |             19 |          20 | -26.95% |
| early_rally_beaten_down   | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-28    | 2026-10-29   |      342      |             19 |          20 | -11.96% |
| early_rally_beaten_down   | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-28    | 2026-10-29   |      144.14   |             19 |          20 | -24.03% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |             18 |          60 | -4.68%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |             18 |          60 | -0.74%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |             18 |          60 | -1.11%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |             18 |          60 | -7.63%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |             18 |          20 | -2.90%  |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      259.604  |             18 |          20 | -5.69%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |             18 |          20 | -2.90%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |             17 |          60 | -2.03%  |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |             17 |          60 | -16.21% |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       92.11   |             18 |         120 | +3.33%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |             17 |          20 | -1.75%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.73   |             17 |          20 | -26.26% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |             17 |          20 | +6.98%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |             17 |          20 | +4.41%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      263.777  |             17 |          20 | -7.18%  |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |             17 |          20 | +3.77%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |             17 |          20 | -23.47% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       93      |             17 |          20 | +2.34%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |             17 |          20 | -0.77%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |             17 |          20 | -8.33%  |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |             16 |          20 | +19.19% |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |             16 |          20 | +3.83%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.3719 |             16 |          20 | +8.71%  |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      159.6    |             16 |          20 | +4.82%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      378.388  |             16 |          20 | -15.62% |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |             16 |          20 | -8.67%  |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |             16 |          20 | +7.52%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |             16 |          20 | +1.40%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             15 |          20 | +6.42%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             15 |          20 | -15.74% |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             15 |          20 | -13.23% |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |             15 |          20 | -10.08% |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             15 |          20 | -15.74% |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             15 |          20 | -13.23% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |             15 |          20 | +4.80%  |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |             15 |          20 | -11.28% |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |             14 |          60 | +10.96% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |             14 |          60 | -9.26%  |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |             14 |          60 | +3.30%  |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |             14 |          60 | +1.88%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             14 |          60 | -27.04% |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |             15 |         120 | -7.58%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             15 |         120 | +6.42%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |             15 |         120 | -11.29% |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             14 |          20 | -27.04% |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |             14 |          20 | +8.94%  |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |             14 |          20 | -8.58%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |             14 |          20 | -7.49%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |             14 |          20 | -5.97%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |             14 |          20 | -5.86%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |             14 |          20 | -0.11%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          60 | -30.58% |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             13 |          60 | +9.29%  |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |             13 |          60 | +7.07%  |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |             13 |          60 | +2.28%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |             13 |          60 | -5.98%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |             13 |          60 | +0.01%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      385.935  |             13 |          60 | -1.06%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             13 |          60 | -16.50% |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |             14 |         120 | -3.03%  |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          20 | -30.58% |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             13 |          20 | +9.29%  |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             13 |          20 | -16.50% |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |             13 |          20 | -24.51% |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |             13 |          20 | +2.16%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      319.28   |             12 |          60 | +0.01%  |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.2594 |             13 |         120 | -0.80%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.4744 |             13 |         120 | +1.28%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |             12 |          20 | -17.27% |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             12 |          20 | +0.30%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      162.81   |             12 |          20 | +2.76%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48.1006 |             12 |          20 | -4.60%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       96.896  |             12 |          20 | -3.34%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             12 |          20 | +0.30%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.99   |             12 |          20 | +7.69%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |             12 |          20 | +6.65%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.71   |             12 |          20 | -1.70%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    | 2026-11-10   |       14.52   |             11 |          60 | -3.10%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    | 2026-11-10   |      173.97   |             11 |          60 | -10.69% |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    | 2026-11-10   |       54.99   |             11 |          20 | -16.38% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    | 2026-11-10   |       94.89   |             11 |          20 | -4.20%  |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    | 2026-11-10   |       84.538  |             11 |          20 | -2.94%  |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    | 2026-11-10   |      129.79   |             11 |          20 | -1.90%  |
| jev_skip                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-09    | 2026-11-10   |       28.44   |             11 |          20 | -4.61%  |
| insider_buy_beaten_down   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-09    | 2026-11-10   |      390.578  |             11 |         120 | -2.24%  |
| insider_buy_beaten_down   | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-09    | 2026-11-10   |       69.218  |             11 |         120 | -6.24%  |
| jev_pick                  | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-10    | 2026-11-11   |       69.1584 |             10 |          20 | -6.16%  |
| falling_wedge_beaten_down | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-11    | 2026-11-12   |      659.81   |              9 |          20 | -4.22%  |
| early_rally_beaten_down   | [ON](https://www.tradingview.com/chart/?symbol=ON)       | 2026-11-11    | 2026-11-12   |       71.43   |              9 |          20 | -13.92% |
| early_rally_beaten_down   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-11    | 2026-11-12   |      598.63   |              9 |          20 | -1.50%  |
| jev_pick                  | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-11-11    | 2026-11-12   |       36.8386 |              9 |          20 | +7.09%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-12    | 2026-11-13   |      169.91   |              8 |          60 | -8.55%  |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-12    | 2026-11-13   |        9.11   |              8 |          60 | -10.43% |
| falling_wedge_beaten_down | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-12    | 2026-11-13   |      356.54   |              8 |          20 | -15.56% |
| jev_pick                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-12    | 2026-11-13   |       15.63   |              8 |          20 | -9.98%  |
| insider_buy_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-12    | 2026-11-13   |      229.75   |              8 |         120 | -14.59% |
| insider_buy_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-12    | 2026-11-13   |      159.17   |              8 |         120 | +3.42%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-11-13    | 2026-11-16   |       13.37   |              7 |          20 | +6.36%  |
| jev_pick                  | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-13    | 2026-11-16   |      201.36   |              7 |          20 | -2.54%  |
| insider_buy_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-13    | 2026-11-16   |       85.14   |              7 |         120 | +4.91%  |
| early_rally_beaten_down   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              6 |          20 | +2.19%  |
| jev_pick                  | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              6 |          20 | +2.19%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-11-17    | 2026-11-18   |       35.54   |              5 |          60 | +0.59%  |
| falling_wedge_beaten_down | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-17    | 2026-11-18   |       85.44   |              5 |          20 | +4.54%  |
| insider_buy_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-11-13    | 2026-11-16   |       21.02   |              7 |         120 | -3.85%  |
| insider_buy_beaten_down   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-16    | 2026-11-17   |        9.25   |              6 |         120 | -11.78% |
| early_rally_beaten_down   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              5 |          20 | +2.51%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-17    | 2026-11-18   |      348.71   |              5 |          20 | -13.66% |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              5 |          20 | +2.51%  |
| newsday                   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-18    | 2026-11-19   |      214.73   |              4 |          60 | +2.65%  |
| insider_buy_beaten_down   | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-17    | 2026-11-18   |      337.63   |              5 |         120 | -5.44%  |
| early_rally_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-18    | 2026-11-19   |      230.5    |              4 |          20 | -14.86% |
| early_rally_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-18    | 2026-11-19   |       93.34   |              4 |          20 | -4.31%  |
| early_rally_beaten_down   | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              4 |          20 | -6.01%  |
| jev_pick                  | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              4 |          20 | -6.01%  |
| newsday                   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-19    | 2026-11-20   |       87.09   |              3 |          60 | +0.15%  |
| early_rally_beaten_down   | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-19    | 2026-11-20   |      287.01   |              3 |          20 | -4.55%  |
| early_rally_beaten_down   | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-19    | 2026-11-20   |      505.18   |              3 |          20 | -4.49%  |
| jev_pick                  | [SNPS](https://www.tradingview.com/chart/?symbol=SNPS)   | 2026-11-19    | 2026-11-20   |      425      |              3 |          20 | -2.40%  |
| newsday                   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-11-20    | 2026-11-23   |      274.02   |              2 |          60 | +1.97%  |
| insider_buy_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-19    | 2026-11-20   |      123.65   |              3 |         120 | +2.97%  |
| early_rally_beaten_down   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-11-20    | 2026-11-23   |       22.06   |              2 |          20 | +3.72%  |
| jev_pick                  | [KMI](https://www.tradingview.com/chart/?symbol=KMI)     | 2026-11-20    | 2026-11-23   |       30.71   |              2 |          20 | +1.20%  |
| jev_pick                  | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-20    | 2026-11-23   |      387.33   |              2 |          20 | -1.42%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-20    | 2026-11-23   |      125      |              2 |          20 | +1.86%  |
| jev_pick                  | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-20    | 2026-11-23   |      303.58   |              2 |          20 | -9.76%  |
| jev_pick                  | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-20    | 2026-11-23   |      553      |              2 |          20 | -12.75% |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-11-20    | 2026-11-23   |      246.81   |              2 |          20 | -8.15%  |
| jev_pick                  | [TT](https://www.tradingview.com/chart/?symbol=TT)       | 2026-11-20    | 2026-11-23   |      408.02   |              2 |          20 | -0.87%  |
| jev_pick                  | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-20    | 2026-11-23   |      183.02   |              2 |          20 | -11.73% |
| newsday                   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-11-23    | 2026-11-24   |      256.5    |              1 |          60 | -1.99%  |
| falling_wedge_beaten_down | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-23    | 2026-11-24   |      169.2    |              1 |          20 | -4.52%  |
| insider_buy_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-20    | 2026-11-23   |      140.78   |              2 |         120 | +2.19%  |
| early_rally_beaten_down   | [APO](https://www.tradingview.com/chart/?symbol=APO)     | 2026-11-23    | 2026-11-24   |      116.18   |              1 |          20 | +3.15%  |
| jev_pick                  | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-23    | 2026-11-24   |      139.38   |              1 |          20 | +3.21%  |
| jev_pick                  | [STLD](https://www.tradingview.com/chart/?symbol=STLD)   | 2026-11-23    | 2026-11-24   |      211.71   |              1 |          20 | +1.66%  |
| insider_buy_beaten_down   | [BG](https://www.tradingview.com/chart/?symbol=BG)       | 2026-11-23    | 2026-11-24   |       91.8    |              1 |         120 | -8.43%  |
| insider_buy_beaten_down   | [WMB](https://www.tradingview.com/chart/?symbol=WMB)     | 2026-11-23    | 2026-11-24   |       65.05   |              1 |         120 | +1.46%  |
| early_rally_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-24    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [F](https://www.tradingview.com/chart/?symbol=F)         | 2026-11-24    |              |               |            nan |          20 |         |