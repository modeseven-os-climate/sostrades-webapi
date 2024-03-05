"""add studycase creation status

Revision ID: 5acd0bb7bad9
Revises: 59ef3f9fbb52
Create Date: 2024-03-04 09:30:37.433245

"""
from alembic import op
import sqlalchemy as sa
from sos_trades_api.server.base_server import db
from sos_trades_api.models.database_models import StudyCase


# revision identifiers, used by Alembic.
revision = '5acd0bb7bad9'
down_revision = '59ef3f9fbb52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('study_case', sa.Column('creation_status', sa.String(length=64), nullable=True, server_default=StudyCase.CREATION_NOT_STARTED))
    op.add_column('study_case', sa.Column('reference', sa.String(length=64), nullable=True))
    op.add_column('study_case', sa.Column('from_type', sa.String(length=64), server_default='', nullable=True))
    # ### end Alembic commands ###
    db.session.commit()
        
    # Set the already existing studycase in db creation_status at DONE
    all_studies = StudyCase.query.all()
    for study in all_studies:
        study.creation_status = StudyCase.CREATION_DONE
    db.session.add_all(all_studies)
    db.session.commit()



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('study_case', 'from_type')
    op.drop_column('study_case', 'reference')
    op.drop_column('study_case', 'creation_status')
    # ### end Alembic commands ###
