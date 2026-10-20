# AlgoVision review: what has worked so far - 2026-10-20

What in the daily report is actually relevant on the evidence so far: 30 dated reports, 2026-09-05 to 2026-10-16. Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), not judgement: a table 'works' only with 20+ names and a t of 2 or more on the basket excess; a condition 'separates' only with 12+ names on each side and a t of 2 or more on the difference. The windows overlap and the sample is a few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year backtests decide what enters the report.

## Bottom line

### 20 bars after the listing

**Works or separates so far:** sentiment read positive (diff +3.8%, n 14/49, t 2.2)

**Not working, or the other side did better:** none

**Noise so far:** falling wedge, forming (watch list) (n 44, vs basket -0.2%, t -0.3); insider buys, other (n 22, vs basket +2.2%, t 1.6); growth screen (retired) (n 22, vs basket +1.5%, t 0.7); S: negative sentiment (warning) (diff +0.6%, n 20/43, t 0.4); no warning flag at all (diff +1.5%, n 37/26, t 1.0); read: signs of a bottom (diff -0.6%, n 23/40, t -0.3); 'market-wide' among the causes of the decline (diff -1.3%, n 17/46, t -0.6); analyst consensus buy / strong buy (diff +1.2%, n 51/12, t 0.5); more than 30% below the 52-week high (diff -0.9%, n 23/40, t -0.5); 20-day return above the peer group (vs peers 20d > 0) (diff +3.0%, n 23/40, t 1.7); listed 1-3 days (fresh) vs 4+ days (diff -0.4%, n 14/60, t -0.3); peer group beaten down too (diff +1.7%, n 12/13, t 1.0)

**Too early to say:** news-day (n 9, vs basket -3.3%, t -1.5); falling wedge (confirmed) (n 8, vs basket +3.9%, t 1.7); insider buys, beaten-down (n 13, vs basket +2.1%, t 1.0); early rally (n 0, vs basket , t ); Jev decision (n 0, vs basket , t ); Z: z vs peers below -1 (warning) (diff -3.3%, n 4/59, t -3.5); T: target upside above 50% (warning) (diff -7.0%, n 4/59, t -6.4); D: more than 40% below the 52-week high (a plus over ten years) (diff -1.7%, n 9/54, t -0.5); read: still falling (diff +2.2%, n 1/62, t ); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff , n 0/0, t ); 6-month return below -30% (diff -5.0%, n 8/57, t -2.5); signal-day volume above 1.5x (diff , n 0/7, t ); a 3x+ volume day in the last 10 bars (diff , n 0/7, t ); early rally: two or more rules fired (diff , n 0/0, t ); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff , n 0/0, t ); Jev: P(buy) < 0.2 (diff , n 0/0, t )

### To date (against the current price, every name listed)

**Works or separates so far:** peer group beaten down too (diff +1.3%, n 65/119, t 2.4)

**Not working, or the other side did better:** growth screen (retired) (n 22, vs basket -4.8%, t -2.6); signal-day volume above 1.5x (diff -4.0%, n 12/129, t -2.2)

**Noise so far:** falling wedge (confirmed) (n 37, vs basket +0.3%, t 0.5); early rally (n 88, vs basket -0.3%, t -0.8); falling wedge, forming (watch list) (n 94, vs basket +0.1%, t 0.2); insider buys, other (n 26, vs basket -1.7%, t -1.1); Jev decision (n 76, vs basket -0.3%, t -0.4); Z: z vs peers below -1 (warning) (diff -1.6%, n 16/129, t -1.4); S: negative sentiment (warning) (diff +0.4%, n 39/106, t 0.4); D: more than 40% below the 52-week high (a plus over ten years) (diff -2.3%, n 22/123, t -1.3); no warning flag at all (diff +0.6%, n 88/57, t 0.6); read: signs of a bottom (diff -1.4%, n 49/96, t -1.1); 'market-wide' among the causes of the decline (diff -1.2%, n 44/101, t -1.0); sentiment read positive (diff +1.4%, n 38/107, t 1.5); analyst consensus buy / strong buy (diff +0.6%, n 119/26, t 0.5); more than 30% below the 52-week high (diff -1.7%, n 61/84, t -1.5); 20-day return above the peer group (vs peers 20d > 0) (diff +2.0%, n 48/97, t 1.8); listed 1-3 days (fresh) vs 4+ days (diff +0.7%, n 104/147, t 1.3); 6-month return below -30% (diff -1.9%, n 23/212, t -1.3); early rally: two or more rules fired (diff -1.3%, n 15/73, t -0.9); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff +0.3%, n 15/61, t 0.1); Jev: P(buy) < 0.2 (diff +0.5%, n 34/42, t 0.4)

**Too early to say:** news-day (n 16, vs basket -2.4%, t -1.2); insider buys, beaten-down (n 16, vs basket -0.2%, t -0.2); T: target upside above 50% (warning) (diff -5.5%, n 9/136, t -2.4); read: still falling (diff +1.5%, n 9/136, t 1.0); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff -1.2%, n 17/11, t -1.0); a 3x+ volume day in the last 10 bars (diff +2.7%, n 2/51, t )

## By table (20 bars)

| table | n | n20 | ret 20 | hit 20 | vs SPY 20 | vs basket 20 | t 20 | verdict 20 | to date | hit | vs SPY | vs basket | t | verdict to date | research expected | same sign in both halves |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|:--|:--|:--|
| news-day | 16 | 9 | -6.8% | 11% | -8.3% | -3.3% | -1.5 | too early | -1.8% | 44% | -1.6% | -2.4% | -1.2 | too early | +6-7% vs random at 60 bars |  |
| falling wedge (confirmed) | 37 | 8 | +1.2% | 62% | -0.0% | +3.9% | 1.7 | too early | +1.5% | 68% | +2.2% | +0.3% | 0.5 | noise so far | +3% vs random at 20 bars |  |
| insider buys, beaten-down | 16 | 13 | -1.9% | 38% | -3.6% | +2.1% | 1.0 | too early | -1.7% | 31% | -1.8% | -0.2% | -0.2 | too early | +10% vs random at 60 bars |  |
| early rally | 88 | 0 |  |  |  |  |  | too early | +0.9% | 61% | +1.9% | -0.3% | -0.8 | noise so far | +2-3% net, ~0 vs SPY at 20 bars |  |
| falling wedge, forming (watch list) | 94 | 44 | -3.3% | 32% | -5.1% | -0.2% | -0.3 | noise so far | +0.8% | 60% | +0.8% | +0.1% | 0.2 | noise so far | no edge (a stock still falling) |  |
| insider buys, other | 26 | 22 | -2.3% | 23% | -3.9% | +2.2% | 1.6 | noise so far | -3.2% | 42% | -3.2% | -1.7% | -1.1 | noise so far | no edge |  |
| Jev decision | 76 | 0 |  |  |  |  |  | too early | +3.9% | 82% | +4.6% | -0.3% | -0.4 | noise so far | untested (forward test only) |  |
| growth screen (retired) | 22 | 22 | -3.4% | 36% | -5.2% | +1.5% | 0.7 | noise so far | -7.1% | 27% | -7.3% | -4.8% | -2.6 | not working so far | retired |  |

## By condition (basket excess, with vs without; 20 bars and to date)

| condition | n with | n without | ret 20 with | ret 20 without | hit 20 with | hit 20 without | vs basket 20 with | vs basket 20 without | diff 20 | t 20 | verdict 20 | n with (to date) | n without | ret with | ret without | vs basket with | vs basket without | diff | t | verdict to date |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| Z: z vs peers below -1 (warning) | 4 | 59 | -2.3% | +1.1% | 0% | 73% | -4.2% | -0.8% | -3.3% | -3.5 | too early | 16 | 129 | -0.8% | +1.7% | -1.9% | -0.3% | -1.6% | -1.4 | noise so far |
| S: negative sentiment (warning) | 20 | 43 | +1.3% | +0.6% | 70% | 67% | -0.6% | -1.2% | +0.6% | 0.4 | noise so far | 39 | 106 | +1.4% | +1.4% | -0.2% | -0.6% | +0.4% | 0.4 | noise so far |
| T: target upside above 50% (warning) | 4 | 59 | -5.7% | +1.3% | 0% | 73% | -7.6% | -0.6% | -7.0% | -6.4 | too early | 9 | 136 | -3.7% | +1.7% | -5.7% | -0.2% | -5.5% | -2.4 | too early |
| D: more than 40% below the 52-week high (a plus over ten years) | 9 | 54 | -0.6% | +1.1% | 67% | 69% | -2.5% | -0.8% | -1.7% | -0.5 | too early | 22 | 123 | -0.6% | +1.7% | -2.5% | -0.2% | -2.3% | -1.3 | noise so far |
| no warning flag at all | 37 | 26 | +1.5% | -0.1% | 78% | 54% | -0.4% | -1.9% | +1.5% | 1.0 | noise so far | 88 | 57 | +1.9% | +0.6% | -0.3% | -0.9% | +0.6% | 0.6 | noise so far |
| read: signs of a bottom | 23 | 40 | +0.4% | +1.1% | 65% | 70% | -1.4% | -0.8% | -0.6% | -0.3 | noise so far | 49 | 96 | +0.8% | +1.7% | -1.4% | -0.1% | -1.4% | -1.1 | noise so far |
| read: still falling | 1 | 62 | +3.0% | +0.8% | 100% | 68% | +1.2% | -1.1% | +2.2% |  | too early | 9 | 136 | +1.7% | +1.4% | +0.9% | -0.6% | +1.5% | 1.0 | too early |
| 'market-wide' among the causes of the decline | 17 | 46 | -0.1% | +1.2% | 65% | 70% | -2.0% | -0.7% | -1.3% | -0.6 | noise so far | 44 | 101 | +0.9% | +1.6% | -1.3% | -0.2% | -1.2% | -1.0 | noise so far |
| sentiment read positive | 14 | 49 | +3.8% | -0.0% | 86% | 63% | +1.9% | -1.9% | +3.8% | 2.2 | better with the condition | 38 | 107 | +2.4% | +1.0% | +0.5% | -0.9% | +1.4% | 1.5 | noise so far |
| analyst consensus buy / strong buy | 51 | 12 | +1.1% | -0.2% | 65% | 83% | -0.8% | -2.0% | +1.2% | 0.5 | noise so far | 119 | 26 | +1.5% | +0.8% | -0.4% | -1.0% | +0.6% | 0.5 | noise so far |
| more than 30% below the 52-week high | 23 | 40 | +0.2% | +1.2% | 61% | 72% | -1.6% | -0.7% | -0.9% | -0.5 | noise so far | 61 | 84 | +0.4% | +2.1% | -1.5% | +0.2% | -1.7% | -1.5 | noise so far |
| 20-day return above the peer group (vs peers 20d > 0) | 23 | 40 | +2.7% | -0.2% | 91% | 55% | +0.9% | -2.1% | +3.0% | 1.7 | noise so far | 48 | 97 | +2.8% | +0.7% | +0.8% | -1.2% | +2.0% | 1.8 | noise so far |
| checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 17 | 11 | +0.8% | +2.8% | -0.2% | +1.1% | -1.2% | -1.0 | too early |
| listed 1-3 days (fresh) vs 4+ days | 14 | 60 | -3.0% | -3.0% | 29% | 35% | -0.0% | +0.4% | -0.4% | -0.3 | noise so far | 104 | 147 | +0.9% | +0.4% | +0.2% | -0.5% | +0.7% | 1.3 | noise so far |
| peer group beaten down too | 12 | 13 | -3.0% | -4.2% | 33% | 23% | +0.7% | -1.0% | +1.7% | 1.0 | noise so far | 65 | 119 | +2.1% | +0.5% | +0.7% | -0.6% | +1.3% | 2.4 | better with the condition |
| 6-month return below -30% | 8 | 57 | -8.0% | -1.7% | 12% | 40% | -3.6% | +1.4% | -5.0% | -2.5 | too early | 23 | 212 | -1.6% | +1.0% | -1.7% | +0.1% | -1.9% | -1.3 | noise so far |
| signal-day volume above 1.5x | 0 | 7 |  | -5.4% |  | 29% |  | -1.3% |  |  | too early | 12 | 129 | -2.5% | +0.7% | -4.3% | -0.3% | -4.0% | -2.2 | better without it |
| a 3x+ volume day in the last 10 bars | 0 | 7 |  | -5.4% |  | 29% |  | -1.3% |  |  | too early | 2 | 51 | +1.9% | -0.4% | +1.4% | -1.2% | +2.7% |  | too early |
| early rally: two or more rules fired | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 73 | -0.5% | +1.1% | -1.4% | -0.1% | -1.3% | -0.9 | noise so far |
| Jev: P(buy) >= 0.6 (the jev_pick rule) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 61 | +4.1% | +3.8% | -0.1% | -0.3% | +0.3% | 0.1 | noise so far |
| Jev: P(buy) < 0.2 | 0 | 0 |  |  |  |  |  |  |  |  | too early | 34 | 42 | +4.1% | +3.7% | +0.0% | -0.5% | +0.5% | 0.4 | noise so far |

## The journal: closed trades against the research expectation

| rule | logged | closed | closed mean | closed hit | vs SPY | vs basket | expected hit | open: mean | open: hit | all at the current price: mean | hit | vs basket | verdict (closed) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| early_rally_beaten_down | 86 | 0 |  |  |  |  | 60% | +0.96% | 63% | +0.96% | 64% | -0.04% | too early |
| falling_wedge_beaten_down | 31 | 6 | -0.63% | 50% | -1.23% | +0.71% | 60% | +0.97% | 60% | +0.66% | 58% | -0.54% | too early |
| growth_top10 | 13 | 0 |  |  |  |  |  | -8.60% | 15% | -8.60% | 15% | -6.03% | too early |
| insider_buy_beaten_down | 4 | 0 |  |  |  |  | 68% | +2.02% | 75% | +2.02% | 75% | +2.38% | too early |
| jev_pick | 18 | 0 |  |  |  |  |  | +4.03% | 78% | +4.03% | 78% | -0.14% | too early |
| newsday | 17 | 0 |  |  |  |  | 62% | +1.77% | 47% | +1.77% | 47% | +0.37% | too early |

## What changed since the previous review

No verdict changed since 2026-10-20.

## Method

Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather than the result of a fixed rule). Table verdict: 20+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= 2; 'not working' when negative with t <= -2; 'noise' otherwise. Condition verdict: 12+ names on each side, Welch t on the difference in basket excess; |t| >= 2 names the better side. Journal rule: 10+ closed trades; 'on track' when the mean is positive and the hit rate is within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a forward test, not investment advice.
