# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""
ResourceBlockObject API File
"""

import copy
import logging
from flask_restful import Resource
import g

from .processor_api import Processor
from .memory_api import Memory
from .drive_api import DriveChassisAPI
from .ethernetinterface import EthernetInterface_ndf

members = {}


class DenyResourceBlockActionAPI(Resource):
    """Add same resource for CompositionService, but no method support"""
    def __init__(self, **kwargs):
        logging.info('DenyResourceBlockActionAPI init called %s', kwargs)

    def get(self, ident1, ident2):
        """GET method not support"""
        logging.info('DenyResourceBlockActionAPI get called %s %s', ident1, ident2)
        return {'message': 'Method not support.'}, 405

    def put(self, ident1, ident2):
        """PUT method not support"""
        logging.info('DenyResourceBlockActionAPI put called %s %s', ident1, ident2)
        return {'message': 'Method not support.'}, 405

    def post(self, ident1, ident2):
        """POST method not support"""
        logging.info('DenyResourceBlockActionAPI post called %s %s', ident1, ident2)
        return {'message': 'Method not support.'}, 405

    def patch(self, ident1, ident2):
        """PATCH method not support"""
        logging.info('DenyResourceBlockActionAPI patch called %s %s', ident1, ident2)
        return {'message': 'Method not support.'}, 405

    def delete(self, ident1, ident2):
        """DELETE method not support"""
        logging.info('DenyResourceBlockActionAPI delete called %s %s', ident1, ident2)
        return {'message': 'Method not support.'}, 405


class ResourceBlockObjectAPI(Resource):
    """Add same resource for CompositionService"""
    def __init__(self, **kwargs):
        logging.info('ResourceBlockObjectAPI init called %s', kwargs)

    def replace(self, replace_targets: list, config: dict, prev: str, post: str):
        """Convert the value of the replace_targets key in config from prev to post"""
        for keys in replace_targets:
            posit = config
            for key in keys[0:-1]:
                if key not in posit:
                    break
                posit = posit[key]
            else:
                if keys[-1] in posit:
                    posit[keys[-1]] = posit[keys[-1]].replace(prev, post)

    def get(self, ident1, ident2, ident3):
        """
        ident1: ResourceBlockId
        ident2: ResourceName
        ident3: ResourceId
        members[ResoueceBlockId][ResourceBlockId] == ChassisId
        """
        logging.info('ResourceBlockObjectAPI get called %s %s %s', ident1, ident2, ident3)
        replace_targets = []
        if ident1 not in members or ident3 not in members[ident1]:
            return {'message': 'Not found.'}, 404
        chassid = members[ident1][ident3]
        if ident2 == 'Processors':
            config, status = Processor().get(chassid, ident3)
            key = 'Processor'
            replace_targets.append(['Ports', '@odata.id'])
            replace_targets.append(['MemorySummary', 'Metrics', '@odata.id'])
        elif ident2 == 'Memory':
            config, status = Memory().get(chassid, ident3)
            key = 'Memory'
        elif ident2 == 'Drives':
            config, status = DriveChassisAPI().get(chassid, ident3)
            key = 'Drive'
        elif ident2 == 'EthernetInterfaces':
            config, status = EthernetInterface_ndf().get(chassid, '', '', ident3)
            key = 'EthernetInterface'
        else:
            return {'message': 'Not found.'}, 404
        if status == 200 and isinstance(config, dict):
            replace_targets.append(['Actions', 'Oem', f'#{key}.MetricState', 'target'])
            replace_targets.append(['Actions', f'#{key}.Reset', 'target'])
            replace_targets.append(['EnvironmentMetrics', '@odata.id'])
            replace_targets.append(['Metrics', '@odata.id'])
            post = f'CompositionService/ResourceBlocks/{ident1}'
            rb_config = copy.deepcopy(config)
            self.replace(replace_targets, rb_config, f'Chassis/{chassid}', post)
            rb_config['@odata.id'] = f'{g.rest_base}{post}/{ident2}/{ident3}'
        else:
            rb_config = config
        return rb_config, status


def create_resource_object(rscname: str, rscid: str, chassid: str, rbid: str):
    """Convert 'Chassis/{chassid}' to 'CompositionService/ResourceBlocks/{rbid}'"""
    if rscname not in ['Processors', 'Memory', 'Drives', 'EthernetInterfaces']:
        return
    if rbid not in members:
        members[rbid] = {}
    members[rbid][rscid] = chassid
