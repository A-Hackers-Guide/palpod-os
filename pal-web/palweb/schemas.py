"""Pydantic request/response schemas for pal-web.

The remote-control schemas below enforce the security-critical constraints
of the design doc at parse time (max 60-minute grant, enumerated event
types, redacted payload contract).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# --------------------------------------------------------------------------- #
# Remote-control schemas (APPEND).
# --------------------------------------------------------------------------- #


DeviceType = Literal["macos", "windows", "linux", "ios", "android"]
InitiatedBy = Literal["voice", "web", "ai-agent"]
Initiator = Literal["user", "ai-agent"]
EventType = Literal["mouse_move", "mouse_click", "key_press", "type_text"]
ControlState = Literal["view_only", "granted", "revoked"]


class DeviceRegisterRequest(BaseModel):
    display_name: str = Field(min_length=1, max_length=128)
    device_type: DeviceType
    rustdesk_id: str = Field(min_length=1, max_length=64)
    auth_token: str = Field(min_length=1, max_length=128)


class DeviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    display_name: str
    device_type: DeviceType
    rustdesk_id: str
    paired_at: datetime
    last_seen_at: Optional[datetime]
    control_state: ControlState
    control_grant_expires_at: Optional[datetime]


class GrantControlRequest(BaseModel):
    """Grant window request.

    Field-level validation enforces the doc's non-negotiable ceiling: minutes
    is bounded [1, 60]. Requests outside that range return HTTP 422 before
    the endpoint body ever runs.
    """

    minutes: int = Field(default=15, ge=1, le=60)


class GrantControlResponse(BaseModel):
    device_id: uuid.UUID
    control_state: ControlState
    control_grant_expires_at: datetime


class RevokeControlResponse(BaseModel):
    device_id: uuid.UUID
    control_state: ControlState
    revoked_at: datetime


class SessionCreateRequest(BaseModel):
    """Session-open request.

    BYPASS #9 fix: ``initiated_by`` is server-derived from the authenticated
    principal — clients cannot influence it. The model refuses the field
    entirely so a client that tries to smuggle ``initiated_by: "user"`` on an
    agent-token call gets a 422 rather than a silent override.
    """

    model_config = ConfigDict(extra="forbid")

    device_id: uuid.UUID
    transcript: Optional[str] = None


class SessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    device_id: uuid.UUID
    started_at: datetime
    ended_at: Optional[datetime]
    initiated_by: InitiatedBy
    was_authorized: bool


class InputEventEnvelope(BaseModel):
    """Client -> server input event over the WebSocket.

    BYPASS #9 fix: the ``initiator`` field has been removed. The server
    derives it from the WebSocket's authenticated principal at handshake time
    and writes that value into every audit row. ``extra="forbid"`` blocks the
    common workaround of smuggling the field in anyway — a client-supplied
    ``initiator`` yields a Pydantic ValidationError (and an anomaly row).
    """

    model_config = ConfigDict(extra="forbid")

    type: Literal["input"] = "input"
    event_type: EventType
    payload: dict[str, Any] = Field(default_factory=dict)


class WebSocketError(BaseModel):
    type: Literal["error"] = "error"
    error: str
    code: int


class GrantExpiredNotice(BaseModel):
    type: Literal["grant_expired"] = "grant_expired"
    device_id: uuid.UUID
    expired_at: datetime


class LoginRequest(BaseModel):
    """Login body — accepts the device-local password from .env only."""

    password: str = Field(min_length=1, max_length=256)


class LoginResponse(BaseModel):
    ok: bool
    user_id: uuid.UUID


class GrantEventOut(BaseModel):
    """Row of the grant-event audit trail exposed to the UI."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    device_id: uuid.UUID
    granted_at: datetime
    minutes: int
    origin: str
    revoked_early_at: Optional[datetime] = None


class WSAnomalyOut(BaseModel):
    """One real anomaly row — everything the rate limiter DIDN'T drop."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    session_id: uuid.UUID
    timestamp: datetime
    kind: str
    reason: str
    raw_envelope: str
    initiator: str


class WSAnomalySummaryOut(BaseModel):
    """Per 1-second bucket count of anomalies the rate limiter suppressed."""

    model_config = ConfigDict(from_attributes=True)

    session_id: uuid.UUID
    bucket_start: datetime
    dropped_count: int


class SessionAnomaliesOut(BaseModel):
    """Combined anomalies + summary payload for the UI audit view."""

    anomalies: list[WSAnomalyOut]
    summary: list[WSAnomalySummaryOut]
