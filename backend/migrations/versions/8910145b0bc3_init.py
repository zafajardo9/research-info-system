"""Init

Revision ID: 8910145b0bc3
Revises: 
Create Date: 2023-11-23 19:15:26.097687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '8910145b0bc3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faculty',
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birth', sa.Date(), nullable=False),
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('research_papers',
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('research_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('submitted_date', sa.Date(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('file_path', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('research_adviser', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student',
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('birth', sa.Date(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('section', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('course', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('student_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ethics',
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('research_paper_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('letter_of_intent', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('urec_9', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('urec_10', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('urec_11', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('urec_12', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('certificate_of_validation', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('co_authorship', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['research_paper_id'], ['research_papers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('student_number', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('student_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('faculty_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('roles', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['faculty_id'], ['faculty.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('authors',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('research_paper_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['research_paper_id'], ['research_papers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('modified_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('research_paper_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['research_paper_id'], ['research_papers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('authors')
    op.drop_table('users')
    op.drop_table('ethics')
    op.drop_table('student')
    op.drop_table('research_papers')
    op.drop_table('faculty')
    # ### end Alembic commands ###