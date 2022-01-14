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
from flask import jsonify, make_response
from werkzeug.exceptions import BadRequest

from sos_trades_api.base_server import app
from sos_trades_api.models.database_models import AccessRights
from sos_trades_api.tools.authentication.authentication import auth_required, get_authenticated_user
from sos_trades_api.tools.right_management.functional.study_case_access_right import StudyCaseAccess
from sos_trades_api.controllers.sostrades_main.visualisation_controller import get_execution_sequence_graph_data


@app.route(f'/api/main/visualisation/visualisation-execution-sequence/<int:study_id>', methods=['GET'])
@auth_required
def execution_sequence_graph_data(study_id):
    if study_id is not None:
        # Checking if user can access study data
        user = get_authenticated_user()
        # Verify user has study case authorisation to retrieve execution status of study (RESTRICTED_VIEWER)
        study_case_access = StudyCaseAccess(user.id)
        if not study_case_access.check_user_right_for_study(AccessRights.RESTRICTED_VIEWER, study_id):
            raise BadRequest('You do not have the necessary rights to retrieve '
                             'execution sequence data of this study case')

        # Proceeding after rights verification
        resp = make_response(
            jsonify(get_execution_sequence_graph_data(study_id)), 200)
        return resp

    raise BadRequest('Missing mandatory parameter: study identifier in url')
