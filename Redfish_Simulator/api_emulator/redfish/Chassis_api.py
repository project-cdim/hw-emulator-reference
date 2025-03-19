# Copyright Notice:
# Copyright 2017-2019 DMTF. All rights reserved.
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

# Chassis API File

"""
Collection API:  GET, POST
Singleton  API:  GET, POST, PATCH, DELETE
"""

import g

import traceback
import logging
import copy
from flask import request
from flask_restful import Resource

# Resource and SubResource imports
from .templates.Chassis import get_Chassis_instance
from .environment_metrics_api import create_environment_metrics
from .PowerSupply_api import CreatePowerSupply

members = {}

INTERNAL_ERROR = 500


# Chassis Singleton API
class ChassisAPI(Resource):

    # kwargs is used to pass in the wildcards values to be replaced
    # when an instance is created via get_<resource>_instance().
    #
    # The call to attach the API establishes the contents of kwargs.
    # All subsequent HTTP calls go through __init__.
    #
    # __init__ stores kwargs in wildcards, which is used to pass
    # values to the get_<resource>_instance() call.
    def __init__(self, **kwargs):
        logging.info('ChassisAPI init called')
        try:
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()

    # HTTP GET
    def get(self, ident):
        logging.info('ManagerAPI GET called')
        if ident not in members:
            return 'not found', 404

        # Find the entry with the correct value for Id
        return members[ident], 200

    # HTTP PUT
    def put(self, ident):
        logging.info('ChassisAPI PUT called')
        return 'PUT is not a supported command for ChassisAPI', 405

    # HTTP POST
    # This is an emulator-only POST command that creates new resource
    # instances from a predefined template. The new instance is given
    # the identifier "ident", which is taken from the end of the URL.
    # PATCH commands can then be used to update the new instance.
    def post(self, ident):
        logging.info('ChassisAPI POST called')
        return 'POST is not a supported command for ChassisAPI', 405

    # HTTP PATCH
    def patch(self, ident):
        logging.info('ChassisAPI PATCH called')
        return 'PATCH is not a supported command for ChassisAPI', 405

    # HTTP DELETE
    def delete(self, ident):
        logging.info('ChassisAPI DELETE called')
        return 'DELETE is not a supported command for ChassisAPI', 405


# Chassis Collection API
class ChassisCollectionAPI(Resource):

    def __init__(self):
        logging.info('ChassisCollectionAPI init called')
        self.rb = g.rest_base
        self.config = {
            '@odata.context': self.rb + '$metadata#ChassisCollection.ChassisCollection',
            '@odata.id': self.rb + 'Chassis',
            '@odata.type': '#ChassisCollection.1.0.0.ChassisCollection',
            'Name': 'Chassis Collection',
            'Members@odata.count': len(members),
            'Members': [{'@odata.id': x['@odata.id']} for
                        x in list(members.values())]
        }

    # HTTP GET
    def get(self):
        logging.info('ChassisCollectionAPI GET called')
        try:
            resp = self.config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        logging.info('ChassisCollectionAPI PUT called')
        return 'PUT is not a supported command for ChassisCollectionAPI', 405

    def verify(self, config):
        # TODO: Implement a method to verify that the POST body is valid
        return True,{}

    # HTTP POST
    # POST should allow adding multiple instances to a collection.
    # For now, this only adds one instance.
    # TODO: 'id' should be obtained from the request data.
    def post(self):
        logging.info('ChassisCollectionAPI POST called')
        return 'POST is not a supported command for ChassisCollectionAPI', 405

    # HTTP PATCH
    def patch(self):
        logging.info('ChassisCollectionAPI PATCH called')
        return 'PATCH is not a supported command for ChassisCollectionAPI', 405

    # HTTP DELETE
    def delete(self):
        logging.info('ChassisCollectionAPI DELETE called')
        return 'DELETE is not a supported command for ChassisCollectionAPI', 405


# CreateChassis
#
# Called internally to create instances of a resource. If the
# resource has subordinate resources, those subordinate resource(s)
# are created automatically.
#
# Note: In 'init', the first time through, kwargs may not have any
# values, so we need to check. The call to 'init' stores the path
# wildcards. The wildcards are used to modify the resource template
# when subsequent calls are made to instantiate resources.
class CreateChassis(Resource):

    def __init__(self, **kwargs):
        logging.info('CreateChassis init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

    # Create instance
    def put(self, ident):
        logging.info('CreateChassis put called')
        try:
            global config
            global wildcards
            wildcards['id'] = ident
            target = '-'
            idx = ident.split(target)
            wildcards['ps_id'] = idx[-1]
            config = get_Chassis_instance(wildcards)
            members[ident] = config
            create_environment_metrics(suffix='Chassis', suffix_id=ident, chassis_id=ident,
                                     schema='Chassis', schema_id=ident, sensor_id=wildcards['sensor_id'],
                                     interval=wildcards['interval'])
            CreatePowerSupply(suffix='Chassis', suffix_id=ident, ch_id=ident,
                              schema='Chassis', ps_id=wildcards['ps_id'])
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info('CreateChassis init exit')
        return resp


class ChassisActions_ResetAPI(Resource):

    def __init__(self, **kwargs):
        pass

    def post(self, ident):
        resp = INTERNAL_ERROR
        req = request.get_json()
        logging.info('ChassisActions_ResetAPI')
        
        conf = members[ident]
        conf['Status']['State'] = 'Disabled'
        conf['PowerState'] = 'Off'
        for key, value in req.items():
            if 'ForceRestart' == value or 'GracefulRestart' == value or 'ForceOn' == value or 'On' == value:
                conf['Status']['State'] = 'Enabled'
                conf['PowerState'] = 'On'

        resp = conf, 200
        return resp
