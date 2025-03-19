# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""
Fabric Template File

"""

import copy
from api_emulator.utils import replace_recurse

_TEMPLATE = \
{
    "@odata.id": "{rb}Fabrics/{FabricId}",
    "@odata.type": "#Fabric.v1_3_2.Fabric",
    "Id": "{FabricId}",
    "Name": "Fabric",
    "FabricType": "CXL",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "Switches": {
        "@odata.id": "{rb}Fabrics/{FabricId}/Switches"
    },
    "Zones": {
        "@odata.id": "{rb}CompositionService/ResourceZones"
    }
}

def get_fabric_instance(wildcards):
    """Return Fabric data"""
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    return c
