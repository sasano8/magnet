"""empty message

Revision ID: 20201014_191741
Revises: 20201014_190603
Create Date: 2020-10-14 19:17:42.352967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201014_191741'
down_revision = '20201014_190603'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_profile', sa.Column('order_id', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_profile', 'order_id')
    # ### end Alembic commands ###
