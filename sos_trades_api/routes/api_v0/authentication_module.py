# -*- coding: utf-8 -*-
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

from flask import request, make_response, abort, jsonify

from sos_trades_api.base_server import app
from sos_trades_api.controllers.sostrades_data.authentication_controller import \
    authenticate_user_standard, AuthenticationError


@app.route(f'/api/v0/auth/login', methods=['POST'])
def login():
    """
    Return bearer access token

    :return: json response like {'access_token': access_token}
    """

    if request.json is None:
        abort(400, "'username' and 'password' not found in request")

    elif request.json.get('username') is None:
        abort(400, "'username' not found in request")

    elif request.json.get('password') is None:
        abort(400, "'password' not found in request")

    try:
        username = request.json.get('username')
        password = request.json.get('password')

        access_token, _, _, _ = authenticate_user_standard(username, password)

        return make_response(jsonify({'access_token': access_token}), 200)

    except AuthenticationError as error:
        abort(403, str(error))

    except Exception as err:
        abort(400, str(err))
