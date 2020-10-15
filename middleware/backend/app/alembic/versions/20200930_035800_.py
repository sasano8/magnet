"""empty message

Revision ID: 20200930_035800
Revises: 20200930_032001
Create Date: 2020-09-30 03:58:01.013879

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20200930_035800'
down_revision = '20200930_032001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('__crypto_ohlc_daily', sa.Column('t_cross', sa.Float(), nullable=True, default=0))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('__crypto_ohlc_daily', 't_cross')
    # ### end Alembic commands ###