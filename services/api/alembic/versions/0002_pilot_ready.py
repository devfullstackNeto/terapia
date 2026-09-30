"""Pilot-ready content metadata and self-care completion.

Revision ID: 0002
"""
import sqlalchemy as sa

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("selfcare_items", sa.Column("objective", sa.String(255), nullable=False, server_default="Apoiar uma pausa consciente"))
    op.add_column("selfcare_items", sa.Column("duration_minutes", sa.Integer(), nullable=False, server_default="5"))
    op.add_column("selfcare_items", sa.Column("instructions", sa.Text(), nullable=False, server_default="Siga as orientações sem forçar."))
    op.add_column("selfcare_items", sa.Column("category", sa.String(80), nullable=False, server_default="bem-estar"))
    op.add_column("knowledge_items", sa.Column("category", sa.String(80), nullable=False, server_default="psicoeducação"))
    op.add_column("knowledge_items", sa.Column("tags", sa.String(255), nullable=False, server_default=""))
    op.add_column("knowledge_versions", sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_table(
        "selfcare_uses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("item_id", sa.Integer(), sa.ForeignKey("selfcare_items.id"), nullable=False),
        sa.Column("feedback", sa.String(40), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_selfcare_uses_user_id", "selfcare_uses", ["user_id"])
    op.create_index("ix_selfcare_uses_item_id", "selfcare_uses", ["item_id"])


def downgrade():
    op.drop_table("selfcare_uses")
    op.drop_column("knowledge_versions", "updated_at")
    op.drop_column("knowledge_items", "tags")
    op.drop_column("knowledge_items", "category")
    op.drop_column("selfcare_items", "category")
    op.drop_column("selfcare_items", "instructions")
    op.drop_column("selfcare_items", "duration_minutes")
    op.drop_column("selfcare_items", "objective")
