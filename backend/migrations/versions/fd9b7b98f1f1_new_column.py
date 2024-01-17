"""new column

Revision ID: fd9b7b98f1f1
Revises: 863d7b3efa62
Create Date: 2024-01-18 00:10:27.165265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'fd9b7b98f1f1'
down_revision: Union[str, None] = '863d7b3efa62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('RISfaculty_research_papers', sa.Column('publisher', sqlmodel.sql.sqltypes.AutoString(), nullable=False))



def downgrade() -> None:

    op.drop_column('RISfaculty_research_papers', 'publisher')