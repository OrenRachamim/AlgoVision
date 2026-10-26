# AlgoVision review: what has worked so far - 2026-10-26

What in the daily report is actually relevant on the evidence so far: 34 dated reports, 2026-09-05 to 2026-10-22. Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), not judgement: a table 'works' only with 20+ names and a t of 2 or more on the basket excess; a condition 'separates' only with 12+ names on each side and a t of 2 or more on the difference. The windows overlap and the sample is a few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year backtests decide what enters the report.

## Bottom line

### 20 bars after the listing

**Works or separates so far:** sentiment read positive (diff +3.5%, n 17/62, t 2.3); 20-day return above the peer group (vs peers 20d > 0) (diff +3.8%, n 29/50, t 2.4)

**Not working, or the other side did better:** none

**Noise so far:** falling wedge, forming (watch list) (n 56, vs basket +0.2%, t 0.3); insider buys, other (n 24, vs basket +1.8%, t 1.4); growth screen (retired) (n 22, vs basket +1.5%, t 0.7); S: negative sentiment (warning) (diff -0.3%, n 25/54, t -0.2); no warning flag at all (diff +1.7%, n 47/32, t 1.1); read: signs of a bottom (diff -1.4%, n 30/49, t -0.8); 'market-wide' among the causes of the decline (diff -1.3%, n 18/61, t -0.7); analyst consensus buy / strong buy (diff +0.3%, n 65/14, t 0.1); more than 30% below the 52-week high (diff -0.8%, n 31/48, t -0.4); listed 1-3 days (fresh) vs 4+ days (diff +1.1%, n 17/75, t 0.7); peer group beaten down too (diff +1.8%, n 15/21, t 1.3)

**Too early to say:** news-day (n 10, vs basket -5.3%, t -1.9); falling wedge (confirmed) (n 12, vs basket +2.3%, t 1.3); insider buys, beaten-down (n 14, vs basket +2.0%, t 1.0); early rally (n 0, vs basket , t ); MA200 cross after a long run below (n 0, vs basket , t ); Jev decision (n 0, vs basket , t ); Z: z vs peers below -1 (warning) (diff -6.6%, n 6/73, t -3.0); T: target upside above 50% (warning) (diff -4.6%, n 5/74, t -1.7); D: more than 40% below the 52-week high (a plus over ten years) (diff -2.3%, n 11/68, t -0.7); read: still falling (diff +6.1%, n 2/77, t ); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff , n 0/0, t ); 6-month return below -30% (diff -4.1%, n 10/72, t -1.9); signal-day volume above 1.5x (diff -2.4%, n 1/11, t ); a 3x+ volume day in the last 10 bars (diff , n 0/12, t ); early rally: two or more rules fired (diff , n 0/0, t ); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff , n 0/0, t ); Jev: P(buy) < 0.2 (diff , n 0/0, t )

### To date (against the current price, every name listed)

**Works or separates so far:** read: still falling (diff +3.3%, n 12/144, t 2.5); 20-day return above the peer group (vs peers 20d > 0) (diff +2.6%, n 52/104, t 2.0); peer group beaten down too (diff +3.2%, n 71/137, t 4.0)

**Not working, or the other side did better:** growth screen (retired) (n 22, vs basket -10.0%, t -4.4); read: signs of a bottom (diff -3.6%, n 54/102, t -2.5); 'market-wide' among the causes of the decline (diff -2.8%, n 51/105, t -2.2)

**Noise so far:** falling wedge (confirmed) (n 39, vs basket +0.2%, t 0.2); early rally (n 104, vs basket +0.6%, t 1.1); falling wedge, forming (watch list) (n 97, vs basket +0.1%, t 0.1); insider buys, other (n 26, vs basket -3.2%, t -1.8); Jev decision (n 126, vs basket +0.0%, t 0.0); Z: z vs peers below -1 (warning) (diff -2.3%, n 20/136, t -1.1); S: negative sentiment (warning) (diff +1.2%, n 45/111, t 0.9); D: more than 40% below the 52-week high (a plus over ten years) (diff -3.9%, n 25/131, t -1.7); no warning flag at all (diff +0.7%, n 92/64, t 0.6); sentiment read positive (diff +0.6%, n 42/114, t 0.5); analyst consensus buy / strong buy (diff -2.3%, n 126/30, t -1.6); more than 30% below the 52-week high (diff -2.0%, n 66/90, t -1.5); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff -2.8%, n 22/16, t -1.6); listed 1-3 days (fresh) vs 4+ days (diff +1.6%, n 84/192, t 1.9); 6-month return below -30% (diff -2.7%, n 26/234, t -1.5); signal-day volume above 1.5x (diff -3.0%, n 15/151, t -1.2); early rally: two or more rules fired (diff -1.8%, n 15/89, t -0.8); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff -1.5%, n 23/103, t -0.9); Jev: P(buy) < 0.2 (diff +1.4%, n 66/60, t 1.2)

**Too early to say:** news-day (n 16, vs basket -6.4%, t -2.7); insider buys, beaten-down (n 17, vs basket -1.2%, t -0.8); MA200 cross after a long run below (n 3, vs basket +1.3%, t 0.9); T: target upside above 50% (warning) (diff -12.3%, n 9/147, t -6.2); a 3x+ volume day in the last 10 bars (diff +1.0%, n 2/57, t )

## By table (20 bars)

| table | n | n20 | ret 20 | hit 20 | vs SPY 20 | vs basket 20 | t 20 | verdict 20 | to date | hit | vs SPY | vs basket | t | verdict to date | research expected | same sign in both halves |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|:--|:--|:--|
| news-day | 16 | 10 | -7.8% | 10% | -9.1% | -5.3% | -1.9 | too early | -3.6% | 38% | -2.6% | -6.4% | -2.7 | too early | +6-7% vs random at 60 bars |  |
| falling wedge (confirmed) | 39 | 12 | +2.2% | 75% | +1.5% | +2.3% | 1.3 | too early | +3.2% | 82% | +4.6% | +0.2% | 0.2 | noise so far | +3% vs random at 20 bars |  |
| insider buys, beaten-down | 17 | 14 | -1.6% | 43% | -3.2% | +2.0% | 1.0 | too early | -0.6% | 41% | +0.1% | -1.2% | -0.8 | too early | +10% vs random at 60 bars |  |
| early rally | 104 | 0 |  |  |  |  |  | too early | +2.9% | 74% | +4.6% | +0.6% | 1.1 | noise so far | +2-3% net, ~0 vs SPY at 20 bars |  |
| MA200 cross after a long run below | 3 | 0 |  |  |  |  |  | too early | +0.8% | 67% | +1.2% | +1.3% | 0.9 | too early | no edge in both periods |  |
| falling wedge, forming (watch list) | 97 | 56 | -1.5% | 43% | -2.8% | +0.2% | 0.3 | noise so far | +2.8% | 66% | +3.6% | +0.1% | 0.1 | noise so far | no edge (a stock still falling) |  |
| insider buys, other | 26 | 24 | -2.1% | 25% | -3.6% | +1.8% | 1.4 | noise so far | -2.4% | 54% | -1.6% | -3.2% | -1.8 | noise so far | no edge |  |
| Jev decision | 126 | 0 |  |  |  |  |  | too early | +3.5% | 71% | +5.0% | +0.0% | 0.0 | noise so far | untested (forward test only) |  |
| growth screen (retired) | 22 | 22 | -3.4% | 36% | -5.2% | +1.5% | 0.7 | noise so far | -9.9% | 14% | -9.3% | -10.0% | -4.4 | not working so far | retired |  |

## By condition (basket excess, with vs without; 20 bars and to date)

| condition | n with | n without | ret 20 with | ret 20 without | hit 20 with | hit 20 without | vs basket 20 with | vs basket 20 without | diff 20 | t 20 | verdict 20 | n with (to date) | n without | ret with | ret without | vs basket with | vs basket without | diff | t | verdict to date |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| Z: z vs peers below -1 (warning) | 6 | 73 | -5.0% | +2.0% | 0% | 77% | -6.9% | -0.3% | -6.6% | -3.0 | too early | 20 | 136 | +0.0% | +3.5% | -2.5% | -0.2% | -2.3% | -1.1 | noise so far |
| S: negative sentiment (warning) | 25 | 54 | +1.1% | +1.6% | 68% | 72% | -0.9% | -0.7% | -0.3% | -0.2 | noise so far | 45 | 111 | +3.5% | +2.9% | +0.3% | -0.9% | +1.2% | 0.9 | noise so far |
| T: target upside above 50% (warning) | 5 | 74 | -3.0% | +1.8% | 20% | 74% | -5.1% | -0.5% | -4.6% | -1.7 | too early | 9 | 147 | -8.0% | +3.8% | -12.1% | +0.2% | -12.3% | -6.2 | too early |
| D: more than 40% below the 52-week high (a plus over ten years) | 11 | 68 | -0.8% | +1.8% | 64% | 72% | -2.7% | -0.4% | -2.3% | -0.7 | too early | 25 | 131 | -0.3% | +3.7% | -3.8% | +0.1% | -3.9% | -1.7 | noise so far |
| no warning flag at all | 47 | 32 | +2.3% | +0.3% | 81% | 56% | -0.1% | -1.8% | +1.7% | 1.1 | noise so far | 92 | 64 | +3.7% | +2.2% | -0.2% | -1.0% | +0.7% | 0.6 | noise so far |
| read: signs of a bottom | 30 | 49 | +0.6% | +2.0% | 70% | 71% | -1.6% | -0.2% | -1.4% | -0.8 | noise so far | 54 | 102 | +1.0% | +4.2% | -2.9% | +0.7% | -3.6% | -2.5 | better without it |
| read: still falling | 2 | 77 | +7.1% | +1.3% | 100% | 70% | +5.2% | -0.9% | +6.1% |  | too early | 12 | 144 | +4.1% | +3.0% | +2.5% | -0.8% | +3.3% | 2.5 | better with the condition |
| 'market-wide' among the causes of the decline | 18 | 61 | +0.1% | +1.9% | 67% | 72% | -1.7% | -0.5% | -1.3% | -0.7 | noise so far | 51 | 105 | +1.1% | +4.0% | -2.4% | +0.4% | -2.8% | -2.2 | better without it |
| sentiment read positive | 17 | 62 | +3.9% | +0.8% | 88% | 66% | +2.0% | -1.5% | +3.5% | 2.3 | better with the condition | 42 | 114 | +3.4% | +3.0% | -0.1% | -0.7% | +0.6% | 0.5 | noise so far |
| analyst consensus buy / strong buy | 65 | 14 | +1.5% | +1.1% | 69% | 79% | -0.7% | -1.0% | +0.3% | 0.1 | noise so far | 126 | 30 | +2.7% | +4.5% | -1.0% | +1.3% | -2.3% | -1.6 | noise so far |
| more than 30% below the 52-week high | 31 | 48 | +1.0% | +1.8% | 65% | 75% | -1.3% | -0.4% | -0.8% | -0.4 | noise so far | 66 | 90 | +2.0% | +3.9% | -1.7% | +0.3% | -2.0% | -1.5 | noise so far |
| 20-day return above the peer group (vs peers 20d > 0) | 29 | 50 | +4.0% | +0.0% | 93% | 58% | +1.6% | -2.1% | +3.8% | 2.4 | better with the condition | 52 | 104 | +4.8% | +2.2% | +1.2% | -1.4% | +2.6% | 2.0 | better with the condition |
| checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 22 | 16 | +0.2% | +3.8% | -1.5% | +1.2% | -2.8% | -1.6 | noise so far |
| listed 1-3 days (fresh) vs 4+ days | 17 | 75 | -0.5% | -2.0% | 41% | 44% | +1.1% | -0.1% | +1.1% | 0.7 | noise so far | 84 | 192 | +3.5% | +1.7% | +1.0% | -0.6% | +1.6% | 1.9 | noise so far |
| peer group beaten down too | 15 | 21 | -0.9% | -1.1% | 47% | 48% | +1.1% | -0.6% | +1.8% | 1.3 | noise so far | 71 | 137 | +5.3% | +1.5% | +2.4% | -0.9% | +3.2% | 4.0 | better with the condition |
| 6-month return below -30% | 10 | 72 | -5.5% | -0.3% | 20% | 51% | -2.8% | +1.3% | -4.1% | -1.9 | too early | 26 | 234 | -0.4% | +3.0% | -2.1% | +0.5% | -2.7% | -1.5 | noise so far |
| signal-day volume above 1.5x | 1 | 11 | +2.5% | -2.6% | 100% | 45% | -3.2% | -0.8% | -2.4% |  | too early | 15 | 151 | +0.3% | +2.6% | -2.6% | +0.5% | -3.0% | -1.2 | noise so far |
| a 3x+ volume day in the last 10 bars | 0 | 12 |  | -2.2% |  | 50% |  | -1.0% |  |  | too early | 2 | 57 | +2.3% | +1.6% | +0.3% | -0.7% | +1.0% |  | too early |
| early rally: two or more rules fired | 0 | 0 |  |  |  |  |  |  |  |  | too early | 15 | 89 | +1.6% | +3.1% | -0.9% | +0.9% | -1.8% | -0.8 | noise so far |
| Jev: P(buy) >= 0.6 (the jev_pick rule) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 23 | 103 | +2.7% | +3.7% | -1.2% | +0.3% | -1.5% | -0.9 | noise so far |
| Jev: P(buy) < 0.2 | 0 | 0 |  |  |  |  |  |  |  |  | too early | 66 | 60 | +3.5% | +3.6% | +0.7% | -0.7% | +1.4% | 1.2 | noise so far |

## The journal: closed trades against the research expectation

| rule | logged | closed | closed mean | closed hit | vs SPY | vs basket | expected hit | open: mean | open: hit | all at the current price: mean | hit | vs basket | verdict (closed) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| early_rally_beaten_down | 101 | 0 |  |  |  |  | 60% | +2.94% | 73% | +2.94% | 73% | +0.91% | too early |
| falling_wedge_beaten_down | 33 | 10 | +0.45% | 60% | +0.03% | -0.77% | 60% | +2.64% | 83% | +1.98% | 76% | -0.41% | on track |
| growth_top10 | 13 | 0 |  |  |  |  |  | -11.06% | 23% | -11.06% | 23% | -10.78% | too early |
| insider_buy_beaten_down | 4 | 0 |  |  |  |  | 68% | +4.02% | 75% | +4.02% | 75% | +2.64% | too early |
| jev_pick | 30 | 0 |  |  |  |  |  | +2.56% | 60% | +2.56% | 60% | -1.14% | too early |
| jev_skip | 6 | 0 |  |  |  |  |  | +1.56% | 50% | +1.56% | 50% | +1.84% | too early |
| newsday | 18 | 0 |  |  |  |  | 62% | +0.10% | 39% | +0.10% | 41% | -3.46% | too early |

## What changed since the previous review

- insider buys, other (to date): not working so far -> noise so far
- read: still falling (to date): too early -> better with the condition
- 20-day return above the peer group (vs peers 20d > 0) (to date): noise so far -> better with the condition
- checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (to date): better without it -> noise so far
- falling_wedge_beaten_down (20 bars): too early -> on track

## Method

Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather than the result of a fixed rule). Table verdict: 20+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= 2; 'not working' when negative with t <= -2; 'noise' otherwise. Condition verdict: 12+ names on each side, Welch t on the difference in basket excess; |t| >= 2 names the better side. Journal rule: 10+ closed trades; 'on track' when the mean is positive and the hit rate is within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a forward test, not investment advice.
