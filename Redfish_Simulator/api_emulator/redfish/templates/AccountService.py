# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy
from api_emulator.utils import replace_recurse

_TEMPLATE = {
    "@odata.id": "/redfish/v1/AccountService",
    "@odata.type": "#AccountService.v1_17_0.AccountService",
    "@odata.context": "/redfish/v1/$metadata#AccountService.AccountService",
    "Id": "AccountService",
    "Name": "Account Service",
    "Description": "Local Manager Account Service",
    "Status": {"State": "Enabled", "Health": "OK"},
    "ServiceEnabled": True,
    "Accounts": {"@odata.id": "/redfish/v1/AccountService/Accounts"},
    "Roles": {"@odata.id": "/redfish/v1/AccountService/Roles"},
}


def get_AccountService_instance(wildcards):
    c = copy.deepcopy(_TEMPLATE)
    replace_recurse(c, wildcards)
    return c
