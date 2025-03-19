# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#FabricAdapter.v1_5_3.FabricAdapter",
    "Id": "Bridge",
    "Name": "Gen-Z Bridge",
    "Manufacturer": "Contoso",
    "Model": "Gen-Z Bridge Model X",
    "PartNumber": "975999-001",
    "SparePartNumber": "152111-A01",
    "SKU": "Contoso 2-port Gen-Z Bridge",
    "SerialNumber": "2M220100SL",
    "ASICRevisionIdentifier": "A0",
    "ASICPartNumber": "53312",
    "ASICManufacturer": "Contoso",
    "FirmwareVersion": "7.4.10",
    "Status": {"State": "Enabled", "Health": "OK"},
    "Ports": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/FabricAdapters/{fa_id}/Ports"
    },
    "PCIeInterface": {
        "MaxPCIeType": "Gen4",
        "MaxLanes": 64,
        "PCIeType": "Gen4",
        "LanesInUse": 64,
    },
    "UUID": "45724775-ed3b-2214-1313-9865200c1cc1",
    "FabricType": "PCIe",
    "Location": {
        "PartLocation": {
            "LocationOrdinalValue": 1,
            "LocationType": "Slot",
        },
        "PartLocationContext": "",
    },
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/FabricAdapters/{fa_id}",
}


def format_FabricAdapter_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Ports"]["@odata.id"] = c["Ports"]["@odata.id"].format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    return c
