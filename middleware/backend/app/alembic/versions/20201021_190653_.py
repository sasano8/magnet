"""empty message

Revision ID: 20201021_190653
Revises: 20201021_070445
Create Date: 2020-10-21 19:06:54.280990

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20201021_190653'
down_revision = '20201021_070445'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('__crypto_ohlc_daily', 't_cross',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               comment='1=golden cross -1=dead cross',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('__crypto_ohlc_daily', 't_cross',
               existing_type=postgresql.DOUBLE_PRECISION(precision=53),
               comment=None,
               existing_comment='1=golden cross -1=dead cross',
               existing_nullable=False)
    # ### end Alembic commands ###
