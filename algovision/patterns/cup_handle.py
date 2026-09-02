"""Cup and Handle (bullish continuation) and its inverted counterpart."""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd

from algovision.core.geometry import clamp, prior_trend, r_squared, ramp_score, tolerance_score, volume_trend
from algovision.core.types import KeyPoint, Line, PatternMatch, Pivot
from algovision.patterns.base import Detector


class CupAndHandleDetector(Detector):
    names = ("Cup and Handle", "Inverted Cup and Handle")

    def detect(self, symbol: str, df: pd.DataFrame, pivots: List[Pivot], order: int) -> List[PatternMatch]:
        out = self._detect(symbol, df, pivots, order, inverted=False)
        out += self._detect(symbol, df, pivots, order, inverted=True)
        return out

    def _detect(self, symbol, df, pivots, order, inverted: bool) -> List[PatternMatch]:
        cfg = self.cfg
        close, high, low, vol = self.arrays(df)
        n = len(close)
        sgn = -1 if inverted else 1            # work in a frame where the cup always opens upward
        c = sgn * close
        rims = [p for p in pivots if p.kind == sgn]
        out: List[PatternMatch] = []
        for a_i, a in enumerate(rims):
            for b in rims[a_i + 1:]:
                L = b.idx - a.idx
                if L < cfg.cup_min_bars:
                    continue
                if L > cfg.cup_max_bars:
                    break
                A, B = sgn * a.price, sgn * b.price
                rim = max(A, B)
                # 1. rims roughly level; right rim may not exceed the left by much
                rim_diff = (B - A) / abs(A)
                if abs(rim_diff) > cfg.cup_rim_tol:
                    continue
                seg = c[a.idx:b.idx + 1]
                # 2. nothing inside the cup above the rims
                if seg[1:-1].max() > rim * (1 + 0.01):
                    continue
                bottom_rel = int(np.argmin(seg))
                bottom_idx = a.idx + bottom_rel
                depth = (rim - seg[bottom_rel]) / abs(rim)
                if not (cfg.cup_min_depth <= depth <= cfg.cup_max_depth):
                    continue
                # 3. bottom sits in the middle part of the cup (not a V at one edge)
                pos = bottom_rel / L
                if not (0.2 <= pos <= 0.8):
                    continue
                # 4. rounded: a parabola should explain the cup well
                x = np.linspace(-1, 1, len(seg))
                coeffs = np.polyfit(x, seg, 2)
                fitted = np.polyval(coeffs, x)
                r2 = r_squared(seg, fitted)
                if coeffs[0] <= 0 or r2 < cfg.cup_min_r2:
                    continue
                # 5. handle: pullback after the right rim, shallow and short
                h_start = b.idx
                h_max_len = max(cfg.handle_min_bars, int(L * cfg.handle_max_frac))
                h_end_limit = min(n - 1, h_start + h_max_len)
                if h_end_limit - h_start < cfg.handle_min_bars:
                    continue
                hseg = c[h_start:h_end_limit + 1]
                # the handle ends at breakout (close above rim) or at the last available bar
                bo: Optional[int] = None
                for j in range(h_start + cfg.handle_min_bars, n):
                    if c[j] > rim * (1 + cfg.breakout_confirm_pct):
                        bo = j
                        break
                    if j >= h_end_limit:
                        break
                h_end = bo if bo is not None else h_end_limit
                handle = c[h_start:h_end + 1]
                h_low_rel = int(np.argmin(handle[:-1])) if len(handle) > 1 else 0
                h_low_idx = h_start + h_low_rel
                h_depth = (rim - handle[h_low_rel]) / abs(rim)
                if h_depth < 0.005:
                    continue                       # no pullback == no handle
                if h_depth > cfg.handle_max_depth or h_depth > depth * cfg.handle_max_depth_frac:
                    continue
                # the handle must stay in the upper half of the cup
                if handle[h_low_rel] < seg[bottom_rel] + 0.5 * (rim - seg[bottom_rel]):
                    continue
                if bo is None and (n - 1 - h_low_idx) > h_max_len:
                    status = "expired"
                elif bo is None:
                    status = "forming"
                else:
                    status = "confirmed"
                end_idx = bo if bo is not None else n - 1
                # failure: price falls below the cup midpoint before breaking out
                mid = seg[bottom_rel] + 0.5 * (rim - seg[bottom_rel])
                if bo is None and c[h_start:end_idx + 1].min() < mid:
                    status = "failed"
                trend = prior_trend(close, a.idx, max(L // 2, 20)) * sgn
                vt_cup = volume_trend(vol, a.idx, b.idx)
                vt_handle = volume_trend(vol, h_start, h_end)

                s_depth = 1.0 - clamp(abs(depth - 0.25) / 0.30)      # ~12-35% is textbook
                s_round = ramp_score(r2, cfg.cup_min_r2, 0.95)
                s_rim = tolerance_score(rim_diff, cfg.cup_rim_tol)
                s_pos = 1.0 - clamp(abs(pos - 0.5) / 0.3)
                s_handle = 1.0 - clamp(h_depth / cfg.handle_max_depth)
                s_trend = ramp_score(trend, 0.0, 0.15)
                s_vol = 0.5 if vt_handle is None else clamp(0.5 - vt_handle)
                comps = {"depth": (s_depth, 0.15), "roundness": (s_round, 0.25), "rims": (s_rim, 0.15),
                         "bottom_position": (s_pos, 0.10), "handle": (s_handle, 0.15), "trend": (s_trend, 0.10),
                         "volume": (s_vol, 0.10)}
                bo_reason = None
                if bo is not None:
                    s_bo, bo_reason = self.breakout_volume_reason(vol, bo)
                    comps["breakout_volume"] = (s_bo, 0.15)
                score = sum(v * w for v, w in comps.values()) / sum(w for _, w in comps.values())
                if status == "failed":
                    score *= 0.6
                elif status == "expired":
                    score *= 0.7
                if score < cfg.min_score * 0.8:
                    continue

                real_rim = sgn * rim
                real_bottom = close[bottom_idx]
                height = abs(real_rim - real_bottom)
                target = real_rim + sgn * height
                name = "Inverted Cup and Handle" if inverted else "Cup and Handle"
                reasons = [
                    f"Rounded {'top' if inverted else 'bottom'} over {L} bars from {a.price:.2f} to {b.price:.2f} "
                    f"(rims within {abs(rim_diff) * 100:.1f}%)",
                    f"Cup depth {depth * 100:.1f}% (typical 12-35%); low at bar {bottom_idx}, "
                    f"{pos * 100:.0f}% of the way across (U-shape, not V)",
                    f"Parabolic fit explains {r2 * 100:.0f}% of the cup's shape (rounded, not jagged)",
                    f"Handle: {h_end - h_start} bars pulling back {h_depth * 100:.1f}% from the rim "
                    f"(<= {cfg.handle_max_depth_frac * 100:.0f}% of the cup depth, stays in upper half)",
                ]
                if trend > 0.05:
                    reasons.append(f"Price {'fell' if inverted else 'rose'} {abs(trend) * 100:.1f}% before the cup (continuation context)")
                if vt_cup is not None:
                    reasons.append(f"Volume {'fell' if vt_cup < 0 else 'rose'} {abs(vt_cup) * 100:.0f}% across the cup")
                if vt_handle is not None and vt_handle < 0:
                    reasons.append(f"Volume dried up {abs(vt_handle) * 100:.0f}% in the handle (classic)")
                if status == "confirmed":
                    reasons.append(f"Confirmed: close {close[bo]:.2f} broke {'below' if inverted else 'above'} the rim ({real_rim:.2f}) at bar {bo}")
                    if bo_reason:
                        reasons.append(bo_reason)
                elif status == "forming":
                    reasons.append(f"Handle in progress; a close {'below' if inverted else 'above'} {real_rim:.2f} would confirm "
                                   f"(last close {close[-1]:.2f})")
                elif status == "failed":
                    reasons.append("Failed: the handle fell below the cup midpoint")
                else:
                    reasons.append("Expired: handle overstayed without a breakout")
                reasons.append(f"Measured move: cup depth {height:.2f} projected from the rim -> target {target:.2f} "
                               f"({(target / close[end_idx] - 1) * 100:+.1f}%)")
                m = PatternMatch(
                    symbol=symbol, pattern=name, direction="bearish" if inverted else "bullish", status=status,
                    start_idx=a.idx, end_idx=end_idx, score=float(score), reasons=reasons,
                    key_points=[KeyPoint(a.idx, a.price, "Left rim"), KeyPoint(bottom_idx, float(real_bottom), "Cup low" if not inverted else "Cup high"),
                                KeyPoint(b.idx, b.price, "Right rim"), KeyPoint(h_low_idx, float(close[h_low_idx]), "Handle low" if not inverted else "Handle high")],
                    lines=[Line(a.idx, real_rim, max(end_idx, b.idx + 5), real_rim, "Rim / breakout level", "dashed")],
                    metrics={"cup_bars": L, "depth": depth, "r2": r2, "rim_diff": rim_diff, "bottom_pos": pos,
                             "handle_bars": h_end - h_start, "handle_depth": h_depth, "prior_trend": trend,
                             "components": {k: v[0] for k, v in comps.items()}},
                    breakout_idx=bo, breakout_price=float(close[bo]) if bo is not None else None,
                    level=float(real_rim), target=float(target), stop=float(close[h_low_idx]), scale=order,
                )
                out.append(m)
        return out
