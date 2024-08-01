import sqlalchemy as sa
from alembic import op

from sos_trades_api.server.base_server import db

"""add error management on study object

Revision ID: 35ba4ee9fc53
Revises: b4c65e383551
Create Date: 2021-12-01 15:35:13.637919

"""

# revision identifiers, used by Alembic.
revision = "35ba4ee9fc53"
down_revision = "b4c65e383551"
branch_labels = None
depends_on = None


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.add_column("study_case", sa.Column("error", sa.Text(), nullable=True))
        op.add_column("study_case", sa.Column("disabled", sa.Boolean(), nullable=False))

        db.session.commit()
        # ### end Alembic commands ###
    except Exception as exc:
        db.session.rollback()
        raise exc

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("study_case", "error")
    op.drop_column("study_case", "disabled")
    # ### end Alembic commands ###
