# Growth screen (`python -m algovision growth`)

Long-horizon stock selection for the S&P 500 + NASDAQ-100 universe. Each name is scored 0-1 on four blocks
(percentile ranks within the universe), and every pick comes with a one-line explanation.

| block | weight | inputs | tested? |
|---|---|---|---|
| growth | 40 % | revenue yoy (latest quarter), 3-year revenue CAGR, EPS yoy, operating-margin change | no (Yahoo gives 4 years of fundamentals) |
| quality | 20 % | operating margin, FCF margin, ROE, low debt/equity, shrinking share count | no |
| momentum | 25 % | 12-1 and 6-1 price momentum, above the 200-day MA | **yes**: top-decile 12-1 momentum beat the universe in 2016-22 and 2023-26 (`research_factors.md`) |
| valuation | 15 % | PEG and forward P/E (cheaper ranks higher) | no |

Hard filters: revenue growing year on year; positive free cash flow or operating profit; 260+ days of prices.
Duplicate share classes are collapsed. `--max-per-sector 3` caps sector concentration in the printed list.
A **cyclical flag** marks names whose current growth is more than three times their 3-year trend (memory chips,
energy, airlines): those are usually at a cyclical peak, and the screen would otherwise love them.

```bash
python -m algovision growth --top 20 --explain --max-per-sector 3
```

## What to expect, honestly

* The only block with evidence is momentum. The fundamental blocks are a disciplined description of the
  business, not a proven predictor. Academic evidence for profitability/quality factors is decent, for
  "high revenue growth" it is weak to negative (growth is priced in, and fastest-growth names underperform on
  average). The screen leans on quality and valuation to offset that.
* The daily journal logs the diversified top 10 as long positions (`growth_top10`, reviewed after 250 bars) and
  marks them against SPY over the same period. That forward test is the real evaluation; expect to wait a year.
* Concentration risk is structural: growth screens cluster in whatever is booming (today: AI semiconductors and
  memory). The sector cap limits it; it does not remove it.

This is a screen, not advice: it says which names best fit a fixed definition of "growing, profitable, in an
uptrend, not absurdly priced" as of today's data.
