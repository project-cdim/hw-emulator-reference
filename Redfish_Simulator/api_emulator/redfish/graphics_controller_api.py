# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""GraphicsController

    GraphicsController processing
"""

import logging
from flask_restful import Resource

from .templates.GraphicsController import format_GraphicsController_template

members = {}

INTERNAL_ERROR = 500

config = {}


class GraphicsControllerAPI(Resource):
    """GraphicsController Acquisition and Operation API
    Class to acquisition and operation GraphicsController
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET GraphicsController"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class GraphicsControllerCollectionAPI(Resource):
    """GraphicsController Collection Management API
    Class to manage the collection of GraphicsController
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#GraphicsControllerCollection.GraphicsControllerCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#GraphicsControllerCollection.GraphicsControllerCollection",
        }

    def get(self, ident):
        """GET GraphicsController collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/GraphicsControllers"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_graphics_controller(**kwargs):
    """Create GraphicsController"""
    logging.info("CreateGraphicsController")
    gc_id = kwargs["gc_id"]
    suffix_id = kwargs["suffix_id"]

    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][gc_id] = format_GraphicsController_template(**kwargs)
