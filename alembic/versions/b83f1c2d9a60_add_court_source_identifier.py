"""Add stable source identifier to court_sources.

Revision ID: b83f1c2d9a60
Revises: 70a0a04f5a58
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b83f1c2d9a60"
down_revision: Union[str, Sequence[str], None] = "70a0a04f5a58"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add nullable source identity without modifying existing records."""
    op.add_column(
        "court_sources",
        sa.Column("source_identifier", sa.String(length=200), nullable=True),
    )
    op.create_unique_constraint(
        "uq_court_sources_source_identity",
        "court_sources",
        ["source_name", "source_identifier"],
    )


def downgrade() -> None:
    """Remove source identity (destructive for populated identifiers)."""
    op.drop_constraint(
        "uq_court_sources_source_identity",
        "court_sources",
        type_="unique",
    )
    op.drop_column("court_sources", "source_identifier")