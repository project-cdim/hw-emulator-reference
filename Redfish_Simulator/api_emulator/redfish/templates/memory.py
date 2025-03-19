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


from copy import deepcopy

_TEMPLATE = {
    '@odata.context': '{rb}$metadata#Memory.Memory',
    '@odata.id': "{rb}{suffix}/{suffix_id}/Memory/{memory_id}",
    '@odata.type': '#Memory.v1_20_0.Memory',
    'MaxTDPMilliWatts': [
        12000
    ],
    'CapacityMiB': -1,
    'LogicalSizeMiB': 0,
    'VolatileSizeMiB': 0,
    'NonVolatileSizeMiB': 0,
    'PersistentRegionNumberLimit': 1,
    'PersistentRegionSizeLimitMiB': 8000,
    'PersistentRegionSizeMaxMiB': 8000,
    'VolatileRegionNumberLimit': 1,
    'VolatileRegionSizeLimitMiB': 8000,
    'VolatileRegionSizeMaxMiB': 8000,
    'AllocationAlignmentMiB': 123,
    'AllocationIncrementMiB': 50,
    'AllowedSpeedsMHz': [30],
    'OperatingSpeedMhz': 3200,
    'BusWidthBits': 72,
    'DataWidthBits': 64,
    'Enabled': True,
    'Name': 'Memory',
    'Id': '{memory_id}',
    'Links': {
        'Chassis': {
            '@odata.id': '{rb}Chassis/{chassis_id}'
        }
    },
    'Manufacturer': 'Generic',
    'Model': 'Modelxxx',
    'MemoryDeviceType': '',  # DDR4
    'MemoryType': '',  # DRAM,NVDIMM_N,F,P
    'OperatingMemoryModes': [],  # Volatile,PMEM, Block
    'SerialNumber': '{mem_sereal}',
    'PartNumber': '975421-B20',
    'Status': {'Health': 'OK', 'State': 'Enabled'},
    'PowerState': "On",
    'PowerCapability': True,
    'VendorID': 'Generic',
    'MemoryMedia': [
        "DRAM"
    ],
    'MemoryLocation': {
        "Socket": 1,
        "MemoryController": 1,
        "Channel": 1,
        "Slot": 1
    },
    'CXL': {
        'LabelStorageSizeBytes': 1,
        'StagedNonVolatileSizeMiB': 256,
        'StagedVolatileSizeMiB': 256
    },
    "Location": {
        "PartLocation": {
            "LocationOrdinalValue": 0,
            "LocationType": "Slot",
        },
        "PartLocationContext": ""
    },
    "Metrics": {
        "@odata.id": "{rb}{suffix}/{suffix_id}/Memory/{memory_id}/MemoryMetrics"
    },
    "EnvironmentMetrics": {
        "@odata.id": "{rb}{suffix}/{suffix_id}/Memory/{memory_id}/EnvironmentMetrics"
    },
    "Actions": {
        "#Memory.Reset": {
            "target": "{rb}{suffix}/{suffix_id}/Memory/{memory_id}/Actions/Memory.Reset",
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
            "#Memory.MetricState": {
                "target": "{rb}{suffix}/{suffix_id}/Memory/{memory_id}/Actions/Memory.MetricState",
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


def format_memory_template(**kwargs):
    """
    Format the processor template -- returns the template
    """
    # params:
    defaults = {'rb': '/redfish/v1/',
                'capacitymb': 16384,
                'devicetype': 'DDR4',
                'type': 'DRAM',
                'operatingmodes': ['Volatile']}

    defaults.update(kwargs)

    c = deepcopy(_TEMPLATE)
    c['@odata.context'] = c['@odata.context'].format(**defaults)
    c['@odata.id'] = c['@odata.id'].format(**defaults)
    c['Id'] = c['Id'].format(**defaults)
    if kwargs.get('mem_sereal') is not None:
        c['SerialNumber'] = c['SerialNumber'].format(**defaults)
    else:
        c['SerialNumber'] = "TJ27JXQY"

    c['Links']['Chassis']['@odata.id'] = c['Links']['Chassis']['@odata.id'].format(**defaults)

    if defaults['linkProcessors'] is not None:
        processor = [{"@odata.id": "{rb}Processors/{linkProcessors}".format(rb=defaults['rb'], linkProcessors=x)}
                     for x in defaults['linkProcessors']]
        c['Links']['Processors'] = processor

    if 'pcie_id' in defaults:
        c['Links']['PCIeDevice'] = {}
        c['Links']['PCIeDevice']['@odata.id'] = '{rb}Chassis/{chassis_id}/PCIeDevices/{pcie_id}'.format(**defaults)

    c['Metrics']['@odata.id'] = c['Metrics']['@odata.id'].format(**defaults)
    c['EnvironmentMetrics']['@odata.id'] = c['EnvironmentMetrics']['@odata.id'].format(**defaults)

    c['Model'] = defaults['model']
    if 'state' in defaults['dev_param']:
        c['Status']['State'] = defaults['dev_param']['state']
    if 'health' in defaults['dev_param']:
        c['Status']['Health'] = defaults['dev_param']['health']
    if 'capacityMiB' in defaults['dev_param']:
        c['CapacityMiB'] = defaults['dev_param']['capacityMiB']
    if 'operatingSpeedMhz' in defaults['dev_param']:
        c['OperatingSpeedMhz'] = defaults['dev_param']['operatingSpeedMhz']

    c['MemoryDeviceType'] = defaults['devicetype']
    c['MemoryType'] = defaults['type']
    c['OperatingMemoryModes'] = defaults['operatingmodes']

    if 'Actions' in c:
        c['Actions']['#Memory.Reset']['target'] = c['Actions']['#Memory.Reset']['target'].format(**defaults)
        c['Actions']['Oem']['#Memory.MetricState']['target'] = c['Actions']['Oem']['#Memory.MetricState']['target'].format(**defaults)

    if 'reset_action' in defaults:
        if defaults['reset_action'] == 'invalid':
            del c['Actions']['#Memory.Reset']

    return c
