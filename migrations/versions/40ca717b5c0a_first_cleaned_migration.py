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
from sqlalchemy.dialects import mysql

"""First cleaned migration

Revision ID: 40ca717b5c0a
Revises: 
Create Date: 2021-10-05 17:50:29.107226

"""

# revision identifiers, used by Alembic.
revision = "40ca717b5c0a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("access_rights",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("access_right", sa.String(length=64), nullable=True),
    sa.Column("description", sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_access_rights_access_right"), "access_rights", ["access_right"], unique=True)
    op.create_table("process",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("name", sa.String(length=64), nullable=True),
    sa.Column("process_path", sa.String(length=255), nullable=True),
    sa.Column("disabled", sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_process_name"), "process", ["name"], unique=False)
    op.create_table("user_profile",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("name", sa.String(length=64), nullable=True),
    sa.Column("description", sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("name"),
    sqlite_autoincrement=True,
    )
    op.create_table("reference_study",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("process_id", sa.Integer(), nullable=True),
    sa.Column("name", sa.String(length=128), nullable=True),
    sa.Column("reference_path", sa.String(length=128), nullable=True),
    sa.Column("reference_type", sa.String(length=128), nullable=True),
    sa.Column("creation_date", sa.DateTime(timezone=True), nullable=True),
    sa.Column("execution_status", sa.String(length=64), server_default="FINISHED", nullable=True),
    sa.Column("generation_logs", sa.Text(), nullable=True),
    sa.Column("kubernete_pod_name", sa.String(length=128), server_default="", nullable=True),
    sa.Column("disabled", sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(["process_id"], ["process.id"], name="fk_reference_study_process_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_reference_study_execution_status"), "reference_study", ["execution_status"], unique=False)
    op.create_index(op.f("ix_reference_study_name"), "reference_study", ["name"], unique=False)
    op.create_index(op.f("ix_reference_study_reference_path"), "reference_study", ["reference_path"], unique=False)
    op.create_index(op.f("ix_reference_study_reference_type"), "reference_study", ["reference_type"], unique=False)
    op.create_table("user",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("username", sa.String(length=64), nullable=True),
    sa.Column("firstname", sa.String(length=64), nullable=True),
    sa.Column("lastname", sa.String(length=64), nullable=True),
    sa.Column("email", sa.String(length=120), nullable=True),
    sa.Column("department", sa.String(length=120), nullable=True),
    sa.Column("company", sa.String(length=120), nullable=True),
    sa.Column("password_hash", sa.String(length=128), nullable=True),
    sa.Column("is_logged", sa.Boolean(), nullable=True),
    sa.Column("user_profile_id", sa.Integer(), nullable=True),
    sa.Column("reset_uuid", sa.String(length=36), nullable=True),
    sa.Column("account_source", sa.String(length=64), server_default="local_account", nullable=False),
    sa.Column('last_login_date', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column('last_password_reset_date', sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.ForeignKeyConstraint(["user_profile_id"], ["user_profile.id"], name="fk_user_user_profile_id"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_user_company"), "user", ["company"], unique=False)
    op.create_index(op.f("ix_user_department"), "user", ["department"], unique=False)
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_firstname"), "user", ["firstname"], unique=False)
    op.create_index(op.f("ix_user_lastname"), "user", ["lastname"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table("group",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("name", sa.String(length=64), nullable=True),
    sa.Column("creator_id", sa.Integer(), nullable=True),
    sa.Column("creation_date", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("description", sa.String(length=255), nullable=True),
    sa.Column("confidential", sa.Boolean(), nullable=True),
    sa.Column("is_default_applicative_group", sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(["creator_id"], ["user.id"], name="fk_group_creator_id"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_group_name"), "group", ["name"], unique=True)
    op.create_table("process_access_user",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("process_id", sa.Integer(), nullable=False),
    sa.Column("right_id", sa.Integer(), nullable=True),
    sa.Column("source", sa.String(length=94), server_default="USER", nullable=True),
    sa.ForeignKeyConstraint(["process_id"], ["process.id"], name="fk_process_access_user_process_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["right_id"], ["access_rights.id"], name="fk_process_access_user_right_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="fk_process_access_user_user_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("user_id", "process_id"),
    sqlite_autoincrement=True,
    )
    op.create_table("reference_study_execution_log",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("reference_id", sa.Integer(), nullable=True),
    sa.Column("name", sa.Text(), nullable=True),
    sa.Column("log_level_name", sa.String(length=64), nullable=True),
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("message", sa.Text(), nullable=True),
    sa.Column("exception", sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(["reference_id"], ["reference_study.id"], name="fk_reference_study_execution_log_reference_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_table("group_access_group",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("group_id", sa.Integer(), nullable=False),
    sa.Column("group_member_id", sa.Integer(), nullable=False),
    sa.Column("right_id", sa.Integer(), nullable=True),
    sa.Column("group_members_ids", sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["group.id"], name="fk_group_access_group_group_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["group_member_id"], ["group.id"], name="fk_group_access_group_group_member_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["right_id"], ["access_rights.id"], name="fk_group_access_group_right_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("group_id", "group_member_id"),
    sqlite_autoincrement=True,
    )
    op.create_table("group_access_user",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("group_id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("right_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["group.id"], name="fk_group_access_user_group_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["right_id"], ["access_rights.id"], name="fk_group_access_user_right_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="fk_group_access_user_user_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("user_id", "group_id"),
    sqlite_autoincrement=True,
    )
    op.create_table("process_access_group",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("group_id", sa.Integer(), nullable=False),
    sa.Column("process_id", sa.Integer(), nullable=False),
    sa.Column("right_id", sa.Integer(), nullable=True),
    sa.Column("source", sa.String(length=94), server_default="USER", nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["group.id"], name="fk_process_access_group_group_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["process_id"], ["process.id"], name="fk_process_access_group_process_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["right_id"], ["access_rights.id"], name="fk_process_access_group_right_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("group_id", "process_id"),
    sqlite_autoincrement=True,
    )
    op.create_table("study_case",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("group_id", sa.Integer(), nullable=False),
    sa.Column("name", sa.String(length=64), nullable=True),
    sa.Column("repository", sa.String(length=64), server_default="test", nullable=True),
    sa.Column("process", sa.String(length=64), nullable=True),
    sa.Column("process_id", sa.Integer(), nullable=True),
    sa.Column("description", mysql.TEXT(), nullable=True),
    sa.Column("creation_date", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("modification_date", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("user_id_execution_authorised", sa.Integer(), nullable=True),
    sa.Column("current_execution_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["group.id"], name="fk_study_case_group_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["process_id"], ["process.id"], name="fk_study_case_process_id"),
    sa.ForeignKeyConstraint(["user_id_execution_authorised"], ["user.id"], name="fk_study_case_user_id_execution_authorised"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_study_case_name"), "study_case", ["name"], unique=False)
    op.create_index(op.f("ix_study_case_process"), "study_case", ["process"], unique=False)
    op.create_index(op.f("ix_study_case_repository"), "study_case", ["repository"], unique=False)
    op.create_table("notification",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=True),
    sa.Column("author", sa.String(length=94), nullable=True),
    sa.Column("type", sa.String(length=64), nullable=True),
    sa.Column("message", sa.String(length=255), nullable=True),
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_notification_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_notification_author"), "notification", ["author"], unique=False)
    op.create_index(op.f("ix_notification_type"), "notification", ["type"], unique=False)
    op.create_table("study_case_access_group",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("group_id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=False),
    sa.Column("right_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["group.id"], name="fk_study_case_access_group_group_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["right_id"], ["access_rights.id"], name="fk_study_case_access_group_right_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_access_group_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("group_id", "study_case_id"),
    sqlite_autoincrement=True,
    )
    op.create_table("study_case_access_user",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=False),
    sa.Column("right_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["right_id"], ["access_rights.id"], name="fk_study_case_access_user_right_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_access_user_study_case_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="fk_study_case_access_user_user_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sa.UniqueConstraint("user_id", "study_case_id"),
    sqlite_autoincrement=True,
    )
    op.create_table("study_case_execution",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=True),
    sa.Column("execution_status", sa.String(length=64), server_default="FINISHED", nullable=True),
    sa.Column("execution_type", sa.String(length=64), server_default="", nullable=True),
    sa.Column("kubernetes_pod_name", sa.String(length=128), server_default="", nullable=True),
    sa.Column("process_identifier", sa.Integer(), nullable=True),
    sa.Column("creation_date", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("requested_by", sa.String(length=64), server_default="", nullable=False),
    sa.Column("cpu_usage", sa.String(length=32), server_default="----", nullable=True),
    sa.Column("memory_usage", sa.String(length=32), server_default="----", nullable=True),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_execution_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_study_case_execution_execution_status"), "study_case_execution", ["execution_status"], unique=False)
    op.create_index(op.f("ix_study_case_execution_execution_type"), "study_case_execution", ["execution_type"], unique=False)
    op.create_index(op.f("ix_study_case_execution_requested_by"), "study_case_execution", ["requested_by"], unique=False)
    op.create_table("study_case_validation",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=True),
    sa.Column("namespace", sa.Text(), nullable=True),
    sa.Column("discipline_name", sa.Text(), nullable=True),
    sa.Column("validation_comment", sa.Text(), nullable=True),
    sa.Column("validation_state", sa.String(length=64), nullable=True),
    sa.Column("validation_type", sa.String(length=64), nullable=True),
    sa.Column("validation_date", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("validation_user", sa.Text(), nullable=True),
    sa.Column("validation_user_department", sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_validation_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_table("study_coedition_user",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=True),
    sa.Column("study_case_id", sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_coedition_user_study_case_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="fk_study_coedition_user_user_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_table("user_study_preference",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("user_id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=False),
    sa.Column("preference", mysql.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_user_study_preference_study_case_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="fk_user_study_preference_user_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_table("study_case_change",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("notification_id", sa.Integer(), nullable=True),
    sa.Column("variable_id", sa.Text(), nullable=True),
    sa.Column("variable_type", sa.String(length=64), nullable=True),
    sa.Column("change_type", sa.String(length=64), nullable=True),
    sa.Column("new_value", sa.Text(), nullable=True),
    sa.Column("old_value", sa.Text(), nullable=True),
    sa.Column("old_value_blob", sa.LargeBinary().with_variant(mysql.LONGBLOB(), 'mysql'), nullable=True),
    sa.Column("last_modified", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.ForeignKeyConstraint(["notification_id"], ["notification.id"], name="fk_study_case_change_notification_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_index(op.f("ix_study_case_change_change_type"), "study_case_change", ["change_type"], unique=False)
    op.create_index(op.f("ix_study_case_change_variable_type"), "study_case_change", ["variable_type"], unique=False)
    op.create_table("study_case_discipline_status",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=True),
    sa.Column("study_case_execution_id", sa.Integer(), nullable=True),
    sa.Column("discipline_key", sa.Text(), nullable=True),
    sa.Column("status", sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(["study_case_execution_id"], ["study_case_execution.id"], name="fk_study_case_discipline_status_study_case_execution_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_discipline_status_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    op.create_table("study_case_execution_log",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("study_case_id", sa.Integer(), nullable=True),
    sa.Column("study_case_execution_id", sa.Integer(), nullable=True),
    sa.Column("name", sa.Text(), nullable=True),
    sa.Column("log_level_name", sa.String(length=64), nullable=True),
    sa.Column("created", sa.DateTime(timezone=True), server_default=sa.func.current_timestamp(), nullable=True),
    sa.Column("message", sa.Text(), nullable=True),
    sa.Column("exception", sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(["study_case_execution_id"], ["study_case_execution.id"], name="fk_study_case_execution_log_study_case_execution_id", ondelete="CASCADE"),
    sa.ForeignKeyConstraint(["study_case_id"], ["study_case.id"], name="fk_study_case_execution_log_study_case_id", ondelete="CASCADE"),
    sa.PrimaryKeyConstraint("id"),
    sqlite_autoincrement=True,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("study_case_execution_log")
    op.drop_table("study_case_discipline_status")
    op.drop_index(op.f("ix_study_case_change_variable_type"), table_name="study_case_change")
    op.drop_index(op.f("ix_study_case_change_change_type"), table_name="study_case_change")
    op.drop_table("study_case_change")
    op.drop_table("user_study_preference")
    op.drop_table("study_coedition_user")
    op.drop_table("study_case_validation")
    op.drop_index(op.f("ix_study_case_execution_requested_by"), table_name="study_case_execution")
    op.drop_index(op.f("ix_study_case_execution_execution_type"), table_name="study_case_execution")
    op.drop_index(op.f("ix_study_case_execution_execution_status"), table_name="study_case_execution")
    op.drop_table("study_case_execution")
    op.drop_table("study_case_access_user")
    op.drop_table("study_case_access_group")
    op.drop_index(op.f("ix_notification_type"), table_name="notification")
    op.drop_index(op.f("ix_notification_author"), table_name="notification")
    op.drop_table("notification")
    op.drop_index(op.f("ix_study_case_repository"), table_name="study_case")
    op.drop_index(op.f("ix_study_case_process"), table_name="study_case")
    op.drop_index(op.f("ix_study_case_name"), table_name="study_case")
    op.drop_table("study_case")
    op.drop_table("process_access_group")
    op.drop_table("group_access_user")
    op.drop_table("group_access_group")
    op.drop_table("reference_study_execution_log")
    op.drop_table("process_access_user")
    op.drop_index(op.f("ix_group_name"), table_name="group")
    op.drop_table("group")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_lastname"), table_name="user")
    op.drop_index(op.f("ix_user_firstname"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_index(op.f("ix_user_department"), table_name="user")
    op.drop_index(op.f("ix_user_company"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_reference_study_reference_type"), table_name="reference_study")
    op.drop_index(op.f("ix_reference_study_reference_path"), table_name="reference_study")
    op.drop_index(op.f("ix_reference_study_name"), table_name="reference_study")
    op.drop_index(op.f("ix_reference_study_execution_status"), table_name="reference_study")
    op.drop_table("reference_study")
    op.drop_table("user_profile")
    op.drop_index(op.f("ix_process_name"), table_name="process")
    op.drop_table("process")
    op.drop_index(op.f("ix_access_rights_access_right"), table_name="access_rights")
    op.drop_table("access_rights")
    # ### end Alembic commands ###
