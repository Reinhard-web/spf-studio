from alembic import op
import sqlalchemy as sa


revision = "256ab5e19c1c"
down_revision = "d741bd45b805"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "learnings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("experiment_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("learning_type", sa.String(length=50), nullable=False),
        sa.Column("confidence", sa.String(length=50), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["experiment_id"],
            ["experiments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_learnings_organization_id",
        "learnings",
        ["organization_id"],
    )

    op.create_index(
        "ix_learnings_experiment_id",
        "learnings",
        ["experiment_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_learnings_experiment_id",
        table_name="learnings",
    )
    op.drop_index(
        "ix_learnings_organization_id",
        table_name="learnings",
    )
    op.drop_table("learnings")