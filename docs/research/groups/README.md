# Groups as one stock: does the peer group confirm a signal, and is the group itself a signal?

Tables: `docs/research/groups/`. Reproduce with `python -m algovision research-groups`.

Peer groups are built point-in-time (from the three years before each signal's year, `algovision/peers.py`), aggregated into equal-weight daily-rebalanced baskets (`algovision/research/groups.py`), and the falling-wedge screen is run on stocks and on baskets alike. Train = signals before 2023-01-01, test = after. Excess = return over random entries in the same stock (or basket) over the same holding period.

## 1. Confirmation by the group (stock-level beaten-down falling-wedge breakouts)

829 beaten-down wedge breakouts in stocks with a point-in-time group (812 with a group of 3+ members). Conditions:

- **group beaten down**: the basket itself has a 6-month return below -8% and is below its 200-day MA at the signal.
- **group wedge breakout**: the basket broke out of its own falling wedge within the 10 bars before the signal.
- **group in a wedge**: the basket is inside a forming or confirmed falling wedge at the signal.
- **most members beaten down**: more than half of the other members are beaten down.
- **another member signalled**: at least one other member had a wedge breakout within about 10 bars.
- **stock below its group (z < -1)**: the stock's 20-day return relative to the group is more than one standard deviation under its norm.
- **stock above its group (z > +1)**: the opposite.

| condition | period | state | n | 20-bar return | hit | excess over random (95% CI) |
|---|---|---|---|---|---|---|
| group beaten down | train | yes | 251 | +5.14% | 72% | +3.59% (+2.3 to +4.9) |
| group beaten down | train | no | 194 | +4.53% | 71% | +3.15% (+1.7 to +4.5) |
| group beaten down | test | yes | 104 | +3.28% | 68% | +2.22% (+0.4 to +4.3) |
| group beaten down | test | no | 260 | +1.58% | 56% | +0.28% (-1.0 to +1.6) |
| group wedge breakout | train | yes | 89 | +6.59% | 78% | +5.20% (+2.9 to +7.4) |
| group wedge breakout | train | no | 356 | +4.45% | 70% | +2.95% (+1.7 to +4.0) |
| group wedge breakout | test | yes | 36 | +3.95% | 78% | +2.57% (-1.0 to +6.0) |
| group wedge breakout | test | no | 328 | +1.86% | 57% | +0.65% (-0.5 to +1.8) |
| group in a wedge | train | yes | 89 | +3.41% | 56% | +1.68% (-0.5 to +3.9) |
| group in a wedge | train | no | 356 | +5.24% | 75% | +3.83% (+2.7 to +5.0) |
| group in a wedge | test | yes | 78 | -0.17% | 51% | -1.32% (-3.7 to +1.0) |
| group in a wedge | test | no | 286 | +2.68% | 62% | +1.43% (+0.1 to +2.7) |
| most members beaten down | train | yes | 231 | +5.60% | 73% | +4.00% (+2.5 to +5.5) |
| most members beaten down | train | no | 214 | +4.10% | 70% | +2.75% (+1.3 to +4.0) |
| most members beaten down | test | yes | 86 | +3.55% | 70% | +2.27% (-0.0 to +4.4) |
| most members beaten down | test | no | 278 | +1.61% | 56% | +0.39% (-0.8 to +1.7) |
| another member signalled | train | yes | 297 | +5.65% | 75% | +4.13% (+3.0 to +5.2) |
| another member signalled | train | no | 148 | +3.33% | 64% | +1.92% (-0.0 to +3.8) |
| another member signalled | test | yes | 216 | +1.99% | 59% | +0.83% (-0.5 to +2.2) |
| another member signalled | test | no | 148 | +2.18% | 60% | +0.84% (-0.7 to +2.6) |
| stock below its group (z < -1) | train | yes | 72 | +5.09% | 76% | +3.99% (+1.4 to +6.4) |
| stock below its group (z < -1) | train | no | 373 | +4.83% | 70% | +3.28% (+2.1 to +4.3) |
| stock below its group (z < -1) | test | yes | 35 | +4.09% | 71% | +2.93% (-1.7 to +7.0) |
| stock below its group (z < -1) | test | no | 329 | +1.85% | 58% | +0.61% (-0.5 to +1.7) |
| stock above its group (z > +1) | train | yes | 41 | +6.19% | 78% | +5.19% (+2.4 to +7.5) |
| stock above its group (z > +1) | train | no | 404 | +4.74% | 71% | +3.22% (+2.3 to +4.3) |
| stock above its group (z > +1) | test | yes | 42 | -0.12% | 50% | -1.29% (-4.7 to +2.6) |
| stock above its group (z > +1) | test | no | 322 | +2.35% | 61% | +1.11% (+0.0 to +2.3) |
| group beaten down AND group wedge breakout | train | yes | 63 | +7.06% | 79% | +5.64% (+2.7 to +8.2) |
| group beaten down AND group wedge breakout | train | no | 382 | +4.52% | 70% | +3.03% (+2.0 to +4.2) |
| group beaten down AND group wedge breakout | test | yes | 11 | +5.37% | 82% | +4.24% (-2.2 to +10.8) |
| group beaten down AND group wedge breakout | test | no | 353 | +1.96% | 59% | +0.73% (-0.5 to +1.8) |
| group beaten down OR most members beaten down | train | yes | 264 | +5.31% | 72% | +3.79% (+2.6 to +5.2) |
| group beaten down OR most members beaten down | train | no | 181 | +4.24% | 70% | +2.83% (+1.3 to +4.3) |
| group beaten down OR most members beaten down | test | yes | 116 | +3.27% | 68% | +2.11% (+0.4 to +3.9) |
| group beaten down OR most members beaten down | test | no | 248 | +1.50% | 55% | +0.24% (-1.0 to +1.6) |

### Is any condition consistent?

The difference between the *yes* and the *no* rows (excess over random), train and test, at 20 and at 60 bars, and the number of years (with 5+ signals on each side) in which the 20-bar difference was positive. "Consistent" = at least +0.5% in both periods at 20 bars.

| condition | yes - no, train (20 bars) | yes - no, test (20 bars) | yes - no, train (60 bars) | yes - no, test (60 bars) | years positive (20 bars) | consistent |
|---|---|---|---|---|---|---|
| group beaten down | +0.43% (n=251) | +1.94% (n=104) | -1.74% | +1.02% | 4/7 | no |
| group wedge breakout | +2.25% (n=89) | +1.92% (n=36) | -3.76% | +2.60% | 5/8 | **yes** |
| group in a wedge | -2.15% (n=89) | -2.75% (n=78) | -0.61% | +0.26% | 0/6 | no |
| most members beaten down | +1.24% (n=231) | +1.88% (n=86) | -2.18% | -0.88% | 6/6 | **yes** |
| another member signalled | +2.21% (n=297) | -0.01% (n=216) | -0.78% | -1.48% | 6/8 | no |
| stock below its group (z < -1) | +0.70% (n=72) | +2.31% (n=35) | -1.16% | +1.00% | 7/8 | **yes** |
| stock above its group (z > +1) | +1.97% (n=41) | -2.40% (n=42) | +2.10% | +1.30% | 3/5 | no |
| group beaten down AND group wedge breakout | +2.61% (n=63) | +3.50% (n=11) | -7.24% | -0.53% | 2/3 | **yes** |
| group beaten down OR most members beaten down | +0.95% (n=264) | +1.87% (n=116) | -1.32% | -0.66% | 4/7 | **yes** |

Robustness: the same conditions on **all** wedge breakouts (beaten-down or not):

| condition | period | state | n | 20-bar return | hit | excess over random (95% CI) |
|---|---|---|---|---|---|---|
| group beaten down | train | yes | 302 | +4.30% | 70% | +2.81% (+1.6 to +3.9) |
| group beaten down | train | no | 866 | +2.81% | 64% | +1.41% (+0.8 to +2.1) |
| group beaten down | test | yes | 150 | +3.27% | 66% | +2.16% (+0.6 to +3.6) |
| group beaten down | test | no | 1211 | +1.35% | 56% | -0.00% (-0.5 to +0.6) |
| group wedge breakout | train | yes | 182 | +5.33% | 71% | +3.84% (+2.4 to +5.2) |
| group wedge breakout | train | no | 986 | +2.80% | 65% | +1.39% (+0.8 to +2.0) |
| group wedge breakout | test | yes | 154 | +2.62% | 64% | +1.22% (-0.3 to +2.8) |
| group wedge breakout | test | no | 1207 | +1.43% | 57% | +0.11% (-0.4 to +0.7) |
| another member signalled | train | yes | 719 | +3.93% | 70% | +2.45% (+1.8 to +3.1) |
| another member signalled | train | no | 449 | +2.01% | 60% | +0.69% (-0.3 to +1.6) |
| another member signalled | test | yes | 813 | +1.93% | 58% | +0.57% (-0.1 to +1.3) |
| another member signalled | test | no | 548 | +1.03% | 57% | -0.25% (-1.1 to +0.6) |
| stock below its group (z < -1) | train | yes | 200 | +3.02% | 67% | +1.80% (-0.0 to +3.3) |
| stock below its group (z < -1) | train | no | 968 | +3.23% | 66% | +1.77% (+1.2 to +2.4) |
| stock below its group (z < -1) | test | yes | 201 | +2.04% | 58% | +0.62% (-1.0 to +2.4) |
| stock below its group (z < -1) | test | no | 1160 | +1.48% | 57% | +0.17% (-0.4 to +0.7) |

## 2. The group as the instrument (falling-wedge breakouts on the baskets)

306 basket breakouts, 71 in beaten-down baskets.

| set | period | n | basket 20-bar return | basket hit | basket excess over random (95% CI) | members' mean 20-bar return | members' hit |
|---|---|---|---|---|---|---|---|
| all basket breakouts | train | 141 | +4.45% | 72% | +3.25% (+2.0 to +4.5) | +4.27% | 68% |
| all basket breakouts | test | 153 | +1.78% | 61% | +0.53% (-0.5 to +1.6) | +1.81% | 57% |
| beaten-down baskets | train | 45 | +4.89% | 69% | +3.87% (+1.3 to +6.4) | +4.96% | 69% |
| beaten-down baskets | test | 24 | +2.09% | 54% | +0.66% (-2.4 to +3.8) | +1.96% | 54% |
| beaten-down baskets, most members beaten | train | 42 | +5.38% | 71% | +4.29% (+1.6 to +6.6) | +5.44% | 71% |
| beaten-down baskets, most members beaten | test | 16 | +1.46% | 44% | +0.10% (-3.4 to +3.4) | +1.31% | 45% |

## 3. Reading

A condition counts only if the *yes* rows beat the *no* rows in excess return in **both** periods with a meaningful size (about +1% or more over 20 bars) and a usable sample. Everything else is noise, however good it looks in one period.

Systematic screens and an event study on today's index members (survivorship bias), not investment advice.
