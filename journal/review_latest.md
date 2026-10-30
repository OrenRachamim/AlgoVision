# AlgoVision review: what has worked so far - 2026-10-30

What in the daily report is actually relevant on the evidence so far: 38 dated reports, 2026-09-05 to 2026-10-28. Every name is measured from its first appearance in a table, entry at the next open, over two horizons: 20 bars ahead, and to the current close ('to date': every name ever listed, each over its own holding length), against the beaten-down basket of that day (the fair benchmark for rules that only buy beaten-down stocks) and against the SPY. Every table and condition gets a verdict per horizon. The verdicts are fixed rules (at the end), not judgement: a table 'works' only with 20+ names and a t of 2 or more on the basket excess; a condition 'separates' only with 12+ names on each side and a t of 2 or more on the difference. The windows overlap and the sample is a few weeks in one regime, so the t overstates the evidence; the thresholds are strict on purpose. The review changes no rule: the ten-year backtests decide what enters the report.

## Bottom line

### 20 bars after the listing

**Works or separates so far:** 20-day return above the peer group (vs peers 20d > 0) (diff +3.1%, n 32/56, t 2.1); peer group beaten down too (diff +3.7%, n 19/27, t 2.9)

**Not working, or the other side did better:** none

**Noise so far:** falling wedge, forming (watch list) (n 64, vs basket +0.2%, t 0.2); insider buys, other (n 24, vs basket +1.8%, t 1.4); growth screen (retired) (n 22, vs basket +1.5%, t 0.7); S: negative sentiment (warning) (diff -0.5%, n 26/62, t -0.3); D: more than 40% below the 52-week high (a plus over ten years) (diff -2.2%, n 12/76, t -0.7); no warning flag at all (diff +1.8%, n 55/33, t 1.3); read: signs of a bottom (diff -2.0%, n 31/57, t -1.2); 'market-wide' among the causes of the decline (diff -0.4%, n 23/65, t -0.2); sentiment read positive (diff +2.1%, n 20/68, t 1.4); analyst consensus buy / strong buy (diff +0.1%, n 71/17, t 0.1); more than 30% below the 52-week high (diff -1.4%, n 33/55, t -0.8); listed 1-3 days (fresh) vs 4+ days (diff -0.3%, n 24/79, t -0.2)

**Too early to say:** news-day (n 10, vs basket -5.3%, t -1.9); falling wedge (confirmed) (n 15, vs basket +1.0%, t 0.6); insider buys, beaten-down (n 14, vs basket +2.0%, t 1.0); early rally (n 0, vs basket , t ); MA200 cross after a long run below (n 0, vs basket , t ); Jev decision (n 0, vs basket , t ); Z: z vs peers below -1 (warning) (diff -6.7%, n 6/82, t -3.1); T: target upside above 50% (warning) (diff -4.7%, n 5/83, t -1.8); read: still falling (diff +4.3%, n 3/85, t 1.5); MACD pre-touch probability >= 70% (lines still apart) (diff , n 0/3, t ); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff , n 0/0, t ); 6-month return below -30% (diff -3.8%, n 10/83, t -1.8); signal-day volume above 1.5x (diff -2.0%, n 1/12, t ); a 3x+ volume day in the last 10 bars (diff , n 0/13, t ); early rally: two or more rules fired (diff , n 0/0, t ); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff , n 0/0, t ); Jev: P(buy) < 0.2 (diff , n 0/0, t )

### To date (against the current price, every name listed)

**Works or separates so far:** read: still falling (diff +3.9%, n 12/146, t 3.0); peer group beaten down too (diff +4.5%, n 73/145, t 4.4)

**Not working, or the other side did better:** news-day (n 24, vs basket -4.5%, t -2.2); growth screen (retired) (n 22, vs basket -9.0%, t -4.2); read: signs of a bottom (diff -4.4%, n 56/102, t -3.0)

**Noise so far:** falling wedge (confirmed) (n 42, vs basket +0.9%, t 0.7); early rally (n 109, vs basket +0.2%, t 0.3); falling wedge, forming (watch list) (n 99, vs basket -0.0%, t -0.0); insider buys, other (n 26, vs basket -2.9%, t -1.7); Jev decision (n 128, vs basket -0.2%, t -0.3); Z: z vs peers below -1 (warning) (diff -1.7%, n 21/137, t -0.8); S: negative sentiment (warning) (diff +1.6%, n 45/113, t 1.1); D: more than 40% below the 52-week high (a plus over ten years) (diff -3.0%, n 26/132, t -1.2); no warning flag at all (diff -0.3%, n 93/65, t -0.2); 'market-wide' among the causes of the decline (diff +0.1%, n 53/105, t 0.1); sentiment read positive (diff +0.4%, n 43/115, t 0.3); analyst consensus buy / strong buy (diff -0.4%, n 128/30, t -0.2); more than 30% below the 52-week high (diff -1.3%, n 67/91, t -0.9); 20-day return above the peer group (vs peers 20d > 0) (diff +1.5%, n 52/106, t 1.1); checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) (diff +0.7%, n 23/19, t 0.3); listed 1-3 days (fresh) vs 4+ days (diff +1.1%, n 90/204, t 1.2); 6-month return below -30% (diff -2.5%, n 27/243, t -1.2); signal-day volume above 1.5x (diff -1.6%, n 19/157, t -0.8); early rally: two or more rules fired (diff -1.3%, n 17/92, t -0.7); Jev: P(buy) >= 0.6 (the jev_pick rule) (diff -1.2%, n 24/104, t -0.7); Jev: P(buy) < 0.2 (diff +1.3%, n 66/62, t 1.0)

**Too early to say:** insider buys, beaten-down (n 17, vs basket -2.8%, t -2.0); MA200 cross after a long run below (n 3, vs basket -1.9%, t -0.6); T: target upside above 50% (warning) (diff -6.5%, n 10/148, t -2.4); MACD pre-touch probability >= 70% (lines still apart) (diff , n 0/12, t ); a 3x+ volume day in the last 10 bars (diff +7.0%, n 2/62, t )

## By table (20 bars)

| table | n | n20 | ret 20 | hit 20 | vs SPY 20 | vs basket 20 | t 20 | verdict 20 | to date | hit | vs SPY | vs basket | t | verdict to date | research expected | same sign in both halves |
|:--|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|:--|:--|:--|
| news-day | 24 | 10 | -7.8% | 10% | -9.1% | -5.3% | -1.9 | too early | -1.1% | 42% | -1.3% | -4.5% | -2.2 | not working so far | +6-7% vs random at 60 bars |  |
| falling wedge (confirmed) | 42 | 15 | +2.2% | 73% | +1.7% | +1.0% | 0.6 | too early | +5.2% | 79% | +5.4% | +0.9% | 0.7 | noise so far | +3% vs random at 20 bars |  |
| insider buys, beaten-down | 17 | 14 | -1.6% | 43% | -3.2% | +2.0% | 1.0 | too early | -0.8% | 35% | -1.3% | -2.8% | -2.0 | too early | +10% vs random at 60 bars |  |
| early rally | 109 | 0 |  |  |  |  |  | too early | +4.1% | 78% | +4.6% | +0.2% | 0.3 | noise so far | +2-3% net, ~0 vs SPY at 20 bars |  |
| MA200 cross after a long run below | 3 | 0 |  |  |  |  |  | too early | +0.8% | 67% | +0.1% | -1.9% | -0.6 | too early | no edge in both periods |  |
| falling wedge, forming (watch list) | 99 | 64 | -0.3% | 48% | -1.5% | +0.2% | 0.2 | noise so far | +4.1% | 75% | +3.7% | -0.0% | -0.0 | noise so far | no edge (a stock still falling) |  |
| insider buys, other | 26 | 24 | -2.1% | 25% | -3.6% | +1.8% | 1.4 | noise so far | -0.9% | 50% | -1.3% | -2.9% | -1.7 | noise so far | no edge |  |
| Jev decision | 128 | 0 |  |  |  |  |  | too early | +4.9% | 75% | +5.1% | -0.2% | -0.3 | noise so far | untested (forward test only) |  |
| growth screen (retired) | 22 | 22 | -3.4% | 36% | -5.2% | +1.5% | 0.7 | noise so far | -7.8% | 14% | -8.4% | -9.0% | -4.2 | not working so far | retired |  |

## By condition (basket excess, with vs without; 20 bars and to date)

| condition | n with | n without | ret 20 with | ret 20 without | hit 20 with | hit 20 without | vs basket 20 with | vs basket 20 without | diff 20 | t 20 | verdict 20 | n with (to date) | n without | ret with | ret without | vs basket with | vs basket without | diff | t | verdict to date |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| Z: z vs peers below -1 (warning) | 6 | 82 | -5.0% | +2.7% | 0% | 78% | -6.9% | -0.1% | -6.7% | -3.1 | too early | 21 | 137 | +2.2% | +4.8% | -2.2% | -0.5% | -1.7% | -0.8 | noise so far |
| S: negative sentiment (warning) | 26 | 62 | +1.3% | +2.5% | 69% | 74% | -0.9% | -0.4% | -0.5% | -0.3 | noise so far | 45 | 113 | +5.3% | +4.2% | +0.4% | -1.2% | +1.6% | 1.1 | noise so far |
| T: target upside above 50% (warning) | 5 | 83 | -3.0% | +2.5% | 20% | 76% | -5.1% | -0.3% | -4.7% | -1.8 | too early | 10 | 148 | -1.4% | +4.9% | -6.8% | -0.3% | -6.5% | -2.4 | too early |
| D: more than 40% below the 52-week high (a plus over ten years) | 12 | 76 | -0.2% | +2.5% | 67% | 74% | -2.5% | -0.3% | -2.2% | -0.7 | noise so far | 26 | 132 | +1.9% | +5.0% | -3.2% | -0.2% | -3.0% | -1.2 | noise so far |
| no warning flag at all | 55 | 33 | +3.2% | +0.5% | 82% | 58% | +0.1% | -1.7% | +1.8% | 1.3 | noise so far | 93 | 65 | +4.7% | +4.2% | -0.8% | -0.6% | -0.3% | -0.2 | noise so far |
| read: signs of a bottom | 31 | 57 | +0.6% | +3.1% | 68% | 75% | -1.9% | +0.1% | -2.0% | -1.2 | noise so far | 56 | 102 | +1.9% | +5.9% | -3.6% | +0.8% | -4.4% | -3.0 | better without it |
| read: still falling | 3 | 85 | +7.1% | +2.0% | 100% | 72% | +3.6% | -0.7% | +4.3% | 1.5 | too early | 12 | 146 | +6.5% | +4.3% | +2.9% | -1.0% | +3.9% | 3.0 | better with the condition |
| 'market-wide' among the causes of the decline | 23 | 65 | +2.2% | +2.2% | 70% | 74% | -0.9% | -0.5% | -0.4% | -0.2 | noise so far | 53 | 105 | +4.5% | +4.5% | -0.7% | -0.7% | +0.1% | 0.1 | noise so far |
| sentiment read positive | 20 | 68 | +3.8% | +1.7% | 85% | 69% | +1.1% | -1.0% | +2.1% | 1.4 | noise so far | 43 | 115 | +4.6% | +4.4% | -0.4% | -0.8% | +0.4% | 0.3 | noise so far |
| analyst consensus buy / strong buy | 71 | 17 | +2.1% | +2.5% | 70% | 82% | -0.5% | -0.7% | +0.1% | 0.1 | noise so far | 128 | 30 | +4.5% | +4.4% | -0.8% | -0.4% | -0.4% | -0.2 | noise so far |
| more than 30% below the 52-week high | 33 | 55 | +1.1% | +2.8% | 64% | 78% | -1.4% | -0.1% | -1.4% | -0.8 | noise so far | 67 | 91 | +3.8% | +5.0% | -1.5% | -0.2% | -1.3% | -0.9 | noise so far |
| 20-day return above the peer group (vs peers 20d > 0) | 32 | 56 | +4.3% | +1.0% | 91% | 62% | +1.4% | -1.7% | +3.1% | 2.1 | better with the condition | 52 | 106 | +5.6% | +3.9% | +0.3% | -1.2% | +1.5% | 1.1 | noise so far |
| MACD pre-touch probability >= 70% (lines still apart) | 0 | 3 |  | -13.6% |  | 0% |  | -15.5% |  |  | too early | 0 | 12 |  | -2.3% |  | -6.1% |  |  | too early |
| checklist: 4 or 5 checks passed (vs 3 or fewer, among the names in the checklist) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 23 | 19 | +1.8% | +1.4% | -2.0% | -2.7% | +0.7% | 0.3 | noise so far |
| listed 1-3 days (fresh) vs 4+ days | 24 | 79 | +0.9% | -1.4% | 50% | 47% | -0.2% | +0.1% | -0.3% | -0.2 | noise so far | 90 | 204 | +4.5% | +3.1% | +0.4% | -0.7% | +1.1% | 1.2 | noise so far |
| peer group beaten down too | 19 | 27 | +2.0% | -0.4% | 58% | 52% | +2.0% | -1.7% | +3.7% | 2.9 | better with the condition | 73 | 145 | +7.3% | +2.4% | +2.9% | -1.6% | +4.5% | 4.4 | better with the condition |
| 6-month return below -30% | 10 | 83 | -5.5% | +0.5% | 20% | 55% | -2.8% | +1.0% | -3.8% | -1.8 | too early | 27 | 243 | +1.1% | +4.2% | -2.2% | +0.3% | -2.5% | -1.2 | noise so far |
| signal-day volume above 1.5x | 1 | 12 | +2.5% | -2.3% | 100% | 50% | -3.2% | -1.2% | -2.0% |  | too early | 19 | 157 | +2.4% | +3.8% | -1.7% | -0.0% | -1.6% | -0.8 | noise so far |
| a 3x+ volume day in the last 10 bars | 0 | 13 |  | -1.9% |  | 54% |  | -1.3% |  |  | too early | 2 | 62 | +9.6% | +2.8% | +5.9% | -1.0% | +7.0% |  | too early |
| early rally: two or more rules fired | 0 | 0 |  |  |  |  |  |  |  |  | too early | 17 | 92 | +2.9% | +4.4% | -0.9% | +0.4% | -1.3% | -0.7 | noise so far |
| Jev: P(buy) >= 0.6 (the jev_pick rule) | 0 | 0 |  |  |  |  |  |  |  |  | too early | 24 | 104 | +4.3% | +5.0% | -1.2% | +0.0% | -1.2% | -0.7 | noise so far |
| Jev: P(buy) < 0.2 | 0 | 0 |  |  |  |  |  |  |  |  | too early | 66 | 62 | +5.0% | +4.8% | +0.5% | -0.9% | +1.3% | 1.0 | noise so far |

## The journal: closed trades against the research expectation

| rule | logged | closed | closed mean | closed hit | vs SPY | vs basket | expected hit | open: mean | open: hit | all at the current price: mean | hit | vs basket | verdict (closed) |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|:--|
| early_rally_beaten_down | 108 | 0 |  |  |  |  | 60% | +4.34% | 78% | +4.34% | 79% | +0.55% | too early |
| falling_wedge_beaten_down | 35 | 12 | +1.08% | 67% | +0.76% | -1.12% | 60% | +3.15% | 70% | +2.44% | 69% | -0.91% | on track |
| growth_top10 | 13 | 0 |  |  |  |  |  | -6.70% | 23% | -6.70% | 23% | -7.60% | too early |
| insider_buy_beaten_down | 4 | 0 |  |  |  |  | 68% | +2.70% | 75% | +2.70% | 75% | -0.52% | too early |
| jev_pick | 33 | 10 | +5.44% | 60% | +5.60% | -2.21% |  | +3.36% | 78% | +3.99% | 73% | -1.18% | on track |
| jev_skip | 6 | 0 |  |  |  |  |  | +6.19% | 100% | +6.19% | 100% | +3.40% | too early |
| newsday | 29 | 0 |  |  |  |  | 62% | +0.01% | 38% | +0.01% | 44% | -3.90% | too early |

## What changed since the previous review

- news-day (to date): too early -> not working so far
- peer group beaten down too (20 bars): noise so far -> better with the condition
- jev_pick (20 bars): too early -> on track

## Method

Source: the tables of the dated reports (journal/report_<date>.md) and the journal's mark_to_market.csv. Two horizons: 20 bars after the listing, and to the current close (every name, over its own holding length; an uneven horizon, so it summarises where things stand now rather than the result of a fixed rule). Table verdict: 20+ names with a return at the horizon; 'works' when the mean excess over the beaten-down basket is positive with t >= 2; 'not working' when negative with t <= -2; 'noise' otherwise. Condition verdict: 12+ names on each side, Welch t on the difference in basket excess; |t| >= 2 names the better side. Journal rule: 10+ closed trades; 'on track' when the mean is positive and the hit rate is within 10 points of the expectation. Survivorship bias, overlapping windows and a single regime apply throughout. Systematic screens and a forward test, not investment advice.
