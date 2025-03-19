# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


from copy import deepcopy

_TEMPLATE = {
    "@odata.context": "{rb}$metadata#NetworkInterface.NetworkInterface",
    "@odata.type": "#NetworkInterface.v1_2_2.NetworkInterface",
    "Id": "{ni_id}",
    "Name": "Network Device View",
    "Ports": {"@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}/Ports"},
    "NetworkDeviceFunctions": {
        "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions"
    },
    "Links": {
        "NetworkAdapter": {
            "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}"
        }
    },
    "@odata.id": "{rb}{suffix}/{suffix_id}/NetworkInterfaces/{ni_id}",
}


def format_NetworkInterface_template(**kwargs):
    defaults = {"rb": "/redfish/v1/", "suffix": "Systems"}

    defaults.update(kwargs)
    c = deepcopy(_TEMPLATE)
    c["Id"] = c["Id"].format(**defaults)
    c["@odata.context"] = c["@odata.context"].format(**defaults)
    c["@odata.id"] = c["@odata.id"].format(**defaults)
    c["NetworkDeviceFunctions"]["@odata.id"] = c["NetworkDeviceFunctions"][
        "@odata.id"
    ].format(**defaults)
    c["Ports"]["@odata.id"] = c["Ports"]["@odata.id"].format(**defaults)
    c["Links"]["NetworkAdapter"]["@odata.id"] = c["Links"]["NetworkAdapter"][
        "@odata.id"
    ].format(**defaults)

    return c
