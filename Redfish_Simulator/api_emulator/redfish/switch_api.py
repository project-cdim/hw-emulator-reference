# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""
Switch and Switch Collection API File

"""

import logging
from flask_restful import Resource
import g
from .templates.switch import get_switch_instance

members = {}

class SwitchCollectionAPI(Resource):
    """Resource implementation for - /redfish/v1/Fabrics/{FabricId}/Switches"""

    def __init__(self):
        logging.info('SwitchCollectionAPI init called')
        self.rb = g.rest_base
        self.config = {
            '@odata.type': '#SwitchCollection.SwitchCollection',
            'Name': 'Switch Collection',
        }

    def get(self, ident):
        """HTTP get method"""
        logging.info('SwitchCollectionAPI %s GET called', ident)
        if not ident in members:
            return 'Not Found', 404

        self.config['@odata.id'] = f'{self.rb}Fabrics/{ident}/Switches'
        self.config['Members@odata.count'] = len(members[ident])
        self.config['Members'] = [{'@odata.id':x['@odata.id']} for
                x in list(members[ident].values())]
        return self.config, 200


class SwitchAPI(Resource):
    """Resource implementation for - /redfish/v1/Fabrics/{FabricId}/Switches/{SwitchId}"""

    def get(self, ident1, ident2):
        """HTTP get method"""
        logging.info('PCIeSwitchAPI %s %s GET called', ident1, ident2)
        resp = 'Not Found', 404
        if ident1 in members and ident2 in members[ident1]:
            resp = members[ident1][ident2], 200
        return resp


def create_switch(fabric_id, switch_id, chassis_id, switch, portnum):
    """An alternative to the post of SwitchAPI, an interface for creating at startup."""
    logging.info('create_switch %s, %s called', fabric_id, switch_id)
    wildcards = {'rb': g.rest_base, 'FabricId': fabric_id, 'SwitchId': switch_id,
                 'Manufacturer': switch['manufacturer'], 'Model': switch['model'],
                 'SerialNumber': switch['serialNumber'], 'ChassisId': chassis_id,
                 'VCSCount': portnum[0], 'MAXPortCount': portnum[1]}
    config = get_switch_instance(wildcards)
    if not fabric_id in members:
        members[fabric_id] = {}
    members[fabric_id][switch_id] = config
