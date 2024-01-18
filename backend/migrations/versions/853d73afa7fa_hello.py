"""Hello

Revision ID: 853d73afa7fa
Revises: fd9b7b98f1f1
Create Date: 2024-01-18 10:36:56.659580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '853d73afa7fa'
down_revision: Union[str, None] = 'fd9b7b98f1f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_foreign_key(None, 'RISUsers', 'SPSStudent', ['student_id'], ['StudentId'])


def downgrade() -> None:

    op.drop_constraint(None, 'RISUsers', type_='foreignkey')