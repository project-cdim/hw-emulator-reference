# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md
#
# The original DMTF contents of this file have been modified to support
# The Redfish Interface Emulator. These modifications are subject to the following:
# Copyright 2025 NEC Corporation
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# EventService API File

"""
Collection API:  GET
Singleton  API:  (None)
"""

import g

import sys, traceback
import logging
import copy
from flask import Flask, request, make_response, render_template
from flask_restful import reqparse, Api, Resource

# Resource and SubResource imports
from .templates.EventService import get_EventService_instance
from .Subscriptions_api import SubscriptionCollectionAPI, SubscriptionAPI, CreateSubscription

config = {}

INTERNAL_ERROR = 500


# EventService Singleton API
# EventService does not have a Singleton API


# EventService Collection API
class EventServiceAPI(Resource):

	def __init__(self, **kwargs):
		logging.info('EventServiceAPI init called')
		try:
			global config
			config = get_EventService_instance(kwargs)
			resp = config, 200
		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR

	# HTTP GET
	def get(self):
		logging.info('EventServiceAPI GET called')
		try:
			global config
			resp = config, 200
		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		return resp

	# HTTP PUT
	def put(self):
		logging.info('EventServiceAPI PUT called')
		return 'PUT is not a supported command for EventServiceAPI', 405

	# HTTP POST
	def patch(self):
		logging.info('EventServiceAPI POST called')
		return 'POST is not a supported command for EventServiceAPI', 405

	# HTTP PATCH
	def patch(self):
		logging.info('EventServiceAPI PATCH called')
		return 'PATCH is not a supported command for EventServiceAPI', 405

	# HTTP DELETE
	def delete(self):
		logging.info('EventServiceAPI DELETE called')
		return 'DELETE is not a supported command for EventServiceAPI', 405


# CreateEventService
#
# Called internally to create instances of a resource. If the
# resource has subordinate resources, those subordinate resource(s)
# are created automatically.
#
# Note: In 'init', the first time through, kwargs may not have any
# values, so we need to check. The call to 'init' stores the path
# wildcards. The wildcards are used to modify the resource template
# when subsequent calls are made to instantiate resources.
#
# TODO: Determine need for CreateEventService
class CreateEventService(Resource):

	def __init__(self, **kwargs):
		logging.info('CreateEventService init called')
		if 'resource_class_kwargs' in kwargs:
			global wildcards
			wildcards = copy.deepcopy(kwargs['resource_class_kwargs'])

	# Attach APIs for subordinate resource(s). Attach the APIs for
	# a resource collection and its singletons.
	def put(self,ident):
		logging.info('CreateEventService put called')
		try:
			global config
			global wildcards
			wildcards['id'] = ident
			config=get_EventService_instance(wildcards)
			g.api.add_resource(SubscriptionCollectionAPI,   '/redfish/v1/EventService/Subscriptions')
			g.api.add_resource(SubscriptionAPI,             '/redfish/v1/EventService/Subscriptions/<string:ident>', resource_class_kwargs={'rb': g.rest_base})
			# Create an instance of subordinate subscription resource
			cfg = CreateSubscription()
			out = cfg.__init__(resource_class_kwargs={'rb': g.rest_base,'id':"1"})
			out = cfg.put("1")
			resp = config, 200
		except Exception:
			traceback.print_exc()
			resp = INTERNAL_ERROR
		logging.info('CreateEventService put exit')
		return resp



_TEST_EVENT_TEMPLATE = \
{
	"Events@odata.count": 1,
	"Id": "{Id}",
	"Events": [
		{
			"MessageArgs": {},
			"Message": "{Message}",
			"EventGroupId": "{EventGroupId}",
			"EventId": "1",
			"MemberId": "0001",
			"MessageId": "{MessageId}",
			"EventTimestamp": "{EventTimestamp}",
			"OriginOfCondition": {
				"@odata.id": "{OriginOfCondition}"
			}
		}
	],
	"@odata.type": "#Event.v1_5_0.Event",
	"Name": "SubmitTestEvent",
	"Description": "This resource represents an event for a Redfish implementation."
}

class EventServiceActions_SubmitTestEventAPI(Resource):

	def __init__(self, **kwargs):
		pass

	def post(self):
		resp = INTERNAL_ERROR
		req = request.get_json()
		logging.info('EventServiceActions_SubmitTestEventAPI')
		
		c = copy.deepcopy(_TEST_EVENT_TEMPLATE)

		c['Id'] = req['EventId']
		c['Events'][0]['Message'] = req['Message']
		c['Events'][0]['MessageArgs'] = req['MessageArgs']
		c['Events'][0]['EventGroupId'] = req['EventGroupId']
		c['Events'][0]['MessageId'] = req['MessageId']
		c['Events'][0]['EventTimestamp'] = req['EventTimestamp']
		c['Events'][0]['OriginOfCondition']['@odata.id'] = req['OriginOfCondition']

		resp = c, 200
		return resp