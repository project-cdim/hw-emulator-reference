# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""Storage

    Storage processing
"""

import traceback
import logging
import copy
from flask_restful import Resource
import g

from .templates.Storage import format_storage_template, get_Storage_instance

members = {}
systemMembers = {}
INTERNAL_ERROR = 500


class StorageSystemAPI(Resource):
    """
    SimpleStorage.v1_2_0.SimpleStorage
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident1, ident2):
        """GET SystemStorage"""
        if ident1 not in systemMembers:
            return "not found", 404
        if ident2 not in systemMembers[ident1]:
            return "not found", 404
        return systemMembers[ident1][ident2], 200


class StorageAPI(Resource):
    """
    SimpleStorage.v1_2_0.SimpleStorage
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident):
        """GET SimpleStorage"""
        logging.info("StorageAPI get called")
        if ident not in members:
            return "not found", 404
        return members[ident], 200


class StorageSystemCollectionAPI(Resource):
    """
    SimpleStorage.v1_2_0.SimpleStorageCollection
    """

    def __init__(self, rb, suffix):
        """
        StorageCollection Constructor
        """
        self.config = {
            "@odata.context": f"{rb}$metadata#StorageCollection.StorageCollection",
            "@odata.id": f"{rb}{suffix}",
            "@odata.type": "#StorageCollection.StorageCollection",
            "Name": "Storages Collection",
        }

    def get(self, ident):
        """GET SimpleStorage collection"""
        try:
            if ident not in systemMembers:
                return 404
            procs = []
            for p in systemMembers.get(ident, {}).values():
                procs.append({"@odata.id": p["@odata.id"]})
            prefix = self.config["@odata.id"]
            self.config["@odata.id"] = f"{prefix}/{ident}/Storage"
            self.config["Members"] = procs
            self.config["Members@odata.count"] = len(procs)
            resp = self.config, 200
        except Exception as e:  # pylint: disable=W0718
            logging.error(e)
            resp = "internal error", INTERNAL_ERROR
        return resp


class StorageCollectionAPI(Resource):
    """
    Storage.v1_2_0.StorageCollection
    """

    def __init__(self):
        self.rb = g.rest_base

        logging.info(members)

        self.config = {
            "@odata.type": "#StorageCollectionAPI.StorageCollectionAPI",
            "Name": "StorageCollectionAPI",
            "Members@odata.count": {},
            "Members": {},
        }
        self.config["Members@odata.count"] = len(members)
        self.config["Members"] = [
            {"@odata.id": x["@odata.id"]} for x in list(members.values())
        ]

    def get(self):
        """GET Storage collection"""
        try:
            resp = self.config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp


class CreateStorage(Resource):
    """
    Create Storage Class
    """

    def __init__(self, **kwargs):
        logging.info("CreateStorage init called")
        if "resource_class_kwargs" in kwargs:
            global wildcards
            wildcards = copy.deepcopy(kwargs["resource_class_kwargs"])

    # Create instance
    def put(self, ident):
        """PUT Storage"""
        logging.info("CreateStorage put called")
        try:
            global config
            wildcards["id"] = ident
            config = get_Storage_instance(wildcards)
            members[ident] = config
            logging.info(ident)
            resp = config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        logging.info("CreateStorage init exit")
        return resp


def create_system_storage(**kwargs):
    """Create Storage"""
    logging.info("CreateSystemStorage init called")
    suffix_id = kwargs["suffix_id"]
    storage_id = kwargs["storage_id"]
    chassis_id = kwargs["chassis_id"]
    if suffix_id not in systemMembers:
        systemMembers[suffix_id] = {}

    kwargs["url"] = "{rb}{suffix}/{suffix_id}/Storage/{storage_id}".format(**kwargs)
    systemMembers[suffix_id][storage_id] = format_storage_template(**kwargs)

    rb = kwargs["rb"]
    sctr_list = kwargs["sctrList"]
    vol_list = kwargs["volList"]
    dri_list = kwargs["driList"]
    url = "{rb}Storage/{storage_id}".format(**kwargs)
    CreateStorage(
        resource_class_kwargs={
            "rb": rb,
            "suffix": kwargs["suffix"],
            "suffix_id": suffix_id,
            "url": url,
            "chassis_id": chassis_id,
            "id": storage_id,
            "storage_id": storage_id,
            "driList": dri_list,
            "sctrList": sctr_list,
            "volList": vol_list,
        }
    ).put(storage_id)
