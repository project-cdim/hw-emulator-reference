# Copyright Notice:
# Copyright 2017-2019 DMTF. All rights reserved.
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

# Manager Template File

import copy

_TEMPLATE = \
{
    "@Redfish.Copyright": "Copyright 2014-2019 DMTF. All rights reserved.",
    "@odata.context": "{rb}$metadata#Manager.Manager",
    "@odata.id": "{rb}Managers/{id}",
    "@odata.type": "#Manager.v1_20_0.Manager",
    "Id": "{id}",
    "Name": "Manager",
    "ManagerType": "BMC",
    "Description": "BMC",
    "ServiceEntryPointUUID": "92384634-2938-2342-8820-489239905423",
    "UUID": "00000000-0000-0000-0000-000000000000",
    "Model": "Joo Janta 200",
    "DateTime": "2015-03-13T04:14:33+06:00",
    "DateTimeLocalOffset": "+06:00",
    "Status": {
        "State": "Enabled",
        "Health": "OK"
    },
    "PowerState": "On",
    "AdditionalFirmwareVersions": {
        "Bootloader": "v2022.01",
        "Kernel": "Linux 5.13.0-30-generic arm71",
    },
    "GraphicalConsole": {
        "ServiceEnabled": True,
        "MaxConcurrentSessions": 2,
        "ConnectTypesSupported": [
            "KVMIP"
        ]
    },
    "SerialConsole": {
        "ServiceEnabled": True,
        "MaxConcurrentSessions": 1,
        "ConnectTypesSupported": [
            "Telnet",
            "SSH",
            "IPMI"
        ]
    },
    "SerialNumber": "Manager12345",
    "PartNumber": "Manager6789",
    "Manufacturer": "",
    "CommandShell": {
        "ServiceEnabled": True,
        "MaxConcurrentSessions": 4,
        "ConnectTypesSupported": [
            "Telnet",
            "SSH"
        ]
    },
    "FirmwareVersion": "1.00",
    "LastResetTime": "2015-03-13T04:14:33+06:00",
    "Location": {
        "PartLocation": {
            "LocationOrdinalValue": 0,
            "LocationType": "Slot",
        },
        "PartLocationContext": ""
    },
    "NetworkProtocol": {
        "@odata.id": "{rb}Managers/{id}/NetworkProtocol"
    },
    "EthernetInterfaces": {
        "@odata.id": "{rb}Managers/{id}/EthernetInterfaces"
    },
    "SerialInterfaces": {
        "@odata.id": "{rb}Managers/{id}/SerialInterfaces"
    },
    "LogServices": {
        "@odata.id": "{rb}Managers/{id}/LogServices"
    },
    "VirtualMedia": {
        "@odata.id": "{rb}Managers/{id}/VM1"
    },
    "Links": {
        "ManagerForServers": [
            {
                "@odata.id": "{rb}Systems/{linkSystem}"
            }
        ],
        "ManagerForChassis": [
            {
                "@odata.id": "{rb}Chassis/{linkChassis}"
            }
        ],
        "ManagerInChassis": {
            "@odata.id": "{rb}Chassis/{linkInChassis}"
        }
    },
    "Actions": {
        "#Manager.Reset": {
            "target": "{rb}Managers/{id}/Actions/Manager.Reset",
            "ResetType@Redfish.AllowableValues": [
                "ForceRestart",
                "GracefulRestart"
            ]
        }
    }
}


def get_Manager_instance(wildcards):
    """
    Instantiate and format the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their repalcement values

    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)

    c['NetworkProtocol']['@odata.id'] = c['NetworkProtocol']['@odata.id'].format(**wildcards)
    c['EthernetInterfaces']['@odata.id'] = c['EthernetInterfaces']['@odata.id'].format(**wildcards)
    c['SerialInterfaces']['@odata.id'] = c['SerialInterfaces']['@odata.id'].format(**wildcards)
    c['LogServices']['@odata.id'] = c['LogServices']['@odata.id'].format(**wildcards)
    c['VirtualMedia']['@odata.id'] = c['VirtualMedia']['@odata.id'].format(**wildcards)

    systems = wildcards['linkSystem']
    if type(systems) is list:
        mfs = [{'@odata.id': c['Links']['ManagerForServers'][0]['@odata.id'].format(rb=wildcards['rb'], linkSystem=x)}
               for x in systems]
    else:
        mfs = [{'@odata.id': c['Links']['ManagerForServers'][0]['@odata.id'].format(**wildcards)}]

    chaasis = wildcards['linkChassis']
    if type(chaasis) is list:
        mfc = [{'@odata.id': c['Links']['ManagerForChassis'][0]['@odata.id'].format(rb=wildcards['rb'], linkChassis=x)}
               for x in chaasis]
    else:
        mfc = [{'@odata.id': c['Links']['ManagerForChassis'][0]['@odata.id'].format(**wildcards)}]

    c['Links']['ManagerForServers'] = mfs
    c['Links']['ManagerForChassis'] = mfc

    c['Links']['ManagerInChassis']['@odata.id'] = c['Links']['ManagerInChassis']['@odata.id'].format(**wildcards)

    c['Actions']['#Manager.Reset']['target'] = c['Actions']['#Manager.Reset']['target'].format(**wildcards)

    return c
