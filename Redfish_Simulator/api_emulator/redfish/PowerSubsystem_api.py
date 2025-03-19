# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import traceback
import logging
import copy
from flask import request
from flask_restful import Resource

from .PowerSupply_api import CreatePowerSupply
from .templates.PowerSubsystem import get_PowerSubsystem_instance

members = {}

foo = 'false'
INTERNAL_ERROR = 500

config = {}


class PowerSubsystemAPI(Resource):
    # INIT
    def __init__(self, **kwargs):
        logging.info('PowerSubsystemAPI init called')
        try:
            global wildcards
            wildcards = kwargs
        except Exception:
            traceback.print_exc()

    # HTTP GET
    def get(self, ident):
        logging.info('PowerSubsystemAPI GET called')
        try:
            # Find the entry with the correct value for Id
            resp = 404
            logging.info(members)
            logging.info(ident)
            if ident in members:
                resp = members[ident], 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self, ident):
        logging.info('PowerSubsystemAPI PUT called')
        return 'PUT is not a supported command for PowerSubsystemAPI', 405

    # HTTP POST
    def post(self, ident):
        logging.info('PowerSubsystemAPI POST called')
        return 'POST is not a supported command for PowerSubsystemAPI', 405

    # HTTP PATCH
    def patch(self, ident):
        logging.info('PowerSubsystemAPI PATCH called')
        return 'PATCH is not a supported command for PowerSubsystemAPI', 405

    # HTTP DELETE
    def delete(self, ident):
        logging.info('PowerSubsystemAPI DELETE called')
        return 'DELETE is not a supported command for PowerSubsystemAPI', 405


# ThermalCollection API
# Thermal does not have a collection API


class CreatePowerSubsystem(Resource):

    def __init__(self, **kwargs):
        logging.info('CreatePowerSubsystem init called')
        if 'resource_class_kwargs' in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])
            logging.debug(wildcards)

    # PUT
    # - Create the resource (since URI variables are avaiable)
    def put(self, ch_id, chassis_count):
        logging.info('CreatePowerSubsystem put called')
        try:
            global wildcards
            config = get_PowerSubsystem_instance(wildcards)
            members[ch_id] = config
            CreatePowerSupply(ch_id=ch_id, ps_id='PS-'+str(chassis_count))
            resp = config, 200
        except Exception:
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp
