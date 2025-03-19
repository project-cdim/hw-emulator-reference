# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""MemoryMetrics
    MemoryMetrics processing
"""

import traceback
import logging
import random
from flask_restful import Resource
import g

from .templates.MemoryMetrics import format_MemoryMetrics_template

from .metrics_state_api import get_metric_state, get_spec, set_spec

members = {}

INTERNAL_ERROR = 500

config = {}


class MemoryMetricsAPI(Resource):
    """MemoryMetrics Acquisition and Operation API
    Class to acquisition and operation MemoryMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET MemoryMetrics"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404

        item = set_metrics_param(ident1, ident2)

        return item, 200


class MemoryMetricsCollectionAPI(Resource):
    """MemoryMetrics Collection Management API
    Class to manage the collection of MemoryMetrics
    """

    def __init__(self):
        self.rb = g.rest_base

        self.config = {
            "@odata.type": "#MemoryMetricsCollection.MemoryMetricsCollection",
            "Name": "MemoryMetrics",
            "Members@odata.count": {},
            "Members": {},
        }
        self.config["Members@odata.count"] = len(members)
        self.config["Members"] = [
            {"@odata.id": x["@odata.id"]} for x in list(members.values())
        ]

    def get(self):
        """GET MemoryMetrics Collection"""
        try:
            resp = self.config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


def create_memory_metrics(**kwargs):
    """Create MemoryMetrics"""
    logging.info("CreateMemoryMetrics")
    memory_id = kwargs["memory_id"]
    suffix_id = kwargs["suffix_id"]
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][memory_id] = format_MemoryMetrics_template(**kwargs)

    if kwargs.get("spec"):
        set_spec(suffix_id, memory_id, kwargs["spec"])


def set_metrics_param(ident1, ident2):
    """Set Metrics parameter"""

    logging.info("setMetricsParam")

    spec = get_spec(ident1, ident2)

    item = members[ident1][ident2]

    state = get_metric_state(ident1, ident2)

    item["BandwidthPercent"] = set_param(state, spec)

    return item


METRIC_STATE = {
    1: {"steady": [0, 40], "low": [40, 60], "high": [80, 100], "action": [60, 80]},
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
