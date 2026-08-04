"""`python -m palface` entry point.

Boots the renderer, optionally connects to pal-voice via WebSocket, and runs
the main loop until Esc/Q or a QUIT event.

Runs happily with pal-voice absent — the bridge just keeps trying to reconnect
in the background while the face displays its idle behavior.
"""

from __future__ import annotations

import argparse
import logging
import sys

from .bridge import Bridge
from .config import load_config
from .renderer import Renderer


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="palface", description="PAL Face Renderer")
    p.add_argument("-c", "--config", default=None, help="Path to config.yaml")
    p.add_argument("--offline", action="store_true",
                   help="Do not attempt to connect to pal-voice.")
    p.add_argument("--windowed", action="store_true",
                   help="Force windowed mode (overrides config.fullscreen).")
    p.add_argument("--width", type=int, default=None)
    p.add_argument("--height", type=int, default=None)
    p.add_argument("--fps", type=int, default=None)
    p.add_argument("--url", default=None, help="Override pal-voice WebSocket URL")
    p.add_argument("--show-fps", action="store_true", help="Draw FPS overlay")
    p.add_argument("--show-mask", action="store_true",
                   help="Draw the sphere-mask outline in magenta")
    p.add_argument("-v", "--verbose", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_arg_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )

    cfg = load_config(args.config)

    # CLI overrides.
    if args.windowed:
        cfg.screen.fullscreen = False
    if args.width:
        cfg.screen.width = args.width
    if args.height:
        cfg.screen.height = args.height
    if args.fps:
        cfg.screen.target_fps = args.fps
    if args.url:
        cfg.bridge.url = args.url
    if args.offline:
        cfg.bridge.offline = True
    if args.show_fps:
        cfg.debug.show_fps = True
    if args.show_mask:
        cfg.debug.show_mask = True

    bridge: Bridge | None = None
    if not cfg.bridge.offline:
        bridge = Bridge(
            cfg.bridge.url,
            reconnect_initial_seconds=cfg.bridge.reconnect_initial_seconds,
            reconnect_max_seconds=cfg.bridge.reconnect_max_seconds,
        )
        bridge.start()

    try:
        r = Renderer(cfg, bridge=bridge)
        r.run()
    finally:
        if bridge is not None:
            bridge.stop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
