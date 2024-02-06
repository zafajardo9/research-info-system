"""added field

Revision ID: ab58ebbb4f9a
Revises: ef129dbb087e
Create Date: 2024-02-06 10:18:37.804769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = 'ab58ebbb4f9a'
down_revision: Union[str, None] = 'ef129dbb087e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('RISfaculty_research_papers', sa.Column('keywords', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    
    

def downgrade() -> None:

    op.drop_column('RISfaculty_research_papers', 'keywords')
    
    
    