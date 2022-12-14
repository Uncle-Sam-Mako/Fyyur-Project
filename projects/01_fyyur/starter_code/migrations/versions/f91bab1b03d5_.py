"""empty message

Revision ID: f91bab1b03d5
Revises: 503a1aae4dfb
Create Date: 2022-08-13 20:43:18.084736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f91bab1b03d5'
down_revision = '503a1aae4dfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website_link', sa.String(), nullable=False))
    op.drop_column('Artist', 'web_link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('web_link', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('Artist', 'website_link')
    # ### end Alembic commands ###
