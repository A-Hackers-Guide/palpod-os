"""Configuration loading via pydantic-settings.

Loads config.yaml (if present) and merges with defaults. CLI flags win over
YAML which wins over the built-in defaults defined here.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class ScreenConfig(BaseModel):
    width: int = 1080
    height: int = 1080
    sphere_radius_frac: float = 0.98
    fullscreen: bool = True
    sdl_driver: Optional[str] = None
    fb_device: Optional[str] = None
    target_fps: int = 60
    vsync: bool = True


class BridgeConfig(BaseModel):
    url: str = "ws://localhost:7777"
    reconnect_initial_seconds: float = 0.5
    reconnect_max_seconds: float = 30.0
    offline: bool = False


class AnimationConfig(BaseModel):
    state_transition_ms: int = 350
    bob_amplitude_px: float = 6.0
    bob_period_seconds: float = 3.4
    blink_interval_min: float = 4.0
    blink_interval_max: float = 6.5
    blink_duration_ms: int = 120
    glance_interval_min: float = 6.0
    glance_interval_max: float = 14.0
    glance_offset_frac: float = 0.06
    glance_duration_ms: int = 800
    idle_expression_interval_min: float = 5.0
    idle_expression_interval_max: float = 12.0
    idle_expression_hold_ms_min: int = 900
    idle_expression_hold_ms_max: int = 1800
    idle_expressions: List[str] = Field(
        default_factory=lambda: [
            "HAPPY",
            "WINK",
            "SURPRISED",
            "SUSPICIOUS",
            "THINKING",
        ]
    )


class DebugConfig(BaseModel):
    show_fps: bool = False
    show_mask: bool = False


class AppConfig(BaseModel):
    screen: ScreenConfig = Field(default_factory=ScreenConfig)
    bridge: BridgeConfig = Field(default_factory=BridgeConfig)
    animation: AnimationConfig = Field(default_factory=AnimationConfig)
    debug: DebugConfig = Field(default_factory=DebugConfig)


def load_config(path: Optional[str] = None) -> AppConfig:
    """Load config from YAML file, or return defaults if path is None/missing."""
    if not path:
        return AppConfig()
    p = Path(path)
    if not p.exists():
        return AppConfig()
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return AppConfig(**data)
