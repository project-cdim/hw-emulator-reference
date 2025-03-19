# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""
Collection API:  GET, POST
Singleton  API:  GET, POST, PATCH, DELETE
"""

import traceback
import os
import logging
from flask_restful import Resource
import g

# Resource and SubResource imports
from .templates.ManagerAccount import get_ManagerAccount_instance

members = {}

INTERNAL_ERROR = 500


class ManagerAccountAPI(Resource):
    """ManagerAccount Acquisition and Operation API
    Class to acquisition and operation ManagerAccount
    """

    def __init__(self, **kwargs):
        pass

    def get(self, ident):
        """GET ManagerAccount"""
        logging.info("ManagerAccountAPI GET called")
        try:
            # Find the entry with the correct value for Id
            resp = 404
            if ident in members:
                resp = members[ident], 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        """PUT ManagerAccount"""
        logging.info("ManagerAccountAPI PUT called")
        return "PUT is not a supported command for ManagerAccountAPI", 405

    # HTTP POST
    def post(self):
        """POST ManagerAccount"""
        logging.info("ManagerAccountAPI POST called")
        return "POST is not a supported command for ManagerAccountAPI", 405

    # HTTP PATCH
    def patch(self):
        """PATCH ManagerAccount"""
        logging.info("ManagerAccountAPI PATCH called")
        return "PATCH is not a supported command for ManagerAccountAPI", 405

    # HTTP DELETE
    def delete(self):
        """DELETE ManagerAccount"""
        logging.info("ManagerAccountAPI DELETE called")
        return "DELETE is not a supported command for ManagerAccountAPI", 405


# ManagerAccount Collection API
class ManagerAccountCollectionAPI(Resource):
    """ManagerAccount Collection Management API
    Class to manage the collection of ManagerAccount
    """

    def __init__(self):
        logging.info("ManagerAccountCollectionAPI init called")
        self.rb = os.path.join(g.rest_base, "AccountService/")
        self.config = {
            "@odata.id": self.rb + "Accounts",
            "@odata.type": "#ManagerAccountCollection.ManagerAccountCollection",
            "Name": "ManagerAccount Collection",
            "Members": [],
            "Members@odata.count": 0,
        }
        self.config["Members@odata.count"] = len(members)
        self.config["Members"] = [
            {"@odata.id": x["@odata.id"]} for x in list(members.values())
        ]

    # HTTP GET
    def get(self):
        """GET ManagerAccount collection"""
        logging.info("ManagerAccountCollectionAPI GET called")
        try:
            resp = self.config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        """PUT ManagerAccount collection"""
        logging.info("ManagerAccountCollectionAPI PUT called")
        return "PUT is not a supported command for ManagerAccountCollectionAPI", 405

    # HTTP POST
    def post(self):
        """POST ManagerAccount collection"""
        logging.info("ManagerAccountCollectionAPI POST called")
        return "POST is not a supported command for ManagerAccountCollectionAPI", 405

    # HTTP PATCH
    def patch(self):
        """PATCH ManagerAccount collection"""
        logging.info("ManagerAccountCollectionAPI PATCH called")
        return "PATCH is not a supported command for ManagerAccountCollectionAPI", 405

    # HTTP DELETE
    def delete(self):
        """DELETE ManagerAccount collection"""
        logging.info("ManagerAccountCollectionAPI DELETE called")
        return "DELETE is not a supported command for ManagerAccountCollectionAPI", 405


def create_manager_account(**kwargs):
    """Create ManagerAccount"""
    logging.info("CreateManagerAccount called")

    mem_id = len(members) + 1
    if str(mem_id) not in members:
        members[str(mem_id)] = {}
        kwargs["account_id"] = str(mem_id)
        members[str(mem_id)] = get_ManagerAccount_instance(**kwargs)
