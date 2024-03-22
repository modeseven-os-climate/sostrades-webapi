"""add flavors in pod allocation

Revision ID: dda4d408a5e0
Revises: 5b6303f4ab8e
Create Date: 2024-03-21 11:08:52.739843

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dda4d408a5e0'
down_revision = '5b6303f4ab8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pod_allocation', sa.Column('flavor', sa.String(length=64), server_default='', nullable=True))
    op.drop_column('pod_allocation', 'cpu_requested')
    op.drop_column('pod_allocation', 'memory_requested')
    op.drop_column('pod_allocation', 'memory_usage')
    op.drop_column('pod_allocation', 'memory_limit')
    op.drop_column('pod_allocation', 'cpu_limit')
    op.drop_column('pod_allocation', 'cpu_usage')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pod_allocation', sa.Column('cpu_usage', mysql.VARCHAR(length=32), server_default=sa.text("'----'"), nullable=True))
    op.add_column('pod_allocation', sa.Column('cpu_limit', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('pod_allocation', sa.Column('memory_limit', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('pod_allocation', sa.Column('memory_usage', mysql.VARCHAR(length=32), server_default=sa.text("'----'"), nullable=True))
    op.add_column('pod_allocation', sa.Column('memory_requested', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('pod_allocation', sa.Column('cpu_requested', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('pod_allocation', 'flavor')
    # ### end Alembic commands ###
