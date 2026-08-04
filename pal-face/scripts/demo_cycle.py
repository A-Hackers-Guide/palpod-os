"""Demo cycler — runs the renderer and steps through every expression.

Used by standalone-demo.sh (and by anyone who just wants to eyeball the face).
No pal-voice required.
"""

from __future__ import annotations

import argparse
import itertools
import time

from palface.config import load_config
from palface.renderer import Renderer
from palface.states import FaceStateName


CYCLE = [
    FaceStateName.NEUTRAL,
    FaceStateName.HAPPY,
    FaceStateName.WINK,
    FaceStateName.SURPRISED,
    FaceStateName.ANGRY,
    FaceStateName.SUSPICIOUS,
    FaceStateName.LISTENING,
    FaceStateName.THINKING,
    FaceStateName.TALKING,
]


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Cycle through all 9 PAL expressions.")
    p.add_argument("-c", "--config", default=None)
    p.add_argument("--hold", type=float, default=3.0, help="Seconds per expression.")
    p.add_argument("--windowed", action="store_true")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--show-fps", action="store_true")
    p.add_argument("--show-mask", action="store_true")
    return p.parse_args()


def main() -> int:
    args = _parse_args()
    cfg = load_config(args.config)
    if args.windowed:
        cfg.screen.fullscreen = False
    if args.width:
        cfg.screen.width = args.width
    if args.height:
        cfg.screen.height = args.height
    if args.show_fps:
        cfg.debug.show_fps = True
    if args.show_mask:
        cfg.debug.show_mask = True
    cfg.bridge.offline = True  # explicit

    r = Renderer(cfg, bridge=None)

    # Fake TTS audio driver for the TALKING pose so the mouth actually opens.
    import math
    tts_phase = 0.0

    cycle = itertools.cycle(CYCLE)
    current = next(cycle)
    r.set_state(current)
    next_switch = time.monotonic() + args.hold

    import pygame
    running = True
    while running:
        # Event pump — copy of Renderer's, so Esc still quits.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN and e.key in (pygame.K_ESCAPE, pygame.K_q):
                running = False

        now = time.monotonic()
        if now >= next_switch:
            current = next(cycle)
            r.set_state(current)
            next_switch = now + args.hold

        # Fake TALKING audio: sinusoid at 5Hz.
        if current == FaceStateName.TALKING:
            tts_phase += 1.0 / cfg.screen.target_fps
            r._talking_openness = 0.5 + 0.5 * abs(math.sin(tts_phase * math.tau * 2.5))

        r.render_frame()
        r.clock.tick(cfg.screen.target_fps)

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
