# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.id": "{rb}AccountService/Accounts/{account_id}",
    "@odata.type": "#ManagerAccount.v1_13_0.ManagerAccount",
    "Id": "{account_id}",
    "Name": "ManagerAccount {account_id}",
    "Description": "User Account",
    "UserName": "{user_name}",
    "AccountTypes": ["Redfish"],
}


def get_ManagerAccount_instance(**kwargs):
    """
    Instantiate and format the template

    Arguments:
        wildcard - A dictionary of wildckwargsards strings and their replacement values

    """
    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    c["Id"] = c["Id"].format(**kwargs)
    c["Name"] = c["Name"].format(**kwargs)
    c["UserName"] = c["UserName"].format(**kwargs)

    return c
