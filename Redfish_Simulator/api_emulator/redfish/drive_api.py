# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""Drive

    Drive processing
"""

import logging
import copy
from flask import request
from flask_restful import Resource

from .templates.Drive import format_Drive_template
from .environment_metrics_api import create_environment_metrics
from .drive_metrics_api import create_drive_metrics
from .metrics_state_api import set_metric_state

from .ComputerSystem_api import ComputerSystemCollectionAPI
from .Chassis_api import ChassisCollectionAPI

members = {}

INTERNAL_ERROR = 500

config = {}


class DriveChassisAPI(Resource):
    """Chassis Drive Acquisition and Operation API
    Class to acquisition and operation Chassis Drive
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident3):
        """GET Chassis Drive"""
        if ident1 not in members:
            return "not found", 404
        if ident3 not in members[ident1]:
            return "not found", 404

        mem = copy.deepcopy(members[ident1][ident3])
        mem["@odata.id"] = f"/redfish/v1/Chassis/{ident1}/Drives/{ident3}"
        return mem, 200


class DriveSystemsAPI(Resource):
    """Systems Drive Acquisition and Operation API
    Class to acquisition and operation Systems Drive
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET Systems Drive"""
        if ident1 not in members:
            return "not found", 404
        if ident3 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident3], 200


class DriveCollectionAPI(Resource):
    """Drive Collection Management API
    Class to manage the collection of Drive
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#DriveCollection.DriveCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#DriveCollection.DriveCollection",
            "Name": "Drives Collection",
        }

    def get(self, ident):
        """GET Drive collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Drives"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_drive(**kwargs):
    """Create Drive"""
    logging.info("CreateDrive")
    drive_id = kwargs["drive_id"]
    suffix_id = kwargs["suffix_id"]
    sensor_id = kwargs["sensor_id"]
    interval = kwargs["dev_param"]["sensingInterval"]

    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][drive_id] = format_Drive_template(**kwargs)

    create_drive_metrics(
        rb=kwargs["rb"],
        suffix=kwargs["suffix"],
        suffix_id=suffix_id,
        drive_id=drive_id,
        storage_id=kwargs["storage_id"],
    )
    create_environment_metrics(
        suffix=kwargs["suffix"],
        suffix_id=suffix_id,
        chassis_id=kwargs["chassis_id"],
        schema="Drives",
        storage_id=kwargs["storage_id"],
        schema_id=drive_id,
        sensor_id=sensor_id,
        spec={"CapableSpeedGbs": members[suffix_id][drive_id]["CapableSpeedGbs"]},
        interval=interval,
    )


class DriveActionsResetAPI(Resource):
    """Drive power operation"""

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        """POST Drive power operation"""
        resp = INTERNAL_ERROR
        req = request.get_json()
        logging.info("DriveActions_ResetAPI")

        resp = self.chassis_drive_reset(req, ident1, ident2)

        self.system_drive_reset(req, ident2)

        return resp

    def chassis_drive_reset(self, req, ident1, ident2):
        """Chassis Drive reset"""
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

    def system_drive_reset(self, req, ident2):
        """Systems Drive reset"""
        system = ComputerSystemCollectionAPI().get()
        for system_url in system[0]["Members"]:

            target = "/"
            idx = system_url["@odata.id"].split(target)
            system_id = idx[-1]
            if members.get(system_id, {}).get(ident2):
                conf = members[system_id][ident2]
                conf["PowerState"] = "Off"
                for value in req.values():
                    if value in ["ForceRestart", "GracefulRestart", "ForceOn", "On"]:
                        conf["Status"]["State"] = "Enabled"
                        conf["PowerState"] = "On"

                if conf["PowerState"] == "Off":
                    set_metric_state(system_id, ident2, "action", "off")
                else:
                    set_metric_state(system_id, ident2, "action", "on")


class DriveActionsMetricStateAPI(Resource):
    """Drive metric state operation"""

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        """POST Drive metric state"""
        resp = INTERNAL_ERROR
        req = request.get_json()

        logging.info("DriveActions_MetricStateAPI")

        for value in req.values():
            resp = set_metric_state(ident1, ident2, value, None)

        return resp
