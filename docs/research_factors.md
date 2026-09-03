# Momentum and short-term reversal on the same universe

Tables: [`research/factors/`](research/factors/). Reproduce with `python -m algovision factors`.
Same data (518 S&P 500 / NASDAQ-100 members, 2016-09 to 2026-09, daily), same discipline (train before
2023-01-01, test after; local random baselines for the event study; costs included).

**Survivorship warning, stronger here than for patterns.** The universe is today's index members. Stocks
that fell out of the index (the true "losers") are missing, so the bottom momentum decile is made of losers
that recovered, and every long-only number is inflated. Comparisons *between* groups inside the universe and
against the equal-weight universe are the robust part; absolute returns are not.

## 1. Cross-sectional momentum (monthly deciles, trade at next open, 10 bps per side on turnover)

Annual return of the top decile minus the equal-weight universe (the long leg's edge), and the long-short spread
net of both legs' costs:

| formation | top − universe, train | t | top − universe, test | t | long-short net, all | t | hit (months) |
|---|---|---|---|---|---|---|---|
| 12-1 (12 months, skip last) | +3.9 % | 0.9 | **+24.8 %** | 2.4 | +5.2 % | 1.0 | 55 % |
| 6-1 | +7.1 % | 1.6 | +9.7 % | 1.2 | +1.9 % | 0.6 | 53 % |
| 3-1 | +5.6 % | 1.5 | +4.0 % | 0.6 | −5.6 % | −0.6 | 49 % |
| 1-0 (last month) | −3.8 % | −1.0 | +20.0 % | 2.3 | −2.7 % | −0.1 | 48 % |

Reading:

* The top decile beat the universe in every variant and in both periods, but the size is unstable. For 12-1
  almost the entire profit sits in 2023-26 (the AI mega-cap rally): +24.8 % a year in the test period against
  +3.9 % and not significant before. 6-1 is the most consistent (+7 % / +10 %), still with t-stats below 2.
* The long-short spread is not significant in any variant (best t = 1.0). The bottom decile did *not*
  underperform (survivorship: the losers that survived are the ones that bounced), so shorting losers added nothing here.
* Turnover: the top decile turns over ~27 % a month for 12-1 (cheap) and ~85 % for 1-0 (expensive).
* Max drawdown of the top decile: −23 % (12-1), against −27 % for the universe. It is not a smoother ride.

Time-series momentum on SPY (long when the 12-month return is positive, else cash): Sharpe 0.67 vs 0.88 for
buy-and-hold; a 200-day MA filter gives the same Sharpe as buy-and-hold (0.88) with a −21 % instead of −34 %
max drawdown. Trend filters bought lower drawdown at the price of return in this decade.

## 2. Short-term reversal

### (a) Event study: buy after an N-sigma down day, short after an N-sigma up day

Entry at the next open, returns net of 5 bps, compared with the same holding period on random nearby days in
the same stock (`xloc`). One event per cluster; 30,976 spikes and 31,685 crashes at 2σ.

| event | hold | net return | hit | local random hit | xloc | t | train xloc | test xloc |
|---|---|---|---|---|---|---|---|---|
| buy 2σ down day | 1 | −0.01 % | 50.0 % | 50.9 % | +0.01 % | 0.9 | +0.02 % | −0.00 % |
| buy 2σ down day | 3 | −0.13 % | 51.6 % | 53.5 % | **−0.27 %** | −10.0 | −0.42 % | +0.01 % |
| buy 2σ down day | 10 | +0.34 % | 55.7 % | 56.6 % | −0.38 % | −7.6 | −0.73 % | +0.27 % |
| buy 3σ down day | 3 | −0.66 % | 49.0 % | 53.5 % | −0.79 % | −13.9 | −1.19 % | −0.03 % |
| short 2σ up day | 5 | −0.21 % | 46.4 % | 45.9 % | +0.13 % | 4.1 | +0.19 % | +0.04 % |
| buy 3-day 2σ decline | 3 | −0.13 % | 51.3 % | 53.3 % | −0.26 % | −6.8 | −0.60 % | +0.42 % |

Reading:

* **Buying single-stock crashes does not work on large caps.** After a 2σ down day the stock keeps
  *underperforming* its own random baseline for days (−0.27 % at 3 days, t = −10; −0.79 % after a 3σ day).
  Big down days in large caps are mostly news (earnings, guidance) and news drifts, it does not bounce.
  2020 alone: −2.2 % per event in three days (t = −17).
* It is worse in beaten-down stocks (below the 200-day MA: −0.36 % vs −0.20 % above). Contrast with the wedge:
  a *slow* bottoming in a beaten-down stock has an edge, a *sharp* crash in one does not.
* Shorting spikes has a statistically visible but economically useless edge (+0.13 % over 5 days before
  costs, negative after).
* The test period flips sign for the 3-day version (+0.42 % at 3 days, t = 7.4), i.e. the effect is regime
  dependent and the sign is not predictable ex ante.
* Equal-weight portfolio of all 2σ crash buys, hold 3 days: Sharpe 0.30, max drawdown −38 %; shorting spikes:
  Sharpe −0.78.

### (b) Weekly cross-sectional reversal (rank on last week's return, hold a week)

| | train | test |
|---|---|---|
| last week's winners (D10) − universe | **−16.4 % / yr** (t = −3.9) | −2.0 % (t = −0.2) |
| last week's losers (D1) − universe | +1.5 % (t = 0.5) | +3.8 % (t = 0.7) |
| long losers / short winners, gross | +20 % | +8 % |
| same, net of 10 bps per side (85 % weekly turnover) | **−33 %** | −23 % |

The classic weekly reversal was real until 2022 and lived entirely in the short leg (last week's winners
underperform); it faded to nothing in 2023-26, and at any realistic cost it is a machine for paying commissions.

## Bottom line

* **Momentum**: the only thing here with a consistent sign. Holding the top decile of 6-12-month winners beat
  the universe in both periods, by an unstable amount (+4 % to +25 % a year), with low turnover and no better
  drawdown. Not significant as a long-short factor in this sample, and inflated by survivorship on the long
  side. Reasonable as a *tilt* inside a long portfolio; not a standalone trading strategy on ten years of data.
* **Short-term reversal**: dead at the single-stock daily level for US large caps in this decade, and negative
  after big crash days. The weekly cross-sectional version faded and cannot pay its costs.
* Pattern of everything tested so far: slow, regime-level effects (beaten-down stock, slow bottoming,
  multi-month momentum) survive; fast, price-only signals (chart shapes, day-level reversal, small take-profits)
  do not, because that is where the fastest money already is.
