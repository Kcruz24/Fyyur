"""empty message

Revision ID: e5e36670bd59
Revises: ecc2f251e131
Create Date: 2021-07-27 17:11:23.838659

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5e36670bd59'
down_revision = 'ecc2f251e131'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venues', sa.Boolean(), nullable=True))
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'seeking_talent')
    op.drop_column('artist', 'seeking_venues')
    # ### end Alembic commands ###
