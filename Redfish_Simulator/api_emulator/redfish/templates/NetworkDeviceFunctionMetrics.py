# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#NetworkDeviceFunctionMetrics.v1_2_0.NetworkDeviceFunctionMetrics",
    "Id": "NetworkDeviceFunctionMetrics",
    "Name": "Network Device Function Metrics",
    "TXAvgQueueDepthPercent": 13.7,
    "RXAvgQueueDepthPercent": 21.2,
    "RXFrames": 27193387,
    "RXBytes": 7754199970,
    "RXUnicastFrames": 26193387,
    "RXMulticastFrames": 1000000,
    "TXFrames": 18205770,
    "TXBytes": 9436506547,
    "TXUnicastFrames": 17205770,
    "TXMulticastFrames": 1000000,
    "TXQueuesEmpty": False,
    "RXQueuesEmpty": False,
    "TXQueuesFull": 0,
    "RXQueuesFull": 0,
    "Ethernet": {"NumOffloadedIPv4Conns": 0, "NumOffloadedIPv6Conns": 0},
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{ndf_id}/Metrics",
}


def get_NetworkDeviceFunctionMetrics_instance(**kwargs):

    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    return c
