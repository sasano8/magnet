"""empty message

Revision ID: 20201113_014939
Revises: 20201112_002104
Create Date: 2020-11-13 01:49:40.147602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201113_014939'
down_revision = '20201112_002104'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trade_job', sa.Column('bet_strategy', sa.String(length=255), nullable=True))
    op.add_column('trade_profile', sa.Column('bet_strategy', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trade_profile', 'bet_strategy')
    op.drop_column('trade_job', 'bet_strategy')
    # ### end Alembic commands ###
