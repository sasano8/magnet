"""empty message

Revision ID: 20201021_002319
Revises: 20201021_002015
Create Date: 2020-10-21 00:23:19.622443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201021_002319'
down_revision = '20201021_002015'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('trade_job_name_key', 'trade_job', type_='unique')
    op.drop_constraint('trade_profile_name_key', 'trade_profile', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('trade_profile_name_key', 'trade_profile', ['name'])
    op.create_unique_constraint('trade_job_name_key', 'trade_job', ['name'])
    # ### end Alembic commands ###
