# Volume around the turn, backtested (2016-2026)

Hypothesis: when a decline starts to stop and the turn comes on relatively high volume, the odds of a reversal are better than on a quiet turn. Tested on the three rules with ten-year event tables, train (before 2023-01-01) and test (from 2023-01-01) separately. Entry at the next open, 10 bps cost, excess measured over random entries in the same stock within half a year of the signal (``xloc``), which cancels the stock's drift and the regime around the signal.

Volume features are point-in-time at the signal bar and the averages end the bar before, so the signal day is never compared with itself: the signal-day ratio (volume / prior 20-day average), the 5-day ratio (last five bars / prior 20-day average), a climax day (>= 3x the prior 60-day average) within the last 10 bars, the ratio on the day of the lowest close of the last 20 bars, and the share of the last 10 bars' volume that came on up days.

A condition **helps** when the yes rows beat the no rows in excess return in **both** periods by at least 0.5% over 20 bars with at least 30 events on each side; it **hurts** when the no rows beat the yes rows by the same margin in both periods; everything else is noise however good one period looks. Survivorship bias applies (today's index members).

## Beaten-down falling-wedge breakout (hold 20 bars)

3192 events, 506 stocks, 2016-11-01 to 2026-10-08; volume context available for 3192 of them.

### Conditions

| condition | train: yes n / excess / hit vs no n / excess / hit (20) | test: the same (20) | yes - no train / test (20) | yes - no train / test (60) | years positive | verdict |
|---|---|---|---|---|---|---|
| signal-day volume >= 1.5x the prior 20-day average | 219 / +0.95% / 53% vs 1517 / +2.56% / 66% | 197 / +0.78% / 54% vs 1208 / +0.69% / 57% | -1.60% / +0.09% | -1.96% / -0.51% | 3/10 | noise |
| signal-day volume >= 2.5x the prior 20-day average | 37 / +1.64% / 51% vs 1699 / +2.37% / 64% | 32 / +0.35% / 59% vs 1373 / +0.71% / 57% | -0.73% / -0.36% | -4.47% / -1.27% | 3/7 | noise |
| signal-day volume >= 5x the prior 20-day average | 5 / +8.40% / 80% vs 1731 / +2.34% / 64% | 2 / -0.97% / 50% vs 1403 / +0.70% / 57% | +6.07% / -1.67% | +3.10% / +24.20% | 0/0 | noise |
| 5-day volume >= 1.3x the prior 20-day average (expanding into the turn) | 217 / +2.24% / 63% vs 1519 / +2.37% / 64% | 190 / +0.50% / 59% vs 1215 / +0.73% / 56% | -0.12% / -0.23% | -0.47% / -1.28% | 6/10 | noise |
| a >= 3x (60-day average) volume day within the last 10 bars (climax) | 99 / +3.09% / 66% vs 1637 / +2.31% / 64% | 98 / +1.17% / 61% vs 1307 / +0.67% / 56% | +0.78% / +0.51% | -1.44% / +3.15% | 6/10 | **helps (consistent)** |
| volume on the 20-bar low-close day >= 2x its prior 20-day average (capitulation at the low) | 77 / +2.19% / 61% vs 1659 / +2.36% / 64% | 88 / +1.53% / 60% vs 1317 / +0.65% / 56% | -0.17% / +0.88% | -1.56% / +1.57% | 7/10 | noise |
| >= 60% of the last 10 bars' volume on up days (accumulation) | 505 / +1.95% / 60% vs 1231 / +2.52% / 66% | 407 / +0.80% / 58% vs 998 / +0.66% / 56% | -0.57% / +0.14% | +0.57% / -0.53% | 4/10 | noise |

### Signal-day volume (vs the prior 20-day average)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| < 0.8x | train | 550 | +3.37% | 70% | +3.03% |
| 0.8-1.2x | train | 727 | +2.59% | 64% | +2.34% |
| 1.2-2x | train | 376 | +2.10% | 59% | +1.66% |
| 2-3x | train | 65 | +0.91% | 49% | +1.07% |
| > 3x | train | 15 | +1.55% | 60% | +2.21% |
| < 0.8x | test | 393 | +1.31% | 54% | +0.32% |
| 0.8-1.2x | test | 611 | +1.52% | 58% | +0.80% |
| 1.2-2x | test | 323 | +1.60% | 58% | +1.11% |
| 2-3x | test | 61 | +0.75% | 54% | +0.26% |
| > 3x | test | 17 | -0.87% | 59% | -0.28% |

### Largest volume day of the last 10 bars (vs the prior 60-day average)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| < 1.5x | train | 864 | +2.98% | 65% | +2.56% |
| 1.5-3x | train | 766 | +2.19% | 62% | +2.01% |
| 3-5x | train | 77 | +3.93% | 68% | +3.75% |
| > 5x | train | 22 | +1.22% | 59% | +0.77% |
| < 1.5x | test | 646 | +0.64% | 52% | -0.42% |
| 1.5-3x | test | 661 | +2.21% | 61% | +1.73% |
| 3-5x | test | 76 | +1.92% | 63% | +2.04% |
| > 5x | test | 22 | -1.23% | 55% | -1.84% |

## News-day in a beaten-down stock, long (hold 60 bars)

1084 events, 367 stocks, 2017-10-20 to 2026-07-15; volume context available for 1083 of them.

### Conditions

| condition | train: yes n / excess / hit vs no n / excess / hit (20) | test: the same (20) | yes - no train / test (20) | yes - no train / test (60) | years positive | verdict |
|---|---|---|---|---|---|---|
| signal-day volume >= 5x the prior 20-day average | 224 / +3.50% / 65% vs 380 / +3.04% / 58% | 194 / +2.68% / 62% vs 286 / +3.34% / 56% | +0.46% / -0.66% | +1.69% / -1.81% | 5/10 | noise |
| 5-day volume >= 1.3x the prior 20-day average (expanding into the turn) | 585 / +3.10% / 60% vs 19 / +6.65% / 63% | 461 / +2.85% / 58% vs 19 / +8.58% / 68% | -3.56% / -5.73% | -1.41% / -18.89% | 0/3 | noise |
| a >= 3x (60-day average) volume day within the last 10 bars (climax) | 530 / +3.24% / 59% vs 74 / +3.01% / 69% | 428 / +2.93% / 58% vs 52 / +4.32% / 63% | +0.23% / -1.39% | +5.82% / -17.70% | 4/9 | noise |
| volume on the 20-bar low-close day >= 2x its prior 20-day average (capitulation at the low) | 417 / +2.63% / 59% vs 187 / +4.50% / 64% | 373 / +2.65% / 58% vs 107 / +4.57% / 60% | -1.88% / -1.92% | -1.25% / -9.82% | 3/10 | **hurts (consistent)** |
| >= 60% of the last 10 bars' volume on up days (accumulation) | 88 / +3.64% / 60% vs 516 / +3.13% / 60% | 51 / +6.06% / 55% vs 429 / +2.72% / 59% | +0.51% / +3.34% | -3.66% / +14.45% | 4/8 | **helps (consistent)** |

### Signal-day volume (vs the prior 20-day average)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| 3-5x | train | 379 | +2.25% | 58% | +3.02% |
| 5-8x | train | 147 | +2.84% | 63% | +3.27% |
| > 8x | train | 77 | +4.73% | 69% | +3.94% |
| 3-5x | test | 286 | +2.71% | 56% | +3.34% |
| 5-8x | test | 134 | +1.67% | 59% | +2.12% |
| > 8x | test | 60 | +4.57% | 68% | +3.92% |

### Largest volume day of the last 10 bars (vs the prior 60-day average)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| < 1.5x | train | 4 | -3.60% | 50% | -4.07% |
| 1.5-3x | train | 70 | +3.10% | 70% | +3.41% |
| 3-5x | train | 311 | +1.33% | 53% | +2.06% |
| > 5x | train | 219 | +4.67% | 68% | +4.91% |
| < 1.5x | test | 1 | +8.62% | 100% | +7.27% |
| 1.5-3x | test | 51 | +3.78% | 63% | +4.26% |
| 3-5x | test | 237 | +2.86% | 55% | +3.39% |
| > 5x | test | 191 | +2.06% | 61% | +2.35% |

## Early rally in a beaten-down stock (hold 20 bars)

5425 events, 507 stocks, 2017-10-20 to 2026-07-14; volume context available for 5425 of them.

### Conditions

| condition | train: yes n / excess / hit vs no n / excess / hit (20) | test: the same (20) | yes - no train / test (20) | yes - no train / test (60) | years positive | verdict |
|---|---|---|---|---|---|---|
| signal-day volume >= 1.5x the prior 20-day average | 422 / +2.73% / 58% vs 2910 / +4.13% / 61% | 329 / +3.68% / 58% vs 1764 / +3.63% / 59% | -1.40% / +0.05% | -1.40% / +0.21% | 3/10 | noise |
| signal-day volume >= 2.5x the prior 20-day average | 90 / +4.80% / 54% vs 3242 / +3.93% / 61% | 72 / +3.40% / 57% vs 2021 / +3.65% / 59% | +0.88% / -0.24% | +1.40% / +4.93% | 5/9 | noise |
| signal-day volume >= 5x the prior 20-day average | 9 / +5.01% / 67% vs 3323 / +3.95% / 61% | 5 / +18.42% / 80% vs 2088 / +3.60% / 58% | +1.06% / +14.81% | +3.33% / +87.89% | 0/0 | noise |
| 5-day volume >= 1.3x the prior 20-day average (expanding into the turn) | 297 / +2.88% / 58% vs 3035 / +4.05% / 61% | 233 / +3.19% / 55% vs 1860 / +3.69% / 59% | -1.17% / -0.50% | +1.11% / +2.48% | 4/10 | **hurts (consistent)** |
| a >= 3x (60-day average) volume day within the last 10 bars (climax) | 242 / +3.67% / 60% vs 3090 / +3.97% / 61% | 183 / +4.02% / 60% vs 1910 / +3.60% / 58% | -0.30% / +0.42% | +2.72% / +1.67% | 6/10 | noise |
| volume on the 20-bar low-close day >= 2x its prior 20-day average (capitulation at the low) | 233 / +3.16% / 54% vs 3099 / +4.01% / 62% | 234 / +4.08% / 60% vs 1859 / +3.58% / 58% | -0.85% / +0.50% | -0.41% / -0.29% | 2/9 | noise |
| >= 60% of the last 10 bars' volume on up days (accumulation) | 1536 / +3.73% / 59% vs 1796 / +4.14% / 62% | 1012 / +3.04% / 56% vs 1081 / +4.20% / 61% | -0.41% / -1.16% | -0.74% / -1.17% | 2/10 | noise |

### Signal-day volume (vs the prior 20-day average)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| < 0.8x | train | 1095 | +2.85% | 62% | +3.97% |
| 0.8-1.2x | train | 1374 | +3.11% | 62% | +4.23% |
| 1.2-2x | train | 696 | +2.29% | 58% | +3.48% |
| 2-3x | train | 116 | +1.29% | 59% | +2.82% |
| > 3x | train | 50 | +3.24% | 56% | +5.48% |
| < 0.8x | test | 568 | +2.58% | 58% | +3.87% |
| 0.8-1.2x | test | 883 | +2.34% | 59% | +3.80% |
| 1.2-2x | test | 494 | +1.92% | 58% | +3.10% |
| 2-3x | test | 110 | +2.20% | 60% | +3.38% |
| > 3x | test | 38 | +2.22% | 55% | +4.09% |

### Largest volume day of the last 10 bars (vs the prior 60-day average)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| < 1.5x | train | 1555 | +2.51% | 59% | +3.66% |
| 1.5-3x | train | 1535 | +3.11% | 63% | +4.29% |
| 3-5x | train | 195 | +3.22% | 63% | +4.12% |
| > 5x | train | 47 | -0.21% | 47% | +1.81% |
| < 1.5x | test | 858 | +2.14% | 58% | +3.50% |
| 1.5-3x | test | 1052 | +2.41% | 59% | +3.68% |
| 3-5x | test | 148 | +2.88% | 63% | +4.53% |
| > 5x | test | 35 | +0.14% | 46% | +1.88% |

## Verdicts

- **Beaten-down falling-wedge breakout (hold 20 bars)**: *a >= 3x (60-day average) volume day within the last 10 bars (climax)* helps (+0.78% train, +0.51% test at 20 bars; -1.44% / +3.15% at 60).
- **News-day in a beaten-down stock, long (hold 60 bars)**: *volume on the 20-bar low-close day >= 2x its prior 20-day average (capitulation at the low)* hurts (-1.88% train, -1.92% test at 20 bars; -1.25% / -9.82% at 60).
- **News-day in a beaten-down stock, long (hold 60 bars)**: *>= 60% of the last 10 bars' volume on up days (accumulation)* helps (+0.51% train, +3.34% test at 20 bars; -3.66% / +14.45% at 60).
- **Early rally in a beaten-down stock (hold 20 bars)**: *5-day volume >= 1.3x the prior 20-day average (expanding into the turn)* hurts (-1.17% train, -0.50% test at 20 bars; +1.11% / +2.48% at 60).

## Reading

Only a condition marked **helps** or **hurts** in a family is a candidate for that family's rule, and only as stated. The bucket tables show whether the effect is monotonic (more volume, more edge) or a threshold; a condition that passes while its buckets wander is weaker than one whose buckets line up. A volume feature that passes in one family and fails in another stays confined to the family where it passed.

Systematic screens and an event study on today's index members (survivorship bias), not investment advice.
