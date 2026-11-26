"""create example_items table

Revision ID: 0001
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "example_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_example_items_id", "example_items", ["id"])
    op.create_index("ix_example_items_title", "example_items", ["title"])


def downgrade():
    op.drop_index("ix_example_items_title", table_name="example_items")
    op.drop_index("ix_example_items_id", table_name="example_items")
    op.drop_table("example_items")
