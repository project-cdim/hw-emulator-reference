# Copyright Notice:
# Copyright 2016-2021 DMTF. All rights reserved.
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

# Redfish Event Service and Events

import logging

class Subscription(object):
	"""
	Subscription class
	"""
	def __init__(self, rest_base, idx, dest, types, context):
		"""
		Subscription constructor

		Arguments:
			rest_base - Base URL of the RESTful interface
			idx - Subscription id
			dest - URI where events should be sent
			types- Event types (Alert, StatusChange, ResourceAdded, ResourceUpdated, ResourceDeleted)
			context - User name
		"""
		self.rb = rest_base

		self.config = {
			'@odata.id': '/redfish/v1/EventService/Subscriptions/' + str(idx),
			'@odata.type': '#EventDestination.v1_10_1.EventDestination',
			'Id': str(idx),
			'Name': 'EventDestination ' + str(idx),
			'Destination': dest,
			'EventTypes': types,
			'Context': context,
			'Protocol': 'Redfish'
		}

	@property
	def configuration(self):
		"""
		Configuration property.
		"""
		c = self.config.copy()
		return c

class Subscriptions(object):
	"""
	Event Subscriptions
	"""
	def __init__(self, rest_base):
		"""
		Subscription collection constructor

		Arguments:
			rest_base - Base URL of the RESTful interface
		"""
		self.rb = rest_base
		self.members = []

		self.config = {
			'@odata.type': '#EventDestinationCollection.EventDestinationCollection',
			'Name': 'Event Subscription Collection',
			'Members': {},
			'Members@odata.count': 0
		}

	@property
	def configuration(self):
		"""
		Configuration property.
		"""

		logging.info('configurations caaaaaaaaalled')
		
		c = self.config.copy()
		c['Members@odata.count'] = len(self.members)
		c['Members'] = self.members
		logging.info(c)
		resp = self.config
		logging.info(resp)
		return resp

	def add_subscription(self, destination, types, context):
		"""
		Add subscription to the collection

		Arguments:
			destination - Event destination URI
			types - Event types
			context - User name
		"""
		sub_id = len(self.members) + 1
		sub = Subscription(self.rb, sub_id, destination, types, context)
		self.members.append('/redfish/v1/EventService/Subscriptions/' + str(sub_id))
		return sub

class EventService(object):
	"""
	Event Service class
	"""
	def __init__(self, rest_base):
		"""
		EventService Constructor

		Arguments:
			rest_base - Base URL of the RESTful interface
		"""
		self.rb = rest_base


		self.config = {
			'@odata.id': self.rb + 'EventService',
			'@odata.type': '#EventService.1_7_0.EventService',
			'Name': 'Event Service',
			'ServiceEnabled': True,
			'DeliveryRetryAttempts': 3,
			'DeliveryRetryIntervalInSeconds': 60,
			'EventTypesForSubscription': ['StatusChange',
										  'ResourceUpdated',
										  'ResourceAdded',
										  'ResourceRemoved',
										  'Alert'
										  ],
			'Subscriptions': {
			  '@odata.id': '/redfish/v1/EventService/Subscriptions'
			},
			'Actions': {
						'#EventService.SendTestEvent': {
							'target': '/redfish/v1/EventService/Actions/EventService.SendTestEvent',
							'EventType@Redfish.AllowableValues': [
								  'StatusChange',
								  'ResourceUpdated',
								  'ResourceAdded',
								  'ResourceRemoved',
								  'Alert'
								  ]
							},
						'Oem': {}
					},
			'Oem': {}
		}

	@property
	def configuration(self):
		"""
		Configuration property.
		"""
		c = self.config.copy()
		return c
