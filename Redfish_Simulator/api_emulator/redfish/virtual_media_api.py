# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""VirtualMedia

    VirtualMedia processing
"""
import logging
from flask_restful import Resource

from .templates.VirtualMedia import format_VirtualMedia_template

members = {}

INTERNAL_ERROR = 500

config = {}


class VirtualMediaAPI(Resource):
    """VirtualMedia Acquisition and Operation API
    Class to acquisition and operation VirtualMedia
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET VirtualMedia"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class VirtualMediaCollectionAPI(Resource):
    """VirtualMedia Collection Acquisition and Operation API
    Class to acquisition and operation VirtualMedia Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#VirtualMediaCollection.VirtualMediaCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#VirtualMediaCollection.VirtualMediaCollection",
            "Name": "VirtualMedias Collection",
        }

    def get(self, ident):
        """GET VirtualMedia Collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/VirtualMedia"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_virtual_media(**kwargs):
    """Create VirtualMedia"""
    logging.info("CreateVirtualMedia")
    vm_id = kwargs["vm_id"]
    suffix_id = kwargs["suffix_id"]

    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][vm_id] = format_VirtualMedia_template(**kwargs)
