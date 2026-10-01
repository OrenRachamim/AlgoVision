# Peer-group scan of the liquid US universe (origin)

These four scripts are the original full-universe study, copied unchanged from
`OrenRachamim/DataStoreApi`, branch `ccr-bafd8b58-nwg5rq`, directory `market-analysis/`
(commit faf3caa, 2026-10-01). They are kept here as the reference for `algovision/peers.py`,
which ports the parts that proved useful onto the frames AlgoVision already holds.

| file | what it does |
|---|---|
| `universe.py` | builds a tradable universe from the Nasdaq screener (all US exchanges, no ETFs / preferreds / warrants / units), downloads 3 years of history with yfinance and filters on median 60-day dollar volume and price |
| `scan_analysis.py` | market-neutral correlations (residuals vs RSP), Ward clustering into data-driven groups, industry cohesion, per-stock peers, within-group lead-lag (FDR-corrected), shock spillover, 20-day divergence from the peer group with a historical reversion check, cohesion changes |
| `leadlag_analysis.py` | lead-lag helpers (`bh` = Benjamini-Hochberg) and the sector-level lead-lag study |
| `sector_correlation.py` | the first, sector-level correlation study |

Run them on their own (they need `scipy`, `scikit-learn`, `yfinance`):

```bash
cd research/peers
python universe.py --years 3 --min-dv 20e6 --min-price 5 --cache cache
python scan_analysis.py --cache cache --clusters 220 --out scan_results.json
```

## What the scan found (1,827 liquid US stocks, 2023-10-03 to 2026-10-01)

- Data-driven groups match the Nasdaq industry classification only loosely (adjusted Rand index 0.25);
  the closest peers of a stock are often outside its official industry.
- Divergence from peers: stocks more than two standard deviations **below** their group over 20 days
  regained +0.65% relative to the group over the next 20 days (t = 2.3, 24 non-overlapping samples).
  Stocks stretched above their group showed nothing (t = -0.6). The cross-sectional rank correlation
  of the z-score with the next 20-day relative return is not significant (IC -0.011, t = -1.1).
- Lead-lag inside groups: 22,902 pairs, 6% nominally significant, **none** after FDR correction. Not used.
- Shock spillover: peers move with the shocked stock on the day (t = 139), and give back about 0.2%
  over days 2-5 (t = -8.4), too small to trade. Not used.

What AlgoVision uses: the peer list, the group and the current divergence, as **context** in every
brief and in the Hebrew wedge file, plus one weak signal (+0.5) in the rule-based read when z <= -2.
