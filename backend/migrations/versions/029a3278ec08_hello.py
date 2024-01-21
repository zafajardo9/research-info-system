"""Hello

Revision ID: 029a3278ec08
Revises: 853d73afa7fa
Create Date: 2024-01-21 13:24:51.304387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel
# revision identifiers, used by Alembic.
revision: str = '029a3278ec08'
down_revision: Union[str, None] = '853d73afa7fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column('RISannouncements', sa.Column('image', sqlmodel.sql.sqltypes.AutoString(), nullable=True))



def downgrade() -> None:

    op.drop_column('RISannouncements', 'image')