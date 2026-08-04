"""SQLAlchemy ORM models for pal-web.

The remote-control models below (RemoteDevice, RemoteSession, RemoteInputEvent)
implement the session-scoped consent model documented in the pal-web design doc:
input events on remote user devices are only ever permitted while
``RemoteDevice.control_grant_expires_at`` is in the future, and every input
event — permitted or rejected — is written to RemoteInputEvent for audit.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    TypeDecorator,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB as _PG_JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UUID(TypeDecorator):
    """Portable UUID type: postgresql.UUID on postgres, CHAR(32) elsewhere."""

    impl = Uuid
    cache_ok = True

    def __init__(self, as_uuid: bool = True) -> None:  # noqa: FBT001, FBT002
        self._as_uuid = as_uuid
        super().__init__()

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(Uuid(as_uuid=self._as_uuid))


class JSONB(TypeDecorator):
    """Portable JSONB: postgresql.JSONB on postgres, generic JSON elsewhere."""

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(_PG_JSONB())
        return dialect.type_descriptor(JSON())

from .database import Base


# --------------------------------------------------------------------------- #
# Remote-control models (APPEND — see design doc §"Your scope").
# --------------------------------------------------------------------------- #


class RemoteDevice(Base):
    """A paired remote device (user's laptop, phone, workstation) reachable
    through the self-hosted RustDesk relay.

    ``control_grant_expires_at`` is the single source of truth for whether the
    Pod is currently allowed to send *input* events (mouse/keyboard) to this
    device. It is set only by the /grant-control endpoint, which itself
    requires the ``X-Consent-Origin: user-tap`` header. When the timestamp is
    NULL or in the past, the device is view-only.
    """

    __tablename__ = "remote_devices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    device_type: Mapped[str] = mapped_column(String(32), nullable=False)  # macos, windows, linux, ios, android
    rustdesk_id: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    auth_token: Mapped[str] = mapped_column(String(128), nullable=False)

    # The consent window. NULL == view-only. A timestamp in the past == expired
    # (view-only). A timestamp in the future == control granted.
    control_grant_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    paired_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    owner_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    sessions: Mapped[list["RemoteSession"]] = relationship(
        "RemoteSession", back_populates="device", cascade="all, delete-orphan"
    )


class RemoteSession(Base):
    """A single view or control session against a RemoteDevice.

    ``was_authorized`` records whether an active control grant was in force
    for the entire session — i.e. did any input event fire under a valid
    grant window. Purely view-only sessions have was_authorized=False (no
    grant was needed, no grant was used).
    """

    __tablename__ = "remote_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("remote_devices.id", ondelete="CASCADE"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # 'voice' | 'web' | 'ai-agent'
    initiated_by: Mapped[str] = mapped_column(String(16), nullable=False)
    transcript: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    was_authorized: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    device: Mapped[RemoteDevice] = relationship("RemoteDevice", back_populates="sessions")
    input_events: Mapped[list["RemoteInputEvent"]] = relationship(
        "RemoteInputEvent", back_populates="session", cascade="all, delete-orphan"
    )


class RemoteInputEvent(Base):
    """Audit log of every attempted input event.

    Rows exist for BOTH authorized and rejected events. The
    ``grant_active_at_time`` column is the server's authoritative snapshot at
    the instant of the event — the pair (authorized, grant_active_at_time)
    lets a reviewer distinguish rejected events (e.g. expired grant) from
    accepted ones. Payloads are stored redacted: for `type_text` events we
    persist a length + hash, not the raw keystrokes.
    """

    __tablename__ = "remote_input_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("remote_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    # 'mouse_move' | 'mouse_click' | 'key_press' | 'type_text'
    event_type: Mapped[str] = mapped_column(String(16), nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # 'user' | 'ai-agent'
    initiator: Mapped[str] = mapped_column(String(16), nullable=False)
    authorized: Mapped[bool] = mapped_column(Boolean, nullable=False)
    grant_active_at_time: Mapped[bool] = mapped_column(Boolean, nullable=False)

    session: Mapped[RemoteSession] = relationship("RemoteSession", back_populates="input_events")


class RemoteGrantEvent(Base):
    """Append-only audit log of every control grant + revoke.

    Solves BYPASS #6 (grant window rollover unbounded): the daily rolling cap
    on control minutes is computed from this table, and the 30-second cool-down
    between grants uses the most recent row's ``granted_at``. Revocation
    stamps ``revoked_early_at`` on the still-open row so a reviewer can
    reconstruct which grants actually ran to their advertised expiry vs. which
    were cut short by the user.

    ``csrf_token_hash`` and ``origin`` freeze the exact authenticating context
    of every mint — indispensable when investigating an incident.
    """

    __tablename__ = "remote_grant_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("remote_devices.id", ondelete="CASCADE"),
        nullable=False,
    )
    granted_by_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False
    )
    granted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    csrf_token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    origin: Mapped[str] = mapped_column(String(255), nullable=False)
    revoked_early_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class RemoteWSAnomaly(Base):
    """Every malformed / unexpected WebSocket envelope gets a row.

    Solves the partial-audit gap: previously non-``input`` envelopes were
    silently ``continue``d and malformed input envelopes returned a WS error
    but wrote no audit row. Now both cases land here (rate-limited to at most
    10 rows per session-second) so a reviewer can see the shape of every
    payload that hit the WS layer.
    """

    __tablename__ = "remote_ws_anomalies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("remote_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    # 'invalid' — extend if new anomaly categories emerge.
    kind: Mapped[str] = mapped_column(String(32), nullable=False, default="invalid")
    reason: Mapped[str] = mapped_column(String(255), nullable=False)
    raw_envelope: Mapped[str] = mapped_column(Text, nullable=False)
    initiator: Mapped[str] = mapped_column(String(16), nullable=False)


class RemoteWSAnomalySummary(Base):
    """Per-second per-session count of anomalies the rate limiter DROPPED.

    Before this table existed the rate limiter silently discarded every write
    past the 10/second ceiling — a security-conscious owner had no way to
    tell whether an attacker was flooding the WS with garbage under the audit
    log. Now every drop increments the current 1-second bucket's
    ``dropped_count`` via an upsert on ``(session_id, bucket_start)``, so the
    audit view can render "10 rows + N suppressed" for the interval.
    """

    __tablename__ = "remote_ws_anomaly_summary"
    __table_args__ = (
        UniqueConstraint(
            "session_id",
            "bucket_start",
            name="uq_remote_ws_anomaly_summary_session_bucket",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("remote_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    bucket_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    dropped_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
