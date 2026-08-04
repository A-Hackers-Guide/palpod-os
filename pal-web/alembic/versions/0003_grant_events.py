"""remote_grant_events, remote_ws_anomalies

Revision ID: 0003_grant_events
Revises: 0002_remote_devices
Create Date: 2026-08-04

Closes the audit-trail half of security-reviewer BYPASS #6 (grant window
rollover unbounded) and the "audit gap" partial finding.

* remote_grant_events is append-only. Every accepted grant writes a row in
  the same transaction as the ``control_grant_expires_at`` update on
  remote_devices, and every revoke stamps ``revoked_early_at`` on the still-
  open row. The 30-second cool-down and 240-minute-per-24-hour cap are both
  computed from this table.
* remote_ws_anomalies logs malformed / unexpected WebSocket envelopes with
  the raw payload truncated to 512 chars.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = "0003_grant_events"
down_revision = "0002_remote_devices"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "remote_grant_events",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "device_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("remote_devices.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "granted_by_user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "granted_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("minutes", sa.Integer(), nullable=False),
        sa.Column("csrf_token_hash", sa.String(length=64), nullable=False),
        sa.Column("origin", sa.String(length=255), nullable=False),
        sa.Column("revoked_early_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_remote_grant_events_device_id_granted_at",
        "remote_grant_events",
        ["device_id", "granted_at"],
    )

    op.create_table(
        "remote_ws_anomalies",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column(
            "session_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("remote_sessions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "kind",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'invalid'"),
        ),
        sa.Column("reason", sa.String(length=255), nullable=False),
        sa.Column("raw_envelope", sa.Text(), nullable=False),
        sa.Column("initiator", sa.String(length=16), nullable=False),
    )
    op.create_index(
        "ix_remote_ws_anomalies_session_id_timestamp",
        "remote_ws_anomalies",
        ["session_id", "timestamp"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_remote_ws_anomalies_session_id_timestamp",
        table_name="remote_ws_anomalies",
    )
    op.drop_table("remote_ws_anomalies")

    op.drop_index(
        "ix_remote_grant_events_device_id_granted_at",
        table_name="remote_grant_events",
    )
    op.drop_table("remote_grant_events")
