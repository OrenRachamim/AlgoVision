import numpy as np
import pandas as pd

from algovision import forward_note as N
from algovision.review import MIN_N, MIN_SPLIT


def _forward(section, n, xbk20, xbk_latest, read=None, seed=0, noise=0.001):
    """A synthetic forward frame: n names of one section with the given mean basket excess (plus ``noise``)."""
    rng = np.random.default_rng(seed)
    d = {"section": [section] * n, "symbol": [f"S{i}" for i in range(n)],
         "ret_20": rng.normal(0.02, 0.001, n), "spy_20": np.full(n, 0.01), "ret_latest": rng.normal(0.03, 0.001, n), "spy_latest": np.full(n, 0.01)}
    d["bk_20"] = d["ret_20"] - (xbk20 + rng.normal(0, noise, n))
    d["bk_latest"] = d["ret_latest"] - (xbk_latest + rng.normal(0, noise, n))
    F = pd.DataFrame(d)
    for h in ("20", "latest"):
        F[f"xspy_{h}"] = F[f"ret_{h}"] - F[f"spy_{h}"]
        F[f"xbk_{h}"] = F[f"ret_{h}"] - F[f"bk_{h}"]
    if read is not None:
        F["read"] = read
    return F


def test_table_note_quotes_both_benchmarks_and_the_review_verdict():
    F = _forward("newsday", MIN_N + 4, -0.05, -0.04)
    en = N.table_note(F, "newsday")
    assert en.startswith("**Forward test so far**") and "vs SPY" in en and "vs the beaten-down basket" in en
    assert "verdict: not working so far" in en and "Below the research expectation so far" in en and "stays in the report" in en
    he = N.table_note(F, "newsday", "he")
    assert he.startswith("**מבחן קדימה עד כה**") and "מול SPY" in he and "מול סל המוכות" in he and "לא עובד עד כה" in he and "מתחת לציפיית המחקר" in he
    assert N.table_note(F, "wedge") == "" and N.table_note(None, "newsday") == "" and N.table_note(pd.DataFrame(), "newsday") == ""


def test_table_note_marks_below_expectation_only_on_the_review_verdict():
    F = _forward("early_rally", MIN_N + 4, 0.03, 0.02)
    en = N.table_note(F, "early_rally")
    assert "verdict: works so far" in en and "Below the research expectation" not in en
    small = _forward("early_rally", 6, -0.05, -0.04)                 # too few names: no marker, verdict too early
    assert "too early" in N.table_note(small, "early_rally") and "Below the research expectation" not in N.table_note(small, "early_rally")
    noisy = _forward("wedge", MIN_N + 4, -0.002, -0.002, seed=3, noise=0.05)    # negative but within noise: no marker either
    assert "verdict: noise so far" in N.table_note(noisy, "wedge") and "Below the research expectation" not in N.table_note(noisy, "wedge")
    watch = _forward("wedge_watch", MIN_N + 4, -0.05, -0.04)        # a context table expects no edge: never marked
    assert "not working so far" in N.table_note(watch, "wedge_watch") and "Below the research expectation" not in N.table_note(watch, "wedge_watch")


def test_group_first_frame_keeps_duplicates_and_order():
    df = pd.DataFrame({"symbol": ["A", "B", "A", "C"], "v": [1, 2, 3, 4]})
    out = N.group_first_frame(df, {"C": {"g_beaten": True}})
    # C first (its group is beaten down), then the others in the order their symbol was first seen, duplicates kept together
    assert list(out["symbol"]) == ["C", "A", "A", "B"] and list(out["v"]) == [4, 1, 3, 2]
    assert len(N.group_first_frame(df.iloc[:0], {})) == 0


def test_read_note_splits_the_briefs_by_the_read():
    n = 2 * MIN_SPLIT + 4
    F = _forward("briefs", n, -0.03, -0.03, read=["signs of a bottom"] * (n // 2) + ["undecided"] * (n - n // 2))
    # make the 'signs of a bottom' half worse than the rest at both horizons
    F.loc[F["read"] == "signs of a bottom", ["xbk_20", "xbk_latest"]] -= 0.06
    en = N.read_note(F)
    assert en.startswith("**The read 'signs of a bottom' in the forward test**") and "better without it" in en and "have done worse" in en
    he = N.read_note(F, "he")
    assert "סימני תחתית" in he and "בלי התנאי טוב יותר" in he and "פחות טוב" in he
    assert N.read_note(F[F["read"] == "undecided"]) == "" and N.read_note(None) == ""      # one side only: nothing to say


def test_group_first_is_a_stable_reorder():
    peers = {"A": {"g_beaten": False}, "B": {"g_beaten": True}, "C": {}, "D": {"g_beaten": True}}
    assert N.group_first(["A", "B", "C", "D", "E"], peers) == ["B", "D", "A", "C", "E"]
    assert N.group_first([], peers) == []
