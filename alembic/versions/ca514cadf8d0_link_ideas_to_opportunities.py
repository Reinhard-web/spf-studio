"""link ideas to opportunities

Revision ID: ca514cadf8d0
Revises: 4fcd539f7c5d
Create Date: 2026-09-16 14:36:53.347879

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ca514cadf8d0"
down_revision: Union[str, Sequence[str], None] = "4fcd539f7c5d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "ideas",
        sa.Column("opportunity_id", sa.Integer(), nullable=True),
    )

    op.create_index(
        "ix_ideas_opportunity_id",
        "ideas",
        ["opportunity_id"],
    )

    op.create_foreign_key(
        "fk_ideas_opportunity_id",
        "ideas",
        "opportunities",
        ["opportunity_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_ideas_opportunity_id",
        "ideas",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_ideas_opportunity_id",
        table_name="ideas",
    )

    op.drop_column(
        "ideas",
        "opportunity_id",
    )