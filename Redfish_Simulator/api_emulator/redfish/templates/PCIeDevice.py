# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE

import copy

_TEMPLATE = {
    "@odata.type": "#PCIeDevice.v1_17_0.PCIeDevice",
    "Id": "{pcie_id}",
    "Name": "Simple Two-Port NIC",
    "Description": "Simple Two-Port NIC PCIe Device",
    "AssetTag": "ORD-4302015-18432RS",
    "Manufacturer": "Contoso",
    "Model": "SuperNIC 2000",
    "SKU": "89587433",
    "SerialNumber": "{SerialNumber}",
    "PartNumber": "232-4598D7",
    "DeviceType": "MultiFunction",
    "FirmwareVersion": "12.342-343",
    "Status": {"State": "Enabled", "Health": "OK", "HealthRollup": "OK"},
    "PCIeInterface": {
        "PCIeType": "Gen2",
        "MaxPCIeType": "Gen3",
        "LanesInUse": 4,
        "MaxLanes": 4,
    },
    "Slot": {
        "Lanes": 16,
        "Location": {
            "PartLocation": {
                "LocationOrdinalValue": 0,
                "LocationType": "Slot",
            },
        },
        "PCIeType": "Gen5",
        "SlotType": "OEM",
    },
    "CXLDevice": {"DeviceType": "Simulated", "MaxNumberLogicalDevices": 1},
    "CXLLogicalDevices": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pcie_id}/CXLLogicalDevices"
    },
    "PCIeFunctions": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pcie_id}/PCIeFunctions"
    },
    "Links": {
        "Chassis": [{"@odata.id": "/redfish/v1/Chassis/{chassis_id}"}],
        "Oem": {},
    },
    "Oem": {},
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/PCIeDevices/{pcie_id}",
}


def format_PCIeDevice_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Id"] = c["Id"].format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)

    if kwargs.get("SerialNumber") is not None:
        c["SerialNumber"] = c["SerialNumber"].format(**kwargs)
    else:
        c["SerialNumber"] = "2M220100SL"

    c["Links"]["Chassis"][0]["@odata.id"] = c["Links"]["Chassis"][0][
        "@odata.id"
    ].format(**kwargs)
    c["PCIeFunctions"]["@odata.id"] = c["PCIeFunctions"]["@odata.id"].format(**kwargs)
    c["CXLLogicalDevices"]["@odata.id"] = c["CXLLogicalDevices"]["@odata.id"].format(
        **kwargs
    )

    return c
