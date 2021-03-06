"""empty message

Revision ID: 1e2869a009a1
Revises: 1049189fa2f3
Create Date: 2020-08-30 10:05:16.623775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1e2869a009a1'
down_revision = '1049189fa2f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingester',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pipeline', sa.String(length=255), nullable=True),
    sa.Column('crawler_name', sa.String(length=255), nullable=True),
    sa.Column('keyword', sa.String(length=255), nullable=True),
    sa.Column('option_keywords', sa.String(length=1023), nullable=True),
    sa.Column('deps', sa.Integer(), nullable=False),
    sa.Column('referer', sa.String(length=1023), nullable=True),
    sa.Column('url', sa.String(length=1023), nullable=True),
    sa.Column('url_cache', sa.String(length=1023), nullable=True),
    sa.Column('title', sa.String(length=1023), nullable=True),
    sa.Column('summary', sa.String(length=1023), nullable=True),
    sa.Column('current_page_num', sa.Integer(), nullable=False),
    sa.Column('detail', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ingester_id'), 'ingester', ['id'], unique=False)
    op.drop_index('ix_index_queue_id', table_name='index_queue')
    op.drop_table('index_queue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('index_queue',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('pipeline', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('crawler_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('keyword', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.Column('option_keywords', sa.VARCHAR(length=1023), autoincrement=False, nullable=True),
    sa.Column('deps', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('referer', sa.VARCHAR(length=1023), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(length=1023), autoincrement=False, nullable=True),
    sa.Column('url_cache', sa.VARCHAR(length=1023), autoincrement=False, nullable=True),
    sa.Column('title', sa.VARCHAR(length=1023), autoincrement=False, nullable=True),
    sa.Column('summary', sa.VARCHAR(length=1023), autoincrement=False, nullable=True),
    sa.Column('current_page_num', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('detail', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='index_queue_pkey')
    )
    op.create_index('ix_index_queue_id', 'index_queue', ['id'], unique=False)
    op.drop_index(op.f('ix_ingester_id'), table_name='ingester')
    op.drop_table('ingester')
    # ### end Alembic commands ###
