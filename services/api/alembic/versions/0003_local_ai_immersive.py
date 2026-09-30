"""Local AI and immersive wellbeing features.

Revision ID: 0003
"""

import sqlalchemy as sa

from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint("appointments_slot_id_key", "appointments", type_="unique")
    op.create_index("ix_appointments_slot_id", "appointments", ["slot_id"])
    op.add_column("journal_entries", sa.Column("tags", sa.String(255), nullable=False, server_default=""))
    op.add_column("selfcare_uses", sa.Column("status", sa.String(20), nullable=False, server_default="completed"))
    op.add_column("selfcare_uses", sa.Column("started_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.alter_column("selfcare_uses", "completed_at", existing_type=sa.DateTime(), nullable=True, server_default=None)
    op.create_table(
        "journal_attachments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entry_id", sa.Integer(), sa.ForeignKey("journal_entries.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("filename", sa.String(180), nullable=False),
        sa.Column("content_type", sa.String(80), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("content", sa.LargeBinary(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_journal_attachments_entry_id", "journal_attachments", ["entry_id"])
    op.create_index("ix_journal_attachments_user_id", "journal_attachments", ["user_id"])
    op.create_table(
        "chat_feedback",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("message_id", sa.Integer(), sa.ForeignKey("conversation_messages.id"), nullable=False, unique=True),
        sa.Column("useful", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_chat_feedback_user_id", "chat_feedback", ["user_id"])


def downgrade():
    op.drop_index("ix_appointments_slot_id", table_name="appointments")
    op.create_unique_constraint("appointments_slot_id_key", "appointments", ["slot_id"])
    op.drop_table("chat_feedback")
    op.drop_table("journal_attachments")
    op.alter_column("selfcare_uses", "completed_at", existing_type=sa.DateTime(), nullable=False)
    op.drop_column("selfcare_uses", "started_at")
    op.drop_column("selfcare_uses", "status")
    op.drop_column("journal_entries", "tags")
