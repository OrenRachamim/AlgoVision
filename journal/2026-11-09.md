# Forward-test journal - 2026-11-09

Data through 2026-11-09; 518 of 518 symbols loaded.

## New signals today (6)

| rule                    | symbol                                                 | signal_date   |   ref_price |   hold_bars | note                                                       |
|:------------------------|:-------------------------------------------------------|:--------------|------------:|------------:|:-----------------------------------------------------------|
| newsday                 | [TTD](https://www.tradingview.com/chart/?symbol=TTD)   | 2026-11-09    |       14.93 |          60 | gap +6.6%, vol 6.0x, 6m -31%, vs MA200 -23%                |
| newsday                 | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA) | 2026-11-09    |      178.67 |          60 | gap -7.3%, vol 3.9x, 6m -18%, vs MA200 -13%                |
| early_rally_beaten_down | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB) | 2026-11-09    |       58.86 |          20 | rsi_turn; day +10.9%, 10d +9.4%, 6m -50%, vs MA200 -25%    |
| early_rally_beaten_down | [NRG](https://www.tradingview.com/chart/?symbol=NRG)   | 2026-11-09    |       97.4  |          20 | rsi_turn; day +10.3%, 10d +4.6%, 6m -28%, vs MA200 -26%    |
| early_rally_beaten_down | [EXE](https://www.tradingview.com/chart/?symbol=EXE)   | 2026-11-09    |       85.96 |          20 | golden_20_50; day +1.6%, 10d -8.6%, 6m -10%, vs MA200 -10% |
| early_rally_beaten_down | [PLD](https://www.tradingview.com/chart/?symbol=PLD)   | 2026-11-09    |      130.55 |          20 | rsi_turn; day +2.8%, 10d +3.4%, 6m -8%, vs MA200 -4%       |

## Running results

Expectation vs realised (all logged trades, closed and open marked to market; 'vs beaten basket' = minus the equal-weight return of the stocks that were beaten down on the signal date over the same window):

| rule                      | research expected                                |   logged |   closed | mean   | hit   | vs SPY   | vs beaten basket   |
|:--------------------------|:-------------------------------------------------|---------:|---------:|:-------|:------|:---------|:-------------------|
| early_rally_beaten_down   | +2-3% net at 20 bars, hit ~58-61%, ~0 vs SPY     |      125 |       44 | +6.44% | 80%   | +9.19%   | +0.70%             |
| falling_wedge_beaten_down | +3% vs random at 20 bars, hit ~60%               |       35 |       23 | +3.54% | 69%   | +5.39%   | -1.59%             |
| insider_buy_beaten_down   | +10% vs random at 60 bars, +15% at 120, hit ~68% |       11 |        0 | +5.27% | 73%   | +5.91%   | +2.01%             |
| jev_pick                  | untested (forward test only)                     |       59 |       18 | +2.71% | 58%   | +3.47%   | -1.70%             |
| jev_skip                  | untested; a fall is the success case             |       15 |        0 | +7.62% | 93%   | +8.63%   | +5.14%             |
| newsday                   | +6-7% vs random at 60 bars, hit ~62%             |       47 |        0 | +0.64% | 51%   | +1.64%   | -4.48%             |

**early_rally_beaten_down** (expected: +2-3% net, hit ~58-61%, +3.5-4% vs random entry in the same stock, ~0 vs SPY at 20 bars (docs/research_rally.md))
- logged: 125, closed: 44, open: 81
- closed trades: mean +7.11%, median +7.16%, hit 89%, best +26.9%, worst -25.6%
- open trades mark-to-market: mean +6.06%, hit 75%
- SPY over the same holding periods: mean -2.75% (excess +9.19%)
- beaten-down basket over the same holding periods: mean +5.74% (excess +0.70%; the fair benchmark for a rule that only buys beaten-down stocks)

**falling_wedge_beaten_down** (expected: +3% vs random, hit ~60% (docs/research_falling_wedge.md))
- logged: 35, closed: 23, open: 12
- closed trades: mean +1.96%, median +4.10%, hit 65%, best +15.9%, worst -22.2%
- open trades mark-to-market: mean +6.58%, hit 75%
- SPY over the same holding periods: mean -1.84% (excess +5.39%)
- beaten-down basket over the same holding periods: mean +5.14% (excess -1.59%; the fair benchmark for a rule that only buys beaten-down stocks)

**insider_buy_beaten_down** (expected: +10% vs random at 60 bars, +15% at 120, hit ~68% (docs/research_insiders.md))
- logged: 11, closed: 0, open: 11
- open trades mark-to-market: mean +5.27%, hit 73%
- SPY over the same holding periods: mean -0.65% (excess +5.91%)
- beaten-down basket over the same holding periods: mean +3.26% (excess +2.01%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_pick** (expected: untested: the Jev decision model's 'buy' (P >= 0.6) on a listed stock, logged by daily-report (algovision/decide.py))
- logged: 59, closed: 18, open: 41
- closed trades: mean +7.18%, median +9.08%, hit 67%, best +26.9%, worst -11.0%
- open trades mark-to-market: mean +0.74%, hit 54%
- SPY over the same holding periods: mean -0.76% (excess +3.47%)
- beaten-down basket over the same holding periods: mean +4.41% (excess -1.70%; the fair benchmark for a rule that only buys beaten-down stocks)

**jev_skip** (expected: untested: the model's 'skip' (P(skip) >= 0.5); the call is right when the stock falls, so a NEGATIVE return is the success case)
- logged: 15, closed: 0, open: 15
- open trades mark-to-market: mean +7.62%, hit 93%
- SPY over the same holding periods: mean -1.00% (excess +8.63%)
- beaten-down basket over the same holding periods: mean +2.49% (excess +5.14%; the fair benchmark for a rule that only buys beaten-down stocks)

**newsday** (expected: +6-7% vs random, hit ~62% (docs/research_anomalies.md))
- logged: 47, closed: 0, open: 47
- open trades mark-to-market: mean +0.64%, hit 51%
- SPY over the same holding periods: mean -0.99% (excess +1.64%)
- beaten-down basket over the same holding periods: mean +5.12% (excess -4.48%; the fair benchmark for a rule that only buys beaten-down stocks)


## Open positions

| rule                      | symbol                                                   | signal_date   | entry_date   |   entry_price |   bars_elapsed |   hold_bars | ret     |
|:--------------------------|:---------------------------------------------------------|:--------------|:-------------|--------------:|---------------:|------------:|:--------|
| newsday                   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-09-04    | 2026-09-08   |      100.58   |             45 |          60 | +11.88% |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-04    | 2026-09-08   |      920.51   |             45 |          60 | -21.37% |
| newsday                   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-09-08    | 2026-09-09   |      232.548  |             44 |          60 | -7.01%  |
| newsday                   | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-09-09    | 2026-09-10   |      631.394  |             43 |          60 | +9.62%  |
| insider_buy_beaten_down   | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-09-08    | 2026-09-09   |       52.32   |             44 |         120 | +14.43% |
| newsday                   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-10    | 2026-09-11   |       54.66   |             42 |          60 | +16.96% |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-09-15    | 2026-09-16   |      441.33   |             39 |          60 | -31.30% |
| insider_buy_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-09-15    | 2026-09-16   |       54.37   |             39 |         120 | +17.58% |
| insider_buy_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-09-10    | 2026-09-11   |       72.99   |             42 |         120 | -2.49%  |
| newsday                   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-09-18    | 2026-09-21   |       71.82   |             36 |          60 | -10.96% |
| newsday                   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-09-24    | 2026-09-25   |       33.99   |             32 |          60 | -3.18%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-09-29    | 2026-09-30   |      602.02   |             29 |          60 | +20.22% |
| newsday                   | [CTVA](https://www.tradingview.com/chart/?symbol=CTVA)   | 2026-10-01    | 2026-10-02   |       12.385  |             27 |          60 | -2.22%  |
| newsday                   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-01    | 2026-10-02   |      614      |             27 |          60 | +17.88% |
| newsday                   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-02    | 2026-10-05   |       33.82   |             26 |          60 | +17.92% |
| newsday                   | [CHRW](https://www.tradingview.com/chart/?symbol=CHRW)   | 2026-10-05    | 2026-10-06   |      140.83   |             25 |          60 | -8.41%  |
| newsday                   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-10-09    | 2026-10-12   |      149.6    |             21 |          60 | +12.77% |
| newsday                   | [T](https://www.tradingview.com/chart/?symbol=T)         | 2026-10-09    | 2026-10-12   |       22.26   |             21 |          60 | -2.07%  |
| falling_wedge_beaten_down | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-13    | 2026-10-14   |       32.85   |             19 |          20 | -2.95%  |
| early_rally_beaten_down   | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-13    | 2026-10-14   |      182.6    |             19 |          20 | -6.41%  |
| early_rally_beaten_down   | [OTIS](https://www.tradingview.com/chart/?symbol=OTIS)   | 2026-10-13    | 2026-10-14   |       67.9    |             19 |          20 | +16.01% |
| early_rally_beaten_down   | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-13    | 2026-10-14   |      220.63   |             19 |          20 | +17.81% |
| early_rally_beaten_down   | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-10-13    | 2026-10-14   |       57.3149 |             19 |          20 | +13.76% |
| early_rally_beaten_down   | [DOV](https://www.tradingview.com/chart/?symbol=DOV)     | 2026-10-13    | 2026-10-14   |      191.79   |             19 |          20 | +11.05% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-14    | 2026-10-15   |       61.43   |             18 |          60 | -20.27% |
| early_rally_beaten_down   | [ROL](https://www.tradingview.com/chart/?symbol=ROL)     | 2026-10-14    | 2026-10-15   |       33.27   |             18 |          20 | +16.44% |
| early_rally_beaten_down   | [CIEN](https://www.tradingview.com/chart/?symbol=CIEN)   | 2026-10-14    | 2026-10-15   |      342.5    |             18 |          20 | -21.36% |
| early_rally_beaten_down   | [EFX](https://www.tradingview.com/chart/?symbol=EFX)     | 2026-10-14    | 2026-10-15   |      153.24   |             18 |          20 | +22.90% |
| early_rally_beaten_down   | [LYB](https://www.tradingview.com/chart/?symbol=LYB)     | 2026-10-14    | 2026-10-15   |       61.37   |             18 |          20 | -3.05%  |
| early_rally_beaten_down   | [LMT](https://www.tradingview.com/chart/?symbol=LMT)     | 2026-10-14    | 2026-10-15   |      531      |             18 |          20 | +10.77% |
| newsday                   | [CRWV](https://www.tradingview.com/chart/?symbol=CRWV)   | 2026-10-15    | 2026-10-16   |       65.195  |             17 |          60 | -24.87% |
| falling_wedge_beaten_down | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             17 |          20 | +1.58%  |
| falling_wedge_beaten_down | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-15    | 2026-10-16   |       27.96   |             17 |          20 | +16.06% |
| falling_wedge_beaten_down | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-15    | 2026-10-16   |       83.4    |             17 |          20 | +17.18% |
| falling_wedge_beaten_down | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-15    | 2026-10-16   |      529.98   |             17 |          20 | -11.98% |
| falling_wedge_beaten_down | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-15    | 2026-10-16   |      357.38   |             17 |          20 | -2.21%  |
| early_rally_beaten_down   | [AZO](https://www.tradingview.com/chart/?symbol=AZO)     | 2026-10-15    | 2026-10-16   |     3091      |             17 |          20 | +5.19%  |
| early_rally_beaten_down   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-15    | 2026-10-16   |       13.29   |             17 |          20 | +12.34% |
| early_rally_beaten_down   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-10-15    | 2026-10-16   |       36.42   |             17 |          20 | -22.19% |
| early_rally_beaten_down   | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-10-15    | 2026-10-16   |      120.66   |             17 |          20 | +12.77% |
| early_rally_beaten_down   | [SYK](https://www.tradingview.com/chart/?symbol=SYK)     | 2026-10-15    | 2026-10-16   |      295.89   |             17 |          20 | +10.08% |
| early_rally_beaten_down   | [NFLX](https://www.tradingview.com/chart/?symbol=NFLX)   | 2026-10-15    | 2026-10-16   |       69.87   |             17 |          20 | -8.47%  |
| early_rally_beaten_down   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-15    | 2026-10-16   |       44.45   |             17 |          20 | -0.97%  |
| early_rally_beaten_down   | [DOW](https://www.tradingview.com/chart/?symbol=DOW)     | 2026-10-15    | 2026-10-16   |       29.93   |             17 |          20 | +3.44%  |
| early_rally_beaten_down   | [LDOS](https://www.tradingview.com/chart/?symbol=LDOS)   | 2026-10-15    | 2026-10-16   |      125.05   |             17 |          20 | +8.56%  |
| early_rally_beaten_down   | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-10-15    | 2026-10-16   |      244.31   |             17 |          20 | +15.20% |
| early_rally_beaten_down   | [ALGN](https://www.tradingview.com/chart/?symbol=ALGN)   | 2026-10-15    | 2026-10-16   |      150.37   |             17 |          20 | +15.89% |
| early_rally_beaten_down   | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-15    | 2026-10-16   |      505.78   |             17 |          20 | +4.98%  |
| early_rally_beaten_down   | [LOW](https://www.tradingview.com/chart/?symbol=LOW)     | 2026-10-15    | 2026-10-16   |      195.819  |             17 |          20 | +18.53% |
| early_rally_beaten_down   | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-15    | 2026-10-16   |       37.67   |             17 |          20 | +5.87%  |
| early_rally_beaten_down   | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-15    | 2026-10-16   |       85.4496 |             17 |          20 | +23.50% |
| early_rally_beaten_down   | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-10-15    | 2026-10-16   |       79.6    |             17 |          20 | +9.12%  |
| early_rally_beaten_down   | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-15    | 2026-10-16   |      255.41   |             17 |          20 | +13.32% |
| early_rally_beaten_down   | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-15    | 2026-10-16   |      170.42   |             17 |          20 | +1.80%  |
| early_rally_beaten_down   | [CBRE](https://www.tradingview.com/chart/?symbol=CBRE)   | 2026-10-15    | 2026-10-16   |      136.02   |             17 |          20 | +1.58%  |
| falling_wedge_beaten_down | [HSY](https://www.tradingview.com/chart/?symbol=HSY)     | 2026-10-16    | 2026-10-19   |      169.41   |             16 |          20 | +2.40%  |
| falling_wedge_beaten_down | [MKC](https://www.tradingview.com/chart/?symbol=MKC)     | 2026-10-16    | 2026-10-19   |       45.99   |             16 |          20 | +4.11%  |
| early_rally_beaten_down   | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-16    | 2026-10-19   |      511      |             16 |          20 | +5.49%  |
| early_rally_beaten_down   | [COO](https://www.tradingview.com/chart/?symbol=COO)     | 2026-10-16    | 2026-10-19   |       57.29   |             16 |          20 | +11.59% |
| early_rally_beaten_down   | [AON](https://www.tradingview.com/chart/?symbol=AON)     | 2026-10-16    | 2026-10-19   |      288.293  |             16 |          20 | +16.47% |
| early_rally_beaten_down   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-16    | 2026-10-19   |      268.28   |             16 |          20 | +13.45% |
| early_rally_beaten_down   | [LHX](https://www.tradingview.com/chart/?symbol=LHX)     | 2026-10-16    | 2026-10-19   |      245.16   |             16 |          20 | +10.71% |
| early_rally_beaten_down   | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-10-16    | 2026-10-19   |       47.42   |             16 |          20 | +33.95% |
| early_rally_beaten_down   | [VICI](https://www.tradingview.com/chart/?symbol=VICI)   | 2026-10-16    | 2026-10-19   |       23.48   |             16 |          20 | +7.16%  |
| early_rally_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             16 |          20 | +8.40%  |
| early_rally_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-16    | 2026-10-19   |      104.16   |             16 |          20 | -4.70%  |
| early_rally_beaten_down   | [O](https://www.tradingview.com/chart/?symbol=O)         | 2026-10-16    | 2026-10-19   |       55.5347 |             16 |          20 | +7.14%  |
| early_rally_beaten_down   | [HD](https://www.tradingview.com/chart/?symbol=HD)       | 2026-10-16    | 2026-10-19   |      306.55   |             16 |          20 | +15.29% |
| early_rally_beaten_down   | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-10-16    | 2026-10-19   |       33.45   |             16 |          20 | -4.69%  |
| insider_buy_beaten_down   | [PEP](https://www.tradingview.com/chart/?symbol=PEP)     | 2026-10-16    | 2026-10-19   |      130.88   |             16 |         120 | +8.40%  |
| early_rally_beaten_down   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-19    | 2026-10-20   |      454.74   |             15 |          20 | -2.90%  |
| falling_wedge_beaten_down | [BX](https://www.tradingview.com/chart/?symbol=BX)       | 2026-10-20    | 2026-10-21   |      110.684  |             14 |          20 | +12.08% |
| falling_wedge_beaten_down | [TSN](https://www.tradingview.com/chart/?symbol=TSN)     | 2026-10-20    | 2026-10-21   |       55.27   |             14 |          20 | +8.32%  |
| early_rally_beaten_down   | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |             14 |          20 | +12.53% |
| early_rally_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-10-20    | 2026-10-21   |       86.03   |             14 |          20 | +13.60% |
| early_rally_beaten_down   | [CMCSA](https://www.tradingview.com/chart/?symbol=CMCSA) | 2026-10-20    | 2026-10-21   |       21.94   |             14 |          20 | +11.71% |
| early_rally_beaten_down   | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-20    | 2026-10-21   |       78.84   |             14 |          20 | +16.16% |
| early_rally_beaten_down   | [CMI](https://www.tradingview.com/chart/?symbol=CMI)     | 2026-10-20    | 2026-10-21   |      545      |             14 |          20 | -14.41% |
| early_rally_beaten_down   | [TXT](https://www.tradingview.com/chart/?symbol=TXT)     | 2026-10-20    | 2026-10-21   |       77.73   |             14 |          20 | +9.88%  |
| early_rally_beaten_down   | [CARR](https://www.tradingview.com/chart/?symbol=CARR)   | 2026-10-20    | 2026-10-21   |       56.269  |             14 |          20 | -5.22%  |
| jev_pick                  | [ODFL](https://www.tradingview.com/chart/?symbol=ODFL)   | 2026-10-20    | 2026-10-21   |      189.29   |             14 |          20 | -9.72%  |
| jev_pick                  | [FERG](https://www.tradingview.com/chart/?symbol=FERG)   | 2026-10-20    | 2026-10-21   |      227.11   |             14 |          20 | +14.45% |
| jev_pick                  | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-20    | 2026-10-21   |      465.97   |             14 |          20 | -5.24%  |
| jev_pick                  | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-10-20    | 2026-10-21   |       62.31   |             14 |          20 | -12.25% |
| jev_pick                  | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-20    | 2026-10-21   |      338.03   |             14 |          20 | -5.49%  |
| jev_pick                  | [JBL](https://www.tradingview.com/chart/?symbol=JBL)     | 2026-10-20    | 2026-10-21   |      281.5    |             14 |          20 | -10.28% |
| jev_skip                  | [LULU](https://www.tradingview.com/chart/?symbol=LULU)   | 2026-10-20    | 2026-10-21   |      100      |             14 |          20 | +12.53% |
| early_rally_beaten_down   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-21    | 2026-10-22   |      363.84   |             13 |          20 | -3.95%  |
| jev_pick                  | [VMC](https://www.tradingview.com/chart/?symbol=VMC)     | 2026-10-21    | 2026-10-22   |      264.64   |             13 |          20 | +9.37%  |
| jev_pick                  | [MLM](https://www.tradingview.com/chart/?symbol=MLM)     | 2026-10-21    | 2026-10-22   |      509.34   |             13 |          20 | +4.25%  |
| jev_pick                  | [NOC](https://www.tradingview.com/chart/?symbol=NOC)     | 2026-10-21    | 2026-10-22   |      544.7    |             13 |          20 | -1.03%  |
| jev_skip                  | [LEN](https://www.tradingview.com/chart/?symbol=LEN)     | 2026-10-21    | 2026-10-22   |       77.57   |             13 |          20 | +18.06% |
| jev_skip                  | [CLX](https://www.tradingview.com/chart/?symbol=CLX)     | 2026-10-21    | 2026-10-22   |       84.3752 |             13 |          20 | +25.07% |
| early_rally_beaten_down   | [PNR](https://www.tradingview.com/chart/?symbol=PNR)     | 2026-10-22    | 2026-10-23   |       54.61   |             12 |          20 | +28.55% |
| early_rally_beaten_down   | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |             12 |          20 | +16.39% |
| early_rally_beaten_down   | [FICO](https://www.tradingview.com/chart/?symbol=FICO)   | 2026-10-22    | 2026-10-23   |      818.29   |             12 |          20 | -11.55% |
| early_rally_beaten_down   | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-22    | 2026-10-23   |       28.89   |             12 |          20 | +12.32% |
| early_rally_beaten_down   | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |             12 |          20 | +5.64%  |
| early_rally_beaten_down   | [PHM](https://www.tradingview.com/chart/?symbol=PHM)     | 2026-10-22    | 2026-10-23   |      117.97   |             12 |          20 | +15.18% |
| early_rally_beaten_down   | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |             12 |          20 | +6.45%  |
| jev_pick                  | [KKR](https://www.tradingview.com/chart/?symbol=KKR)     | 2026-10-22    | 2026-10-23   |       92.15   |             12 |          20 | +6.45%  |
| jev_pick                  | [ISRG](https://www.tradingview.com/chart/?symbol=ISRG)   | 2026-10-22    | 2026-10-23   |      443.65   |             12 |          20 | +3.81%  |
| jev_pick                  | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-10-22    | 2026-10-23   |      126.05   |             12 |          20 | +3.57%  |
| jev_skip                  | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-10-22    | 2026-10-23   |       13      |             12 |          20 | +14.85% |
| jev_skip                  | [BLDR](https://www.tradingview.com/chart/?symbol=BLDR)   | 2026-10-22    | 2026-10-23   |       56.68   |             12 |          20 | +16.39% |
| jev_skip                  | [NVR](https://www.tradingview.com/chart/?symbol=NVR)     | 2026-10-22    | 2026-10-23   |     6000      |             12 |          20 | +5.64%  |
| newsday                   | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |             11 |          60 | -5.26%  |
| jev_pick                  | [FIX](https://www.tradingview.com/chart/?symbol=FIX)     | 2026-10-23    | 2026-10-26   |     1175.01   |             11 |          20 | -5.26%  |
| jev_pick                  | [CASY](https://www.tradingview.com/chart/?symbol=CASY)   | 2026-10-23    | 2026-10-26   |      698.589  |             11 |          20 | -0.92%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-10-26    | 2026-10-27   |     1703.28   |             10 |          60 | -10.02% |
| jev_pick                  | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-26    | 2026-10-27   |      280.98   |             10 |          20 | +8.32%  |
| newsday                   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-27    | 2026-10-28   |       91      |              9 |          60 | +9.08%  |
| newsday                   | [HUBB](https://www.tradingview.com/chart/?symbol=HUBB)   | 2026-10-27    | 2026-10-28   |      444.68   |              9 |          60 | -0.70%  |
| falling_wedge_beaten_down | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-27    | 2026-10-28   |       58.64   |              9 |          20 | +30.05% |
| early_rally_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-10-27    | 2026-10-28   |       56.79   |              9 |          20 | -14.69% |
| early_rally_beaten_down   | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-27    | 2026-10-28   |       53.3582 |              9 |          20 | +15.05% |
| newsday                   | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-28    | 2026-10-29   |      325.01   |              8 |          60 | +7.53%  |
| newsday                   | [BSX](https://www.tradingview.com/chart/?symbol=BSX)     | 2026-10-28    | 2026-10-29   |       41.81   |              8 |          60 | +5.29%  |
| newsday                   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |              8 |          60 | -15.75% |
| newsday                   | [CSGP](https://www.tradingview.com/chart/?symbol=CSGP)   | 2026-10-28    | 2026-10-29   |       27.69   |              8 |          60 | +12.82% |
| falling_wedge_beaten_down | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-10-28    | 2026-10-29   |       94.96   |              8 |          20 | +4.38%  |
| early_rally_beaten_down   | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-28    | 2026-10-29   |      237.96   |              8 |          20 | -15.75% |
| early_rally_beaten_down   | [AVGO](https://www.tradingview.com/chart/?symbol=AVGO)   | 2026-10-28    | 2026-10-29   |      342      |              8 |          20 | -6.58%  |
| early_rally_beaten_down   | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-10-28    | 2026-10-29   |      144.14   |              8 |          20 | -16.89% |
| newsday                   | [ALNY](https://www.tradingview.com/chart/?symbol=ALNY)   | 2026-10-29    | 2026-10-30   |      172.7    |              7 |          60 | -9.32%  |
| newsday                   | [GOOGL](https://www.tradingview.com/chart/?symbol=GOOGL) | 2026-10-29    | 2026-10-30   |      281.12   |              7 |          60 | +2.50%  |
| newsday                   | [GOOG](https://www.tradingview.com/chart/?symbol=GOOG)   | 2026-10-29    | 2026-10-30   |      279.69   |              7 |          60 | +2.26%  |
| newsday                   | [HII](https://www.tradingview.com/chart/?symbol=HII)     | 2026-10-29    | 2026-10-30   |      317      |              7 |          60 | -3.99%  |
| early_rally_beaten_down   | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              7 |          20 | +12.26% |
| early_rally_beaten_down   | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-29    | 2026-10-30   |      260      |              7 |          20 | +6.19%  |
| jev_pick                  | [CVNA](https://www.tradingview.com/chart/?symbol=CVNA)   | 2026-10-29    | 2026-10-30   |       67.93   |              7 |          20 | +12.26% |
| newsday                   | [RDDT](https://www.tradingview.com/chart/?symbol=RDDT)   | 2026-10-30    | 2026-11-02   |       92.21   |              6 |          60 | +9.30%  |
| newsday                   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-10-30    | 2026-11-02   |       65.4    |              6 |          60 | -9.22%  |
| insider_buy_beaten_down   | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-29    | 2026-10-30   |       92.11   |              7 |         120 | +7.76%  |
| early_rally_beaten_down   | [WY](https://www.tradingview.com/chart/?symbol=WY)       | 2026-10-30    | 2026-11-02   |       20.57   |              6 |          20 | +2.72%  |
| jev_pick                  | [VRT](https://www.tradingview.com/chart/?symbol=VRT)     | 2026-10-30    | 2026-11-02   |      235.73   |              6 |          20 | -14.96% |
| jev_pick                  | [CPRT](https://www.tradingview.com/chart/?symbol=CPRT)   | 2026-10-30    | 2026-11-02   |       30.24   |              6 |          20 | +7.31%  |
| jev_pick                  | [FER](https://www.tradingview.com/chart/?symbol=FER)     | 2026-10-30    | 2026-11-02   |       56.5664 |              6 |          20 | +8.53%  |
| jev_pick                  | [CEG](https://www.tradingview.com/chart/?symbol=CEG)     | 2026-10-30    | 2026-11-02   |      264.18   |              6 |          20 | +4.51%  |
| jev_pick                  | [PEG](https://www.tradingview.com/chart/?symbol=PEG)     | 2026-10-30    | 2026-11-02   |       72.21   |              6 |          20 | +3.91%  |
| jev_pick                  | [TPL](https://www.tradingview.com/chart/?symbol=TPL)     | 2026-10-30    | 2026-11-02   |      328.49   |              6 |          20 | -15.29% |
| jev_skip                  | [XYL](https://www.tradingview.com/chart/?symbol=XYL)     | 2026-10-30    | 2026-11-02   |       93      |              6 |          20 | +6.73%  |
| jev_skip                  | [LII](https://www.tradingview.com/chart/?symbol=LII)     | 2026-10-30    | 2026-11-02   |      344.58   |              6 |          20 | +1.42%  |
| jev_skip                  | [NKE](https://www.tradingview.com/chart/?symbol=NKE)     | 2026-10-30    | 2026-11-02   |       39      |              6 |          20 | +2.26%  |
| early_rally_beaten_down   | [CHTR](https://www.tradingview.com/chart/?symbol=CHTR)   | 2026-11-02    | 2026-11-03   |      113.99   |              5 |          20 | +6.33%  |
| early_rally_beaten_down   | [LVS](https://www.tradingview.com/chart/?symbol=LVS)     | 2026-11-02    | 2026-11-03   |       38.15   |              5 |          20 | +5.32%  |
| early_rally_beaten_down   | [WYNN](https://www.tradingview.com/chart/?symbol=WYNN)   | 2026-11-02    | 2026-11-03   |       77.6    |              5 |          20 | +11.73% |
| jev_pick                  | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-02    | 2026-11-03   |      159.6    |              5 |          20 | +5.71%  |
| jev_pick                  | [ETN](https://www.tradingview.com/chart/?symbol=ETN)     | 2026-11-02    | 2026-11-03   |      379.55   |              5 |          20 | -5.34%  |
| jev_pick                  | [MPWR](https://www.tradingview.com/chart/?symbol=MPWR)   | 2026-11-02    | 2026-11-03   |     1303.15   |              5 |          20 | +6.51%  |
| jev_skip                  | [IDXX](https://www.tradingview.com/chart/?symbol=IDXX)   | 2026-11-02    | 2026-11-03   |      662.26   |              5 |          20 | +6.70%  |
| jev_skip                  | [AOS](https://www.tradingview.com/chart/?symbol=AOS)     | 2026-11-02    | 2026-11-03   |       65.04   |              5 |          20 | +0.25%  |
| early_rally_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |              4 |          20 | +2.05%  |
| early_rally_beaten_down   | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |              4 |          20 | -3.03%  |
| early_rally_beaten_down   | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |              4 |          20 | +2.57%  |
| jev_pick                  | [ORCL](https://www.tradingview.com/chart/?symbol=ORCL)   | 2026-11-03    | 2026-11-04   |      121.78   |              4 |          20 | -1.63%  |
| jev_pick                  | [GEV](https://www.tradingview.com/chart/?symbol=GEV)     | 2026-11-03    | 2026-11-04   |      855.245  |              4 |          20 | -3.03%  |
| jev_pick                  | [ECHO](https://www.tradingview.com/chart/?symbol=ECHO)   | 2026-11-03    | 2026-11-04   |       98.65   |              4 |          20 | +2.57%  |
| jev_pick                  | [TPR](https://www.tradingview.com/chart/?symbol=TPR)     | 2026-11-03    | 2026-11-04   |      123.01   |              4 |          20 | +10.62% |
| jev_pick                  | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-03    | 2026-11-04   |       30.58   |              4 |          20 | -7.33%  |
| newsday                   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-04    | 2026-11-05   |       81.92   |              3 |          60 | +18.90% |
| newsday                   | [FIS](https://www.tradingview.com/chart/?symbol=FIS)     | 2026-11-04    | 2026-11-05   |       29.9    |              3 |          60 | -5.22%  |
| newsday                   | [VST](https://www.tradingview.com/chart/?symbol=VST)     | 2026-11-04    | 2026-11-05   |      116.86   |              3 |          60 | +14.60% |
| newsday                   | [TRMB](https://www.tradingview.com/chart/?symbol=TRMB)   | 2026-11-04    | 2026-11-05   |       53.6    |              3 |          60 | +2.01%  |
| newsday                   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |              3 |          60 | -5.54%  |
| insider_buy_beaten_down   | [BA](https://www.tradingview.com/chart/?symbol=BA)       | 2026-11-03    | 2026-11-04   |      177      |              4 |         120 | -2.61%  |
| insider_buy_beaten_down   | [MGM](https://www.tradingview.com/chart/?symbol=MGM)     | 2026-11-03    | 2026-11-04   |       32.25   |              4 |         120 | +2.05%  |
| insider_buy_beaten_down   | [CAT](https://www.tradingview.com/chart/?symbol=CAT)     | 2026-11-03    | 2026-11-04   |      609.45   |              4 |         120 | -1.73%  |
| early_rally_beaten_down   | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-04    | 2026-11-05   |      202.85   |              3 |          20 | -5.54%  |
| early_rally_beaten_down   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-04    | 2026-11-05   |      349.83   |              3 |          20 | +17.20% |
| early_rally_beaten_down   | [UBER](https://www.tradingview.com/chart/?symbol=UBER)   | 2026-11-04    | 2026-11-05   |       70.77   |              3 |          20 | +0.57%  |
| jev_pick                  | [HAL](https://www.tradingview.com/chart/?symbol=HAL)     | 2026-11-04    | 2026-11-05   |       33.4    |              3 |          20 | -4.55%  |
| jev_skip                  | [NEE](https://www.tradingview.com/chart/?symbol=NEE)     | 2026-11-04    | 2026-11-05   |       89.95   |              3 |          20 | -3.44%  |
| jev_skip                  | [FISV](https://www.tradingview.com/chart/?symbol=FISV)   | 2026-11-04    | 2026-11-05   |       62.27   |              3 |          20 | +2.01%  |
| jev_skip                  | [MCD](https://www.tradingview.com/chart/?symbol=MCD)     | 2026-11-04    | 2026-11-05   |      281      |              3 |          20 | +0.16%  |
| newsday                   | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      898.27   |              2 |          60 | -1.31%  |
| newsday                   | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |              2 |          60 | +9.63%  |
| newsday                   | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-05    | 2026-11-06   |      355.95   |              2 |          60 | +15.18% |
| newsday                   | [QCOM](https://www.tradingview.com/chart/?symbol=QCOM)   | 2026-11-05    | 2026-11-06   |      161.28   |              2 |          60 | +6.32%  |
| newsday                   | [MELI](https://www.tradingview.com/chart/?symbol=MELI)   | 2026-11-05    | 2026-11-06   |     1542.5    |              2 |          60 | -0.64%  |
| newsday                   | [IRM](https://www.tradingview.com/chart/?symbol=IRM)     | 2026-11-05    | 2026-11-06   |      106.03   |              2 |          60 | +4.55%  |
| newsday                   | [ROK](https://www.tradingview.com/chart/?symbol=ROK)     | 2026-11-05    | 2026-11-06   |      387.33   |              2 |          60 | +0.52%  |
| newsday                   | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |              2 |          60 | +5.30%  |
| insider_buy_beaten_down   | [INTC](https://www.tradingview.com/chart/?symbol=INTC)   | 2026-11-04    | 2026-11-05   |       56.51   |              3 |         120 | +5.06%  |
| jev_pick                  | [SNDK](https://www.tradingview.com/chart/?symbol=SNDK)   | 2026-11-05    | 2026-11-06   |      898.27   |              2 |          20 | -1.31%  |
| jev_pick                  | [PWR](https://www.tradingview.com/chart/?symbol=PWR)     | 2026-11-05    | 2026-11-06   |      539.5    |              2 |          20 | +9.63%  |
| jev_pick                  | [ADI](https://www.tradingview.com/chart/?symbol=ADI)     | 2026-11-05    | 2026-11-06   |      374.81   |              2 |          20 | +5.30%  |
| jev_pick                  | [FSLR](https://www.tradingview.com/chart/?symbol=FSLR)   | 2026-11-05    | 2026-11-06   |      196.05   |              2 |          20 | -2.26%  |
| jev_pick                  | [EME](https://www.tradingview.com/chart/?symbol=EME)     | 2026-11-05    | 2026-11-06   |      618.62   |              2 |          20 | +5.54%  |
| newsday                   | [AXON](https://www.tradingview.com/chart/?symbol=AXON)   | 2026-11-06    | 2026-11-09   |      320.5    |              1 |          60 | -5.40%  |
| insider_buy_beaten_down   | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-05    | 2026-11-06   |       46.48   |              2 |         120 | +4.24%  |
| insider_buy_beaten_down   | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-05    | 2026-11-06   |       92.86   |              2 |         120 | +5.24%  |
| early_rally_beaten_down   | [ALB](https://www.tradingview.com/chart/?symbol=ALB)     | 2026-11-06    | 2026-11-09   |       97.46   |              1 |          20 | +1.70%  |
| early_rally_beaten_down   | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |              1 |          20 | +2.87%  |
| early_rally_beaten_down   | [TMUS](https://www.tradingview.com/chart/?symbol=TMUS)   | 2026-11-06    | 2026-11-09   |      162.5    |              1 |          20 | +3.82%  |
| jev_pick                  | [BKR](https://www.tradingview.com/chart/?symbol=BKR)     | 2026-11-06    | 2026-11-09   |       48      |              1 |          20 | +0.94%  |
| jev_pick                  | [CRH](https://www.tradingview.com/chart/?symbol=CRH)     | 2026-11-06    | 2026-11-09   |       97.3    |              1 |          20 | +0.44%  |
| jev_pick                  | [HWM](https://www.tradingview.com/chart/?symbol=HWM)     | 2026-11-06    | 2026-11-09   |      210.21   |              1 |          20 | +2.87%  |
| jev_pick                  | [PDD](https://www.tradingview.com/chart/?symbol=PDD)     | 2026-11-06    | 2026-11-09   |       80.935  |              1 |          20 | -0.54%  |
| jev_pick                  | [DPZ](https://www.tradingview.com/chart/?symbol=DPZ)     | 2026-11-06    | 2026-11-09   |      334.28   |              1 |          20 | -0.03%  |
| jev_skip                  | [APP](https://www.tradingview.com/chart/?symbol=APP)     | 2026-11-06    | 2026-11-09   |      387.725  |              1 |          20 | +5.75%  |
| newsday                   | [TTD](https://www.tradingview.com/chart/?symbol=TTD)     | 2026-11-09    |              |               |            nan |          60 |         |
| newsday                   | [NVDA](https://www.tradingview.com/chart/?symbol=NVDA)   | 2026-11-09    |              |               |            nan |          60 |         |
| early_rally_beaten_down   | [RKLB](https://www.tradingview.com/chart/?symbol=RKLB)   | 2026-11-09    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [NRG](https://www.tradingview.com/chart/?symbol=NRG)     | 2026-11-09    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [EXE](https://www.tradingview.com/chart/?symbol=EXE)     | 2026-11-09    |              |               |            nan |          20 |         |
| early_rally_beaten_down   | [PLD](https://www.tradingview.com/chart/?symbol=PLD)     | 2026-11-09    |              |               |            nan |          20 |         |