# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""MetricsState

    MetricsState processing
"""

import time
import logging
import threading

from flask_restful import Resource


STATE = "steady"
stateList = ["off", "steady", "low", "high", "action"]

setaction = {"tread": {}, "valid": False}

spec = {}

INTERNAL_ERROR = 500


class MetricsStateAPI(Resource):
    """Class to set metric state
    A class that manipulates metric state through user operations.
    """

    # kwargs is use to pass in the wildcards values to replace when the instance is created.
    def __init__(self, **kwargs):
        pass

    def post(self, ident1, ident2, ident3):
        """POST metric state"""
        return set_metric_state(ident1, ident2, ident3, None)

    def get(self):
        """GET metric state"""
        return "GET is not supported", 405, {"Allow": "POST"}

    def patch(self):
        """PATCH metric state"""
        return "PATCH is not supported", 405, {"Allow": "POST"}

    def put(self):
        """PUT metric state"""
        return "PUT is not supported", 405, {"Allow": "POST"}

    def delete(self):
        """DELETE metric state"""
        return "DELETE is not supported", 405, {"Allow": "POST"}


def set_metric_state(sys_id, device_id, ident, power):
    """Metric state change function
    A function to change the state of the metric state
    """
    resp = INTERNAL_ERROR
    if spec.get(sys_id, {}).get(device_id):

        if ident in stateList:
            if ident == "action" and setaction["valid"] is False:
                setaction["valid"] = True
                setaction["tread"] = threading.Thread(
                    target=set_action_state,
                    args=[sys_id, device_id, power],
                    daemon=True,
                )
                setaction["tread"].start()  # pylint: disable=E1101

            spec[sys_id][device_id]["state"] = ident
            resp = spec[sys_id][device_id]["state"], 200

    return resp


def set_action_state(sys_id, device_id, power):
    """Metric state change function in Action operation
    A function to change and manage the state of a metric state through an action operation
    """

    if spec.get(sys_id, {}).get(device_id):

        logging.info(spec[sys_id][device_id]["state"])
        time.sleep(5)

        if power is not None and power == "off":
            spec[sys_id][device_id]["state"] = "off"
        else:
            spec[sys_id][device_id]["state"] = "steady"

        setaction["valid"] = False

        logging.info(spec[sys_id][device_id]["state"])


def get_metric_state(sys_id, device_id):
    """Metric state get function
    A function to get the state of the metric state
    """
    resp = None
    if spec.get(sys_id, {}).get(device_id):
        resp = spec[sys_id][device_id]["state"]

    return resp


ITEM_SPEC = {
    "TotalEnabledCores": {2: 1, 4: 2, 8: 3},
    "CapacityMiB": {2048: 1, 4096: 2, 8192: 3},
    "CapableSpeedGbs": {2800: 1, 3200: 2, 3600: 3},
    "BitRate": {"4800": 1, "9600": 2, "19200": 3},
}


def set_spec(sys_id, device_id, item):
    """Device spec set function
    A function to set the spec of the device
    """

    logging.info("setSpec")

    if sys_id not in spec:
        spec[sys_id] = {}

    if device_id not in spec[sys_id]:
        spec[sys_id][device_id] = {}
        spec[sys_id][device_id]["state"] = "steady"

    for key, value in ITEM_SPEC.items():
        if key in item:
            spec[sys_id][device_id]["spec"] = value[item[key]]


def get_spec(ident1, ident2):
    """Device spec get function
    A function to get the spec of the device
    """
    return spec[ident1][ident2]["spec"]
