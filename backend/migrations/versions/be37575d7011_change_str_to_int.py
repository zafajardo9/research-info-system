"""change str to int

Revision ID: be37575d7011
Revises: 96b71376f35c
Create Date: 2023-12-19 23:44:43.534940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be37575d7011'
down_revision: Union[str, None] = '96b71376f35c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_navigation_role_id'), 'navigation_role', ['id'], unique=True)
    op.execute("ALTER TABLE workflow_steps ALTER COLUMN step_number TYPE INTEGER USING step_number::integer")


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('workflow_steps', 'step_number',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_index(op.f('ix_navigation_role_id'), table_name='navigation_role')
    # ### end Alembic commands ###
