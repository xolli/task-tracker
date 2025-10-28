"""
add timestamps to tasks

Revision ID: a1b2c3d4e5f6
Revises: c3a1c9b7d3a1
Create Date: 2025-10-29 00:40:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a1b2c3d4e5f6"
down_revision = "c3a1c9b7d3a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add timestamp columns (PostgreSQL-compatible)
    op.add_column("tasks", sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("tasks", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))

    # Backfill created_at for existing rows to current timestamp; keep updated_at as NULL
    op.execute(sa.text("UPDATE tasks SET created_at = NOW() WHERE created_at IS NULL"))



def downgrade() -> None:
    op.drop_column("tasks", "updated_at")
    op.drop_column("tasks", "created_at")
