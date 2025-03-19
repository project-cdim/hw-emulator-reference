# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#PCIeFunction.v1_6_0.PCIeFunction",
    "Id": "{pcie_f_id}",
    "Name": "FC Port 2",
    "Description": "FC Port 2",
    "FunctionId": 2,
    "FunctionType": "Physical",
    "DeviceClass": "NetworkController",
    "DeviceId": "0x{pcie_d_id}",
    "VendorId": "0x{pcie_v_id}",
    "ClassCode": "0x010802",
    "RevisionId": "0x00",
    "SubsystemId": "0xABCD",
    "SubsystemVendorId": "0xABCD",
    "FunctionProtocol": "PCIe",
    "Status": {"State": "Enabled", "Health": "OK", "HealthRollup": "OK"},
    "Links": {
        "PCIeDevice": {
            "@odata.id": "/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pcie_id}"
        }
    },
    "Oem": {},
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pcie_id}/PCIeFunctions/{pcie_f_id}",
}


def format_PCIeFunction_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Id"] = c["Id"].format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    c["Links"]["PCIeDevice"]["@odata.id"] = c["Links"]["PCIeDevice"][
        "@odata.id"
    ].format(**kwargs)

    if kwargs.get("pcie_d_id") is not None:
        c["DeviceId"] = c["DeviceId"].format(**kwargs)
    else:
        c["DeviceId"] = "0xABCD"

    if kwargs.get("pcie_v_id") is not None:
        c["VendorId"] = c["VendorId"].format(**kwargs)
    else:
        c["VendorId"] = "0xABCD"

    return c
