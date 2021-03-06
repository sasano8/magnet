"""empty message

Revision ID: 20200924_104512
Revises: 20200910_020631
Create Date: 2020-09-24 10:45:12.579936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20200924_104512'
down_revision = '20200910_020631'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('crypto_ohlc_daily',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('market', sa.String(length=255), nullable=False),
    sa.Column('product', sa.String(length=255), nullable=False),
    sa.Column('close_time', sa.DateTime(), nullable=False),
    sa.Column('open_price', sa.Float(), nullable=False),
    sa.Column('high_price', sa.Float(), nullable=False),
    sa.Column('low_price', sa.Float(), nullable=False),
    sa.Column('close_price', sa.Float(), nullable=False),
    sa.Column('volume', sa.Float(), nullable=False),
    sa.Column('quote_volume', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_crypto_ohlc_daily_id'), 'crypto_ohlc_daily', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_crypto_ohlc_daily_id'), table_name='crypto_ohlc_daily')
    op.drop_table('crypto_ohlc_daily')
    # ### end Alembic commands ###
