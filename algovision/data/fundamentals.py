"""Fundamental data from Yahoo's fundamentals time-series endpoint (no crumb needed).

Gives ~4 fiscal years of annual figures, the last 5 quarters, and trailing
valuation ratios.  Cached as JSON per symbol; refreshed daily.
"""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd

from algovision.data.provider import _DEFAULT_CACHE, _UA

log = logging.getLogger(__name__)

TYPES = [
    "annualTotalRevenue", "quarterlyTotalRevenue", "annualNetIncome", "quarterlyNetIncome",
    "annualDilutedEPS", "quarterlyDilutedEPS", "quarterlyGrossProfit", "annualOperatingIncome",
    "quarterlyOperatingIncome", "annualFreeCashFlow", "quarterlyFreeCashFlow", "quarterlyTotalDebt",
    "quarterlyStockholdersEquity", "quarterlyBasicAverageShares", "quarterlyResearchAndDevelopment",
    "trailingPegRatio", "trailingPeRatio", "trailingForwardPeRatio", "trailingMarketCap",
    "trailingEnterprisesValueRevenueRatio",
]


def fetch_fundamentals(symbol: str, timeout: int = 40, retries: int = 3) -> Dict[str, List[Dict]]:
    """Raw series: {type: [{"date": ..., "value": ...}, ...]} sorted by date."""
    import requests

    url = f"https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{symbol}"
    params = {"type": ",".join(TYPES), "period1": "946684800", "period2": str(int(time.time()) + 86400 * 400),
              "merge": "false", "padTimeSeries": "false"}
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=_UA, timeout=timeout)
            if r.status_code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            r.raise_for_status()
            out: Dict[str, List[Dict]] = {}
            for res in r.json()["timeseries"]["result"]:
                t = res["meta"]["type"][0]
                rows = []
                for v in res.get(t, []) or []:
                    if v and v.get("reportedValue") is not None:
                        rows.append({"date": v["asOfDate"], "value": float(v["reportedValue"]["raw"])})
                out[t] = sorted(rows, key=lambda x: x["date"])
            return out
        except Exception as exc:  # noqa: BLE001
            last = exc
            time.sleep(1 + attempt)
    raise RuntimeError(f"{symbol}: fundamentals failed ({last})")


def _last(series: List[Dict], k: int = 1) -> Optional[float]:
    return series[-k]["value"] if len(series) >= k else None


def _sum_last(series: List[Dict], k: int = 4) -> Optional[float]:
    return float(sum(x["value"] for x in series[-k:])) if len(series) >= k else None


def features(raw: Dict[str, List[Dict]]) -> Dict[str, Optional[float]]:
    """Growth / quality / valuation features from the raw series."""
    g = lambda t: raw.get(t, [])  # noqa: E731
    rev_a, rev_q = g("annualTotalRevenue"), g("quarterlyTotalRevenue")
    ni_q, eps_a, eps_q = g("quarterlyNetIncome"), g("annualDilutedEPS"), g("quarterlyDilutedEPS")
    gp_q, oi_q, fcf_q = g("quarterlyGrossProfit"), g("quarterlyOperatingIncome"), g("quarterlyFreeCashFlow")
    debt_q, eq_q, sh_q, rd_q = g("quarterlyTotalDebt"), g("quarterlyStockholdersEquity"), g("quarterlyBasicAverageShares"), g("quarterlyResearchAndDevelopment")
    f: Dict[str, Optional[float]] = {}

    def growth(a, b):
        return (a / b - 1.0) if (a is not None and b is not None and b > 0) else None

    def cagr(series, years):
        if len(series) > years and series[-1 - years]["value"] > 0 and series[-1]["value"] > 0:
            return (series[-1]["value"] / series[-1 - years]["value"]) ** (1 / years) - 1.0
        return None

    f["rev_cagr_3y"] = cagr(rev_a, 3)
    f["rev_growth_1y"] = growth(_last(rev_a), _last(rev_a, 2))
    f["rev_yoy_q"] = growth(_last(rev_q), _last(rev_q, 5))          # latest quarter vs same quarter last year
    f["eps_growth_1y"] = growth(_last(eps_a), _last(eps_a, 2)) if (_last(eps_a, 2) or 0) > 0 else None
    f["eps_yoy_q"] = growth(_last(eps_q), _last(eps_q, 5)) if (_last(eps_q, 5) or 0) > 0 else None
    rev_ttm, gp_ttm, oi_ttm, fcf_ttm, ni_ttm = (_sum_last(x) for x in (rev_q, gp_q, oi_q, fcf_q, ni_q))
    f["rev_ttm"] = rev_ttm
    f["gross_margin"] = gp_ttm / rev_ttm if gp_ttm is not None and rev_ttm else None
    f["op_margin"] = oi_ttm / rev_ttm if oi_ttm is not None and rev_ttm else None
    f["fcf_margin"] = fcf_ttm / rev_ttm if fcf_ttm is not None and rev_ttm else None
    f["net_margin"] = ni_ttm / rev_ttm if ni_ttm is not None and rev_ttm else None
    # margin trend: latest quarter operating margin vs same quarter last year
    if len(oi_q) >= 5 and len(rev_q) >= 5 and rev_q[-1]["value"] and rev_q[-5]["value"]:
        f["op_margin_change"] = oi_q[-1]["value"] / rev_q[-1]["value"] - oi_q[-5]["value"] / rev_q[-5]["value"]
    else:
        f["op_margin_change"] = None
    f["rd_intensity"] = (_sum_last(rd_q) / rev_ttm) if rd_q and rev_ttm and _sum_last(rd_q) is not None else None
    eq, debt = _last(eq_q), _last(debt_q)
    f["roe"] = ni_ttm / eq if ni_ttm is not None and eq and eq > 0 else None
    f["debt_to_equity"] = debt / eq if debt is not None and eq and eq > 0 else None
    f["share_change_1y"] = growth(_last(sh_q), _last(sh_q, 5))
    mcap = _last(g("trailingMarketCap"))
    f["market_cap"] = mcap
    f["fcf_yield"] = fcf_ttm / mcap if fcf_ttm is not None and mcap else None
    f["peg"] = _last(g("trailingPegRatio"))
    f["pe"] = _last(g("trailingPeRatio"))
    f["forward_pe"] = _last(g("trailingForwardPeRatio"))
    f["ev_to_revenue"] = _last(g("trailingEnterprisesValueRevenueRatio"))
    f["rule_of_40"] = (f["rev_yoy_q"] + f["fcf_margin"]) if f["rev_yoy_q"] is not None and f["fcf_margin"] is not None else None
    f["last_report"] = rev_q[-1]["date"] if rev_q else None
    return f


class FundamentalsProvider:
    def __init__(self, cache_dir: Optional[Path] = _DEFAULT_CACHE, max_age_hours: float = 24.0, workers: int = 4,
                 offline: bool = False):
        self.cache_dir = Path(cache_dir) / "fundamentals" if cache_dir else None
        self.max_age = max_age_hours * 3600
        self.workers = workers
        self.offline = offline
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, symbol: str) -> Dict[str, List[Dict]]:
        p = self.cache_dir / f"{symbol}.json" if self.cache_dir else None
        if p and p.exists() and (self.offline or time.time() - p.stat().st_mtime < self.max_age):
            return json.loads(p.read_text())
        if self.offline:
            raise RuntimeError(f"{symbol}: no cached fundamentals")
        raw = fetch_fundamentals(symbol)
        if p:
            p.write_text(json.dumps(raw))
        return raw

    def get_many(self, symbols: Iterable[str]) -> Dict[str, Dict[str, List[Dict]]]:
        out = {}
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futs = {ex.submit(self.get, s): s for s in symbols}
            for f in as_completed(futs):
                s = futs[f]
                try:
                    out[s] = f.result()
                except Exception as exc:  # noqa: BLE001
                    log.warning("%s: %s", s, exc)
        return out

    def feature_table(self, symbols: Iterable[str]) -> pd.DataFrame:
        raw = self.get_many(symbols)
        rows = []
        for s, r in raw.items():
            f = features(r)
            f["symbol"] = s
            rows.append(f)
        return pd.DataFrame(rows).set_index("symbol") if rows else pd.DataFrame()
