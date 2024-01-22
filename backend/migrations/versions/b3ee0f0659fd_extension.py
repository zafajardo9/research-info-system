"""extension

Revision ID: b3ee0f0659fd
Revises: 029a3278ec08
Create Date: 2024-01-22 12:41:18.264049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = 'b3ee0f0659fd'
down_revision: Union[str, None] = '029a3278ec08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    
    
    op.add_column('RISresearch_papers', sa.Column('extension', sa.Boolean(), nullable=True))
    op.add_column('RISresearch_papers', sa.Column('extension_type', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    


def downgrade() -> None:

    op.drop_column('RISresearch_papers', 'extension_type')
    op.drop_column('RISresearch_papers', 'extension')