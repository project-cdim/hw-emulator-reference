# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
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

# Redfish Memorys and Memory Resources. Based on version 1.0.0

from flask_restful import Resource
import logging
import copy
from .templates.ethernetinterface import format_nic_template

members = {}
sys_id = {}
INTERNAL_ERROR = 500


class EthernetInterface(Resource):
    """
    EthernetInterface.v1_3_0.EthernetInterface
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        if ident2 not in members:
            return 'not found', 404
        if sys_id.get(ident2, {}).get('schema'):
            mem = copy.deepcopy(members[ident2])
            mem['@odata.id'] = '/redfish/v1/Systems/{ident1}/EthernetInterfaces/{ident2}'.format(ident1=sys_id[ident2]['schema'], ident2=ident2)
            return mem, 200
        else:
            return 'not found', 404


class EthernetInterface_ndf(Resource):
    """
    EthernetInterface.v1_3_0.EthernetInterface
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3, ident4):
        if ident4 not in members:
            return 'not found', 404
        return members[ident4], 200


class EthernetInterfaceCollection(Resource):
    """
    EthernetInterface.v1_3_0.EthernetInterfaceCollection
    """

    def __init__(self, rb, suffix):
        """
        EthernetInterfaceCollection Constructor
        """
        self.config = {'@odata.context': '{rb}$metadata#EthernetInterfaceCollection.EthernetInterfaceCollection'.format(rb=rb),
                       '@odata.id': '{rb}{suffix}'.format(rb=rb, suffix=suffix),
                       '@odata.type': '#EthernetInterfaceCollection.EthernetInterfaceCollection',
                       'Name': 'Ethernet Interfaces Collection'}

    def get(self, ident):
        try:
            procs = []
            for p in members.values():
                target = '/'
                idx = p['@odata.id'].split(target)
                ei_id = idx[-1]
                if sys_id.get(ei_id, {}).get('schema') == ident:
                    p_url = copy.deepcopy(p['@odata.id'])
                    p_url = '/redfish/v1/Systems/{ident1}/EthernetInterfaces/{ident2}'.format(ident1=sys_id[ei_id]['schema'], ident2=ei_id)
                    procs.append({'@odata.id': p_url})
            self.config['@odata.id'] = '{prefix}/{ident}/EthernetInterfaces'.format(prefix=self.config['@odata.id'], ident=ident)
            self.config['Members'] = procs
            self.config['Members@odata.count'] = len(procs)
            resp = self.config, 200
        except Exception as e:
            logging.error(e)
            resp = 'internal error', INTERNAL_ERROR
        return resp


class EthernetInterface_ndf_Collection(Resource):
    """
    EthernetInterface.v1_3_0.EthernetInterfaceCollection
    """

    def __init__(self, rb, suffix):
        """
        EthernetInterfaceCollection Constructor
        """
        self.config = {'@odata.context': '{rb}$metadata#EthernetInterfaceCollection.EthernetInterfaceCollection'.format(rb=rb),
                       '@odata.id': '{rb}{suffix}'.format(rb=rb, suffix=suffix),
                       '@odata.type': '#EthernetInterfaceCollection.EthernetInterfaceCollection',
                       'Name': 'Ethernet Interfaces Collection'}

    def get(self, ident1, ident2, ident3):
        try:
            procs = []
            for p in members.values():
                target = '/'
                idx = p['@odata.id'].split(target)
                ei_id = idx[-1]
                logging.info(ei_id)
                logging.info(sys_id.get(ei_id))
                logging.info(ident3)
                if sys_id.get(ei_id, {}).get('ndf_id') == ident3:
                    procs.append({'@odata.id': p['@odata.id']})
            self.config['@odata.id'] = '{prefix}/{ident1}/NetworkAdapters/{ident2}/NetworkDeviceFunctions/{ident3}/EthernetInterfaces'.format(prefix=self.config['@odata.id'], ident1=ident1, ident2=ident2, ident3=ident3)
            self.config['Members'] = procs
            self.config['Members@odata.count'] = len(procs)
            resp = self.config, 200
        except Exception as e:
            logging.error(e)
            resp = 'internal error', INTERNAL_ERROR
        return resp


def CreateEthernetInterface(**kwargs):
    ei_id = kwargs['ei_id']

    members[ei_id] = format_nic_template(**kwargs)
    if kwargs.get('schema_id'):
        sys_id[ei_id] = {}
        sys_id[ei_id]['schema'] = kwargs['schema_id']
        sys_id[ei_id]['ndf_id'] = kwargs['ndf_id']
