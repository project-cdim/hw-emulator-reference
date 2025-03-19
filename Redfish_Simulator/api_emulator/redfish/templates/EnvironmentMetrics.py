# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
import random

_TEMPLATE = {
    "@odata.type": "#EnvironmentMetrics.v1_3_2.EnvironmentMetrics",
    "Name": "Processor Environment Metrics",
    "TemperatureCelsius": {
        "DataSourceUri": "/redfish/v1/Chassis/1U/Sensors/CPU1Temp",
        "Reading": 44,
    },
    "PowerWatts": {
        "DataSourceUri": "/redfish/v1/Chassis/1U/Sensors/CPU1Power",
        "Reading": 12.87,
    },
    "FanSpeedsPercent": [
        {
            "DataSourceUri": "/redfish/v1/Chassis/1U/Sensors/CPUFan1",
            "DeviceName": "CPU #1 Fan Speed",
            "Reading": 80,
        }
    ],
    "EnergyJoules": {
        "DataSourceUri": "/redfish/v1/Chassis/{chassis_id}/Sensors/{sensor_id}",
        "Reading": 25,
    },
    "Oem": {},
    "@odata.id": "/redfish/v1/{suffix}/{suffix_id}/{schema}/{schema_id}/EnvironmentMetrics",
}


def format_EnvironmentMetrics_template(**kwargs):

    c = copy.deepcopy(_TEMPLATE)

    if kwargs["suffix"] == "Systems":
        if kwargs["schema"] == "Drives":
            c["@odata.id"] = (
                "/redfish/v1/{suffix}/{suffix_id}/Storage/{storage_id}/{schema}/{schema_id}/EnvironmentMetrics".format(
                    **kwargs
                )
            )
        else:
            c["@odata.id"] = c["@odata.id"].format(**kwargs)
    else:
        if kwargs["schema"] == "Chassis":
            c["@odata.id"] = (
                "/redfish/v1/{suffix}/{suffix_id}/EnvironmentMetrics".format(**kwargs)
            )
        else:
            c["@odata.id"] = c["@odata.id"].format(**kwargs)

    c["EnergyJoules"]["DataSourceUri"] = c["EnergyJoules"]["DataSourceUri"].format(
        **kwargs
    )

    c["EnergyJoules"]["Reading"] = random.randint(0, 100)

    return c
