"""empty message

Revision ID: 94a80e30f633
Revises: 4d6ea11a90d4
Create Date: 2022-08-14 00:21:46.248260

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '94a80e30f633'
down_revision = '4d6ea11a90d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'start_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('start_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
