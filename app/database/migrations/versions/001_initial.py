"""Alembic script runner."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "opportunities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("contact_name", sa.String(255), nullable=False),
        sa.Column("contact_email", sa.String(255), nullable=False),
        sa.Column("opportunity_name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("estimated_value", sa.Float, nullable=True),
        sa.Column("currency", sa.String(10), server_default="USD"),
        sa.Column("stage", sa.String(50), nullable=False, server_default="Lead nuevo"),
        sa.Column("priority", sa.String(50), nullable=False, server_default="Media"),
        sa.Column("probability", sa.Integer, nullable=False, server_default="0"),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("next_follow_up_date", sa.Date, nullable=True),
        sa.Column("last_interaction_summary", sa.Text, nullable=True),
        sa.Column("ai_recommendation", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
    )


def downgrade() -> None:
    op.drop_table("opportunities")
