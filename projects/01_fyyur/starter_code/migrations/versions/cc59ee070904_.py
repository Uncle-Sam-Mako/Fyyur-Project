"""empty message

Revision ID: cc59ee070904
Revises: e1381aa6c684
Create Date: 2022-08-13 12:56:14.628037

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc59ee070904'
down_revision = 'e1381aa6c684'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artiste_venue',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id')
    )
    op.drop_table('tags')
    op.drop_column('Artist', 'sex')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('sex', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    op.create_table('tags',
    sa.Column('artist_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('venue_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], name='tags_artist_id_fkey'),
    sa.ForeignKeyConstraint(['venue_id'], ['Venue.id'], name='tags_venue_id_fkey'),
    sa.PrimaryKeyConstraint('artist_id', 'venue_id', name='tags_pkey')
    )
    op.drop_table('artiste_venue')
    # ### end Alembic commands ###