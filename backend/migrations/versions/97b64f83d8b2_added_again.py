"""added-again

Revision ID: 97b64f83d8b2
Revises: 275a340ace61
Create Date: 2024-01-23 15:30:41.429258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '97b64f83d8b2'
down_revision: Union[str, None] = '275a340ace61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_foreign_key(None, 'RISset_defense', 'RISClass', ['class_id'], ['id'])



def downgrade() -> None:

    op.drop_constraint(None, 'RISset_defense', type_='foreignkey')