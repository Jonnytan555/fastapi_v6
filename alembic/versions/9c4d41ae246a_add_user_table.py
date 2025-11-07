"""add user table

Revision ID: 9c4d41ae246a
Revises: 1366c95b72b3
Create Date: 2025-11-07 11:37:59.790584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c4d41ae246a'
down_revision: Union[str, Sequence[str], None] = '1366c95b72b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', 
                  sa.Column('id', sa.Integer(), nullable=False),
                  sa.Column('email', sa.String(), nullable=False), # type: ignore
                  sa.Column('password', sa.String(), nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                  server_default=sa.text('now()'), nullable=False),
                  sa.PrimaryKeyConstraint('id'),
                  sa.UniqueConstraint('email')
                  )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
