"""halo

Revision ID: 93955d0b100f
Revises: 97b64f83d8b2
Create Date: 2024-01-23 15:58:14.346973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '93955d0b100f'
down_revision: Union[str, None] = '97b64f83d8b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RISset_defense_class',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('class_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('set_defense_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['RISClass.id'], ),
    sa.ForeignKeyConstraint(['set_defense_id'], ['RISset_defense.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    
    op.drop_constraint('RISset_defense_class_id_fkey', 'RISset_defense', type_='foreignkey')
    op.drop_column('RISset_defense', 'class_id')
    



def downgrade() -> None:
    
    op.add_column('RISset_defense', sa.Column('class_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('RISset_defense_class_id_fkey', 'RISset_defense', 'RISClass', ['class_id'], ['id'])
    # ### end Alembic commands ###
