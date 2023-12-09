"""GHello?

Revision ID: dc02ab763efb
Revises: 2e5c45204596
Create Date: 2023-12-09 21:46:24.776155

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dc02ab763efb'
down_revision: Union[str, None] = '2e5c45204596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section_assigned_prof', sa.Column('research_type_prof_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_constraint('section_assigned_prof_user_id_fkey', 'section_assigned_prof', type_='foreignkey')
    op.create_foreign_key(None, 'section_assigned_prof', 'research_type_assigned_prof', ['research_type_prof_id'], ['id'])
    op.drop_column('section_assigned_prof', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section_assigned_prof', sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'section_assigned_prof', type_='foreignkey')
    op.create_foreign_key('section_assigned_prof_user_id_fkey', 'section_assigned_prof', 'users', ['user_id'], ['id'])
    op.drop_column('section_assigned_prof', 'research_type_prof_id')
    # ### end Alembic commands ###
