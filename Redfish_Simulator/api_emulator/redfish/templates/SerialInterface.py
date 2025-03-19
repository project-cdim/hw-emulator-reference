# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#SerialInterface.v1_2_1.SerialInterface",
    "Id": "{si_id}",
    "Name": "Manager Serial Interface 1",
    "Description": "Management for Serial Interface",
    "InterfaceEnabled": True,
    "SignalType": "Rs232",
    "BitRate": "9600",
    "Parity": "None",
    "DataBits": "8",
    "StopBits": "1",
    "FlowControl": "None",
    "ConnectorType": "RJ45",
    "PinOut": "Cyclades",
    "@odata.id": "/redfish/v1/Managers/{manager_id}/SerialInterfaces/{si_id}",
}


def format_SerialInterfaces_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    c["Id"] = c["Id"].format(**kwargs)

    return c
