# Can the setups be trusted? - AlgoVision research report

Generated 2026-09-03T06:10:16. Universe: **all (S&P 500 + NASDAQ-100)** (518 symbols, 514 with events), period 10y, daily bars, benchmark SPY. Detector config: min_score=0.6.

## Method


* Every **confirmed** pattern is one event. The signal bar is the later of the breakout bar and the bar at which
  the last swing point of the structure became knowable (`pivot + order`), so nothing from the future is used to
  decide the shape. Entry is the **next bar's open**.
* Returns are **signed by the pattern's direction** (a bearish pattern "wins" when price falls) and measured over
  5/10/20/40/60 bars, close-to-entry.
* Three baselines: raw, **minus SPY** over the same window, and **minus random-date entries in the same stock and
  direction** (20 draws per event). The random-date baseline cancels each stock's drift and the survivorship bias
  of using today's index members, so it is the number to trust.
* A fourth, stricter baseline, **local random entries** (`xloc`): random dates within +-126 bars of the signal in the
  same stock and direction. This also cancels the *regime* around the signal (bear patterns cluster in bear phases),
  so it is the number the verdicts are based on.
* `p` / `p_loc` are one-sided permutation p-values: the share of "no-skill" replicates (one random date per event)
  whose mean return is at least as good as the pattern's. CIs are 95% bootstrap intervals of the mean excess return.
* Trade simulation: enter at next open, exit at the measured-move **target** or the pattern **stop** (whichever is
  touched first; stop wins ties) or after 60 bars. R = result / initial risk. Profit factor = gross wins / gross losses in R.
* **Walk-forward validation**: on a random subsample the detectors were re-run bar by bar seeing only past data;
  its events are compared with the fast hindsight method to quantify look-ahead bias.

## Headline numbers (20-bar horizon)

* Events: **48426** across 514 symbols; 16 pattern types.
* Mean 20-bar return in the pattern's direction: **-0.20%** (hit rate 49.7%, random-date hit rate 50.2%).
* Excess over SPY: **-0.12%**; excess over random-date entries: **-0.30%** (95% CI -0.39% to -0.21%, permutation p = 1.000).
* Excess over **local** random entries (same stock, +-6 months): **-0.31%** (95% CI -0.40% to -0.21%, p = 1.000; local random hit rate 49.8%).
* Trade simulation: target hit first 29.4%, stop hit first 56.3%, average R = +0.02, profit factor 1.03, average reward:risk 3.52.

## Per-pattern results

| pattern                    |     n |   n_symbols | hit_20   | rand_hit_20   | ret_20   | xspy_20   | xrand_20   |   p_20 | xloc_20   | xloc_lo_20   | xloc_hi_20   |   ploc_20 | target_rate   | stop_rate   |   avg_r |   profit_factor | verdict                                          |
|:---------------------------|------:|------------:|:---------|:--------------|:---------|:----------|:-----------|-------:|:----------|:-------------|:-------------|----------:|:--------------|:------------|--------:|----------------:|:-------------------------------------------------|
| Ascending Triangle         |  3163 |         509 | 57.2%    | 57.4%         | +1.09%   | +0.03%    | -0.23%     |  0.938 | -0.59%    | -0.89%       | -0.29%       |     1     | 30.7%         | 56.8%       |    0.2  |            1.36 | worse than random                                |
| Bear Flag                  |  4742 |         510 | 38.3%    | 43.2%         | -3.42%   | -1.43%    | -1.77%     |  1     | -2.85%    | -3.23%       | -2.45%       |     1     | 8.0%          | 84.1%       |   -0.41 |            0.51 | worse than random                                |
| Bull Flag                  |  7707 |         514 | 54.6%    | 56.8%         | +1.19%   | +0.21%    | -0.53%     |  1     | -1.01%    | -1.26%       | -0.76%       |     1     | 22.1%         | 67.8%       |    0.27 |            1.4  | worse than random                                |
| Cup and Handle             |  1224 |         474 | 52.9%    | 56.8%         | +0.30%   | -0.18%    | -1.02%     |  1     | -1.32%    | -1.80%       | -0.83%       |     1     | 16.7%         | 58.5%       |    0.17 |            1.29 | worse than random                                |
| Descending Triangle        |  1644 |         492 | 42.3%    | 43.3%         | -1.88%   | -0.27%    | -0.62%     |  0.997 | -1.15%    | -1.64%       | -0.70%       |     1     | 20.3%         | 69.4%       |   -0.25 |            0.64 | worse than random                                |
| Double Bottom              |  5597 |         513 | 56.6%    | 57.0%         | +1.19%   | +0.14%    | -0.27%     |  0.984 | +0.35%    | +0.08%       | +0.60%       |     0.002 | 57.6%         | 24.7%       |    0.1  |            1.35 | edge vs random (statistically significant)       |
| Double Top                 |  6109 |         513 | 40.4%    | 42.4%         | -1.93%   | -0.56%    | -0.46%     |  1     | -0.20%    | -0.49%       | +0.07%       |     0.962 | 43.1%         | 40.5%       |   -0.19 |            0.58 | no detectable edge                               |
| Falling Wedge              |  3183 |         508 | 61.5%    | 56.7%         | +2.24%   | +0.46%    | +0.89%     |  0     | +1.63%    | +1.29%       | +1.96%       |     0     | 31.8%         | 49.0%       |    0.39 |            1.79 | edge vs random (statistically significant)       |
| Head and Shoulders         |  1782 |         490 | 42.2%    | 42.4%         | -1.84%   | -0.23%    | -0.37%     |  0.954 | +0.05%    | -0.45%       | +0.55%       |     0.405 | 24.7%         | 58.5%       |   -0.26 |            0.58 | no detectable edge                               |
| Inverse Head and Shoulders |  1728 |         487 | 58.2%    | 57.0%         | +1.47%   | +0.34%    | +0.06%     |  0.398 | +0.92%    | +0.50%       | +1.34%       |     0     | 38.7%         | 42.3%       |    0.21 |            1.48 | edge vs random (statistically significant)       |
| Inverted Cup and Handle    |   564 |         340 | 38.8%    | 43.0%         | -1.41%   | +0.07%    | -0.10%     |  0.614 | -0.83%    | -1.78%       | +0.05%       |     0.996 | 15.1%         | 69.9%       |   -0.28 |            0.6  | no detectable edge                               |
| Rectangle                  |  1337 |         484 | 52.0%    | 51.6%         | +0.23%   | -0.01%    | -0.20%     |  0.792 | -0.47%    | -0.97%       | +0.06%       |     0.982 | 56.2%         | 32.8%       |    0.04 |            1.1  | no detectable edge                               |
| Rising Wedge               |  5611 |         511 | 45.7%    | 41.9%         | -0.89%   | -0.01%    | +0.50%     |  0     | +0.92%    | +0.70%       | +1.16%       |     0     | 17.5%         | 66.6%       |   -0.15 |            0.78 | edge vs random (statistically significant)       |
| Symmetrical Triangle       |  3678 |         505 | 51.9%    | 51.1%         | +0.25%   | +0.17%    | +0.02%     |  0.428 | -0.15%    | -0.44%       | +0.16%       |     0.865 | 19.5%         | 68.9%       |    0.2  |            1.32 | weak / unproven (positive R but not significant) |
| Triple Bottom              |   143 |         128 | 55.9%    | 57.1%         | +1.42%   | +0.49%    | +0.07%     |  0.45  | +1.39%    | -0.16%       | +2.93%       |     0.011 | 51.0%         | 21.0%       |    0.13 |            1.51 | weak / unproven (positive R but not significant) |
| Triple Top                 |   214 |         179 | 42.7%    | 42.0%         | -0.08%   | +1.12%    | +1.35%     |  0.007 | +1.18%    | -0.34%       | +2.87%       |     0.008 | 35.0%         | 32.2%       |   -0.2  |            0.51 | no detectable edge                               |
| ALL                        | 48426 |         514 | 49.7%    | 50.2%         | -0.20%   | -0.12%    | -0.30%     |  1     | -0.31%    | -0.40%       | -0.21%       |     1     | 29.4%         | 56.3%       |    0.02 |            1.03 | worse than random                                |

## Across horizons (all patterns pooled)

|   horizon |     n | hit   | rand_hit   | ret    | xspy   | xrand   | ci_lo   | ci_hi   |   p | xloc   |   p_loc |
|----------:|------:|:------|:-----------|:-------|:-------|:--------|:--------|:--------|----:|:-------|--------:|
|         5 | 48330 | 50.0% | 50.3%      | -0.06% | -0.02% | -0.08%  | -0.1%   | -0.0%   |   1 | -0.10% |       1 |
|        10 | 48242 | 49.8% | 50.3%      | -0.08% | -0.06% | -0.14%  | -0.2%   | -0.1%   |   1 | -0.16% |       1 |
|        20 | 48057 | 49.7% | 50.2%      | -0.20% | -0.12% | -0.30%  | -0.4%   | -0.2%   |   1 | -0.31% |       1 |
|        40 | 47587 | 48.8% | 49.9%      | -0.58% | -0.23% | -0.83%  | -1.0%   | -0.7%   |   1 | -0.77% |       1 |
|        60 | 47133 | 48.9% | 49.5%      | -0.65% | -0.34% | -1.00%  | -1.2%   | -0.8%   |   1 | -1.01% |       1 |

## By direction

| direction   |     n | ret    | xspy   | xrand   | hit   | target_rate   | stop_rate   |   avg_r | xloc   |
|:------------|------:|:-------|:-------|:--------|:------|:--------------|:------------|--------:|:-------|
| bearish     | 22546 | -1.93% | -0.50% | -0.48%  | 41.5% | 23.7%         | 63.2%       |   -0.25 | -0.59% |
| bullish     | 25511 | +1.34% | +0.21% | -0.15%  | 57.0% | 34.9%         | 50.6%       |    0.25 | -0.06% |

## Score calibration (Spearman rho between score and excess return = -0.014, p = 0.003)

|   score_min |    n |   score_max | ret    | xrand   | hit   | target_rate   |   avg_r |
|------------:|-----:|------------:|:-------|:--------|:------|:--------------|--------:|
|    0.600003 | 9612 |        0.64 | -0.18% | -0.26%  | 49.9% | 32.1%         |    0.01 |
|    0.63878  | 9611 |        0.68 | -0.16% | -0.27%  | 50.3% | 31.3%         |    0.03 |
|    0.677718 | 9611 |        0.72 | -0.21% | -0.32%  | 50.0% | 28.7%         |    0.01 |
|    0.720177 | 9611 |        0.78 | -0.16% | -0.27%  | 49.1% | 27.3%         |    0.01 |
|    0.775839 | 9612 |        1    | -0.27% | -0.38%  | 49.5% | 28.7%         |    0.02 |

## Raising the scanner threshold

|   min_score |     n | hit   | ret    | xrand   | xloc   | target_rate   |   avg_r |
|------------:|------:|:------|:-------|:--------|:-------|:--------------|--------:|
|         0.6 | 48057 | 49.7% | -0.20% | -0.30%  | -0.31% | 29.6%         |    0.02 |
|         0.7 | 23603 | 49.5% | -0.21% | -0.33%  | -0.43% | 28.1%         |    0.02 |
|         0.8 |  6595 | 49.3% | -0.33% | -0.40%  | -0.58% | 28.6%         |    0.01 |
|         0.9 |   852 | 46.1% | -0.90% | -0.89%  | -0.76% | 35.4%         |   -0.01 |

## Conditional view per pattern (excess 20-bar return over local random entries; blank = fewer than 100 events)

| pattern                    | xrand_all   | xrand vol>=1.5x   | xrand vol<1.5x   | xrand same-bar   | xrand delayed   | xrand extended>3%   | xrand near level   |    n |   years |   years_positive |
|:---------------------------|:------------|:------------------|:-----------------|:-----------------|:----------------|:--------------------|:-------------------|-----:|--------:|-----------------:|
| Ascending Triangle         | -0.59%      | -0.26%            | -0.73%           | -0.62%           | -0.56%          | +0.02%              | -0.74%             | 3146 |      10 |                2 |
| Bear Flag                  | -2.85%      | -0.62%            | -3.24%           | -2.85%           |                 | -3.82%              | -2.45%             | 4703 |      11 |                2 |
| Bull Flag                  | -1.01%      | -0.70%            | -1.06%           | -1.01%           |                 | +0.08%              | -1.29%             | 7620 |      11 |                2 |
| Cup and Handle             | -1.32%      | -1.33%            | -1.31%           | -1.27%           | -1.62%          | -1.34%              | -1.31%             | 1215 |      10 |                3 |
| Descending Triangle        | -1.15%      | -0.68%            | -1.46%           | -1.08%           | -1.23%          | -0.88%              | -1.23%             | 1631 |      11 |                1 |
| Double Bottom              | +0.35%      | +0.12%            | +0.53%           | +0.29%           | +0.67%          | +0.39%              | +0.34%             | 5567 |      11 |                7 |
| Double Top                 | -0.20%      | -0.08%            | -0.34%           | -0.25%           | -0.00%          | -0.21%              | -0.19%             | 6065 |      11 |                3 |
| Falling Wedge              | +1.63%      | +1.96%            | +1.54%           | +1.33%           | +1.81%          | +1.99%              | +1.47%             | 3165 |      11 |                9 |
| Head and Shoulders         | +0.05%      | -0.05%            | +0.12%           | +0.24%           | -0.30%          | +0.40%              | -0.08%             | 1760 |      10 |                5 |
| Inverse Head and Shoulders | +0.92%      | +0.71%            | +1.03%           | +0.84%           | +1.11%          | +1.16%              | +0.86%             | 1717 |      10 |                9 |
| Inverted Cup and Handle    | -0.83%      | -0.90%            | -0.79%           | -1.08%           | +0.29%          |                     | -1.51%             |  562 |       9 |                2 |
| Rectangle                  | -0.47%      | -0.58%            | -0.38%           | -0.39%           | -0.84%          | -0.65%              | -0.43%             | 1326 |      10 |                2 |
| Rising Wedge               | +0.92%      | +0.95%            | +0.91%           | +0.96%           | +0.90%          | +0.88%              | +0.94%             | 5574 |      11 |                9 |
| Symmetrical Triangle       | -0.15%      | -0.42%            | -0.06%           | +0.13%           | -0.27%          | +0.04%              | -0.21%             | 3650 |      11 |                5 |
| Triple Bottom              | +1.39%      |                   |                  | +1.32%           |                 |                     | +1.55%             |  143 |       0 |                0 |
| Triple Top                 | +1.18%      | +1.34%            |                  | +0.96%           |                 |                     | +1.43%             |  213 |       2 |                0 |

## Breakout volume

| volume_bucket   |     n | ret    | xspy   | xrand   | hit   | target_rate   | stop_rate   |   avg_r | xloc   |
|:----------------|------:|:-------|:-------|:--------|:------|:--------------|:------------|--------:|:-------|
| <0.8x           |  9008 | -0.40% | -0.18% | -0.72%  | 50.1% | 19.1%         | 69.8%       |    0.06 | -0.94% |
| 0.8-1.1x        | 10393 | -0.18% | -0.17% | -0.46%  | 49.7% | 23.7%         | 62.8%       |    0.03 | -0.52% |
| 1.1-1.5x        | 13280 | -0.10% | -0.12% | -0.15%  | 50.0% | 30.6%         | 55.1%       |    0.03 | -0.10% |
| 1.5-2.5x        | 11056 | -0.17% | -0.08% | -0.08%  | 49.0% | 35.7%         | 49.8%       |   -0.03 | +0.00% |
| >2.5x           |  4301 | -0.16% | -0.01% | -0.08%  | 50.3% | 47.3%         | 34.9%       |   -0.02 | +0.06% |

## By year

|   year |    n | ret    | xspy   | xrand   | hit   | target_rate   | stop_rate   |   avg_r | xloc   |
|-------:|-----:|:-------|:-------|:--------|:------|:--------------|:------------|--------:|:-------|
|   2016 |  705 | +0.27% | -0.31% | -0.13%  | 51.9% | 35.7%         | 52.2%       |    0.11 | +0.04% |
|   2017 | 4001 | +0.10% | -0.06% | -0.14%  | 51.8% | 33.0%         | 54.0%       |    0.16 | -0.13% |
|   2018 | 4548 | -0.75% | -0.30% | -0.74%  | 46.7% | 28.0%         | 56.1%       |   -0.05 | -0.71% |
|   2019 | 4802 | -0.12% | -0.29% | -0.36%  | 52.4% | 27.6%         | 56.7%       |    0.08 | -0.19% |
|   2020 | 5077 | +0.29% | -0.03% | +0.22%  | 50.4% | 31.7%         | 57.2%       |    0.09 | +0.15% |
|   2021 | 4779 | -0.42% | -0.28% | -0.60%  | 50.0% | 29.6%         | 57.0%       |    0    | -0.67% |
|   2022 | 5638 | -0.64% | -0.27% | -0.47%  | 47.9% | 26.4%         | 59.4%       |   -0.17 | -0.77% |
|   2023 | 5303 | +0.08% | +0.12% | -0.08%  | 50.8% | 29.5%         | 55.4%       |    0.05 | +0.04% |
|   2024 | 4843 | -0.23% | -0.02% | -0.43%  | 49.4% | 30.5%         | 56.7%       |    0.04 | -0.39% |
|   2025 | 5103 | -0.14% | -0.05% | -0.19%  | 49.3% | 30.6%         | 56.6%       |    0.06 | -0.19% |
|   2026 | 3258 | -0.14% | +0.04% | -0.25%  | 48.3% | 29.2%         | 55.7%       |   -0.07 | -0.27% |

## By pivot scale

|   scale |     n | ret    | xspy   | xrand   | hit   | target_rate   | stop_rate   |   avg_r | xloc   |
|--------:|------:|:-------|:-------|:--------|:------|:--------------|:------------|--------:|:-------|
|       3 | 33332 | -0.26% | -0.21% | -0.44%  | 49.6% | 29.1%         | 61.7%       |    0.02 | -0.61% |
|       5 |  7505 | -0.03% | +0.01% | +0.05%  | 50.5% | 34.2%         | 48.5%       |    0.01 | +0.34% |
|       8 |  4550 | +0.17% | +0.26% | +0.20%  | 50.5% | 29.7%         | 42.9%       |    0.02 | +0.67% |
|      13 |  2670 | -0.42% | -0.02% | -0.34%  | 48.8% | 23.7%         | 37.7%       |   -0.03 | +0.00% |

## Forming setups: once the shape is complete, does it confirm?

`failed` means price broke the *opposite* way (or invalidated the shape) before confirming. Flags, cups, rectangles and symmetrical triangles have no failure rule in the detectors - they are only recorded once they break out - so their 100% is by construction, not evidence.

| pattern                    |     n |   confirmed |   failed |   expired | confirm_rate   | fail_rate   | expire_rate   |
|:---------------------------|------:|------------:|---------:|----------:|:---------------|:------------|:--------------|
| Ascending Triangle         |  4412 |        3072 |     1340 |         0 | 69.6%          | 30.4%       | +0.00%        |
| Bear Flag                  |  4566 |        4566 |        0 |         0 | 100.0%         | 0.0%        | +0.00%        |
| Bull Flag                  |  7440 |        7440 |        0 |         0 | 100.0%         | 0.0%        | +0.00%        |
| Cup and Handle             |  1198 |        1198 |        0 |         0 | 100.0%         | 0.0%        | +0.00%        |
| Descending Triangle        |  2827 |        1589 |     1238 |         0 | 56.2%          | 43.8%       | +0.00%        |
| Double Bottom              |  5841 |        5354 |      487 |         0 | 91.7%          | 8.3%        | +0.00%        |
| Double Top                 |  7081 |        5880 |     1199 |         2 | 83.0%          | 16.9%       | +0.03%        |
| Falling Wedge              |  3175 |        3095 |       80 |         0 | 97.5%          | 2.5%        | +0.00%        |
| Head and Shoulders         |  1922 |        1729 |      192 |         1 | 90.0%          | 10.0%       | +0.05%        |
| Inverse Head and Shoulders |  1750 |        1684 |       62 |         4 | 96.2%          | 3.5%        | +0.23%        |
| Inverted Cup and Handle    |   558 |         558 |        0 |         0 | 100.0%         | 0.0%        | +0.00%        |
| Rectangle                  |  1308 |        1308 |        0 |         0 | 100.0%         | 0.0%        | +0.00%        |
| Rising Wedge               |  5707 |        5461 |      246 |         0 | 95.7%          | 4.3%        | +0.00%        |
| Symmetrical Triangle       |  3587 |        3587 |        0 |         0 | 100.0%         | 0.0%        | +0.00%        |
| Triple Bottom              |   160 |         140 |       20 |         0 | 87.5%          | 12.5%       | +0.00%        |
| Triple Top                 |   270 |         206 |       64 |         0 | 76.3%          | 23.7%       | +0.00%        |
| ALL                        | 51802 |       46867 |     4928 |         7 | 90.5%          | 9.5%        | +0.01%        |

## Look-ahead check: walk-forward vs hindsight

Sample: 80 symbols, last 1000 bars each, detection window 400 bars, step 1.

* Hindsight events in that range: 3347; walk-forward events: 4106; hindsight events also found point-in-time (within 3 bars): 2827 (84%).
* 20-bar mean return: hindsight -0.12% vs walk-forward +0.04%; hit rate 49.0% vs 49.7%; excess over random -0.22% vs -0.02%; excess over local random -0.22% vs +0.00%.
* Target-first rate: 29.3% vs 27.9%; average R: +0.02 vs +0.03.

Walk-forward per pattern:

| pattern                    |    n | hit_20   | rand_hit_20   | ret_20   | xrand_20   |   p_20 | target_rate   | stop_rate   |   avg_r |
|:---------------------------|-----:|:---------|:--------------|:---------|:-----------|-------:|:--------------|:------------|--------:|
| Ascending Triangle         |  244 | 55.2%    | 56.8%         | +1.42%   | +0.01%     |  0.48  | 30.3%         | 54.5%       |    0.08 |
| Bear Flag                  |  461 | 44.4%    | 43.7%         | -2.37%   | -0.77%     |  0.909 | 9.8%          | 82.4%       |   -0.29 |
| Bull Flag                  |  657 | 53.8%    | 54.4%         | +2.00%   | +0.11%     |  0.397 | 23.4%         | 68.2%       |    0.27 |
| Cup and Handle             |   88 | 53.5%    | 57.4%         | +1.27%   | -0.61%     |  0.725 | 23.9%         | 48.9%       |    0.23 |
| Descending Triangle        |  154 | 39.6%    | 44.1%         | -1.84%   | -0.53%     |  0.744 | 19.5%         | 72.7%       |   -0.31 |
| Double Bottom              |  407 | 51.7%    | 56.2%         | +1.03%   | -0.50%     |  0.815 | 59.7%         | 25.6%       |    0.07 |
| Double Top                 |  450 | 40.9%    | 42.6%         | -1.88%   | -0.38%     |  0.781 | 44.0%         | 39.1%       |   -0.17 |
| Falling Wedge              |  336 | 60.7%    | 55.5%         | +2.41%   | +1.12%     |  0.021 | 30.4%         | 51.2%       |    0.56 |
| Head and Shoulders         |  173 | 47.0%    | 39.2%         | -1.89%   | +0.04%     |  0.468 | 19.7%         | 57.8%       |   -0.23 |
| Inverse Head and Shoulders |  128 | 57.1%    | 56.3%         | +2.36%   | +0.83%     |  0.167 | 40.6%         | 37.5%       |    0.24 |
| Inverted Cup and Handle    |   52 | 28.8%    | 41.4%         | -4.74%   | -3.03%     |  0.983 | 5.8%          | 76.9%       |   -0.61 |
| Rectangle                  |   81 | 54.4%    | 51.0%         | +0.53%   | +0.14%     |  0.431 | 56.8%         | 29.6%       |    0.01 |
| Rising Wedge               |  489 | 47.9%    | 42.0%         | -0.88%   | +0.60%     |  0.079 | 15.1%         | 63.0%       |   -0.09 |
| Symmetrical Triangle       |  360 | 50.4%    | 48.9%         | +0.18%   | +0.22%     |  0.326 | 16.4%         | 71.1%       |    0.04 |
| Triple Bottom              |   11 | 54.5%    | 55.5%         | +1.72%   | -0.09%     |  0.507 | 81.8%         | 9.1%        |    0.23 |
| Triple Top                 |   15 | 33.3%    | 41.3%         | -2.14%   | -0.46%     |  0.584 | 13.3%         | 26.7%       |   -0.31 |
| ALL                        | 4106 | 49.7%    | 49.2%         | +0.04%   | -0.02%     |  0.52  | 27.9%         | 57.2%       |    0.03 |

## Caveats


* Universe = today's index members (survivorship bias). The random-date baseline in the same stock is the control
  for this; the raw and SPY-adjusted numbers are inflated by it.
* No transaction costs, slippage or position sizing; overnight gap from signal close to next open is included.
* Events overlap in time and across correlated stocks, so effective sample sizes are smaller than `n` and
  p-values are optimistic. Treat borderline significance as noise.
* Many comparisons are made (patterns x horizons); with ~16 patterns, expect roughly one spurious "significant"
  result at p<0.05 by chance.
* Score is a geometric-fit measure. Calibration tells you whether it also predicts outcomes.
