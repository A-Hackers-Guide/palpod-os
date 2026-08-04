"""Eye layout and drawing.

Base eye rects in the 100x100 face-space (from the spec):

    left:  x=24 y=22 w=14 h=36 rx=7
    right: x=62 y=22 w=14 h=36 rx=7

Both are drawn by the same pill primitive. Per-eye scale/rotation/offset come
from the interpolated FaceState.
"""

from __future__ import annotations

from typing import Tuple

import pygame

from . import colors
from .shapes import draw_eye
from .states import EyeState


# Base geometry in face-space (100x100 units).
BASE_LEFT = (24.0, 22.0, 14.0, 36.0)   # x, y, w, h
BASE_RIGHT = (62.0, 22.0, 14.0, 36.0)


def _draw_one(
    surface: pygame.Surface,
    base_xywh: Tuple[float, float, float, float],
    eye: EyeState,
    face_origin_px: Tuple[float, float],
    face_size_px: float,
    breath_multiplier: float,
    glow_intensity: float,
) -> None:
    x, y, w, h = base_xywh
    unit = face_size_px / 100.0
    # Center of the base pill in face-space.
    cx_f = x + w / 2.0
    cy_f = y + h / 2.0
    # Apply eye offset (fraction of face size = fraction of 100 units).
    cx_f += eye.offset_x_frac * 100.0
    cy_f += eye.offset_y_frac * 100.0

    # Face-space -> device px.
    ox, oy = face_origin_px
    cx = ox + cx_f * unit
    cy = oy + cy_f * unit
    base_w_px = w * unit
    base_h_px = h * unit

    # Breath modulation: uniform scale on top of state scale.
    sx = eye.scale_x * breath_multiplier
    sy = eye.scale_y * breath_multiplier

    glow_alpha = int(max(0, min(255, colors.FEATURE_GLOW[3] * glow_intensity)))
    glow = (
        colors.FEATURE_GLOW[0],
        colors.FEATURE_GLOW[1],
        colors.FEATURE_GLOW[2],
        glow_alpha,
    )
    glow_radius = max(3, int(face_size_px * 0.015))

    draw_eye(
        surface=surface,
        center=(cx, cy),
        base_w=base_w_px,
        base_h=base_h_px,
        scale_x=sx,
        scale_y=sy,
        rotation_deg=eye.rotation_deg,
        color=colors.FEATURE_WHITE,
        glow_color=glow,
        glow_radius_px=glow_radius,
    )


def draw_eyes(
    surface: pygame.Surface,
    left: EyeState,
    right: EyeState,
    face_origin_px: Tuple[float, float],
    face_size_px: float,
    breath_multiplier: float = 1.0,
    glow_intensity: float = 1.0,
) -> None:
    _draw_one(surface, BASE_LEFT, left, face_origin_px, face_size_px,
              breath_multiplier, glow_intensity)
    _draw_one(surface, BASE_RIGHT, right, face_origin_px, face_size_px,
              breath_multiplier, glow_intensity)
