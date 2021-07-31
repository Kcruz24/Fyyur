"""empty message

Revision ID: 40c03cf9c8c0
Revises: 4496f2fa70ff
Create Date: 2021-07-30 00:24:38.028407

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '40c03cf9c8c0'
down_revision = '4496f2fa70ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'start_time',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('show', 'start_time',
                    existing_type=postgresql.TIMESTAMP(),
                    nullable=True)
    # ### end Alembic commands ###
