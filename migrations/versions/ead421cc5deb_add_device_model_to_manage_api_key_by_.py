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

"""Add device model to manage api-key by group

Revision ID: ead421cc5deb
Revises: 23659f27ce8a
Create Date: 2022-05-18 16:34:06.326494

"""
# revision identifiers, used by Alembic.
revision = "ead421cc5deb"
down_revision = "23659f27ce8a"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("device",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("device_name", sa.String(length=80), nullable=True),
    sa.Column("device_key", sa.String(length=80), server_default="8536f2e37df1459493258c513477adc2", nullable=True),
    sa.Column("group_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["group.id"], name="fk_device_group_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("device")
    # ### end Alembic commands ###
