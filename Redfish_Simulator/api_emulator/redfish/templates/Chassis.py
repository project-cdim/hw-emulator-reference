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

# Chassis Template File

import copy
from api_emulator.utils import replace_recurse

_TEMPLATE = \
    {
        "@odata.context": "{rb}$metadata#Chassis.Chassis",
        "@odata.id": "{rb}Chassis/{id}",
        "@odata.type": "#Chassis.v1_26_0.Chassis",
        "Id": "{id}",
        "Name": "Computer System Chassis",
        "ChassisType": "Enclosure",
        "Manufacturer": "Redfish Computers",
        "Model": "3500RX",
        "SKU": "8675309",
        "SerialNumber": "437XR1138R2",
        "UUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "Version": "1.02",
        "PartNumber": "224071-J23",
        "AssetTag": "Chicago-45Z-2381",
        "PowerState": "On",
        "MaxPowerWatts": 800,
        "MinPowerWatts": 50,
        "Status": {
            "State": "Enabled",
            "Health": "OK"
        },
        "Location": {
            "PartLocation": {
                "LocationOrdinalValue": 1,
                "LocationType": "Slot",
            },
            "PartLocationContext": "text"
        },
        "Thermal": {
            "@odata.id": "{rb}Chassis/{id}/Thermal"
        },
        "Power": {
            "@odata.id": "{rb}Chassis/{id}/Power"
        },
        "Processors": {
            "@odata.id": "{rb}Chassis/{id}/Processors"
        },
        "Memory": {
            "@odata.id": "{rb}Chassis/{id}/Memory"
        },
        "Drives": {
            "@odata.id": "{rb}Chassis/{id}/Drives"
        },
        "NetworkAdapters": {
            "@odata.id": "{rb}Chassis/{id}/NetworkAdapters"
        },
        "FabricAdapters": {
            "@odata.id": "{rb}Chassis/{id}/FabricAdapters"
        },
        "PCIeDevices": {
            "@odata.id": "{rb}Chassis/{id}/PCIeDevices"
        },
        "EnvironmentMetrics": {
            "@odata.id": "{rb}Chassis/{id}/EnvironmentMetrics"
        },
        "Sensors": {
            "@odata.id": "{rb}Chassis/{id}/Sensors"
        },
        "Links": {
            "ComputerSystems": [],
            "Drives": [],
            "Processors": [],
            "Storage": [],
            "ResourceBlocks": [],
            "ManagedBy": [],
            "ManagersInChassis": [],
            "ContainedBy": {
                "@odata.id": "{rb}Chassis/{id}"
            },
            "Contains": [],
            "PowerSupplies": []
         }
    }


def get_Chassis_instance(wildcards):
    """
    Creates an instace of TEMPLATE and replace wildcards as specfied
    """
    c = copy.deepcopy(_TEMPLATE)
    compsys = [{"@odata.id": "{rb}Systems/{linkSystem}".format(rb=wildcards['rb'], linkSystem=x)}
               for x in wildcards['linkSystem']]
    drives = [{"@odata.id": "{rb}Chassis/{id}/Drives/{linkDrive}".format(rb=wildcards['rb'], id=wildcards['id'], linkDrive=x)}
              for x in wildcards['linkDrive']]
    proces = [{"@odata.id": "{rb}Chassis/{id}/Processors/{linkProcessor}".format(rb=wildcards['rb'], id=wildcards['id'], linkProcessor=x)}
              for x in wildcards['linkProcessor']]
    rcblocks = [{"@odata.id": "{rb}CompositionService/ResourceBlocks/{linkRB}".format(rb=wildcards['rb'], linkRB=x)}
                for x in wildcards['linkResourceBlocks']]
    managers = [{"@odata.id": "{rb}Managers/{linkMgr}".format(rb=wildcards['rb'], linkMgr=wildcards['linkMgr'])}]
    psupplies = [{"@odata.id": "{rb}Chassis/{id}/PowerSubsystem/PowerSupplies/{ps_id}".format(rb=wildcards['rb'], id=wildcards['id'], ps_id=wildcards['ps_id'])}]

    c['Links']['ComputerSystems'] = compsys
    c['Links']['Drives'] = drives
    c['Links']['Processors'] = proces
    c['Links']['ResourceBlocks'] = rcblocks
    c['Links']['ManagedBy'] = managers
    c['Links']['ManagersInChassis'] = managers
    c['Links']['PowerSupplies'] = psupplies
    replace_recurse(c, wildcards)

    c['Links']['ContainedBy']['@odata.id'] = c['Links']['ContainedBy']['@odata.id'].format(**wildcards)

    if 'Processors' not in wildcards['linkResource']:
        del c['Processors']

    if 'Memory' not in wildcards['linkResource']:
        del c['Memory']

    if 'Drive' not in wildcards['linkResource']:
        del c['Drives']

    if 'NetworkAdapter' not in wildcards['linkResource']:
        del c['NetworkAdapters']

    return c
