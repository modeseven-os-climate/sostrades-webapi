'''
Copyright 2022 Airbus SAS
Modifications on 2024/06/07 Copyright 2024 Capgemini
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

'''
import sqlalchemy as sa
from alembic import op

"""Add study case logging table

Revision ID: d341b6f43c5b
Revises: ead421cc5deb
Create Date: 2022-07-26 11:07:28.253405

"""
# revision identifiers, used by Alembic.
revision = "d341b6f43c5b"
down_revision = "ead421cc5deb"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('study_case_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('study_case_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('log_level_name', sa.String(length=64), nullable=True),
    sa.Column('created', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('exception', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['study_case_id'], ['study_case.id'], name='fk_study_case_log_study_case_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("study_case_log")
    # ### end Alembic commands ###
