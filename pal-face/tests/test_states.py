"""Tests for the FaceState dataclass and enum plumbing."""

from palface.states import EyeState, FaceState, FaceStateName, MouthState


def test_default_face_state_is_neutral():
    fs = FaceState()
    assert fs.name == FaceStateName.NEUTRAL
    assert fs.left_eye.scale_x == 1.0
    assert fs.mouth.openness == 0.0


def test_copy_is_deep_enough_for_mutation():
    fs = FaceState()
    dup = fs.copy()
    dup.left_eye.scale_x = 0.25
    dup.mouth.openness = 0.9
    assert fs.left_eye.scale_x == 1.0
    assert fs.mouth.openness == 0.0
    assert dup.left_eye.scale_x == 0.25
    assert dup.mouth.openness == 0.9


def test_face_state_name_from_string_upper():
    assert FaceStateName("HAPPY") == FaceStateName.HAPPY
    assert FaceStateName("TALKING").value == "TALKING"


def test_all_nine_states_present():
    expected = {
        "NEUTRAL", "HAPPY", "WINK", "SURPRISED", "ANGRY",
        "SUSPICIOUS", "LISTENING", "THINKING", "TALKING",
    }
    got = {s.value for s in FaceStateName}
    assert got == expected


def test_eye_and_mouth_state_defaults():
    e = EyeState()
    assert e.scale_x == 1.0 and e.scale_y == 1.0
    assert e.rotation_deg == 0.0
    m = MouthState()
    assert m.scale_x == 1.0 and m.scale_y == 1.0
    assert m.openness == 0.0
