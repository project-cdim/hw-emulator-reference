# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""
Switch Template File

"""

import copy
from api_emulator.utils import replace_recurse

_TEMPLATE = \
{
    "@odata.id": "{rb}Fabrics/{FabricId}/Switches/{SwitchId}",
    "@odata.type": "#Switch.v1_9_3.Switch",
    "Id": "{SwitchId}",
    "Name": "Switch",
    "SwitchType": "CXL",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK"
    },
    "CXL": {
        "MaxVCSsSupported": 0,
        "TotalNumbervPPBs": 0,
        "VCS": {
            "HDMDecoders": 0
        }
    },
    "Links": {
        "Chassis": {
            "@odata.id": "{rb}Chassis/{ChassisId}"
        }
    },
    "Manufacturer": "{Manufacturer}",
    "Model": "{Model}",
    "SerialNumber": "{SerialNumber}",
}

def get_switch_instance(wildcards):
    """Return Switch data"""
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    c["CXL"]["TotalNumbervPPBs"] = wildcards["VCSCount"] * wildcards["MAXPortCount"]
    c["CXL"]["MaxVCSsSupported"] = wildcards["VCSCount"]
    c["CXL"]["VCS"]["HDMDecoders"] = wildcards["VCSCount"]
    return c
