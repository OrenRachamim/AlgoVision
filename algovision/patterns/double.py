"""Double / Triple Tops and Bottoms."""

from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd

from algovision.core.geometry import clamp, prior_trend, ramp_score, tolerance_score
from algovision.core.types import KeyPoint, Line, PatternMatch, Pivot
from algovision.patterns.base import Detector


class DoubleTopBottomDetector(Detector):
    names = ("Double Top", "Double Bottom", "Triple Top", "Triple Bottom")

    def detect(self, symbol: str, df: pd.DataFrame, pivots: List[Pivot], order: int) -> List[PatternMatch]:
        out: List[PatternMatch] = []
        for top in (True, False):
            out.extend(self._detect(symbol, df, pivots, order, top, count=3))
            out.extend(self._detect(symbol, df, pivots, order, top, count=2))
        return out

    def _detect(self, symbol, df, pivots, order, top: bool, count: int) -> List[PatternMatch]:
        cfg = self.cfg
        close, high, low, vol = self.arrays(df)
        n = len(close)
        sgn = 1 if top else -1
        length = 2 * count - 1
        want = [sgn if k % 2 == 0 else -sgn for k in range(length)]
        out: List[PatternMatch] = []
        for i in range(len(pivots) - length + 1):
            seq = pivots[i:i + length]
            if [p.kind for p in seq] != want:
                continue
            peaks = seq[0::2]
            troughs = seq[1::2]
            P = np.array([p.price for p in peaks])
            T = np.array([t.price for t in troughs])
            ref = float(P.mean())
            # 1. peaks level with each other
            spread = float((P.max() - P.min()) / ref)
            if spread > cfg.dt_peak_tol:
                continue
            # 2. meaningful pullback between them (shallowest one counts)
            if top:
                depth = float((ref - T.max()) / ref)
            else:
                depth = float((T.min() - ref) / ref)
            if depth < cfg.dt_min_depth:
                continue
            # 3. separation in time
            gaps = [peaks[k + 1].idx - peaks[k].idx for k in range(count - 1)]
            if min(gaps) < cfg.dt_min_separation:
                continue
            # for a triple, the troughs must be level too (rising troughs == ascending triangle)
            if count == 3:
                tspread = float((T.max() - T.min()) / ref)
                if tspread > cfg.dt_peak_tol:
                    continue
            first, last = peaks[0], peaks[-1]
            width = last.idx - first.idx
            level = float(T.min() if top else T.max())   # confirmation line (lowest trough for tops)
            direction = -1 if top else 1
            trend = prior_trend(close, first.idx, max(width, 20)) * sgn
            bo = self.breakout(close, last.idx + 1, lambda x, _l=level: _l, direction)
            extreme = float(P.max() if top else P.min())
            fail_idx = None
            for j in range(last.idx + 1, n if bo is None else bo):
                if (top and close[j] > extreme * (1 + cfg.dt_peak_tol)) or (not top and close[j] < extreme * (1 - cfg.dt_peak_tol)):
                    fail_idx = j
                    break
            if fail_idx is not None:
                status, end_idx, bo = "failed", fail_idx, None
            elif bo is not None:
                status, end_idx = "confirmed", bo
            else:
                status, end_idx = "forming", n - 1
                if n - 1 - last.idx > max(width, 30):
                    status = "expired"

            height = abs(ref - level)
            target = level + direction * height
            s_level = tolerance_score(spread, cfg.dt_peak_tol)
            s_depth = ramp_score(depth, cfg.dt_min_depth, 0.10)
            s_trend = ramp_score(trend, 0.0, 0.10)
            s_sep = ramp_score(min(gaps), cfg.dt_min_separation, cfg.dt_min_separation * 3)
            comps = {"level": (s_level, 0.3), "depth": (s_depth, 0.2), "trend": (s_trend, 0.2), "separation": (s_sep, 0.1)}
            bo_reason = None
            if bo is not None:
                s_bo, bo_reason = self.breakout_volume_reason(vol, bo)
                comps["breakout_volume"] = (s_bo, 0.2)
            score = sum(v * w for v, w in comps.values()) / sum(w for _, w in comps.values())
            if status == "failed":
                score *= 0.6
            elif status == "expired":
                score *= 0.7

            word = "Top" if top else "Bottom"
            name = f"{'Triple' if count == 3 else 'Double'} {word}"
            what = "peaks" if top else "troughs"
            pts = ", ".join(f"{p.price:.2f}" for p in peaks)
            reasons = [
                f"{count} {what} at {pts} within {spread * 100:.1f}% of each other (tolerance {cfg.dt_peak_tol * 100:.1f}%)",
                f"Pullback between the {what} is {depth * 100:.1f}% deep (minimum {cfg.dt_min_depth * 100:.0f}%)",
                f"{what.capitalize()} are {min(gaps)}+ bars apart (minimum {cfg.dt_min_separation})",
            ]
            if trend > 0.03:
                reasons.append(f"Price {'rose' if top else 'fell'} {abs(trend) * 100:.1f}% into the pattern (prior trend present)")
            else:
                reasons.append(f"Weak prior {'uptrend' if top else 'downtrend'} ({trend * 100:+.1f}%) - lowers confidence")
            if status == "confirmed":
                reasons.append(f"Confirmed: close {close[bo]:.2f} broke the {'support' if top else 'resistance'} at {level:.2f} at bar {bo}")
                if bo_reason:
                    reasons.append(bo_reason)
            elif status == "forming":
                reasons.append(f"Waiting for a close {'below' if top else 'above'} {level:.2f} (last close {close[-1]:.2f})")
            elif status == "failed":
                reasons.append(f"Failed: price pushed through the {what} level ({extreme:.2f}) before confirming")
            else:
                reasons.append("Expired: no confirmation within a reasonable time")
            reasons.append(f"Measured move: {height:.2f} projected from {level:.2f} -> target {target:.2f} "
                           f"({(target / close[end_idx] - 1) * 100:+.1f}%)")

            kps = [KeyPoint(p.idx, p.price, f"{word} {k + 1}") for k, p in enumerate(peaks)]
            kps += [KeyPoint(t.idx, t.price, "Trough" if top else "Peak") for t in troughs]
            m = PatternMatch(
                symbol=symbol, pattern=name, direction="bearish" if top else "bullish", status=status,
                start_idx=first.idx, end_idx=end_idx, score=float(score), reasons=reasons, key_points=kps,
                lines=[Line(first.idx, level, max(end_idx, last.idx + 5), level, "Confirmation level", "dashed"),
                       Line(first.idx, ref, last.idx, ref, f"{word} level", "dotted")],
                metrics={"peak_spread": spread, "depth": depth, "prior_trend": trend, "min_gap": min(gaps),
                         "components": {k: v[0] for k, v in comps.items()}},
                breakout_idx=bo, breakout_price=float(close[bo]) if bo is not None else None,
                level=level, target=float(target), stop=extreme, scale=order,
            )
            out.append(m)
        return out
