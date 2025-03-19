# Copyright Notice:
# Copyright 2016-2019 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/main/LICENSE.md
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

# SessionService Template File

import copy

_TEMPLATE = {
    "@Redfish.Copyright": "Copyright 2014-2021 DMTF. All rights reserved.",
    "@odata.context": "/redfish/v1/$metadata#SessionService.SessionService",
    "@odata.type": "#SessionService.v1_2_0.SessionService",
    "@odata.id": "/redfish/v1/SessionService",
    "Id": "SessionService",
    "Name": "Session Service",
    "Description": "Session Service",
    "Status": {"State": "Enabled", "Health": "OK"},
    "ServiceEnabled": True,
    "SessionTimeout": 30,
    "Sessions": {"@odata.id": "/redfish/v1/SessionService/Sessions"},
}


def get_SessionService_instance(wildcards):
    """
    Instantiates and formats the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their replacement values
    """
    c = copy.deepcopy(_TEMPLATE)

    c["@odata.context"] = c["@odata.context"].format(**wildcards)
    c["@odata.id"] = c["@odata.id"].format(**wildcards)
    c["Id"] = c["Id"].format(**wildcards)
    c["Name"] = c["Name"].format(**wildcards)
    c["Sessions"]["@odata.id"] = c["Sessions"]["@odata.id"].format(**wildcards)

    return c
