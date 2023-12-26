"""edit column

Revision ID: 23e5e4b34daa
Revises: 4c48edc719fb
Create Date: 2023-12-26 16:59:45.645448

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '23e5e4b34daa'
down_revision: Union[str, None] = '4c48edc719fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('class', 'section',
               existing_type=sa.INTEGER(),
               type_= sqlmodel.sql.sqltypes.AutoString(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('class', 'section',
               existing_type=sqlmodel.sql.sqltypes.AutoString(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
