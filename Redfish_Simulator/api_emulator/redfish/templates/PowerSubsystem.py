# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
from api_emulator.utils import replace_recurse

_TEMPLATE = {
    "@odata.type": "#PowerSubsystem.v1_1_3.PowerSubsystem",
    "Id": "PowerSubsystem",
    "Name": "Power Subsystem for Chassis",
    "CapacityWatts": 2000,
    "Allocation": {"RequestedWatts": 1500, "AllocatedWatts": 1200},
    "PowerSupplyRedundancy": [
        {
            "RedundancyType": "Failover",
            "MaxSupportedInGroup": 2,
            "MinNeededInGroup": 1,
            "RedundancyGroup": [
                {
                    "@odata.id": "/redfish/v1/Chassis/1U/PowerSubsystem/PowerSupplies/Bay1"
                },
                {
                    "@odata.id": "/redfish/v1/Chassis/1U/PowerSubsystem/PowerSupplies/Bay2"
                },
            ],
            "Status": {"State": "UnavailableOffline", "Health": "OK"},
        }
    ],
    "PowerSupplies": {
        "@odata.id": "/redfish/v1/Chassis/1U/PowerSubsystem/PowerSupplies"
    },
    "Status": {"State": "Enabled", "Health": "OK"},
    "Oem": {},
    "@odata.id": "/redfish/v1/Chassis/1U/PowerSubsystem",
}


def get_PowerSubsystem_instance(wildcards):
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    return c
