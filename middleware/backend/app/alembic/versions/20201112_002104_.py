"""empty message

Revision ID: 20201112_002104
Revises: 20201112_002032
Create Date: 2020-11-12 00:21:05.334646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201112_002104'
down_revision = '20201112_002032'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_job', sa.Column('order_logic', sa.JSON(), nullable=True))
    op.add_column('trade_job', sa.Column('trade_rule', sa.JSON(), nullable=True))
    op.add_column('trade_profile', sa.Column('order_logic', sa.JSON(), nullable=True))
    op.add_column('trade_profile', sa.Column('trade_rule', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_profile', 'trade_rule')
    op.drop_column('trade_profile', 'order_logic')
    op.drop_column('trade_job', 'trade_rule')
    op.drop_column('trade_job', 'order_logic')
    # ### end Alembic commands ###
