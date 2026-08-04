"""FaceState dataclass + enum of the 9 canonical PAL expressions.

A FaceState is a *purely numeric* description of what a face frame looks like.
It has no dependency on Pygame — the interpolator can lerp between two states,
and the renderer turns the final numeric state into pixels.

Coordinate system for the face is normalized to a 100x100 unit square, matching
the spec-sheet SVG path. `renderer.py` scales this to the actual display size.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum


class FaceStateName(str, Enum):
    NEUTRAL = "NEUTRAL"
    HAPPY = "HAPPY"
    WINK = "WINK"
    SURPRISED = "SURPRISED"
    ANGRY = "ANGRY"
    SUSPICIOUS = "SUSPICIOUS"
    LISTENING = "LISTENING"
    THINKING = "THINKING"
    TALKING = "TALKING"


@dataclass
class EyeState:
    # Multiplicative scales on the base eye pill.
    scale_x: float = 1.0
    scale_y: float = 1.0
    # Rotation in degrees, applied to each eye individually.
    rotation_deg: float = 0.0
    # Translation offset expressed as fraction of face size (100 units).
    offset_x_frac: float = 0.0
    offset_y_frac: float = 0.0


@dataclass
class MouthState:
    # Base shape is the cup-scoop. scale_y > 1 = bigger cup, < 1 = flatter.
    scale_x: float = 1.0
    scale_y: float = 1.0
    # 0.0 = cup smile, 1.0 = round "O" (talking / surprised).
    openness: float = 0.0
    # Offset in fraction of face size.
    offset_x_frac: float = 0.0
    offset_y_frac: float = 0.0


@dataclass
class FaceState:
    name: FaceStateName = FaceStateName.NEUTRAL
    left_eye: EyeState = field(default_factory=EyeState)
    right_eye: EyeState = field(default_factory=EyeState)
    mouth: MouthState = field(default_factory=MouthState)
    # Overall glow multiplier for the drop-shadow bloom.
    glow_intensity: float = 1.0
    # A rhythmic breathing multiplier — the renderer can modulate size by this.
    # Used by LISTENING to gently pulse. 1.0 = static.
    breath_amplitude: float = 0.0
    breath_period_s: float = 1.2

    def copy(self) -> "FaceState":
        return replace(
            self,
            left_eye=replace(self.left_eye),
            right_eye=replace(self.right_eye),
            mouth=replace(self.mouth),
        )
