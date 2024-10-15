"""
increase size of reference path

Revision ID: fb0a1fde7fe0
Revises: bcc99700bfe4
Create Date: 2022-09-21 11:28:43.480706

"""
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "fb0a1fde7fe0"
down_revision = "bcc99700bfe4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("reference_study") as batch_op:
        batch_op.alter_column("reference_path",
                            existing_type=mysql.VARCHAR(length=128),
                            type_=mysql.VARCHAR(length=256),
                            existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("reference_study", "reference_path",
               existing_type=mysql.VARCHAR(length=256),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=True)
    # ### end Alembic commands ###
