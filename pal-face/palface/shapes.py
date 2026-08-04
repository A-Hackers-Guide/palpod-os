"""Procedural draw helpers.

Every face pixel is drawn by these functions — no image assets. The functions
work in absolute device pixels; the renderer converts from the 100-unit face
space to pixels before calling them.
"""

from __future__ import annotations

import math
from typing import Sequence, Tuple

import pygame


ColorRGB = Tuple[int, int, int]
ColorRGBA = Tuple[int, int, int, int]


# ---------------------------------------------------------------------------
# Radial gradient background
# ---------------------------------------------------------------------------
def radial_gradient(
    surface: pygame.Surface,
    center: Tuple[int, int],
    radius: int,
    inner_color: ColorRGB,
    outer_color: ColorRGB,
    steps: int = 48,
) -> None:
    """Cheap radial gradient by stacking `steps` filled circles.

    48 steps is imperceptible at 1080p; keeps the render hot loop under 1ms.
    """
    if radius <= 0:
        return
    ir, ig, ib = inner_color
    orr, og, ob = outer_color
    # Draw from outside in so the innermost bright disc lands on top.
    for i in range(steps, 0, -1):
        t = i / steps
        r = int(radius * t)
        color = (
            int(orr + (ir - orr) * (1.0 - t)),
            int(og + (ig - og) * (1.0 - t)),
            int(ob + (ib - ob) * (1.0 - t)),
        )
        pygame.draw.circle(surface, color, center, r)


# ---------------------------------------------------------------------------
# Rounded rect / pill (the eye base shape)
# ---------------------------------------------------------------------------
def rounded_rect_pill(
    surface: pygame.Surface,
    rect: pygame.Rect,
    color: ColorRGB,
    radius: int,
) -> None:
    """Draw a filled rounded rectangle (a "pill" when radius >= w/2).

    Uses pygame.draw.rect's border_radius (SDL2 native, hardware-fast).
    """
    if rect.width <= 0 or rect.height <= 0:
        return
    r = min(radius, rect.width // 2, rect.height // 2)
    pygame.draw.rect(surface, color, rect, border_radius=r)


def draw_eye(
    surface: pygame.Surface,
    center: Tuple[float, float],
    base_w: float,
    base_h: float,
    scale_x: float,
    scale_y: float,
    rotation_deg: float,
    color: ColorRGB,
    glow_color: ColorRGBA,
    glow_radius_px: int = 10,
) -> None:
    """Draw one eye — pill shape, scaled, optionally rotated, with a soft glow.

    Rotation is done by rendering the pill onto a small transparent surface,
    calling pygame.transform.rotate(), then blitting to `surface`.
    """
    w = max(1, int(round(base_w * scale_x)))
    h = max(1, int(round(base_h * scale_y)))
    # Padding around the pill so rotation and glow don't clip.
    pad = max(2, glow_radius_px + 4)
    src = pygame.Surface((w + pad * 2, h + pad * 2), pygame.SRCALPHA)

    # Glow: draw a slightly larger, semi-transparent pill first.
    if glow_color[3] > 0 and glow_radius_px > 0:
        glow_rect = pygame.Rect(
            pad - glow_radius_px // 2,
            pad - glow_radius_px // 2,
            w + glow_radius_px,
            h + glow_radius_px,
        )
        gr = min(glow_rect.width // 2, glow_rect.height // 2)
        pygame.draw.rect(src, glow_color, glow_rect, border_radius=gr)

    # Main pill.
    body_rect = pygame.Rect(pad, pad, w, h)
    br = min(body_rect.width // 2, body_rect.height // 2)
    pygame.draw.rect(src, color, body_rect, border_radius=br)

    if abs(rotation_deg) > 0.05:
        rotated = pygame.transform.rotate(src, rotation_deg)
        rect = rotated.get_rect(center=(int(center[0]), int(center[1])))
        surface.blit(rotated, rect.topleft)
    else:
        rect = src.get_rect(center=(int(center[0]), int(center[1])))
        surface.blit(src, rect.topleft)


# ---------------------------------------------------------------------------
# Cup-scoop smile
# ---------------------------------------------------------------------------
#
# Spec-sheet SVG path (in a 100x100 face-space, y grows downward):
#   M 30 60 L 70 60 C 78 82, 22 82, 30 60 Z
#
# That's:
#   - Start at (30, 60)   — top-left corner of the cup rim.
#   - Line to (70, 60)    — top-right corner of the cup rim.
#   - Cubic Bezier back to (30, 60) with control points (78, 82) and (22, 82).
#
# We flatten the cubic to a polyline and fill with pygame.draw.polygon.
def _bezier_cubic(p0, p1, p2, p3, steps: int = 24):
    pts = []
    for i in range(steps + 1):
        t = i / steps
        mt = 1.0 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def cup_smile_points(
    cx: float,
    cy: float,
    face_px: float,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
) -> list[Tuple[float, float]]:
    """Return the polygon points for the cup-scoop smile centered at (cx, cy).

    face_px = size (in device pixels) that the 100x100 face-space maps to.
    scale_x / scale_y are additional multiplicative scales relative to the base
    cup, pivoting on its own center.
    """
    # Face-space anchors (from the SVG path).
    p_start = (30.0, 60.0)
    p_line_end = (70.0, 60.0)
    ctrl1 = (78.0, 82.0)
    ctrl2 = (22.0, 82.0)
    p_close = p_start

    # Straight top edge: two points.
    # Curved bottom: cubic bezier from p_line_end back to p_start.
    curve = _bezier_cubic(p_line_end, ctrl1, ctrl2, p_close, steps=28)
    raw = [p_start, p_line_end] + curve[1:]  # avoid duplicating p_line_end

    # Transform: center-of-cup in face-space is roughly (50, 71) (midpoint of
    # rim (50, 60) and cup bottom (~50, 82)). Pivot scaling around that point
    # so scale_x doesn't shove the cup off to one side.
    pivot_fx, pivot_fy = 50.0, 71.0
    unit = face_px / 100.0
    out = []
    for fx, fy in raw:
        # Pivot-scale in face-space.
        sx = pivot_fx + (fx - pivot_fx) * scale_x
        sy = pivot_fy + (fy - pivot_fy) * scale_y
        # Convert face-space to device px: (fx - 50, fy - 71) around (cx, cy).
        dx = (sx - pivot_fx) * unit
        dy = (sy - pivot_fy) * unit
        out.append((cx + dx, cy + dy))
    return out


def draw_cup_smile(
    surface: pygame.Surface,
    cx: float,
    cy: float,
    face_px: float,
    scale_x: float,
    scale_y: float,
    color: ColorRGB,
    glow_color: ColorRGBA,
    glow_radius_px: int = 8,
) -> None:
    """Draw the cup-scoop mouth with an optional soft glow."""
    pts = cup_smile_points(cx, cy, face_px, scale_x=scale_x, scale_y=scale_y)
    if len(pts) < 3:
        return

    if glow_color[3] > 0 and glow_radius_px > 0:
        # Compute a slightly-larger scale-out for the glow polygon.
        gscale = 1.0 + glow_radius_px / max(20.0, face_px * 0.4)
        gpts = cup_smile_points(
            cx, cy, face_px, scale_x=scale_x * gscale, scale_y=scale_y * gscale
        )
        # Draw glow onto a per-pixel-alpha surface so alpha compositing works.
        bounds = _polygon_bounds(gpts + pts)
        pad = glow_radius_px + 4
        gw = int(bounds[2] - bounds[0]) + pad * 2
        gh = int(bounds[3] - bounds[1]) + pad * 2
        gsurf = pygame.Surface((gw, gh), pygame.SRCALPHA)
        gox = bounds[0] - pad
        goy = bounds[1] - pad
        glow_pts = [(x - gox, y - goy) for x, y in gpts]
        pygame.draw.polygon(gsurf, glow_color, glow_pts)
        surface.blit(gsurf, (int(gox), int(goy)))

    pygame.draw.polygon(surface, color, [(int(x), int(y)) for x, y in pts])


def draw_oval_mouth(
    surface: pygame.Surface,
    cx: float,
    cy: float,
    face_px: float,
    scale_x: float,
    scale_y: float,
    color: ColorRGB,
    glow_color: ColorRGBA,
    glow_radius_px: int = 8,
) -> None:
    """Draw a filled oval mouth — used for full openness (talking peak / surprised)."""
    unit = face_px / 100.0
    # Base oval is inscribed in the cup's bounding box (roughly 40x22 face-units).
    base_w = 40.0 * unit * scale_x
    base_h = 26.0 * unit * scale_y
    rect = pygame.Rect(0, 0, max(2, int(base_w)), max(2, int(base_h)))
    rect.center = (int(cx), int(cy) + int(4 * unit))

    if glow_color[3] > 0 and glow_radius_px > 0:
        grect = rect.inflate(glow_radius_px, glow_radius_px)
        gsurf = pygame.Surface(grect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(gsurf, glow_color, gsurf.get_rect())
        surface.blit(gsurf, grect.topleft)

    pygame.draw.ellipse(surface, color, rect)


def draw_blended_mouth(
    surface: pygame.Surface,
    cx: float,
    cy: float,
    face_px: float,
    scale_x: float,
    scale_y: float,
    openness: float,
    color: ColorRGB,
    glow_color: ColorRGBA,
    glow_radius_px: int = 8,
) -> None:
    """Draw the mouth as a blend between cup smile (openness=0) and oval (openness=1).

    Implementation: draw both onto their own alpha surfaces, composite with
    alpha weighted by openness. This gives a clean crossfade without any
    per-vertex morphing headache.
    """
    o = max(0.0, min(1.0, openness))
    if o <= 0.001:
        draw_cup_smile(
            surface, cx, cy, face_px, scale_x, scale_y, color, glow_color, glow_radius_px
        )
        return
    if o >= 0.999:
        draw_oval_mouth(
            surface, cx, cy, face_px, scale_x, scale_y, color, glow_color, glow_radius_px
        )
        return

    # Sized to fit either shape.
    unit = face_px / 100.0
    w = int(50.0 * unit * max(scale_x, 1.0)) + glow_radius_px * 2 + 8
    h = int(36.0 * unit * max(scale_y, 1.0)) + glow_radius_px * 2 + 8
    tmp = pygame.Surface((w, h), pygame.SRCALPHA)
    local_cx = w / 2
    local_cy = h / 2

    # Cup layer @ (1-o)
    cup = pygame.Surface((w, h), pygame.SRCALPHA)
    draw_cup_smile(cup, local_cx, local_cy, face_px, scale_x, scale_y,
                   color, glow_color, glow_radius_px)
    cup.set_alpha(int(255 * (1.0 - o)))
    tmp.blit(cup, (0, 0))

    # Oval layer @ o
    oval = pygame.Surface((w, h), pygame.SRCALPHA)
    draw_oval_mouth(oval, local_cx, local_cy, face_px, scale_x, scale_y,
                    color, glow_color, glow_radius_px)
    oval.set_alpha(int(255 * o))
    tmp.blit(oval, (0, 0))

    surface.blit(tmp, (int(cx - local_cx), int(cy - local_cy)))


# ---------------------------------------------------------------------------
# Sphere mask
# ---------------------------------------------------------------------------
def apply_sphere_mask(
    surface: pygame.Surface,
    center: Tuple[int, int],
    radius: int,
    mask_color: ColorRGB = (0, 0, 0),
) -> None:
    """Blacken everything outside a circle of `radius` around `center`.

    For a real round OLED display, pixels outside the physical circle don't
    exist. On a square debug monitor this keeps the illusion of a round face.

    Implementation: build a 4-corner mask that covers the square-minus-circle
    area, blit on top. Cheap and does not require per-pixel alpha ops.
    """
    W, H = surface.get_size()
    # We stamp the mask by drawing a filled rectangle covering the full
    # surface and then punching out a circle. Using a per-pixel-alpha
    # scratch surface keeps this in one blit.
    mask = pygame.Surface((W, H), pygame.SRCALPHA)
    mask.fill((mask_color[0], mask_color[1], mask_color[2], 255))
    # Punch out the visible circle by drawing a transparent circle over it.
    pygame.draw.circle(mask, (0, 0, 0, 0), center, radius)
    surface.blit(mask, (0, 0))


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def _polygon_bounds(pts: Sequence[Tuple[float, float]]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))
