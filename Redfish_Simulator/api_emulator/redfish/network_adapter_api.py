# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""NetworkAdapter

    NetworkAdapter processing
"""

import logging
from flask import request
from flask_restful import Resource

from .templates.NetworkAdapter import format_NetworkAdapter_template
from .network_adapter_metrics_api import create_network_adapter_metrics
from .environment_metrics_api import create_environment_metrics
from .serial_interface_api import set_connect_nic_id
from .Chassis_api import ChassisCollectionAPI
from .metrics_state_api import set_metric_state


members = {}

INTERNAL_ERROR = 500

config = {}


class NetworkAdapterAPI(Resource):
    """NetworkAdapter Acquisition and Operation API
    Class to acquisition and operation NetworkAdapter
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET NetworkAdapter"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404

        target = "-"
        idx = ident2.split(target)
        nic_id = idx[-1]
        set_connect_nic_id(nic_id)
        return members[ident1][ident2], 200


class NetworkAdapterCollectionAPI(Resource):
    """NetworkAdapter Collection Management API
    Class to manage the collection of NetworkAdapter
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#NetworkAdapterCollection.NetworkAdapterCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#NetworkAdapterCollection.NetworkAdapterCollection",
            "Name": "Network Adapters Collection",
        }

    def get(self, ident):
        """GET NetworkAdapter collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/NetworkAdapters"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_network_adapter(**kwargs):
    """Create NetworkAdapter"""
    logging.info("CreateNetworkAdapter")
    na_id = kwargs["na_id"]
    chassis_id = kwargs["chassis_id"]

    ndf_list = kwargs["ndfList"]
    port_na_list = kwargs["portNAList"]
    sensor_id = kwargs["sensor_id"]
    interval = kwargs["dev_param"]["sensingInterval"]

    if chassis_id not in members:
        members[chassis_id] = {}
    members[chassis_id][na_id] = format_NetworkAdapter_template(**kwargs)

    create_network_adapter_metrics(
        chassis_id=chassis_id,
        na_id=na_id,
        spec={"BitRate": kwargs["dev_param"]["bitRate"]},
    )
    create_environment_metrics(
        suffix="Chassis",
        suffix_id=chassis_id,
        chassis_id=chassis_id,
        schema="NetworkAdapters",
        schema_id=na_id,
        ndfList=ndf_list,
        portNAList=port_na_list,
        sensor_id=sensor_id,
        spec={"BitRate": kwargs["dev_param"]["bitRate"]},
        interval=interval,
    )


class NetworkAdapterActionsResetAPI(Resource):
    """NetworkAdapter Reset Action API
    Class to reset action of NetworkAdapter
    """

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        """POST reset action"""
        resp = INTERNAL_ERROR
        req = request.get_json()
        logging.info("NetworkAdapterActions_ResetAPI")

        chassis = ChassisCollectionAPI().get()
        for chassis_url in chassis[0]["Members"]:
            target = "/"
            idx = chassis_url["@odata.id"].split(target)
            chassis_id = idx[-1]
            if members.get(chassis_id, {}).get(ident2):
                conf = members[ident1][ident2]
                conf["PowerState"] = "Off"
                for value in req.values():
                    if value in ["ForceRestart", "GracefulRestart", "ForceOn", "On"]:
                        conf["Status"]["State"] = "Enabled"
                        conf["PowerState"] = "On"

                if conf["PowerState"] == "Off":
                    set_metric_state(ident1, ident2, "action", "off")
                else:
                    set_metric_state(ident1, ident2, "action", "on")

        resp = conf, 200
        return resp


class NetworkAdapterActionsMetricStateAPI(Resource):
    """NetworkAdapter Set Metric State API
    Class to set metric state of NetworkAdapter
    """

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        """POST metric state"""
        resp = INTERNAL_ERROR
        req = request.get_json()

        logging.info("NetworkAdapterActionsMetricStateAPI")

        for value in req.values():
            resp = set_metric_state(ident1, ident2, value, None)

        return resp
