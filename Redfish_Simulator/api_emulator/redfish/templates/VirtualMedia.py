# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#VirtualMedia.v1_6_4.VirtualMedia",
    "Id": "CD1",
    "Name": "Virtual CD",
    "MediaTypes": ["CD", "DVD"],
    "Image": "redfish.dmtf.org/freeImages/freeOS.1.1.iso",
    "ImageName": "mymedia-read-only",
    "ConnectedVia": "Applet",
    "Inserted": True,
    "WriteProtected": False,
    "TransferMethod": "Stream",
    "TransferProtocolType": "OEM",
    "Status": {"State": "Enabled", "Health": "OK"},
    "@odata.id": "/redfish/v1/Systems/{suffix_id}/VirtualMedia/{vm_id}",
}


def format_VirtualMedia_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Id"] = "{vm_id}".format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)
    return c
