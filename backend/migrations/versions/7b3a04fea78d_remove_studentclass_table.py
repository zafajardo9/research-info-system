"""remove studentclass table

Revision ID: 7b3a04fea78d
Revises: 23e5e4b34daa
Create Date: 2023-12-26 20:55:27.043911

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '7b3a04fea78d'
down_revision: Union[str, None] = '23e5e4b34daa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_class')
    op.add_column('student', sa.Column('class_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.create_foreign_key(None, 'student', 'class', ['class_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'student', type_='foreignkey')
    op.drop_column('student', 'class_id')
    op.create_table('student_class',
    sa.Column('student_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('class_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], name='student_class_class_id_fkey'),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], name='student_class_student_id_fkey'),
    sa.PrimaryKeyConstraint('student_id', 'class_id', name='student_class_pkey')
    )
    # ### end Alembic commands ###
