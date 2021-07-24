"""Add array column for genres and change looking_for_talent to seeking_talent

Revision ID: b9fd346a0eaf
Revises: e62899e10d03
Create Date: 2021-07-24 18:46:59.514796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9fd346a0eaf'
down_revision = 'e62899e10d03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('seeking_venues', sa.Boolean(), nullable=True))
    op.drop_column('artist', 'looking_for_venues')
    op.add_column('venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.drop_column('venue', 'looking_for_talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('looking_for_talent', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('venue', 'seeking_talent')
    op.add_column('artist', sa.Column('looking_for_venues', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('artist', 'seeking_venues')
    # ### end Alembic commands ###
