"""Do some stocks lead the others in their group?

Three tests on daily returns net of the market (residuals on RSP):

1. Pairwise predictive regression for every ordered pair (A -> B) inside a group:
       e_B[t] = a + b1*e_B[t-1] + c*e_A[t-1] + d*mkt[t-1] + u
   c > 0 and significant means yesterday's move in A predicts today's move in B, beyond B's own
   history and the market. White (HC0) standard errors; Benjamini-Hochberg FDR across all pairs;
   stability checked by re-estimating on each half of the sample.
2. Leader score per stock: share of its peers it predicts minus share that predict it.
3. Shock spillover: on days a stock moves more than 2.5 sd (net of market), the average signed
   response of its subgroup peers on the same day and over the next 1-5 days.
Also the same pairwise regression between subgroup baskets (cross-group leadership).

Usage: python leadlag_analysis.py [--years 3] [--out leadlag_results.json]
"""
import argparse
import json

import numpy as np
import pandas as pd
import yfinance as yf
from scipy import stats

from hierarchy_analysis import HIERARCHY, MARKET, resid

FDR = 0.10
SHOCK_SD = 2.5


def ols_t(y, X):
    """OLS with HC0 robust SE. Returns (coef, t) for the last regressor."""
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    cov = XtX_inv @ (X.T * u ** 2) @ X @ XtX_inv
    return beta[-1], beta[-1] / np.sqrt(cov[-1, -1])


def lead_test(e_a, e_b, mkt):
    """Does e_a[t-1] predict e_b[t]? Arrays aligned on the same days."""
    y = e_b[1:]
    X = np.column_stack([np.ones(len(y)), e_b[:-1], mkt[:-1], e_a[:-1]])
    return ols_t(y, X)


def bh(pvals, q):
    """Benjamini-Hochberg: boolean mask of discoveries."""
    p = np.asarray(pvals)
    order = np.argsort(p)
    thresh = q * (np.arange(1, len(p) + 1) / len(p))
    passed = p[order] <= thresh
    k = np.max(np.where(passed)[0]) + 1 if passed.any() else 0
    mask = np.zeros(len(p), bool)
    mask[order[:k]] = True
    return mask


def pair_table(E, mkt, pairs, meta):
    n = len(E)
    half = n // 2
    rows = []
    for a, b in pairs:
        ea, eb = E[a].values, E[b].values
        c, t = lead_test(ea, eb, mkt)
        c1, t1 = lead_test(ea[:half], eb[:half], mkt[:half])
        c2, t2 = lead_test(ea[half:], eb[half:], mkt[half:])
        hit = float((np.sign(ea[:-1]) == np.sign(eb[1:])).mean())
        rows.append(dict(leader=a, follower=b, coef=c, t=t, p=2 * stats.norm.sf(abs(t)),
                         t_h1=t1, t_h2=t2, coef_h1=c1, coef_h2=c2, hit=hit, **meta(a, b)))
    df = pd.DataFrame(rows)
    df["fdr"] = bh(df.p.values, FDR)
    df["stable"] = (np.sign(df.t_h1) == np.sign(df.t)) & (np.sign(df.t_h2) == np.sign(df.t)) \
        & (df.t_h1.abs() > 1.0) & (df.t_h2.abs() > 1.0)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", type=int, default=3)
    ap.add_argument("--out", default="leadlag_results.json")
    args = ap.parse_args()

    where = {t: (g, s) for g, (_, subs) in HIERARCHY.items() for s, m in subs.items() for t in m}
    px = yf.download(sorted(set(where) | {MARKET}), period=f"{args.years}y", auto_adjust=True,
                     progress=False)["Close"].ffill(limit=2)
    logret = np.log(px).diff().iloc[1:]
    stocks = [t for t in where if t in logret and logret[t].notna().mean() > 0.97]
    R = logret[stocks].dropna()
    mkt_s = logret[MARKET].loc[R.index]
    E = resid(R, mkt_s)
    mkt = mkt_s.values

    # 1. pairwise within groups
    pairs = [(a, b) for a in stocks for b in stocks if a != b and where[a][0] == where[b][0]]
    meta = lambda a, b: dict(group=where[a][0], sub_leader=where[a][1], sub_follower=where[b][1],
                             same_sub=where[a][1] == where[b][1])
    P = pair_table(E, mkt, pairs, meta)

    # 2. leader score
    sig = P[P.fdr & (P.coef > 0)]
    lead_rows = []
    for t in stocks:
        peers = sum(1 for o in stocks if o != t and where[o][0] == where[t][0])
        out_t = P[P.leader == t]
        in_t = P[P.follower == t]
        lead_rows.append(dict(
            ticker=t, group=where[t][0], sub=where[t][1], peers=peers,
            leads=int(((out_t.t > 1.96)).sum()), led_by=int(((in_t.t > 1.96)).sum()),
            leads_fdr=int((sig.leader == t).sum()), led_by_fdr=int((sig.follower == t).sum()),
            mean_t_out=float(out_t.t.mean()), mean_t_in=float(in_t.t.mean()),
        ))
    L = pd.DataFrame(lead_rows)
    L["score"] = (L.leads - L.led_by) / L.peers

    # 3. shock spillover inside subgroups
    sd = E.std()
    shocks = []
    for a in stocks:
        peers = [o for o in stocks if o != a and where[o][:2] == where[a][:2]]
        if not peers:
            continue
        days = np.where(np.abs(E[a].values) > SHOCK_SD * sd[a])[0]
        for d in days:
            if d + 5 >= len(E):
                continue
            s = np.sign(E[a].values[d])
            pe = E[peers].values
            shocks.append(dict(stock=a, group=where[a][0], sub=where[a][1], date=str(E.index[d].date()),
                               size=float(E[a].values[d] / sd[a]),
                               d0=float(s * pe[d].mean()), d1=float(s * pe[d + 1].mean()),
                               d2_5=float(s * pe[d + 2:d + 6].sum(axis=0).mean())))
    S = pd.DataFrame(shocks)

    def summarize(df):
        out = {}
        for k in ["d0", "d1", "d2_5"]:
            v = df[k].values
            out[k] = float(v.mean())
            out[k + "_t"] = float(v.mean() / (v.std(ddof=1) / np.sqrt(len(v)))) if len(v) > 2 else None
        out["n"] = int(len(df))
        return out

    shock_by_sub = []
    for (g, s), df in S.groupby(["group", "sub"]):
        shock_by_sub.append(dict(group=g, sub=s, **summarize(df)))
    shock_by_stock = []
    for a, df in S.groupby("stock"):
        shock_by_stock.append(dict(stock=a, group=where[a][0], sub=where[a][1], **summarize(df)))
    shock_all = summarize(S)

    # 4. subgroup baskets across groups
    baskets = {}
    for g, (_, subs) in HIERARCHY.items():
        for s, m in subs.items():
            m = [t for t in m if t in R]
            if len(m) > 1:
                baskets[f"{g}|{s}"] = R[m].mean(axis=1)
    B = resid(pd.DataFrame(baskets), mkt_s)
    bpairs = [(a, b) for a in B for b in B if a != b]
    BP = pair_table(B, mkt, bpairs, lambda a, b: dict(same_group=a.split("|")[0] == b.split("|")[0]))

    # weekly horizon: does last week's move in A predict this week's move in B?
    Rw = R.resample("W-FRI").sum()
    mw = mkt_s.resample("W-FRI").sum()
    Ew = resid(Rw, mw)
    PW = pair_table(Ew, mw.values, pairs, meta)

    # null check: how many FDR hits would we expect by chance? shuffle leader series in time
    rng = np.random.default_rng(0)
    null_hits = []
    for _ in range(5):
        perm = rng.permutation(len(E))
        Ep = E.copy()
        Ep[:] = E.values[perm]
        sample = [pairs[i] for i in rng.choice(len(pairs), 600, replace=False)]
        Pn = pair_table(Ep, mkt[perm], sample, lambda a, b: {})
        null_hits.append(float((Pn.t.abs() > 1.96).mean()))

    rec = lambda df: json.loads(df.to_json(orient="records", double_precision=4))
    out = dict(
        period=dict(start=str(R.index[0].date()), end=str(R.index[-1].date()), days=len(R)),
        params=dict(fdr=FDR, shock_sd=SHOCK_SD),
        summary=dict(
            pairs=len(P), nominal_5pct=int((P.t.abs() > 1.96).sum()),
            nominal_share=float((P.t.abs() > 1.96).mean()),
            null_share=float(np.mean(null_hits)),
            fdr_hits=int(P.fdr.sum()), fdr_pos=int((P.fdr & (P.coef > 0)).sum()),
            fdr_stable=int((P.fdr & P.stable).sum()),
            same_sub_share=float((P[P.same_sub].t.abs() > 1.96).mean()),
            diff_sub_share=float((P[~P.same_sub].t.abs() > 1.96).mean()),
            mean_hit=float(P.hit.mean()),
            weekly_weeks=len(Ew), weekly_nominal_share=float((PW.t.abs() > 1.96).mean()),
            weekly_fdr=int(PW.fdr.sum()), weekly_stable=int(((PW.t.abs() > 1.96) & PW.stable).sum()),
            basket_pairs=len(BP), basket_fdr=int(BP.fdr.sum()),
            basket_nominal_share=float((BP.t.abs() > 1.96).mean()),
        ),
        top_pairs=rec(P.sort_values("t", ascending=False).head(40)),
        neg_pairs=rec(P.sort_values("t").head(15)),
        group_summary=rec(P.groupby("group").apply(lambda d: pd.Series(dict(
            pairs=len(d), share_sig=(d.t.abs() > 1.96).mean(), fdr=int(d.fdr.sum()),
            mean_t=d.t.mean()))).reset_index()),
        leaders=rec(L.sort_values("score", ascending=False)),
        t_matrix={g: dict(stocks=[t for t in stocks if where[t][0] == g],
                          t=[[None if a == b else round(float(P[(P.leader == a) & (P.follower == b)].t.iloc[0]), 2)
                              for b in stocks if where[b][0] == g] for a in stocks if where[a][0] == g])
                  for g in HIERARCHY},
        subs={t: where[t][1] for t in stocks},
        shock_all=shock_all, shock_by_sub=shock_by_sub, shock_by_stock=shock_by_stock,
        weekly_top=rec(PW.sort_values("t", ascending=False).head(15)),
        basket_top=rec(BP.sort_values("t", ascending=False).head(20)),
    )
    with open(args.out, "w") as f:
        json.dump(out, f, allow_nan=False, default=lambda o: None)

    print(json.dumps(out["summary"], indent=1))
    cols = ["leader", "follower", "group", "coef", "t", "t_h1", "t_h2", "hit", "fdr", "stable"]
    print(P.sort_values("t", ascending=False).head(25)[cols].round(3).to_string())
    print(P.sort_values("t").head(8)[cols].round(3).to_string())
    print(L.sort_values("score", ascending=False).head(12).round(2).to_string())
    print(L.sort_values("score").head(6).round(2).to_string())
    print("shock all", shock_all)
    print(pd.DataFrame(shock_by_sub).sort_values("d1_t", ascending=False).round(4).to_string())
    print(BP.sort_values("t", ascending=False).head(12)[["leader", "follower", "coef", "t", "t_h1", "t_h2", "fdr"]].round(3).to_string())


if __name__ == "__main__":
    main()
