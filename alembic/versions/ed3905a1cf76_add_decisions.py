from alembic import op
import sqlalchemy as sa


revision = "ed3905a1cf76"
down_revision = "256ab5e19c1c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "decisions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=True),
        sa.Column("opportunity_id", sa.Integer(), nullable=True),
        sa.Column("idea_id", sa.Integer(), nullable=True),
        sa.Column("experiment_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("decision", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("decided_by", sa.String(length=100), nullable=True),
        sa.Column(
            "decided_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
        ),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problems.id"],
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["opportunities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["idea_id"],
            ["ideas.id"],
        ),
        sa.ForeignKeyConstraint(
            ["experiment_id"],
            ["experiments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_decisions_organization_id",
        "decisions",
        ["organization_id"],
    )

    op.create_index(
        "ix_decisions_problem_id",
        "decisions",
        ["problem_id"],
    )

    op.create_index(
        "ix_decisions_opportunity_id",
        "decisions",
        ["opportunity_id"],
    )

    op.create_index(
        "ix_decisions_idea_id",
        "decisions",
        ["idea_id"],
    )

    op.create_index(
        "ix_decisions_experiment_id",
        "decisions",
        ["experiment_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_decisions_experiment_id",
        table_name="decisions",
    )
    op.drop_index(
        "ix_decisions_idea_id",
        table_name="decisions",
    )
    op.drop_index(
        "ix_decisions_opportunity_id",
        table_name="decisions",
    )
    op.drop_index(
        "ix_decisions_problem_id",
        table_name="decisions",
    )
    op.drop_index(
        "ix_decisions_organization_id",
        table_name="decisions",
    )
    op.drop_table("decisions")