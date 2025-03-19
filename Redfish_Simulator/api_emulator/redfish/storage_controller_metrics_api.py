# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""StorageControllerMetrics

    StorageControllerMetrics processing
"""


import logging
from flask_restful import Resource

from .templates.StorageControllerMetrics import format_StorageControllerMetrics_template

members = {}

INTERNAL_ERROR = 500

config = {}


class StorageControllerMetricsChassisAPI(Resource):
    """StorageControllerMetrics Acquisition and Operation API
    Class to acquisition and operation StorageControllerMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET StorageControllerMetrics"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class StorageControllerMetricsSystemsAPI(Resource):
    """StorageControllerMetrics Acquisition and Operation API
    Class to acquisition and operation StorageControllerMetrics
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET StorageControllerMetrics"""
        if ident2 not in members:
            return "not found", 404
        if ident3 not in members[ident2]:
            return "not found", 404
        return members[ident2][ident3], 200


def create_storage_controller_metrics(**kwargs):
    """Create StorageControllerMetrics"""
    logging.info("CreateStorageControllerMetrics")
    sctr_id = kwargs["sctr_id"]
    storage_id = kwargs["storage_id"]
    if storage_id not in members:
        members[storage_id] = {}
    members[storage_id][sctr_id] = format_StorageControllerMetrics_template(**kwargs)
