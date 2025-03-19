# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#NetworkAdapter.v1_11_0.NetworkAdapter",
    "Id": "{na_id}",
    "Name": "Network Adapter View",
    "Manufacturer": "Contoso",
    "Model": "599TPS-T",
    "SKU": "Contoso TPS-Net 2-Port Base-T",
    "SerialNumber": "{neta_sereal}",
    "PartNumber": "975421-B20",
    "Ports": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/Ports"
    },
    "Metrics": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/Metrics"
    },
    "NetworkDeviceFunctions": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions"
    },
    "EnvironmentMetrics": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/EnvironmentMetrics"
    },
    "PowerState": "On",
    "Status": {"State": "Enabled", "Health": "OK"},
    "PowerCapability": True,
    "Controllers": [
        {
            "FirmwarePackageVersion": "7.4.10",
            "ControllerCapabilities": {
                "NetworkPortCount": 2,
                "NetworkDeviceFunctionCount": 8,
                "DataCenterBridging": {"Capable": True},
                "VirtualizationOffload": {
                    "VirtualFunction": {
                        "DeviceMaxCount": 256,
                        "NetworkPortMaxCount": 128,
                        "MinAssignmentGroupSize": 4,
                    },
                    "SRIOV": {"SRIOVVEPACapable": True},
                },
                "NPIV": {"MaxDeviceLogins": 4, "MaxPortLogins": 2},
                "NPAR": {"NparCapable": True, "NparEnabled": False},
            },
            "PCIeInterface": {
                "PCIeType": "Gen2",
                "MaxPCIeType": "Gen3",
                "LanesInUse": 1,
                "MaxLanes": 4,
            },
            "Location": {
                "PartLocation": {
                    "ServiceLabel": "Slot 1",
                    "LocationType": "Slot",
                    "LocationOrdinalValue": 0,
                    "Reference": "Rear",
                    "Orientation": "LeftToRight",
                }
            },
            "Identifiers": [
                {"DurableNameFormat": "NAA", "DurableName": "32ADF365C6C1B7BD"}
            ],
            "Links": {
                "PCIeDevices": [{"@odata.id": "/redfish/v1/Systems/1/PCIeDevices/NIC"}],
                "Ports": [
                    {
                        "@odata.id": "/redfish/v1/Chassis/1/NetworkAdapters/9fd725a1/Ports/1"
                    }
                ],
                "NetworkDeviceFunctions": [
                    {
                        "@odata.id": "/redfish/v1/Chassis/1/NetworkAdapters/1/NetworkDeviceFunctions/1"
                    }
                ],
            },
        }
    ],
    "Location": {
        "PartLocation": {
            "LocationOrdinalValue": 1,
            "LocationType": "Slot",
        },
        "PartLocationContext": "",
    },
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}",
    "Actions": {
        "#NetworkAdapter.Reset": {
            "target": "{rb}{suffix}/{chassis_id}/NetworkAdapters/{na_id}/Actions/NetworkAdapter.Reset",
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
            "#NetworkAdapter.MetricState": {
                "target": "{rb}{suffix}/{chassis_id}/NetworkAdapters/{na_id}/Actions/NetworkAdapter.MetricState",
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


def format_NetworkAdapter_template(**kwargs):
    """
    Format the processor template -- returns the template
    """
    # params:
    defaults = {
        "rb": "/redfish/v1/",
        "suffix": "Systems",
        "speedmbps": 10000,
        "vlanid": 0,
    }

    defaults.update(kwargs)

    c = copy.deepcopy(_TEMPLATE)
    c["@odata.id"] = c["@odata.id"].format(**defaults)
    c["Id"] = c["Id"].format(**defaults)

    if "pcie_id" in defaults:
        pcie_device = [
            {
                "@odata.id": "{rb}Chassis/{chassis_id}/PCIeDevices/{pcie_id}".format(
                    rb=kwargs["rb"],
                    chassis_id=kwargs["chassis_id"],
                    pcie_id=kwargs["pcie_id"],
                )
            }
        ]
        c["Controllers"][0]["Links"]["PCIeDevices"] = pcie_device

    if "portNAList" in defaults:
        port = [
            {
                "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}/Ports/{linkPort}".format(
                    rb=kwargs["rb"],
                    chassis_id=kwargs["chassis_id"],
                    na_id=kwargs["na_id"],
                    linkPort=x,
                )
            }
            for x in kwargs["portNAList"]
        ]
        c["Controllers"][0]["Links"]["Ports"] = port

    if "ndfList" in defaults:
        ndf = [
            {
                "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{linkNdf}".format(
                    rb=kwargs["rb"],
                    chassis_id=kwargs["chassis_id"],
                    na_id=kwargs["na_id"],
                    linkNdf=x,
                )
            }
            for x in kwargs["ndfList"]
        ]
        c["Controllers"][0]["Links"]["NetworkDeviceFunctions"] = ndf

    c["Metrics"]["@odata.id"] = c["Metrics"]["@odata.id"].format(**defaults)
    c["EnvironmentMetrics"]["@odata.id"] = c["EnvironmentMetrics"]["@odata.id"].format(
        **defaults
    )
    c["NetworkDeviceFunctions"]["@odata.id"] = c["NetworkDeviceFunctions"][
        "@odata.id"
    ].format(**defaults)
    c["Ports"]["@odata.id"] = c["Ports"]["@odata.id"].format(**defaults)

    c["Model"] = defaults["model"]
    if kwargs.get("neta_sereal") is not None:
        c["SerialNumber"] = c["SerialNumber"].format(**defaults)
    if "state" in defaults["dev_param"]:
        c["Status"]["State"] = defaults["dev_param"]["state"]
    if "health" in defaults["dev_param"]:
        c["Status"]["Health"] = defaults["dev_param"]["health"]

    if "Actions" in c:
        c["Actions"]["#NetworkAdapter.Reset"]["target"] = c["Actions"][
            "#NetworkAdapter.Reset"
        ]["target"].format(**defaults)
        c["Actions"]["Oem"]["#NetworkAdapter.MetricState"]["target"] = c["Actions"][
            "Oem"
        ]["#NetworkAdapter.MetricState"]["target"].format(**defaults)
    if "reset_action" in defaults:
        if defaults["reset_action"] == "invalid":
            del c["Actions"]["#NetworkAdapter.Reset"]

    c["Controllers"][0]["Identifiers"][0]["DurableName"] = (
        "32ADF365CNIC{neta_sereal}".format(**defaults)
    )

    return c
