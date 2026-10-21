# AlgoVision review: what has worked so far - 2026-10-21

What in the daily report is actually relevant on the evidence so far: 31 dated reports, 2026-09-05 to 2026-10-19. Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), not judgement: a table 'works' only with 20+ names and a t of 2 or more on the basket excess; a condition 'separates' only with 12+ names on each side and a t of 2 or more on the difference. The windows overlap and the sample is a few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year backtests decide what enters the report.

## Bottom line

### 20 bars after the listing

**Works or separates so far:** sentiment read positive (diff +3.7%, n 16/53, t 2.4); 20-day return above the peer group (vs peers 20d > 0) (diff +3.5%, n 24/45, t 2.0)

**Not working, or the other side did better:** none

**Noise so far:** falling wedge, forming (watch list) (n 48, vs basket -0.3%, t -0.4); insider buys, other (n 23, vs basket +1.9%, t 1.4); growth screen (retired) (n 22, vs basket +1.5%, t 0.7); S: negative sentiment (warning) (diff +1.3%, n 21/48, t 0.9); no warning flag at all (diff +0.7%, n 42/27, t 0.5); read: signs of a bottom (diff -0.2%, n 25/44, t -0.1); 'market-wide' among the causes of the decline (diff -0.9%, n 18/51, t -0.5); analyst consensus buy / strong buy (diff +1.5%, n 56/13, t 0.7); more than 30% below the 52-week high (diff -1.0%, n 26/43, t -0.6); listed 1-3 days (fresh) vs 4+ days (diff -0.4%, n 14/66, t -0.2); peer group beaten down too (diff +1.0%, n 13/15, t 0.6)

**Too early to say:** news-day (n 9, vs basket -3.3%, t -1.5); falling wedge (confirmed) (n 9, vs basket +4.0%, t 2.0); insider buys, beaten-down (n 14, vs basket +2.0%, t 1.0); early rally (n 0, vs basket , t ); Jev decision (n 0, vs basket , t ); Z: z vs peers below -1 (warning) (diff -3.3%, n 4/65, t -3.5); T: target upside above 50% (warning) (diff -6.9%, n 4/65, t -6.5); D: more than 40% below the 52-week high (a plus over ten years) (diff -0.3%, n 10/59, t -0.1); read: still falling (diff +6.5%, n 2/67, t ); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff , n 0/0, t ); 6-month return below -30% (diff -3.3%, n 9/62, t -1.5); signal-day volume above 1.5x (diff , n 0/8, t ); a 3x+ volume day in the last 10 bars (diff , n 0/8, t ); early rally: two or more rules fired (diff , n 0/0, t ); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff , n 0/0, t ); Jev: P(buy) < 0.2 (diff , n 0/0, t )

### To date (against the current price, every name listed)

**Works or separates so far:** peer group beaten down too (diff +1.6%, n 66/121, t 2.6)

**Not working, or the other side did better:** growth screen (retired) (n 22, vs basket -5.8%, t -3.0); signal-day volume above 1.5x (diff -4.7%, n 12/132, t -2.3)

**Noise so far:** falling wedge (confirmed) (n 37, vs basket +0.4%, t 0.7); early rally (n 89, vs basket -0.3%, t -0.6); falling wedge, forming (watch list) (n 96, vs basket +0.1%, t 0.2); insider buys, other (n 26, vs basket -2.0%, t -1.3); Jev decision (n 76, vs basket -0.4%, t -0.6); Z: z vs peers below -1 (warning) (diff -0.5%, n 17/130, t -0.3); S: negative sentiment (warning) (diff +0.7%, n 39/108, t 0.7); D: more than 40% below the 52-week high (a plus over ten years) (diff -2.5%, n 22/125, t -1.3); no warning flag at all (diff +0.2%, n 89/58, t 0.2); read: signs of a bottom (diff -2.1%, n 50/97, t -1.7); 'market-wide' among the causes of the decline (diff -1.6%, n 45/102, t -1.4); sentiment read positive (diff +1.2%, n 39/108, t 1.2); analyst consensus buy / strong buy (diff +0.1%, n 120/27, t 0.1); more than 30% below the 52-week high (diff -1.5%, n 62/85, t -1.3); 20-day return above the peer group (vs peers 20d > 0) (diff +1.7%, n 48/99, t 1.5); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff -1.6%, n 17/15, t -1.5); listed 1-3 days (fresh) vs 4+ days (diff +0.9%, n 87/168, t 1.5); 6-month return below -30% (diff -2.3%, n 23/216, t -1.5); early rally: two or more rules fired (diff -1.2%, n 15/74, t -0.8); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff -0.3%, n 15/61, t -0.1); Jev: P(buy) < 0.2 (diff +1.0%, n 34/42, t 0.7)

**Too early to say:** news-day (n 16, vs basket -2.9%, t -1.5); insider buys, beaten-down (n 17, vs basket -0.2%, t -0.2); T: target upside above 50% (warning) (diff -6.5%, n 9/138, t -2.7); read: still falling (diff +1.8%, n 9/138, t 1.3); a 3x+ volume day in the last 10 bars (diff +3.2%, n 2/53, t )

## By table (20 bars)

| table | n | n20 | ret 20 | hit 20 | vs SPY 20 | vs basket 20 | t 20 | verdict 20 | to date | hit | vs SPY | vs basket | t | verdict to date | research expected | same sign in both halves |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|:--|:--|:--|
| news-day | 16 | 9 | -6.8% | 11% | -8.3% | -3.3% | -1.5 | too early | -0.9% | 50% | -1.1% | -2.9% | -1.5 | too early | +6-7% vs random at 60 bars |  |
| falling wedge (confirmed) | 37 | 9 | +1.9% | 67% | +0.9% | +4.0% | 2.0 | too early | +3.0% | 81% | +3.3% | +0.4% | 0.7 | noise so far | +3% vs random at 20 bars |  |
| insider buys, beaten-down | 17 | 14 | -1.6% | 43% | -3.2% | +2.0% | 1.0 | too early | -0.4% | 41% | -0.8% | -0.2% | -0.2 | too early | +10% vs random at 60 bars |  |
| early rally | 89 | 0 |  |  |  |  |  | too early | +2.2% | 81% | +2.9% | -0.3% | -0.6 | noise so far | +2-3% net, ~0 vs SPY at 20 bars |  |
| falling wedge, forming (watch list) | 96 | 48 | -3.0% | 35% | -4.5% | -0.3% | -0.4 | noise so far | +2.1% | 66% | +1.8% | +0.1% | 0.2 | noise so far | no edge (a stock still falling) |  |
| insider buys, other | 26 | 23 | -2.4% | 22% | -3.9% | +1.9% | 1.4 | noise so far | -2.2% | 46% | -2.6% | -2.0% | -1.3 | noise so far | no edge |  |
| Jev decision | 76 | 0 |  |  |  |  |  | too early | +5.1% | 86% | +5.5% | -0.4% | -0.6 | noise so far | untested (forward test only) |  |
| growth screen (retired) | 22 | 22 | -3.4% | 36% | -5.2% | +1.5% | 0.7 | noise so far | -6.8% | 32% | -7.4% | -5.8% | -3.0 | not working so far | retired |  |

## By condition (basket excess, with vs without; 20 bars and to date)

| condition | n with | n without | ret 20 with | ret 20 without | hit 20 with | hit 20 without | vs basket 20 with | vs basket 20 without | diff 20 | t 20 | verdict 20 | n with (to date) | n without | ret with | ret without | vs basket with | vs basket without | diff | t | verdict to date |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| Z: z vs peers below -1 (warning) | 4 | 65 | -2.3% | +1.0% | 0% | 72% | -4.2% | -0.9% | -3.3% | -3.5 | too early | 17 | 130 | +1.5% | +2.9% | -0.9% | -0.4% | -0.5% | -0.3 | noise so far |
| S: negative sentiment (warning) | 21 | 48 | +1.7% | +0.4% | 71% | 67% | -0.1% | -1.5% | +1.3% | 0.9 | noise so far | 39 | 108 | +2.9% | +2.6% | +0.0% | -0.6% | +0.7% | 0.7 | noise so far |
| T: target upside above 50% (warning) | 4 | 65 | -5.7% | +1.2% | 0% | 72% | -7.6% | -0.7% | -6.9% | -6.5 | too early | 9 | 138 | -3.2% | +3.1% | -6.5% | -0.1% | -6.5% | -2.7 | too early |
| D: more than 40% below the 52-week high (a plus over ten years) | 10 | 59 | +0.5% | +0.9% | 70% | 68% | -1.3% | -1.0% | -0.3% | -0.1 | too early | 22 | 125 | +0.6% | +3.1% | -2.6% | -0.1% | -2.5% | -1.3 | noise so far |
| no warning flag at all | 42 | 27 | +1.1% | +0.4% | 76% | 56% | -0.8% | -1.5% | +0.7% | 0.5 | noise so far | 89 | 58 | +3.1% | +2.2% | -0.4% | -0.6% | +0.2% | 0.2 | noise so far |
| read: signs of a bottom | 25 | 44 | +0.7% | +0.9% | 68% | 68% | -1.2% | -1.0% | -0.2% | -0.1 | noise so far | 50 | 97 | +1.6% | +3.3% | -1.9% | +0.3% | -2.1% | -1.7 | noise so far |
| read: still falling | 2 | 67 | +7.1% | +0.6% | 100% | 67% | +5.2% | -1.3% | +6.5% |  | too early | 9 | 138 | +3.3% | +2.7% | +1.2% | -0.6% | +1.8% | 1.3 | too early |
| 'market-wide' among the causes of the decline | 18 | 51 | +0.1% | +1.1% | 67% | 69% | -1.7% | -0.8% | -0.9% | -0.5 | noise so far | 45 | 102 | +2.0% | +3.1% | -1.6% | +0.0% | -1.6% | -1.4 | noise so far |
| sentiment read positive | 16 | 53 | +3.7% | -0.0% | 88% | 62% | +1.8% | -1.9% | +3.7% | 2.4 | better with the condition | 39 | 108 | +3.5% | +2.4% | +0.4% | -0.8% | +1.2% | 1.2 | noise so far |
| analyst consensus buy / strong buy | 56 | 13 | +1.1% | -0.4% | 66% | 77% | -0.8% | -2.3% | +1.5% | 0.7 | noise so far | 120 | 27 | +2.8% | +2.5% | -0.5% | -0.5% | +0.1% | 0.1 | noise so far |
| more than 30% below the 52-week high | 26 | 43 | +0.2% | +1.2% | 62% | 72% | -1.7% | -0.7% | -1.0% | -0.6 | noise so far | 62 | 85 | +1.9% | +3.3% | -1.3% | +0.2% | -1.5% | -1.3 | noise so far |
| 20-day return above the peer group (vs peers 20d > 0) | 24 | 45 | +3.1% | -0.4% | 92% | 56% | +1.2% | -2.3% | +3.5% | 2.0 | better with the condition | 48 | 99 | +3.9% | +2.1% | +0.7% | -1.0% | +1.7% | 1.5 | noise so far |
| checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 17 | 15 | +1.5% | +3.4% | -0.8% | +0.8% | -1.6% | -1.5 | noise so far |
| listed 1-3 days (fresh) vs 4+ days | 14 | 66 | -3.0% | -2.5% | 29% | 39% | -0.0% | +0.3% | -0.4% | -0.2 | noise so far | 87 | 168 | +2.7% | +1.5% | +0.4% | -0.5% | +0.9% | 1.5 | noise so far |
| peer group beaten down too | 13 | 15 | -2.6% | -2.7% | 38% | 33% | +0.7% | -0.2% | +1.0% | 0.6 | noise so far | 66 | 121 | +3.6% | +1.7% | +0.9% | -0.7% | +1.6% | 2.6 | better with the condition |
| 6-month return below -30% | 9 | 62 | -5.9% | -1.6% | 22% | 44% | -2.2% | +1.1% | -3.3% | -1.5 | too early | 23 | 216 | -0.6% | +2.4% | -2.1% | +0.2% | -2.3% | -1.5 | noise so far |
| signal-day volume above 1.5x | 0 | 8 |  | -3.3% |  | 38% |  | -0.0% |  |  | too early | 12 | 132 | -1.7% | +2.1% | -4.8% | -0.1% | -4.7% | -2.3 | better without it |
| a 3x+ volume day in the last 10 bars | 0 | 8 |  | -3.3% |  | 38% |  | -0.0% |  |  | too early | 2 | 53 | +4.0% | +1.2% | +2.3% | -0.9% | +3.2% |  | too early |
| early rally: two or more rules fired | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 74 | +1.0% | +2.4% | -1.3% | -0.1% | -1.2% | -0.8 | noise so far |
| Jev: P(buy) >= 0.6 (the jev_pick rule) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 61 | +4.9% | +5.2% | -0.7% | -0.4% | -0.3% | -0.1 | noise so far |
| Jev: P(buy) < 0.2 | 0 | 0 |  |  |  |  |  |  |  |  | too early | 34 | 42 | +5.6% | +4.7% | +0.1% | -0.9% | +1.0% | 0.7 | noise so far |

## The journal: closed trades against the research expectation

| rule | logged | closed | closed mean | closed hit | vs SPY | vs basket | expected hit | open: mean | open: hit | all at the current price: mean | hit | vs basket | verdict (closed) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| early_rally_beaten_down | 93 | 0 |  |  |  |  | 60% | +2.30% | 76% | +2.30% | 83% | +0.03% | too early |
| falling_wedge_beaten_down | 33 | 6 | -0.63% | 50% | -1.23% | +0.71% | 60% | +2.65% | 74% | +2.02% | 74% | -0.25% | too early |
| growth_top10 | 13 | 0 |  |  |  |  |  | -8.07% | 23% | -8.07% | 23% | -6.83% | too early |
| insider_buy_beaten_down | 4 | 0 |  |  |  |  | 68% | +2.86% | 75% | +2.86% | 75% | +1.92% | too early |
| jev_pick | 18 | 0 |  |  |  |  |  | +4.74% | 78% | +4.74% | 78% | -0.87% | too early |
| newsday | 17 | 0 |  |  |  |  | 62% | +2.91% | 53% | +2.91% | 53% | +0.15% | too early |

## What changed since the previous review

No verdict changed since 2026-10-20.

## Method

Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather than the result of a fixed rule). Table verdict: 20+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= 2; 'not working' when negative with t <= -2; 'noise' otherwise. Condition verdict: 12+ names on each side, Welch t on the difference in basket excess; |t| >= 2 names the better side. Journal rule: 10+ closed trades; 'on track' when the mean is positive and the hit rate is within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a forward test, not investment advice.
