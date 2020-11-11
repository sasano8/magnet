"""empty message

Revision ID: 20201110_090058
Revises: 20201110_072326
Create Date: 2020-11-10 09:00:59.111523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201110_090058'
down_revision = '20201110_072326'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_job', sa.Column('version', sa.Integer(), nullable=True))
    op.add_column('trade_profile', sa.Column('version', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_profile', 'version')
    op.drop_column('trade_job', 'version')
    # ### end Alembic commands ###
