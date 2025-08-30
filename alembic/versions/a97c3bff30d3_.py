"""empty message

Revision ID: a97c3bff30d3
Revises: 
Create Date: 2025-08-30 21:25:26.369223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a97c3bff30d3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('createdAt', sa.DateTime, nullable=False ),
        sa.Column('updatedAt', sa.DateTime, nullable=True),
        sa.Column('isPrivate', sa.Boolean, default=False)
    )


def downgrade() -> None:
    op.drop_table('users')
