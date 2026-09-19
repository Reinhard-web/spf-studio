"""add projects table

Revision ID: ba1ff61faf0e
Revises: fc9b7c183620
Create Date: 2026-09-20 01:30:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ba1ff61faf0e"
down_revision: Union[str, Sequence[str], None] = "fc9b7c183620"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("project_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("repository_url", sa.String(length=500), nullable=True),
        sa.Column("environment", sa.String(length=100), nullable=True),
        sa.Column("current_version", sa.String(length=100), nullable=True),
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
            name="fk_projects_organization_id_organizations",
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"],
            name="fk_projects_product_id_products",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_projects_organization_id"),
        "projects",
        ["organization_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_projects_product_id"),
        "projects",
        ["product_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_projects_slug"),
        "projects",
        ["slug"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_projects_slug"), table_name="projects")
    op.drop_index(op.f("ix_projects_product_id"), table_name="projects")
    op.drop_index(op.f("ix_projects_organization_id"), table_name="projects")

    op.drop_constraint(
        "fk_projects_product_id_products",
        "projects",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_projects_organization_id_organizations",
        "projects",
        type_="foreignkey",
    )

    op.drop_table("projects")