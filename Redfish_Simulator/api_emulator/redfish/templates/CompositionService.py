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

# CompositionService Template File

import copy
import strgen

_TEMPLATE = \
{
	"@odata.context": "{rb}$metadata#CompositionService.CompositionService",
	"@odata.type": "#CompositionService.v1_0_0.CompositionService",
	"@odata.id": "{rb}CompositionService",
	"Id": "{id}",
	"Name": "Composition Service",
	"Status": {
		"State": "Enabled",
		"Health": "OK"
	},
	"ServiceEnabled": True,
	"ResourceBlocks": {
		"@odata.id": "{rb}CompositionService/ResourceBlocks"
	},
	"ResourceZones": {
		"@odata.id": "{rb}CompositionService/ResourceZones"
	}
}


def get_CompositionService_instance(wildcards):
	"""
	Instantiates and formats the template

	Arguments:
		wildcard - A dictionary of wildcards strings and their repalcement values
	"""
	c = copy.deepcopy(_TEMPLATE)

	c['@odata.context'] = c['@odata.context'].format(**wildcards)
	c['@odata.id'] = c['@odata.id'].format(**wildcards)
	c['Id'] = c['Id'].format(**wildcards)
	c['ResourceBlocks']['@odata.id'] = c['ResourceBlocks']['@odata.id'].format(**wildcards)
	c['ResourceZones']['@odata.id'] = c['ResourceZones']['@odata.id'].format(**wildcards)

	return c
