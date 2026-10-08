"""Create snapshot-url column

Revision ID: 1debb4a94a11
Revises: 
Create Date: 2026-10-07 13:53:34.069200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1debb4a94a11'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("canvases", sa.Column('thumnail_url', sa.String(255), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("canvases", "thumbnail_url")
