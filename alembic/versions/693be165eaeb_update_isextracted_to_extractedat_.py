"""Update isExtracted to extractedAt, converted to datetime, to capture when extractation did happend

Revision ID: 693be165eaeb
Revises: 9a7cf47454a6
Create Date: 2025-09-07 00:23:03.322232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '693be165eaeb'
down_revision: Union[str, None] = '9a7cf47454a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1) Add the new column (nullable to allow backfill)
    op.add_column(
        'users',
        sa.Column('extractedAt', postgresql.TIMESTAMP(timezone=True), nullable=True)
    )

    # 2) Backfill: where the old flag was true, set extractedAt to NOW()
    # Adjust this logic if you have a better timestamp source
    op.execute(
        "UPDATE users SET \"extractedAt\" = NOW() WHERE \"isExtracted\" = TRUE"
    )

    # 3) Drop the old column
    op.drop_column('users', 'isExtracted')

def downgrade():
    # 1) Recreate the old column, default false
    op.add_column(
        'users',
        sa.Column('isExtracted', sa.Boolean(), server_default=sa.text('false'), nullable=False)
    )

    # 2) Backfill the flag from extractedAt
    op.execute(
        "UPDATE users SET \"isExtracted\" = TRUE WHERE \"extractedAt\" IS NOT NULL"
    )

    # 3) Drop the new column
    op.drop_column('users', 'extractedAt')

