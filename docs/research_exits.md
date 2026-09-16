# Exit rules: is "hold 20 bars" really the best you can do?

Question: on the three entries the journal forward-tests, does an *adaptive* exit (take a quick profit, a target
that rises with time, a per-day return threshold, a trailing stop) beat the plain time exit, either per trade or
per bar of capital? Code: `algovision/research/exits.py` (`python -m algovision.research.exits --wedge-csv ...
--insider-dir ...`); tables: [`research/exits/`](research/exits/).

Setup, same discipline as the other studies: 518 S&P 500 / NASDAQ-100 members, 10 years of daily bars, entry at
the next open, 10 bps per round trip, train before 2023-01-01, test after. Entries (all long, all in beaten-down
stocks: below the 200-day MA and down > 8 % over six months): confirmed Falling Wedge (959 events), news-day gap
(1,121), single insider purchase >= $100k (698). Every exit rule is also applied to 10 random entries per event
in the same stock within ±6 months, so **excess** = what the signal adds *under that exit*: a take-profit rule
changes hit rates and holding times on any price series, and only the paired comparison separates the entry from
the exit. Two yardsticks: **net return per trade** and **return per bar of capital** (bp / bar), the "2 % in one
day beats 2 % in five" view.

Pre-registered exit families (thresholds fixed before looking): time 5 / 10 / 20 / 40 / 60; take 2-8 % then
time; rising target (+2 % on day 1 growing 0.25-0.5 % a day); per-day threshold (exit when return >= r % x days,
r = 0.5 / 1 / 2); the rule as proposed ("hybrid": +2 % on day 1, otherwise wait for +6 %, time 7 / 10 / 20);
trailing stop 3 / 5 / 8 % below the highest close.

## Answer: no exit rule beats the time exit per trade, and none beats it per bar of capital either

Test period (2023-26), the numbers that matter. Full grids with train / test / all and confidence intervals in
[`research/exits/exits.md`](research/exits/exits.md).

| entry (journal hold) | exit rule | hit | bars | net / trade | excess vs random | bp / bar | excess bp / bar |
|---|---|---|---|---|---|---|---|
| Falling Wedge (20) | **time 20** | 59 % | 20 | **+2.05 %** | +2.78 % | 10.2 | +13.9 |
| | time 40 | 64 % | 40 | +4.96 % | +6.62 % | 12.4 | +16.6 |
| | time 60 | 62 % | 60 | +5.93 % | +8.89 % | 9.9 | +14.8 |
| | take 2 % / time 20 | 87 % | 6.5 | +0.52 % | +0.68 % | 7.9 | +9.9 |
| | rising 2 % +0.5 %/bar / 20 | 77 % | 10.5 | +0.83 % | +1.20 % | 8.0 | +11.1 |
| | per-day 2 % / 20 | 65 % | 17.1 | +2.21 % | +2.86 % | 12.9 | +16.6 |
| | hybrid 2 % → 6 % / 10 | 67 % | 7.0 | +0.73 % | +0.94 % | 10.4 | +13.2 |
| | trail 5 % / 20 | 48 % | 13.8 | +1.20 % | +2.03 % | 8.7 | +15.0 |
| News day (60) | **time 60** | 64 % | 60 | **+8.56 %** | +11.06 % | **14.3** | +18.4 |
| | time 20 | 59 % | 20 | +2.72 % | +3.87 % | 13.6 | +19.3 |
| | take 5 % / time 60 | 84 % | 20 | +2.23 % | +3.36 % | 11.0 | +14.9 |
| | per-day 0.5 % / 60 | 82 % | 19 | +1.69 % | +2.79 % | 8.7 | +13.4 |
| | hybrid 2 % → 6 % / 10 | 74 % | 5.1 | +0.42 % | +0.85 % | 8.3 | +14.2 |
| | trail 8 % / 60 | 50 % | 31 | +3.72 % | +5.60 % | 12.1 | +19.2 |
| Insider buy (120; 60 here) | **time 60** | 61 % | 60 | **+4.37 %** | +8.08 % | 7.3 | +13.5 |
| | time 10 | 59 % | 10 | +1.20 % | +1.89 % | 12.0 | +18.9 |
| | take 2 % / time 20 | 87 % | 6.0 | +0.86 % | +1.30 % | 14.4 | +19.6 |
| | per-day 0.5 % / 20 | 83 % | 7.0 | +1.07 % | +1.77 % | 15.2 | +22.6 |
| | hybrid 2 % → 6 % / 10 | 70 % | 6.2 | +0.95 % | +1.48 % | 15.2 | +22.1 |
| | trail 5 % / 60 | 47 % | 21 | +1.57 % | +3.20 % | 7.4 | +16.7 |

Four things hold across the three entries and both periods:

1. **Per trade, the time exit wins everywhere.** Every take-profit, rising-target, per-day and trailing rule
   earns less per signal than simply holding to the time limit, in train and in test, for all three entries.
   The longer holds earn the most per signal: wedge time 60 +4.2 % / +5.9 % (train / test) vs time 20 +3.9 % /
   +2.1 %; news day time 60 +8.2 % / +8.6 %; insider time 60 +9.8 % / +4.4 %.
2. **Per bar of capital, the quick-profit rules do not win either.** The intuition "2 % in a day is a better use
   of money than 2 % in five" is right as arithmetic and wrong as a rule, because the rule does not choose
   which trades get the fast 2 %. Decomposition, wedge test period:

   | rule | hit | winners | losers |
   |---|---|---|---|
   | time 20 | 59 % | +8.4 % in 20 bars | −7.2 % in 20 bars |
   | take 2 % / time 20 | 87 % | +2.0 % in 4.5 bars | −9.2 % in 20 bars |
   | hybrid 2 % → 6 % / time 20 | 75 % | +4.0 % in 8.9 bars | −7.7 % in 20 bars |
   | per-day 2 % / time 20 | 65 % | +7.3 % in 15 bars | −7.1 % in 20 bars |
   | trail 5 % / time 20 | 48 % | +8.1 % in 18 bars | −5.1 % in 9.7 bars |

   A take-profit caps the winners at +2 % and sends them home early, while the losers (which never reach the
   target) stay the full 20 bars and end worse than under the time exit (−9.2 % vs −7.2 %, because the ones that
   bounced to +2 % and left were the milder losers). Capital is freed on the trades that were paying and kept
   in the ones that were not. Net: 7.9 bp / bar vs 10.2 for the time exit, and +0.5 % vs +2.1 % per trade.
3. **The high hit rate is manufactured, not earned.** Under "take 2 %" the random entries in the same stocks win
   85 % of the time too, and still lose money (−0.2 to −0.9 % per trade after costs, in every entry and period).
   Hit rate under a take-profit rule says nothing about expectancy; the paired excess does.
4. **Trailing stops are the worst family.** 3-5 % trails are hit by noise on 95-100 % of trades, the hit rate
   falls to 40-50 % and per-trade returns drop by a third to a half; an 8 % trail with a 60-bar limit is
   the only one close to the time exit, because it rarely triggers.

Where an adaptive rule looks better it is not consistent:

* **per-day 2 % on the wedge** beats time 20 in test (+2.21 % vs +2.05 %, 12.9 vs 10.2 bp / bar) but not in
  train (+3.11 % vs +3.93 %, 19.3 vs 19.7 bp / bar); it exits early on only 16-21 % of trades, so it is mostly
  the time exit with a small, sign-flipping difference.
* **insider buys in the test period** earn more per bar with short holds (time 10: 12.0 bp; per-day 0.5 %: 15.2
  bp) than with time 60 (7.3 bp), the opposite of the train period (time 60: 16.3 bp, the best of all rules).
  With 265 test events this is the edge arriving faster in 2023-26, not a reason to change the exit; per trade
  time 60 still earns 3-4x more.

## What this means for the journal

* Keep the time exits: 20 bars for the wedge, 60 for the news day, 120 for insiders. If capital is not the
  binding constraint (about 20 open positions and 0-2 new signals a day, so it is not), a longer wedge hold
  earns more per signal: 40-60 bars was better than 20 per trade in both periods, at a lower return per bar in
  train and an equal one in test. 20 remains the conservative choice; 40 is defensible.
* Do not add a take-profit, a rising target or a trailing stop. They convert a few large wins into many small
  ones, keep the losers, and pay the spread more often. If a rule is wanted for the *feeling* of banking gains,
  the per-day threshold is the least harmful (it rarely fires), but it adds nothing.
* Capital efficiency comes from the entry, not the exit: among the tested rules the news day earns ~14 bp / bar
  for 60 bars and the wedge ~10-12; a "faster" exit lowers both.

## Caveats

Daily bars: a target and a close-based trailing stop cannot see intraday order inside a bar; targets fill at
the target or the open (gap-through), trails at the close. Survivorship applies to all three entries (today's
index members); the paired random baseline removes the stock's drift but not the membership bias. The insider
horizon here is 60 bars (the journal holds 120). Thresholds were fixed once and not tuned; 27 rules x 3
entries is still many comparisons, so a single cell that beats the time exit in one period is expected by
chance, which is why only effects present in both periods are reported as findings.
