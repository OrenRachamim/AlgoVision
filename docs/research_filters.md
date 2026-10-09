# Filters from the forward test, backtested (2016-2026)

The first five weeks of the daily reports (2026-09-05 to 2026-10-08) suggested a few filters: a regime gate on the beaten-down basket, two of the flags (an unusual drop against peers, a decline deeper than 40% from the 52-week high), a preference for declines the market dragged, and that forming wedges are not a signal. Five weeks and one regime prove nothing, so each candidate is tested here on the three rules with ten-year event tables, train (before 2023-01-01) and test (from 2023-01-01) separately. Entry at the next open, 10 bps cost, excess measured over random entries in the same stock within half a year of the signal (``xloc``), which cancels the stock's drift and the regime around the signal.

A condition **helps** when the yes rows beat the no rows in excess return in **both** periods by at least 0.5% over 20 bars with at least 30 events on each side; it **hurts** when the no rows beat the yes rows by the same margin in both periods; everything else is noise however good one period looks. Conditions are point-in-time at the signal bar: the basket and the breadth use membership fixed 20 bars earlier; the sector proxies stand in for the correlation peer groups of the reports, which have no ten-year history.

## Beaten-down falling-wedge breakout (hold 20 bars)

3192 events, 506 stocks, 2016-11-01 to 2026-10-08; context available for 3192 of them.

### Conditions

| condition | train: yes n / excess / hit vs no n / excess / hit (20) | test: the same (20) | yes - no train / test (20) | yes - no train / test (60) | years positive | verdict |
|---|---|---|---|---|---|---|
| regime: beaten-down basket up over the last 20 bars | 900 / +2.10% / 60% vs 836 / +2.63% / 69% | 807 / +0.96% / 57% vs 598 / +0.36% / 56% | -0.53% / +0.60% | -1.53% / -0.68% | 4/10 | noise |
| regime: breadth (share above the 50-day MA) rising vs 20 bars ago | 823 / +2.61% / 62% vs 913 / +2.12% / 65% | 564 / +1.36% / 58% vs 841 / +0.26% / 56% | +0.49% / +1.11% | -0.15% / +1.55% | 6/10 | noise |
| SPY above its 50-day MA | 1101 / +1.58% / 62% vs 635 / +3.69% / 68% | 983 / +0.67% / 56% vs 422 / +0.78% / 58% | -2.10% / -0.11% | -5.20% / -2.49% | 3/10 | noise |
| flag D: more than 40% below the 52-week high | 91 / +6.96% / 69% vs 1645 / +2.10% / 64% | 58 / +6.70% / 64% vs 1347 / +0.44% / 56% | +4.86% / +6.26% | +3.60% / +13.80% | 6/6 | **helps (consistent)** |
| flag Z (proxy): 20-day return vs sector, z below -1 | 281 / +2.00% / 65% vs 1455 / +2.42% / 64% | 204 / -0.06% / 59% vs 1201 / +0.83% / 56% | -0.42% / -0.89% | -2.01% / -3.27% | 6/10 | noise |
| market-driven decline: sector explains >= 50% of the 60-bar fall | 302 / +4.21% / 66% vs 1434 / +1.96% / 64% | 237 / +2.79% / 65% vs 1168 / +0.28% / 55% | +2.25% / +2.51% | +1.97% / +7.27% | 9/10 | **helps (consistent)** |

### Wedge score (terciles)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| low score | train | 586 | +3.11% | 66% | +2.96% |
| mid score | train | 556 | +3.05% | 67% | +2.63% |
| high score | train | 594 | +1.83% | 59% | +1.50% |
| low score | test | 462 | +1.60% | 59% | +0.99% |
| mid score | test | 492 | +1.40% | 55% | +0.66% |
| high score | test | 451 | +1.24% | 55% | +0.45% |

## News-day in a beaten-down stock, long (hold 60 bars)

1084 events, 367 stocks, 2017-10-20 to 2026-07-15; context available for 1084 of them.

### Conditions

| condition | train: yes n / excess / hit vs no n / excess / hit (20) | test: the same (20) | yes - no train / test (20) | yes - no train / test (60) | years positive | verdict |
|---|---|---|---|---|---|---|
| regime: beaten-down basket up over the last 20 bars | 334 / +3.74% / 63% vs 270 / +2.55% / 57% | 253 / +2.61% / 57% vs 227 / +3.59% / 59% | +1.19% / -0.98% | -2.50% / -9.15% | 4/10 | noise |
| regime: breadth (share above the 50-day MA) rising vs 20 bars ago | 312 / +3.39% / 62% vs 292 / +3.01% / 59% | 205 / +4.14% / 62% vs 275 / +2.28% / 56% | +0.38% / +1.86% | -1.70% / +2.25% | 6/10 | noise |
| SPY above its 50-day MA | 315 / +1.97% / 61% vs 289 / +4.56% / 60% | 349 / +2.89% / 58% vs 131 / +3.56% / 59% | -2.58% / -0.67% | -8.47% / -10.25% | 2/9 | **hurts (consistent)** |
| flag D: more than 40% below the 52-week high | 202 / +5.65% / 59% vs 402 / +1.98% / 61% | 139 / +6.37% / 62% vs 341 / +1.73% / 57% | +3.67% / +4.63% | +12.62% / +12.38% | 9/9 | **helps (consistent)** |
| flag Z (proxy): 20-day return vs sector, z below -1 | 348 / +3.18% / 60% vs 256 / +3.25% / 61% | 288 / +2.67% / 62% vs 192 / +3.68% / 53% | -0.08% / -1.01% | +1.46% / -4.85% | 4/10 | noise |
| market-driven decline: sector explains >= 50% of the 60-bar fall | 116 / +4.60% / 66% vs 488 / +2.88% / 59% | 43 / +1.62% / 56% vs 437 / +3.22% / 59% | +1.72% / -1.59% | +7.12% / +8.44% | 4/6 | noise |

### Gap size

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| 4-7% | train | 246 | +2.18% | 59% | +2.67% |
| 7-12% | train | 211 | +2.88% | 62% | +3.71% |
| >12% | train | 147 | +3.36% | 60% | +3.40% |
| 4-7% | test | 164 | +4.27% | 67% | +4.61% |
| 7-12% | test | 172 | +0.91% | 48% | +1.43% |
| >12% | test | 144 | +2.89% | 61% | +3.31% |

### Gap direction

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| gap down | train | 477 | +2.97% | 61% | +3.33% |
| gap up | train | 127 | +1.76% | 59% | +2.76% |
| gap down | test | 396 | +2.50% | 58% | +2.59% |
| gap up | test | 84 | +3.38% | 60% | +5.37% |

### Late entry (first close above the previous bar's high within 10 bars) vs the next open

| period | n | late entry found | next open 20: net / hit / vs SPY | late entry 20: net / hit / vs SPY | next open 60: net / hit / vs SPY | late entry 60: net / hit / vs SPY |
|---|---|---|---|---|---|---|
| train | 604 | 95% | +2.71% / 60% / +1.67% (n=604) | +2.51% / 58% / +1.25% (n=574) | +8.17% / 65% / +5.57% (n=604) | +8.07% / 65% / +5.31% (n=574) |
| test | 480 | 90% | +2.65% / 58% / +0.70% (n=480) | +2.77% / 58% / +1.20% (n=433) | +8.46% / 64% / +2.67% (n=480) | +9.12% / 63% / +3.30% (n=431) |

## Early rally in a beaten-down stock (hold 20 bars)

5425 events, 507 stocks, 2017-10-20 to 2026-07-14; context available for 5425 of them.

### Conditions

| condition | train: yes n / excess / hit vs no n / excess / hit (20) | test: the same (20) | yes - no train / test (20) | yes - no train / test (60) | years positive | verdict |
|---|---|---|---|---|---|---|
| regime: beaten-down basket up over the last 20 bars | 1908 / +3.17% / 58% vs 1424 / +5.00% / 65% | 1337 / +2.97% / 55% vs 756 / +4.82% / 64% | -1.83% / -1.85% | -2.70% / -5.13% | 3/10 | **hurts (consistent)** |
| regime: breadth (share above the 50-day MA) rising vs 20 bars ago | 1894 / +3.32% / 57% vs 1438 / +4.78% / 66% | 1165 / +3.82% / 59% vs 928 / +3.41% / 58% | -1.47% / +0.41% | -1.77% / -1.39% | 2/10 | noise |
| SPY above its 50-day MA | 1766 / +3.19% / 58% vs 1566 / +4.81% / 65% | 1530 / +3.21% / 56% vs 563 / +4.81% / 65% | -1.61% / -1.61% | -3.13% / -3.98% | 2/9 | **hurts (consistent)** |
| flag D: more than 40% below the 52-week high | 558 / +7.76% / 62% vs 2774 / +3.18% / 61% | 320 / +7.10% / 60% vs 1773 / +3.01% / 58% | +4.58% / +4.09% | +6.29% / +11.35% | 8/9 | **helps (consistent)** |
| flag Z (proxy): 20-day return vs sector, z below -1 | 484 / +3.54% / 60% vs 2848 / +4.02% / 61% | 219 / +3.30% / 57% vs 1874 / +3.68% / 59% | -0.48% / -0.38% | +0.48% / -1.62% | 4/10 | noise |
| market-driven decline: sector explains >= 50% of the 60-bar fall | 1169 / +6.64% / 70% vs 2163 / +2.50% / 56% | 337 / +5.13% / 68% vs 1756 / +3.35% / 57% | +4.15% / +1.78% | +2.99% / +5.22% | 6/9 | **helps (consistent)** |

### Depth of the decline (6-month return)

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| 6m < -30% | train | 483 | +6.21% | 65% | +8.65% |
| -30% to -20% | train | 743 | +3.53% | 64% | +5.27% |
| -20% to -8% | train | 2106 | +1.74% | 59% | +2.41% |
| 6m < -30% | test | 222 | +5.03% | 59% | +8.05% |
| -30% to -20% | test | 438 | +2.14% | 57% | +3.73% |
| -20% to -8% | test | 1433 | +1.92% | 59% | +2.93% |

### Rules fired within a week

| bucket | period | n | net 20-bar return | hit | excess over local random |
|---|---|---|---|---|---|
| 1 | train | 2758 | +2.46% | 60% | +3.51% |
| 2 | train | 489 | +4.35% | 66% | +6.09% |
| 3 | train | 81 | +4.45% | 65% | +5.87% |
| 4 | train | 4 | +5.46% | 75% | +7.06% |
| 1 | test | 1682 | +2.26% | 59% | +3.53% |
| 2 | test | 344 | +2.72% | 60% | +4.23% |
| 3 | test | 65 | +0.75% | 48% | +3.09% |
| 4 | test | 2 | +6.63% | 100% | +6.54% |

## Verdicts

- **Beaten-down falling-wedge breakout (hold 20 bars)**: *flag D: more than 40% below the 52-week high* helps (+4.86% train, +6.26% test at 20 bars).
- **Beaten-down falling-wedge breakout (hold 20 bars)**: *market-driven decline: sector explains >= 50% of the 60-bar fall* helps (+2.25% train, +2.51% test at 20 bars).
- **News-day in a beaten-down stock, long (hold 60 bars)**: *SPY above its 50-day MA* hurts (-2.58% train, -0.67% test at 20 bars).
- **News-day in a beaten-down stock, long (hold 60 bars)**: *flag D: more than 40% below the 52-week high* helps (+3.67% train, +4.63% test at 20 bars).
- **Early rally in a beaten-down stock (hold 20 bars)**: *regime: beaten-down basket up over the last 20 bars* hurts (-1.83% train, -1.85% test at 20 bars).
- **Early rally in a beaten-down stock (hold 20 bars)**: *SPY above its 50-day MA* hurts (-1.61% train, -1.61% test at 20 bars).
- **Early rally in a beaten-down stock (hold 20 bars)**: *flag D: more than 40% below the 52-week high* helps (+4.58% train, +4.09% test at 20 bars).
- **Early rally in a beaten-down stock (hold 20 bars)**: *market-driven decline: sector explains >= 50% of the 60-bar fall* helps (+4.15% train, +1.78% test at 20 bars).

## Reading

Only a condition marked **helps** or **hurts** in a family is a candidate for that family's rule, and only as the filter stated (a gate on entry, not a score). A condition that passes in one family and fails in another stays confined to the family where it passed. The reports keep showing the flags and the regime line as context either way; this file says which of them earned the right to be a rule.

Systematic screens and an event study on today's index members (survivorship bias), not investment advice.
