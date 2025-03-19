# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#GraphicsController.v1_0_2.GraphicsController",
    "Id": "{gc_id}",
    "Name": "Contoso Graphics Controller 1",
    "AssetTag": "",
    "Manufacturer": "Contoso",
    "Model": "{model}",
    "SKU": "80937",
    "SerialNumber": "{gc_sereal}",
    "PartNumber": "G37891",
    "SparePartNumber": "G37890",
    "BiosVersion": "90.02.17.00.7D",
    "DriverVersion": "27.21.14.6079 (Contoso 460.79) DCH / Win 10 64",
    "Status": {"State": "Enabled", "Health": "OK"},
    "Location": {
        "PartLocation": {
            "ServiceLabel": "Slot 1",
            "LocationOrdinalValue": 1,
            "LocationType": "Slot",
            "Orientation": "LeftToRight",
            "Reference": "Rear",
        }
    },
    "Links": {"Processors": [], "PCIeDevice": {}},
    "Oem": {},
    "@odata.id": "/redfish/v1/Systems/{suffix_id}/GraphicsControllers/{gc_id}",
}


def format_GraphicsController_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Id"] = c["Id"].format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    c["Model"] = c["Model"].format(**kwargs)
    if kwargs.get("gc_sereal") is not None:
        c["SerialNumber"] = c["SerialNumber"].format(**kwargs)
    if "state" in kwargs["dev_param"]:
        c["Status"]["State"] = kwargs["dev_param"]["state"]
    if "health" in kwargs["dev_param"]:
        c["Status"]["Health"] = kwargs["dev_param"]["health"]

    return c
