"""empty message

Revision ID: 20201021_002015
Revises: 20201021_002002
Create Date: 2020-10-21 00:20:16.341066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201021_002015'
down_revision = '20201021_002002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'trade_profile', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trade_profile', type_='unique')
    # ### end Alembic commands ###
