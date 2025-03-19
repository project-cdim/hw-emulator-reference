# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#VolumeMetrics.v1_0_3.VolumeMetrics",
    "Id": "Metrics",
    "Name": "Volume Metrics for NVMe IO Controller",
    "CorrectableIOReadErrorCount": 184,
    "UncorrectableIOReadErrorCount": 0,
    "CorrectableIOWriteErrorCount": 18,
    "UncorrectableIOWriteErrorCount": 0,
    "@odata.id": "/redfish/v1/Systems/Sys-1/Storage/SimplestNVMeSSD/Volume/Volume-1/Metrics",
}


def format_VolumeMetrics_template(**kwargs):

    c = copy.deepcopy(_TEMPLATE)

    if kwargs["suffix"] == "Systems":
        c["@odata.id"] = (
            "{rb}{suffix}/{suffix_id}/Storage/{storage_id}/Volumes/{volume_id}/Metrics".format(
                **kwargs
            )
        )
    else:
        c["@odata.id"] = "{rb}{suffix}/{suffix_id}/Volumes/{volume_id}/Metrics".format(
            **kwargs
        )
    return c
