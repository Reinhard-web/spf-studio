from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4fcd539f7c5d"
down_revision: Union[str, Sequence[str], None] = "ed3905a1cf76"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "decisions",
        sa.Column("learning_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "decisions",
        sa.Column("evidence_id", sa.Integer(), nullable=True),
    )

    op.create_foreign_key(
        "fk_decisions_learning_id",
        "decisions",
        "learnings",
        ["learning_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_decisions_evidence_id",
        "decisions",
        "evidence",
        ["evidence_id"],
        ["id"],
    )

    op.create_index(
        "ix_decisions_learning_id",
        "decisions",
        ["learning_id"],
    )

    op.create_index(
        "ix_decisions_evidence_id",
        "decisions",
        ["evidence_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_decisions_evidence_id",
        table_name="decisions",
    )

    op.drop_index(
        "ix_decisions_learning_id",
        table_name="decisions",
    )

    op.drop_constraint(
        "fk_decisions_evidence_id",
        "decisions",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_decisions_learning_id",
        "decisions",
        type_="foreignkey",
    )

    op.drop_column("decisions", "evidence_id")
    op.drop_column("decisions", "learning_id")