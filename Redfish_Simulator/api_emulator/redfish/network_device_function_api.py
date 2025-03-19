# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""NetworkDeviceFunction

    NetworkDeviceFunction processing
"""

import logging
from flask_restful import Resource

from .templates.NetworkDeviceFunction import format_NetworkDeviceFunction_template
from .network_device_function_metrics_api import create_network_device_function_metrics

members = {}

INTERNAL_ERROR = 500

config = {}


class NetworkDeviceFunctionAPI(Resource):
    """NetworkDeviceFunction Acquisition and Operation API
    Class to acquisition and operation NetworkDeviceFunction
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):
        """GET NetworkDeviceFunction"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        if ident3 not in members[ident1][ident2]:
            return "not found", 404
        return members[ident1][ident2][ident3], 200


class NetworkDeviceFunctionCollectionAPI(Resource):
    """NetworkDeviceFunction Collection Acquisition and Operation API
    Class to acquisition and operation NetworkDeviceFunction Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#NetworkDeviceFunctionCollection.NetworkDeviceFunctionCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#NetworkDeviceFunctionCollection.NetworkDeviceFunctionCollection",
            "Name": "Network Device Functions Collection",
        }

    def get(self, ident1, ident2):
        """GET NetworkDeviceFunction collection"""
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
                f"{prefix}/{ident1}/NetworkAdapters/{ident2}/NetworkDeviceFunctions"
            )
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_network_device_function(**kwargs):
    """Create NetworkDeviceFunction"""
    logging.info("CreateNetworkDeviceFunction")
    ndf_id = kwargs["ndf_id"]
    na_id = kwargs["na_id"]
    chassis_id = kwargs["chassis_id"]

    if chassis_id not in members:
        members[chassis_id] = {}
    if na_id not in members[chassis_id]:
        members[chassis_id][na_id] = {}
    members[chassis_id][na_id][ndf_id] = format_NetworkDeviceFunction_template(**kwargs)

    create_network_device_function_metrics(
        chassis_id=chassis_id, na_id=na_id, ndf_id=ndf_id
    )
