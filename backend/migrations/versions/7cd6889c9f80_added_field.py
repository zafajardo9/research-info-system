"""added field

Revision ID: 7cd6889c9f80
Revises: 605dc15935ce
Create Date: 2024-01-15 09:06:27.315550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7cd6889c9f80'
down_revision: Union[str, None] = '605dc15935ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('RISfaculty_research_papers', sa.Column('date_publish', sa.Date(), nullable=False))


def downgrade() -> None:
    op.drop_column('RISfaculty_research_papers', 'date_publish')
    
    
    