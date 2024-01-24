"""added

Revision ID: ef129dbb087e
Revises: 379e50754390
Create Date: 2024-01-24 17:43:14.072034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = 'ef129dbb087e'
down_revision: Union[str, None] = '379e50754390'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.drop_table('RISset_defense_class')

    op.add_column('RISfaculty_research_papers', sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    

def downgrade() -> None:

    op.drop_column('RISfaculty_research_papers', 'status')