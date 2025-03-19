# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md
#
# processor_api.py adapted from api_emulator/redfish/processor.py
# The original DMTF contents of this file have been modified to support
# The Redfish Interface Emulator. These modifications are subject to the following:
# Copyright 2025 NEC Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Redfish Processors and Processor Resources. Based on version 1.0.0

import logging
import json
import os
from flask_restful import Resource
from flask import request

from .templates.processor import format_processor_template
from .processor_metrics_api import create_processor_metrics
from .environment_metrics_api import create_environment_metrics
from .memory_metrics_api import create_memory_metrics

from .ComputerSystem_api import ComputerSystemCollectionAPI, ComputerSystemActions_ResetAPI
from .Chassis_api import ChassisCollectionAPI

from .memory_api import MemoryActionsResetAPI
from .drive_api import DriveActionsResetAPI
from .network_adapter_api import NetworkAdapterActionsResetAPI

from .metrics_state_api import set_metric_state

members = {}
INTERNAL_ERROR = 500
DEVICE_POWER_LINK = None
DEVICE_LIST = "emulator-config_device_populate.json"


class Processor(Resource):
    """
    Processor.1.0.0.Processor
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        if ident1 not in members:
            return "ResourceNotFound", 404
        if ident2 not in members[ident1]:
            return "ResourceNotFound", 404
        return members[ident1][ident2], 200


class Processors(Resource):
    """
    Processor.1.0.0.ProcessorCollection
    """

    def __init__(self, rb, suffix):
        """
        Processors Constructor
        """
        self.config = {
            "@odata.context": f"{rb}$metadata#ProcessorCollection.ProcessorCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#ProcessorCollection.ProcessorCollection",
            "Name": "Processors Collection"
        }

    def get(self, ident):
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Processors"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class ChassisProcessors(Resource):
    """
    Processor.1.0.0.ProcessorCollection
    """

    def __init__(self, rb, suffix):
        """
        Processors Constructor
        """
        self.config = {
            "@odata.context": f"{rb}$metadata#ProcessorCollection.ProcessorCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#ProcessorCollection.ProcessorCollection",
            "Name": "Processors Collection"
        }

    def get(self, ident):
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Processors"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_processor(**kwargs):
    logging.info("CreateProcessor")

    suffix_id = kwargs["suffix_id"]
    chassis_id = kwargs["chassis_id"]
    processor_id = kwargs["processor_id"]
    sensor_id = kwargs["sensor_id"]
    interval = kwargs["dev_param"]["sensingInterval"]
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][processor_id] = format_processor_template(**kwargs)

    if kwargs["sys_id"]:
        create_processor_metrics(
            suffix=kwargs["suffix"],
            suffix_id=kwargs["sys_id"],
            chassis_id=chassis_id,
            processor_id=processor_id,
            spec={
                "TotalEnabledCores": members[suffix_id][processor_id]["TotalEnabledCores"]
            },
        )
        create_environment_metrics(
            suffix=kwargs["suffix"],
            suffix_id=kwargs["sys_id"],
            chassis_id=chassis_id,
            schema="Processors",
            schema_id=processor_id,
            sensor_id=sensor_id,
            spec={
                "TotalEnabledCores": members[suffix_id][processor_id]["TotalEnabledCores"]
            },
            interval=interval,
        )
        create_memory_metrics(
            suffix=kwargs["suffix"],
            suffix_id=kwargs["sys_id"],
            memory_id=processor_id
        )

    if "power_link" in kwargs:
        global DEVICE_POWER_LINK  # pylint: disable=W0603
        DEVICE_POWER_LINK = kwargs["power_link"]


class ProcessorActionsResetAPI(Resource):

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        resp = INTERNAL_ERROR

        resp = post_power(ident2)

        if DEVICE_POWER_LINK:
            chassis = ChassisCollectionAPI().get()
            for chassis_url in chassis[0]["Members"]:
                target = "/"
                idx = chassis_url["@odata.id"].split(target)
                chassis_id = idx[-1]
                set_in_device_power(chassis_id, ident2)

        return resp


def post_power(ident):
    logging.info("ProcessorActions_ResetAPI")

    req = request.get_json()

    resp = chassis_processor_reset(req, ident)

    system_processor_reset(req, ident)

    return resp


def chassis_processor_reset(req, ident):
    """Chassis Processor reset
    """
    chassis = ChassisCollectionAPI().get()
    for chassis_url in chassis[0]["Members"]:
        target = "/"
        idx = chassis_url["@odata.id"].split(target)
        chassis_id = idx[-1]
        if members.get(chassis_id, {}).get(ident):
            conf = members[chassis_id][ident]
            conf["PowerState"] = "Off"
            for value in req.values():
                if value in ["ForceRestart", "GracefulRestart", "ForceOn", "On"]:
                    conf["Status"]["State"] = "Enabled"
                    conf["PowerState"] = "On"

            if conf["PowerState"] == "Off":
                set_metric_state(chassis_id, ident, "action", "off")
            else:
                set_metric_state(chassis_id, ident, "action", "on")

    resp = conf, 200

    return resp


def system_processor_reset(req, ident):
    """Systems Processor reset
    """

    system = ComputerSystemCollectionAPI().get()
    for system_url in system[0]["Members"]:

        target = "/"
        idx = system_url["@odata.id"].split(target)
        system_id = idx[-1]
        if members.get(system_id, {}).get(ident):
            conf = members[system_id][ident]
            conf["PowerState"] = "Off"
            for value in req.values():
                if value in ["ForceRestart", "GracefulRestart", "ForceOn", "On"]:
                    conf["Status"]["State"] = "Enabled"
                    conf["PowerState"] = "On"

            ComputerSystemActions_ResetAPI().post(system_id)

            if conf["PowerState"] == "Off":
                set_metric_state(system_id, ident, "action", "off")
            else:
                set_metric_state(system_id, ident, "action", "on")


def set_in_device_power(chassis_id, ident2):
    logging.info("set_in_device_power")

    device_list = get_device_list()

    target = "-"
    idx = ident2.split(target)
    cpu_id = idx[-1]
    for cpu_template in device_list.get("cpu"):
        if cpu_id == cpu_template.get("deviceID"):
            for indevice in cpu_template.get("link"):
                device_action_api_call(indevice.get("deviceID"), chassis_id)


def device_action_api_call(indevice_id, chassis_id):
    if indevice_id.startswith("10"):
        device_id = "MEM-" + indevice_id
        MemoryActionsResetAPI().post(chassis_id, device_id)

    if indevice_id.startswith("20"):
        device_id = "DRI-" + indevice_id
        DriveActionsResetAPI().post(chassis_id, device_id)

    if indevice_id.startswith("30"):
        device_id = "NIC-" + indevice_id
        NetworkAdapterActionsResetAPI().post(chassis_id, device_id)

    if indevice_id.startswith("50"):
        device_id = "PROC-" + indevice_id
        post_power(device_id)


def get_device_list():
    device_list = None

    if os.path.exists(DEVICE_LIST):
        with open(DEVICE_LIST, "r") as f:  # pylint: disable=W1514
            infragen_config = json.load(f)
            with open(infragen_config["POPULATE"], "r") as f:  # pylint: disable=W1514
                device_list = json.load(f)

    return device_list


class ProcessorActionsResetToDefaultsAPI(Resource):
    def __init__(self, **kwargs):
        pass

    def post(self):
        logging.info("ProcessorActions_ResetToDefaultsAPI")
        return (
            "POST is not a supported command for ProcessorActions_ResetToDefaultsAPI",
            405,
        )


class ProcessorActionsMetricStateAPI(Resource):
    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        resp = INTERNAL_ERROR
        req = request.get_json()

        logging.info("ProcessorActions_MetricStateAPI")

        for value in req.values():
            if chassis_id := self.get_chassis_device(ident2):
                resp = set_metric_state(chassis_id, ident2, value, None)
            if system_id := self.get_system_device(ident2):
                set_metric_state(system_id, ident2, value, None)

        return resp

    def get_system_device(self, ident):
        system = ComputerSystemCollectionAPI().get()
        for system_url in system[0]["Members"]:

            target = "/"
            idx = system_url["@odata.id"].split(target)
            system_id = idx[-1]
            if members.get(system_id, {}).get(ident):
                return system_id

        return None

    def get_chassis_device(self, ident):
        chassis = ChassisCollectionAPI().get()
        for chassis_url in chassis[0]["Members"]:
            target = "/"
            idx = chassis_url["@odata.id"].split(target)
            chassis_id = idx[-1]
            if members.get(chassis_id, {}).get(ident):
                return chassis_id

        return None
