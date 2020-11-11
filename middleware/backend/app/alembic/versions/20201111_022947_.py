"""empty message

Revision ID: 20201111_022947
Revises: 20201110_220510
Create Date: 2020-11-11 02:29:48.044127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201111_022947'
down_revision = '20201110_220510'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_job', sa.Column('last_check_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_job', 'last_check_date')
    # ### end Alembic commands ###