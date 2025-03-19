# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""FabricAdapter

    FabricAdapter processing
"""

import logging
from flask_restful import Resource

from .templates.FabricAdapter import format_FabricAdapter_template


members = {}

INTERNAL_ERROR = 500

config = {}


class FabricAdapterAPI(Resource):
    """FabricAdapter Acquisition and Operation API
    Class to acquisition and operation FabricAdapter
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET FabricAdapter"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class FabricAdapterCollectionAPI(Resource):
    """FabricAdapter Collection Management API
    Class to manage the collection of FabricAdapter
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#FabricAdapterCollection.FabricAdapterCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#FabricAdapterCollection.FabricAdapterCollection",
        }

    def get(self, ident):
        """GET FabricAdapter collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/FabricAdapter"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_fabric_adapter(**kwargs):
    """Create FabricAdapter"""
    logging.info("CreateFabricAdapter")
    fa_id = kwargs["fa_id"]
    chassis_id = kwargs["chassis_id"]

    if chassis_id not in members:
        members[chassis_id] = {}
    members[chassis_id][fa_id] = format_FabricAdapter_template(**kwargs)
