# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


"""AccountService

    AccountService processing
"""

import traceback
import logging
from flask_restful import Resource

from .templates.AccountService import get_AccountService_instance

config = {}

INTERNAL_ERROR = 500


class AccountServiceAPI(Resource):
    """AccountService acquisition and operation
    Class to acquisition and operation AccountService
    """

    def __init__(self, **kwargs):
        logging.info("AccountServiceAPI init called")
        try:
            global config  # pylint: disable=W0603
            config = get_AccountService_instance(kwargs)
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()

    # HTTP GET
    def get(self):
        """GET AccountService"""
        logging.info("AccountServiceAPI GET called")
        try:
            resp = config, 200
        except Exception:  # pylint: disable=W0718
            traceback.print_exc()
            resp = INTERNAL_ERROR
        return resp

    # HTTP PUT
    def put(self):
        """PUT AccountService"""
        logging.info("AccountServiceAPI PUT called")
        return "PUT is not a supported command for AccountServiceAPI", 405

    # HTTP POST
    def post(self):
        """POST AccountService"""
        logging.info("AccountServiceAPI POST called")
        return "POST is not a supported command for AccountServiceAPI", 405

    # HTTP PATCH
    def patch(self):
        """PATCH AccountService"""
        logging.info("AccountServiceAPI PATCH called")
        return "PATCH is not a supported command for AccountServiceAPI", 405

    # HTTP DELETE
    def delete(self):
        """DELETE AccountService"""
        logging.info("AccountServiceAPI DELETE called")
        return "DELETE is not a supported command for AccountServiceAPI", 405
