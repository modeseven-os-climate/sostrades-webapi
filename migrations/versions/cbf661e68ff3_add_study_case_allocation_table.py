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

"""Add study case allocation table

Revision ID: cbf661e68ff3
Revises: d341b6f43c5b
Create Date: 2022-08-12 10:34:00.497218

"""
# revision identifiers, used by Alembic.
revision = "cbf661e68ff3"
down_revision = "d341b6f43c5b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("study_case_allocation",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=False),
    sa.Column("status", sa.String(length=64), server_default="", nullable=True),
    sa.Column("kubernetes_pod_name", sa.String(length=128), server_default="", nullable=True),
    sa.Column("message", sa.Text(), nullable=True),
    sa.Column("creation_date", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_allocation_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("kubernetes_pod_name"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_study_case_allocation_study_case_id"), "study_case_allocation", ["study_case_id"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_study_case_allocation_study_case_id"), table_name="study_case_allocation")
    op.drop_table("study_case_allocation")
    # ### end Alembic commands ###
