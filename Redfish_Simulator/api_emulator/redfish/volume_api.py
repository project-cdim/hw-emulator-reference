# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""Volume

    Volume processing
"""

import logging
import random
from flask_restful import Resource

from .templates.Volume import format_Volume_template
from .volume_metrics_api import create_volume_metrics
from .metrics_state_api import get_metric_state, get_spec, set_spec

members = {}

INTERNAL_ERROR = 500

config = {}


class VolumeChassisAPI(Resource):
    """Volume Acquisition and Operation API
    Class to acquisition and operation Volume
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET Volume"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404

        drive_url = members[ident1][ident2]["Links"]["Drives"][0]["@odata.id"]
        target = "/"
        idx = drive_url.split(target)
        dri_id = idx[-1]

        item = set_metrics_param(ident1, ident2, ident1, dri_id)

        return item, 200


class VolumeSystemsAPI(Resource):
    """Volume Acquisition and Operation API
    Class to acquisition and operation Volume
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET Volume"""
        if ident2 not in members:
            return "not found", 404
        if ident3 not in members[ident2]:
            return "not found", 404

        drive_url = members[ident2][ident3]["Links"]["Drives"][0]["@odata.id"]
        target = "/"
        idx = drive_url.split(target)
        dri_id = idx[-1]

        item = set_metrics_param(ident2, ident3, ident2, dri_id)

        return item, 200


class VolumeChassisCollectionAPI(Resource):
    """Volume Collection Acquisition and Operation API
    Class to acquisition and operation Volume Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#VolumeCollection.VolumeCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#VolumeCollection.VolumeCollection",
            "Name": "Volumes Collection",
        }

    def get(self, ident):
        """GET Volume collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Volumes"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class VolumeSystemsCollectionAPI(Resource):
    """Volume Collection Acquisition and Operation API
    Class to acquisition and operation Volume Collection
    """

    def __init__(self, rb):
        self.config = {
            "@odata.context": f"{rb}$metadata#VolumeCollection.VolumeCollection",
            "@odata.id": f"{rb}Systems",
            "@odata.type": "#VolumeCollection.VolumeCollection",
            "Name": "Volumes Collection",
        }

    def get(self, ident1, ident2):
        """GET Volume collection"""
        try:
            if ident2 not in members:
                return 404
            procs = []
            for p in members.get(ident2, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident1}/Storage/{ident2}/Volumes"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_volume(**kwargs):
    """Create Volume"""
    logging.info("CreateVolume")
    volume_id = kwargs["volume_id"]
    drive_id = kwargs["drive_id"]
    storage_id = kwargs["storage_id"]

    if storage_id not in members:
        members[storage_id] = {}
    members[storage_id][volume_id] = format_Volume_template(**kwargs)

    create_volume_metrics(
        rb=kwargs["rb"],
        suffix=kwargs["suffix"],
        suffix_id=kwargs["suffix_id"],
        storage_id=storage_id,
        volume_id=volume_id,
    )

    set_spec(storage_id, drive_id, kwargs["spec"])


def set_metrics_param(ident1, ident2, storage_id, dri_id):
    """Set Metrics parameter"""

    logging.info("setMetricsParam")

    spec = get_spec(storage_id, dri_id)

    item = members[ident1][ident2]

    state = get_metric_state(storage_id, dri_id)

    item["RemainingCapacityPercent"] = set_param(state, spec)

    return item


METRIC_STATE = {
    1: {"steady": [0, 40], "low": [10, 30], "high": [80, 100], "action": [60, 80]},
    2: {"steady": [0, 20], "low": [20, 40], "high": [70, 90], "action": [50, 70]},
    3: {"steady": [0, 10], "low": [10, 30], "high": [60, 80], "action": [40, 60]},
}


def set_param(state, spec):
    """Set parameter"""
    resp = random.randint(0, 100)
    if state == "off":
        resp = 0
        return resp

    resp = random.randint(METRIC_STATE[spec][state][0], METRIC_STATE[spec][state][1])

    return resp
