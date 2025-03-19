# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#StorageController.v1_9_0.StorageController",
    "Id": "1",
    "Name": "NVMe IO Controller",
    "Status": {"State": "Enabled", "Health": "OK"},
    "Identifiers": [{"DurableNameFormat": "NAA", "DurableName": "32ADF365C6C1B7BD"}],
    "Manufacturer": "Storage Controller Manufacturer",
    "Model": "Storage Controller Model ",
    "SupportedControllerProtocols": ["NVMeOverFabrics"],
    "NVMeControllerProperties": {
        "NVMeVersion": "1.4",
        "ControllerType": "IO",
        "NVMeControllerAttributes": {
            "ReportsUUIDList": False,
            "SupportsSQAssociations": False,
            "ReportsNamespaceGranularity": False,
            "SupportsTrafficBasedKeepAlive": False,
            "SupportsPredictableLatencyMode": False,
            "SupportsEnduranceGroups": False,
            "SupportsReadRecoveryLevels": False,
            "SupportsNVMSets": False,
            "SupportsExceedingPowerOfNonOperationalState": False,
            "Supports128BitHostId": False,
        },
        "NVMeSMARTCriticalWarnings": {
            "PMRUnreliable": False,
            "PowerBackupFailed": False,
            "MediaInReadOnly": False,
            "OverallSubsystemDegraded": False,
            "SpareCapacityWornOut": False,
        },
    },
    "SpeedGbps": 12,
    "Metrics": {
        "@odata.id": "/redfish/v1/Storage/{storage_id}/Controllers/{strCtr_id}/Metrics"
    },
    "Ports": {},
    "@odata.id": "/redfish/v1/Storage/{storage_id}/Controllers/{strCtr_id}",
}


def format_StorageController_template(**kwargs):
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
        c["Ports"]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Controllers/{strCtr_id}/Ports".format(
                **defaults
            )
        )
        c["Metrics"]["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Controllers/{strCtr_id}/Metrics".format(
                **defaults
            )
        )
        c["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Controllers/{strCtr_id}".format(
                **defaults
            )
        )
    else:
        c["Ports"]["@odata.id"] = (
            "{rb}Storage/{storage_id}/Controllers/{strCtr_id}/Ports".format(**defaults)
        )
        c["Metrics"]["@odata.id"] = (
            "{rb}Storage/{storage_id}/Controllers/{strCtr_id}/Metrics".format(
                **defaults
            )
        )
        c["@odata.id"] = "{rb}Storage/{storage_id}/Controllers/{strCtr_id}".format(
            **defaults
        )

    return c
