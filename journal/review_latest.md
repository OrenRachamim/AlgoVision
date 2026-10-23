# AlgoVision review: what has worked so far - 2026-10-23

What in the daily report is actually relevant on the evidence so far: 33 dated reports, 2026-09-05 to 2026-10-21. Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), not judgement: a table 'works' only with 20+ names and a t of 2 or more on the basket excess; a condition 'separates' only with 12+ names on each side and a t of 2 or more on the difference. The windows overlap and the sample is a few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year backtests decide what enters the report.

## Bottom line

### 20 bars after the listing

**Works or separates so far:** sentiment read positive (diff +3.5%, n 17/59, t 2.3); 20-day return above the peer group (vs peers 20d > 0) (diff +3.7%, n 28/48, t 2.4)

**Not working, or the other side did better:** none

**Noise so far:** falling wedge, forming (watch list) (n 54, vs basket -0.1%, t -0.2); insider buys, other (n 24, vs basket +1.8%, t 1.4); growth screen (retired) (n 22, vs basket +1.5%, t 0.7); S: negative sentiment (warning) (diff -0.5%, n 24/52, t -0.4); no warning flag at all (diff +2.0%, n 45/31, t 1.4); read: signs of a bottom (diff -0.3%, n 29/47, t -0.2); 'market-wide' among the causes of the decline (diff -1.4%, n 18/58, t -0.7); analyst consensus buy / strong buy (diff +1.9%, n 63/13, t 0.9); more than 30% below the 52-week high (diff -0.6%, n 29/47, t -0.3); listed 1-3 days (fresh) vs 4+ days (diff -0.1%, n 16/72, t -0.1); peer group beaten down too (diff +1.6%, n 14/20, t 1.1)

**Too early to say:** news-day (n 9, vs basket -3.3%, t -1.5); falling wedge (confirmed) (n 11, vs basket +2.8%, t 1.5); insider buys, beaten-down (n 14, vs basket +2.0%, t 1.0); early rally (n 0, vs basket , t ); MA200 cross after a long run below (n 0, vs basket , t ); Jev decision (n 0, vs basket , t ); Z: z vs peers below -1 (warning) (diff -6.7%, n 6/70, t -3.0); T: target upside above 50% (warning) (diff -4.6%, n 5/71, t -1.7); D: more than 40% below the 52-week high (a plus over ten years) (diff -2.4%, n 11/65, t -0.7); read: still falling (diff +6.1%, n 2/74, t ); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff , n 0/0, t ); 6-month return below -30% (diff -4.0%, n 10/69, t -1.9); signal-day volume above 1.5x (diff , n 0/11, t ); a 3x+ volume day in the last 10 bars (diff , n 0/11, t ); early rally: two or more rules fired (diff , n 0/0, t ); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff , n 0/0, t ); Jev: P(buy) < 0.2 (diff , n 0/0, t )

### To date (against the current price, every name listed)

**Works or separates so far:** peer group beaten down too (diff +3.3%, n 70/128, t 4.2)

**Not working, or the other side did better:** insider buys, other (n 26, vs basket -3.8%, t -2.1); growth screen (retired) (n 22, vs basket -10.1%, t -4.8); read: signs of a bottom (diff -4.3%, n 52/101, t -2.8); 'market-wide' among the causes of the decline (diff -3.4%, n 49/104, t -2.5); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff -3.9%, n 19/16, t -2.2)

**Noise so far:** falling wedge (confirmed) (n 39, vs basket +0.3%, t 0.3); early rally (n 97, vs basket +0.6%, t 1.0); falling wedge, forming (watch list) (n 96, vs basket +0.1%, t 0.1); Jev decision (n 120, vs basket -0.1%, t -0.2); Z: z vs peers below -1 (warning) (diff -2.9%, n 19/134, t -1.4); S: negative sentiment (warning) (diff +1.4%, n 44/109, t 1.0); D: more than 40% below the 52-week high (a plus over ten years) (diff -3.6%, n 24/129, t -1.4); no warning flag at all (diff +0.6%, n 90/63, t 0.4); sentiment read positive (diff +0.8%, n 41/112, t 0.6); analyst consensus buy / strong buy (diff -2.5%, n 123/30, t -1.7); more than 30% below the 52-week high (diff -1.3%, n 64/89, t -0.9); 20-day return above the peer group (vs peers 20d > 0) (diff +2.3%, n 51/102, t 1.7); listed 1-3 days (fresh) vs 4+ days (diff +1.6%, n 79/187, t 1.9); 6-month return below -30% (diff -2.4%, n 24/226, t -1.2); signal-day volume above 1.5x (diff -5.1%, n 12/144, t -1.7); early rally: two or more rules fired (diff -1.9%, n 15/82, t -0.9); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff -1.6%, n 21/99, t -0.8); Jev: P(buy) < 0.2 (diff +1.6%, n 62/58, t 1.3)

**Too early to say:** news-day (n 16, vs basket -4.7%, t -2.0); insider buys, beaten-down (n 17, vs basket -0.8%, t -0.5); MA200 cross after a long run below (n 1, vs basket +2.8%, t ); T: target upside above 50% (warning) (diff -11.7%, n 9/144, t -4.7); read: still falling (diff +4.0%, n 11/142, t 3.2); a 3x+ volume day in the last 10 bars (diff +1.3%, n 2/56, t )

## By table (20 bars)

| table | n | n20 | ret 20 | hit 20 | vs SPY 20 | vs basket 20 | t 20 | verdict 20 | to date | hit | vs SPY | vs basket | t | verdict to date | research expected | same sign in both halves |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|:--|:--|:--|
| news-day | 16 | 9 | -6.8% | 11% | -8.3% | -3.3% | -1.5 | too early | -0.7% | 56% | -0.2% | -4.7% | -2.0 | too early | +6-7% vs random at 60 bars |  |
| falling wedge (confirmed) | 39 | 11 | +2.1% | 73% | +1.3% | +2.8% | 1.5 | too early | +4.4% | 85% | +5.3% | +0.3% | 0.3 | noise so far | +3% vs random at 20 bars |  |
| insider buys, beaten-down | 17 | 14 | -1.6% | 43% | -3.2% | +2.0% | 1.0 | too early | +0.9% | 41% | +1.1% | -0.8% | -0.5 | too early | +10% vs random at 60 bars |  |
| early rally | 97 | 0 |  |  |  |  |  | too early | +4.2% | 86% | +5.5% | +0.6% | 1.0 | noise so far | +2-3% net, ~0 vs SPY at 20 bars |  |
| MA200 cross after a long run below | 1 | 0 |  |  |  |  |  | too early | +2.7% | 100% | +3.7% | +2.8% |  | too early | no edge in both periods |  |
| falling wedge, forming (watch list) | 96 | 54 | -2.1% | 41% | -3.4% | -0.1% | -0.2 | noise so far | +3.9% | 70% | +4.2% | +0.1% | 0.1 | noise so far | no edge (a stock still falling) |  |
| insider buys, other | 26 | 24 | -2.1% | 25% | -3.6% | +1.8% | 1.4 | noise so far | -2.0% | 50% | -1.7% | -3.8% | -2.1 | not working so far | no edge |  |
| Jev decision | 120 | 0 |  |  |  |  |  | too early | +4.7% | 81% | +5.8% | -0.1% | -0.2 | noise so far | untested (forward test only) |  |
| growth screen (retired) | 22 | 22 | -3.4% | 36% | -5.2% | +1.5% | 0.7 | noise so far | -8.9% | 18% | -8.8% | -10.1% | -4.8 | not working so far | retired |  |

## By condition (basket excess, with vs without; 20 bars and to date)

| condition | n with | n without | ret 20 with | ret 20 without | hit 20 with | hit 20 without | vs basket 20 with | vs basket 20 without | diff 20 | t 20 | verdict 20 | n with (to date) | n without | ret with | ret without | vs basket with | vs basket without | diff | t | verdict to date |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| Z: z vs peers below -1 (warning) | 6 | 70 | -5.0% | +1.9% | 0% | 77% | -6.9% | -0.2% | -6.7% | -3.0 | too early | 19 | 134 | +0.8% | +4.8% | -3.1% | -0.2% | -2.9% | -1.4 | noise so far |
| S: negative sentiment (warning) | 24 | 52 | +0.8% | +1.6% | 67% | 73% | -1.1% | -0.5% | -0.5% | -0.4 | noise so far | 44 | 109 | +4.8% | +4.1% | +0.5% | -0.9% | +1.4% | 1.0 | noise so far |
| T: target upside above 50% (warning) | 5 | 71 | -3.0% | +1.7% | 20% | 75% | -5.1% | -0.4% | -4.6% | -1.7 | too early | 9 | 144 | -6.3% | +4.9% | -11.5% | +0.2% | -11.7% | -4.7 | too early |
| D: more than 40% below the 52-week high (a plus over ten years) | 11 | 65 | -0.8% | +1.7% | 64% | 72% | -2.7% | -0.4% | -2.4% | -0.7 | too early | 24 | 129 | +1.2% | +4.8% | -3.5% | +0.0% | -3.6% | -1.4 | noise so far |
| no warning flag at all | 45 | 31 | +2.3% | +0.0% | 82% | 55% | +0.1% | -1.9% | +2.0% | 1.4 | noise so far | 90 | 63 | +4.9% | +3.4% | -0.3% | -0.9% | +0.6% | 0.4 | noise so far |
| read: signs of a bottom | 29 | 47 | +1.2% | +1.5% | 72% | 70% | -0.9% | -0.6% | -0.3% | -0.2 | noise so far | 52 | 101 | +1.8% | +5.5% | -3.3% | +0.9% | -4.3% | -2.8 | better without it |
| read: still falling | 2 | 74 | +7.1% | +1.2% | 100% | 70% | +5.2% | -0.9% | +6.1% |  | too early | 11 | 142 | +6.1% | +4.1% | +3.2% | -0.8% | +4.0% | 3.2 | too early |
| 'market-wide' among the causes of the decline | 18 | 58 | +0.1% | +1.7% | 67% | 72% | -1.7% | -0.4% | -1.4% | -0.7 | noise so far | 49 | 104 | +2.0% | +5.3% | -2.8% | +0.6% | -3.4% | -2.5 | better without it |
| sentiment read positive | 17 | 59 | +3.9% | +0.6% | 88% | 66% | +2.0% | -1.5% | +3.5% | 2.3 | better with the condition | 41 | 112 | +4.7% | +4.1% | +0.1% | -0.7% | +0.8% | 0.6 | noise so far |
| analyst consensus buy / strong buy | 63 | 13 | +1.7% | -0.4% | 70% | 77% | -0.4% | -2.3% | +1.9% | 0.9 | noise so far | 123 | 30 | +3.9% | +5.7% | -1.0% | +1.5% | -2.5% | -1.7 | noise so far |
| more than 30% below the 52-week high | 29 | 47 | +0.9% | +1.7% | 66% | 74% | -1.1% | -0.5% | -0.6% | -0.3 | noise so far | 64 | 89 | +3.6% | +4.7% | -1.2% | +0.0% | -1.3% | -0.9 | noise so far |
| 20-day return above the peer group (vs peers 20d > 0) | 28 | 48 | +3.8% | -0.1% | 93% | 58% | +1.6% | -2.1% | +3.7% | 2.4 | better with the condition | 51 | 102 | +5.8% | +3.5% | +1.0% | -1.3% | +2.3% | 1.7 | noise so far |
| checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 19 | 16 | +1.1% | +5.4% | -2.1% | +1.7% | -3.9% | -2.2 | better without it |
| listed 1-3 days (fresh) vs 4+ days | 16 | 72 | -1.9% | -2.0% | 38% | 43% | +0.2% | +0.3% | -0.1% | -0.1 | noise so far | 79 | 187 | +4.9% | +3.0% | +1.1% | -0.5% | +1.6% | 1.9 | noise so far |
| peer group beaten down too | 14 | 20 | -1.6% | -1.3% | 43% | 45% | +1.1% | -0.5% | +1.6% | 1.1 | noise so far | 70 | 128 | +6.5% | +2.8% | +2.3% | -0.9% | +3.3% | 4.2 | better with the condition |
| 6-month return below -30% | 10 | 69 | -5.5% | -0.8% | 20% | 49% | -2.8% | +1.2% | -4.0% | -1.9 | too early | 24 | 226 | +1.1% | +4.2% | -1.9% | +0.5% | -2.4% | -1.2 | noise so far |
| signal-day volume above 1.5x | 0 | 11 |  | -2.6% |  | 45% |  | -0.8% |  |  | too early | 12 | 144 | +0.1% | +3.9% | -4.6% | +0.5% | -5.1% | -1.7 | noise so far |
| a 3x+ volume day in the last 10 bars | 0 | 11 |  | -2.6% |  | 45% |  | -0.8% |  |  | too early | 2 | 56 | +3.4% | +2.5% | +0.4% | -1.0% | +1.3% |  | too early |
| early rally: two or more rules fired | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 82 | +2.6% | +4.5% | -1.0% | +0.9% | -1.9% | -0.9 | noise so far |
| Jev: P(buy) >= 0.6 (the jev_pick rule) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 21 | 99 | +4.0% | +4.9% | -1.5% | +0.2% | -1.6% | -0.8 | noise so far |
| Jev: P(buy) < 0.2 | 0 | 0 |  |  |  |  |  |  |  |  | too early | 62 | 58 | +4.8% | +4.7% | +0.7% | -0.9% | +1.6% | 1.3 | noise so far |

## The journal: closed trades against the research expectation

| rule | logged | closed | closed mean | closed hit | vs SPY | vs basket | expected hit | open: mean | open: hit | all at the current price: mean | hit | vs basket | verdict (closed) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| early_rally_beaten_down | 101 | 0 |  |  |  |  | 60% | +4.32% | 79% | +4.32% | 85% | +0.96% | too early |
| falling_wedge_beaten_down | 33 | 9 | +0.32% | 56% | -0.14% | -0.56% | 60% | +4.22% | 83% | +3.15% | 76% | -0.15% | too early |
| growth_top10 | 13 | 0 |  |  |  |  |  | -9.53% | 23% | -9.53% | 23% | -10.33% | too early |
| insider_buy_beaten_down | 4 | 0 |  |  |  |  | 68% | +5.79% | 75% | +5.79% | 75% | +3.25% | too early |
| jev_pick | 27 | 0 |  |  |  |  |  | +3.86% | 67% | +3.86% | 72% | -1.82% | too early |
| jev_skip | 3 | 0 |  |  |  |  |  | +5.50% | 100% | +5.50% | 100% | +4.67% | too early |
| newsday | 17 | 0 |  |  |  |  | 62% | +2.87% | 59% | +2.87% | 59% | -1.83% | too early |

## What changed since the previous review

- insider buys, other (to date): noise so far -> not working so far
- read: signs of a bottom (to date): noise so far -> better without it
- 'market-wide' among the causes of the decline (to date): noise so far -> better without it
- checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (to date): noise so far -> better without it
- signal-day volume above 1.5x (to date): better without it -> noise so far

## Method

Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather than the result of a fixed rule). Table verdict: 20+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= 2; 'not working' when negative with t <= -2; 'noise' otherwise. Condition verdict: 12+ names on each side, Welch t on the difference in basket excess; |t| >= 2 names the better side. Journal rule: 10+ closed trades; 'on track' when the mean is positive and the hit rate is within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a forward test, not investment advice.
