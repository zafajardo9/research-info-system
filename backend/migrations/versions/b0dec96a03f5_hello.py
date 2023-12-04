"""Hello

Revision ID: b0dec96a03f5
Revises: 4fad4633eba6
Create Date: 2023-11-28 17:02:22.605708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'b0dec96a03f5'
down_revision: Union[str, None] = '4fad4633eba6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('role', 'id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('workflow', sa.Column('type', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workflow', 'type')
    op.alter_column('role', 'id',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###