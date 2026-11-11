# Forward-test journal - 2026-11-11

Data through 2026-11-11; 518 of 518 symbols loaded.

## New signals today (3)

| rule                      | symbol                                               | signal_date   |   ref_price |   hold_bars | note                                                   |
|:--------------------------|:-----------------------------------------------------|:--------------|------------:|------------:|:-------------------------------------------------------|
| falling_wedge_beaten_down | [EME](https://www.tradingview.com/chart/?symbol=EME) | 2026-11-11    |      666.74 |          20 | score 0.62, stop 570.52, level 663.43                  |
| early_rally_beaten_down   | [ON](https://www.tradingview.com/chart/?symbol=ON)   | 2026-11-11    |       73.62 |          20 | rsi_turn; day +5.8%, 10d -2.7%, 6m -36%, vs MA200 -11% |
| early_rally_beaten_down   | [PWR](https://www.tradingview.com/chart/?symbol=PWR) | 2026-11-11    |      607.94 |          20 | rsi_turn; day +4.3%, 10d +0.2%, 6m -21%, vs MA200 -4%  |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      127 |       54 | +6.55% | 80%   | +8.64%   | +0.25%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       36 |       24 | +3.11% | 66%   | +4.67%   | -2.26%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       13 |        0 | +5.21% | 77%   | +4.72%   | +0.50%             |
| jev_pick                  | untested (forward test only)                     |       60 |       18 | +3.63% | 65%   | +3.73%   | -1.87%             |
| jev_skip                  | untested; a fall is the success case             |       16 |        0 | +5.68% | 69%   | +5.65%   | +1.49%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       47 |        0 | +2.90% | 57%   | +2.89%   | -3.44%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 127, closed: 54, open: 73
- closed trades: mean +7.46%, median +7.72%, hit 87%, best +26.9%, worst -25.6%
- open trades mark-to-market: mean +5.86%, hit 75%
- SPY over the same holding periods: mean -2.09% (excess +8.64%)
- beaten-down basket over the same holding periods: mean +6.29% (excess +0.25%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 36, closed: 24, open: 12
- closed trades: mean +1.75%, median +3.91%, hit 62%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean +6.07%, hit 73%
- SPY over the same holding periods: mean -1.56% (excess +4.67%)
- beaten-down basket over the same holding periods: mean +5.37% (excess -2.26%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 13, closed: 0, open: 13
- open trades mark-to-market: mean +5.21%, hit 77%
- SPY over the same holding periods: mean +0.49% (excess +4.72%)
- beaten-down basket over the same holding periods: mean +4.71% (excess +0.50%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 60, closed: 18, open: 42
- closed trades: mean +7.18%, median +9.08%, hit 67%, best +26.9%, worst -11.0%
- open trades mark-to-market: mean +2.11%, hit 64%
- SPY over the same holding periods: mean -0.10% (excess +3.73%)
- beaten-down basket over the same holding periods: mean +5.50% (excess -1.87%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 16, closed: 0, open: 16
- open trades mark-to-market: mean +5.68%, hit 69%
- SPY over the same holding periods: mean +0.04% (excess +5.65%)
- beaten-down basket over the same holding periods: mean +4.19% (excess +1.49%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 47, closed: 0, open: 47
- open trades mark-to-market: mean +2.90%, hit 57%
- SPY over the same holding periods: mean +0.02% (excess +2.89%)
- beaten-down basket over the same holding periods: mean +6.34% (excess -3.44%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             47 |          60 | +6.83%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             47 |          60 | -20.82% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             46 |          60 | -3.68%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             45 |          60 | +13.10% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             46 |         120 | +14.43% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             44 |          60 | +15.13% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             41 |          60 | -28.53% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             41 |         120 | +15.74% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             44 |         120 | -3.16%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             38 |          60 | -10.14% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             34 |          60 | -1.53%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             31 |          60 | +21.07% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             29 |          60 | -1.98%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             29 |          60 | +18.71% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             28 |          60 | +13.31% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             27 |          60 | -5.02%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             23 |          60 | +15.08% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             23 |          60 | +0.00%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             20 |          60 | -1.07%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             19 |          60 | -6.79%  |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             19 |          20 | -1.06%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |       27.96   |             19 |          20 | +15.06% |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |       83.4    |             19 |          20 | +15.42% |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |      529.98   |             19 |          20 | -12.59% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |      357.38   |             19 |          20 | -1.86%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |     3091      |             19 |          20 | +4.75%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |       13.29   |             19 |          20 | +20.24% |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |       36.42   |             19 |          20 | -17.05% |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |      120.66   |             19 |          20 | +10.51% |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |      295.89   |             19 |          20 | +7.74%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |       69.87   |             19 |          20 | -7.63%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |       44.45   |             19 |          20 | +1.53%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |       29.93   |             19 |          20 | +8.72%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |      125.05   |             19 |          20 | +7.07%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |      244.31   |             19 |          20 | +12.48% |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |      150.37   |             19 |          20 | +14.44% |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |      505.78   |             19 |          20 | +3.63%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |      195.819  |             19 |          20 | +18.27% |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |       37.67   |             19 |          20 | +1.73%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |       85.4496 |             19 |          20 | +25.06% |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |       79.6    |             19 |          20 | +8.03%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |      254.94   |             19 |          20 | +11.54% |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |      170.42   |             19 |          20 | +3.53%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             19 |          20 | -1.06%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |      169.41   |             18 |          20 | +4.14%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |       45.99   |             18 |          20 | +2.07%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |      511      |             18 |          20 | +7.82%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |       57.29   |             18 |          20 | +9.84%  |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |      288.293  |             18 |          20 | +16.74% |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |      268.28   |             18 |          20 | +17.03% |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |      245.16   |             18 |          20 | +12.82% |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |       47.42   |             18 |          20 | +34.75% |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |       23.48   |             18 |          20 | +6.22%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             18 |          20 | +9.98%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |      104.16   |             18 |          20 | -8.69%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |       55.5347 |             18 |          20 | +7.27%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |      306.55   |             18 |          20 | +14.60% |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |       33.45   |             18 |          20 | -1.55%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             18 |         120 | +9.98%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |      454.74   |             17 |          20 | -2.48%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |      110.684  |             16 |          20 | +10.23% |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |       55.27   |             16 |          20 | +8.32%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |             16 |          20 | +7.45%  |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |       86.03   |             16 |          20 | +11.89% |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |       21.94   |             16 |          20 | +14.04% |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |       78.84   |             16 |          20 | +9.50%  |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |      545      |             16 |          20 | -15.00% |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |       77.73   |             16 |          20 | +10.56% |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |       56.269  |             16 |          20 | -3.00%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |      189.29   |             16 |          20 | -9.93%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |      227.11   |             16 |          20 | +16.46% |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |      465.97   |             16 |          20 | -4.83%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |       62.31   |             16 |          20 | -9.36%  |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |      338.03   |             16 |          20 | +2.13%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |      281.5    |             16 |          20 | -8.03%  |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |             16 |          20 | +7.45%  |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |      363.84   |             15 |          20 | -3.60%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | 2026-10-22   |      264.153  |             15 |          20 | +7.65%  |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | 2026-10-22   |      509.34   |             15 |          20 | +2.90%  |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |      544.7    |             15 |          20 | +1.15%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |       77.57   |             15 |          20 | +11.29% |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |       84.3752 |             15 |          20 | +26.65% |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    | 2026-10-23   |       54.61   |             14 |          20 | +26.95% |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |             14 |          20 | +9.99%  |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    | 2026-10-23   |      818.29   |             14 |          20 | -10.93% |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    | 2026-10-23   |       28.89   |             14 |          20 | +11.35% |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |             14 |          20 | -1.74%  |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    | 2026-10-23   |      117.97   |             14 |          20 | +9.77%  |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |             14 |          20 | +8.57%  |
| jev_pick                  | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |             14 |          20 | +8.57%  |
| jev_pick                  | [ISRG](https://www.tradingview.com/chart/?symbol=ISRG)   | 2026-10-22    | 2026-10-23   |      443.65   |             14 |          20 | +1.33%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-10-22    | 2026-10-23   |      126.05   |             14 |          20 | +3.16%  |
| jev_skip                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-22    | 2026-10-23   |       13      |             14 |          20 | +22.92% |
| jev_skip                  | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |             14 |          20 | +9.99%  |
| jev_skip                  | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |             14 |          20 | -1.74%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |             13 |          60 | -1.14%  |
| jev_pick                  | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |             13 |          20 | -1.14%  |
| jev_pick                  | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-23    | 2026-10-26   |      698.589  |             13 |          20 | +2.22%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             12 |          60 | -11.23% |
| jev_pick                  | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-26    | 2026-10-27   |      280.98   |             12 |          20 | +11.74% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       91      |             11 |          60 | +4.52%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |             11 |          60 | -0.27%  |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-27    | 2026-10-28   |       58.64   |             11 |          20 | +25.97% |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-10-27    | 2026-10-28   |       56.5204 |             11 |          20 | -12.58% |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-27    | 2026-10-28   |       53.3582 |             11 |          20 | +14.87% |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |             10 |          60 | +7.91%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |             10 |          60 | +7.94%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |             10 |          60 | -13.22% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |             10 |          60 | +9.30%  |
| falling_wedge_beaten_down | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-10-28    | 2026-10-29   |       94.96   |             10 |          20 | +1.06%  |
| early_rally_beaten_down   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |             10 |          20 | -13.22% |
| early_rally_beaten_down   | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-28    | 2026-10-29   |      342      |             10 |          20 | +0.94%  |
| early_rally_beaten_down   | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-28    | 2026-10-29   |      144.14   |             10 |          20 | -10.93% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |              9 |          60 | -7.44%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |              9 |          60 | +4.39%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |              9 |          60 | +3.91%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |              9 |          60 | -0.96%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              9 |          20 | +8.74%  |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      260      |              9 |          20 | +5.67%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              9 |          20 | +8.74%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |              8 |          60 | +14.59% |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |              8 |          60 | -4.43%  |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       92.11   |              9 |         120 | +3.26%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |              8 |          20 | +0.39%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.73   |              8 |          20 | -12.40% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |              8 |          20 | +6.38%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |              8 |          20 | +8.35%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      264.18   |              8 |          20 | +3.99%  |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |              8 |          20 | +2.88%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |              8 |          20 | -14.33% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       93      |              8 |          20 | +2.27%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |              8 |          20 | +1.78%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |              8 |          20 | -1.74%  |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |              7 |          20 | +19.58% |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |              7 |          20 | +5.45%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.6    |              7 |          20 | +10.03% |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      159.6    |              7 |          20 | +7.87%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      378.388  |              7 |          20 | -4.70%  |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |              7 |          20 | +13.47% |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |              7 |          20 | +6.09%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |              7 |          20 | -0.66%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |              6 |          20 | +3.78%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |              6 |          20 | -5.50%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |              6 |          20 | +3.60%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |              6 |          20 | +5.42%  |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |              6 |          20 | -5.50%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |              6 |          20 | +3.60%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |              6 |          20 | +8.40%  |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |              6 |          20 | -1.21%  |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |              5 |          60 | +19.02% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |              5 |          60 | +1.04%  |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |              5 |          60 | +14.20% |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |              5 |          60 | +5.37%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |              5 |          60 | -12.20% |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |              6 |         120 | -1.39%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |              6 |         120 | +3.78%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |              6 |         120 | -1.29%  |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |              5 |          20 | -12.20% |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |              5 |          20 | +15.70% |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |              5 |          20 | -0.13%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |              5 |          20 | -1.41%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |              5 |          20 | -4.40%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |              5 |          20 | +2.62%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |              5 |          20 | -2.21%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      898.27   |              4 |          60 | +8.84%  |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |              4 |          60 | +12.69% |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |              4 |          60 | +13.72% |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |              4 |          60 | +9.48%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |              4 |          60 | -1.98%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |              4 |          60 | +6.04%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      387.33   |              4 |          60 | +4.87%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |              4 |          60 | +9.14%  |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |              5 |         120 | +10.60% |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      898.27   |              4 |          20 | +8.84%  |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |              4 |          20 | +12.69% |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |              4 |          20 | +9.14%  |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |              4 |          20 | -9.15%  |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |              4 |          20 | +7.78%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      319.28   |              3 |          60 | -1.21%  |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.2594 |              4 |         120 | +6.81%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.86   |              4 |         120 | +3.66%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |              3 |          20 | -1.53%  |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |              3 |          20 | +6.56%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      162.81   |              3 |          20 | +5.74%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48.1006 |              3 |          20 | +2.72%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       97.3    |              3 |          20 | -1.07%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |              3 |          20 | +6.56%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.99   |              3 |          20 | -2.44%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |              3 |          20 | -1.70%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.71   |              3 |          20 | +4.40%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    | 2026-11-10   |       14.52   |              2 |          60 | +10.06% |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    | 2026-11-10   |      173.97   |              2 |          60 | -0.14%  |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    | 2026-11-10   |       54.99   |              2 |          20 | +20.29% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    | 2026-11-10   |       94.89   |              2 |          20 | +2.75%  |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    | 2026-11-10   |       85.09   |              2 |          20 | +4.16%  |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    | 2026-11-10   |      129.79   |              2 |          20 | +0.18%  |
| jev_skip                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-09    | 2026-11-10   |       28.44   |              2 |          20 | +6.22%  |
| insider_buy_beaten_down   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-09    | 2026-11-10   |      391.99   |              2 |         120 | +3.62%  |
| insider_buy_beaten_down   | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-09    | 2026-11-10   |       69.74   |              2 |         120 | +1.69%  |
| jev_pick                  | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-10    | 2026-11-11   |       69.68   |              1 |          20 | +1.78%  |
| falling_wedge_beaten_down | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-11    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [ON](https://www.tradingview.com/chart/?symbol=ON)       | 2026-11-11    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-11    |              |               |            nan |          20 |         |