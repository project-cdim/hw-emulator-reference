# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import logging
from flask import request
from flask_restful import Resource

from .templates.PowerSupply import format_PowerSupply_template

members = {}

foo = 'false'
INTERNAL_ERROR = 500

config = {}


class PowerSupplyAPI(Resource):
    # INIT
    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        if ident1 not in members:
            return 'not found', 404
        if ident2 not in members[ident1]:
            return 'not found', 404
        return members[ident1][ident2], 200


class PowerSupplyCollectionAPI(Resource):
    def __init__(self, rb, suffix):
        self.config = {'@odata.context': '{rb}$metadata#PowerSupplyCollection.PowerSupplyCollection'.format(rb=rb),
                       '@odata.id': '{rb}{suffix}'.format(rb=rb, suffix=suffix),
                       '@odata.type': '#PowerSupplyCollection.PowerSupplyCollection'}

    def get(self, ident):
        logging.info("PowerSupplyCollectionAPI")
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({'@odata.id': p['@odata.id']})
            self.config['@odata.id'] = '{prefix}/{ident}/PowerSubsystem/PowerSupply'.format(prefix=self.config['@odata.id'], ident=ident)
            self.config['Members'] = procs
            self.config['Members@odata.count'] = len(procs)
            resp = self.config, 200
        except Exception as e:
            logging.error(e)
            resp = 'internal error', INTERNAL_ERROR
        return resp


def CreatePowerSupply(**kwargs):
    logging.info("CreatePowerSupply")
    ch_id = kwargs['ch_id']
    ps_id = kwargs['ps_id']

    if ch_id not in members:
        members[ch_id] = {}
    members[ch_id][ps_id] = format_PowerSupply_template(**kwargs)


class PowerSupplyActions_ResetAPI(Resource):

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        resp = INTERNAL_ERROR
        req = request.get_json()
        logging.info('PowerSupplyActions_ResetAPI')
        
        conf = members[ident1][ident2]
        conf['Status']['State'] = 'Disabled'
        for key, value in req.items():
            if 'ForceRestart' == value or 'GracefulRestart' == value:
                conf['Status']['State'] = 'Enabled'

        resp = conf, 200
        return resp

