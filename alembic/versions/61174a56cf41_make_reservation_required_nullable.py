"""make reservation required nullable

Revision ID: 61174a56cf41
Revises: b83f1c2d9a60
Create Date: 2026-11-21 20:34:22.830015

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61174a56cf41'
down_revision: Union[str, Sequence[str], None] = 'b83f1c2d9a60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Allow unknown official reservation policies."""

    op.alter_column(
        "courts",
        "reservation_required",
        existing_type=sa.Boolean(),
        nullable=True,
        server_default=None,
        existing_nullable=False,
    )


def downgrade() -> None:
    """Restore non-null policies; converts unknown values to FALSE."""

    op.execute(
        """
        UPDATE courts
        SET reservation_required = FALSE
        WHERE reservation_required IS NULL
        """
    )

    op.alter_column(
        "courts",
        "reservation_required",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text("false"),
        existing_nullable=True,
    )