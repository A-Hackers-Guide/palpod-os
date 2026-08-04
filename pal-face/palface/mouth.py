"""Mouth drawing.

Base is the cup-scoop path from the spec sheet (see palface/shapes.py). When
TALKING, `openness` is driven per frame from TTS audio level and the mouth
crossfades toward a filled oval.
"""

from __future__ import annotations

from typing import Tuple

import pygame

from . import colors
from .shapes import draw_blended_mouth
from .states import MouthState


# The mouth is centered around face-space (50, 71) — see shapes.cup_smile_points.
# We expose the anchor as constants so any future spec tweak lands in one place.
BASE_CENTER_FX = 50.0
BASE_CENTER_FY = 71.0


def draw_mouth(
    surface: pygame.Surface,
    mouth: MouthState,
    face_origin_px: Tuple[float, float],
    face_size_px: float,
    breath_multiplier: float = 1.0,
    glow_intensity: float = 1.0,
) -> None:
    unit = face_size_px / 100.0
    ox, oy = face_origin_px

    cx_f = BASE_CENTER_FX + mouth.offset_x_frac * 100.0
    cy_f = BASE_CENTER_FY + mouth.offset_y_frac * 100.0
    cx = ox + cx_f * unit
    cy = oy + cy_f * unit

    sx = mouth.scale_x * breath_multiplier
    sy = mouth.scale_y * breath_multiplier

    glow_alpha = int(max(0, min(255, colors.FEATURE_GLOW[3] * glow_intensity)))
    glow = (
        colors.FEATURE_GLOW[0],
        colors.FEATURE_GLOW[1],
        colors.FEATURE_GLOW[2],
        glow_alpha,
    )
    glow_radius = max(4, int(face_size_px * 0.018))

    draw_blended_mouth(
        surface=surface,
        cx=cx,
        cy=cy,
        face_px=face_size_px,
        scale_x=sx,
        scale_y=sy,
        openness=mouth.openness,
        color=colors.FEATURE_WHITE,
        glow_color=glow,
        glow_radius_px=glow_radius,
    )
