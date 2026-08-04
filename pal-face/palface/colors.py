"""Palette constants for the PAL face.

The PAL screen is a rich cyan-blue OLED glow with clean white shapes.
Everything downstream should use these constants — never magic RGB tuples.
"""

from __future__ import annotations

# --- Background (radial gradient inner -> outer) ----------------------------
# Bright cyan core fading to a deeper marine blue at the sphere edge.
BG_CENTER = (32, 200, 240)      # inner glow
BG_MID = (18, 130, 210)         # midpoint (unused if 2-stop gradient)
BG_EDGE = (6, 44, 110)          # outer edge, near-black-blue

# --- Face features ----------------------------------------------------------
FEATURE_WHITE = (245, 250, 255)
FEATURE_HIGHLIGHT = (255, 255, 255)

# Soft cyan glow behind features (drop-shadow bloom).
FEATURE_GLOW = (140, 230, 255, 90)      # RGBA — alpha matters

# Outside the sphere mask: pure black so the round display's off pixels stay off.
MASK_OUTSIDE = (0, 0, 0)

# Debug overlays.
DEBUG_MAGENTA = (255, 0, 200)
DEBUG_TEXT = (255, 255, 255)
