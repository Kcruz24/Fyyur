"""Fix column genres to be of type Array
Revision ID: 1b012daef5dc
Revises: cf83d31df06b
Create Date: 2021-07-28 13:21:21.727188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b012daef5dc'
down_revision = 'cf83d31df06b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('venue', sa.Column('genres', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'genres')
    op.drop_column('artist', 'genres')
    # ### end Alembic commands ###
