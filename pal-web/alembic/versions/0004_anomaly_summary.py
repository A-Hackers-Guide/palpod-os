"""remote_ws_anomaly_summary

Revision ID: 0004_anomaly_summary
Revises: 0003_grant_events
Create Date: 2026-08-04

Closes the "silent suppression" partial finding: the anomaly rate limiter
used to drop past-ceiling events with no trace. This table gives the drop
counter a home so a security-conscious owner can see suppression happened
per 1-second bucket per session.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision = "0004_anomaly_summary"
down_revision = "0003_grant_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "remote_ws_anomaly_summary",
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
            "bucket_start",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column("dropped_count", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint(
            "session_id",
            "bucket_start",
            name="uq_remote_ws_anomaly_summary_session_bucket",
        ),
    )
    op.create_index(
        "ix_remote_ws_anomaly_summary_session_bucket",
        "remote_ws_anomaly_summary",
        ["session_id", "bucket_start"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_remote_ws_anomaly_summary_session_bucket",
        table_name="remote_ws_anomaly_summary",
    )
    op.drop_table("remote_ws_anomaly_summary")
