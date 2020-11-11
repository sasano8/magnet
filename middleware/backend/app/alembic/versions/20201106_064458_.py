"""empty message

Revision ID: 20201106_064458
Revises: 20201028_201320
Create Date: 2020-11-06 06:44:58.777290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201106_064458'
down_revision = '20201028_201320'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_job', sa.Column('order_status', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_job', 'order_status')
    # ### end Alembic commands ###
