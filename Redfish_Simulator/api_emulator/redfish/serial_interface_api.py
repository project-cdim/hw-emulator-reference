# Copyright Notice:
# Copyright 2025-2026 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""SerialInterface

    SerialInterface processing
"""

import logging
from flask_restful import Resource

from .templates.SerialInterface import format_SerialInterfaces_template

members = {}

INTERNAL_ERROR = 500

config = {}


class SerialInterfaceAPI(Resource):
    """SerialInterface Acquisition and Operation API
    Class to acquisition and operation SerialInterface
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET SerialInterface"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class SerialInterfaceCollectionAPI(Resource):
    """SerialInterface Collection Acquisition and Operation API
    Class to acquisition and operation SerialInterface Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#SerialInterfaceCollection.SerialInterfaceCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#SerialInterfaceCollection.SerialInterfaceCollection",
            "Name": "SerialInterface Collection",
        }

    def get(self, ident):
        """GET SerialInterface collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/SerialInterfaces"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_serial_interface(**kwargs):
    """Create SerialInterface"""
    logging.info("CreateSerialInterface")

    si_id = kwargs["si_id"]
    manager_id = kwargs["manager_id"]
    if manager_id not in members:
        members[manager_id] = {}
    members[manager_id][si_id] = format_SerialInterfaces_template(**kwargs)
