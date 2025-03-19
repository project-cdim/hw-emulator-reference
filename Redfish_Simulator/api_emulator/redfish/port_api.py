# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""Port

    Port processing
"""

import logging
from flask_restful import Resource

from .templates.Port import format_Port_template

members = {}

INTERNAL_ERROR = 500

config = {}


class PortAPI(Resource):
    """Port Acquisition and Operation API
    Class to acquisition and operation Port
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):
        """GET Port"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        if ident3 not in members[ident1][ident2]:
            return "not found", 404
        return members[ident1][ident2][ident3], 200


class PortControllerAPI(Resource):
    """Port Collection Acquisition and Operation API
    Class to acquisition and operation Port Collection
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3, ident4):  # pylint: disable=W0613
        """GET Port collection"""
        if ident1 not in members:
            return "not found", 404
        if ident3 not in members[ident1]:
            return "not found", 404
        if ident4 not in members[ident1][ident3]:
            return "not found", 404
        return members[ident1][ident3][ident4], 200


class NetworkAdapterPortCollectionAPI(Resource):
    """Port Collection Acquisition and Operation API
    Class to acquisition and operation Port Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#PortCollection.PortCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#PortCollection.PortCollection",
            "Name": "Ports Collection",
        }

    def get(self, ident1, ident2):
        """GET Port collection"""
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
                f"{prefix}/{ident1}/NetworkAdapters/{ident2}/Ports"
            )
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class ProcessorPortCollectionAPI(Resource):
    """Port Collection Acquisition and Operation API
    Class to acquisition and operation Port Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#PortCollection.PortCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#PortCollection.PortCollection",
            "Name": "Ports Collection",
        }

    def get(self, ident1, ident2):
        """GET Port collection"""
        try:
            if ident1 not in members:
                return 404
            if ident2 not in members[ident1]:
                return 404
            procs = []
            for p in members[ident1].get(ident2, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident1}/Processors/{ident2}/Ports"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class PortControllerCollectionAPI(Resource):
    """PortController Collection Acquisition and Operation API
    Class to acquisition and operation Port PortController
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#PortCollection.PortCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#PortCollection.PortCollection",
            "Name": "Ports Collection",
        }

    def get(self, ident1, ident2, ident3):
        """GET PortController collection"""
        try:
            if ident1 not in members:
                return 404
            if ident3 not in members[ident1]:
                return 404
            procs = []
            for p in members[ident1].get(ident3, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = (
                f"{prefix}/{ident1}/Storage/{ident2}/Controllers/{ident3}/Ports"
            )
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_port(**kwargs):
    """Create Port"""
    logging.info("CreatePort")
    port_id = kwargs["port_id"]
    adapter_id = kwargs["adapter_id"]
    suffix_id = kwargs["suffix_id"]

    if suffix_id not in members:
        members[suffix_id] = {}
    if adapter_id not in members[suffix_id]:
        members[suffix_id][adapter_id] = {}
    members[suffix_id][adapter_id][port_id] = format_Port_template(**kwargs)
