# Forward-test journal - 2026-11-10

Data through 2026-11-10; 518 of 518 symbols loaded.

## New signals today (2)

| rule                    | symbol                                               | signal_date   |   ref_price |   hold_bars | note                                                              |
|:------------------------|:-----------------------------------------------------|:--------------|------------:|------------:|:------------------------------------------------------------------|
| insider_buy_beaten_down | [ROK](https://www.tradingview.com/chart/?symbol=ROK) | 2026-11-09    |      397.16 |         120 | 3 buy(s) $1.55M @ 386.36, 6m -12%, vs MA200 -7%; Moret Blake D.   |
| insider_buy_beaten_down | [ADM](https://www.tradingview.com/chart/?symbol=ADM) | 2026-11-09    |       69.3  |         120 | 1 buy(s) $0.20M @ 70.27, 6m -13%, vs MA200 -9%; McAtee David R II |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      125 |       49 | +6.13% | 79%   | +9.00%   | +0.79%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       35 |       24 | +2.98% | 63%   | +4.95%   | -2.04%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       13 |        0 | +3.85% | 69%   | +4.66%   | +1.31%             |
| jev_pick                  | untested (forward test only)                     |       59 |       18 | +2.19% | 56%   | +3.20%   | -1.86%             |
| jev_skip                  | untested; a fall is the success case             |       16 |        0 | +5.42% | 75%   | +6.68%   | +3.51%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       47 |        0 | -0.04% | 51%   | +1.24%   | -4.63%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 125, closed: 49, open: 76
- closed trades: mean +7.35%, median +7.32%, hit 88%, best +26.9%, worst -25.6%
- open trades mark-to-market: mean +5.34%, hit 74%
- SPY over the same holding periods: mean -2.88% (excess +9.00%)
- beaten-down basket over the same holding periods: mean +5.34% (excess +0.79%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 35, closed: 24, open: 11
- closed trades: mean +1.75%, median +3.91%, hit 62%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean +5.67%, hit 64%
- SPY over the same holding periods: mean -1.97% (excess +4.95%)
- beaten-down basket over the same holding periods: mean +5.02% (excess -2.04%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 13, closed: 0, open: 13
- open trades mark-to-market: mean +3.85%, hit 69%
- SPY over the same holding periods: mean -0.82% (excess +4.66%)
- beaten-down basket over the same holding periods: mean +2.54% (excess +1.31%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 59, closed: 18, open: 41
- closed trades: mean +7.18%, median +9.08%, hit 67%, best +26.9%, worst -11.0%
- open trades mark-to-market: mean -0.01%, hit 51%
- SPY over the same holding periods: mean -1.02% (excess +3.20%)
- beaten-down basket over the same holding periods: mean +4.05% (excess -1.86%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 16, closed: 0, open: 16
- open trades mark-to-market: mean +5.42%, hit 75%
- SPY over the same holding periods: mean -1.27% (excess +6.68%)
- beaten-down basket over the same holding periods: mean +1.90% (excess +3.51%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 47, closed: 0, open: 47
- open trades mark-to-market: mean -0.04%, hit 51%
- SPY over the same holding periods: mean -1.29% (excess +1.24%)
- beaten-down basket over the same holding periods: mean +4.59% (excess -4.63%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             46 |          60 | +9.73%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             46 |          60 | -20.62% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             45 |          60 | -5.80%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             44 |          60 | +10.63% |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             45 |         120 | +15.23% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             43 |          60 | +16.30% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             40 |          60 | -31.45% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             40 |         120 | +16.92% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             43 |         120 | -4.03%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             37 |          60 | -11.92% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             33 |          60 | -2.74%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             30 |          60 | +21.37% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             28 |          60 | -1.74%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             28 |          60 | +19.00% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             27 |          60 | +14.34% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             26 |          60 | -8.41%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             22 |          60 | +13.02% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             22 |          60 | -1.44%  |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             19 |          60 | -20.67% |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |       33.27   |             19 |          20 | +15.48% |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |      342.5    |             19 |          20 | -20.55% |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |      153.24   |             19 |          20 | +22.83% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |       61.37   |             19 |          20 | -1.25%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |      531      |             19 |          20 | +13.58% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             18 |          60 | -25.26% |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             18 |          20 | -0.90%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |       27.96   |             18 |          20 | +15.52% |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |       83.4    |             18 |          20 | +16.14% |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |      529.98   |             18 |          20 | -14.30% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |      357.38   |             18 |          20 | -2.64%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |     3091      |             18 |          20 | +4.09%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |       13.29   |             18 |          20 | +16.03% |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |       36.42   |             18 |          20 | -22.27% |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |      120.66   |             18 |          20 | +12.40% |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |      295.89   |             18 |          20 | +9.60%  |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |       69.87   |             18 |          20 | -9.46%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |       44.45   |             18 |          20 | +0.56%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |       29.93   |             18 |          20 | +5.18%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |      125.05   |             18 |          20 | +9.75%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |      244.31   |             18 |          20 | +15.50% |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |      150.37   |             18 |          20 | +15.89% |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |      505.78   |             18 |          20 | +4.43%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |      195.819  |             18 |          20 | +18.41% |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |       37.67   |             18 |          20 | +2.65%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |       85.4496 |             18 |          20 | +24.75% |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |       79.6    |             18 |          20 | +8.38%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |      254.94   |             18 |          20 | +12.70% |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |      170.42   |             18 |          20 | +2.07%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             18 |          20 | -0.90%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |      169.41   |             17 |          20 | +2.68%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |       45.99   |             17 |          20 | +1.59%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |      511      |             17 |          20 | +7.36%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |       57.29   |             17 |          20 | +10.96% |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |      288.293  |             17 |          20 | +16.67% |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |      268.28   |             17 |          20 | +16.88% |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |      245.16   |             17 |          20 | +12.56% |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |       47.42   |             17 |          20 | +33.53% |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |       23.48   |             17 |          20 | +6.43%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             17 |          20 | +9.73%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |      104.16   |             17 |          20 | -7.03%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |       55.5347 |             17 |          20 | +7.21%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |      306.55   |             17 |          20 | +14.50% |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |       33.45   |             17 |          20 | -4.75%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             17 |         120 | +9.73%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |      454.74   |             16 |          20 | -3.73%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |      110.684  |             15 |          20 | +10.70% |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |       55.27   |             15 |          20 | +9.08%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |             15 |          20 | +10.37% |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |       86.03   |             15 |          20 | +12.59% |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |       21.94   |             15 |          20 | +12.81% |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |       78.84   |             15 |          20 | +9.92%  |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |      545      |             15 |          20 | -16.66% |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |       77.73   |             15 |          20 | +11.69% |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |       56.269  |             15 |          20 | -5.79%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |      189.29   |             15 |          20 | -11.24% |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |      227.11   |             15 |          20 | +14.24% |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |      465.97   |             15 |          20 | -6.05%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |       62.31   |             15 |          20 | -12.13% |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |      338.03   |             15 |          20 | -1.79%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |      281.5    |             15 |          20 | -11.25% |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |             15 |          20 | +10.37% |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |      363.84   |             14 |          20 | -4.37%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | 2026-10-22   |      264.153  |             14 |          20 | +8.77%  |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | 2026-10-22   |      509.34   |             14 |          20 | +3.70%  |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |      544.7    |             14 |          20 | +0.72%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |       77.57   |             14 |          20 | +11.72% |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |       84.3752 |             14 |          20 | +26.34% |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    | 2026-10-23   |       54.61   |             13 |          20 | +27.50% |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |             13 |          20 | +11.03% |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    | 2026-10-23   |      818.29   |             13 |          20 | -10.71% |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    | 2026-10-23   |       28.89   |             13 |          20 | +11.80% |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |             13 |          20 | +0.61%  |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    | 2026-10-23   |      117.97   |             13 |          20 | +10.71% |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |             13 |          20 | +9.44%  |
| jev_pick                  | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |             13 |          20 | +9.44%  |
| jev_pick                  | [ISRG](https://www.tradingview.com/chart/?symbol=ISRG)   | 2026-10-22    | 2026-10-23   |      443.65   |             13 |          20 | +1.44%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-10-22    | 2026-10-23   |      126.05   |             13 |          20 | +3.21%  |
| jev_skip                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-22    | 2026-10-23   |       13      |             13 |          20 | +18.62% |
| jev_skip                  | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |             13 |          20 | +11.03% |
| jev_skip                  | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |             13 |          20 | +0.61%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |             12 |          60 | -5.88%  |
| jev_pick                  | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |             12 |          20 | -5.88%  |
| jev_pick                  | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-23    | 2026-10-26   |      698.589  |             12 |          20 | -0.02%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             11 |          60 | -12.51% |
| jev_pick                  | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-26    | 2026-10-27   |      280.98   |             11 |          20 | +11.60% |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       91      |             10 |          60 | +6.42%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |             10 |          60 | -1.55%  |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-27    | 2026-10-28   |       58.64   |             10 |          20 | +24.52% |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-10-27    | 2026-10-28   |       56.79   |             10 |          20 | -15.88% |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-27    | 2026-10-28   |       53.3582 |             10 |          20 | +14.30% |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |              9 |          60 | +7.05%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |              9 |          60 | +6.91%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |              9 |          60 | -18.38% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |              9 |          60 | +9.53%  |
| falling_wedge_beaten_down | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-10-28    | 2026-10-29   |       94.96   |              9 |          20 | -0.03%  |
| early_rally_beaten_down   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |              9 |          20 | -18.38% |
| early_rally_beaten_down   | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-28    | 2026-10-29   |      342      |              9 |          20 | -2.93%  |
| early_rally_beaten_down   | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-28    | 2026-10-29   |      144.14   |              9 |          20 | -18.15% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |              8 |          60 | -12.19% |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |              8 |          60 | +2.23%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |              8 |          60 | +1.87%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |              8 |          60 | -1.08%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              8 |          20 | +7.49%  |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      260      |              8 |          20 | +2.98%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              8 |          20 | +7.49%  |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |              7 |          60 | +7.01%  |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |              7 |          60 | -11.12% |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       92.11   |              8 |         120 | +5.14%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |              7 |          20 | +0.29%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.73   |              7 |          20 | -17.61% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |              7 |          20 | +6.81%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |              7 |          20 | +7.82%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      264.18   |              7 |          20 | +1.36%  |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |              7 |          20 | +3.42%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |              7 |          20 | -16.40% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       93      |              7 |          20 | +4.13%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |              7 |          20 | +0.97%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |              7 |          20 | -0.85%  |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |              6 |          20 | +17.61% |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |              6 |          20 | +7.00%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.6    |              6 |          20 | +12.50% |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      159.6    |              6 |          20 | +5.94%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      379.55   |              6 |          20 | -6.67%  |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |              6 |          20 | +4.18%  |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |              6 |          20 | +5.19%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |              6 |          20 | -1.05%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |              5 |          20 | +2.51%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |              5 |          20 | -6.81%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |              5 |          20 | +5.59%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |              5 |          20 | -3.12%  |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |              5 |          20 | -6.81%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |              5 |          20 | +5.59%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |              5 |          20 | +10.25% |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |              5 |          20 | -7.42%  |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |              4 |          60 | +18.54% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |              4 |          60 | -5.32%  |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |              4 |          60 | +12.25% |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |              4 |          60 | +2.15%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |              4 |          60 | -10.78% |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |              5 |         120 | -2.05%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |              5 |         120 | +2.51%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |              5 |         120 | -4.08%  |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |              4 |          20 | -10.78% |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |              4 |          20 | +13.06% |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |              4 |          20 | -1.02%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |              4 |          20 | -4.61%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |              4 |          20 | -4.09%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |              4 |          20 | +1.69%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |              4 |          20 | +0.42%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      898.27   |              3 |          60 | -4.26%  |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |              3 |          60 | +8.09%  |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |              3 |          60 | +11.11% |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |              3 |          60 | +7.60%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |              3 |          60 | -3.39%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |              3 |          60 | +4.48%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      387.33   |              3 |          60 | +2.54%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |              3 |          60 | +4.93%  |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |              4 |         120 | +2.87%  |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      898.27   |              3 |          20 | -4.26%  |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |              3 |          20 | +8.09%  |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |              3 |          20 | +4.93%  |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |              3 |          20 | -7.69%  |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |              3 |          20 | +4.33%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      319.28   |              2 |          60 | -5.24%  |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.48   |              3 |         120 | +2.78%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.86   |              3 |         120 | +4.31%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |              2 |          20 | -2.60%  |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |              2 |          20 | +4.21%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      162.81   |              2 |          20 | +3.85%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48.33   |              2 |          20 | -1.16%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       97.3    |              2 |          20 | -0.45%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |              2 |          20 | +4.21%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.99   |              2 |          20 | -1.96%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |              2 |          20 | -1.26%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.71   |              2 |          20 | +2.01%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    | 2026-11-10   |       14.601  |              1 |          60 | +5.61%  |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    | 2026-11-10   |      173.98   |              1 |          60 | -2.93%  |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    | 2026-11-10   |       54.99   |              1 |          20 | +14.04% |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    | 2026-11-10   |       94.89   |              1 |          20 | +2.34%  |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    | 2026-11-10   |       85.09   |              1 |          20 | +3.35%  |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    | 2026-11-10   |      129.79   |              1 |          20 | +0.24%  |
| jev_skip                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-09    | 2026-11-10   |       28.44   |              1 |          20 | -0.46%  |
| insider_buy_beaten_down   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-09    | 2026-11-10   |      391.99   |              1 |         120 | +1.32%  |
| insider_buy_beaten_down   | [ADM](https://www.tradingview.com/chart/?symbol=ADM)     | 2026-11-09    | 2026-11-10   |       69.74   |              1 |         120 | -0.63%  |