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
    # Use batch mode for SQLite compatibility (drop column on downgrade, etc.)
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(sa.Column("created_at", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))

    # Backfill created_at for existing rows to current timestamp; keep updated_at as NULL
    op.execute("UPDATE tasks SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")



def downgrade() -> None:
    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.drop_column("updated_at")
        batch_op.drop_column("created_at")
