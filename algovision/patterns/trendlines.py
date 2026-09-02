"""Trendline-bounded patterns: triangles, wedges and rectangles.

Consecutive alternating pivots are split into highs and lows; a straight line
is fitted to each set.  The pair of lines is then classified by the
(normalised) slope of each boundary:

* Ascending triangle   - flat top, rising bottom            (bullish)
* Descending triangle  - falling top, flat bottom           (bearish)
* Symmetrical triangle - falling top, rising bottom         (breakout direction)
* Rising wedge         - both rising, converging            (bearish)
* Falling wedge        - both falling, converging           (bullish)
* Rectangle            - both flat                          (breakout direction)
"""

from __future__ import annotations

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

from algovision.core.geometry import clamp, fit_line, prior_trend, ramp_score, volume_trend
from algovision.core.types import KeyPoint, Line, PatternMatch, Pivot
from algovision.patterns.base import Detector


class TrendlinePatternDetector(Detector):
    names = ("Ascending Triangle", "Descending Triangle", "Symmetrical Triangle",
             "Rising Wedge", "Falling Wedge", "Rectangle")

    def detect(self, symbol: str, df: pd.DataFrame, pivots: List[Pivot], order: int) -> List[PatternMatch]:
        cfg = self.cfg
        close, high, low, vol = self.arrays(df)
        n = len(close)
        out: List[PatternMatch] = []
        for k in range(cfg.tl_min_pivots, cfg.tl_max_pivots + 1):
            for i in range(len(pivots) - k + 1):
                seq = pivots[i:i + k]
                m = self._evaluate(symbol, seq, close, high, low, vol, n, order)
                if m is not None:
                    out.append(m)
        return out

    # ------------------------------------------------------------------
    def _classify(self, su: float, sl: float, conv: float) -> Optional[Tuple[str, str]]:
        f = self.cfg.tl_flat_slope
        flat_u, flat_l = abs(su) <= f, abs(sl) <= f
        if flat_u and flat_l:
            return "Rectangle", "neutral"
        if flat_u and sl > f:
            return "Ascending Triangle", "bullish"
        if flat_l and su < -f:
            return "Descending Triangle", "bearish"
        if su < -f and sl > f:
            # both sides must contribute to the squeeze, otherwise it is a
            # lopsided channel rather than a symmetrical triangle
            if min(abs(su), abs(sl)) / max(abs(su), abs(sl)) < 0.3:
                return None
            return "Symmetrical Triangle", "neutral"
        if su > f and sl > f and conv > 0.15:
            return "Rising Wedge", "bearish"
        if su < -f and sl < -f and conv > 0.15:
            return "Falling Wedge", "bullish"
        return None

    def _evaluate(self, symbol, seq, close, high, low, vol, n, order) -> Optional[PatternMatch]:
        cfg = self.cfg
        highs = [p for p in seq if p.kind > 0]
        lows = [p for p in seq if p.kind < 0]
        if len(highs) < 2 or len(lows) < 2:
            return None
        x0, x1 = seq[0].idx, seq[-1].idx
        width = x1 - x0
        if width < 10:
            return None
        su_raw, iu, ru = fit_line([p.idx for p in highs], [p.price for p in highs])
        sl_raw, il, rl = fit_line([p.idx for p in lows], [p.price for p in lows])
        upper = lambda x: iu + su_raw * x   # noqa: E731
        lower = lambda x: il + sl_raw * x   # noqa: E731
        h0 = upper(x0) - lower(x0)
        h1 = upper(x1) - lower(x1)
        price = float(np.mean(close[x0:x1 + 1]))
        if h0 <= 0 or h0 / price < cfg.tl_min_height or h0 / price > cfg.tl_max_height:
            return None
        # the fitted boundaries must describe the actual traded range, not an
        # extrapolation far above/below it (two steep touches can otherwise
        # produce absurd heights and targets)
        actual_range = float(high[x0:x1 + 1].max() - low[x0:x1 + 1].min())
        if actual_range <= 0 or h0 > 1.25 * actual_range:
            return None
        if lower(x0) < low[x0:x1 + 1].min() - 0.5 * actual_range or upper(x0) > high[x0:x1 + 1].max() + 0.5 * actual_range:
            return None
        # touches must sit close to their line
        if max(ru, rl) / h0 > cfg.tl_max_residual:
            return None
        # each boundary must be *touched* in both halves of the pattern; otherwise
        # one line is just an extrapolation through two distant points
        mid = (x0 + x1) // 2
        for lo_x, hi_x in ((x0, mid), (mid, x1)):
            xs_h = np.arange(lo_x, hi_x + 1)
            if len(xs_h) == 0:
                return None
            if np.min(upper(xs_h) - high[lo_x:hi_x + 1]) > 0.3 * h0:
                return None
            if np.min(low[lo_x:hi_x + 1] - lower(xs_h)) > 0.3 * h0:
                return None
        # normalised slopes: how far each line travels over the pattern, in units of initial height
        su = su_raw * width / h0
        sl = sl_raw * width / h0
        conv = 1.0 - h1 / h0                       # >0 when converging
        cls = self._classify(su, sl, conv)
        if cls is None:
            return None
        name, bias = cls
        if name != "Rectangle" and conv < 0.15:
            return None                            # triangles / wedges must converge
        if name == "Rectangle" and abs(conv) > 0.35:
            return None
        # price must actually stay inside the channel during the pattern (few violations)
        xs = np.arange(x0, x1 + 1)
        above = close[x0:x1 + 1] > upper(xs) * (1 + 0.01)
        below = close[x0:x1 + 1] < lower(xs) * (1 - 0.01)
        viol = float((above | below).mean())
        if viol > 0.10:
            return None
        # apex (triangles / wedges) must not be too far away
        apex = None
        if su_raw != sl_raw:
            apex = (il - iu) / (su_raw - sl_raw)
            if name != "Rectangle" and (apex < x1 or apex - x1 > cfg.tl_apex_max_frac * width):
                return None
        # breakout after the last pivot
        end_limit = n if apex is None else min(n, int(apex) + 1)
        bo_up = self.breakout(close, x1 + 1, upper, +1, None)
        bo_dn = self.breakout(close, x1 + 1, lower, -1, None)
        bo, direction = None, 0
        if bo_up is not None and (bo_dn is None or bo_up <= bo_dn):
            bo, direction = bo_up, +1
        elif bo_dn is not None:
            bo, direction = bo_dn, -1
        expected = {"bullish": 1, "bearish": -1, "neutral": 0}[bias]
        if bo is not None:
            status, end_idx = "confirmed", bo
            if expected != 0 and direction != expected:
                status = "failed"       # broke the "wrong" way
        else:
            end_idx = n - 1
            status = "forming"
            if name != "Rectangle" and apex is not None and n - 1 > apex:
                status = "expired"
            elif n - 1 - x1 > max(width, 30):
                status = "expired"
        final_dir = direction if direction != 0 else expected
        if final_dir == 0:
            trend = prior_trend(close, x0, max(width, 20))
            final_dir = 1 if trend >= 0 else -1    # neutral patterns lean with the prior trend
        trend = prior_trend(close, x0, max(width, 20))
        vt = volume_trend(vol, x0, x1)

        touches = len(highs) + len(lows)
        s_touch = ramp_score(touches, 4, 7)
        s_fit = 1.0 - clamp(max(ru, rl) / h0 / cfg.tl_max_residual)
        s_conv = ramp_score(conv, 0.15, 0.6) if name != "Rectangle" else 1.0 - clamp(abs(conv) / 0.35)
        s_inside = 1.0 - clamp(viol / 0.10)
        s_vol = 0.5 if vt is None else clamp(0.5 - vt)
        s_trend = 0.5
        if name in ("Ascending Triangle", "Falling Wedge", "Rectangle", "Symmetrical Triangle"):
            s_trend = ramp_score(trend * final_dir, -0.05, 0.10)
        elif name in ("Descending Triangle", "Rising Wedge"):
            s_trend = ramp_score(trend * final_dir, -0.05, 0.10)
        comps = {"touches": (s_touch, 0.2), "fit": (s_fit, 0.25), "convergence": (s_conv, 0.15),
                 "containment": (s_inside, 0.15), "volume": (s_vol, 0.1), "trend": (s_trend, 0.15)}
        bo_reason = None
        if bo is not None:
            s_bo, bo_reason = self.breakout_volume_reason(vol, bo)
            comps["breakout_volume"] = (s_bo, 0.15)
        score = sum(v * w for v, w in comps.values()) / sum(w for _, w in comps.values())
        if status == "failed":
            score *= 0.6
        elif status == "expired":
            score *= 0.7

        level = upper(end_idx) if final_dir > 0 else lower(end_idx)
        target = level + final_dir * h0
        if name in ("Rising Wedge", "Falling Wedge"):
            target = upper(x0) if final_dir > 0 else lower(x0)   # wedges retrace to their origin
        stop = lower(end_idx) if final_dir > 0 else upper(end_idx)
        dir_word = "bullish" if final_dir > 0 else "bearish"

        def slope_word(s: float) -> str:
            if abs(s) <= cfg.tl_flat_slope:
                return "flat"
            return "rising" if s > 0 else "falling"

        reasons = [
            f"{len(highs)} swing highs touch a {slope_word(su)} upper line and {len(lows)} swing lows touch a "
            f"{slope_word(sl)} lower line (max deviation {max(ru, rl) / h0 * 100:.0f}% of pattern height)",
            f"Upper line moves {su * 100:+.0f}% and lower line {sl * 100:+.0f}% of the initial height over {width} bars",
            (f"Lines converge: height shrinks {conv * 100:.0f}% from {h0:.2f} to {h1:.2f}" if name != "Rectangle"
             else f"Range holds a height of {h0:.2f} ({h0 / price * 100:.1f}% of price)"),
            f"Price stayed inside the boundaries {100 - viol * 100:.0f}% of the time",
        ]
        if apex is not None and name != "Rectangle":
            reasons.append(f"Apex projected at bar {int(apex)} ({int(apex) - x1} bars after the last touch)")
        if vt is not None:
            reasons.append(f"Volume {'contracted' if vt < 0 else 'expanded'} {abs(vt) * 100:.0f}% during the pattern"
                           + (" (classic consolidation)" if vt < 0 else ""))
        if abs(trend) > 0.03:
            reasons.append(f"Prior move into the pattern: {trend * 100:+.1f}%")
        if status == "confirmed":
            reasons.append(f"Confirmed: close {close[bo]:.2f} broke {'above the upper' if direction > 0 else 'below the lower'} "
                           f"line ({(upper if direction > 0 else lower)(bo):.2f}) at bar {bo} - {dir_word} resolution")
            if bo_reason:
                reasons.append(bo_reason)
        elif status == "failed":
            reasons.append(f"Failed: price broke {'up' if direction > 0 else 'down'} against the expected {bias} bias")
        elif status == "forming":
            reasons.append(f"Still inside the pattern: upper line ~{upper(n - 1):.2f}, lower line ~{lower(n - 1):.2f}, "
                           f"last close {close[-1]:.2f}; expected bias {bias}")
        else:
            reasons.append("Expired: reached the apex / went stale without a breakout")
        reasons.append(f"Target {target:.2f} ({(target / close[end_idx] - 1) * 100:+.1f}%)")

        kps = [KeyPoint(p.idx, p.price, "H" if p.kind > 0 else "L") for p in seq]
        xe = max(end_idx, x1 + 5)
        lines = [Line(x0, upper(x0), xe, upper(xe), "Upper line"), Line(x0, lower(x0), xe, lower(xe), "Lower line")]
        return PatternMatch(
            symbol=symbol, pattern=name, direction=dir_word if status == "confirmed" or bias == "neutral" else bias,
            status=status, start_idx=x0, end_idx=end_idx, score=float(score), reasons=reasons,
            key_points=kps, lines=lines,
            metrics={"upper_slope": su, "lower_slope": sl, "convergence": conv, "touches": touches,
                     "max_residual": max(ru, rl) / h0, "violations": viol, "apex": apex, "prior_trend": trend,
                     "volume_trend": vt, "components": {k: v[0] for k, v in comps.items()}},
            breakout_idx=bo, breakout_price=float(close[bo]) if bo is not None else None,
            level=float(level), target=float(target), stop=float(stop), scale=order,
        )
