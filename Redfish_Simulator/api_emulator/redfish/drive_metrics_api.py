# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""DriveMetrics

    DriveMetrics processing
"""

import logging
from flask_restful import Resource

from .templates.DriveMetrics import format_DriveMetrics_template

members = {}

INTERNAL_ERROR = 500

config = {}


class DriveMetricsChassisAPI(Resource):
    """Chassis DriveMetrics Acquisition and Operation API
    Class to acquisition and operation Chassis DriveMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET Chassis DriveMetrics"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class DriveMetricsSystemsAPI(Resource):
    """Systems DriveMetrics Acquisition and Operation API
    Class to acquisition and operation Systems DriveMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET Systems DriveMetrics"""
        if ident1 not in members:
            return "not found", 404
        if ident3 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident3], 200


def create_drive_metrics(**kwargs):
    """Create DriveMetrics"""
    logging.info("CreateDriveMetrics")
    drive_id = kwargs["drive_id"]
    suffix_id = kwargs["suffix_id"]
    if suffix_id not in members:
        members[suffix_id] = {}
    members[suffix_id][drive_id] = format_DriveMetrics_template(**kwargs)
