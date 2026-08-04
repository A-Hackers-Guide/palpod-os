"""httpx-based client for the self-hosted RustDesk (hbbs/hbbr) stack.

Every method takes an ``authorization_context`` describing the caller's grant
state. On input-event methods the client checks the context AT ENTRY and
raises ``InsufficientAuthorization`` if a control grant is not active. This
is defense-in-depth: the router already checks the grant window before
calling into this client, so the client refusing again means a bug or a
compromised caller can never sneak an input event past.

The context shape:

    {
        "grant_active": bool,
        "grant_expires_at": Optional[datetime],
        "initiator": "user" | "ai-agent",
    }
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

import httpx


HBBS_BASE_URL = os.environ.get("RUSTDESK_HBBS_URL", "http://hbbs:21114")
HBBR_BASE_URL = os.environ.get("RUSTDESK_HBBR_URL", "http://hbbr:21117")

_INPUT_EVENT_TYPES: frozenset[str] = frozenset(
    {"mouse_move", "mouse_click", "key_press", "type_text"}
)


class InsufficientAuthorization(Exception):
    """Raised when an input dispatch is attempted without an active grant.

    This exception is the last line of defense — hitting it should always
    indicate either (a) a bug in the router, or (b) a caller trying to bypass
    the router. Either way the event MUST NOT be forwarded to RustDesk.
    """

    def __init__(self, event_type: str, context: "AuthorizationContext"):
        self.event_type = event_type
        self.context = context
        super().__init__(
            f"input event {event_type!r} rejected: grant_active="
            f"{context['grant_active']}, expires_at={context['grant_expires_at']}"
        )


AuthorizationContext = dict  # {"grant_active": bool, "grant_expires_at": Optional[datetime], "initiator": str}


@dataclass
class ScreenFrame:
    rustdesk_id: str
    png_bytes: bytes
    captured_at: datetime


class RustDeskClient:
    """Thin async wrapper around the RustDesk hbbs/hbbr HTTP surface.

    The class is intentionally small: it exists so the router can be unit-
    tested with a respx-mocked httpx transport, and so the authorization
    check on input events sits behind ONE function that cannot be forgotten.
    """

    def __init__(
        self,
        hbbs_base_url: str = HBBS_BASE_URL,
        hbbr_base_url: str = HBBR_BASE_URL,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self._hbbs_base_url = hbbs_base_url.rstrip("/")
        self._hbbr_base_url = hbbr_base_url.rstrip("/")
        self._owns_client = http_client is None
        self._http = http_client or httpx.AsyncClient(timeout=5.0)

    async def close(self) -> None:
        if self._owns_client:
            await self._http.aclose()

    # -- Read paths (no authorization check needed) ------------------------- #

    async def list_online_devices(
        self, *, authorization_context: AuthorizationContext
    ) -> list[dict[str, Any]]:
        """Return the list of currently-online device records from hbbs.

        View-only endpoint; requires no grant. The context is still accepted
        so the client's surface is uniform and audit-loggable.
        """
        _ = authorization_context  # unused but part of the contract
        resp = await self._http.get(f"{self._hbbs_base_url}/api/status/online")
        resp.raise_for_status()
        data = resp.json()
        return list(data.get("devices", []))

    async def get_screen_frame(
        self, rustdesk_id: str, *, authorization_context: AuthorizationContext
    ) -> ScreenFrame:
        """Fetch a single PNG frame via the relay.

        View-only endpoint; requires no grant. The context is still accepted
        so the client's surface is uniform and audit-loggable.
        """
        _ = authorization_context  # unused but part of the contract
        resp = await self._http.get(
            f"{self._hbbr_base_url}/frame/{rustdesk_id}"
        )
        resp.raise_for_status()
        return ScreenFrame(
            rustdesk_id=rustdesk_id,
            png_bytes=resp.content,
            captured_at=datetime.now(timezone.utc),
        )

    # -- Input dispatch (authorization-gated) ------------------------------- #

    async def send_input_event(
        self,
        rustdesk_id: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        authorization_context: AuthorizationContext,
    ) -> None:
        """Forward an input event to the relay.

        Raises :class:`InsufficientAuthorization` before touching the network
        if:
          - the event_type is an input event, AND
          - ``authorization_context['grant_active']`` is not truthy, OR
          - ``authorization_context['grant_expires_at']`` is in the past.

        The router MUST also check the grant state — this check exists so
        that even if the caller is buggy or malicious, no input event ever
        leaves the pal-web process without an active grant.
        """
        if event_type in _INPUT_EVENT_TYPES:
            self._enforce_grant(event_type, authorization_context)

        resp = await self._http.post(
            f"{self._hbbr_base_url}/input/{rustdesk_id}",
            json={"event_type": event_type, "payload": payload},
        )
        resp.raise_for_status()

    # -- Internal ----------------------------------------------------------- #

    @staticmethod
    def _enforce_grant(
        event_type: str, context: AuthorizationContext
    ) -> None:
        grant_active = bool(context.get("grant_active"))
        expires_at: Optional[datetime] = context.get("grant_expires_at")

        if not grant_active:
            raise InsufficientAuthorization(event_type, context)

        # Even if the caller claims grant_active=True, verify the timestamp is
        # actually in the future. A stale context must not slip through.
        if expires_at is None:
            raise InsufficientAuthorization(event_type, context)
        now = datetime.now(timezone.utc)
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= now:
            raise InsufficientAuthorization(event_type, context)
