"""empty message

Revision ID: 20201110_220510
Revises: 20201110_091345
Create Date: 2020-11-10 22:05:11.353836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201110_220510'
down_revision = '20201110_091345'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_job', sa.Column('job_type', sa.String(length=255), nullable=True))
    op.add_column('trade_profile', sa.Column('job_type', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_profile', 'job_type')
    op.drop_column('trade_job', 'job_type')
    # ### end Alembic commands ###
