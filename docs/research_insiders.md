# Insider buying (SEC Form 4): the strongest signal in the project so far

Data: the SEC's quarterly insider-transactions data sets (Forms 3/4/5, structured), 2016q3-2026q1, restricted to
open-market trades by **officers and directors** of the 518 S&P 500 / NASDAQ-100 members: 12,959 purchases and
212,560 sales. The **filing date** (median 2 days after the trade) is the signal date; entry at the next open.
Same discipline as every other study: train before 2023-01-01, test after, local random baseline (same stock,
±6 months), SPY-adjusted returns, 10 bps cost. Tables: [`research/insiders/`](research/insiders/); code:
`algovision/data/insiders.py`, `algovision/research/anomalies.py::dated_event_returns`.

## Results (long the stock; excess over local random, t-statistic)

| event | n | 60 bars | 120 bars | train 120 | test 120 |
|---|---|---|---|---|---|
| cluster buy: >= 2 insiders within 30 days | 635 | **+5.3 %** (t 6.0), hit 68 % | **+6.5 %** (t 5.0) | +8.0 % (t 4.9) | +2.9 % (t 1.4) |
| cluster buy: >= 3 insiders | 295 | +5.5 % (t 4.3) | +7.3 % (t 4.1) | +8.2 % (t 3.7) | +4.7 % (t 1.7) |
| single purchase >= $100k | 1,599 | +3.0 % (t 4.9) | **+5.6 %** (t 6.8) | +5.3 % (t 5.4) | **+6.0 % (t 4.1)** |
| single purchase >= $1M | 423 | +3.4 % (t 2.9) | +4.1 % (t 2.4) | +3.9 % (t 1.8) | +4.7 % (t 1.8) |
| control: cluster **sell**, >= 3 insiders | 7,860 | **−1.7 %** (t −6.8) | **−3.9 %** (t −11.0) | −4.4 % (t −11.0) | −3.0 % (t −4.2) |

Insider purchases predict outperformance over 2-6 months; clustered insider sales predict underperformance,
both with the same sign in both periods. Every yearly cohort of cluster buys was positive except 2021 (−3.8 %).

## The same regime effect, in its strongest form

| single purchases >= $100k, by state of the stock | n (train / test) | excess 60 bars | excess 120 bars |
|---|---|---|---|
| **beaten-down** (below 200-day MA, 6-month return < −8 %) | 436 / 202 | **+10.9 % / +8.4 %** (t 9.1 / 7.1) | **+17.3 % / +13.3 %** (t 10.9 / 7.5) |
| below the MA but not beaten-down | 191 / 91 | −0.3 % / +5.0 % | +4.2 % / +8.5 % |
| above the 200-day MA | 479 / 200 | **−3.3 % / −2.8 %** (t −3.4 / −1.5) | −5.1 % / −2.4 % |

Cluster buys in beaten-down stocks: +14.9 % / +8.6 % at 60 bars (t 8.8 / 4.9), +17.8 % / +9.5 % at 120 bars,
hit rate 72 %, positive in 8 of 9 years (2021: −0.4 %), about 31 events a year (~15 open positions with a
120-bar hold). An insider buying into an uptrend carries no information; an insider buying a stock that has
been beaten down is the strongest thing this project has measured.

Equal-weight portfolio of cluster buys in beaten-down stocks, 5 bps per trade:

| hold | CAGR | Sharpe | max drawdown | test CAGR | test Sharpe | random-shift test | SPY test |
|---|---|---|---|---|---|---|---|
| 60 bars | 22.3 % | 0.87 | −53 % | 36.5 % | 1.40 | 30.7 % / 0.94 | 1.35 |
| **120 bars** | 20.7 % | 0.83 | −53 % | **41.2 %** | **1.55** | 23.6 % / 0.90 | 1.45 |
| 250 bars | 18.8 % | 0.82 | −49 % | 28.6 % | 1.44 | 30.2 % / 1.44 | 1.42 |

The whole-period drawdown (−53 %) is 2020: these are beaten-down stocks, and the portfolio held ~15 of them
through March 2020, then made +23 % on that cohort. Size accordingly.

Other cuts: purchase size 250k-5M is the sweet spot (> $5M clusters carry no excess, they are often
founders / 10 %-owner-like directors); CEO/CFO involvement makes no difference; the effect builds over 60-120
days and is small in the first 20.

## Caveats

* **Survivorship**, as everywhere in this project, and again strongest in the beaten-down subset: insiders who
  bought into companies that then left the index are missing. The 2024-25 cohorts (+11 % / +10 % at 60 bars,
  removals not yet realised) argue it is not only that.
* The structured data sets are published with a lag of several months (latest: 2026q1). A **live** version needs
  EDGAR's daily index of Form 4 filings; see `insiders_live` in the CLI.
* 635 cluster events over ten years is not a large sample; the beaten-down subset is ~300. The t-statistics are
  large because the effect is large, not because n is.

## Bottom line

Insider open-market buying, filtered to beaten-down stocks, gives roughly +10 % over two to three months and
+15 % over six versus a random entry in the same stock, in both halves of the decade, with a sell-side mirror
image. It is the same idea the project keeps finding (a fallen stock plus a credible catalyst), with the most
credible catalyst of all: the people who run the company putting their own money in.
