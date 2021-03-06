"""empty message

Revision ID: 22356aca97da
Revises: a0e32b898309
Create Date: 2020-07-02 23:28:43.782650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22356aca97da'
down_revision = 'a0e32b898309'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('case_node',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('is_system', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_node_id'), 'case_node', ['id'], unique=False)
    op.create_table('target',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('node_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['case_node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_target_id'), 'target', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_target_id'), table_name='target')
    op.drop_table('target')
    op.drop_index(op.f('ix_case_node_id'), table_name='case_node')
    op.drop_table('case_node')
    # ### end Alembic commands ###
