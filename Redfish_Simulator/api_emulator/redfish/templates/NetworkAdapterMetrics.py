# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
import random

_TEMPLATE = {
    "@odata.type": "#NetworkAdapterMetrics.v1_1_0.NetworkAdapterMetrics",
    "Id": "NetworkAdapterMetrics",
    "Name": "Network Adapter Metrics",
    "HostBusRXPercent": 35.53,
    "HostBusTXPercent": 14.17,
    "CPUCorePercent": 8.35,
    "NCSIRXFrames": 0,
    "NCSITXFrames": 0,
    "NCSIRXBytes": 0,
    "NCSITXBytes": 0,
    "RXBytes": 7754199970,
    "RXMulticastFrames": 1941,
    "RXUnicastFrames": 27193387,
    "TXBytes": 9436506547,
    "TXMulticastFrames": 153,
    "TXUnicastFrames": 18205770,
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/Metrics",
}


def format_NetworkAdapterMetrics_template(**kwargs):

    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**kwargs)

    c["HostBusRXPercent"] = round(random.uniform(0, 100), 2)
    c["HostBusTXPercent"] = round(random.uniform(0, 100), 2)
    return c
