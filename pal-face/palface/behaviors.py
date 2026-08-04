"""Idle behaviors: blinks, glances, micro-expressions.

Behaviors return *modifiers* that layer on top of the base FaceState — they
never overwrite the current expression. This keeps the state machine simple
(only the "big" states like TALKING / LISTENING change the base) while the
face still feels alive when it's just sitting there.
"""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import List, Optional

from .config import AnimationConfig
from .expressions import get as get_expression
from .states import FaceState, FaceStateName


@dataclass
class BlinkModifier:
    """Multiplicative scale_y modifier for both eyes during a blink."""
    scale_y: float = 1.0


@dataclass
class GlanceModifier:
    """Additive offset_x_frac for both eyes (they look together)."""
    offset_x_frac: float = 0.0


class BlinkController:
    """Schedules random blinks and returns the current eyelid scale multiplier."""

    def __init__(self, cfg: AnimationConfig):
        self.cfg = cfg
        self._next_blink_at = self._schedule_next(time.monotonic())
        self._blink_started_at: Optional[float] = None

    def _schedule_next(self, now: float) -> float:
        return now + random.uniform(
            self.cfg.blink_interval_min, self.cfg.blink_interval_max
        )

    def force_blink(self) -> None:
        """External trigger — e.g. debug key or scripted moment."""
        self._blink_started_at = time.monotonic()

    def update(self) -> BlinkModifier:
        now = time.monotonic()
        if self._blink_started_at is None and now >= self._next_blink_at:
            self._blink_started_at = now
            self._next_blink_at = self._schedule_next(now)

        if self._blink_started_at is None:
            return BlinkModifier(scale_y=1.0)

        elapsed_ms = (now - self._blink_started_at) * 1000.0
        dur = self.cfg.blink_duration_ms
        if elapsed_ms >= dur:
            self._blink_started_at = None
            return BlinkModifier(scale_y=1.0)

        # Two-phase: 0->0.5 close (1 -> 0.06), 0.5->1 open (0.06 -> 1).
        t = elapsed_ms / dur
        if t < 0.5:
            k = t / 0.5
            scale_y = 1.0 + (0.06 - 1.0) * k
        else:
            k = (t - 0.5) / 0.5
            scale_y = 0.06 + (1.0 - 0.06) * k
        return BlinkModifier(scale_y=scale_y)


class GlanceController:
    """Occasionally slides the eyes ±X to imply the head glancing."""

    def __init__(self, cfg: AnimationConfig):
        self.cfg = cfg
        self._next_glance_at = self._schedule_next(time.monotonic())
        self._glance_started_at: Optional[float] = None
        self._glance_direction: float = 1.0

    def _schedule_next(self, now: float) -> float:
        return now + random.uniform(
            self.cfg.glance_interval_min, self.cfg.glance_interval_max
        )

    def update(self) -> GlanceModifier:
        now = time.monotonic()
        if self._glance_started_at is None and now >= self._next_glance_at:
            self._glance_started_at = now
            self._next_glance_at = self._schedule_next(now)
            self._glance_direction = random.choice((-1.0, 1.0))

        if self._glance_started_at is None:
            return GlanceModifier(offset_x_frac=0.0)

        elapsed_ms = (now - self._glance_started_at) * 1000.0
        dur = self.cfg.glance_duration_ms
        if elapsed_ms >= dur:
            self._glance_started_at = None
            return GlanceModifier(offset_x_frac=0.0)

        # Ease in/out: go out to peak by mid, back to 0 by end.
        t = elapsed_ms / dur
        # sine wave, one full arc.
        import math
        env = math.sin(t * math.pi)
        return GlanceModifier(
            offset_x_frac=self._glance_direction * self.cfg.glance_offset_frac * env
        )


class IdleExpressionController:
    """When base state is NEUTRAL, occasionally *ghost-target* a micro expression
    (HAPPY, WINK, etc.) for a short duration.

    Returns the FaceState the renderer should aim at, or None to keep NEUTRAL.
    """

    def __init__(self, cfg: AnimationConfig):
        self.cfg = cfg
        self._next_burst_at = self._schedule_next(time.monotonic())
        self._burst_expiry: Optional[float] = None
        self._current: Optional[FaceState] = None
        self._pool: List[FaceStateName] = [FaceStateName(s) for s in cfg.idle_expressions]

    def _schedule_next(self, now: float) -> float:
        return now + random.uniform(
            self.cfg.idle_expression_interval_min,
            self.cfg.idle_expression_interval_max,
        )

    def update(self, base_state_name: FaceStateName) -> Optional[FaceState]:
        # Only fire while truly idle (base = NEUTRAL).
        if base_state_name != FaceStateName.NEUTRAL:
            self._current = None
            self._burst_expiry = None
            return None

        now = time.monotonic()
        if self._burst_expiry is not None and now >= self._burst_expiry:
            self._current = None
            self._burst_expiry = None
            self._next_burst_at = self._schedule_next(now)

        if self._current is None and now >= self._next_burst_at:
            pick = random.choice(self._pool) if self._pool else None
            if pick is None:
                self._next_burst_at = self._schedule_next(now)
                return None
            self._current = get_expression(pick)
            hold_ms = random.uniform(
                self.cfg.idle_expression_hold_ms_min,
                self.cfg.idle_expression_hold_ms_max,
            )
            self._burst_expiry = now + hold_ms / 1000.0

        return self._current


def apply_modifiers(
    state: FaceState,
    blink: BlinkModifier,
    glance: GlanceModifier,
) -> FaceState:
    """Layer blink + glance on top of the given FaceState (returns a copy)."""
    out = state.copy()
    out.left_eye.scale_y *= blink.scale_y
    out.right_eye.scale_y *= blink.scale_y
    out.left_eye.offset_x_frac += glance.offset_x_frac
    out.right_eye.offset_x_frac += glance.offset_x_frac
    return out
