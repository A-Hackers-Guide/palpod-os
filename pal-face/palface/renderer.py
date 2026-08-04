"""Main render loop.

Design goals:
  * Rock-solid 60 fps (target frame time < 16.6ms on Jetson Orin).
  * Every visual layered in one hot loop with as few allocations as possible.
  * Pure procedural — no image files.

Frame layout:
  1. Clear + radial gradient background.
  2. Apply floating "bob" translation to the face origin.
  3. Compute effective FaceState = interpolator.current  (+ idle burst target)
                                   + blink & glance modifiers.
  4. Draw eyes.
  5. Draw mouth.
  6. Apply the sphere mask (blackens outside the round display).
  7. flip().
"""

from __future__ import annotations

import logging
import math
import os
import sys
import time
from typing import Optional

import pygame

from . import behaviors, colors, expressions
from .bridge import Bridge, BridgeEvent
from .config import AppConfig
from .eyes import draw_eyes
from .interpolator import Interpolator
from .mouth import draw_mouth
from .shapes import apply_sphere_mask, radial_gradient
from .states import FaceState, FaceStateName


log = logging.getLogger(__name__)


def _setup_sdl_env(cfg: AppConfig) -> None:
    """Set SDL_VIDEODRIVER and friends before pygame.display.init()."""
    if cfg.screen.sdl_driver:
        os.environ["SDL_VIDEODRIVER"] = cfg.screen.sdl_driver
    if cfg.screen.fb_device:
        os.environ.setdefault("SDL_FBDEV", cfg.screen.fb_device)
    # Sensible defaults for kiosk on Jetson.
    os.environ.setdefault("SDL_MOUSE_RELATIVE", "0")


class Renderer:
    def __init__(self, cfg: AppConfig, bridge: Optional[Bridge] = None):
        self.cfg = cfg
        self.bridge = bridge

        _setup_sdl_env(cfg)
        pygame.init()
        pygame.mouse.set_visible(False)

        flags = pygame.SCALED
        if cfg.screen.fullscreen:
            flags |= pygame.FULLSCREEN
        vsync = 1 if cfg.screen.vsync else 0
        self.screen = pygame.display.set_mode(
            (cfg.screen.width, cfg.screen.height), flags, vsync=vsync
        )
        pygame.display.set_caption("PAL Face")

        # Sphere geometry.
        self.center = (cfg.screen.width // 2, cfg.screen.height // 2)
        self.sphere_radius = int(
            min(cfg.screen.width, cfg.screen.height) / 2 * cfg.screen.sphere_radius_frac
        )
        # Face "canvas" is a square inscribed in the sphere.
        # face_size is the side of the 100-unit square in device px.
        self.face_size_px = self.sphere_radius * 2 * 0.72  # leaves margin from rim

        # State machine.
        initial = expressions.get(FaceStateName.NEUTRAL)
        self.interp = Interpolator(initial, duration_ms=cfg.animation.state_transition_ms)
        self._base_state_name: FaceStateName = FaceStateName.NEUTRAL

        # Idle behaviors.
        self.blink_ctrl = behaviors.BlinkController(cfg.animation)
        self.glance_ctrl = behaviors.GlanceController(cfg.animation)
        self.idle_ctrl = behaviors.IdleExpressionController(cfg.animation)

        # TTS state — talking openness driven live by tts_frame events.
        self._talking_openness = 0.0
        self._tts_active = False

        # Font for debug HUD.
        self._debug_font = pygame.font.Font(None, 24) if cfg.debug.show_fps else None

        self.clock = pygame.time.Clock()
        self._start_time = time.monotonic()
        self._running = False

        # Precompute per-frame background surface — a static bg surface we can
        # blit each frame instead of redrawing 48 concentric circles.
        self._bg_cache = self._build_bg_cache()

    # -----------------------------------------------------------------------
    def _build_bg_cache(self) -> pygame.Surface:
        surf = pygame.Surface(self.screen.get_size())
        surf.fill(colors.MASK_OUTSIDE)
        radial_gradient(
            surf,
            self.center,
            self.sphere_radius,
            colors.BG_CENTER,
            colors.BG_EDGE,
            steps=64,
        )
        return surf

    # -----------------------------------------------------------------------
    def set_state(self, name: FaceStateName | str) -> None:
        """Public entry point — pal-voice bridge and keyboard scripts call this."""
        if isinstance(name, str):
            try:
                name = FaceStateName(name.upper())
            except ValueError:
                log.warning("unknown face state %r", name)
                return
        self._base_state_name = name
        target = expressions.get(name)
        self.interp.set_target(target, duration_ms=self.cfg.animation.state_transition_ms)

    # -----------------------------------------------------------------------
    def _handle_bridge_events(self, events: list[BridgeEvent]) -> None:
        for ev in events:
            if ev.kind == "face_state":
                self.set_state(ev.payload["state"])
            elif ev.kind == "tts_start":
                self._tts_active = True
                self.set_state(FaceStateName.TALKING)
            elif ev.kind == "tts_end":
                self._tts_active = False
                self._talking_openness = 0.0
                # Return to NEUTRAL after a TTS burst unless a state message
                # says otherwise on the next tick.
                self.set_state(FaceStateName.NEUTRAL)
            elif ev.kind == "tts_frame":
                # Smooth per-frame audio level -> openness (map with slight ceiling).
                lvl = max(0.0, min(1.0, ev.payload.get("audio_level", 0.0)))
                # Ease: 0 -> 0.0 openness, 0.6+ -> 1.0. Feels punchier than linear.
                self._talking_openness = min(1.0, lvl / 0.6)

    # -----------------------------------------------------------------------
    def _compute_effective_state(self) -> FaceState:
        # 1. Base = interpolator's current position.
        state = self.interp.current

        # 2. Idle micro-expressions retarget the interpolator itself while
        #    base is NEUTRAL. When the burst clears, we retarget back.
        idle_target = self.idle_ctrl.update(self._base_state_name)
        if self._base_state_name == FaceStateName.NEUTRAL:
            if idle_target is not None:
                if self.interp.target.name != idle_target.name:
                    self.interp.set_target(
                        idle_target,
                        duration_ms=self.cfg.animation.state_transition_ms,
                    )
                    state = self.interp.current
            else:
                # No active burst. If interp target is not NEUTRAL, drift back.
                if self.interp.target.name != FaceStateName.NEUTRAL:
                    self.interp.set_target(
                        expressions.get(FaceStateName.NEUTRAL),
                        duration_ms=self.cfg.animation.state_transition_ms,
                    )
                    state = self.interp.current

        # 3. TALKING mouth openness override — driven live from TTS audio.
        if state.name == FaceStateName.TALKING:
            state.mouth.openness = self._talking_openness

        # 4. Breathing modulation (LISTENING).
        if state.breath_amplitude > 0.001:
            phase = (time.monotonic() - self._start_time) / max(
                0.05, state.breath_period_s
            )
            breath = 1.0 + state.breath_amplitude * math.sin(phase * math.tau)
        else:
            breath = 1.0

        # 5. Blink & glance modifiers (idle behaviors).
        # Blinks skip during TALKING peaks so the mouth isn't fighting a squint,
        # but only if TTS is actively producing audio.
        blink = self.blink_ctrl.update()
        glance = self.glance_ctrl.update()
        state = behaviors.apply_modifiers(state, blink, glance)

        # Store breath multiplier on the state via a sentinel attribute? Cleaner
        # to just return it separately — but the renderer wants both. Attach:
        state._breath_multiplier = breath  # type: ignore[attr-defined]
        return state

    # -----------------------------------------------------------------------
    def _face_origin_with_bob(self) -> tuple[float, float]:
        """Top-left of the 100x100 face-space, in device pixels, including the bob offset."""
        t = time.monotonic() - self._start_time
        bob = self.cfg.animation.bob_amplitude_px * math.sin(
            (t / max(0.05, self.cfg.animation.bob_period_seconds)) * math.tau
        )
        ox = self.center[0] - self.face_size_px / 2.0
        oy = self.center[1] - self.face_size_px / 2.0 + bob
        return (ox, oy)

    # -----------------------------------------------------------------------
    def render_frame(self, effective: Optional[FaceState] = None) -> None:
        """Draw one full frame to the display."""
        if effective is None:
            effective = self._compute_effective_state()
        breath = getattr(effective, "_breath_multiplier", 1.0)

        # Background.
        self.screen.blit(self._bg_cache, (0, 0))

        # Face.
        origin = self._face_origin_with_bob()
        draw_eyes(
            self.screen,
            effective.left_eye,
            effective.right_eye,
            face_origin_px=origin,
            face_size_px=self.face_size_px,
            breath_multiplier=breath,
            glow_intensity=effective.glow_intensity,
        )
        draw_mouth(
            self.screen,
            effective.mouth,
            face_origin_px=origin,
            face_size_px=self.face_size_px,
            breath_multiplier=breath,
            glow_intensity=effective.glow_intensity,
        )

        # Sphere mask.
        apply_sphere_mask(self.screen, self.center, self.sphere_radius,
                          colors.MASK_OUTSIDE)

        # Debug overlays.
        if self.cfg.debug.show_mask:
            pygame.draw.circle(self.screen, colors.DEBUG_MAGENTA,
                               self.center, self.sphere_radius, 2)
        if self._debug_font is not None:
            fps = self.clock.get_fps()
            hud = self._debug_font.render(
                f"FPS {fps:5.1f}  state={effective.name.value}  "
                f"conn={'y' if (self.bridge and self.bridge.connected) else 'n'}",
                True,
                colors.DEBUG_TEXT,
            )
            self.screen.blit(hud, (16, 16))

        pygame.display.flip()

    # -----------------------------------------------------------------------
    def _pump_events(self) -> None:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self._running = False
            elif e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE, pygame.K_q):
                    self._running = False
                # Number keys map to the 9 states (see scripts/keyboard-control.py
                # for a friendlier legend). Handy in every mode.
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
                    self.set_state(_KEYS[e.key])
                if e.key == pygame.K_b:
                    self.blink_ctrl.force_blink()

    # -----------------------------------------------------------------------
    def run(self) -> None:
        self._running = True
        target_fps = self.cfg.screen.target_fps
        try:
            while self._running:
                self._pump_events()
                if self.bridge is not None:
                    self._handle_bridge_events(self.bridge.drain())
                self.render_frame()
                self.clock.tick(target_fps)
        finally:
            pygame.quit()

    # Alias for scripts that just want a quick "run for N seconds" harness.
    def run_for(self, seconds: float) -> None:
        self._running = True
        deadline = time.monotonic() + seconds
        target_fps = self.cfg.screen.target_fps
        try:
            while self._running and time.monotonic() < deadline:
                self._pump_events()
                if self.bridge is not None:
                    self._handle_bridge_events(self.bridge.drain())
                self.render_frame()
                self.clock.tick(target_fps)
        finally:
            pygame.quit()


def main_render_loop(cfg: AppConfig, bridge: Optional[Bridge] = None) -> None:
    r = Renderer(cfg, bridge=bridge)
    r.run()
