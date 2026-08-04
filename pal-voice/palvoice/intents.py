"""Voice-intent recognition + handlers.

This module implements the voice-facing side of the session-scoped-consent
model. The rules from the design doc are non-negotiable and enforced here:

* Recognizing a "grant Pod control" utterance MUST return an intent object
  whose handler tells the user to open pal-web and confirm. It MUST NOT
  hit the /grant-control endpoint itself. Even if it tried, the endpoint
  would refuse — pal-web requires ``X-Consent-Origin: user-tap``, a header
  only the browser's physical-tap handler sets.
* Recognizing an action utterance ("click send") on a device with NO active
  control grant returns a refusal that the orchestrator speaks back.
* Recognizing an action utterance on a device WITH an active grant returns
  an intent whose handler dispatches the input event through the authorized
  WebSocket.

The interface below is intentionally small — a real deployment plugs it into
whatever ASR + intent-classification model pal-voice runs. The classifier
here uses simple regexes because the tests only care about the branching
logic and the security posture.
"""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Awaitable, Callable, Optional, Protocol


# --------------------------------------------------------------------------- #
# Intent data classes
# --------------------------------------------------------------------------- #


@dataclass
class Intent:
    """Base class. Subclasses are matched by ``isinstance``."""


@dataclass
class RemoteViewIntent(Intent):
    """The user asked to see a device — view-only stream."""

    target_device: str


@dataclass
class RemoteGrantRequestIntent(Intent):
    """The user asked pal-voice to grant control.

    IMPORTANT: pal-voice does not actually grant. The handler for this
    intent produces a spoken response telling the user to open pal-web and
    tap the button. The web UI is where the grant is minted.
    """

    target_device: str
    minutes: int


@dataclass
class RemoteActionIntent(Intent):
    """The user asked pal-voice to perform an action on a remote device."""

    target_device: str
    action_verb: str
    target_element: Optional[str] = None


@dataclass
class UnknownIntent(Intent):
    raw: str = ""


# --------------------------------------------------------------------------- #
# Handler responses
# --------------------------------------------------------------------------- #


@dataclass
class SpokenResponse:
    """What the orchestrator speaks back to the user."""

    text: str
    dispatched_action: bool = False
    bounced_to_web: bool = False
    view_opened: bool = False
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


# --------------------------------------------------------------------------- #
# Grant-state lookup + input dispatch (dependency-injected in tests)
# --------------------------------------------------------------------------- #


class GrantChecker(Protocol):
    """Returns the current control-grant expiry for a device, or None."""

    async def __call__(self, target_device: str) -> Optional[datetime]: ...


class InputDispatcher(Protocol):
    """Dispatches an input event through the AUTHORIZED WebSocket path.

    The dispatcher's implementation is expected to already sit inside a
    session bound to a device whose grant is active. It re-checks anyway —
    defense in depth mirrors the pal-web side.
    """

    async def __call__(
        self, target_device: str, event_type: str, payload: dict
    ) -> None: ...


class ViewOpener(Protocol):
    """Opens a view-only stream in the pal-web UI."""

    async def __call__(self, target_device: str) -> None: ...


# --------------------------------------------------------------------------- #
# Parser
# --------------------------------------------------------------------------- #


_VIEW_RE = re.compile(
    r"""(?ix)
    ^\s*
    (?:please\s+)?
    (?:show|display|open|pull\s+up)\s+
    (?:me\s+)?
    (?:the\s+)?
    (?P<device>[a-z0-9\-\s]+?)
    \s*$
    """
)

_GRANT_RE = re.compile(
    r"""(?ix)
    ^\s*
    (?:let\s+me\s+)?
    (?:grant|give)\s+
    (?:pod\s+)?
    control\s+
    (?:of\s+)?
    (?:my\s+)?
    (?P<device>[a-z0-9\-\s]+?)
    (?:\s+for\s+(?P<minutes>\d+)\s+minutes?)?
    \s*$
    """
)

_ACTION_RE = re.compile(
    r"""(?ix)
    ^\s*
    (?P<verb>click|press|tap|type|select|open)
    \s+
    (?P<element>[a-z0-9\-\s]+?)
    (?:\s+on\s+(?:my\s+)?(?P<device>[a-z0-9\-\s]+?))?
    \s*$
    """
)


def parse(utterance: str) -> Intent:
    """Classify an utterance into a structured intent.

    The regexes are simple on purpose — the point of this module is the
    branching logic, not NLU quality. The device string is normalized
    (lowercased, whitespace-collapsed).
    """
    if not utterance or not utterance.strip():
        return UnknownIntent(raw=utterance or "")

    # Order matters: try the most specific patterns first.
    m = _GRANT_RE.match(utterance)
    if m:
        device = _normalize_device(m.group("device"))
        minutes_str = m.group("minutes")
        minutes = int(minutes_str) if minutes_str else 15
        # Cap at 60; the web endpoint would refuse anything higher.
        minutes = max(1, min(minutes, 60))
        return RemoteGrantRequestIntent(target_device=device, minutes=minutes)

    m = _ACTION_RE.match(utterance)
    if m:
        return RemoteActionIntent(
            target_device=_normalize_device(m.group("device") or ""),
            action_verb=m.group("verb").lower(),
            target_element=m.group("element").strip().lower(),
        )

    m = _VIEW_RE.match(utterance)
    if m:
        return RemoteViewIntent(target_device=_normalize_device(m.group("device")))

    return UnknownIntent(raw=utterance)


def _normalize_device(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


# --------------------------------------------------------------------------- #
# Handlers
# --------------------------------------------------------------------------- #


async def handle_view(
    intent: RemoteViewIntent, *, open_view: ViewOpener
) -> SpokenResponse:
    """Open a view-only stream. Never touches input authorization."""
    await open_view(intent.target_device)
    return SpokenResponse(
        text=f"Showing {intent.target_device}. View-only.",
        view_opened=True,
        metadata={"target_device": intent.target_device},
    )


async def handle_grant_request(
    intent: RemoteGrantRequestIntent,
) -> SpokenResponse:
    """Handle a "grant Pod control" utterance.

    NON-NEGOTIABLE: this handler NEVER calls /grant-control. It builds a
    spoken response asking the user to open pal-web and tap.
    """
    return SpokenResponse(
        text=(
            f"Open the pal-web app on your phone or laptop and confirm the "
            f"grant for {intent.target_device} — {intent.minutes} minutes."
        ),
        bounced_to_web=True,
        dispatched_action=False,
        metadata={
            "target_device": intent.target_device,
            "minutes": intent.minutes,
            "action_required": "user_tap_in_palweb",
        },
    )


async def handle_action(
    intent: RemoteActionIntent,
    *,
    check_grant: GrantChecker,
    dispatch: InputDispatcher,
) -> SpokenResponse:
    """Handle "click X on Y" style utterances.

    * If the device has no active control grant, speak the exact refusal
      required by the design doc and return without dispatching.
    * If it does, translate the action verb into an input event and
      dispatch through the authorized WebSocket path.
    """
    expiry = await check_grant(intent.target_device)
    now = datetime.now(timezone.utc)
    grant_active = expiry is not None and (
        expiry.replace(tzinfo=timezone.utc) if expiry.tzinfo is None else expiry
    ) > now

    if not grant_active:
        return SpokenResponse(
            text=(
                f"I don't currently have control of {intent.target_device}. "
                f"Grant me control in the pal-web app first."
            ),
            dispatched_action=False,
            error="no_active_grant",
            metadata={"target_device": intent.target_device},
        )

    event_type, payload = _verb_to_event(intent.action_verb, intent.target_element or "")
    await dispatch(intent.target_device, event_type, payload)
    return SpokenResponse(
        text=f"OK — {intent.action_verb} {intent.target_element} on {intent.target_device}.",
        dispatched_action=True,
        metadata={
            "target_device": intent.target_device,
            "event_type": event_type,
        },
    )


def _verb_to_event(verb: str, element: str) -> tuple[str, dict]:
    if verb in ("click", "tap", "select"):
        return "mouse_click", {"target_element": element}
    if verb == "type":
        return "type_text", {"text": element}
    if verb == "press":
        return "key_press", {"key": element}
    if verb == "open":
        return "mouse_click", {"target_element": element, "hint": "open"}
    return "mouse_click", {"target_element": element}


# --------------------------------------------------------------------------- #
# Top-level orchestrator entry point
# --------------------------------------------------------------------------- #


async def handle_utterance(
    utterance: str,
    *,
    check_grant: GrantChecker,
    dispatch: InputDispatcher,
    open_view: ViewOpener,
) -> SpokenResponse:
    """Parse an utterance and route to the appropriate handler.

    Any unknown utterance yields a benign "didn't catch that" response.
    """
    intent = parse(utterance)
    if isinstance(intent, RemoteViewIntent):
        return await handle_view(intent, open_view=open_view)
    if isinstance(intent, RemoteGrantRequestIntent):
        return await handle_grant_request(intent)
    if isinstance(intent, RemoteActionIntent):
        return await handle_action(intent, check_grant=check_grant, dispatch=dispatch)
    return SpokenResponse(text="Sorry — I didn't catch that.", error="unknown_intent")
