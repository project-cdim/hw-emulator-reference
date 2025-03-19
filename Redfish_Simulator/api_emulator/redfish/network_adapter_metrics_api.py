# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""NetworkAdapterMetrics

    NetworkAdapterMetrics processing
"""

import traceback
import logging
import random
from flask_restful import Resource
import g

from .templates.NetworkAdapterMetrics import format_NetworkAdapterMetrics_template
from .metrics_state_api import get_metric_state, get_spec, set_spec

members = {}

INTERNAL_ERROR = 500

config = {}


class NetworkAdapterMetricsAPI(Resource):
    """NetworkAdapterMetric Acquisition and Operation API
    Class to acquisition and operation NetworkAdapterMetric
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET  NetworkAdapterMetric"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404

        item = set_metrics_param(ident1, ident2)

        return item, 200


class NetworkAdapterMetricsCollectionAPI(Resource):
    """NetworkAdapterMetric Collection Management API
    Class to manage the collection of NetworkAdapterMetric
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
        """GET  NetworkAdapterMetric collection"""
        try:
            resp = self.config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


def create_network_adapter_metrics(**kwargs):
    """Create NetworkAdapterMetric"""
    logging.info("CreateNetworkAdapterMetrics")
    na_id = kwargs["na_id"]
    chassis_id = kwargs["chassis_id"]
    if chassis_id not in members:
        members[chassis_id] = {}
    members[chassis_id][na_id] = format_NetworkAdapterMetrics_template(**kwargs)

    set_spec(chassis_id, na_id, kwargs["spec"])


def set_metrics_param(ident1, ident2):
    """Set Metrics parameter"""

    logging.info("setMetricsParam")

    spec = get_spec(ident1, ident2)

    item = members[ident1][ident2]

    state = get_metric_state(ident1, ident2)

    item["HostBusRXPercent"] = set_param(state, spec)
    item["HostBusTXPercent"] = set_param(state, spec)

    return item


METRIC_STATE = {
    1: {"steady": [0, 40], "low": [40, 60], "high": [80, 100], "action": [60, 80]},
    2: {"steady": [0, 20], "low": [20, 40], "high": [70, 90], "action": [50, 70]},
    3: {"steady": [0, 10], "low": [10, 30], "high": [60, 80], "action": [40, 60]},
}


def set_param(state, spec):
    """Set parameter"""
    resp = round(random.uniform(0, 100), 2)
    if state == "off":
        resp = round(0, 2)
        return resp

    resp = round(
        random.uniform(METRIC_STATE[spec][state][0], METRIC_STATE[spec][state][1]), 2
    )

    return resp
