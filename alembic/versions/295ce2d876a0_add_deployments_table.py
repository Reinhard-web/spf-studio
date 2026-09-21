"""add deployments table

Revision ID: 295ce2d876a0
Revises: 09cc73b310d8
Create Date: 2026-09-21 13:11:04.636035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "295ce2d876a0"
down_revision: Union[str, Sequence[str], None] = "09cc73b310d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "deployments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("build_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("version", sa.String(length=100), nullable=False),
        sa.Column("environment", sa.String(length=100), nullable=False),
        sa.Column("target", sa.String(length=200), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=True),
        sa.Column("logs", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_deployments_organization_id_organizations",
        ),
        sa.ForeignKeyConstraint(
            ["build_id"],
            ["builds.id"],
            name="fk_deployments_build_id_builds",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_deployments_build_id"),
        "deployments",
        ["build_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_deployments_organization_id"),
        "deployments",
        ["organization_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f("ix_deployments_organization_id"),
        table_name="deployments",
    )
    op.drop_index(
        op.f("ix_deployments_build_id"),
        table_name="deployments",
    )
    op.drop_table("deployments")