"""empty message

Revision ID: fea9d35609b1
Revises: 30a810b9474a
Create Date: 2022-08-13 10:11:17.414551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fea9d35609b1'
down_revision = '30a810b9474a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('web_link', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'web_link')
    # ### end Alembic commands ###
