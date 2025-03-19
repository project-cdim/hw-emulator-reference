# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""NetworkInterface

    NetworkInterface processing
"""

import logging
from flask_restful import Resource

from .templates.NetworkInterface import format_NetworkInterface_template

members = {}

INTERNAL_ERROR = 500


class NetworkInterfaceAPI(Resource):
    """NetworkInterface Acquisition and Operation API
    Class to acquisition and operation NetworkInterface
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET  NetworkInterface"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class NetworkInterfaceCollectionAPI(Resource):
    """NetworkInterface Collection Acquisition and Operation API
    Class to acquisition and operation NetworkInterface Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#NetworkInterfaceCollection.NetworkInterfaceCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#NetworkInterfaceCollection.NetworkInterfaceCollection",
            "Name": "Network Interfaces Collection",
        }

    def get(self, ident):
        """GET NetworkInterface collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/NetworkInterfaces"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_network_interface(**kwargs):
    """Create NetworkInterface"""
    suffix_id = kwargs["suffix_id"]
    ni_id = kwargs["ni_id"]
    if suffix_id not in members:
        members[suffix_id] = {}

    members[suffix_id][ni_id] = format_NetworkInterface_template(**kwargs)
