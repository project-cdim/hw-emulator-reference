# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#Drive.v1_21_0.Drive",
    "Id": "{drive_id}",
    "Name": "Drive Sample",
    "LocationIndicatorActive": True,
    "Model": "C123",
    "Revision": "100A",
    "Status": {"State": "Enabled", "Health": "OK"},
    "CapacityBytes": 899527000000,
    "FailurePredicted": False,
    "Protocol": "SAS",
    "MediaType": "HDD",
    "Manufacturer": "Contoso",
    "SerialNumber": "{dri_sereal}",
    "PartNumber": "C123-1111",
    "Identifiers": [{"DurableNameFormat": "NAA", "DurableName": "32ADF365C6C1B7BD"}],
    "PowerState": "On",
    "PowerCapability": True,
    "HotspareType": "None",
    "EncryptionAbility": "SelfEncryptingDrive",
    "EncryptionStatus": "Unlocked",
    "RotationSpeedRPM": 15000,
    "BlockSizeBytes": 512,
    "CapableSpeedGbs": 12,
    "NegotiatedSpeedGbs": 12,
    "PredictedMediaLifeLeftPercent": 50,
    "EnvironmentMetrics": {
        "@odata.id": "{rb}{suffix}/{chassis_id}/Drives/{drive_id}/EnvironmentMetrics"
    },
    "Metrics": {"@odata.id": "{rb}{suffix}/{chassis_id}/Drives/{drive_id}/Metrics"},
    "Links": {
        "Chassis": {"@odata.id": "/redfish/v1/Chassis/{chassis_id}"},
        "NetworkDeviceFunctions": [],
        "StoragePools": [],
        "Volumes": [
            {
                "@odata.id": "/redfish/v1/{suffix}/{suffix_id}/Storage/{storage_id}/Volumes/{volume_id}"
            }
        ],
        "Storage": {"@odata.id": "/redfish/v1/Storage/{storage_id}"},
    },
    "PhysicalLocation": {},
    "@odata.id": "/redfish/v1/{suffix}/{chassis_id}/Drives/{drive_id}",
    "Actions": {
        "#Drive.Reset": {
            "target": "{rb}{suffix}/{chassis_id}/Drives/{drive_id}/Actions/Drive.Reset",
            "ResetType@Redfish.AllowableValues": [
                "On",
                "ForceOff",
                "GracefulShutdown",
                "GracefulRestart",
                "ForceRestart",
                "ForceOn",
            ],
        },
        "Oem": {
            "#Drive.MetricState": {
                "target": "{rb}Chassis/{chassis_id}/Drives/{drive_id}/Actions/Drive.MetricState",
                "StateType@Redfish.AllowableValues": [
                    "off",
                    "steady",
                    "low",
                    "high",
                    "action",
                ],
            }
        },
    },
}


def format_Drive_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    defaults = {
        "rb": "/redfish/v1/",
        "suffix": "Chassis",
        "capacitymb": 16384,
        "devicetype": "DDR4",
        "type": "DRAM",
        "operatingmodes": ["Volatile"],
    }

    defaults.update(kwargs)

    if kwargs["suffix"] == "Systems":
        c["Links"]["Volumes"][0]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Volumes/{volume_id}".format(
                **defaults
            )
        )
        c["Links"]["Storage"]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}".format(**defaults)
        )
        c["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Drives/{drive_id}".format(
                **defaults
            )
        )
        c["EnvironmentMetrics"]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Drives/{drive_id}/EnvironmentMetrics".format(
                **defaults
            )
        )
        c["Metrics"]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Drives/{drive_id}/Metrics".format(
                **defaults
            )
        )
    else:
        c["Links"]["Volumes"][0]["@odata.id"] = (
            "{rb}Storage/{storage_id}/Volumes/{volume_id}".format(**defaults)
        )
        c["Links"]["Storage"]["@odata.id"] = "{rb}Storage/{storage_id}".format(
            **defaults
        )
        c["@odata.id"] = "{rb}{suffix}/{suffix_id}/Drives/{drive_id}".format(**defaults)
        c["EnvironmentMetrics"]["@odata.id"] = (
            "{rb}{suffix}/{chassis_id}/Drives/{drive_id}/EnvironmentMetrics".format(
                **defaults
            )
        )
        c["Metrics"]["@odata.id"] = (
            "{rb}{suffix}/{chassis_id}/Drives/{drive_id}/Metrics".format(**defaults)
        )
        if "Actions" in c:
            c["Actions"]["#Drive.Reset"]["target"] = c["Actions"]["#Drive.Reset"][
                "target"
            ].format(**defaults)
            c["Actions"]["Oem"]["#Drive.MetricState"]["target"] = c["Actions"]["Oem"][
                "#Drive.MetricState"
            ]["target"].format(**defaults)

    if "pcie_f_id" in defaults and "pcie_id" in defaults:
        c["Links"]["PCIeFunctions"] = []
        func = "{rb}Chassis/{chassis_id}/PCIeDevices/{pcie_id}/PCIeFunctions/{pcie_f_id}".format(
            **defaults
        )
        c["Links"]["PCIeFunctions"].append({"@odata.id": func})

    c["Links"]["Chassis"]["@odata.id"] = c["Links"]["Chassis"]["@odata.id"].format(
        **defaults
    )
    c["Id"] = c["Id"].format(**defaults)
    if kwargs.get("dri_sereal") is not None:
        c["SerialNumber"] = c["SerialNumber"].format(**defaults)

    if "reset_action" in defaults:
        if defaults["reset_action"] == "invalid":
            del c["Actions"]["#Drive.Reset"]

    c["Model"] = defaults["model"]

    if "state" in defaults["dev_param"]:
        c["Status"]["State"] = defaults["dev_param"]["state"]
    if "health" in defaults["dev_param"]:
        c["Status"]["Health"] = defaults["dev_param"]["health"]
    if "driveCapableSpeedGbs" in defaults["dev_param"]:
        c["CapableSpeedGbs"] = defaults["dev_param"]["driveCapableSpeedGbs"]
    if "driveCapacityBytes" in defaults["dev_param"]:
        c["CapacityBytes"] = defaults["dev_param"]["driveCapacityBytes"] * 1048576

    c["Identifiers"][0]["DurableName"] = "32ADF365CDRI{dri_sereal}".format(**defaults)

    return c
