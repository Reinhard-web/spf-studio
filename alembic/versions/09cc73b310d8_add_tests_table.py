"""add tests table

Revision ID: 09cc73b310d8
Revises: 12a7c6fd0355
Create Date: 2026-09-20 02:03:08.728480
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "09cc73b310d8"
down_revision: Union[str, Sequence[str], None] = "12a7c6fd0355"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("build_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("test_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("environment", sa.String(length=100), nullable=False),
        sa.Column("command", sa.Text(), nullable=True),
        sa.Column("results", sa.Text(), nullable=True),
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
            name="fk_tests_organization_id_organizations",
        ),
        sa.ForeignKeyConstraint(
            ["build_id"],
            ["builds.id"],
            name="fk_tests_build_id_builds",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_tests_organization_id"),
        "tests",
        ["organization_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_tests_build_id"),
        "tests",
        ["build_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_tests_build_id"),
        table_name="tests",
    )

    op.drop_index(
        op.f("ix_tests_organization_id"),
        table_name="tests",
    )

    op.drop_constraint(
        "fk_tests_build_id_builds",
        "tests",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_tests_organization_id_organizations",
        "tests",
        type_="foreignkey",
    )

    op.drop_table("tests")