"""hello

Revision ID: 379e50754390
Revises: 93955d0b100f
Create Date: 2024-01-24 06:40:29.559324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = '379e50754390'
down_revision: Union[str, None] = '93955d0b100f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('RISset_defense', sa.Column('class_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_foreign_key(None, 'RISset_defense', 'RISClass', ['class_id'], ['id'])
    

def downgrade() -> None:
    
    
    op.drop_constraint(None, 'RISset_defense', type_='foreignkey')
    op.drop_column('RISset_defense', 'class_id')
    
    
   
    
    op.create_table('RISset_defense_class',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('class_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('set_defense_id', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['RISClass.id'], name='RISset_defense_class_class_id_fkey'),
    sa.ForeignKeyConstraint(['set_defense_id'], ['RISset_defense.id'], name='RISset_defense_class_set_defense_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='RISset_defense_class_pkey')
    )
    
    
    