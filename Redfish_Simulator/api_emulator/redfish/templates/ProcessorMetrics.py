# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
import random

_TEMPLATE = {
    "@odata.type": "#ProcessorMetrics.v1_6_4.ProcessorMetrics",
    "Id": "Metrics",
    "Name": "Processor Metrics",
    "BandwidthPercent": 62,
    "OperatingSpeedMHz": 2400,
    "ThrottlingCelsius": 65,
    "FrequencyRatio": 0.00432,
    "Cache": [
        {
            "Level": "3",
            "CacheMiss": 0.12,
            "HitRatio": 0.719,
            "CacheMissesPerInstruction": 0.00088,
            "OccupancyBytes": 3030144,
            "OccupancyPercent": 90.1,
        }
    ],
    "LocalMemoryBandwidthBytes": 18253611008,
    "RemoteMemoryBandwidthBytes": 81788928,
    "KernelPercent": 2.3,
    "UserPercent": 34.7,
    "CoreMetrics": [
        {
            "CoreId": "core0",
            "InstructionsPerCycle": 1.16,
            "UnhaltedCycles": 6254383746,
            "MemoryStallCount": 58372,
            "IOStallCount": 2634872,
            "CoreCache": [
                {
                    "Level": "2",
                    "CacheMiss": 0.472,
                    "HitRatio": 0.57,
                    "CacheMissesPerInstruction": 0.00346,
                    "OccupancyBytes": 198231,
                    "OccupancyPercent": 77.4,
                }
            ],
            "CStateResidency": [
                {"Level": "C0", "Residency": 1.13},
                {"Level": "C1", "Residency": 26},
                {"Level": "C3", "Residency": 0.00878},
                {"Level": "C6", "Residency": 0.361},
                {"Level": "C7", "Residency": 72.5},
            ],
        }
    ],
    "Oem": {},
    "@odata.id": "/redfish/v1/Systems/{suffix_id}/Processors/{processor_id}/ProcessorMetrics",
}


def format_ProcessorMetrics_template(**kwargs):

    defaults = {"rb": "/redfish/v1/"}

    defaults.update(kwargs)

    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**defaults)

    c["BandwidthPercent"] = random.randint(0, 100)
    return c
