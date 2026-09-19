"""link products to ideas

Revision ID: fc9b7c183620
Revises: 81d914c36ced
Create Date: 2026-09-20 01:07:53.180959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fc9b7c183620"
down_revision: Union[str, Sequence[str], None] = "81d914c36ced"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "products",
        sa.Column("idea_id", sa.Integer(), nullable=True),
    )

    op.create_index(
        op.f("ix_products_idea_id"),
        "products",
        ["idea_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_products_idea_id_ideas",
        "products",
        "ideas",
        ["idea_id"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_products_idea_id_ideas",
        "products",
        type_="foreignkey",
    )

    op.drop_index(
        op.f("ix_products_idea_id"),
        table_name="products",
    )

    op.drop_column(
        "products",
        "idea_id",
    )