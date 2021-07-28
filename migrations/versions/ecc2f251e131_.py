"""empty message

Revision ID: ecc2f251e131
Revises: 89ae4c0331ec
Create Date: 2021-07-27 17:11:04.042979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecc2f251e131'
down_revision = '89ae4c0331ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'seeking_venues')
    op.drop_column('venue', 'seeking_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('seeking_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('artist', sa.Column('seeking_venues', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###