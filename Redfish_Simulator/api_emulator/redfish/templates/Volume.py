# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#Volume.v1_10_1.Volume",
    "Id": "2",
    "Name": "Virtual Disk 2",
    "Status": {"State": "Enabled", "Health": "OK"},
    "Encrypted": False,
    "RAIDType": "RAID0",
    "CapacityBytes": 899527000000,
    "Identifiers": [
        {
            "DurableNameFormat": "UUID",
            "DurableName": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        }
    ],
    "AccessCapabilities": ["Append", "Read"],
    "OptimumIOSizeBytes": 8096,
    "MaxBlockSizeBytes": 1024,
    "BlockSizeBytes": 512,
    "RecoverableCapacitySourceCount": 16,
    "RemainingCapacityPercent": 20,
    "Manufacturer": "Contoso",
    "Model": "Modelxx123",
    "DisplayName": "Name123",
    "VolumeType": "Mirrored",
    "VolumeUsage": "SystemData",
    "Capacity": {
        "Data": {
            "AllocatedBytes": 104857600,
            "ConsumedBytes": 1024000,
            "GuaranteedBytes": 104857600,
            "ProvisionedBytes": 107374182400,
        },
        "Metadata": {
            "AllocatedBytes": 104857600,
            "ConsumedBytes": 0,
            "GuaranteedBytes": 104857600,
            "ProvisionedBytes": 107374182400,
        },
        "Snapshot": {
            "AllocatedBytes": 104857600,
            "ConsumedBytes": 0,
            "GuaranteedBytes": 104857600,
            "ProvisionedBytes": 107374182400,
        },
    },
    "Metrics": {
        "@odata.id": "/redfish/v1/{suffix}/{storage_id}/Volumes/{volume_id}/Metrics"
    },
    "Links": {
        "Drives": [{"@odata.id": "/redfish/v1/Chassis/{chassis_id}/Drives/{drive_id}"}]
    },
    "@odata.id": "/redfish/v1/{suffix}/{storage_id}/Volumes/{volume_id}",
}


def format_Volume_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    defaults = {
        "rb": "/redfish/v1/",
        "suffix": "Storage",
        "capacitymb": 16384,
        "devicetype": "DDR4",
        "type": "DRAM",
        "operatingmodes": ["Volatile"],
    }

    defaults.update(kwargs)

    if kwargs["suffix"] == "Systems":
        c["Links"]["Drives"][0]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Drives/{drive_id}".format(
                **defaults
            )
        )
        c["Metrics"]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Volumes/{volume_id}/Metrics".format(
                **defaults
            )
        )
        c["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Volumes/{volume_id}".format(
                **defaults
            )
        )
    else:
        c["Links"]["Drives"][0]["@odata.id"] = (
            "{rb}Chassis/{chassis_id}/Drives/{drive_id}".format(**defaults)
        )
        c["Metrics"]["@odata.id"] = (
            "{rb}Storage/{storage_id}/Volumes/{volume_id}/Metrics".format(**defaults)
        )
        c["@odata.id"] = "{rb}Storage/{storage_id}/Volumes/{volume_id}".format(
            **defaults
        )

    c["CapacityBytes"] = defaults["capacitygb"] * 1048576

    c["Identifiers"][0]["DurableName"] = (
        "ba123bd1-04bd-40a5-9773-6a647a3f{dri_sereal}".format(**defaults)
    )

    return c
