"""empty message

Revision ID: 20201110_091145
Revises: 20201110_090851
Create Date: 2020-11-10 09:11:46.441631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20201110_091145'
down_revision = '20201110_090851'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trade_job', 'detector_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('trade_job', 'monitor_topic',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('trade_job', 'trade_type',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('trade_profile', 'detector_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('trade_profile', 'monitor_topic',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('trade_profile', 'trade_type',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('trade_profile', 'trade_type',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('trade_profile', 'monitor_topic',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('trade_profile', 'detector_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('trade_job', 'trade_type',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('trade_job', 'monitor_topic',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('trade_job', 'detector_name',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
