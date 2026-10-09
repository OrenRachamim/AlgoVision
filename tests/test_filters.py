import numpy as np
import pandas as pd

from algovision.research import filters as F
from algovision.research.factors import load_panel


def _frame(n=700, drift=0.0, seed=0, start="2023-01-02"):
    rng = np.random.default_rng(seed)
    close = 100 * np.cumprod(1 + rng.normal(drift, 0.012, n))
    idx = pd.bdate_range(start, periods=n)
    o = np.r_[close[0], close[:-1]]
    return pd.DataFrame({"Open": o, "High": np.maximum(o, close) * 1.005, "Low": np.minimum(o, close) * 0.995, "Close": close,
                         "Volume": np.full(n, 1e6)}, index=idx)


def test_conditions_and_study(tmp_path):
    frames = {**{f"D{i}": _frame(drift=-0.002, seed=i) for i in range(6)}, **{f"U{i}": _frame(drift=0.002, seed=10 + i) for i in range(6)}}
    spy = _frame(drift=0.0004, seed=99)
    panel = load_panel(list(frames), lambda s: frames[s])
    sectors = {s: ("tech" if int(s[1]) % 2 else "util") for s in frames}
    ctx = F.panel_context(panel, spy["Close"], sectors)
    assert set(ctx) >= {"basket20", "breadth50", "spy_above_ma50", "dd252", "z_rel20", "close"}
    idx = panel["Close"].index
    rng = np.random.default_rng(3)
    rows = []
    for k in range(120):
        s = list(frames)[k % 12]
        t = int(rng.integers(300, len(idx) - 70))
        c = frames[s]["Close"].to_numpy()
        o = frames[s]["Open"].to_numpy()
        rows.append({"symbol": s, "date": idx[t], "ret_20": c[t + 20] / o[t + 1] - 1, "xloc_20": rng.normal(0, 0.02), "ret_60": c[t + 60] / o[t + 1] - 1,
                     "xloc_60": rng.normal(0, 0.03)})
    ev = F.attach_conditions(pd.DataFrame(rows), ctx, "date")
    for c in F.CONDITION_NAMES:
        assert c in ev and ev[c].dtype == bool
    assert ev["ctx_ok"].all() and np.isfinite(ev["x_dd252"]).all()
    detail, find = F.condition_study(ev, "2025-01-01", list(F.CONDITION_NAMES), 20, 60)
    assert len(find) == len(F.CONDITION_NAMES) and {"consistent", "consistent_negative", "years_positive"} <= set(find.columns)
    assert set(detail["period"]) == {"train", "test"} and set(detail["state"]) == {"yes", "no"}
    ev["bucket"] = pd.cut(ev["x_dd252"], [-1, -0.2, 0], labels=["deep", "shallow"])
    bt = F.bucket_table(ev, "bucket", "2025-01-01")
    assert {"deep", "shallow"} >= set(bt["bucket"])
    late = F.newsday_late_entry(panel, spy["Close"], ev[["symbol", "date"]].copy())
    assert len(late) == len(ev) and {"std_ret_20", "late_ret_20", "late_entry_pos"} <= set(late.columns)
    lt = F.late_entry_table(late, "2025-01-01")
    assert set(lt["period"]) == {"train", "test"}
    fam = {"Test family": {"events": ev, "ret_col": "ret", "x_col": "xloc", "date_col": "date", "buckets": {"Depth": "bucket"}, "late": late, "slug": "test"}}
    p = F.write_filters_report(tmp_path, "2025-01-01", fam, doc_path=tmp_path / "doc.md")
    text = p.read_text(encoding="utf-8")
    assert "## Verdicts" in text and "### Conditions" in text and "Late entry" in text and (tmp_path / "doc.md").exists()
    assert (tmp_path / "test_findings.csv").exists()
