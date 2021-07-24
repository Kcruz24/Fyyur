"""Add associative table Show and complete model relationships

Revision ID: 85380696a127
Revises: 6280a9df5774
Create Date: 2021-07-23 19:21:57.659369

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '85380696a127'
down_revision = '6280a9df5774'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=False),
                    sa.Column('genres', sa.String(length=120), nullable=False),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=False),
                    sa.Column('website_link', sa.String(length=500), nullable=True),
                    sa.Column('looking_for_venues', sa.Boolean(), nullable=True),
                    sa.Column('seeking_description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('facebook_link'),
                    sa.UniqueConstraint('image_link'),
                    sa.UniqueConstraint('website_link')
                    )
    op.create_table('venue',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('city', sa.String(length=120), nullable=False),
                    sa.Column('state', sa.String(length=120), nullable=False),
                    sa.Column('address', sa.String(length=120), nullable=False),
                    sa.Column('phone', sa.String(length=120), nullable=False),
                    sa.Column('genres', sa.String(length=120), nullable=False),
                    sa.Column('facebook_link', sa.String(length=120), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=False),
                    sa.Column('website_link', sa.String(length=500), nullable=False),
                    sa.Column('looking_for_talent', sa.Boolean(), nullable=True),
                    sa.Column('seeking_description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('facebook_link'),
                    sa.UniqueConstraint('image_link'),
                    sa.UniqueConstraint('website_link')
                    )
    op.create_table('Show',
                    sa.Column('venue_pk_fk', sa.Integer(), nullable=False),
                    sa.Column('artist_pk_fk', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_pk_fk'], ['artist.id'], ),
                    sa.ForeignKeyConstraint(['venue_pk_fk'], ['venue.id'], ),
                    sa.PrimaryKeyConstraint('venue_pk_fk', 'artist_pk_fk')
                    )
    op.drop_table('Venue')
    op.drop_table('Artist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Artist_id_seq"\'::regclass)'),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
                    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
                    sa.Column('website_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
                    sa.Column('looking_for_venues', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('seeking_description', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='Artist_pkey'),
                    sa.UniqueConstraint('facebook_link', name='Artist_facebook_link_key'),
                    sa.UniqueConstraint('image_link', name='Artist_image_link_key'),
                    sa.UniqueConstraint('website_link', name='Artist_website_link_key')
                    )
    op.create_table('Venue',
                    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Venue_id_seq"\'::regclass)'),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
                    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
                    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
                    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
                    sa.Column('website_link', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
                    sa.Column('looking_for_talent', sa.BOOLEAN(), autoincrement=False, nullable=True),
                    sa.Column('seeking_description', sa.VARCHAR(), autoincrement=False, nullable=True),
                    sa.PrimaryKeyConstraint('id', name='Venue_pkey'),
                    sa.UniqueConstraint('facebook_link', name='Venue_facebook_link_key'),
                    sa.UniqueConstraint('image_link', name='Venue_image_link_key'),
                    sa.UniqueConstraint('website_link', name='Venue_website_link_key')
                    )
    op.drop_table('Show')
    op.drop_table('venue')
    op.drop_table('artist')
    # ### end Alembic commands ###
