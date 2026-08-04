"""The 9 canonical PAL expressions.

Each function returns a fresh FaceState. Callers may then mutate the returned
object (e.g. the TALKING renderer overrides `mouth.openness` per frame).
"""

from __future__ import annotations

from typing import Callable, Dict

from .states import EyeState, FaceState, FaceStateName, MouthState


def neutral() -> FaceState:
    return FaceState(name=FaceStateName.NEUTRAL)


def happy() -> FaceState:
    # Squinty eyes + bigger cup smile.
    return FaceState(
        name=FaceStateName.HAPPY,
        left_eye=EyeState(scale_y=0.5),
        right_eye=EyeState(scale_y=0.5),
        mouth=MouthState(scale_x=1.18, scale_y=1.45),
        glow_intensity=1.15,
    )


def wink() -> FaceState:
    return FaceState(
        name=FaceStateName.WINK,
        left_eye=EyeState(scale_y=0.08),
        right_eye=EyeState(),
        mouth=MouthState(scale_x=1.05, scale_y=1.15),
    )


def surprised() -> FaceState:
    return FaceState(
        name=FaceStateName.SURPRISED,
        left_eye=EyeState(scale_x=1.18, scale_y=1.08),
        right_eye=EyeState(scale_x=1.18, scale_y=1.08),
        mouth=MouthState(scale_x=0.45, scale_y=0.75, openness=0.8),
        glow_intensity=1.2,
    )


def angry() -> FaceState:
    return FaceState(
        name=FaceStateName.ANGRY,
        left_eye=EyeState(rotation_deg=22.0),
        right_eye=EyeState(rotation_deg=-22.0),
        mouth=MouthState(scale_y=0.28),
        glow_intensity=0.9,
    )


def suspicious() -> FaceState:
    return FaceState(
        name=FaceStateName.SUSPICIOUS,
        left_eye=EyeState(scale_y=0.35),
        right_eye=EyeState(scale_y=0.35),
        mouth=MouthState(scale_y=0.4, offset_x_frac=0.15),
    )


def listening() -> FaceState:
    return FaceState(
        name=FaceStateName.LISTENING,
        left_eye=EyeState(scale_x=1.1, scale_y=1.1),
        right_eye=EyeState(scale_x=1.1, scale_y=1.1),
        mouth=MouthState(),
        glow_intensity=1.25,
        breath_amplitude=0.05,   # 0.95 <-> 1.05
        breath_period_s=1.2,
    )


def thinking() -> FaceState:
    return FaceState(
        name=FaceStateName.THINKING,
        left_eye=EyeState(scale_y=0.75, offset_y_frac=-0.03),
        right_eye=EyeState(scale_y=0.75, offset_y_frac=-0.03),
        mouth=MouthState(scale_y=0.7),
    )


def talking() -> FaceState:
    # Mouth openness is driven per frame from TTS audio_level.
    # Eyes stay neutral (blink behaviors still run on top).
    return FaceState(
        name=FaceStateName.TALKING,
        left_eye=EyeState(),
        right_eye=EyeState(),
        mouth=MouthState(openness=0.0),
        glow_intensity=1.1,
    )


EXPRESSIONS: Dict[FaceStateName, Callable[[], FaceState]] = {
    FaceStateName.NEUTRAL: neutral,
    FaceStateName.HAPPY: happy,
    FaceStateName.WINK: wink,
    FaceStateName.SURPRISED: surprised,
    FaceStateName.ANGRY: angry,
    FaceStateName.SUSPICIOUS: suspicious,
    FaceStateName.LISTENING: listening,
    FaceStateName.THINKING: thinking,
    FaceStateName.TALKING: talking,
}


def get(state: FaceStateName | str) -> FaceState:
    """Build a fresh FaceState for the named expression."""
    if isinstance(state, str):
        state = FaceStateName(state.upper())
    return EXPRESSIONS[state]()
