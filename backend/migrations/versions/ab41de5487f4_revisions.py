"""revisions

Revision ID: ab41de5487f4
Revises: ff80a93c0b06
Create Date: 2024-01-03 08:48:02.594508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ab41de5487f4'
down_revision: Union[str, None] = 'ff80a93c0b06'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workflow_class',
    sa.Column('workflow_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('class_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['class_id'], ['class.id'], ),
    sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id'], ),
    sa.PrimaryKeyConstraint('workflow_id', 'class_id')
    )
    op.drop_constraint('workflow_class_id_fkey', 'workflow', type_='foreignkey')
    op.drop_column('workflow', 'class_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workflow', sa.Column('class_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_foreign_key('workflow_class_id_fkey', 'workflow', 'class', ['class_id'], ['id'])
    op.drop_table('workflow_class')
    # ### end Alembic commands ###
