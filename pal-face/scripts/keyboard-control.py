"""Run the face with keyboard control.

Hotkeys:
    1 NEUTRAL   2 HAPPY   3 WINK
    4 SURPRISED 5 ANGRY   6 SUSPICIOUS
    7 LISTENING 8 THINKING 9 TALKING
    b force blink
    +/- adjust simulated TTS audio level (while TALKING)
    ESC / q  quit
"""

from __future__ import annotations

import argparse
import pygame

from palface.config import load_config
from palface.renderer import Renderer
from palface.states import FaceStateName


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--config", default=None)
    ap.add_argument("--windowed", action="store_true")
    ap.add_argument("--width", type=int, default=None)
    ap.add_argument("--height", type=int, default=None)
    ap.add_argument("--show-fps", action="store_true")
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.windowed:
        cfg.screen.fullscreen = False
    if args.width:
        cfg.screen.width = args.width
    if args.height:
        cfg.screen.height = args.height
    if args.show_fps:
        cfg.debug.show_fps = True
    cfg.bridge.offline = True

    r = Renderer(cfg, bridge=None)
    print(__doc__ or "")

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif e.key == pygame.K_PLUS or e.key == pygame.K_EQUALS:
                    r._talking_openness = min(1.0, r._talking_openness + 0.1)
                    print("openness:", round(r._talking_openness, 2))
                elif e.key == pygame.K_MINUS:
                    r._talking_openness = max(0.0, r._talking_openness - 0.1)
                    print("openness:", round(r._talking_openness, 2))
                else:
                    _KEYS = {
                        pygame.K_1: FaceStateName.NEUTRAL,
                        pygame.K_2: FaceStateName.HAPPY,
                        pygame.K_3: FaceStateName.WINK,
                        pygame.K_4: FaceStateName.SURPRISED,
                        pygame.K_5: FaceStateName.ANGRY,
                        pygame.K_6: FaceStateName.SUSPICIOUS,
                        pygame.K_7: FaceStateName.LISTENING,
                        pygame.K_8: FaceStateName.THINKING,
                        pygame.K_9: FaceStateName.TALKING,
                    }
                    if e.key in _KEYS:
                        r.set_state(_KEYS[e.key])
                        print("state:", _KEYS[e.key].value)
                    elif e.key == pygame.K_b:
                        r.blink_ctrl.force_blink()

        r.render_frame()
        r.clock.tick(cfg.screen.target_fps)

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
