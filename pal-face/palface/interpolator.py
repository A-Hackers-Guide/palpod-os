"""Smooth interpolation between FaceStates.

Uses easeInOutCubic. If a new target arrives mid-transition, the Interpolator
snapshots the current interpolated value as the new "from" state and starts a
fresh transition to the new "to" state — preventing visual snaps.
"""

from __future__ import annotations

import time
from dataclasses import replace

from .states import EyeState, FaceState, MouthState


def ease_in_out_cubic(t: float) -> float:
    """Standard easeInOutCubic on [0,1]."""
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0
    if t < 0.5:
        return 4.0 * t * t * t
    p = 2.0 * t - 2.0
    return 0.5 * p * p * p + 1.0


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _lerp_eye(a: EyeState, b: EyeState, t: float) -> EyeState:
    return EyeState(
        scale_x=_lerp(a.scale_x, b.scale_x, t),
        scale_y=_lerp(a.scale_y, b.scale_y, t),
        rotation_deg=_lerp(a.rotation_deg, b.rotation_deg, t),
        offset_x_frac=_lerp(a.offset_x_frac, b.offset_x_frac, t),
        offset_y_frac=_lerp(a.offset_y_frac, b.offset_y_frac, t),
    )


def _lerp_mouth(a: MouthState, b: MouthState, t: float) -> MouthState:
    return MouthState(
        scale_x=_lerp(a.scale_x, b.scale_x, t),
        scale_y=_lerp(a.scale_y, b.scale_y, t),
        openness=_lerp(a.openness, b.openness, t),
        offset_x_frac=_lerp(a.offset_x_frac, b.offset_x_frac, t),
        offset_y_frac=_lerp(a.offset_y_frac, b.offset_y_frac, t),
    )


def lerp_state(a: FaceState, b: FaceState, t: float) -> FaceState:
    """Linearly interpolate all numeric fields of two FaceStates.

    Name of the output = name of b (the target), so downstream code that keys
    on state name (e.g. TALKING driver) reads the destination even mid-morph.
    """
    return FaceState(
        name=b.name,
        left_eye=_lerp_eye(a.left_eye, b.left_eye, t),
        right_eye=_lerp_eye(a.right_eye, b.right_eye, t),
        mouth=_lerp_mouth(a.mouth, b.mouth, t),
        glow_intensity=_lerp(a.glow_intensity, b.glow_intensity, t),
        breath_amplitude=_lerp(a.breath_amplitude, b.breath_amplitude, t),
        breath_period_s=_lerp(a.breath_period_s, b.breath_period_s, t),
    )


class Interpolator:
    """Tracks a from-state, to-state, and progress. Retargets on new goals."""

    def __init__(self, initial: FaceState, duration_ms: int = 350):
        self.duration_ms = max(1, int(duration_ms))
        self._from = initial.copy()
        self._to = initial.copy()
        self._start = time.monotonic()
        self._done = True

    @property
    def current(self) -> FaceState:
        """The current interpolated state (based on wall clock)."""
        if self._done:
            return self._to.copy()
        elapsed_ms = (time.monotonic() - self._start) * 1000.0
        t_raw = elapsed_ms / self.duration_ms
        if t_raw >= 1.0:
            self._done = True
            return self._to.copy()
        return lerp_state(self._from, self._to, ease_in_out_cubic(t_raw))

    @property
    def done(self) -> bool:
        # Force a re-check so `done` reflects reality even if `current` was not
        # asked for since the deadline passed.
        _ = self.current
        return self._done

    @property
    def target(self) -> FaceState:
        return self._to

    def set_target(self, target: FaceState, duration_ms: int | None = None) -> None:
        """Start a new transition. Snapshots current position as the new "from"."""
        if duration_ms is not None:
            self.duration_ms = max(1, int(duration_ms))
        self._from = self.current  # snapshot mid-morph if necessary
        self._to = target.copy()
        self._start = time.monotonic()
        self._done = False
