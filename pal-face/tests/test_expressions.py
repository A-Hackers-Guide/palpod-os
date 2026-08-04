"""Verify each of the 9 expressions is defined and returns a well-formed FaceState."""

import pytest

from palface import expressions
from palface.states import FaceState, FaceStateName


ALL_STATES = list(FaceStateName)


@pytest.mark.parametrize("name", ALL_STATES)
def test_expression_defined(name):
    fs = expressions.get(name)
    assert isinstance(fs, FaceState)
    assert fs.name == name


@pytest.mark.parametrize("name", ALL_STATES)
def test_expression_fields_finite(name):
    fs = expressions.get(name)
    for eye in (fs.left_eye, fs.right_eye):
        assert eye.scale_x > 0
        assert eye.scale_y >= 0
    assert 0.0 <= fs.mouth.openness <= 1.0
    assert fs.glow_intensity > 0.0


def test_get_accepts_string():
    fs = expressions.get("happy")
    assert fs.name == FaceStateName.HAPPY
    fs2 = expressions.get("TALKING")
    assert fs2.name == FaceStateName.TALKING


def test_get_rejects_bad_string():
    with pytest.raises(ValueError):
        expressions.get("BOGUS")


def test_wink_asymmetric():
    fs = expressions.get(FaceStateName.WINK)
    assert fs.left_eye.scale_y < 0.2 < fs.right_eye.scale_y


def test_angry_rotates_opposite():
    fs = expressions.get(FaceStateName.ANGRY)
    assert fs.left_eye.rotation_deg == -fs.right_eye.rotation_deg
    assert fs.left_eye.rotation_deg != 0.0


def test_listening_breathes():
    fs = expressions.get(FaceStateName.LISTENING)
    assert fs.breath_amplitude > 0.0
    assert fs.breath_period_s > 0.0
