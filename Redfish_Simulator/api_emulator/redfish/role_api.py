# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""Role

    Role processing
"""

import traceback
import os
import logging
from flask_restful import Resource
import g

# Resource and SubResource imports
from .templates.Role import get_Role_instance

members = {}

INTERNAL_ERROR = 500


# Role Singleton API
class RoleAPI(Resource):
    """Role Acquisition and Operation API
    Class to acquisition and operation Role
    """

    def __init__(self, **kwargs):
        pass

    # HTTP GET
    def get(self, ident):
        """GET Role"""
        logging.info("RoleAPI GET called")
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
        """PUT Role"""
        logging.info("RoleAPI PUT called")
        return "PUT is not a supported command for RoleAPI", 405

    # HTTP POST
    def post(self):
        """POST Role"""
        logging.info("RoleAPI POST called")
        return "POST is not a supported command for RoleAPI", 405

    # HTTP PATCH
    def patch(self):
        """PATCH Role"""
        logging.info("RoleAPI PATCH called")
        return "PATCH is not a supported command for RoleAPI", 405

    # HTTP DELETE
    def delete(self):
        """DELETE Role"""
        logging.info("RoleAPI DELETE called")
        return "DELETE is not a supported command for RoleAPI", 405


# Role Collection API
class RoleCollectionAPI(Resource):
    """Role Collection Acquisition and Operation API
    Class to acquisition and operation Role Collection
    """

    def __init__(self):
        logging.info("RoleCollectionAPI init called")
        self.rb = os.path.join(g.rest_base, "AccountService/")
        self.config = {
            "@odata.id": self.rb + "Roles",
            "@odata.type": "#RoleCollection.RoleCollection",
            "Name": "Role Collection",
            "Links": {},
        }
        self.config["Links"]["Members@odata.count"] = len(members)
        self.config["Links"]["Members"] = [
            {"@odata.id": x["@odata.id"]} for x in list(members.values())
        ]

    # HTTP GET
    def get(self):
        """GET Role Collection"""
        logging.info("RoleCollectionAPI GET called")
        try:
            resp = self.config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        """PUT Role Collection"""
        logging.info("RoleCollectionAPI PUT called")
        return "PUT is not a supported command for RoleCollectionAPI", 405

    # HTTP POST
    def post(self):
        """POST Role Collection"""
        logging.info("RoleCollectionAPI POST called")
        return "POST is not a supported command for RoleCollectionAPI", 405

    # HTTP PATCH
    def patch(self):
        """PATCH Role Collection"""
        logging.info("RoleCollectionAPI PATCH called")
        return "PATCH is not a supported command for RoleCollectionAPI", 405

    # HTTP DELETE
    def delete(self):
        """DELETE Role Collection"""
        logging.info("RoleCollectionAPI DELETE called")
        return "DELETE is not a supported command for RoleCollectionAPI", 405


def create_role_account(**kwargs):
    """Create Role"""
    logging.info("CreateRoleAccount called")

    mem_id = len(members) + 1
    if str(mem_id) not in members:
        members[str(mem_id)] = {}
        kwargs["role_id"] = str(mem_id)
        members[str(mem_id)] = get_Role_instance(**kwargs)
