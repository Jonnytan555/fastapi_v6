"""add content column to posts table

Revision ID: 1366c95b72b3
Revises: 1755adb2e26d
Create Date: 2025-11-07 11:33:19.175995

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1366c95b72b3'
down_revision: Union[str, Sequence[str], None] = '1755adb2e26d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
