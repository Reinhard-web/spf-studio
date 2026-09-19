from alembic import op
import sqlalchemy as sa


revision = "7f1f57d124a9"
down_revision = "27846292ccfe"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "experiments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("idea_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("hypothesis", sa.Text(), nullable=False),
        sa.Column("uncertainty", sa.Text(), nullable=True),
        sa.Column("assumptions", sa.Text(), nullable=True),
        sa.Column("methodology", sa.Text(), nullable=False),
        sa.Column("success_criteria", sa.Text(), nullable=False),
        sa.Column("failure_criteria", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("outcome", sa.String(length=50), nullable=True),
        sa.Column("results", sa.Text(), nullable=True),
        sa.Column("learning", sa.Text(), nullable=True),
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
        ),
        sa.ForeignKeyConstraint(
            ["idea_id"],
            ["ideas.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_experiments_organization_id",
        "experiments",
        ["organization_id"],
    )

    op.create_index(
        "ix_experiments_idea_id",
        "experiments",
        ["idea_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_experiments_idea_id",
        table_name="experiments",
    )
    op.drop_index(
        "ix_experiments_organization_id",
        table_name="experiments",
    )
    op.drop_table("experiments")