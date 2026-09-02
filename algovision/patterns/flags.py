"""Bull / Bear flags: a sharp pole followed by a short counter-trend channel."""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd

from scipy.signal import argrelextrema

from algovision.core.geometry import clamp, fit_line, ramp_score, volume_trend
from algovision.core.pivots import atr
from algovision.core.types import KeyPoint, Line, PatternMatch, Pivot
from algovision.patterns.base import Detector


class FlagDetector(Detector):
    names = ("Bull Flag", "Bear Flag")
    single_scale = True        # flags are short: evaluated once, with fine local extrema

    def detect(self, symbol: str, df: pd.DataFrame, pivots: List[Pivot], order: int) -> List[PatternMatch]:
        out: List[PatternMatch] = []
        for bull in (True, False):
            out.extend(self._detect(symbol, df, pivots, order, bull))
        return out

    def _detect(self, symbol, df, pivots, order, bull: bool) -> List[PatternMatch]:
        cfg = self.cfg
        close, high, low, vol = self.arrays(df)
        a = atr(df)
        n = len(close)
        sgn = 1 if bull else -1
        out: List[PatternMatch] = []
        # pole tops (bull) / pole bottoms (bear): fine-grained local extrema
        if bull:
            ends = argrelextrema(high, np.greater_equal, order=2)[0]
        else:
            ends = argrelextrema(low, np.less_equal, order=2)[0]
        seen = set()
        for t in ends:
            t = int(t)
            # pole start: extreme within the previous pole_max_bars
            s0 = max(0, t - cfg.flag_pole_max_bars)
            if bull:
                s = s0 + int(np.argmin(low[s0:t + 1]))
                pole = high[t] - low[s]
            else:
                s = s0 + int(np.argmax(high[s0:t + 1]))
                pole = high[s] - low[t]
            if t - s < 3 or pole <= 0:
                continue
            base = low[s] if bull else high[s]
            pole_pct = pole / base
            if pole_pct < cfg.flag_pole_min_pct or pole < cfg.flag_pole_min_atr * a[t]:
                continue
            # consolidation window
            best: Optional[PatternMatch] = None
            for k in range(cfg.flag_min_bars, cfg.flag_max_bars + 1):
                e = t + k
                if e >= n:
                    break
                xs = np.arange(t + 1, e + 1)
                wh, wl = high[t + 1:e + 1], low[t + 1:e + 1]
                su, iu, ru = fit_line(xs, wh)
                sl, il, rl = fit_line(xs, wl)
                upper = lambda x, _i=iu, _s=su: _i + _s * x   # noqa: E731
                lower = lambda x, _i=il, _s=sl: _i + _s * x   # noqa: E731
                ch_h = float(np.mean(upper(xs) - lower(xs)))
                if ch_h <= 0:
                    continue
                retrace = ((high[t] - wl.min()) / pole) if bull else ((wh.max() - low[t]) / pole)
                if retrace > cfg.flag_max_retrace:
                    break                                   # deeper pullback -> not a flag
                # channel should drift against (or flat to) the pole and lines should be roughly parallel
                drift = (su + sl) / 2 * k / pole             # total drift as a fraction of the pole
                if drift * sgn > 0.05:
                    continue
                parallel = abs(su - sl) * k / ch_h
                if parallel > 0.8:
                    continue
                if ch_h / pole > 0.6:
                    continue
                # breakout: first close beyond the upper (bull) / lower (bear) line, after the window
                nxt = e + 1
                bo = None
                if nxt < n:
                    lvl = upper(nxt) if bull else lower(nxt)
                    margin = max(cfg.breakout_confirm_pct * lvl, 0.2 * ch_h)   # must clear the tight channel
                    if (bull and close[nxt] > lvl + margin) or (not bull and close[nxt] < lvl - margin):
                        bo = nxt
                if bo is None and nxt < n:
                    continue                                 # still inside the flag: try a longer window
                status = "confirmed" if bo is not None else "forming"
                end_idx = bo if bo is not None else n - 1
                key = (s, t)
                if key in seen and status == "forming":
                    break
                vt = volume_trend(vol, t + 1, e)
                s_pole = ramp_score(pole_pct, cfg.flag_pole_min_pct, cfg.flag_pole_min_pct * 2.5)
                s_retr = 1.0 - clamp((retrace - 0.15) / (cfg.flag_max_retrace - 0.15))
                s_par = 1.0 - clamp(parallel / 1.2)
                s_tight = 1.0 - clamp((ch_h / pole - 0.1) / 0.5)
                s_vol = 0.5 if vt is None else clamp(0.5 - vt)
                comps = {"pole": (s_pole, 0.3), "retrace": (s_retr, 0.2), "parallel": (s_par, 0.15),
                         "tightness": (s_tight, 0.15), "volume": (s_vol, 0.1)}
                bo_reason = None
                if bo is not None:
                    s_bo, bo_reason = self.breakout_volume_reason(vol, bo)
                    comps["breakout_volume"] = (s_bo, 0.15)
                score = sum(v * w for v, w in comps.values()) / sum(w for _, w in comps.values())
                level = upper(end_idx) if bull else lower(end_idx)
                target = level + sgn * pole
                stop = float(wl.min()) if bull else float(wh.max())
                name = "Bull Flag" if bull else "Bear Flag"
                reasons = [
                    f"Pole: price {'rose' if bull else 'fell'} {pole_pct * 100:.1f}% in {t - s} bars "
                    f"({pole / a[t]:.1f}x ATR) from {base:.2f} to {high[t] if bull else low[t]:.2f}",
                    f"Flag: {k}-bar channel drifting {abs(drift) * 100:.0f}% of the pole {'against' if drift * sgn < 0 else 'along'} the trend, "
                    f"retracing only {retrace * 100:.0f}% of the pole (max {cfg.flag_max_retrace * 100:.0f}%)",
                    f"Channel boundaries are near-parallel (divergence {parallel * 100:.0f}% of channel height); "
                    f"channel height is {ch_h / pole * 100:.0f}% of the pole",
                ]
                if vt is not None:
                    reasons.append(f"Volume {'dried up' if vt < 0 else 'rose'} {abs(vt) * 100:.0f}% inside the flag"
                                   + (" (classic)" if vt < 0 else ""))
                if status == "confirmed":
                    reasons.append(f"Confirmed: close {close[bo]:.2f} broke {'above' if bull else 'below'} the flag at bar {bo}")
                    if bo_reason:
                        reasons.append(bo_reason)
                else:
                    reasons.append(f"Forming: flag boundary at ~{level:.2f}, last close {close[-1]:.2f}")
                reasons.append(f"Measured move: pole length {pole:.2f} projected from the breakout -> target {target:.2f} "
                               f"({(target / close[end_idx] - 1) * 100:+.1f}%)")
                xe = max(end_idx, e)
                m = PatternMatch(
                    symbol=symbol, pattern=name, direction="bullish" if bull else "bearish", status=status,
                    start_idx=s, end_idx=end_idx, score=float(score), reasons=reasons,
                    key_points=[KeyPoint(s, float(base), "Pole start"), KeyPoint(t, float(high[t] if bull else low[t]), "Pole end")],
                    lines=[Line(t + 1, upper(t + 1), xe, upper(xe), "Flag upper"), Line(t + 1, lower(t + 1), xe, lower(xe), "Flag lower"),
                           Line(s, float(base), t, float(high[t] if bull else low[t]), "Pole", "dotted")],
                    metrics={"pole_pct": pole_pct, "pole_bars": t - s, "flag_bars": k, "retrace": retrace,
                             "drift": drift, "parallel": parallel, "volume_trend": vt,
                             "components": {kk: v[0] for kk, v in comps.items()}},
                    breakout_idx=bo, breakout_price=float(close[bo]) if bo is not None else None,
                    level=float(level), target=float(target), stop=stop, scale=order,
                )
                seen.add(key)
                best = m
                break
            if best is not None:
                out.append(best)
        return out
