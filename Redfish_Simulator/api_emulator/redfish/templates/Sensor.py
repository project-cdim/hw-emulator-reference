# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
import datetime
import logging

_TEMPLATE = {
    "@odata.type": "#Sensor.v1_10_1.Sensor",
    "Id": "CabinetTemp",
    "Name": "Rack Temperature",
    "ReadingType": "Temperature",
    "ReadingTime": "2023-06-03T04:14:00Z",
    "Status": {"State": "Enabled", "Health": "OK"},
    "Reading": 31.6,
    "ReadingUnits": "C",
    "ReadingRangeMin": 0,
    "ReadingRangeMax": 70,
    "Accuracy": 0.25,
    "Precision": 1,
    "SensorResetTime": "2023-06-03T04:14:00Z",
    "SensingInterval": "PT3S",
    "PhysicalContext": "Chassis",
    "Thresholds": {
        "UpperCritical": {"Reading": 40, "Activation": "Increasing"},
        "UpperCaution": {"Reading": 35, "Activation": "Increasing"},
        "LowerCaution": {"Reading": 10, "Activation": "Increasing"},
    },
    "Oem": {},
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/Sensors/{sen_id}",
}


def format_Sensor_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)

    now = datetime.datetime.utcnow()
    nowtime = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    c["ReadingTime"] = nowtime

    reset = now + datetime.timedelta(days=-3)
    resetTime = reset.strftime("%Y-%m-%dT%H:%M:%SZ")
    c["SensorResetTime"] = resetTime

    logging.info(kwargs)
    if "interval" in kwargs:
        c["SensingInterval"] = kwargs["interval"]

    return c
