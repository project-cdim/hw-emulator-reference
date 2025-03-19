# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#CXLLogicalDevice.v1_2_1.CXLLogicalDevice",
    "Id": "{cxl_id}",
    "Name": "CXL Logical Device Type 1",
    "Description": "Locally attached CXL Logical Device Type 1",
    "Identifiers": [
        {"DurableName": "4C-1D-96-FF-FE-DD-D8-35:0001", "DurableNameFormat": "GCXLID"}
    ],
    "MemorySizeMiB": 8192,
    "QoS": {"AllocatedBandwidth": 10, "LimitPercent": 80},
    "Status": {"State": "Enabled", "Health": "OK"},
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pcie_id}/CXLLogicalDevices/{cxl_id}",
}


def format_CXLLogicalDevice_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Id"] = c["Id"].format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)

    return c
