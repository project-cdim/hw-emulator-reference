# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md
#
# memory_api.py adapted from api_emulator/redfish/memory.py
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

# Redfish Memorys and Memory Resources. Based on version 1.0.0

import logging

from flask_restful import Resource
from flask import request

from .templates.memory import format_memory_template

from .memory_metrics_api import create_memory_metrics
from .environment_metrics_api import create_environment_metrics

from .metrics_state_api import set_metric_state

from .ComputerSystem_api import ComputerSystemCollectionAPI
from .Chassis_api import ChassisCollectionAPI

members = {}
INTERNAL_ERROR = 500


class Memory(Resource):
    """
    Memory.1.0.2.Memory
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class MemoryCollection(Resource):
    """
    Memory.1.0.2.MemoryCollection
    """

    def __init__(self, rb, suffix):
        """
        Memorys Constructor
        """
        self.config = {
            "@odata.context": f"{rb}$metadata#MemoryCollection.MemoryCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#MemoryCollection.MemoryCollection",
            "Name": "Memorys Collection"
        }

    def get(self, ident):
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Memory"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class ChassisMemoryCollection(Resource):
    """
    Memory.1.0.2.MemoryCollection
    """

    def __init__(self, rb, suffix):
        """
        Memorys Constructor
        """
        self.config = {
            "@odata.context": f"{rb}$metadata#MemoryCollection.MemoryCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#MemoryCollection.MemoryCollection",
            "Name": "Memorys Collection"
        }

    def get(self, ident):
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Memory"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_memory(**kwargs):
    suffix_id = kwargs["suffix_id"]
    memory_id = kwargs["memory_id"]
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][memory_id] = format_memory_template(**kwargs)


def create_chassis_memory(**kwargs):
    logging.info("CreateChassisMemory")
    chassis_id = kwargs["chassis_id"]
    memory_id = kwargs["memory_id"]
    suffix_id = kwargs["suffix_id"]
    sensor_id = kwargs["sensor_id"]
    interval = kwargs["dev_param"]["sensingInterval"]
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][memory_id] = format_memory_template(**kwargs)
    create_memory_metrics(
        suffix=kwargs["suffix"],
        suffix_id=suffix_id,
        memory_id=memory_id,
        spec={"CapacityMiB": members[suffix_id][memory_id]["CapacityMiB"]},
    )
    create_environment_metrics(
        suffix=kwargs["suffix"],
        suffix_id=suffix_id,
        chassis_id=chassis_id,
        schema="Memory",
        schema_id=memory_id,
        sensor_id=sensor_id,
        spec={"CapacityMiB": members[suffix_id][memory_id]["CapacityMiB"]},
        interval=interval,
    )


class MemoryActionsResetAPI(Resource):

    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        resp = INTERNAL_ERROR
        req = request.get_json()
        logging.info("MemoryActions_ResetAPI")

        resp = self.chassis_memory_reset(req, ident1, ident2)

        self.system_memory_reset(req, ident2)

        return resp

    def chassis_memory_reset(self, req, ident1, ident2):
        """Chassis Memory reset
        """

        chassis = ChassisCollectionAPI().get()
        for chassis_url in chassis[0]["Members"]:

            target = "/"
            idx = chassis_url["@odata.id"].split(target)
            chassis_id = idx[-1]
            if members.get(chassis_id, {}).get(ident2):
                conf = members[chassis_id][ident2]
                conf["PowerState"] = "Off"
                for value in req.values():
                    if value in ["ForceRestart", "GracefulRestart", "ForceOn", "On"]:
                        conf["Status"]["State"] = "Enabled"
                        conf["PowerState"] = "On"

                if conf["PowerState"] == "Off":
                    set_metric_state(chassis_id, ident2, "action", "off")
                else:
                    set_metric_state(chassis_id, ident2, "action", "on")

        resp = conf, 200

        return resp

    def system_memory_reset(self, req, ident2):
        """Systems Memory reset
        """
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


class MemoryActionsResetToDefaultsAPI(Resource):
    def __init__(self, **kwargs):
        pass

    def post(self):
        logging.info("MemoryActions_ResetToDefaultsAPI POST called")
        return (
            "POST is not a supported command for MemoryActions_ResetToDefaultsAPI",
            405,
        )


class MemoryActionsMetricStateAPI(Resource):
    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2):
        resp = INTERNAL_ERROR
        req = request.get_json()

        logging.info("MemoryActions_MetricStateAPI")

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
