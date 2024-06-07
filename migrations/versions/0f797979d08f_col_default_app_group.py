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

from sos_trades_api.models.database_models import Group
from sos_trades_api.server.base_server import db

"""col_default_app_group

Revision ID: 0f797979d08f
Revises: 89b66a62d3a7
Create Date: 2022-02-14 16:53:50.917357

"""

# revision identifiers, used by Alembic.
revision = "0f797979d08f"
down_revision = "89b66a62d3a7"
branch_labels = None
depends_on = None


def upgrade():
    try:
        # ### commands auto generated by Alembic - please adjust! ###
        op.add_column("group", sa.Column("is_default_applicative_group", sa.Boolean(), nullable=True))
        db.session.commit()
        sos_trades_group = Group.query.filter(
            Group.name == Group.SOS_TRADES_DEV_GROUP).first()

        if sos_trades_group is not None:
            sos_trades_group.is_default_applicative_group = True
            db.session.commit()
        # ### end Alembic commands ###
    except:
        db.session.rollback()

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("group", "is_default_applicative_group")
    # ### end Alembic commands ###
