# AlgoVision review: what has worked so far - 2026-10-28

What in the daily report is actually relevant on the evidence so far: 36 dated reports, 2026-09-05 to 2026-10-26. Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), not judgement: a table 'works' only with 20+ names and a t of 2 or more on the basket excess; a condition 'separates' only with 12+ names on each side and a t of 2 or more on the difference. The windows overlap and the sample is a few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year backtests decide what enters the report.

## Bottom line

### 20 bars after the listing

**Works or separates so far:** 20-day return above the peer group (vs peers 20d > 0) (diff +3.7%, n 29/53, t 2.4)

**Not working, or the other side did better:** none

**Noise so far:** falling wedge, forming (watch list) (n 57, vs basket +0.1%, t 0.1); insider buys, other (n 24, vs basket +1.8%, t 1.4); growth screen (retired) (n 22, vs basket +1.5%, t 0.7); S: negative sentiment (warning) (diff -0.2%, n 26/56, t -0.1); D: more than 40% below the 52-week high (a plus over ten years) (diff -2.0%, n 12/70, t -0.7); no warning flag at all (diff +1.6%, n 49/33, t 1.1); read: signs of a bottom (diff -1.4%, n 30/52, t -0.8); 'market-wide' among the causes of the decline (diff -1.0%, n 19/63, t -0.5); sentiment read positive (diff +3.0%, n 18/64, t 2.0); analyst consensus buy / strong buy (diff +0.2%, n 67/15, t 0.1); more than 30% below the 52-week high (diff -0.7%, n 32/50, t -0.4); listed 1-3 days (fresh) vs 4+ days (diff +0.5%, n 19/77, t 0.3); peer group beaten down too (diff +2.3%, n 15/24, t 1.7)

**Too early to say:** news-day (n 10, vs basket -5.3%, t -1.9); falling wedge (confirmed) (n 15, vs basket +1.0%, t 0.6); insider buys, beaten-down (n 14, vs basket +2.0%, t 1.0); early rally (n 0, vs basket , t ); MA200 cross after a long run below (n 0, vs basket , t ); Jev decision (n 0, vs basket , t ); Z: z vs peers below -1 (warning) (diff -6.6%, n 6/76, t -3.0); T: target upside above 50% (warning) (diff -4.6%, n 5/77, t -1.7); read: still falling (diff +4.5%, n 3/79, t 1.5); MACD pre-touch probability >= 70% (lines still apart) (diff , n 0/3, t ); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff , n 0/0, t ); 6-month return below -30% (diff -3.8%, n 10/76, t -1.8); signal-day volume above 1.5x (diff -2.0%, n 1/12, t ); a 3x+ volume day in the last 10 bars (diff , n 0/13, t ); early rally: two or more rules fired (diff , n 0/0, t ); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff , n 0/0, t ); Jev: P(buy) < 0.2 (diff , n 0/0, t )

### To date (against the current price, every name listed)

**Works or separates so far:** read: still falling (diff +2.8%, n 12/146, t 2.3); peer group beaten down too (diff +4.1%, n 71/138, t 4.8)

**Not working, or the other side did better:** growth screen (retired) (n 22, vs basket -7.7%, t -4.0); read: signs of a bottom (diff -3.4%, n 56/102, t -2.5)

**Noise so far:** falling wedge (confirmed) (n 39, vs basket +0.4%, t 0.4); early rally (n 104, vs basket +0.1%, t 0.1); falling wedge, forming (watch list) (n 98, vs basket +0.1%, t 0.1); insider buys, other (n 26, vs basket -2.8%, t -1.7); Jev decision (n 128, vs basket -0.3%, t -0.5); Z: z vs peers below -1 (warning) (diff -1.6%, n 21/137, t -0.8); S: negative sentiment (warning) (diff +0.7%, n 45/113, t 0.5); D: more than 40% below the 52-week high (a plus over ten years) (diff -3.3%, n 26/132, t -1.5); no warning flag at all (diff +0.3%, n 93/65, t 0.3); 'market-wide' among the causes of the decline (diff -0.3%, n 53/105, t -0.3); sentiment read positive (diff +0.9%, n 43/115, t 0.7); analyst consensus buy / strong buy (diff -0.9%, n 128/30, t -0.6); more than 30% below the 52-week high (diff -1.7%, n 67/91, t -1.3); 20-day return above the peer group (vs peers 20d > 0) (diff +1.9%, n 52/106, t 1.6); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff -0.9%, n 23/19, t -0.5); listed 1-3 days (fresh) vs 4+ days (diff +1.4%, n 79/200, t 1.6); 6-month return below -30% (diff -2.0%, n 26/235, t -1.2); signal-day volume above 1.5x (diff -2.3%, n 15/152, t -1.0); early rally: two or more rules fired (diff -2.0%, n 15/89, t -1.3); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff -1.5%, n 24/104, t -0.9); Jev: P(buy) < 0.2 (diff +0.5%, n 66/62, t 0.5)

**Too early to say:** news-day (n 18, vs basket -5.3%, t -2.1); insider buys, beaten-down (n 17, vs basket -2.0%, t -1.5); MA200 cross after a long run below (n 3, vs basket -1.4%, t -0.7); T: target upside above 50% (warning) (diff -6.9%, n 10/148, t -2.8); MACD pre-touch probability >= 70% (lines still apart) (diff , n 0/12, t ); a 3x+ volume day in the last 10 bars (diff +1.7%, n 2/58, t )

## By table (20 bars)

| table | n | n20 | ret 20 | hit 20 | vs SPY 20 | vs basket 20 | t 20 | verdict 20 | to date | hit | vs SPY | vs basket | t | verdict to date | research expected | same sign in both halves |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|:--|:--|:--|
| news-day | 18 | 10 | -7.8% | 10% | -9.1% | -5.3% | -1.9 | too early | -2.9% | 39% | -3.2% | -5.3% | -2.1 | too early | +6-7% vs random at 60 bars |  |
| falling wedge (confirmed) | 39 | 15 | +2.2% | 73% | +1.7% | +1.0% | 0.6 | too early | +3.3% | 79% | +3.5% | +0.4% | 0.4 | noise so far | +3% vs random at 20 bars |  |
| insider buys, beaten-down | 17 | 14 | -1.6% | 43% | -3.2% | +2.0% | 1.0 | too early | -1.6% | 41% | -2.1% | -2.0% | -1.5 | too early | +10% vs random at 60 bars |  |
| early rally | 104 | 0 |  |  |  |  |  | too early | +2.5% | 75% | +3.0% | +0.1% | 0.1 | noise so far | +2-3% net, ~0 vs SPY at 20 bars |  |
| MA200 cross after a long run below | 3 | 0 |  |  |  |  |  | too early | -0.5% | 67% | -1.3% | -1.4% | -0.7 | too early | no edge in both periods |  |
| falling wedge, forming (watch list) | 98 | 57 | -1.4% | 44% | -2.7% | +0.1% | 0.1 | noise so far | +2.5% | 64% | +2.1% | +0.1% | 0.1 | noise so far | no edge (a stock still falling) |  |
| insider buys, other | 26 | 24 | -2.1% | 25% | -3.6% | +1.8% | 1.4 | noise so far | -2.4% | 46% | -2.9% | -2.8% | -1.7 | noise so far | no edge |  |
| Jev decision | 128 | 0 |  |  |  |  |  | too early | +3.3% | 70% | +3.5% | -0.3% | -0.5 | noise so far | untested (forward test only) |  |
| growth screen (retired) | 22 | 22 | -3.4% | 36% | -5.2% | +1.5% | 0.7 | noise so far | -8.2% | 14% | -8.8% | -7.7% | -4.0 | not working so far | retired |  |

## By condition (basket excess, with vs without; 20 bars and to date)

| condition | n with | n without | ret 20 with | ret 20 without | hit 20 with | hit 20 without | vs basket 20 with | vs basket 20 without | diff 20 | t 20 | verdict 20 | n with (to date) | n without | ret with | ret without | vs basket with | vs basket without | diff | t | verdict to date |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| Z: z vs peers below -1 (warning) | 6 | 76 | -5.0% | +2.1% | 0% | 78% | -6.9% | -0.3% | -6.6% | -3.0 | too early | 21 | 137 | +0.6% | +3.3% | -2.1% | -0.5% | -1.6% | -0.8 | noise so far |
| S: negative sentiment (warning) | 26 | 56 | +1.3% | +1.8% | 69% | 73% | -0.9% | -0.7% | -0.2% | -0.1 | noise so far | 45 | 113 | +3.0% | +2.8% | -0.2% | -0.9% | +0.7% | 0.5 | noise so far |
| T: target upside above 50% (warning) | 5 | 77 | -3.0% | +1.9% | 20% | 75% | -5.1% | -0.5% | -4.6% | -1.7 | too early | 10 | 148 | -3.3% | +3.3% | -7.1% | -0.2% | -6.9% | -2.8 | too early |
| D: more than 40% below the 52-week high (a plus over ten years) | 12 | 70 | -0.2% | +1.9% | 67% | 73% | -2.5% | -0.5% | -2.0% | -0.7 | noise so far | 26 | 132 | -0.0% | +3.5% | -3.4% | -0.1% | -3.3% | -1.5 | noise so far |
| no warning flag at all | 49 | 33 | +2.4% | +0.5% | 82% | 58% | -0.1% | -1.7% | +1.6% | 1.1 | noise so far | 93 | 65 | +3.3% | +2.3% | -0.5% | -0.9% | +0.3% | 0.3 | noise so far |
| read: signs of a bottom | 30 | 52 | +0.6% | +2.2% | 70% | 73% | -1.6% | -0.2% | -1.4% | -0.8 | noise so far | 56 | 102 | +0.9% | +4.0% | -2.8% | +0.5% | -3.4% | -2.5 | better without it |
| read: still falling | 3 | 79 | +7.1% | +1.4% | 100% | 71% | +3.6% | -0.9% | +4.5% | 1.5 | too early | 12 | 146 | +3.8% | +2.8% | +1.9% | -0.9% | +2.8% | 2.3 | better with the condition |
| 'market-wide' among the causes of the decline | 19 | 63 | +0.6% | +1.9% | 68% | 73% | -1.5% | -0.5% | -1.0% | -0.5 | noise so far | 53 | 105 | +2.6% | +3.0% | -0.9% | -0.6% | -0.3% | -0.3 | noise so far |
| sentiment read positive | 18 | 64 | +3.8% | +1.0% | 89% | 67% | +1.6% | -1.4% | +3.0% | 2.0 | noise so far | 43 | 115 | +3.4% | +2.7% | +0.0% | -0.9% | +0.9% | 0.7 | noise so far |
| analyst consensus buy / strong buy | 67 | 15 | +1.6% | +1.5% | 70% | 80% | -0.7% | -0.9% | +0.2% | 0.1 | noise so far | 128 | 30 | +2.8% | +3.3% | -0.8% | +0.0% | -0.9% | -0.6 | noise so far |
| more than 30% below the 52-week high | 32 | 50 | +1.2% | +1.9% | 66% | 76% | -1.2% | -0.5% | -0.7% | -0.4 | noise so far | 67 | 91 | +1.9% | +3.6% | -1.7% | +0.1% | -1.7% | -1.3 | noise so far |
| 20-day return above the peer group (vs peers 20d > 0) | 29 | 53 | +4.0% | +0.3% | 93% | 60% | +1.6% | -2.1% | +3.7% | 2.4 | better with the condition | 52 | 106 | +4.3% | +2.2% | +0.6% | -1.3% | +1.9% | 1.6 | noise so far |
| MACD pre-touch probability >= 70% (lines still apart) | 0 | 3 |  | -13.6% |  | 0% |  | -15.5% |  |  | too early | 0 | 12 |  | -4.7% |  | -6.9% |  |  | too early |
| checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 23 | 19 | +0.6% | +2.0% | -1.4% | -0.5% | -0.9% | -0.5 | noise so far |
| listed 1-3 days (fresh) vs 4+ days | 19 | 77 | -0.4% | -1.8% | 42% | 45% | +0.4% | -0.1% | +0.5% | 0.3 | noise so far | 79 | 200 | +3.5% | +1.4% | +0.6% | -0.8% | +1.4% | 1.6 | noise so far |
| peer group beaten down too | 15 | 24 | -0.9% | -0.8% | 47% | 50% | +1.1% | -1.2% | +2.3% | 1.7 | noise so far | 71 | 138 | +5.5% | +1.1% | +2.6% | -1.4% | +4.1% | 4.8 | better with the condition |
| 6-month return below -30% | 10 | 76 | -5.5% | -0.2% | 20% | 53% | -2.8% | +1.0% | -3.8% | -1.8 | too early | 26 | 235 | -0.1% | +2.6% | -1.8% | +0.2% | -2.0% | -1.2 | noise so far |
| signal-day volume above 1.5x | 1 | 12 | +2.5% | -2.3% | 100% | 50% | -3.2% | -1.2% | -2.0% |  | too early | 15 | 152 | +0.8% | +2.3% | -2.3% | +0.0% | -2.3% | -1.0 | noise so far |
| a 3x+ volume day in the last 10 bars | 0 | 13 |  | -1.9% |  | 54% |  | -1.3% |  |  | too early | 2 | 58 | +3.1% | +1.6% | +1.0% | -0.7% | +1.7% |  | too early |
| early rally: two or more rules fired | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 89 | +0.9% | +2.8% | -1.6% | +0.4% | -2.0% | -1.3 | noise so far |
| Jev: P(buy) >= 0.6 (the jev_pick rule) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 24 | 104 | +2.4% | +3.5% | -1.5% | +0.0% | -1.5% | -0.9 | noise so far |
| Jev: P(buy) < 0.2 | 0 | 0 |  |  |  |  |  |  |  |  | too early | 66 | 62 | +3.0% | +3.6% | -0.0% | -0.5% | +0.5% | 0.5 | noise so far |

## The journal: closed trades against the research expectation

| rule | logged | closed | closed mean | closed hit | vs SPY | vs basket | expected hit | open: mean | open: hit | all at the current price: mean | hit | vs basket | verdict (closed) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| early_rally_beaten_down | 103 | 0 |  |  |  |  | 60% | +2.60% | 74% | +2.60% | 75% | +0.35% | too early |
| falling_wedge_beaten_down | 34 | 11 | +0.81% | 64% | +0.44% | -0.90% | 60% | +1.87% | 74% | +1.52% | 73% | -0.88% | on track |
| growth_top10 | 13 | 0 |  |  |  |  |  | -8.79% | 23% | -8.79% | 23% | -8.08% | too early |
| insider_buy_beaten_down | 4 | 0 |  |  |  |  | 68% | +2.20% | 75% | +2.20% | 75% | +0.76% | too early |
| jev_pick | 33 | 0 |  |  |  |  |  | +2.20% | 67% | +2.20% | 67% | -1.41% | too early |
| jev_skip | 6 | 0 |  |  |  |  |  | +1.70% | 67% | +1.70% | 67% | +0.69% | too early |
| newsday | 21 | 0 |  |  |  |  | 62% | -1.54% | 38% | -1.54% | 42% | -4.61% | too early |

## What changed since the previous review

- D: more than 40% below the 52-week high (a plus over ten years) (20 bars): too early -> noise so far
- sentiment read positive (20 bars): better with the condition -> noise so far
- 'market-wide' among the causes of the decline (to date): better without it -> noise so far
- 20-day return above the peer group (vs peers 20d > 0) (to date): better with the condition -> noise so far

## Method

Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather than the result of a fixed rule). Table verdict: 20+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= 2; 'not working' when negative with t <= -2; 'noise' otherwise. Condition verdict: 12+ names on each side, Welch t on the difference in basket excess; |t| >= 2 names the better side. Journal rule: 10+ closed trades; 'on track' when the mean is positive and the hit rate is within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a forward test, not investment advice.
