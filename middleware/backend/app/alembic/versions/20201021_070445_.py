"""empty message

Revision ID: 20201021_070445
Revises: 20201021_065048
Create Date: 2020-10-21 07:04:45.710116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201021_070445'
down_revision = '20201021_065048'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix___crypto_ohlc_daily_id', table_name='__crypto_ohlc_daily')
    op.drop_index('ix___topic_id', table_name='__topic')
    op.drop_index('ix_case_node_id', table_name='case_node')
    op.drop_index('ix_executor_id', table_name='executor')
    op.drop_index('ix_executor_job_id', table_name='executor_job')
    op.drop_index('ix_keywords_id', table_name='keywords')
    op.drop_index('ix_target_id', table_name='target')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_target_id', 'target', ['id'], unique=False)
    op.create_index('ix_keywords_id', 'keywords', ['id'], unique=False)
    op.create_index('ix_executor_job_id', 'executor_job', ['id'], unique=False)
    op.create_index('ix_executor_id', 'executor', ['id'], unique=False)
    op.create_index('ix_case_node_id', 'case_node', ['id'], unique=False)
    op.create_index('ix___topic_id', '__topic', ['id'], unique=False)
    op.create_index('ix___crypto_ohlc_daily_id', '__crypto_ohlc_daily', ['id'], unique=False)
    # ### end Alembic commands ###
