"""add builds table

Revision ID: 12a7c6fd0355
Revises: ba1ff61faf0e
Create Date: 2026-09-20 01:49:19.282279
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "12a7c6fd0355"
down_revision: Union[str, Sequence[str], None] = "ba1ff61faf0e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "builds",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("version", sa.String(length=100), nullable=False),
        sa.Column("build_number", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("environment", sa.String(length=100), nullable=False),
        sa.Column("branch", sa.String(length=200), nullable=True),
        sa.Column("commit_sha", sa.String(length=100), nullable=True),
        sa.Column("preview_url", sa.String(length=500), nullable=True),
        sa.Column("logs", sa.Text(), nullable=True),
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
            name="fk_builds_organization_id_organizations",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="fk_builds_project_id_projects",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_builds_organization_id"),
        "builds",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_builds_project_id"),
        "builds",
        ["project_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_builds_project_id"), table_name="builds")
    op.drop_index(op.f("ix_builds_organization_id"), table_name="builds")

    op.drop_constraint(
        "fk_builds_project_id_projects",
        "builds",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_builds_organization_id_organizations",
        "builds",
        type_="foreignkey",
    )

    op.drop_table("builds")