# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""
Fabric and Fabric Collection API File

"""

import logging
from flask_restful import Resource
import g
from .templates.fabric import get_fabric_instance


members = {}


class FabricAPI(Resource):
    """Resource implementation for - /redfish/v1/Fabrics/{FabricId}"""

    def get(self, ident):
        """HTTP get method"""
        logging.info('FabricAPI %s get called', ident)
        if ident not in members:
            return 'not found', 404
        return members[ident], 200


class FabricCollectionAPI(Resource):
    """Resource implementation for - /redfish/v1/Fabrics"""

    def __init__(self):
        self.rb = g.rest_base
        self.config = {
            '@odata.type': '#FabricCollection.FabricCollection',
            '@odata.id': f'{self.rb}Fabrics',
            'Name': 'Fabric Collection',
            'Members@odata.count': {},
            'Members': {}
        }
        self.config['Members@odata.count'] = len(members)
        self.config['Members'] = [{'@odata.id': x['@odata.id']} for x in list(members.values())]

    def get(self):
        """HTTP get method"""
        return self.config, 200


def create_fabric(fabric_id):
    """An alternative to the post of FabricAPI, an interface for creating at startup."""
    logging.info('create_fabric %s called', fabric_id)
    wildcard = {'FabricId': fabric_id, 'rb': g.rest_base}
    config = get_fabric_instance(wildcard)
    members[fabric_id] = config
