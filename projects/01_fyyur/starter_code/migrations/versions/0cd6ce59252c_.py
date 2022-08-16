"""empty message

Revision ID: 0cd6ce59252c
Revises: 332974334c95
Create Date: 2022-08-16 11:19:10.214197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cd6ce59252c'
down_revision = '332974334c95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###
