from alembic import op
import sqlalchemy as sa


revision = "27846292ccfe"
down_revision = "1ab1cc99217f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "problem_opportunities",
        sa.Column("problem_id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problems.id"],
        ),
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["opportunities.id"],
        ),
        sa.PrimaryKeyConstraint(
            "problem_id",
            "opportunity_id",
        ),
    )

    op.create_index(
        "ix_problem_opportunities_problem_id",
        "problem_opportunities",
        ["problem_id"],
    )

    op.create_index(
        "ix_problem_opportunities_opportunity_id",
        "problem_opportunities",
        ["opportunity_id"],
    )

    op.create_table(
        "opportunity_ideas",
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("idea_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["opportunity_id"],
            ["opportunities.id"],
        ),
        sa.ForeignKeyConstraint(
            ["idea_id"],
            ["ideas.id"],
        ),
        sa.PrimaryKeyConstraint(
            "opportunity_id",
            "idea_id",
        ),
    )

    op.create_index(
        "ix_opportunity_ideas_opportunity_id",
        "opportunity_ideas",
        ["opportunity_id"],
    )

    op.create_index(
        "ix_opportunity_ideas_idea_id",
        "opportunity_ideas",
        ["idea_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_opportunity_ideas_idea_id",
        table_name="opportunity_ideas",
    )
    op.drop_index(
        "ix_opportunity_ideas_opportunity_id",
        table_name="opportunity_ideas",
    )
    op.drop_table("opportunity_ideas")

    op.drop_index(
        "ix_problem_opportunities_opportunity_id",
        table_name="problem_opportunities",
    )
    op.drop_index(
        "ix_problem_opportunities_problem_id",
        table_name="problem_opportunities",
    )
    op.drop_table("problem_opportunities")