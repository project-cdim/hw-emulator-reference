# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""StorageController

    StorageController processing
"""

import logging
from flask_restful import Resource

from .templates.StorageController import format_StorageController_template
from .storage_controller_metrics_api import create_storage_controller_metrics

members = {}

INTERNAL_ERROR = 500

config = {}


class StorageControllerChassisAPI(Resource):
    """StorageController Acquisition and Operation API
    Class to acquisition and operation StorageController
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET StorageController"""
        if ident1 not in members:
            return "not found", 404
        if ident2 not in members[ident1]:
            return "not found", 404
        return members[ident1][ident2], 200


class StorageControllerSystemsAPI(Resource):
    """StorageController Acquisition and Operation API
    Class to acquisition and operation StorageController
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2, ident3):  # pylint: disable=W0613
        """GET StorageController"""
        if ident2 not in members:
            return "not found", 404
        if ident3 not in members[ident2]:
            return "not found", 404
        return members[ident2][ident3], 200


class StorageControllerChassisCollectionAPI(Resource):
    """StorageController Collection Acquisition and Operation API
    Class to acquisition and operation StorageController Collection
    """

    def __init__(self, rb):
        self.config = {
            "@odata.context": f"{rb}$metadata#StorageControllerCollection.StorageControllerCollection",
            "@odata.id": f"{rb}Storage",
            "@odata.type": "#StorageControllerCollection.StorageControllerCollection",
            "Name": "StorageController Collection",
        }

    def get(self, ident):
        """GET StorageController Collection"""
        try:
            if ident not in members:
                return 404
            procs = []
            for p in members.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Controllers"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class StorageControllerSystemsCollectionAPI(Resource):
    """StorageController Collection Acquisition and Operation API
    Class to acquisition and operation StorageController Collection
    """

    def __init__(self, rb, suffix):
        self.config = {
            "@odata.context": f"{rb}$metadata#StorageControllerCollection.StorageControllerCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#StorageControllerCollection.StorageControllerCollection",
            "Name": "StorageController Collection",
        }

    def get(self, ident1, ident2):
        """GET StorageController Collection"""
        try:
            if ident2 not in members:
                return 404
            procs = []
            for p in members.get(ident2, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident1}/Storage/{ident2}/Controllers"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


def create_storage_controller(**kwargs):
    """Create StorageController"""
    logging.info("CreateStorageController")
    sctr_id = kwargs["strCtr_id"]
    storage_id = kwargs["storage_id"]
    suffix_id = kwargs["suffix_id"]

    if storage_id not in members:
        members[storage_id] = {}
    members[storage_id][sctr_id] = format_StorageController_template(**kwargs)
    create_storage_controller_metrics(
        rb=kwargs["rb"],
        suffix=kwargs["suffix"],
        suffix_id=suffix_id,
        storage_id=storage_id,
        sctr_id=sctr_id,
    )
