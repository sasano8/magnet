"""empty message

Revision ID: 20201026_094051
Revises: 20201026_094002
Create Date: 2020-10-26 09:40:51.679802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201026_094051'
down_revision = '20201026_094002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('__crypto_ohlc_daily', sa.Column('close_time', sa.Date(), nullable=True))
    op.create_unique_constraint(None, '__crypto_ohlc_daily', ['provider', 'market', 'product', 'periods', 'close_time'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, '__crypto_ohlc_daily', type_='unique')
    op.drop_column('__crypto_ohlc_daily', 'close_time')
    # ### end Alembic commands ###
