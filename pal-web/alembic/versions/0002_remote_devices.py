"""remote_devices, remote_sessions, remote_input_events

Revision ID: 0002_remote_devices
Revises: 0001_init
Create Date: 2026-08-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0002_remote_devices"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "remote_devices",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("device_type", sa.String(length=32), nullable=False),
        sa.Column("rustdesk_id", sa.String(length=64), nullable=False, unique=True),
        sa.Column("auth_token", sa.String(length=128), nullable=False),
        sa.Column(
            "control_grant_expires_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
        sa.Column(
            "paired_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_index(
        "ix_remote_devices_owner_user_id", "remote_devices", ["owner_user_id"]
    )

    op.create_table(
        "remote_sessions",
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
            "started_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("initiated_by", sa.String(length=16), nullable=False),
        sa.Column("transcript", sa.Text(), nullable=True),
        sa.Column(
            "was_authorized",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.create_index(
        "ix_remote_sessions_device_id", "remote_sessions", ["device_id"]
    )

    op.create_table(
        "remote_input_events",
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
        sa.Column("event_type", sa.String(length=16), nullable=False),
        sa.Column(
            "payload_json",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("initiator", sa.String(length=16), nullable=False),
        sa.Column("authorized", sa.Boolean(), nullable=False),
        sa.Column("grant_active_at_time", sa.Boolean(), nullable=False),
    )
    op.create_index(
        "ix_remote_input_events_session_id",
        "remote_input_events",
        ["session_id"],
    )
    op.create_index(
        "ix_remote_input_events_authorized",
        "remote_input_events",
        ["authorized"],
    )


def downgrade() -> None:
    op.drop_index("ix_remote_input_events_authorized", table_name="remote_input_events")
    op.drop_index("ix_remote_input_events_session_id", table_name="remote_input_events")
    op.drop_table("remote_input_events")

    op.drop_index("ix_remote_sessions_device_id", table_name="remote_sessions")
    op.drop_table("remote_sessions")

    op.drop_index("ix_remote_devices_owner_user_id", table_name="remote_devices")
    op.drop_table("remote_devices")
