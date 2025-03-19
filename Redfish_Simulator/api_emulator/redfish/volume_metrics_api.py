# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""VolumeMetrics

    VolumeMetrics processing
"""

import logging
from flask_restful import Resource

from .templates.VolumeMetrics import format_VolumeMetrics_template

members = {}

INTERNAL_ERROR = 500

config = {}


class VolumeMetricsChassisAPI(Resource):
    """VolumeMetrics Acquisition and Operation API
    Class to acquisition and operation VolumeMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET VolumeMetrics"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class VolumeMetricsSystemsAPI(Resource):
    """VolumeMetrics Collection Acquisition and Operation API
    Class to acquisition and operation VolumeMetrics Collection
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET VolumeMetrics"""
        if ident2 not in members:
            return "not found", 404
        if ident3 not in members[ident2]:
            return "not found", 404
        return members[ident2][ident3], 200


def create_volume_metrics(**kwargs):
    """Create VolumeMetrics"""
    logging.info("CreateVolumeMetrics")
    volume_id = kwargs["volume_id"]
    storage_id = kwargs["storage_id"]
    if storage_id not in members:
        members[storage_id] = {}
    members[storage_id][volume_id] = format_VolumeMetrics_template(**kwargs)
