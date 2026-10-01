"""Sector co-movement analysis for US equities.

Questions answered:
  1. Do stocks inside a sector move together (raw and after removing the market)?
  2. Does a data-driven clustering of returns recover the GICS sectors?
  3. How does each sector ETF relate to market indices and macro instruments
     (S&P 500, Nasdaq 100, Russell 2000, VIX, 10y yield, dollar, oil, gold, credit)?
  4. How did those relationships change over time (rolling correlations)?

Usage: python sector_correlation.py [--years 3] [--out results.json]
"""
import argparse
import json

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.cluster.hierarchy import fcluster, leaves_list, linkage
from sklearn.metrics import adjusted_rand_score
from scipy.spatial.distance import squareform

SECTORS = {
    "Technology":    ("XLK",  ["AAPL", "MSFT", "NVDA", "AVGO", "ORCL", "CRM", "AMD", "ADBE"]),
    "Financials":    ("XLF",  ["JPM", "BAC", "WFC", "GS", "MS", "C", "SCHW", "BLK"]),
    "Energy":        ("XLE",  ["XOM", "CVX", "COP", "EOG", "SLB", "OXY", "PSX", "MPC"]),
    "Health Care":   ("XLV",  ["UNH", "JNJ", "LLY", "PFE", "MRK", "ABBV", "TMO", "ABT"]),
    "Industrials":   ("XLI",  ["CAT", "HON", "GE", "UNP", "DE", "BA", "LMT", "UPS"]),
    "Cons. Discr.":  ("XLY",  ["AMZN", "TSLA", "HD", "MCD", "NKE", "SBUX", "LOW", "BKNG"]),
    "Cons. Staples": ("XLP",  ["PG", "KO", "PEP", "WMT", "COST", "CL", "MO", "MDLZ"]),
    "Utilities":     ("XLU",  ["NEE", "DUK", "SO", "D", "AEP", "EXC", "SRE", "XEL"]),
    "Materials":     ("XLB",  ["LIN", "SHW", "APD", "FCX", "NEM", "ECL", "DOW", "NUE"]),
    "Real Estate":   ("XLRE", ["PLD", "AMT", "EQIX", "SPG", "PSA", "O", "CCI", "WELL"]),
    "Communication": ("XLC",  ["GOOGL", "META", "NFLX", "DIS", "CMCSA", "VZ", "T", "TMUS"]),
}

# name -> (ticker, transform). "ret" = log return, "diff" = level change (for VIX, yields).
INDICES = {
    "S&P 500":      ("SPY", "ret"),
    "Nasdaq 100":   ("QQQ", "ret"),
    "Russell 2000": ("IWM", "ret"),
    "Dow Jones":    ("DIA", "ret"),
    "VIX":          ("^VIX", "diff"),
    "10Y Yield":    ("^TNX", "diff"),
    "20Y+ Bonds":   ("TLT", "ret"),
    "US Dollar":    ("UUP", "ret"),
    "Oil (WTI)":    ("USO", "ret"),
    "Gold":         ("GLD", "ret"),
    "HY Credit":    ("HYG", "ret"),
}


def download(tickers, years):
    px = yf.download(sorted(set(tickers)), period=f"{years}y", auto_adjust=True,
                     progress=False, threads=True)["Close"]
    return px.dropna(axis=1, how="all").ffill(limit=2)


def avg_offdiag(c):
    a = c.values
    n = a.shape[0]
    return float((a.sum() - np.trace(a)) / (n * n - n)) if n > 1 else float("nan")


def residuals(rets, market):
    """Remove each column's beta exposure to the market return."""
    m = market - market.mean()
    out = {}
    for col in rets:
        y = rets[col]
        beta = ((y - y.mean()) * m).sum() / (m ** 2).sum()
        out[col] = y - beta * market
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--out", default="results.json")
    args = ap.parse_args()

    stock_sector = {s: sec for sec, (_, stocks) in SECTORS.items() for s in stocks}
    etfs = {sec: etf for sec, (etf, _) in SECTORS.items()}
    all_tickers = list(stock_sector) + list(etfs.values()) + [t for t, _ in INDICES.values()] + ["RSP"]
    px = download(all_tickers, args.years)

    logret = np.log(px).diff()
    diffs = px.diff()
    rets = logret.iloc[1:].dropna(axis=0, how="any", subset=[c for c in px if c in stock_sector])
    stocks = [s for s in stock_sector if s in rets]
    # Equal-weight S&P 500 as the market factor, so mega-cap tech does not dominate it.
    market = rets["RSP"]

    R = rets[stocks]
    corr_raw = R.corr()
    corr_res = residuals(R, market).corr()

    # 1. Intra-sector cohesion
    cohesion = []
    for sec, (etf, members) in SECTORS.items():
        m = [s for s in members if s in R]
        others = [s for s in stocks if s not in m]
        intra = avg_offdiag(corr_raw.loc[m, m])
        inter = float(corr_raw.loc[m, others].values.mean())
        intra_res = avg_offdiag(corr_res.loc[m, m])
        inter_res = float(corr_res.loc[m, others].values.mean())
        to_etf = float(R[m].corrwith(rets[etf]).mean())
        same_dir = float(np.mean([(np.sign(R[a]) == np.sign(R[b])).mean()
                                  for i, a in enumerate(m) for b in m[i + 1:]]))
        cohesion.append(dict(sector=sec, etf=etf, n=len(m), intra=intra, inter=inter,
                             intra_resid=intra_res, inter_resid=inter_res,
                             corr_to_etf=to_etf, same_direction=same_dir))

    # Per-stock fit: corr with own-sector peers vs best other sector (residual returns)
    misfits = []
    for s in stocks:
        own = stock_sector[s]
        scores = {}
        for sec, (_, members) in SECTORS.items():
            peers = [p for p in members if p in R and p != s]
            scores[sec] = float(corr_res.loc[s, peers].mean())
        best = max(scores, key=scores.get)
        misfits.append(dict(ticker=s, sector=own, own=scores[own], best_sector=best,
                            best=scores[best], fits=best == own))

    # 2. Clustering vs GICS (on residual correlations)
    dist = np.sqrt(np.clip(2 * (1 - corr_res.values), 0, None))
    np.fill_diagonal(dist, 0)
    Z = linkage(squareform(dist, checks=False), method="ward")
    order = [stocks[i] for i in leaves_list(Z)]
    labels = fcluster(Z, t=len(SECTORS), criterion="maxclust")
    clusters = {}
    for s, lab in zip(stocks, labels):
        clusters.setdefault(int(lab), []).append(s)
    purity = sum(pd.Series([stock_sector[s] for s in mem]).value_counts().iloc[0]
                 for mem in clusters.values()) / len(stocks)
    ari = adjusted_rand_score([stock_sector[s] for s in stocks], labels)

    # 3. Sector ETF vs indices / macro
    idx_series = {}
    for name, (t, tr) in INDICES.items():
        if t in px:
            idx_series[name] = (logret if tr == "ret" else diffs)[t]
    idx_df = pd.DataFrame(idx_series)
    etf_df = pd.DataFrame({sec: logret[etf] for sec, etf in etfs.items() if etf in px})
    both = pd.concat([etf_df, idx_df], axis=1).dropna()
    sector_vs_index = both.corr().loc[etf_df.columns, idx_df.columns]

    betas = {}
    for sec in etf_df:
        y, x = both[sec], both["S&P 500"]
        betas[sec] = float(np.cov(y, x)[0, 1] / np.var(x, ddof=1))
    sector_corr = etf_df.loc[both.index].corr()

    # 4. Rolling 63-day correlations (~1 quarter)
    win = 63
    rolling = {}
    for key in ["S&P 500", "10Y Yield", "Oil (WTI)", "VIX"]:
        rc = both[etf_df.columns].rolling(win).corr(both[key]).dropna()
        rolling[key] = rc.resample("W").last()
    roll_intra = {}
    for sec, (_, members) in SECTORS.items():
        m = [s for s in members if s in R]
        vals, dates = [], []
        for end in range(win, len(R) + 1, 5):
            vals.append(avg_offdiag(R[m].iloc[end - win:end].corr()))
            dates.append(R.index[end - 1])
        roll_intra[sec] = pd.Series(vals, index=dates)
    roll_intra = pd.DataFrame(roll_intra)

    recent = both.iloc[-win:].corr().loc[etf_df.columns, idx_df.columns]

    def frame(df):
        return {"index": [str(i.date()) if hasattr(i, "date") else str(i) for i in df.index],
                "columns": list(df.columns),
                "values": [[None if pd.isna(v) else round(float(v), 4) for v in row] for row in df.values]}

    out = dict(
        period=dict(start=str(rets.index[0].date()), end=str(rets.index[-1].date()), days=len(rets)),
        sectors={sec: dict(etf=etf, stocks=[s for s in mem if s in R]) for sec, (etf, mem) in SECTORS.items()},
        cohesion=cohesion,
        misfits=misfits,
        clustering=dict(purity=purity, ari=float(ari), clusters=clusters, order=order),
        corr_raw=frame(corr_raw.loc[order, order]),
        corr_resid=frame(corr_res.loc[order, order]),
        sector_vs_index=frame(sector_vs_index),
        sector_vs_index_recent=frame(recent),
        sector_corr=frame(sector_corr),
        betas=betas,
        rolling={k: frame(v) for k, v in rolling.items()},
        rolling_intra=frame(roll_intra),
    )
    with open(args.out, "w") as f:
        json.dump(out, f)
    print(json.dumps(dict(period=out["period"], purity=purity, ari=ari), indent=1))
    print(pd.DataFrame(cohesion).round(3).to_string())
    print(sector_vs_index.round(2).to_string())
    print(recent.round(2).to_string())
    print(pd.Series(betas).round(2).to_string())
    print(pd.DataFrame(misfits).query("not fits").round(3).to_string())
    for k, v in clusters.items():
        print(k, v)


if __name__ == "__main__":
    main()
