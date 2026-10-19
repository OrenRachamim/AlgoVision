# Crossing back above the 200-day MA after a long run below it

Event: a close above the 200-day moving average whose previous close was at or below it, after at least 60 consecutive closes at or below the line; at most one event per stock per 20 bars; entry at the next open; 1866 events, 2017-10-30 to 2026-07-23, train < 2023-01-01 / test >= 2023-01-01. *xloc* = the return minus the mean return of 10 random entries in the same stock within +-126 bars (the same horizon), *xspy* = minus the SPY over the same window, *hit* = share of positive returns, *t* = t-statistic of xloc. Buckets by the length of the run below the line (bars).

## Verdict

**Not passed** for runs of 120+ bars at 20 bars (the rule: at least +0.5% over local random entries in both periods with 30+ events each): xloc +0.1% (train, n 446) / +0.9% (test, n 361); vs SPY +0.7% / +0.1%; hit 54% / 52%; raw +1.1% / +1.2%.

## By run length and period

| bucket    | period   |    n | ret_20   | hit_20   | xspy_20   | xloc_20   |   t_20 | ret_60   | hit_60   | xspy_60   | xloc_60   |   t_60 |
|:----------|:---------|-----:|:---------|:---------|:----------|:----------|-------:|:---------|:---------|:----------|:----------|-------:|
| all (60+) | train    | 1064 | -0.5%    | 51%      | -0.7%     | -1.0%     |   -3.4 | +2.4%    | 59%      | +0.3%     | +2.5%     |    4.4 |
| 60-119    | train    |  618 | -1.7%    | 48%      | -1.7%     | -1.9%     |   -4.7 | +0.6%    | 55%      | -1.4%     | +2.0%     |    2.9 |
| 120-199   | train    |  342 | +1.3%    | 55%      | +1.0%     | +0.0%     |    0   | +6.0%    | 65%      | +3.8%     | +4.0%     |    4.5 |
| 200+      | train    |  104 | +0.5%    | 52%      | -0.2%     | +0.4%     |    0.4 | +1.3%    | 61%      | -0.7%     | +0.2%     |    0.1 |
| 120+      | train    |  446 | +1.1%    | 54%      | +0.7%     | +0.1%     |    0.2 | +4.9%    | 64%      | +2.7%     | +3.1%     |    3.3 |
| all (60+) | test     |  802 | +1.4%    | 55%      | +0.2%     | +1.4%     |    3.6 | +2.2%    | 53%      | -2.5%     | +3.3%     |    4.7 |
| 60-119    | test     |  441 | +1.5%    | 57%      | +0.3%     | +1.9%     |    3.7 | +2.6%    | 55%      | -2.5%     | +4.6%     |    5   |
| 120-199   | test     |  225 | +1.1%    | 54%      | -0.1%     | +0.7%     |    1   | +1.0%    | 52%      | -3.6%     | +0.5%     |    0.5 |
| 200+      | test     |  136 | +1.3%    | 49%      | +0.4%     | +1.1%     |    1   | +3.0%    | 53%      | -0.8%     | +3.6%     |    1.6 |
| 120+      | test     |  361 | +1.2%    | 52%      | +0.1%     | +0.9%     |    1.4 | +1.7%    | 52%      | -2.5%     | +1.7%     |    1.6 |

## By year (runs of 120+ bars, 20 bars)

|   year |   n | ret_20   | xloc_20   | xspy_20   | hit_20   |
|-------:|----:|:---------|:----------|:----------|:---------|
|   2018 |  46 | -1.0%    | -1.4%     | -0.7%     | 50%      |
|   2019 | 123 | +0.7%    | +0.6%     | -0.7%     | 54%      |
|   2020 | 111 | +5.0%    | +2.2%     | +3.7%     | 62%      |
|   2021 |  10 | +4.2%    | +4.7%     | +1.5%     | 80%      |
|   2022 | 156 | -0.9%    | -1.6%     | +0.1%     | 49%      |
|   2023 | 147 | +2.8%    | +2.7%     | +1.5%     | 55%      |
|   2024 |  57 | -1.1%    | -1.3%     | -2.0%     | 40%      |
|   2025 |  99 | +0.3%    | -0.6%     | -1.4%     | 57%      |
|   2026 |  58 | +1.1%    | +0.8%     | +1.2%     | 50%      |

Survivorship bias applies (today's index members). Not investment advice.
