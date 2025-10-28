"""
create tasks table

Revision ID: c3a1c9b7d3a1
Revises: 
Create Date: 2025-10-28 20:58:00.000000
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "c3a1c9b7d3a1"
down_revision = None
branch_labels = None
depends_on = None


STATUS_VALUES = ("pending", "in_progress", "done")


def upgrade() -> None:
    # Create table with CHECK constraint embedded (works on SQLite)
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default=sa.text("'pending'")),
        sa.CheckConstraint(
            f"status IN ({', '.join([repr(v) for v in STATUS_VALUES])})",
            name="ck_tasks_status_valid",
        ),
    )

    # Indexes similar to SQLModel Field(index=True)
    op.create_index("ix_tasks_title", "tasks", ["title"], unique=False)
    op.create_index("ix_tasks_status", "tasks", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_tasks_status", table_name="tasks")
    op.drop_index("ix_tasks_title", table_name="tasks")
    op.drop_constraint("ck_tasks_status_valid", "tasks", type_="check")
    op.drop_table("tasks")
