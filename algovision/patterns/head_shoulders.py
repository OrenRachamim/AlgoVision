"""Head & Shoulders (top) and Inverse Head & Shoulders (bottom)."""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

from algovision.core.geometry import clamp, prior_trend, ramp_score, tolerance_score, volume_trend
from algovision.core.types import KeyPoint, Line, PatternMatch, Pivot
from algovision.patterns.base import Detector


class HeadAndShouldersDetector(Detector):
    names = ("Head and Shoulders", "Inverse Head and Shoulders")

    def detect(self, symbol: str, df: pd.DataFrame, pivots: List[Pivot], order: int) -> List[PatternMatch]:
        out: List[PatternMatch] = []
        for inverse in (False, True):
            out.extend(self._detect_one(symbol, df, pivots, order, inverse))
        return out

    def _detect_one(self, symbol, df, pivots, order, inverse: bool) -> List[PatternMatch]:
        cfg = self.cfg
        close, high, low, vol = self.arrays(df)
        n = len(close)
        sgn = -1 if inverse else 1          # multiply prices by sgn so "up" is always the head direction
        want = [-sgn, sgn, -sgn, sgn, -sgn]  # kinds: shoulder, trough, head, trough, shoulder  (as sign of pivot)
        want = [1 * sgn, -1 * sgn, 1 * sgn, -1 * sgn, 1 * sgn]
        out: List[PatternMatch] = []
        for i in range(len(pivots) - 4):
            seq = pivots[i:i + 5]
            if [p.kind for p in seq] != want:
                continue
            ls, t1, hd, t2, rs = seq
            LS, T1, HD, T2, RS = (sgn * p.price for p in seq)
            # 1. head must stand above both shoulders
            prominence = (HD - max(LS, RS)) / abs(HD)
            if prominence < cfg.hs_min_head_prominence:
                continue
            # 2. shoulders roughly level
            sym = abs(LS - RS) / ((abs(LS) + abs(RS)) / 2)
            if sym > cfg.hs_shoulder_tol:
                continue
            # 3. neckline roughly flat
            neck_diff = abs(T1 - T2) / abs(HD)
            if neck_diff > cfg.hs_neckline_tol:
                continue
            # 4. troughs clearly below the shoulders
            trough_gap = (min(LS, RS) - max(T1, T2)) / abs(HD)
            if trough_gap < 0.005:
                continue
            # 5. time symmetry
            wl, wr = hd.idx - ls.idx, rs.idx - hd.idx
            ratio = wl / wr if wr else 99
            if not (cfg.hs_time_symmetry[0] <= ratio <= cfg.hs_time_symmetry[1]):
                continue

            width = rs.idx - ls.idx
            slope = (t2.price - t1.price) / (t2.idx - t1.idx)

            def neck(x, _s=slope, _t=t1):
                return _t.price + _s * (x - _t.idx)

            neck_head = neck(hd.idx)
            height = abs(hd.price - neck_head)
            # 6. prior trend (H&S tops need an uptrend into the pattern; inverse needs a downtrend)
            trend = prior_trend(close, ls.idx, max(width, 20)) * sgn
            # 7. breakout search after right shoulder
            direction = -sgn                      # top -> breaks down, inverse -> breaks up
            bo = self.breakout(close, rs.idx + 1, neck, direction)
            # failure: price moves beyond the head before breaking the neckline
            fail_idx = None
            for j in range(rs.idx + 1, n if bo is None else bo):
                if sgn * close[j] > HD:
                    fail_idx = j
                    break
            if fail_idx is not None:
                status = "failed"
                end_idx = fail_idx
                bo = None
            elif bo is not None:
                status = "confirmed"
                end_idx = bo
            else:
                status = "forming"
                end_idx = n - 1
                # too old without a breakout -> the setup is stale
                if n - 1 - rs.idx > max(width, 30):
                    status = "expired"

            # ---- scoring ------------------------------------------------
            s_prom = ramp_score(prominence, cfg.hs_min_head_prominence, 0.06)
            s_sym = tolerance_score(sym, cfg.hs_shoulder_tol)
            s_neck = tolerance_score(neck_diff, cfg.hs_neckline_tol)
            s_time = 1.0 - clamp(abs(np.log(ratio)) / np.log(cfg.hs_time_symmetry[1]))
            s_trend = ramp_score(trend, 0.0, 0.10)
            vtrend = volume_trend(vol, ls.idx, rs.idx)
            s_vol = 0.5 if vtrend is None else clamp(0.5 - vtrend)   # declining volume across the pattern is classic
            comps = {"prominence": (s_prom, 0.22), "symmetry": (s_sym, 0.18), "neckline": (s_neck, 0.15),
                     "timing": (s_time, 0.10), "trend": (s_trend, 0.15), "volume": (s_vol, 0.08)}
            s_bo, bo_reason = (0.5, None)
            if bo is not None:
                s_bo, bo_reason = self.breakout_volume_reason(vol, bo)
                comps["breakout_volume"] = (s_bo, 0.12)
            score = sum(v * w for v, w in comps.values()) / sum(w for _, w in comps.values())
            if status == "failed":
                score *= 0.6
            elif status == "expired":
                score *= 0.7

            name = "Inverse Head and Shoulders" if inverse else "Head and Shoulders"
            side = "bottom" if inverse else "top"
            target = neck(end_idx) + direction * height
            stop = rs.price
            reasons = [
                f"{'Left shoulder' if True else ''} at {ls.price:.2f} and right shoulder at {rs.price:.2f} are within "
                f"{sym * 100:.1f}% of each other (tolerance {cfg.hs_shoulder_tol * 100:.0f}%)",
                f"Head at {hd.price:.2f} is {prominence * 100:.1f}% {'below' if inverse else 'above'} the higher shoulder",
                f"Neckline through {t1.price:.2f} and {t2.price:.2f} is nearly flat ({neck_diff * 100:.1f}% difference)",
                f"Left/right halves take {wl} and {wr} bars (time symmetry ratio {ratio:.2f})",
            ]
            if trend > 0.03:
                reasons.append(f"Price {'fell' if inverse else 'rose'} {abs(trend) * 100:.1f}% into the pattern "
                               f"(a prior {'downtrend' if inverse else 'uptrend'} is required for a {side} reversal)")
            else:
                reasons.append(f"Weak prior {'downtrend' if inverse else 'uptrend'} ({trend * 100:+.1f}%) - lowers confidence")
            if vtrend is not None:
                reasons.append(f"Volume {'declined' if vtrend < 0 else 'rose'} {abs(vtrend) * 100:.0f}% across the pattern"
                               + (" (classic)" if vtrend < 0 else " (atypical)"))
            if status == "confirmed":
                reasons.append(f"Confirmed: close {close[bo]:.2f} broke the neckline ({neck(bo):.2f}) "
                               f"{'up' if inverse else 'down'} at bar {bo}")
                if bo_reason:
                    reasons.append(bo_reason)
            elif status == "forming":
                reasons.append(f"Right shoulder complete; waiting for a close {'above' if inverse else 'below'} "
                               f"the neckline (~{neck(n - 1):.2f}, last close {close[-1]:.2f})")
            elif status == "failed":
                reasons.append(f"Failed: price moved beyond the head ({hd.price:.2f}) before the neckline broke")
            else:
                reasons.append("Expired: no neckline break within a reasonable time after the right shoulder")
            reasons.append(f"Measured move: pattern height {height:.2f} projected from the neckline -> target {target:.2f} "
                           f"({(target / close[end_idx] - 1) * 100:+.1f}% from {close[end_idx]:.2f})")

            m = PatternMatch(
                symbol=symbol, pattern=name, direction="bullish" if inverse else "bearish", status=status,
                start_idx=ls.idx, end_idx=end_idx, score=float(score), reasons=reasons,
                key_points=[KeyPoint(ls.idx, ls.price, "Left shoulder"), KeyPoint(t1.idx, t1.price, "Neck 1"),
                            KeyPoint(hd.idx, hd.price, "Head"), KeyPoint(t2.idx, t2.price, "Neck 2"),
                            KeyPoint(rs.idx, rs.price, "Right shoulder")],
                lines=[Line(t1.idx, t1.price, max(end_idx, rs.idx + 5), neck(max(end_idx, rs.idx + 5)), "Neckline")],
                metrics={"head_prominence": prominence, "shoulder_diff": sym, "neckline_diff": neck_diff,
                         "time_ratio": ratio, "prior_trend": trend, "height": height, "volume_trend": vtrend,
                         "components": {k: v[0] for k, v in comps.items()}},
                breakout_idx=bo, breakout_price=float(close[bo]) if bo is not None else None,
                level=float(neck(end_idx)), target=float(target), stop=float(stop), scale=order,
            )
            out.append(m)
        return out
