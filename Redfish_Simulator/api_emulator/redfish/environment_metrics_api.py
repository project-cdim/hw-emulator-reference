# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""EnvironmentMetrics

    EnvironmentMetrics processing
"""

import logging
import random

from flask_restful import Resource

import g

from .templates.EnvironmentMetrics import format_EnvironmentMetrics_template
from .sensor_api import create_sensor

from .metrics_state_api import get_metric_state, get_spec, set_spec

members = {}

INTERNAL_ERROR = 500

config = {}


class EnvironmentMetricsAPI(Resource):
    """EnvironmentMetrics Acquisition and Operation API
    Class to acquisition and operation EnvironmentMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET EnvironmentMetrics"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404

        item = set_metrics_param(ident1, ident2)
        return item, 200


class EnvironmentMetricsChassisAPI(Resource):
    """Chassis EnvironmentMetrics Acquisition and Operation API
    Class to acquisition and operation Chassis EnvironmentMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1):
        """GET Chassis Drive"""
        resp = 404
        if ident1 not in members:
            return "not found", 404
        if ident1 not in members[ident1]:
            return "not found", 404
        resp = members[ident1][ident1]

        return resp, 200


class EnvironmentMetricsSystemsAPI(Resource):
    """Systems EnvironmentMetrics Acquisition and Operation API
    Class to acquisition and operation Systems EnvironmentMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET Systems Drive"""
        if ident1 not in members:
            return "not found", 404
        if ident3 not in members[ident1]:
            return "not found", 404

        item = set_metrics_param(ident1, ident3)
        return item, 200


def create_environment_metrics(**kwargs):
    """Create EnvironmentMetrics"""
    logging.info("CreateEnvironmentMetrics")
    schema_id = kwargs["schema_id"]
    suffix = kwargs["suffix"]
    suffix_id = kwargs["suffix_id"]
    chassis_id = kwargs["chassis_id"]
    sensor_id = kwargs["sensor_id"]
    interval = kwargs["interval"]
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][schema_id] = format_EnvironmentMetrics_template(**kwargs)

    create_sensor(
        rb=g.rest_base,
        suffix=suffix,
        sen_id=sensor_id,
        suffix_id=suffix_id,
        chassis_id=chassis_id,
        interval=interval,
    )

    if kwargs.get("spec"):
        set_spec(suffix_id, schema_id, kwargs["spec"])
        set_spec(chassis_id, schema_id, kwargs["spec"])


def set_metrics_param(ident1, ident2):
    """Set Metrics parameter"""
    logging.info("setMetricsParam")

    spec = get_spec(ident1, ident2)

    item = members[ident1][ident2]

    state = get_metric_state(ident1, ident2)

    item["EnergyJoules"]["Reading"] = set_param(state, spec)

    return item


METRIC_STATE = {
    1: {"steady": [0, 10], "low": [10, 30], "high": [40, 60], "action": [30, 50]},
    2: {"steady": [0, 20], "low": [20, 40], "high": [70, 90], "action": [90, 100]},
    3: {"steady": [0, 30], "low": [40, 60], "high": [90, 100], "action": [70, 90]},
}


def set_param(state, spec):
    """Set parameter"""
    resp = random.randint(0, 100)
    if state == "off":
        resp = 0
        return resp

    resp = random.randint(METRIC_STATE[spec][state][0], METRIC_STATE[spec][state][1])

    return resp
