# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#DriveMetrics.v1_2_1.DriveMetrics",
    "Name": "Drive Metrics",
    "Id": "Metrics",
    "BadBlockCount": 123098,
    "CorrectableIOReadErrorCount": 184,
    "UncorrectableIOReadErrorCount": 0,
    "CorrectableIOWriteErrorCount": 18,
    "UncorrectableIOWriteErrorCount": 0,
    "PowerOnHours": 3,
    "NVMeSMART": {
        "CriticalWarnings": {
            "PMRUnreliable": False,
            "PowerBackupFailed": False,
            "MediaInReadOnly": False,
            "OverallSubsystemDegraded": False,
            "SpareCapacityWornOut": False,
        },
        "CompositeTemperatureCelsius": 34,
        "AvailableSparePercent": 50,
        "AvailableSpareThresholdPercent": 30,
        "PercentageUsed": 50,
        "EGCriticalWarningSummary": {
            "NamespacesInReadOnlyMode": False,
            "ReliabilityDegraded": False,
            "SpareCapacityUnderThreshold": False,
        },
        "DataUnitsRead": 0,
        "DataUnitsWritten": 0,
        "HostReadCommands": 0,
        "HostWriteCommands": 0,
        "ControllerBusyTimeMinutes": 20,
        "PowerCycles": 49,
        "PowerOnHours": 3,
        "UnsafeShutdowns": 4,
        "MediaAndDataIntegrityErrors": 0,
        "NumberOfErrorInformationLogEntries": 100,
        "WarningCompositeTempTimeMinutes": 0,
        "CriticalCompositeTempTimeMinutes": 0,
        "TemperatureSensorsCelsius": [34, 34, 34, 34, 34, 35, 33, 32],
        "ThermalMgmtTemp1TransitionCount": 10,
        "ThermalMgmtTemp2TransitionCount": 2,
        "ThermalMgmtTemp1TotalTimeSeconds": 20,
        "ThermalMgmtTemp2TotalTimeSeconds": 42,
    },
    "@odata.id": "/redfish/v1/{suffix}/{suffix_id}/Drives/{drive_id}/Metrics",
}


def format_DriveMetrics_template(**kwargs):

    c = copy.deepcopy(_TEMPLATE)

    if kwargs["suffix"] == "Systems":
        c["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Drives/{drive_id}/Metrics".format(
                **kwargs
            )
        )
    else:
        c["@odata.id"] = "{rb}{suffix}/{suffix_id}/Drives/{drive_id}/Metrics".format(
            **kwargs
        )
    return c
