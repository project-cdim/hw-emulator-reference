# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
import random

_TEMPLATE = {
    "@odata.type": "#MemoryMetrics.v1_7_3.MemoryMetrics",
    "Name": "Memory Metrics",
    "Id": "Metrics",
    "BlockSizeBytes": 4096,
    "CurrentPeriod": {"BlocksRead": 0, "BlocksWritten": 0},
    "LifeTime": {"BlocksRead": 0, "BlocksWritten": 0},
    "OperatingSpeedMHz": 3200,
    "CapacityUtilizationPercent": 0,
    "HealthData": {
        "RemainingSpareBlockPercentage": 50,
        "LastShutdownSuccess": True,
        "DataLossDetected": False,
        "PerformanceDegraded": False,
        "PredictedMediaLifeLeftPercent": 50,
        "AlarmTrips": {
            "Temperature": True,
            "SpareBlock": False,
            "UncorrectableECCError": False,
            "CorrectableECCError": False,
        },
    },
    "BandwidthPercent": 600,
    "Oem": {},
    "@odata.id": "/redfish/v1/{suffix}/{suffix_id}/Memory/{memory_id}/MemoryMetrics",
}


def format_MemoryMetrics_template(**kwargs):

    defaults = {
        "rb": "/redfish/v1/",
        "capacitymb": 16384,
        "devicetype": "DDR4",
        "type": "DRAM",
        "operatingmodes": ["Volatile"],
    }

    defaults.update(kwargs)

    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**defaults)
    c["BandwidthPercent"] = random.randint(0, 100)
    return c
