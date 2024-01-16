"""faculty_paper

Revision ID: 863d7b3efa62
Revises: 7cd6889c9f80
Create Date: 2024-01-16 22:32:29.043960

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '863d7b3efa62'
down_revision: Union[str, None] = '7cd6889c9f80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('RISfaculty_research_papers', sa.Column('category', sqlmodel.sql.sqltypes.AutoString(), nullable=False))


def downgrade() -> None:

    op.drop_column('RISfaculty_research_papers', 'category')