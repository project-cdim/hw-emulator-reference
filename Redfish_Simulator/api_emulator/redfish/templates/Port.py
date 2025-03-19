# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy


_TEMPLATE = {
    "@odata.type": "#Port.v1_15_0.Port",
    "Id": "{port_id}",
    "Name": "SAS Port 1",
    "Description": "SAS Port 1",
    "Status": {"State": "Enabled", "Health": "OK"},
    "PortType": "BidirectionalPort",
    "CXL": {
        "ConnectedDeviceMode": "CXL68BFlitAndVH",
        "ConnectedDeviceType": "PCIeDevice",
        "CurrentPortConfigurationState": "USP",
        "MaxLogicalDeviceCount": 4,
        "SupportedCXLModes": ["CXL68BFlitAndVH"],
    },
    "Oem": {},
    "@odata.id": "/redfish/v1/{suffix}/{suffix_id}/{adapter}/{adapter_id}/Ports/{port_id}",
}

_TEMPLATE_ADAPTER = {
    "@odata.type": "#Port.v1_15_0.Port",
    "Id": "{port_id}",
    "Name": "SAS Port 1",
    "Description": "SAS Port 1",
    "Status": {"State": "Enabled", "Health": "OK"},
    "PortProtocol": "SAS",
    "PortType": "BidirectionalPort",
    "CurrentSpeedGbps": 48,
    "Width": 4,
    "MaxSpeedGbps": 48,
    "CXL": {
        "ConnectedDeviceMode": "CXL68BFlitAndVH",
        "ConnectedDeviceType": "PCIeDevice",
        "CurrentPortConfigurationState": "USP",
        "MaxLogicalDeviceCount": 4,
        "SupportedCXLModes": ["CXL68BFlitAndVH"],
    },
    "FunctionMaxBandwidth": [{"AllocationPercent": 80}],
    "FunctionMinBandwidth": [{"AllocationPercent": 80}],
    "LinkConfiguration": [{"CapableLinkSpeedGbps": [10, 40]}],
    "Actions": {"Oem": {}},
    "Oem": {},
    "@odata.id": "/redfish/v1/{suffix}/{suffix_id}/{adapter}/{adapter_id}/Ports/{port_id}",
}


def format_Port_template(**kwargs):

    if kwargs["adapter"] == "NetworkAdapters" or kwargs["adapter"] == "FabricAdapters":
        c = copy.deepcopy(_TEMPLATE_ADAPTER)
    else:
        c = copy.deepcopy(_TEMPLATE)

    c["Id"] = c["Id"].format(**kwargs)
    if kwargs["adapter"] == "Controllers":
        c["@odata.id"] = (
            "/redfish/v1/{suffix}/{suffix_id}/Storage/{storage_id}/{adapter}/{adapter_id}/Ports/{port_id}".format(
                **kwargs
            )
        )
    else:
        c["@odata.id"] = c["@odata.id"].format(**kwargs)
    return c
