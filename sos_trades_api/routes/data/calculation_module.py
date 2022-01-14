'''
Copyright 2022 Airbus SAS

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
from flask import jsonify, make_response, send_file
from werkzeug.exceptions import BadRequest, Unauthorized

from sos_trades_api.models.database_models import AccessRights
from sos_trades_api.base_server import app

from sos_trades_api.tools.right_management.access_right import has_access_to
from sos_trades_api.tools.authentication.authentication import auth_required, get_authenticated_user
from sos_trades_api.controllers.sostrades_data.calculation_controller import calculation_status, \
    calculation_logs, calculation_raw_logs, get_calculation_dashboard, execute_calculation, stop_calculation, delete_calculation_entry
from sos_trades_api.tools.right_management import access_right
from sos_trades_api.tools.right_management.access_right import check_user_is_admin
from sos_trades_api.tools.right_management.functional.study_case_access_right import StudyCaseAccess


@app.route(f'/api/data/calculation/execute/<int:study_id>', methods=['POST'])
@auth_required
def study_case_execution(study_id):
    if study_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()
        # Verify user has study case authorisation to execute study
        # (Contributor)
        study_case_access = StudyCaseAccess(user.id)
        if not study_case_access.check_user_right_for_study(AccessRights.CONTRIBUTOR, study_id):
            app.logger.warn(
                f'Start execution request, user not allowed to execute study case {study_id} ')
            raise BadRequest(
                'You do not have the necessary rights to execute this study case')

        app.logger.info(
            f'Start execution request, user allowed to execute study case {study_id} ')

        # Proceeding after rights verification
        execute_calculation(study_id, user.username)
        resp = make_response(jsonify('Execution started', 200))
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')


@app.route(f'/api/data/calculation/stop/<int:study_id>', methods=['POST'])
@auth_required
def study_case_stop(study_id):
    if study_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()
        # Verify user has study case authorisation to stop execution of study
        # (Contributor)
        study_case_access = StudyCaseAccess(user.id)
        if not study_case_access.check_user_right_for_study(AccessRights.CONTRIBUTOR, study_id):
            app.logger.warn(
                f'Stop execution request, user {user.id} is not allowed to execute study case {study_id} ')
            raise BadRequest(
                'You do not have the necessary rights to stop execution of this study case')

        app.logger.info(
            f'Stop execution request, user {user.id} is allowed to stop study case {study_id} ')

        # Proceeding after rights verification
        stop_calculation(study_id)
        resp = make_response(jsonify('Execution stopped', 200))
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')


@app.route(f'/api/data/calculation/stop/<int:study_case_id>/<int:study_case_execution_id>', methods=['POST'])
@auth_required
def study_case_execution_stop(study_case_id, study_case_execution_id):
    if study_case_id is not None:
        # Checking if user can access study data

        user = get_authenticated_user()
        check_user_is_admin(user.id)  # Raise an exception if not admin

        app.logger.info(
            f'Stop execution request, user {user.id} is allowed to stop study case/execution {study_case_id}/{study_case_execution_id} ')

        # Proceeding after rights verification
        stop_calculation(study_case_id, study_case_execution_id)
        resp = make_response(jsonify('Execution stopped', 200))
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')


@app.route(f'/api/data/calculation/status/<int:study_id>', methods=['GET'])
@auth_required
def study_case_execution_status(study_id):
    if study_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()
        # Verify user has study case authorisation to retrieve execution status
        # of study (RESTRICTED_VIEWER)
        study_case_access = StudyCaseAccess(user.id)
        if not study_case_access.check_user_right_for_study(AccessRights.RESTRICTED_VIEWER, study_id):
            raise BadRequest(
                'You do not have the necessary rights to retrieve execution status of this study case')

        # Proceeding after rights verification
        resp = make_response(jsonify(calculation_status(study_id)), 200)
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')


@app.route(f'/api/data/calculation/logs/<int:study_case_id>', methods=['GET'])
@auth_required
def study_case_logs(study_case_id):
    if study_case_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()

        # Verify user has study case authorisation to retrieve execution logs
        # of study (RESTRICTED_VIEWER)
        study_case_access = StudyCaseAccess(user.id)
        if not study_case_access.check_user_right_for_study(AccessRights.RESTRICTED_VIEWER, study_case_id):
            raise BadRequest(
                'You do not have the necessary rights to retrieve execution logs of this study case')

        # Proceeding after rights verification
        resp = make_response(jsonify(calculation_logs(study_case_id)), 200)
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')


@app.route(f'/api/data/calculation/logs/<int:study_case_id>/<int:study_case_execution_id>', methods=['GET'])
@auth_required
def study_case_execution_logs(study_case_id, study_case_execution_id):
    if study_case_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()
        check_user_is_admin(user.id)  # Raise an exception if not admin

        # Proceeding after rights verification
        resp = make_response(jsonify(calculation_logs(study_case_id, study_case_execution_id)), 200)
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')

@app.route(f'/api/data/calculation/raw-logs/<int:study_case_id>/<int:study_case_execution_id>', methods=['GET'])
@auth_required
def study_case_execution_raw_logs(study_case_id, study_case_execution_id):
    if study_case_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()
        check_user_is_admin(user.id)  # Raise an exception if not admin

        if study_case_id is None:
            raise BadRequest('Missing mandatory parameter: study_case_id')
        if study_case_execution_id is None:
            raise BadRequest('Missing mandatory parameter: study_case_execution_id')

        file_path = calculation_raw_logs(study_case_id, study_case_execution_id)
        if file_path:
            resp = send_file(file_path)
            return resp
        else:
            resp = make_response(jsonify('No logs found.'), 404)
            return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')


@app.route(f'/api/data/calculation/dashboard', methods=['GET'])
@auth_required
def dahsboard_calculation():

    # Checking if user is Admin
    user = get_authenticated_user()

    if has_access_to(user.user_profile_id, access_right.APP_MODULE_ADMIN):

        # Proceeding after rights verification
        return make_response(jsonify(get_calculation_dashboard()), 200)
    else:
        raise Unauthorized(
            'You are not allowed to access this resource')


@app.route(f'/api/data/calculation/delete/<int:study_case_id>/<int:study_case_execution_id>', methods=['DELETE'])
@auth_required
def study_case_execution_delete(study_case_id, study_case_execution_id):
    if study_case_id is not None:
        if study_case_execution_id is not None:
            # Checking if user can access study data
            user = get_authenticated_user()
            check_user_is_admin(user.id)  # Raise an exception if not admin

            # Proceeding after rights verification
            resp = make_response(jsonify(delete_calculation_entry(study_case_id, study_case_execution_id)), 200)
            return resp

        raise BadRequest('Missing mandatory parameter: study identifier in url')

    raise BadRequest('Missing mandatory parameter: study identifier in url')
