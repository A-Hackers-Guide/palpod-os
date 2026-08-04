"""Tests for palvoice.intents.

Each intent parse + handler is covered. The security-critical cases —
grant-request bounces the user to web, action on ungranted device speaks a
refusal — get their own tests marked with CONSENT-BYPASS-ATTEMPT in the
docstring.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from palvoice.intents import (
    RemoteActionIntent,
    RemoteGrantRequestIntent,
    RemoteViewIntent,
    UnknownIntent,
    handle_utterance,
    parse,
)


# --------------------------------------------------------------------------- #
# Parsing
# --------------------------------------------------------------------------- #


def test_parse_view_utterance_returns_view_intent():
    intent = parse("show me the office mac")
    assert isinstance(intent, RemoteViewIntent)
    assert intent.target_device == "office mac"


def test_parse_grant_request_with_minutes():
    intent = parse("let me grant Pod control of my laptop for 10 minutes")
    assert isinstance(intent, RemoteGrantRequestIntent)
    assert intent.target_device == "laptop"
    assert intent.minutes == 10


def test_parse_grant_request_defaults_to_15_minutes():
    intent = parse("grant control of workstation")
    assert isinstance(intent, RemoteGrantRequestIntent)
    assert intent.minutes == 15


def test_parse_grant_request_caps_minutes_at_60():
    """Even if the user says 90 minutes, the intent caps at 60 — mirrors
    the /grant-control endpoint's Pydantic ceiling."""
    intent = parse("grant control of laptop for 90 minutes")
    assert isinstance(intent, RemoteGrantRequestIntent)
    assert intent.minutes == 60


def test_parse_action_utterance():
    intent = parse("click send on my laptop")
    assert isinstance(intent, RemoteActionIntent)
    assert intent.target_device == "laptop"
    assert intent.action_verb == "click"
    assert intent.target_element == "send"


def test_parse_unknown_returns_unknown_intent():
    assert isinstance(parse("what time is it"), UnknownIntent)


# --------------------------------------------------------------------------- #
# Handler behaviors — the security posture
# --------------------------------------------------------------------------- #


class _RecordingDispatcher:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    async def __call__(self, target_device, event_type, payload):
        self.calls.append((target_device, event_type, payload))


class _RecordingViewOpener:
    def __init__(self) -> None:
        self.opened: list[str] = []

    async def __call__(self, target_device):
        self.opened.append(target_device)


def _grant_checker(expiry):
    async def _check(_device):
        return expiry
    return _check


@pytest.mark.asyncio
async def test_view_intent_opens_view_only_stream():
    opener = _RecordingViewOpener()
    disp = _RecordingDispatcher()
    resp = await handle_utterance(
        "show me the office mac",
        check_grant=_grant_checker(None),
        dispatch=disp,
        open_view=opener,
    )
    assert resp.view_opened is True
    assert opener.opened == ["office mac"]
    assert disp.calls == []
    assert "view-only" in resp.text.lower()


@pytest.mark.asyncio
async def test_grant_request_bounces_to_web_and_never_dispatches():
    """CONSENT-BYPASS-ATTEMPT: the voice orchestrator MUST NOT mint a grant.

    A "grant Pod control" utterance produces a spoken response telling the
    user to open pal-web and tap. The handler MUST NOT dispatch any input
    event and MUST NOT hit the /grant-control endpoint.
    """
    disp = _RecordingDispatcher()
    opener = _RecordingViewOpener()
    resp = await handle_utterance(
        "let me grant Pod control of my laptop for 10 minutes",
        check_grant=_grant_checker(None),
        dispatch=disp,
        open_view=opener,
    )
    assert resp.bounced_to_web is True
    assert resp.dispatched_action is False
    assert "pal-web" in resp.text.lower()
    assert disp.calls == []
    assert opener.opened == []
    assert resp.metadata["action_required"] == "user_tap_in_palweb"


@pytest.mark.asyncio
async def test_action_intent_on_ungranted_device_speaks_refusal():
    """CONSENT-BYPASS-ATTEMPT: "click send" with no active grant.

    The handler MUST refuse with the exact language from the design doc
    ("I don't currently have control") and MUST NOT call the dispatcher.
    """
    disp = _RecordingDispatcher()
    resp = await handle_utterance(
        "click send on my laptop",
        check_grant=_grant_checker(None),
        dispatch=disp,
        open_view=_RecordingViewOpener(),
    )
    assert resp.dispatched_action is False
    assert resp.error == "no_active_grant"
    assert "don't currently have control" in resp.text.lower()
    assert "grant me control in the pal-web app first" in resp.text.lower()
    assert disp.calls == []


@pytest.mark.asyncio
async def test_action_intent_on_expired_grant_speaks_refusal():
    """CONSENT-BYPASS-ATTEMPT: an expired grant is treated as no grant."""
    disp = _RecordingDispatcher()
    past = datetime.now(timezone.utc) - timedelta(seconds=1)
    resp = await handle_utterance(
        "click send on my laptop",
        check_grant=_grant_checker(past),
        dispatch=disp,
        open_view=_RecordingViewOpener(),
    )
    assert resp.dispatched_action is False
    assert disp.calls == []


@pytest.mark.asyncio
async def test_action_intent_with_active_grant_dispatches():
    disp = _RecordingDispatcher()
    future = datetime.now(timezone.utc) + timedelta(minutes=5)
    resp = await handle_utterance(
        "click send on my laptop",
        check_grant=_grant_checker(future),
        dispatch=disp,
        open_view=_RecordingViewOpener(),
    )
    assert resp.dispatched_action is True
    assert len(disp.calls) == 1
    device, event_type, payload = disp.calls[0]
    assert device == "laptop"
    assert event_type == "mouse_click"
    assert payload["target_element"] == "send"


@pytest.mark.asyncio
async def test_unknown_utterance_yields_benign_response():
    disp = _RecordingDispatcher()
    resp = await handle_utterance(
        "what time is it",
        check_grant=_grant_checker(None),
        dispatch=disp,
        open_view=_RecordingViewOpener(),
    )
    assert resp.error == "unknown_intent"
    assert disp.calls == []
