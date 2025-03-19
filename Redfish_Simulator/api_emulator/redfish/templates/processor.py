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

# format_processor_template()
from copy import deepcopy

PROCESSOR_TEMPLATE = {
    '@odata.context': '{rb}$metadata#Processor.Processor',
    "@odata.type": "#Processor.v1_20_1.Processor",
    "@odata.id": "{rb}{suffix}/{suffix_id}/Processors/{processor_id}",
    "Name": "Processor",
    "Id": "{processor_id}",
    "ProcessorType": "CPU",
    "ProcessorArchitecture": "x86",
    "InstructionSet": "x86-64",
    "Manufacturer": "{manufacturer}",
    "Model": "{model}",
    "ProcessorId": {
        "VendorId": "GenuineIntel",
        "IdentificationRegisters": "0x34AC34DC8901274A",
        "EffectiveFamily": "0x42",
        "EffectiveModel": "0x61",
        "Step": "0x1",
        "MicrocodeInfo": "0x429943",
        "ProtectedIdentificationNumber": "123456"
    },
    "PowerState": "On",
    "PowerCapability": True,
    "ProcessorIndex": 1,
    "Replaceable": True,
    "SerialNumber": "437XR1138R2",
    "PartNumber": "975421-B20",
    "Socket": "CPU 1",
    'Links': {
        'Chassis': {
            '@odata.id': '{rb}Chassis/{chassis_id}'
        },
        'PCIeDevice': {},
    },
    "MaxSpeedMHz": None,
    "TotalCores": None,
    "TotalThreads": None,
    "TotalEnabledCores": 4,
    "BaseSpeedMHz": None,
    "OperatingSpeedMHz": 3200,
    "TDPWatts": 100,
    "ProcessorMemory": [{
            "CapacityMiB": 123,
            "IntegratedMemory": True,
            "MemoryType": "DDR",
            "SpeedMHz": 1200
        }],
    "MemorySummary": {
        "Metrics": {
            "@odata.id": "{rb}Systems/{sys_id}/Processors/{processor_id}/MemorySummary/MemoryMetrics"
        },
        "TotalCacheSizeMiB": 4096,
        "TotalMemorySizeMiB": 8192,
        "ECCModeEnabled": True
    },
    "Metrics": {
        "@odata.id": "{rb}Systems/{sys_id}/Processors/{processor_id}/ProcessorMetrics"
    },
    "EnvironmentMetrics": {
        "@odata.id": "{rb}Systems/{sys_id}/Processors/{processor_id}/EnvironmentMetrics"
    },
    "Status": {'Health': 'OK', 'State': 'Enabled'},
    "Enabled": True,
    "Actions": {
        "#Processor.Reset": {
            "target": "{rb}{suffix}/{suffix_id}/Processors/{processor_id}/Actions/Processor.Reset",
            "ResetType@Redfish.AllowableValues": [
                "On",
                "ForceOff",
                "GracefulShutdown",
                "GracefulRestart",
                "ForceRestart",
                "ForceOn"
            ]
        },
        "Oem": {
            "#Processor.MetricState": {
                "target": "{rb}{suffix}/{suffix_id}/Processors/{processor_id}/Actions/Processor.MetricState",
                "StateType@Redfish.AllowableValues": [
                    "off",
                    "steady",
                    "low",
                    "high",
                    "action"
                ]
            }
            
        }
    }
}


def format_processor_template(**kwargs):
    """
    Format the processor template -- returns the template
    """
    # params:
    defaults = {'rb': '/redfish/v1/',
                'maxspeedmhz': 2200,
                'BaseSpeedMHz': 1200}

    defaults.update(kwargs)

    c = deepcopy(PROCESSOR_TEMPLATE)
    c['@odata.context'] = c['@odata.context'].format(**defaults)
    c['@odata.id'] = c['@odata.id'].format(**defaults)
    c['Id'] = c['Id'].format(**defaults)
    c['Links']['Chassis']['@odata.id'] = c['Links']['Chassis']['@odata.id'].format(**defaults)
    
    if 'Actions' in c:
        c['Actions']['#Processor.Reset']['target'] = c['Actions']['#Processor.Reset']['target'].format(**defaults)
        c['Actions']['Oem']['#Processor.MetricState']['target'] = c['Actions']['Oem']['#Processor.MetricState']['target'].format(**defaults)

    if 'state' in defaults['dev_param']:
        c['Status']['State'] = defaults['dev_param']['state']
    if 'health' in defaults['dev_param']:
        c['Status']['Health'] = defaults['dev_param']['health']

    c['Model'] = c['Model'].format(**defaults)
    c['Manufacturer'] = c['Manufacturer'].format(**defaults)
    c['ProcessorType'] = defaults['processorType']

    if 'port_id' in defaults:
        c['Ports'] = {"@odata.id": "{rb}Systems/{sys_id}/Processors/{processor_id}/Ports".format(rb=defaults['rb'],
                                                                                                 sys_id=defaults['sys_id'], processor_id=defaults['processor_id'])}

    if 'totalEnabledCores' in defaults['dev_param']:
        c['TotalEnabledCores'] = defaults['dev_param']['totalEnabledCores']
    
    if 'operatingSpeedMHz' in defaults['dev_param']:
        c['OperatingSpeedMHz'] = defaults['dev_param']['operatingSpeedMHz']

    if 'linkProcs' in defaults:
        if 0 < len(defaults['linkProcs']):
            processor = [{"@odata.id": "{rb}{suffix}/{suffix_id}/Processors/{linkProcs}".format(rb=defaults['rb'], suffix=defaults['suffix'], suffix_id=defaults['suffix_id'], linkProcs=x)}
                         for x in defaults['linkProcs']]
            c['Links']['ConnectedProcessors'] = processor

    if 'linkMemorys' in defaults:
        if 0 < len(defaults['linkMemorys']):
            memory = [{"@odata.id": "{rb}{suffix}/{suffix_id}/Memory/{linkMemorys}".format(rb=defaults['rb'], suffix=defaults['suffix'], suffix_id=defaults['suffix_id'], linkMemorys=x)}
                      for x in defaults['linkMemorys']]
            c['Links']['Memory'] = memory

    if 'linkNicDfuncs' in defaults:
        if 0 < len(defaults['linkNicDfuncs']):
            nicdf = [{"@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{ndf_id}".format(rb=defaults['rb'], chassis_id=defaults['chassis_id'], na_id=x['nic'], ndf_id=x['ndf'])}
                     for x in defaults['linkNicDfuncs']]
            c['Links']['NetworkDeviceFunctions'] = nicdf

    if 'linkFabrics' in defaults:
        if 0 < len(defaults['linkFabrics']):
            fabric = [{"@odata.id": "{rb}{suffix}/{suffix_id}/FabricAdapters/{linkFabrics}".format(rb=defaults['rb'], suffix=defaults['suffix'], suffix_id=defaults['suffix_id'], linkFabrics=x)}
                      for x in defaults['linkFabrics']]
            c['Links']['FabricAdapters'] = fabric

    if 'pcie_id' in defaults:
        c['Links']['PCIeDevice'] = {}
        c['Links']['PCIeDevice']['@odata.id'] = '{rb}Chassis/{chassis_id}/PCIeDevices/{pcie_id}'.format(**defaults)
    if 'sys_id' in defaults and defaults.get('sys_id'):
        c['MemorySummary']['Metrics']['@odata.id'] = c['MemorySummary']['Metrics']['@odata.id'].format(**defaults)
        c['Metrics']['@odata.id'] = c['Metrics']['@odata.id'].format(**defaults)
        c['EnvironmentMetrics']['@odata.id'] = c['EnvironmentMetrics']['@odata.id'].format(**defaults)
    else:
        del c['MemorySummary']['Metrics']
        del c['Metrics']
        del c['EnvironmentMetrics']

    c['MaxSpeedMHz'] = defaults['maxspeedmhz']
    c['BaseSpeedMHz'] = defaults['BaseSpeedMHz']

    if 'serialNumber' in defaults:
        c['SerialNumber'] = defaults['serialNumber']
    if kwargs.get('gpu_sereal') is not None:
        c['SerialNumber'] = '{gpu_sereal}'.format(**defaults)
    if 'totalCores' in defaults['dev_param']:
        c['TotalCores'] = defaults['dev_param']['totalCores']
        c['TotalThreads'] = defaults.get('totalthreads', 2*defaults['dev_param']['totalCores'])
    else:
        c['TotalCores'] = 4
        c['TotalThreads'] = defaults.get('totalthreads', 2*4)

    if 'capacityMiB' in defaults['dev_param']:
        c['ProcessorMemory'][0]['CapacityMiB'] = defaults['dev_param']['capacityMiB']

    if 'socketNum' in defaults['dev_param']:
        c['Socket'] = 'CPU {socketNum}'.format(**defaults['dev_param'])

    if 'processorArchitecture' in defaults['dev_param']:
        c['ProcessorArchitecture'] = defaults['dev_param']['processorArchitecture']

    if 'reset_action' in defaults:
        if defaults['reset_action'] == 'invalid':
            del c['Actions']['#Processor.Reset']

    return c
