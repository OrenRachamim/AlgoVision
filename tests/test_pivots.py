import numpy as np
import pandas as pd

from algovision.core.pivots import atr, find_pivots
from algovision.data.synthetic import random_walk, head_and_shoulders


def test_pivots_alternate_and_are_sorted():
    df = random_walk(300, seed=3)
    for order in (3, 5, 8):
        pv = find_pivots(df, order=order)
        assert len(pv) >= 2
        assert all(pv[i].idx < pv[i + 1].idx for i in range(len(pv) - 1))
        assert all(pv[i].kind != pv[i + 1].kind for i in range(len(pv) - 1))
        for p in pv:
            if p.is_high:
                assert np.isclose(p.price, df["High"].iloc[p.idx])
            else:
                assert np.isclose(p.price, df["Low"].iloc[p.idx])


def test_larger_order_gives_fewer_pivots():
    df = random_walk(400, seed=5)
    counts = [len(find_pivots(df, order=o)) for o in (2, 5, 13)]
    assert counts[0] >= counts[1] >= counts[2]


def test_min_move_filter_removes_noise():
    df = random_walk(400, seed=7)
    loose = find_pivots(df, order=3, min_move_atr=0.0, min_move_pct=0.0)
    strict = find_pivots(df, order=3, min_move_atr=3.0, min_move_pct=0.05)
    assert len(strict) < len(loose)


def test_head_pivot_found():
    df, meta = head_and_shoulders()
    pv = find_pivots(df, order=5)
    highs = [p for p in pv if p.is_high]
    head = max(highs, key=lambda p: p.price)
    assert 80 <= head.idx <= 90


def test_atr_positive():
    df = random_walk(100)
    a = atr(df)
    assert a.shape == (100,)
    assert np.all(a > 0)


def test_too_short_series():
    df = random_walk(5)
    assert find_pivots(df, order=5) == []
