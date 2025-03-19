# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#PowerSupply.v1_6_0.PowerSupply",
    "Id": "{ps_id}",
    "Name": "Power Supply Bay 1",
    "Status": {"State": "Enabled", "Health": "Warning"},
    "LineInputStatus": "Normal",
    "Model": "RKS-440DC",
    "Manufacturer": "Contoso Power",
    "FirmwareVersion": "1.00",
    "SerialNumber": "3488247",
    "PartNumber": "23456-133",
    "SparePartNumber": "93284-133",
    "LocationIndicatorActive": False,
    "HotPluggable": False,
    "PowerCapacityWatts": 400,
    "PhaseWiringType": "OnePhase3Wire",
    "PlugType": "IEC_60320_C14",
    "InputRanges": [
        {"NominalVoltageType": "AC200To240V", "CapacityWatts": 400},
        {"NominalVoltageType": "AC120V", "CapacityWatts": 350},
        {"NominalVoltageType": "DC380V", "CapacityWatts": 400},
    ],
    "EfficiencyRatings": [
        {"LoadPercent": 25, "EfficiencyPercent": 75},
        {"LoadPercent": 50, "EfficiencyPercent": 85},
        {"LoadPercent": 90, "EfficiencyPercent": 80},
    ],
    "OutputRails": [
        {"NominalVoltage": 3.3, "PhysicalContext": "SystemBoard"},
        {"NominalVoltage": 5, "PhysicalContext": "SystemBoard"},
        {"NominalVoltage": 12, "PhysicalContext": "StorageDevice"},
    ],
    "Location": {
        "PartLocation": {
            "ServiceLabel": "PSU 1",
            "LocationType": "Bay",
            "LocationOrdinalValue": 0,
        }
    },
    "Links": {"PoweringChassis": {"@odata.id": "/redfish/v1/Chassis/{ch_id}"}},
    "@odata.id": "/redfish/v1/Chassis/{ch_id}/PowerSubsystem/PowerSupplies/{ps_id}",
}


def format_PowerSupply_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    c["Id"] = c["Id"].format(**kwargs)
    c["Links"]["PoweringChassis"]["@odata.id"] = c["Links"]["PoweringChassis"][
        "@odata.id"
    ].format(**kwargs)
    return c
