"""Initial database baseline

Revision ID: 8b8359822a43
Revises: 
Create Date: 2026-09-15 14:03:15.156210

"""
from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = '8b8359822a43'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
