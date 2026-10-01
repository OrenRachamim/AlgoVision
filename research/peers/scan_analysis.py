"""Scan of the whole liquid US stock universe (built by universe.py).

  1. Industry cohesion for every Nasdaq industry with >= 5 liquid stocks, and its index links.
  2. Data-driven groups: Ward clustering of market-neutral correlations across all stocks,
     compared with the official industries.
  3. Per-stock profile: closest peers, group, beta, volatility, liquidity.
  4. Lead-lag inside every data-driven group (next-day predictability, FDR-corrected),
     and peer response to large moves.
  5. Current divergence: each stock's 20-day return relative to its peer group, as a z-score,
     plus a historical check of whether such divergences tended to revert.
  6. Groups whose cohesion changed most in the last quarter.

Usage: python scan_analysis.py [--cache DIR] [--clusters 220] [--out scan_results.json]
"""
import argparse
import json
import pathlib

import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.metrics import adjusted_rand_score

from leadlag_analysis import bh

INDEX = {"S&P 500": ("SPY", "ret"), "Nasdaq 100": ("QQQ", "ret"), "Russell 2000": ("IWM", "ret"),
         "VIX": ("^VIX", "diff"), "10Y Yield": ("^TNX", "diff"), "20Y+ Bonds": ("TLT", "ret"),
         "US Dollar": ("UUP", "ret"), "Oil (WTI)": ("USO", "ret"), "Gold": ("GLD", "ret"), "HY Credit": ("HYG", "ret")}
WIN = 63
REL_WIN = 20


def nan_corr(Z):
    """Correlation of columns that may contain NaN: standardize on available days, fill 0."""
    Z = (Z - Z.mean()) / Z.std()
    A = Z.fillna(0).values
    n = Z.notna().astype(float).values
    return (A.T @ A) / np.maximum(n.T @ n - 1, 1)


def market_resid(R, m):
    """Per-column OLS residual on the market, using each column's available days."""
    out, betas = {}, {}
    for c in R:
        ok = R[c].notna()
        y, x = R[c][ok], m[ok]
        b = np.cov(y, x)[0, 1] / x.var()
        out[c] = R[c] - (y.mean() - b * x.mean()) - b * m
        betas[c] = b
    return pd.DataFrame(out), pd.Series(betas)


def avg_offdiag(C):
    n = C.shape[0]
    return float((C.sum() - np.trace(C)) / (n * n - n)) if n > 1 else None


def leadlag_group(E, mkt, members):
    """Next-day predictive regressions for all ordered pairs inside one group (FWL, HC0)."""
    X = E[members].fillna(0).values
    m = mkt.values
    rows = []
    for j, b in enumerate(members):
        y = X[1:, j]
        Zc = np.column_stack([np.ones(len(y)), X[:-1, j], m[:-1]])
        P = Zc @ np.linalg.pinv(Zc)
        ry = y - P @ y
        RX = X[:-1] - P @ X[:-1]
        sxx = (RX ** 2).sum(0)
        c = RX.T @ ry / sxx
        u = ry[:, None] - RX * c
        se = np.sqrt((RX ** 2 * u ** 2).sum(0)) / sxx
        t = c / se
        for i, a in enumerate(members):
            if a != b:
                rows.append((a, b, c[i], t[i]))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="cache")
    ap.add_argument("--clusters", type=int, default=220)
    ap.add_argument("--out", default="scan_results.json")
    args = ap.parse_args()
    cache = pathlib.Path(args.cache)
    u = pd.read_csv(cache / "universe.csv", index_col=0)
    close = pd.read_pickle(cache / "close.pkl")

    U = u[u.liquid & u.full_history].copy()
    U[["sector", "industry"]] = U[["sector", "industry"]].fillna("Unclassified")
    tick = [t for t in U.index if t in close]
    # dual-class listings (GOOGL/GOOG, FOXA/FOX...): keep the more liquid line
    first = U.name.str.lower().str.split().str[:2].str.join(" ")
    r0 = np.log(close[tick]).diff().iloc[-500:]
    drop = set()
    for _, grp in U.loc[tick].groupby(first.loc[tick]):
        if len(grp) < 2:
            continue
        c = r0[grp.index].corr()
        for a in grp.index:
            for b in grp.index:
                if a < b and c.loc[a, b] > 0.95:
                    drop.add(a if U.dv60[a] < U.dv60[b] else b)
    tick = [t for t in tick if t not in drop]
    print("dropped dual-class", sorted(drop))
    px = close[tick + [t for t, _ in INDEX.values()] + ["RSP"]].ffill(limit=3)
    R = np.log(px).diff().iloc[1:]
    R = R[R["SPY"].notna()]
    # guard against bad prints: drop daily moves beyond +/-80% (splits mis-adjusted etc.)
    S = R[tick].where(R[tick].abs() < 0.58)
    mkt = R["RSP"]
    E, beta = market_resid(S, mkt)
    days = len(S)
    print("stocks", len(tick), "days", days)

    C = nan_corr(E)
    Craw = nan_corr(S)
    Cdf = pd.DataFrame(C, index=tick, columns=tick)

    # ---- 2. clusters
    dist = np.sqrt(np.clip(2 * (1 - C), 0, None))
    np.fill_diagonal(dist, 0)
    Z = linkage(squareform(dist, checks=False), method="ward")
    lab = fcluster(Z, t=args.clusters, criterion="maxclust")
    U = U.loc[tick]
    U["cluster"] = lab
    idx_of = {t: i for i, t in enumerate(tick)}
    groups = []
    for k, members in U.groupby("cluster").groups.items():
        members = list(members)
        ii = [idx_of[t] for t in members]
        sub = U.loc[members]
        top_ind = sub.industry.value_counts()
        lead = sub.sort_values("mcap", ascending=False).index[:4].tolist()
        groups.append(dict(id=int(k), n=len(members), members=sorted(members, key=lambda t: -U.mcap.get(t, 0)),
                           intra=avg_offdiag(C[np.ix_(ii, ii)]), intra_raw=avg_offdiag(Craw[np.ix_(ii, ii)]),
                           industry=top_ind.index[0], industry_share=float(top_ind.iloc[0] / len(members)),
                           industries=int(top_ind.size), sector=sub.sector.value_counts().index[0], top=lead,
                           mcap=float(sub.mcap.sum())))
    G = pd.DataFrame(groups).set_index("id")
    ind_ok = U.industry.map(U.industry.value_counts()) >= 5
    ari = adjusted_rand_score(U.industry[ind_ok], U.cluster[ind_ok])

    # ---- 1. industry cohesion
    idx = pd.DataFrame({n: (R[t] if tr == "ret" else px[t].diff().loc[R.index]) for n, (t, tr) in INDEX.items()})
    inds = []
    for ind, members in U.groupby("industry").groups.items():
        members = list(members)
        if len(members) < 5:
            continue
        ii = [idx_of[t] for t in members]
        basket = S[members].mean(axis=1)
        inds.append(dict(industry=ind, sector=U.loc[members].sector.mode().iloc[0], n=len(members),
                         intra=avg_offdiag(C[np.ix_(ii, ii)]), intra_raw=avg_offdiag(Craw[np.ix_(ii, ii)]),
                         clusters=int(U.loc[members].cluster.nunique()),
                         vs_index={k: round(float(basket.corr(idx[k])), 3) for k in idx},
                         vs_index_recent={k: round(float(basket.iloc[-WIN:].corr(idx[k].iloc[-WIN:])), 3) for k in idx}))
    I = pd.DataFrame(inds)

    # ---- 3. stock profiles
    np.fill_diagonal(C, -np.inf)
    top5 = np.argsort(-C, axis=1)[:, :5]
    np.fill_diagonal(C, 1)
    vol = S.std() * np.sqrt(252)
    ret1y = px[tick].iloc[-1] / px[tick].iloc[-253] - 1
    stocks = []
    for i, t in enumerate(tick):
        row = U.loc[t]
        same_ind = [idx_of[o] for o in U.index[U.industry == row.industry] if o != t]
        same_cl = [idx_of[o] for o in U.index[U.cluster == row.cluster] if o != t]
        stocks.append(dict(t=t, n=row["name"][:60], s=row.sector, ind=row.industry, c=int(row.cluster),
                           mc=round(float(row.mcap) / 1e9, 2) if pd.notna(row.mcap) else None,
                           dv=round(float(row.dv60) / 1e6, 1), b=round(float(beta[t]), 2), v=round(float(vol[t]), 3),
                           r1=round(float(ret1y[t]), 3) if pd.notna(ret1y[t]) else None,
                           pc=round(float(C[i, same_cl].mean()), 3) if same_cl else None,
                           pi=round(float(C[i, same_ind].mean()), 3) if same_ind else None,
                           p=[[tick[j], round(float(C[i, j]), 2)] for j in top5[i]]))

    # ---- 4. lead-lag within clusters
    ll = []
    for k, members in U.groupby("cluster").groups.items():
        members = list(members)
        if 3 <= len(members) <= 150:
            ll += [(k, *r) for r in leadlag_group(E, mkt, members)]
    LL = pd.DataFrame(ll, columns=["cluster", "leader", "follower", "coef", "t"])
    LL["p"] = 2 * stats.norm.sf(LL.t.abs())
    LL["fdr"] = bh(LL.p.values, 0.10)
    half = days // 2
    sig_pairs = LL.sort_values("p").head(60)
    stab = []
    for _, r in sig_pairs.iterrows():
        ts = []
        for part in (slice(0, half), slice(half, None)):
            e = E.iloc[part]
            rr = leadlag_group(e, mkt.iloc[part], [r.leader, r.follower])
            ts.append([x[3] for x in rr if x[0] == r.leader][0])
        stab.append(ts)
    sig_pairs = sig_pairs.assign(t_h1=[s[0] for s in stab], t_h2=[s[1] for s in stab])

    # shock spillover within clusters
    sd = E.std()
    ev = []
    Ev = E.values
    for k, members in U.groupby("cluster").groups.items():
        members = list(members)
        if len(members) < 3:
            continue
        cols = [E.columns.get_loc(t) for t in members]
        block = Ev[:, cols]
        for jj, t in enumerate(members):
            z = block[:, jj] / sd[t]
            for d in np.where(np.abs(z) > 2.5)[0]:
                if d + 5 >= days:
                    continue
                peers = np.delete(block, jj, axis=1)
                s = np.sign(z[d])
                ev.append((s * np.nanmean(peers[d]), s * np.nanmean(peers[d + 1]),
                           s * np.nanmean(np.nansum(peers[d + 2:d + 6], axis=0))))
    EV = np.array(ev)
    shock = {k: dict(mean=float(np.nanmean(EV[:, i])),
                     t=float(np.nanmean(EV[:, i]) / (np.nanstd(EV[:, i]) / np.sqrt(np.isfinite(EV[:, i]).sum()))))
             for i, k in enumerate(["d0", "d1", "d2_5"])}
    shock["n"] = int(len(EV))

    # ---- 5. divergence vs peer group (beta-adjusted to cluster basket, excluding self)
    Sf = S.fillna(0)
    rel = {}
    for k, members in U.groupby("cluster").groups.items():
        members = list(members)
        if len(members) < 3:
            continue
        tot = Sf[members].sum(axis=1)
        for t in members:
            peer = (tot - Sf[t]) / (len(members) - 1)
            b = np.cov(Sf[t], peer)[0, 1] / peer.var()
            rel[t] = Sf[t] - b * peer
    REL = pd.DataFrame(rel)
    roll = REL.rolling(REL_WIN).sum()
    zs = (roll - roll.rolling(252, min_periods=126).mean()) / roll.rolling(252, min_periods=126).std()
    fwd = REL[::-1].rolling(REL_WIN).sum()[::-1].shift(-1)       # next 20 days relative return
    # information coefficient: cross-sectional rank correlation, sampled every 20 days
    ic = []
    for d in range(260, len(zs) - REL_WIN - 1, REL_WIN):
        a, b = zs.iloc[d], fwd.iloc[d]
        ok = a.notna() & b.notna()
        if ok.sum() > 100:
            ic.append(stats.spearmanr(a[ok], b[ok])[0])
    ic = np.array(ic)
    # decile spread: average next-20d relative return of most stretched up vs down (|z|>2)
    # per sampled date (non-overlapping 20-day steps): mean next-20d relative return of stretched stocks
    ups, dns = [], []
    for d in range(260, len(zs) - REL_WIN - 1, REL_WIN):
        a, b = zs.iloc[d], fwd.iloc[d]
        if (a > 2).sum() >= 3:
            ups.append(b[a > 2].mean())
        if (a < -2).sum() >= 3:
            dns.append(b[a < -2].mean())
    tstat = lambda x: float(np.mean(x) / (np.std(x, ddof=1) / np.sqrt(len(x))))
    up, dn, up_t, dn_t = float(np.mean(ups)), float(np.mean(dns)), tstat(ups), tstat(dns)
    z_now = zs.iloc[-1].dropna()
    r_now = roll.iloc[-1]
    div = pd.DataFrame(dict(z=z_now, rel20=r_now.reindex(z_now.index)))
    div["cluster"] = U.cluster.reindex(div.index)
    div_out = pd.concat([div.sort_values("z").head(25), div.sort_values("z").tail(25)])

    # ---- 6. cohesion change by cluster
    chg = []
    for k, members in U.groupby("cluster").groups.items():
        members = list(members)
        if len(members) < 4:
            continue
        recent = E[members].iloc[-WIN:].corr().values
        chg.append(dict(id=int(k), recent=avg_offdiag(recent), full=G.loc[k, "intra"]))
    CH = pd.DataFrame(chg)
    CH["delta"] = CH.recent - CH.full

    rec = lambda df: json.loads(df.to_json(orient="records", double_precision=4))
    out = dict(
        period=dict(start=str(S.index[0].date()), end=str(S.index[-1].date()), days=days),
        universe=dict(prefiltered=len(u), liquid=int(u.liquid.sum()), dual_class_dropped=sorted(drop),
                      analysed=len(tick), min_dv=20e6, min_price=5,
                      sectors=U.sector.value_counts().to_dict(), countries=U.country.value_counts().head(8).to_dict()),
        clustering=dict(k=args.clusters, ari=float(ari)),
        groups=rec(G.reset_index().sort_values("intra", ascending=False)),
        industries=rec(I.sort_values("intra", ascending=False)),
        stocks=stocks,
        leadlag=dict(pairs=len(LL), nominal=float((LL.t.abs() > 1.96).mean()), fdr=int(LL.fdr.sum()),
                     fdr_pos=int((LL.fdr & (LL.coef > 0)).sum()),
                     top=rec(sig_pairs[["cluster", "leader", "follower", "coef", "t", "p", "fdr", "t_h1", "t_h2"]])),
        shock=shock,
        divergence=dict(ic_mean=float(ic.mean()), ic_t=float(ic.mean() / (ic.std(ddof=1) / np.sqrt(len(ic)))),
                        ic_n=len(ic), fwd_up=up, fwd_dn=dn, fwd_up_t=up_t, fwd_dn_t=dn_t, samples=len(ups),
                        now=rec(div_out.reset_index(names="t")), count_abs2=int((z_now.abs() > 2).sum())),
        cohesion_change=rec(CH.sort_values("delta")),
    )
    with open(args.out, "w") as f:
        json.dump(out, f, allow_nan=False, default=lambda o: None)

    print("ARI", round(ari, 3))
    print(G.sort_values("intra", ascending=False).head(30)[["n", "intra", "industry", "industry_share", "industries", "top"]].to_string())
    print(G.n.describe())
    print(I.sort_values("intra", ascending=False)[["industry", "n", "intra", "clusters"]].head(15).to_string())
    print(I.sort_values("intra")[["industry", "n", "intra", "clusters"]].head(10).to_string())
    print("leadlag", out["leadlag"]["pairs"], out["leadlag"]["nominal"], out["leadlag"]["fdr"], out["leadlag"]["fdr_pos"])
    print(sig_pairs.head(20).round(3).to_string())
    print("shock", shock)
    print("divergence", {k: v for k, v in out["divergence"].items() if k != "now"})
    print(div_out.round(2).to_string())
    print(CH.sort_values("delta").head(8).round(3).to_string()); print(CH.sort_values("delta").tail(8).round(3).to_string())
    print("json KB", len(json.dumps(out)) // 1000)


if __name__ == "__main__":
    main()
