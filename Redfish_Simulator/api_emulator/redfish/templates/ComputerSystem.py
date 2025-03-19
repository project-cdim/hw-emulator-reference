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

# Example Resoruce Template
import copy

_TEMPLATE = \
{
    "@odata.context": "{rb}$metadata#ComputerSystem.ComputerSystem",
    "@odata.id": "{rb}Systems/{id}",
    "@odata.type": "#ComputerSystem.v1_23_1.ComputerSystem",
    "Id": "{id}",
    "Name": "My Computer System",
    "SystemType": "Physical",
    "AssetTag": "free form asset tag",
    "Manufacturer": "Manufacturer Name",
    "Model": "Model Name",
    "SKU": "",
    "SerialNumber": "2M220100SL",
    "PartNumber": "",
    "Description": "Description of server",
    "UUID": "00000000-0000-0000-0000-000000000000",
    "HostName": "web-srv344",
    "Status": {
        "State": "Enabled",
        "Health": "OK",
        "HealthRollup": "OK"
    },
    "LocationIndicatorActive": False,
    "PowerState": "On",
    "Boot": {
        "BootSourceOverrideEnabled": "Once",
        "BootSourceOverrideMode": "UEFI",
        "BootSourceOverrideTarget": "Pxe",
        "BootSourceOverrideTarget@Redfish.AllowableValues": [
            "None",
            "Pxe",
            "Floppy",
            "Cd",
            "Usb",
            "Hdd",
            "BiosSetup",
            "Utilities",
            "Diags",
            "UefiTarget",
            "SDCard",
            "UefiHttp"
        ],
        "UefiTargetBootSourceOverride": "uefi device path",
        "BootOptions": {"@odata.id": "{rb}Systems/{id}/BootOptions/1"},
        "BootOrder": []
    },
    "BootProgress": {
        "LastBootTimeSeconds": 676,
        "LastState": "OSRunning",
        "LastStateTime": "2022-10-03T20:00:00Z"
    },
    "LastResetTime": "2022-10-03T20:00:00Z",
    "BiosVersion": "P79 v1.00 (09/20/2013)",
    "ProcessorSummary": {
        "Count": 8,
        "Model": "Multi-Core Intel(R) Xeon(R) processor 7xxx Series",
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollup": "OK"
        }
    },
    "MemorySummary": {
        "TotalSystemMemoryGiB": 16,
        "MemoryMirroring": "System",
        "Status": {
            "State": "Enabled",
            "Health": "OK",
            "HealthRollup": "OK"
        }
    },
    "TrustedModules": [
        {
            "Status": {
                 "State": "Enabled",
                 "Health": "OK"
            },
            "FirmwareVersion": "3.1",
            "FirmwareVersion2": "1",
            "InterfaceTypeSelection": "None"
        }
    ],
    "Processors": {
        "@odata.id": "{rb}Systems/{id}/Processors"
    },
    "Memory": {
        "@odata.id": "{rb}Systems/{id}/Memory"
    },
    "EthernetInterfaces": {
        "@odata.id": "{rb}Systems/{id}/EthernetInterfaces"
    },
    "Storage": {
            "@odata.id": "{rb}Systems/{id}/Storage"
    },
    "SimpleStorage": {
        "@odata.id": "{rb}Systems/{id}/SimpleStorage"
    },
    "NetworkInterfaces": {
        "@odata.id": "{rb}Systems/{id}/NetworkInterfaces"
    },
    "FabricAdapters": {
        "@odata.id": "{rb}Systems/{id}/FabricAdapters"
    },
    "GraphicsControllers": {
        "@odata.id": "{rb}Systems/{id}/GraphicsControllers"
    },
    "VirtualMedia": {
        "@odata.id": "{rb}Systems/{id}/VirtualMedia"
    },
    "PCIeDevices": [
        {
            "@odata.id": "{rb}Chassis/{linkChassis}/PCIeDevices/PROC-0001"
        }
    ],
    "Chassis": [
            {
                "@odata.id": "{rb}Chassis/{linkChassis}"
            }
    ],
    "Links": {
        "Chassis": [
            {
                "@odata.id": "{rb}Chassis/{linkChassis}"
            }
        ],
        "ManagedBy": [
            {
                "@odata.id": "{rb}Managers/{linkMgr}"
            }
        ],
        "Oem": {},
        "ResourceBlocks": [
            {
                "@odata.id": "{rb}CompositionService/ResourceBlocks/{BlockId}"
            }
        ]
    },
    "Actions": {
        "#ComputerSystem.Reset": {
            "target": "{rb}Systems/{id}/Actions/ComputerSystem.Reset", "@Redfish.ActionInfo": "{rb}Systems/{id}/ResetActionInfo",
            "ResetType@Redfish.AllowableValues": [
                "On",
                "ForceOff",
                "GracefulShutdown",
                "GracefulRestart",
                "ForceRestart",
                "ForceOn"
            ]
        },
    }
}


def get_ComputerSystem_instance(wildcards):
    """
    Instantiate and format the template

    Arguments:
        wildcard - A dictionary of wildcards strings and their repalcement values

    """
    c = copy.deepcopy(_TEMPLATE)

    c['@odata.context'] = c['@odata.context'].format(**wildcards)
    c['@odata.id'] = c['@odata.id'].format(**wildcards)
    c['Id'] = c['Id'].format(**wildcards)

    if 'Processors' in wildcards['linkResource'] and wildcards['linkResource']['Processors']:
        c['Processors']['@odata.id'] = "{rb}Systems/{id}/Processors".format(**wildcards)
    else:
        del c['Processors']
    
    if 'Memory' in wildcards['linkResource'] and wildcards['linkResource']['Memory']:
        c['Memory']['@odata.id'] = c['Memory']['@odata.id'].format(**wildcards)
    else:
        del c['Memory']

    if 'Storage' in wildcards['linkResource'] and wildcards['linkResource']['Storage']:
        c['Storage']['@odata.id'] = c['Storage']['@odata.id'].format(**wildcards)
    else:
        del c['Storage']

    if 'NetworkInterfaces' in wildcards['linkResource'] and wildcards['linkResource']['NetworkInterfaces']:
        c['NetworkInterfaces']['@odata.id'] = c['NetworkInterfaces']['@odata.id'].format(**wildcards)
    else:
        del c['NetworkInterfaces']

    c['EthernetInterfaces']['@odata.id'] = c['EthernetInterfaces']['@odata.id'].format(**wildcards)
    c['SimpleStorage']['@odata.id'] = c['SimpleStorage']['@odata.id'].format(**wildcards)

    if 'GraphicControllers' in wildcards['linkResource'] and wildcards['linkResource']['GraphicControllers']:
        c['GraphicsControllers']['@odata.id'] = c['GraphicsControllers']['@odata.id'].format(**wildcards)
    else:
        del c['GraphicsControllers']

    c['FabricAdapters']['@odata.id'] = c['FabricAdapters']['@odata.id'].format(**wildcards)
    c['VirtualMedia']['@odata.id'] = c['VirtualMedia']['@odata.id'].format(**wildcards)

    chassis = [{'@odata.id': "{rb}Chassis/{linkChassis}".format(rb=wildcards['rb'], linkChassis=x)}
               for x in wildcards['linkChassis']]

    pcie_d = [{'@odata.id': "{rb}Chassis/{linkChassis}/PCIeDevices/PCIe-0001".format(rb=wildcards['rb'], linkChassis=x)}
              for x in wildcards['linkChassis']]
    c['PCIeDevices'] = pcie_d

    c['Chassis'] = chassis
    c['Links']['Chassis'] = chassis
    c['Links']['ManagedBy'][0]['@odata.id'] = c['Links']['ManagedBy'][0]['@odata.id'].format(**wildcards)
    if 'BlockId' in wildcards:
        c['Links']['ResourceBlocks'][0]['@odata.id'] = c['Links']['ResourceBlocks'][0]['@odata.id'].format(**wildcards)
    else:
        c['Links']['ResourceBlocks'] = []
    c['Links']['ResourceBlocks@odata.count'] = len(c['Links']['ResourceBlocks'])

    c['Actions']['#ComputerSystem.Reset']['target'] = c['Actions']['#ComputerSystem.Reset']['target'].format(**wildcards)
    c['Actions']['#ComputerSystem.Reset']['@Redfish.ActionInfo'] = c['Actions']['#ComputerSystem.Reset']['@Redfish.ActionInfo'].format(**wildcards)

    return c
