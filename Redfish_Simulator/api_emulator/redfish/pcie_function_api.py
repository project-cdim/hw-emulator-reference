# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""PCIeFunction

    PCIeFunction processing
"""

import logging
from flask_restful import Resource

from .templates.PCIeFunction import format_PCIeFunction_template

members = {}

INTERNAL_ERROR = 500

config = {}


class PCIeFunctionAPI(Resource):
    """PCIeFunction Acquisition and Operation API
    Class to acquisition and operation PCIeFunction
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):
        """GET PCIeFunction"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        if ident3 not in members[ident1][ident2]:
            return "not found", 404
        return members[ident1][ident2][ident3], 200


class PCIeFunctionCollectionAPI(Resource):
    """PCIeFunction Collection Acquisition and Operation API
    Class to acquisition and operation PCIeFunction Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#PCIeFunctionCollection.PCIeFunctionCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#PCIeFunctionCollection.PCIeFunctionCollection",
            "Name": "PCIeDevice Functions Collection",
        }

    def get(self, ident1, ident2):
        """GET PCIeFunction collection"""
        try:
            if ident1 not in members:
                return 404
            if ident2 not in members[ident1]:
                return 404
            procs = []
            for p in members[ident1].get(ident2, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = (
                f"{prefix}/{ident1}/PCIeDevices/{ident2}/PCIeFunctions"
            )
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_pcie_function(**kwargs):
    """Create PCIeFunction"""
    logging.info("CreatePCIeFunction")
    pcie_id = kwargs["pcie_id"]
    pcie_f_id = kwargs["pcie_f_id"]
    chassis_id = kwargs["chassis_id"]

    if chassis_id not in members:
        members[chassis_id] = {}
    if pcie_id not in members[chassis_id]:
        members[chassis_id][pcie_id] = {}
    members[chassis_id][pcie_id][pcie_f_id] = format_PCIeFunction_template(**kwargs)
