"""change column

Revision ID: aef03963050c
Revises: b3ee0f0659fd
Create Date: 2024-01-22 15:40:55.001697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = 'aef03963050c'
down_revision: Union[str, None] = 'b3ee0f0659fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.alter_column('RISresearch_papers', 'extension',
               existing_type=sa.BOOLEAN(),
               type_=sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=True)
    op.drop_column('RISresearch_papers', 'extension_type')
  


def downgrade() -> None:

    op.add_column('RISresearch_papers', sa.Column('extension_type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('RISresearch_papers', 'extension',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
    
    