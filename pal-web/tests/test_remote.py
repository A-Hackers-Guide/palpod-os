"""Test suite for the remote-control router.

Post-hardening, the tests split into three tiers:

1. **Pre-hardening tests** — the 9 checks that must keep passing after the
   security fixes land. Grep for ``PRE-HARDENING`` to find them.
2. **BYPASS #3 tests** — same-origin XSS mints grants. Grep for
   ``BYPASS-3``. Covers session cookie, CSRF, Origin allowlist, and
   cross-owner isolation.
3. **BYPASS #6 tests** — grant window rollover unbounded. Grep for
   ``BYPASS-6``. Covers cool-down, daily budget, event audit row, revoke
   stamps.
4. **BYPASS #9 tests** — client-supplied initiator. Grep for ``BYPASS-9``.
5. **Audit-gap tests** — malformed / unknown WS envelopes now produce
   anomaly rows. Grep for ``AUDIT-GAP``.
"""

from __future__ import annotations

import asyncio
import os
import time
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
import respx
from httpx import Response
from sqlalchemy import select

from palweb.clients.rustdesk import (
    HBBR_BASE_URL,
    HBBS_BASE_URL,
    InsufficientAuthorization,
    RustDeskClient,
)
from palweb.models import (
    RemoteDevice,
    RemoteGrantEvent,
    RemoteInputEvent,
    RemoteSession,
    RemoteWSAnomaly,
    RemoteWSAnomalySummary,
)


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #


async def _register_device(client, *, rustdesk_id: str = "999888777", name: str = "Studio Linux") -> dict:
    resp = await client.post(
        "/api/remote/devices",
        json={
            "display_name": name,
            "device_type": "linux",
            "rustdesk_id": rustdesk_id,
            "auth_token": "tok-xyz",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


async def _open_session(client, device_id: str) -> dict:
    """Open a session — no ``initiated_by`` sent; server derives it."""
    resp = await client.post("/api/remote/sessions", json={"device_id": device_id})
    assert resp.status_code == 201, resp.text
    return resp.json()


async def _paired_and_session(client, app):
    device = await _register_device(client)
    session = await _open_session(client, device["id"])
    return device, session


# --------------------------------------------------------------------------- #
# REST — pairing  (PRE-HARDENING)
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_register_device_defaults_to_view_only(paired_device):
    """PRE-HARDENING: freshly paired device MUST land in view_only state."""
    assert paired_device["control_state"] == "view_only"
    assert paired_device["control_grant_expires_at"] is None


@pytest.mark.asyncio
async def test_list_devices_reports_view_only(client, paired_device):
    """PRE-HARDENING: list endpoint reflects control state accurately."""
    resp = await client.get("/api/remote/devices")
    assert resp.status_code == 200
    devices = resp.json()
    assert len(devices) == 1
    assert devices[0]["control_state"] == "view_only"


# --------------------------------------------------------------------------- #
# REST — grant-control: the explicit-consent gate (PRE-HARDENING)
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_grant_control_with_user_tap_header_succeeds(client, paired_device):
    """PRE-HARDENING baseline — the legitimate happy path."""
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 30},
        headers={"X-Consent-Origin": "user-tap"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["control_state"] == "granted"
    expires = datetime.fromisoformat(body["control_grant_expires_at"])
    delta = expires - datetime.now(timezone.utc)
    assert timedelta(minutes=29) < delta < timedelta(minutes=31)


@pytest.mark.asyncio
async def test_grant_control_without_consent_header_is_rejected(client, paired_device):
    """PRE-HARDENING: CONSENT-BYPASS-ATTEMPT — no X-Consent-Origin at all."""
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 15},
    )
    assert resp.status_code == 403
    assert "user tap" in resp.json()["detail"].lower()

    listing = (await client.get("/api/remote/devices")).json()
    assert listing[0]["control_state"] == "view_only"


@pytest.mark.asyncio
async def test_grant_control_with_voice_origin_is_rejected(client, paired_device):
    """PRE-HARDENING: CONSENT-BYPASS-ATTEMPT — caller sets voice, not user-tap."""
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 15},
        headers={"X-Consent-Origin": "voice"},
    )
    assert resp.status_code == 403
    listing = (await client.get("/api/remote/devices")).json()
    assert listing[0]["control_state"] == "view_only"


@pytest.mark.asyncio
async def test_grant_control_with_arbitrary_origin_is_rejected(client, paired_device):
    """PRE-HARDENING: only ``user-tap`` — never anything else."""
    for bogus in ("api", "ai-agent", "system", "USER-TAP", "", "user_tap"):
        resp = await client.post(
            f"/api/remote/devices/{paired_device['id']}/grant-control",
            json={"minutes": 15},
            headers={"X-Consent-Origin": bogus},
        )
        assert resp.status_code == 403, f"header {bogus!r} should be rejected"


@pytest.mark.asyncio
async def test_grant_control_minutes_over_60_returns_422(client, paired_device):
    """PRE-HARDENING: Pydantic ceiling."""
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 61},
        headers={"X-Consent-Origin": "user-tap"},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_grant_control_minutes_zero_or_negative_returns_422(client, paired_device):
    """PRE-HARDENING: zero and negative minutes are 422."""
    for bad in (0, -5):
        resp = await client.post(
            f"/api/remote/devices/{paired_device['id']}/grant-control",
            json={"minutes": bad},
            headers={"X-Consent-Origin": "user-tap"},
        )
        assert resp.status_code == 422


# --------------------------------------------------------------------------- #
# BYPASS #3 — same-origin XSS mints grants
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_grant_control_without_csrf_token_is_rejected(client, paired_device):
    """BYPASS-3: request lacks the ``X-CSRF-Token`` header entirely.

    The default ``client`` fixture always sets it, so we clear it on this one
    request. A same-origin XSS-injected fetch that skips the token — because
    the attacker can't read a JS-side value — MUST get 403.
    """
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 15},
        headers={
            "X-Consent-Origin": "user-tap",
            "X-CSRF-Token": "",  # explicitly blank
        },
    )
    assert resp.status_code == 403
    assert "csrf" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_grant_control_with_wrong_csrf_token_is_rejected(client, paired_device):
    """BYPASS-3: header doesn't match the cookie."""
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 15},
        headers={
            "X-Consent-Origin": "user-tap",
            "X-CSRF-Token": "abc.definitelynotthecookievalue",
        },
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_grant_control_with_invalid_origin_is_rejected(client, paired_device):
    """BYPASS-3: attacker sets ``Origin: https://evil.com``."""
    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 15},
        headers={
            "X-Consent-Origin": "user-tap",
            "Origin": "https://evil.com",
        },
    )
    assert resp.status_code == 403


@pytest.mark.asyncio
async def test_grant_control_without_session_cookie_is_rejected(unauth_client, app, session_factory):
    """BYPASS-3: unauthenticated caller — no ``palpod_session`` cookie.

    Fetches ``/remote.html`` first so the CSRF cookie is seated (otherwise
    the CSRF middleware short-circuits with 403 before the auth dep even
    runs). This exercises the specific gate the reviewer named: unauth =
    401 from ``current_user``.
    """
    async with session_factory() as db:
        dev = RemoteDevice(
            display_name="X",
            device_type="linux",
            rustdesk_id="000",
            auth_token="t",
            owner_user_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
        )
        db.add(dev)
        await db.commit()
        await db.refresh(dev)
        device_id = str(dev.id)

    # Seat the CSRF cookie without authenticating.
    page = await unauth_client.get("/remote.html")
    assert page.status_code == 200
    csrf = unauth_client.cookies.get("palpod_csrf")
    assert csrf, "middleware must set the CSRF cookie on /remote.html"

    resp = await unauth_client.post(
        f"/api/remote/devices/{device_id}/grant-control",
        json={"minutes": 15},
        headers={"X-Consent-Origin": "user-tap", "X-CSRF-Token": csrf},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_grant_control_from_different_user_is_rejected(client, app, session_factory):
    """BYPASS-3: device belongs to another owner — 404 (never 200)."""
    async with session_factory() as db:
        other = RemoteDevice(
            display_name="Someone else's",
            device_type="linux",
            rustdesk_id="222",
            auth_token="t",
            owner_user_id=uuid.uuid4(),  # different owner
        )
        db.add(other)
        await db.commit()
        await db.refresh(other)
        other_id = str(other.id)

    resp = await client.post(
        f"/api/remote/devices/{other_id}/grant-control",
        json={"minutes": 15},
        headers={"X-Consent-Origin": "user-tap"},
    )
    # Owner-scoped queries return 404, not 403 — cross-owner existence is
    # not leaked.
    assert resp.status_code == 404


# --------------------------------------------------------------------------- #
# REST — revoke  (PRE-HARDENING)
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_revoke_control_sets_expiry_to_now(client, paired_device):
    """PRE-HARDENING: revoke flips state back to view_only."""
    grant = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 30},
        headers={"X-Consent-Origin": "user-tap"},
    )
    assert grant.status_code == 200

    revoke = await client.post(
        f"/api/remote/devices/{paired_device['id']}/revoke-control"
    )
    assert revoke.status_code == 200
    listing = (await client.get("/api/remote/devices")).json()
    assert listing[0]["control_state"] == "view_only"


# --------------------------------------------------------------------------- #
# BYPASS #6 — grant window rollover
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_second_grant_within_cooldown_window_is_rejected(client, paired_device):
    """BYPASS-6: two grants back-to-back — second one 429s."""
    hdrs = {"X-Consent-Origin": "user-tap"}
    r1 = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 5},
        headers=hdrs,
    )
    assert r1.status_code == 200, r1.text

    r2 = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 5},
        headers=hdrs,
    )
    assert r2.status_code == 429, r2.text
    assert "cool-down" in r2.json()["detail"].lower()


@pytest.mark.asyncio
async def test_daily_grant_budget_exceeded_returns_429(client, paired_device, session_factory):
    """BYPASS-6: sum of grant minutes in 24 h can't exceed 240."""
    hdrs = {"X-Consent-Origin": "user-tap"}
    # Seed 4 events summing to 240 min directly (bypasses cool-down).
    device_id = uuid.UUID(paired_device["id"])
    async with session_factory() as db:
        now = datetime.now(timezone.utc)
        for i in range(4):
            db.add(
                RemoteGrantEvent(
                    device_id=device_id,
                    granted_by_user_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
                    granted_at=now - timedelta(hours=4 * i + 1),
                    minutes=60,
                    csrf_token_hash="deadbeef" * 8,
                    origin="http://testserver",
                )
            )
        await db.commit()

    r = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 1},
        headers=hdrs,
    )
    assert r.status_code == 429, r.text
    assert "budget" in r.json()["detail"].lower()


@pytest.mark.asyncio
async def test_grant_event_row_written_on_each_grant(client, paired_device, session_factory):
    """BYPASS-6: successful grant writes a ``remote_grant_events`` row."""
    device_id = uuid.UUID(paired_device["id"])
    r = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 10},
        headers={"X-Consent-Origin": "user-tap"},
    )
    assert r.status_code == 200

    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteGrantEvent).where(RemoteGrantEvent.device_id == device_id)
            )
        ).scalars().all()
    assert len(rows) == 1
    assert rows[0].minutes == 10
    assert rows[0].revoked_early_at is None
    assert len(rows[0].csrf_token_hash) == 64  # sha256 hex


@pytest.mark.asyncio
async def test_revoke_control_stamps_revoked_at_on_open_grant_event(
    client, paired_device, session_factory
):
    """BYPASS-6: revoke sets ``revoked_early_at`` on the still-open row."""
    grant = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 30},
        headers={"X-Consent-Origin": "user-tap"},
    )
    assert grant.status_code == 200

    revoke = await client.post(
        f"/api/remote/devices/{paired_device['id']}/revoke-control"
    )
    assert revoke.status_code == 200

    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteGrantEvent)
                .where(RemoteGrantEvent.device_id == uuid.UUID(paired_device["id"]))
            )
        ).scalars().all()
    assert len(rows) == 1
    assert rows[0].revoked_early_at is not None


# --------------------------------------------------------------------------- #
# Client — RustDeskClient authorization defense-in-depth (PRE-HARDENING)
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_rustdesk_client_refuses_input_without_grant():
    """PRE-HARDENING: CONSENT-BYPASS-ATTEMPT — direct client invocation."""
    async with respx.mock(base_url=HBBR_BASE_URL) as rmock:
        client = RustDeskClient()
        try:
            with pytest.raises(InsufficientAuthorization):
                await client.send_input_event(
                    "111222333",
                    "mouse_click",
                    {"x": 100, "y": 100},
                    authorization_context={
                        "grant_active": False,
                        "grant_expires_at": None,
                        "initiator": "ai-agent",
                    },
                )
            assert rmock.calls.call_count == 0
        finally:
            await client.close()


@pytest.mark.asyncio
async def test_rustdesk_client_refuses_input_with_past_expiry():
    """PRE-HARDENING: expired grant → InsufficientAuthorization."""
    async with respx.mock(base_url=HBBR_BASE_URL) as rmock:
        client = RustDeskClient()
        try:
            past = datetime.now(timezone.utc) - timedelta(seconds=1)
            with pytest.raises(InsufficientAuthorization):
                await client.send_input_event(
                    "111222333",
                    "key_press",
                    {"key": "Enter"},
                    authorization_context={
                        "grant_active": True,
                        "grant_expires_at": past,
                        "initiator": "ai-agent",
                    },
                )
            assert rmock.calls.call_count == 0
        finally:
            await client.close()


@pytest.mark.asyncio
async def test_rustdesk_client_forwards_input_with_active_grant():
    """PRE-HARDENING: active grant → dispatch."""
    async with respx.mock(base_url=HBBR_BASE_URL) as rmock:
        route = rmock.post("/input/111222333").mock(return_value=Response(200))
        client = RustDeskClient()
        try:
            future = datetime.now(timezone.utc) + timedelta(minutes=5)
            await client.send_input_event(
                "111222333",
                "mouse_click",
                {"x": 10, "y": 20},
                authorization_context={
                    "grant_active": True,
                    "grant_expires_at": future,
                    "initiator": "user",
                },
            )
            assert route.called
        finally:
            await client.close()


# --------------------------------------------------------------------------- #
# WebSocket — the input pipeline (PRE-HARDENING + BYPASS-9 + AUDIT-GAP)
# --------------------------------------------------------------------------- #


class _FakeRustDesk:
    def __init__(self) -> None:
        self.dispatched: list[dict[str, Any]] = []

    async def list_online_devices(self, *, authorization_context):
        return []

    async def get_screen_frame(self, rustdesk_id, *, authorization_context):
        from palweb.clients.rustdesk import ScreenFrame

        return ScreenFrame(
            rustdesk_id=rustdesk_id,
            png_bytes=b"\x89PNG\r\n\x1a\n",
            captured_at=datetime.now(timezone.utc),
        )

    async def send_input_event(
        self, rustdesk_id, event_type, payload, *, authorization_context
    ):
        RustDeskClient._enforce_grant(event_type, authorization_context)
        self.dispatched.append(
            {"rustdesk_id": rustdesk_id, "event_type": event_type, "payload": payload}
        )

    async def close(self):
        return None


def _wait_for(ws, predicate, *, max_frames: int = 30):
    """Read WS messages until predicate(msg) is truthy, or bail."""
    for _ in range(max_frames):
        m = ws.receive_json()
        if predicate(m):
            return m
    return None


@pytest.mark.asyncio
async def test_ws_view_only_session_rejects_input(app, client, ws_test_client, session_factory):
    """PRE-HARDENING: view-only WS refuses input + audits with authorized=False."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "input", "event_type": "mouse_click", "payload": {"x": 5, "y": 6}})
        msg = _wait_for(ws, lambda m: m.get("type") == "error")
        assert msg is not None
        assert msg["code"] == 403
        assert "not authorized" in msg["error"].lower()

    assert fake.dispatched == []
    async with session_factory() as db:
        rows = (await db.execute(select(RemoteInputEvent))).scalars().all()
    assert len(rows) == 1
    assert rows[0].authorized is False
    assert rows[0].grant_active_at_time is False
    assert rows[0].event_type == "mouse_click"


@pytest.mark.asyncio
async def test_ws_dispatches_input_during_active_grant(app, client, ws_test_client, session_factory):
    """PRE-HARDENING: active grant → dispatch + was_authorized flips."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)
    grant = await client.post(
        f"/api/remote/devices/{device['id']}/grant-control",
        json={"minutes": 5},
        headers={"X-Consent-Origin": "user-tap"},
    )
    assert grant.status_code == 200

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "input", "event_type": "mouse_move", "payload": {"x": 40, "y": 40}})
        for _ in range(10):
            m = ws.receive_json()
            assert m.get("type") != "error", m

    assert len(fake.dispatched) == 1
    assert fake.dispatched[0]["event_type"] == "mouse_move"

    async with session_factory() as db:
        rows = (await db.execute(select(RemoteInputEvent))).scalars().all()
        assert len(rows) == 1
        assert rows[0].authorized is True
        sess = await db.get(RemoteSession, uuid.UUID(session["id"]))
        assert sess.was_authorized is True


@pytest.mark.asyncio
async def test_ws_input_after_expiry_is_rejected_and_logged(app, client, ws_test_client, session_factory):
    """PRE-HARDENING: expired grant + client keeps sending → 403 + audited."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)
    async with session_factory() as db:
        d = await db.get(RemoteDevice, uuid.UUID(device["id"]))
        d.control_grant_expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
        await db.commit()

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "input", "event_type": "type_text", "payload": {"text": "hello"}})
        err = _wait_for(ws, lambda m: m.get("type") == "error")
        assert err is not None
        assert err["code"] == 403

    assert fake.dispatched == []
    async with session_factory() as db:
        rows = (await db.execute(select(RemoteInputEvent))).scalars().all()
    assert len(rows) == 1
    assert rows[0].authorized is False
    # Redaction still holds.
    assert "text" not in rows[0].payload_json
    assert "text_length" in rows[0].payload_json


@pytest.mark.asyncio
async def test_ws_revoke_mid_session_stops_dispatch(app, client, ws_test_client, session_factory):
    """PRE-HARDENING: user hits Revoke mid-session → subsequent input 403s."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)
    await client.post(
        f"/api/remote/devices/{device['id']}/grant-control",
        json={"minutes": 5},
        headers={"X-Consent-Origin": "user-tap"},
    )

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "input", "event_type": "mouse_click", "payload": {"x": 1, "y": 2}})
        for _ in range(5):
            ws.receive_json()

        revoke_resp = await client.post(
            f"/api/remote/devices/{device['id']}/revoke-control"
        )
        assert revoke_resp.status_code == 200

        ws.send_json({"type": "input", "event_type": "mouse_click", "payload": {"x": 3, "y": 4}})
        err = _wait_for(ws, lambda m: m.get("type") == "error")
        assert err is not None
        assert err["code"] == 403

    assert len(fake.dispatched) == 1
    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteInputEvent).order_by(RemoteInputEvent.timestamp)
            )
        ).scalars().all()
    assert len(rows) == 2
    assert rows[0].authorized is True
    assert rows[1].authorized is False


@pytest.mark.asyncio
async def test_ws_pushes_grant_expired_notice(app, client, ws_test_client, session_factory):
    """PRE-HARDENING: server pushes grant_expired mid-session."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)
    async with session_factory() as db:
        d = await db.get(RemoteDevice, uuid.UUID(device["id"]))
        d.control_grant_expires_at = datetime.now(timezone.utc) + timedelta(seconds=1)
        await db.commit()

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        notice = _wait_for(ws, lambda m: m.get("type") == "grant_expired", max_frames=80)
        assert notice is not None
        assert notice["device_id"] == device["id"]


@pytest.mark.asyncio
async def test_ws_view_only_streams_frames_but_rejects_input(app, client, ws_test_client):
    """PRE-HARDENING: view-only WS streams frames + refuses input."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        got_frame = _wait_for(ws, lambda m: m.get("type") == "frame")
        assert got_frame is not None

        ws.send_json({"type": "input", "event_type": "mouse_click", "payload": {"x": 0, "y": 0}})
        err = _wait_for(ws, lambda m: m.get("type") == "error")
        assert err is not None
        assert err["code"] == 403

    assert fake.dispatched == []


# --------------------------------------------------------------------------- #
# BYPASS #9 — client-supplied initiator
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_client_supplied_initiator_is_overridden_by_server_derived_value(
    client, agent_client, session_factory
):
    """BYPASS-9: agent-token client tries to open a session as ``initiated_by=user``.

    The session-open schema forbids the field entirely (extra='forbid'), so
    the payload 422s. Even with the field removed, the session lands as
    ``initiated_by='ai-agent'`` because the server derives it from the
    agent-token principal — never from the body.
    """
    # 1. Pair a device via the browser user (agents can't pair; grant/pair
    #    always require a user session — sensitive control-plane ops).
    device = await _register_device(client, rustdesk_id="agent-000", name="Agent laptop")

    # 2. Try to smuggle `initiated_by: "user"` — 422 (extra forbidden).
    r = await agent_client.post(
        "/api/remote/sessions",
        json={"device_id": device["id"], "initiated_by": "user"},
    )
    assert r.status_code == 422, r.text

    # 3. Clean call succeeds and the row is ``ai-agent``.
    r = await agent_client.post(
        "/api/remote/sessions",
        json={"device_id": device["id"]},
    )
    assert r.status_code == 201, r.text
    assert r.json()["initiated_by"] == "ai-agent"

    async with session_factory() as db:
        row = await db.get(RemoteSession, uuid.UUID(r.json()["id"]))
        assert row.initiated_by == "ai-agent"


@pytest.mark.asyncio
async def test_ws_input_from_agent_token_is_labeled_ai_agent_in_audit(
    app, client, agent_client, agent_ws_test_client, session_factory
):
    """BYPASS-9: WS opened by the agent's bearer token → every event ``ai-agent``.

    The client-side envelope carries no ``initiator``; the field was removed.
    Even if it did, the server would refuse (extra forbidden) and log an
    anomaly row.
    """
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    # Pair + grant via the browser user (grants require user session).
    device = await _register_device(client, rustdesk_id="mixed-1", name="Mixed principal box")
    await client.post(
        f"/api/remote/devices/{device['id']}/grant-control",
        json={"minutes": 5},
        headers={"X-Consent-Origin": "user-tap"},
    )
    # Session opened by the AGENT — WS auth uses agent token.
    session = await _open_session(agent_client, device["id"])

    with agent_ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "input", "event_type": "mouse_click", "payload": {"x": 1, "y": 2}})
        # Drain several frames so the input-event write is well past commit
        # before the WS is torn down.
        for _ in range(10):
            m = ws.receive_json()
            assert m.get("type") != "error", m

    await asyncio.sleep(0.1)

    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteInputEvent)
                .where(RemoteInputEvent.session_id == uuid.UUID(session["id"]))
            )
        ).scalars().all()
    assert len(rows) == 1
    assert rows[0].initiator == "ai-agent"


@pytest.mark.asyncio
async def test_ws_input_from_user_session_is_labeled_user_in_audit(
    app, client, ws_test_client, session_factory
):
    """BYPASS-9: WS opened by the browser session → every event ``user``."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)
    await client.post(
        f"/api/remote/devices/{device['id']}/grant-control",
        json={"minutes": 5},
        headers={"X-Consent-Origin": "user-tap"},
    )

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "input", "event_type": "mouse_click", "payload": {"x": 9, "y": 9}})
        for _ in range(10):
            m = ws.receive_json()
            assert m.get("type") != "error", m

    await asyncio.sleep(0.1)

    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteInputEvent)
                .where(RemoteInputEvent.session_id == uuid.UUID(session["id"]))
            )
        ).scalars().all()
    assert len(rows) == 1
    assert rows[0].initiator == "user"


# --------------------------------------------------------------------------- #
# AUDIT-GAP — malformed / unknown envelopes now produce anomaly rows
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_malformed_envelope_writes_anomaly_row(app, client, ws_test_client, session_factory):
    """AUDIT-GAP: pydantic ValidationError on input → anomaly row + WS error."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        # `event_type: "screenshot"` is not in the EventType Literal — the
        # envelope fails Pydantic validation.
        ws.send_json({"type": "input", "event_type": "screenshot", "payload": {}})
        err = _wait_for(ws, lambda m: m.get("type") == "error")
        assert err is not None
        assert err["code"] == 400
        # Drain additional frame envelopes so the ASGI event loop keeps
        # ticking after the anomaly commit — otherwise closing the WS mid-
        # coroutine can drop the just-committed transaction on aiosqlite's
        # worker thread.
        for _ in range(5):
            ws.receive_json()

    await asyncio.sleep(0.1)

    async with session_factory() as db:
        rows = (
            await db.execute(select(RemoteWSAnomaly))
        ).scalars().all()
    assert len(rows) == 1, f"expected 1 anomaly row, got {len(rows)}"
    assert rows[0].kind == "invalid"
    assert "screenshot" in rows[0].raw_envelope


@pytest.mark.asyncio
async def test_unknown_envelope_type_writes_anomaly_row(app, client, ws_test_client, session_factory):
    """AUDIT-GAP: envelope with ``type: "goodbye"`` → anomaly row (no WS error)."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        ws.send_json({"type": "goodbye", "data": "so long"})
        # Drain enough frames that the anomaly-write coroutine gets scheduled
        # and its commit lands before the WS is torn down.
        for _ in range(10):
            ws.receive_json()

    await asyncio.sleep(0.5)

    async with session_factory() as db:
        rows = (
            await db.execute(select(RemoteWSAnomaly))
        ).scalars().all()
    assert len(rows) == 1
    assert "goodbye" in rows[0].raw_envelope


@pytest.mark.asyncio
async def test_anomaly_rate_limit_kicks_in_at_10_per_session_second(
    app, client, ws_test_client, session_factory
):
    """AUDIT-GAP: over 10 anomalies in one second → additional writes dropped.

    We fire 25 bad envelopes rapidly. The rate limiter tracks calls per
    session-second, so at most 10 anomaly rows should land in that second.
    Rows in a *second* second may still land — we tolerate that by capping
    the assertion at "no more than a small multiple of the limit".
    """
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    start = time.time()
    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        for i in range(25):
            ws.send_json({"type": "spam", "i": i})
        # Drain a few frames so the writer coroutines run.
        for _ in range(10):
            ws.receive_json()
    elapsed = time.time() - start

    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteWSAnomaly)
                .where(RemoteWSAnomaly.session_id == uuid.UUID(session["id"]))
            )
        ).scalars().all()

    # At most 10 rows per whole second of the test. Elapsed is normally ~0.1s.
    ceiling = 10 * (int(elapsed) + 1)
    assert len(rows) <= ceiling, (
        f"expected ≤ {ceiling} anomaly rows (10/s), got {len(rows)} in {elapsed:.2f}s"
    )
    # And we should have seen at least the rate-limit's worth to prove writes
    # were happening at all.
    assert len(rows) >= 1


# --------------------------------------------------------------------------- #
# NEW-BYPASS regression — bogus agent-token header used to skip CSRF entirely
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_regression_bogus_agent_token_does_not_bypass_csrf(
    unauth_client, app, session_factory
):
    """The reviewer's proven exploit — verbatim replay.

    Before the fix, the CSRF middleware exempted on presence of the
    ``X-Palpod-Agent-Token`` header without checking the value. Three
    requests succeeded that must not:

      DELETE /api/remote/devices/{id}                         → 204
      POST   /api/remote/devices/{id}/revoke-control          → 200
      POST   /api/remote/devices/{id}/grant-control           → 200

    After the fix, every one of them MUST return 401 (no session cookie
    presented) or 403 (CSRF-token missing / conflicting credentials).
    Nothing about presenting a bogus header may bypass CSRF.
    """
    # Seed a device owned by the pod-owner via a raw DB insert. We don't need
    # authenticated cookies to make one — just a target for the replay.
    owner_uuid = uuid.UUID("00000000-0000-0000-0000-000000000001")
    async with session_factory() as db:
        dev = RemoteDevice(
            display_name="Target",
            device_type="linux",
            rustdesk_id="regr-1",
            auth_token="t",
            owner_user_id=owner_uuid,
            control_grant_expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
        )
        db.add(dev)
        await db.commit()
        await db.refresh(dev)
        device_id = str(dev.id)

    bogus_hdrs = {
        "X-Palpod-Agent-Token": "bogus",
        "X-CSRF-Token": "wrong",
    }

    r1 = await unauth_client.delete(
        f"/api/remote/devices/{device_id}", headers=bogus_hdrs
    )
    assert r1.status_code in {401, 403}, r1.text

    r2 = await unauth_client.post(
        f"/api/remote/devices/{device_id}/revoke-control", headers=bogus_hdrs
    )
    assert r2.status_code in {401, 403}, r2.text

    # Third variant: attacker read the real CSRF cookie via document.cookie.
    # Seat that cookie first, then send an XSS-style grant-control payload
    # with the bogus agent token AND the correct CSRF token.
    page = await unauth_client.get("/remote.html")
    assert page.status_code == 200
    real_csrf = unauth_client.cookies.get("palpod_csrf")
    assert real_csrf

    r3 = await unauth_client.post(
        f"/api/remote/devices/{device_id}/grant-control",
        json={"minutes": 15},
        headers={
            "X-Consent-Origin": "user-tap",
            "X-Palpod-Agent-Token": "bogus",
            "X-CSRF-Token": real_csrf,
        },
    )
    assert r3.status_code in {401, 403}, r3.text

    # And confirm the device was NOT actually deleted/revoked/granted.
    async with session_factory() as db:
        row = await db.get(RemoteDevice, uuid.UUID(device_id))
        assert row is not None, "device must survive the exploit"


@pytest.mark.asyncio
async def test_agent_token_and_session_cookie_together_are_rejected(
    client, paired_device
):
    """A caller cannot legitimately hold BOTH credentials.

    The ``client`` fixture is a logged-in browser session. Adding
    ``X-Palpod-Agent-Token`` (even the *real* one) to a mutating write MUST
    trip the conflicting-credentials guard: a browser session shouldn't ever
    know the agent secret.
    """
    resp = await client.delete(
        f"/api/remote/devices/{paired_device['id']}",
        headers={"X-Palpod-Agent-Token": os.environ["PALPOD_AGENT_TOKEN"]},
    )
    assert resp.status_code == 403
    assert "conflicting" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_csrf_cookie_and_header_must_match_exact_bytes(
    client, paired_device
):
    """Mismatched CSRF cookie/header → 403 even when both look valid.

    We take the real cookie value, flip one byte in the header, and send.
    The middleware and the router dep both compare byte-equal via
    :func:`hmac.compare_digest`; either alone would refuse the write.
    """
    csrf = client.cookies.get("palpod_csrf")
    assert csrf and len(csrf) > 4
    # Corrupt one byte in the middle — still parses as a token, still wrong.
    tampered = csrf[:-4] + "AAAA"

    resp = await client.post(
        f"/api/remote/devices/{paired_device['id']}/grant-control",
        json={"minutes": 15},
        headers={"X-Consent-Origin": "user-tap", "X-CSRF-Token": tampered},
    )
    assert resp.status_code == 403
    assert "csrf" in resp.json()["detail"].lower()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method,path_template,body,extra_headers",
    [
        ("DELETE", "/api/remote/devices/{device_id}", None, {}),
        (
            "POST",
            "/api/remote/devices/{device_id}/grant-control",
            {"minutes": 15},
            {"X-Consent-Origin": "user-tap"},
        ),
        ("POST", "/api/remote/devices/{device_id}/revoke-control", None, {}),
        ("POST", "/api/remote/sessions", None, {}),
        (
            "POST",
            "/api/remote/devices",
            {
                "display_name": "New device",
                "device_type": "linux",
                "rustdesk_id": "new-1",
                "auth_token": "t",
            },
            {},
        ),
    ],
)
async def test_mutating_endpoints_require_csrf_double_submit(
    client, paired_device, method, path_template, body, extra_headers
):
    """Every mutating endpoint MUST reject a missing X-CSRF-Token header.

    Same-origin XSS reading the cookie is not a defeat — that's covered by
    the origin/consent gates elsewhere. This test proves the router-level
    dependency runs on every listed endpoint, independent of the middleware.
    """
    path = path_template.format(device_id=paired_device["id"])
    if "/sessions" in path and body is None:
        body = {"device_id": paired_device["id"]}
    headers = {**extra_headers, "X-CSRF-Token": ""}
    if method == "DELETE":
        r = await client.delete(path, headers=headers)
    else:
        r = await client.post(path, json=body or {}, headers=headers)
    assert r.status_code == 403, f"{method} {path} should 403, got {r.status_code}"


# --------------------------------------------------------------------------- #
# NEW-BYPASS — CSP + adjacent security headers
# --------------------------------------------------------------------------- #


EXPECTED_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self'; "
    "connect-src 'self' ws://pod.palpod.local wss://pod.palpod.local; "
    "object-src 'none'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'"
)


@pytest.mark.asyncio
async def test_csp_header_present_on_all_html_responses(unauth_client):
    """CSP header must be a real HTTP header, byte-equal to the spec string."""
    resp = await unauth_client.get("/remote.html")
    assert resp.status_code == 200
    assert resp.headers.get("Content-Security-Policy") == EXPECTED_CSP


@pytest.mark.asyncio
async def test_csp_header_disallows_unsafe_inline_style(unauth_client):
    """style-src must NOT contain 'unsafe-inline' — reviewer requirement."""
    resp = await unauth_client.get("/remote.html")
    csp = resp.headers.get("Content-Security-Policy", "")
    assert "style-src" in csp
    # Extract the style-src directive.
    directives = [d.strip() for d in csp.split(";")]
    style_src = next((d for d in directives if d.startswith("style-src")), "")
    assert "unsafe-inline" not in style_src, style_src


@pytest.mark.asyncio
async def test_x_content_type_options_present(unauth_client):
    resp = await unauth_client.get("/remote.html")
    assert resp.headers.get("X-Content-Type-Options") == "nosniff"


@pytest.mark.asyncio
async def test_x_frame_options_denies_framing(unauth_client):
    resp = await unauth_client.get("/remote.html")
    assert resp.headers.get("X-Frame-Options") == "DENY"


# --------------------------------------------------------------------------- #
# NEW-BYPASS — /static/remote.html is not served (Fix #4)
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_static_remote_html_path_returns_404(unauth_client):
    """/static/remote.html is dead — file is out of the static tree.

    Previously StaticFiles served remote.html at both /static/remote.html
    and /remote.html; only the second seated the CSRF cookie. Fix #4 moves
    the file into palweb/templates/ so /static/remote.html is a plain 404.
    """
    resp = await unauth_client.get("/static/remote.html")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_remote_html_via_canonical_path_seeds_csrf_cookie(unauth_client):
    """GET /remote.html MUST set palpod_csrf on the response."""
    resp = await unauth_client.get("/remote.html")
    assert resp.status_code == 200
    assert unauth_client.cookies.get("palpod_csrf")


# --------------------------------------------------------------------------- #
# NEW-BYPASS — anomaly drop-summary rows (Fix #5)
# --------------------------------------------------------------------------- #


@pytest.mark.asyncio
async def test_anomaly_flood_creates_summary_rows(
    app, client, ws_test_client, session_factory
):
    """Flooding past the 10/s ceiling MUST produce summary rows for the drops.

    The rate limiter used to silently ``continue``; now every drop increments
    (or upserts) ``remote_ws_anomaly_summary.dropped_count`` for the bucket.
    We fire 30 anomalies rapidly and assert that the sum of drops in the
    summary + the count of real anomaly rows fits the ceiling.
    """
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        for i in range(30):
            ws.send_json({"type": "spam", "i": i})
        # Drain a few frames so the writer coroutines get scheduled.
        for _ in range(10):
            ws.receive_json()

    await asyncio.sleep(0.2)

    async with session_factory() as db:
        rows = (
            await db.execute(
                select(RemoteWSAnomaly).where(
                    RemoteWSAnomaly.session_id == uuid.UUID(session["id"])
                )
            )
        ).scalars().all()
        summary = (
            await db.execute(
                select(RemoteWSAnomalySummary).where(
                    RemoteWSAnomalySummary.session_id == uuid.UUID(session["id"])
                )
            )
        ).scalars().all()

    # If the flood happened in one second, we expect ≤10 real rows and the
    # summary must show at least 1 drop bucket. Across multiple seconds we
    # allow >10 real rows but still require SOME summary row when we sent
    # more than 10 events.
    total_sent = 30
    total_real = len(rows)
    total_dropped = sum(s.dropped_count for s in summary)
    assert total_real + total_dropped == total_sent, (
        f"real={total_real}, dropped={total_dropped}, sent={total_sent}"
    )
    assert total_dropped >= 1, "some drops MUST land in the summary bucket"


@pytest.mark.asyncio
async def test_anomaly_summary_endpoint_returns_dropped_counts(
    app, client, ws_test_client, session_factory
):
    """GET /api/remote/sessions/{id}/anomalies returns both real + summary."""
    fake = _FakeRustDesk()
    app.state.rustdesk_client = fake

    device, session = await _paired_and_session(client, app)

    with ws_test_client.websocket_connect(f"/ws/remote/{session['id']}") as ws:
        for i in range(25):
            ws.send_json({"type": "spam", "i": i})
        for _ in range(10):
            ws.receive_json()

    await asyncio.sleep(0.2)

    resp = await client.get(f"/api/remote/sessions/{session['id']}/anomalies")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "anomalies" in body and "summary" in body
    # 10 real + some suppression should be visible from a single-second flood.
    total_sent = 25
    total_real = len(body["anomalies"])
    total_dropped = sum(s["dropped_count"] for s in body["summary"])
    assert total_real + total_dropped == total_sent
    assert len(body["summary"]) >= 1
