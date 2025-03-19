# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.id": "{rb}AccountService/Roles/{role_id}",
    "@odata.type": "#Role.v1_3_3.Role",
    "Id": "{role_id}",
    "Name": "Role {role_id}",
    "Description": "User Account",
    "RoleId": "{role_id}",
}


def get_Role_instance(**kwargs):
    """
    Instantiate and format the template

    Arguments:
        wildcard - A dictionary of wildckwargsards strings and their replacement values

    """
    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    c["Id"] = c["Id"].format(**kwargs)
    c["RoleId"] = c["Id"].format(**kwargs)
    c["Name"] = c["Name"].format(**kwargs)

    return c
