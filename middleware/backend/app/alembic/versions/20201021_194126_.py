"""empty message

Revision ID: 20201021_194126
Revises: 20201021_190653
Create Date: 2020-10-21 19:41:26.619798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201021_194126'
down_revision = '20201021_190653'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table_comment(
        '__crypto_ohlc_daily',
        '外部データソースから取得したチャート',
        existing_comment=None,
        schema=None
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table_comment(
        '__crypto_ohlc_daily',
        existing_comment='外部データソースから取得したチャート',
        schema=None
    )
    # ### end Alembic commands ###
