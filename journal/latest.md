# Forward-test journal - 2026-11-27

Data through 2026-11-27; 518 of 518 symbols loaded.

## New signals today (4)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                    |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:--------------------------------------------------------|
| early_rally_beaten_down | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL) | 2026-11-27    |      176.01 |          20 | rsi_turn; day +0.8%, 10d +2.5%, 6m -22%, vs MA200 -12%  |
| early_rally_beaten_down | [AXON](https://www.tradingview.com/chart/?symbol=AXON) | 2026-11-27    |      363.48 |          20 | rsi_turn; day +6.0%, 10d +18.4%, 6m -19%, vs MA200 -21% |
| early_rally_beaten_down | [NKE](https://www.tradingview.com/chart/?symbol=NKE)   | 2026-11-27    |       37.32 |          20 | rsi_turn; day +1.8%, 10d -1.2%, 6m -18%, vs MA200 -13%  |
| early_rally_beaten_down | [ARE](https://www.tradingview.com/chart/?symbol=ARE)   | 2026-11-27    |       43.37 |          20 | rsi_turn; day +0.6%, 10d -2.1%, 6m -10%, vs MA200 -8%   |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      147 |      108 | +4.14% | 72%   | +7.32%   | +0.30%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       40 |       35 | +1.61% | 60%   | +3.66%   | -2.27%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       23 |        0 | +1.98% | 61%   | +4.48%   | +1.88%             |
| jev_pick                  | untested (forward test only)                     |       81 |       34 | -0.18% | 52%   | +2.24%   | -1.58%             |
| jev_skip                  | untested; a fall is the success case             |       16 |        6 | +3.12% | 62%   | +7.47%   | +4.18%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       54 |        0 | -1.55% | 50%   | +2.15%   | -4.20%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 147, closed: 108, open: 39
- closed trades: mean +5.11%, median +6.19%, hit 78%, best +34.5%, worst -27.9%
- open trades mark-to-market: mean +1.15%, hit 54%
- SPY over the same holding periods: mean -3.18% (excess +7.32%)
- beaten-down basket over the same holding periods: mean +3.83% (excess +0.30%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 40, closed: 35, open: 5
- closed trades: mean +2.10%, median +3.72%, hit 63%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean -1.84%, hit 40%
- SPY over the same holding periods: mean -2.05% (excess +3.66%)
- beaten-down basket over the same holding periods: mean +3.88% (excess -2.27%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 23, closed: 0, open: 23
- open trades mark-to-market: mean +1.98%, hit 61%
- SPY over the same holding periods: mean -2.50% (excess +4.48%)
- beaten-down basket over the same holding periods: mean +0.10% (excess +1.88%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 81, closed: 34, open: 47
- closed trades: mean +2.49%, median +1.43%, hit 56%, best +26.9%, worst -13.9%
- open trades mark-to-market: mean -2.11%, hit 49%
- SPY over the same holding periods: mean -2.42% (excess +2.24%)
- beaten-down basket over the same holding periods: mean +1.40% (excess -1.58%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 16, closed: 6, open: 10
- closed trades: mean +6.82%, median +5.51%, hit 67%, best +28.5%, worst -8.4%
- open trades mark-to-market: mean +0.90%, hit 60%
- SPY over the same holding periods: mean -4.35% (excess +7.47%)
- beaten-down basket over the same holding periods: mean -1.06% (excess +4.18%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 54, closed: 0, open: 54
- open trades mark-to-market: mean -1.55%, hit 50%
- SPY over the same holding periods: mean -3.70% (excess +2.15%)
- beaten-down basket over the same holding periods: mean +2.65% (excess -4.20%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             58 |          60 | +7.39%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             58 |          60 | -23.02% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             57 |          60 | -6.51%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             56 |          60 | +13.24% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             57 |         120 | +20.80% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             55 |          60 | +13.94% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             52 |          60 | -17.64% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             52 |         120 | +14.55% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             55 |         120 | -8.71%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             49 |          60 | -15.16% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             45 |          60 | +3.82%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             42 |          60 | +17.70% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             40 |          60 | -33.31% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             40 |          60 | +15.40% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             39 |          60 | +10.35% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             38 |          60 | +4.37%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      148.554  |             34 |          60 | +14.56% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             34 |          60 | +4.27%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             31 |          60 | -28.13% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             30 |          60 | -32.28% |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             29 |         120 | +10.48% |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1174      |             24 |          60 | -3.86%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             23 |          60 | -10.00% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       90.5956 |             22 |          60 | +5.81%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |             22 |          60 | -2.40%  |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |             21 |          60 | +7.70%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |             21 |          60 | +8.23%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.832  |             21 |          60 | -24.86% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |             21 |          60 | +26.11% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |             20 |          60 | -5.79%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |             20 |          60 | -2.19%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |             20 |          60 | -2.59%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |             20 |          60 | -3.95%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |             19 |          60 | +1.76%  |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |             19 |          60 | -12.23% |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       91.7006 |             20 |         120 | +4.54%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |             19 |          20 | +1.26%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.603  |             19 |          20 | -24.15% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |             19 |          20 | +9.79%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |             19 |          20 | +6.51%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      263.777  |             19 |          20 | -9.73%  |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |             19 |          20 | +4.25%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |             19 |          20 | -19.78% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       92.5867 |             19 |          20 | +3.54%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |             19 |          20 | +1.58%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |             19 |          20 | -4.31%  |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |             18 |          20 | +34.99% |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |             18 |          20 | +7.86%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.3719 |             18 |          20 | +15.53% |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      158.484  |             18 |          20 | +7.39%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      378.388  |             18 |          20 | -13.87% |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |             18 |          20 | -2.93%  |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |             18 |          20 | +8.60%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |             18 |          20 | +3.63%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             17 |          20 | +9.43%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             17 |          20 | -14.02% |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             17 |          20 | -10.02% |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |             17 |          20 | -12.03% |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |             17 |          20 | -14.02% |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |             17 |          20 | -10.02% |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |             17 |          20 | +4.07%  |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |             17 |          20 | -7.75%  |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |             16 |          60 | +14.54% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |             16 |          60 | -5.65%  |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |             16 |          60 | +4.95%  |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |             16 |          60 | +4.07%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             16 |          60 | -26.17% |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |             17 |         120 | -5.51%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |             17 |         120 | +9.43%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |             17 |         120 | -7.83%  |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |             16 |          20 | -26.17% |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |             16 |          20 | +14.12% |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |             16 |          20 | -5.85%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |             16 |          20 | -3.02%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |             16 |          20 | -5.56%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |             16 |          20 | -1.25%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |             16 |          20 | +0.58%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          60 | -23.98% |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             15 |          60 | +7.62%  |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |             15 |          60 | +12.15% |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |             15 |          60 | +11.15% |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |             15 |          60 | -0.62%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |             15 |          60 | -1.58%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      385.935  |             15 |          60 | +2.15%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             15 |          60 | -7.69%  |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |             16 |         120 | +1.57%  |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      112.284  |             11 |          20 | -23.98% |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |             15 |          20 | +7.62%  |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |             15 |          20 | -7.69%  |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |             15 |          20 | -23.61% |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |             15 |          20 | +2.64%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      319.28   |             14 |          60 | +13.84% |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.2594 |             15 |         120 | +2.62%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.4744 |             15 |         120 | +6.09%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |             14 |          20 | -14.91% |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             14 |          20 | +3.43%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      161.671  |             14 |          20 | +5.27%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48.1006 |             14 |          20 | -1.31%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       96.896  |             14 |          20 | +1.25%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |             14 |          20 | +3.43%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.99   |             14 |          20 | +9.19%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |             14 |          20 | +7.19%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.71   |             14 |          20 | +2.97%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    | 2026-11-10   |       14.52   |             13 |          60 | -0.55%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    | 2026-11-10   |      173.97   |             13 |          60 | -13.50% |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    | 2026-11-10   |       54.99   |             13 |          20 | -7.47%  |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    | 2026-11-10   |       94.89   |             13 |          20 | -1.12%  |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    | 2026-11-10   |       84.538  |             13 |          20 | +3.44%  |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    | 2026-11-10   |      129.79   |             13 |          20 | -2.19%  |
| jev_skip                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-09    | 2026-11-10   |       28.44   |             13 |          20 | -0.81%  |
| insider_buy_beaten_down   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-09    | 2026-11-10   |      390.578  |             13 |         120 | +0.94%  |
| insider_buy_beaten_down   | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-09    | 2026-11-10   |       69.218  |             13 |         120 | -2.02%  |
| jev_pick                  | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-10    | 2026-11-11   |       69.1584 |             12 |          20 | -1.94%  |
| falling_wedge_beaten_down | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-11    | 2026-11-12   |      659.81   |             11 |          20 | -3.76%  |
| early_rally_beaten_down   | [ON](https://www.tradingview.com/chart/?symbol=ON)       | 2026-11-11    | 2026-11-12   |       71.43   |             11 |          20 | -7.27%  |
| early_rally_beaten_down   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-11    | 2026-11-12   |      598.63   |             11 |          20 | -3.01%  |
| jev_pick                  | [TSCO](https://www.tradingview.com/chart/?symbol=TSCO)   | 2026-11-11    | 2026-11-12   |       36.8386 |             11 |          20 | +8.61%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-12    | 2026-11-13   |      169.91   |             10 |          60 | -11.43% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-12    | 2026-11-13   |        9.11   |             10 |          60 | -9.33%  |
| falling_wedge_beaten_down | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-12    | 2026-11-13   |      356.54   |             10 |          20 | -12.40% |
| jev_pick                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-12    | 2026-11-13   |       15.63   |             10 |          20 | -7.61%  |
| insider_buy_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-12    | 2026-11-13   |      229.75   |             10 |         120 | -2.59%  |
| insider_buy_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-12    | 2026-11-13   |      159.17   |             10 |         120 | +2.22%  |
| early_rally_beaten_down   | [PCG](https://www.tradingview.com/chart/?symbol=PCG)     | 2026-11-13    | 2026-11-16   |       13.37   |              9 |          20 | +7.93%  |
| jev_pick                  | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-13    | 2026-11-16   |      201.36   |              9 |          20 | +11.14% |
| insider_buy_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-13    | 2026-11-16   |       85.14   |              9 |         120 | +6.44%  |
| early_rally_beaten_down   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              8 |          20 | +6.74%  |
| jev_pick                  | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-16    | 2026-11-17   |      215.69   |              8 |          20 | +6.74%  |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-11-17    | 2026-11-18   |       35.54   |              7 |          60 | +5.01%  |
| falling_wedge_beaten_down | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-17    | 2026-11-18   |       85.44   |              7 |          20 | +6.06%  |
| insider_buy_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-11-13    | 2026-11-16   |       21.02   |              9 |         120 | -0.90%  |
| insider_buy_beaten_down   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-11-16    | 2026-11-17   |        9.25   |              8 |         120 | -10.70% |
| early_rally_beaten_down   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              7 |          20 | +7.21%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-11-17    | 2026-11-18   |      348.71   |              7 |          20 | -10.43% |
| jev_pick                  | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-11-17    | 2026-11-18   |      137.09   |              7 |          20 | +7.21%  |
| newsday                   | [TTWO](https://www.tradingview.com/chart/?symbol=TTWO)   | 2026-11-18    | 2026-11-19   |      214.73   |              6 |          60 | +7.21%  |
| insider_buy_beaten_down   | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-17    | 2026-11-18   |      337.63   |              7 |         120 | -3.47%  |
| early_rally_beaten_down   | [COHR](https://www.tradingview.com/chart/?symbol=COHR)   | 2026-11-18    | 2026-11-19   |      230.5    |              6 |          20 | -2.91%  |
| early_rally_beaten_down   | [AKAM](https://www.tradingview.com/chart/?symbol=AKAM)   | 2026-11-18    | 2026-11-19   |       93.34   |              6 |          20 | -2.91%  |
| early_rally_beaten_down   | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              6 |          20 | +3.85%  |
| jev_pick                  | [GNRC](https://www.tradingview.com/chart/?symbol=GNRC)   | 2026-11-18    | 2026-11-19   |      211.04   |              6 |          20 | +3.85%  |
| newsday                   | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-19    | 2026-11-20   |       87.09   |              5 |          60 | +1.54%  |
| early_rally_beaten_down   | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-19    | 2026-11-20   |      287.01   |              5 |          20 | +1.78%  |
| early_rally_beaten_down   | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-19    | 2026-11-20   |      505.18   |              5 |          20 | +0.89%  |
| jev_pick                  | [SNPS](https://www.tradingview.com/chart/?symbol=SNPS)   | 2026-11-19    | 2026-11-20   |      425      |              5 |          20 | -1.16%  |
| newsday                   | [INTU](https://www.tradingview.com/chart/?symbol=INTU)   | 2026-11-20    | 2026-11-23   |      274.02   |              4 |          60 | -0.76%  |
| insider_buy_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-19    | 2026-11-20   |      123.65   |              5 |         120 | +2.67%  |
| early_rally_beaten_down   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-11-20    | 2026-11-23   |       22.06   |              4 |          20 | +5.21%  |
| jev_pick                  | [KMI](https://www.tradingview.com/chart/?symbol=KMI)     | 2026-11-20    | 2026-11-23   |       30.71   |              4 |          20 | +4.43%  |
| jev_pick                  | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-20    | 2026-11-23   |      387.33   |              4 |          20 | +1.79%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-20    | 2026-11-23   |      125      |              4 |          20 | +1.56%  |
| jev_pick                  | [WDC](https://www.tradingview.com/chart/?symbol=WDC)     | 2026-11-20    | 2026-11-23   |      303.58   |              4 |          20 | -3.78%  |
| jev_pick                  | [STX](https://www.tradingview.com/chart/?symbol=STX)     | 2026-11-20    | 2026-11-23   |      553      |              4 |          20 | -7.84%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-11-20    | 2026-11-23   |      246.81   |              4 |          20 | -4.42%  |
| jev_pick                  | [TT](https://www.tradingview.com/chart/?symbol=TT)       | 2026-11-20    | 2026-11-23   |      408.02   |              4 |          20 | -0.46%  |
| jev_pick                  | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-20    | 2026-11-23   |      183.02   |              4 |          20 | -6.27%  |
| newsday                   | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-11-23    | 2026-11-24   |      256.5    |              3 |          60 | +2.73%  |
| falling_wedge_beaten_down | [ARM](https://www.tradingview.com/chart/?symbol=ARM)     | 2026-11-23    | 2026-11-24   |      169.09   |              3 |          20 | +1.45%  |
| insider_buy_beaten_down   | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-20    | 2026-11-23   |      140.78   |              4 |         120 | +2.12%  |
| early_rally_beaten_down   | [APO](https://www.tradingview.com/chart/?symbol=APO)     | 2026-11-23    | 2026-11-24   |      116.18   |              3 |          20 | +5.84%  |
| jev_pick                  | [TJX](https://www.tradingview.com/chart/?symbol=TJX)     | 2026-11-23    | 2026-11-24   |      139.38   |              3 |          20 | +3.15%  |
| jev_pick                  | [STLD](https://www.tradingview.com/chart/?symbol=STLD)   | 2026-11-23    | 2026-11-24   |      211.71   |              3 |          20 | +4.87%  |
| insider_buy_beaten_down   | [BG](https://www.tradingview.com/chart/?symbol=BG)       | 2026-11-23    | 2026-11-24   |       91.8    |              3 |         120 | -0.44%  |
| insider_buy_beaten_down   | [WMB](https://www.tradingview.com/chart/?symbol=WMB)     | 2026-11-23    | 2026-11-24   |       65.05   |              3 |         120 | +3.20%  |
| early_rally_beaten_down   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-11-24    | 2026-11-25   |      164.43   |              2 |          20 | -1.05%  |
| early_rally_beaten_down   | [F](https://www.tradingview.com/chart/?symbol=F)         | 2026-11-24    | 2026-11-25   |       11.91   |              2 |          20 | +3.53%  |
| falling_wedge_beaten_down | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-11-25    | 2026-11-27   |      177.035  |              1 |          20 | -0.58%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-11-25    | 2026-11-27   |      352      |              1 |          20 | -0.56%  |
| early_rally_beaten_down   | [JBHT](https://www.tradingview.com/chart/?symbol=JBHT)   | 2026-11-25    | 2026-11-27   |      231.59   |              1 |          20 | -0.01%  |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-11-25    | 2026-11-27   |       54.57   |              1 |          20 | -0.04%  |
| early_rally_beaten_down   | [MOS](https://www.tradingview.com/chart/?symbol=MOS)     | 2026-11-25    | 2026-11-27   |       20.75   |              1 |          20 | +1.40%  |
| jev_pick                  | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-11-25    | 2026-11-27   |       20.6    |              1 |          20 | +1.12%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-11-25    | 2026-11-27   |      177.035  |              1 |          20 | -0.58%  |
| jev_pick                  | [KLAC](https://www.tradingview.com/chart/?symbol=KLAC)   | 2026-11-25    | 2026-11-27   |      138.93   |              1 |          20 | +1.39%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-11-27    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-27    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-11-27    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [ARE](https://www.tradingview.com/chart/?symbol=ARE)     | 2026-11-27    |              |               |            nan |          20 |         |