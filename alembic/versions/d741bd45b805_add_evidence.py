from alembic import op
import sqlalchemy as sa


revision = "d741bd45b805"
down_revision = "7f1f57d124a9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "evidence",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("experiment_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("evidence_type", sa.String(length=50), nullable=False),
        sa.Column("source_type", sa.String(length=100), nullable=True),
        sa.Column("source_reference", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=True),
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
            ["experiment_id"],
            ["experiments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_evidence_organization_id",
        "evidence",
        ["organization_id"],
    )

    op.create_index(
        "ix_evidence_experiment_id",
        "evidence",
        ["experiment_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_evidence_experiment_id",
        table_name="evidence",
    )
    op.drop_index(
        "ix_evidence_organization_id",
        table_name="evidence",
    )
    op.drop_table("evidence")