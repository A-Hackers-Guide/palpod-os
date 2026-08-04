"""Tests for interpolator math and retargeting behavior."""

import math
import time

import pytest

from palface.expressions import get
from palface.interpolator import Interpolator, ease_in_out_cubic, lerp_state
from palface.states import FaceStateName


def test_ease_edges_and_midpoint():
    assert ease_in_out_cubic(0.0) == 0.0
    assert ease_in_out_cubic(1.0) == 1.0
    assert 0.49 < ease_in_out_cubic(0.5) < 0.51


def test_ease_monotonic():
    prev = -1.0
    for i in range(101):
        v = ease_in_out_cubic(i / 100)
        assert v >= prev
        prev = v


def test_lerp_state_at_endpoints():
    a = get(FaceStateName.NEUTRAL)
    b = get(FaceStateName.HAPPY)
    at0 = lerp_state(a, b, 0.0)
    at1 = lerp_state(a, b, 1.0)
    # name follows target
    assert at0.name == b.name
    assert at1.name == b.name
    assert at0.left_eye.scale_y == pytest.approx(a.left_eye.scale_y)
    assert at1.left_eye.scale_y == pytest.approx(b.left_eye.scale_y)
    assert at1.mouth.scale_x == pytest.approx(b.mouth.scale_x)


def test_lerp_state_at_midpoint():
    a = get(FaceStateName.NEUTRAL)
    b = get(FaceStateName.HAPPY)
    mid = lerp_state(a, b, 0.5)
    assert mid.left_eye.scale_y == pytest.approx(
        (a.left_eye.scale_y + b.left_eye.scale_y) / 2
    )


def test_interpolator_reports_done_after_duration():
    a = get(FaceStateName.NEUTRAL)
    b = get(FaceStateName.HAPPY)
    interp = Interpolator(a, duration_ms=20)
    interp.set_target(b, duration_ms=20)
    assert not interp.done
    time.sleep(0.05)
    assert interp.done
    cur = interp.current
    assert cur.mouth.scale_x == pytest.approx(b.mouth.scale_x)


def test_interpolator_retarget_mid_flight_no_snap():
    a = get(FaceStateName.NEUTRAL)
    b = get(FaceStateName.HAPPY)
    c = get(FaceStateName.SURPRISED)
    interp = Interpolator(a, duration_ms=200)
    interp.set_target(b, duration_ms=200)
    time.sleep(0.06)  # ~30% of the way toward HAPPY
    mid_pos = interp.current
    interp.set_target(c, duration_ms=200)
    right_after = interp.current
    # The new "from" is the snapshot — meaning immediately after retarget the
    # interpolated value should be within a small epsilon of the mid position.
    assert right_after.left_eye.scale_y == pytest.approx(
        mid_pos.left_eye.scale_y, abs=0.05
    )
    # Fully advancing lands on C.
    time.sleep(0.3)
    fin = interp.current
    assert fin.mouth.scale_x == pytest.approx(c.mouth.scale_x)
    assert fin.name == FaceStateName.SURPRISED
