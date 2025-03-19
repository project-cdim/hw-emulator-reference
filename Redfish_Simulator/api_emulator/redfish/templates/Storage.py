# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


from copy import deepcopy


_TEMPLATE = {
    "@odata.type": "#Storage.v1_18_0.Storage",
    "Id": "{storage_id}",
    "Name": "Local Storage Controller",
    "Description": "Integrated RAID Controller",
    "Status": {"State": "Enabled", "Health": "OK", "HealthRollup": "OK"},
    "Redundancy": [
        {
            "RedundancyEnabled": True,
            "Mode": "Sharing",
            "Name": "Name",
            "MaxNumSupported": 2,
            "MinNumNeeded": 1,
            "RedundancySet": [],
            "Status": {"State": "Enabled", "Health": "OK"},
        }
    ],
    "Controllers": {},
    "Drives": [],
    "Volumes": {},
    "Links": {},
    "@odata.id": "{url}",
}


def format_storage_template(**kwargs):
    """
    Format the processor template -- returns the template
    """

    c = deepcopy(_TEMPLATE)
    c["@odata.id"] = kwargs["url"]
    c["Id"] = c["Id"].format(**kwargs)

    if kwargs["suffix"] == "Systems":
        controllers = {
            "@odata.id": "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Controllers".format(
                rb=kwargs["rb"],
                suffix=kwargs["suffix"],
                suffix_id=kwargs["suffix_id"],
                storage_id=kwargs["storage_id"],
            )
        }
        drives = [
            {
                "@odata.id": "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Drives/{linkDrives}".format(
                    rb=kwargs["rb"],
                    suffix=kwargs["suffix"],
                    suffix_id=kwargs["suffix_id"],
                    storage_id=kwargs["storage_id"],
                    linkDrives=x,
                )
            }
            for x in kwargs["driList"]
        ]
        volumes = {
            "@odata.id": "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Volumes".format(
                rb=kwargs["rb"],
                suffix=kwargs["suffix"],
                suffix_id=kwargs["suffix_id"],
                storage_id=kwargs["storage_id"],
            )
        }
    else:
        controllers = {
            "@odata.id": "{rb}Storage/{storage_id}/Controllers".format(
                rb=kwargs["rb"], storage_id=kwargs["storage_id"]
            )
        }
        drives = [
            {
                "@odata.id": "{rb}Chassis/{chassis_id}/Drives/{linkDrives}".format(
                    rb=kwargs["rb"], chassis_id=kwargs["chassis_id"], linkDrives=x
                )
            }
            for x in kwargs["driList"]
        ]
        volumes = {
            "@odata.id": "{rb}Storage/{storage_id}/Volumes".format(
                rb=kwargs["rb"], storage_id=kwargs["storage_id"]
            )
        }

    c["Controllers"] = controllers
    c["Drives"] = drives
    c["Volumes"] = volumes

    return c


def get_Storage_instance(wildcards):
    c = deepcopy(_TEMPLATE)
    c["Id"] = c["Id"].format(storage_id=wildcards["id"])
    c["@odata.id"] = wildcards["url"]
    controllers = {
        "@odata.id": "{rb}Storage/{storage_id}/Controllers".format(
            rb=wildcards["rb"], storage_id=wildcards["id"]
        )
    }
    volumes = {
        "@odata.id": "{rb}Storage/{storage_id}/Volumes".format(
            rb=wildcards["rb"], storage_id=wildcards["id"]
        )
    }
    drives = [
        {
            "@odata.id": "{rb}Chassis/{chassis_id}/Drives/{linkDrives}".format(
                rb=wildcards["rb"], chassis_id=wildcards["chassis_id"], linkDrives=x
            )
        }
        for x in wildcards["driList"]
    ]

    c["Controllers"] = controllers
    c["Drives"] = drives
    c["Volumes"] = volumes
    return c
