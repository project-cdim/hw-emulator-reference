# Copyright Notice:
# Copyright 2016-2021 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md
#
# The original DMTF contents of this file have been modified to support
# The Redfish Interface Emulator. These modifications are subject to the following:
# Copyright 2025 NEC Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# SessionService API File

"""
Collection API:  GET
Singleton  API:  (None)
"""

import g

import traceback
import logging
import copy
from flask_restful import Resource

# Resource and SubResource imports
from .templates.SessionService import get_SessionService_instance
from .sessions_api import SessionCollectionAPI, SessionAPI, CreateSession

config = {}

INTERNAL_ERROR = 500


# SessionService Singleton API
# SessionService does not have a Singleton API


# SessionService Collection API
class SessionServiceAPI(Resource):

    def __init__(self, **kwargs):
        logging.info('SessionServiceAPI init called')
        try:
            global config
            config = get_SessionService_instance(kwargs)
        except Exception:
            traceback.print_exc()

    # HTTP GET
    def get(self):
        logging.info('SessionServiceAPI GET called')
        try:
            global config
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        logging.info('SessionServiceAPI PUT called')
        return 'PUT is not a supported command for SessionServiceAPI', 405

    # HTTP POST
    def post(self):
        logging.info('SessionServiceAPI POST called')
        return 'POST is not a supported command for SessionServiceAPI', 405

    # HTTP PATCH
    def patch(self):
        logging.info('SessionServiceAPI PATCH called')
        return 'PATCH is not a supported command for SessionServiceAPI', 405

    # HTTP DELETE
    def delete(self):
        logging.info('SessionServiceAPI DELETE called')
        return 'DELETE is not a supported command for SessionServiceAPI', 405


# CreateSessionService
#
# Called internally to create instances of a resource. If the
# resource has subordinate resources, those subordinate resource(s)
# are created automatically.
#
# Note: In 'init', the first time through, kwargs may not have any
# values, so we need to check. The call to 'init' stores the path
# wildcards. The wildcards are used to modify the resource template
# when subsequent calls are made to instantiate resources.
#
# TODO: Determine need for CreateSessionService
class CreateSessionService(Resource):

    def __init__(self, **kwargs):
        logging.info('CreateSessionService init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

    # Attach APIs for subordinate resource(s). Attach the APIs for
    # a resource collection and its singletons.
    def put(self, ident):
        logging.info('CreateSessionService put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            config = get_SessionService_instance(wildcards)
            g.api.add_resource(SessionCollectionAPI,   '/redfish/v1/SessionService/Sessions')
            g.api.add_resource(SessionAPI,             '/redfish/v1/SessionService/Sessions/<string:ident>', resource_class_kwargs={'rb': g.rest_base})
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateSessionService put exit')
        return resp
