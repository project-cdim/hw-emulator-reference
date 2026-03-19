# Copyright Notice:
# Copyright (c) 2016, Contributing Member(s) of Distributed Management Task Force, Inc.. All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/DMTF/Redfish-Interface-Emulator/blob/master/LICENSE.md
#
# The original DMTF contents of this file have been modified to support
# The Redfish Interface Emulator. These modifications are subject to the following:
# Copyright 2025-2026 NEC Corporation
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
 
from api_emulator.redfish.EventService_api import EventServiceAPI, CreateEventService
from api_emulator.redfish.Chassis_api import ChassisCollectionAPI, ChassisAPI, CreateChassis
from api_emulator.redfish.ComputerSystem_api import ComputerSystemCollectionAPI, ComputerSystemAPI, CreateComputerSystem
from api_emulator.redfish.Manager_api import ManagerCollectionAPI, ManagerAPI, CreateManager
from api_emulator.redfish.pcie_switch_api import PCIeSwitchesAPI, PCIeSwitchAPI
from api_emulator.redfish.eg_resource_api import EgResourceCollectionAPI, EgResourceAPI, CreateEgResource
from api_emulator.redfish.power_api import CreatePower
from api_emulator.redfish.thermal_api import CreateThermal
from api_emulator.redfish.ResetAction_api import ResetAction_API
from api_emulator.redfish.ResetActionInfo_api import ResetActionInfo_API
from api_emulator.redfish.processor_api import create_processor
from api_emulator.redfish.memory_api import create_memory, create_chassis_memory
from api_emulator.redfish.simplestorage import CreateSimpleStorage
from api_emulator.redfish.storage_api import create_system_storage
from api_emulator.redfish.ethernetinterface import CreateEthernetInterface
from api_emulator.redfish.drive_api import create_drive
from api_emulator.redfish.volume_api import create_volume
from api_emulator.redfish.storage_controller_api import create_storage_controller
from api_emulator.redfish.storage_api import CreateStorage
from api_emulator.redfish.serial_interface_api import create_serial_interface
from api_emulator.redfish.network_adapter_api import create_network_adapter
from api_emulator.redfish.network_device_function_api import create_network_device_function
from api_emulator.redfish.fabric_adapter_api import create_fabric_adapter
from api_emulator.redfish.port_api import create_port
from api_emulator.redfish.graphics_controller_api import create_graphics_controller
from api_emulator.redfish.virtual_media_api import create_virtual_media
from api_emulator.redfish.pcie_device_api import create_pcie_device
from api_emulator.redfish.pcie_function_api import create_pcie_function
from api_emulator.redfish.cxl_logical_device_api import create_cxl_logical_device
from api_emulator.redfish.PowerSubsystem_api import CreatePowerSubsystem
from api_emulator.redfish.sensor_api import create_sensor
from api_emulator.redfish.network_interface_api import create_network_interface
from api_emulator.redfish.sessions_api import CreateSessionAccount
from api_emulator.redfish.manager_account_api import create_manager_account
from api_emulator.redfish.role_api import create_role_account
from api_emulator.redfish.fabric_api import create_fabric
from api_emulator.redfish.switch_api import create_switch

import g
import logging
import json
import os

from api_emulator.redfish.ResourceBlock_api import CreateResourceBlock
from api_emulator.redfish.ResourceZone_api import CreateResourceZone
from api_emulator.redfish.resourceobject import create_resource_object

TEST_DATA = 'test_device_parameter.json'


def _next_resource_block_id(rb_ids: dict, system=None):
    """Return resource block id
    The resource block ID of the CPU device is generated from the System ID.
    The resource block ID of the external device must be given a unique number.
    """
    if system:
        return system.replace('System', 'ComputeBlock')
    return f'DeviceBlock-{len(rb_ids) + 1}'


def _create_resource_block(rb_id: str, blocks: list, chassis: str,
                           zones: dict[str, list], system_id: str | None = None):
    """Create a resource block and the objects it manages."""
    rblk = CreateResourceBlock(resource_class_kwargs={'rb': g.rest_base})
    rblk.put(rb_id)
    rblk.post(g.rest_base, rb_id, 'linkChassis', chassis)
    zones['GlobalZone'].append(rb_id)
    rblk.post(g.rest_base, rb_id, 'linkZone', 'GlobalZone')
    for resource_name, resource_id in blocks:
        rblk.post(g.rest_base, rb_id, resource_name, resource_id)
        create_resource_object(resource_name, resource_id, chassis, rb_id)
    if system_id:
        rblk.post(g.rest_base, rb_id, 'linkSystem', system_id)
    return rb_id


# In Python 3, xrange() is not supported.  The usage in this file uses the
# Python 3 interpretation of range()
#   python 2 to python 3 equivalencies
#   xrange(10) -> range(10)
#   range(10)  -> list(range(10)
#
def create_resources(template, chassis, suffix, suffix_id):
    resource_ids={'Processors':[],'Memory':[],'SimpleStorage':[],'Storage':[],'EthernetInterfaces':[],'MetricDefinitions':[],'SerialInterface':[],'NetworkAdapter':[],'FabricAdapters':[],'GraphicsController':[],'VirtualMedia':[],'PCIeDevice':[],'Sensor':[]}
    proc_count=mem_count=dsk_count=eth_count=dri_count=vol_count=sctr_count=si_count=na_count=ndf_count=port_count=fa_count=gc_count=vm_count=pcle_count=sen_count=0
    for proc in template['Processors']:
        for k in range(proc.get('Count', 1)):
            proc_id=proc['Id'].format(proc_count)
            proc_count+=1
            resource_ids['Processors'].append(proc_id)
            create_processor(rb=g.rest_base, suffix=suffix, processor_id=proc_id,
                            suffix_id=suffix_id, chassis_id=chassis, totalcores=proc.get('TotalCores', 8),
                            maxspeedmhz=proc.get('MaxSpeedMHz', 2200),linkMemorys=resource_ids['Memory'],serialNumber='437XR1138R2')
    
    for mem in template['Memory']:
        memtype = mem.get('MemoryType', 'DRAM')
        opmodes = ['PMEM'] if 'NV' in memtype else ['Volatile']
        for k in range(mem.get('Count', 1)):
            mem_id=mem['Id'].format(mem_count)
            mem_count+=1
            resource_ids['Memory'].append(mem_id)
            create_memory(rb=g.rest_base, suffix=suffix, memory_id=mem_id,
                         suffix_id=suffix_id, chassis_id=chassis, capacitymb=mem.get('CapacityMiB', 8192),
                         type=memtype, operatingmodes=opmodes, linkProcessors=resource_ids['Processors'])
            create_chassis_memory(rb=g.rest_base, suffix=suffix, memory_id=mem_id,
                         suffix_id=suffix_id, chassis_id=chassis, capacitymb=mem.get('CapacityMiB', 8192),
                         type=memtype, operatingmodes=opmodes, linkProcessors=resource_ids['Processors'])

    for dsk in template['SimpleStorage']:
        for k in range(dsk.get('Count', 1)):
            dsk_id=dsk['Id'].format(dsk_count)
            dsk_count+=1
            resource_ids['SimpleStorage'].append(dsk_id)
            capacitygb = int(dsk['Devices'].get('CapacityBytes',
                                                512 * 1024 ** 3) / 1024 ** 3)
            drives = dsk['Devices'].get('Count', 1)
            CreateSimpleStorage(rb=g.rest_base, suffix=suffix, storage_id=dsk_id,
                                suffix_id=suffix_id, chassis_id=chassis, capacitygb=capacitygb,
                                drives=drives)

    for strg in template['Storage']:
        for k in range(strg.get('Count', 1)):
            dsk_id=strg['Id'].format(dsk_count)
            dsk_count+=1
            resource_ids['Storage'].append(dsk_id)
            capacitygb = int(strg['Devices'].get('CapacityBytes',
                                                512 * 1024 ** 3) / 1024 ** 3)

            driList = []
            volList = []
            sctrList = []
            for dri in strg['Drive']:
                for k in range(dri.get('Count', 1)):
                    dri_id=dri['Id'].format(dri_count)
                    dri_count+=1
                    create_drive(rb=g.rest_base, suffix='Chassis', storage_id=dsk_id, drive_id=dri_id,suffix_id=suffix_id, chassis_id=chassis)
                    driList.append(dri_id)

            for vol in strg['Volume']:
                for k in range(vol.get('Count', 1)):
                    vol_id=vol['Id'].format(vol_count)
                    vol_count+=1
                    create_volume(rb=g.rest_base, suffix=suffix, storage_id=dsk_id,volume_id=vol_id,suffix_id=suffix_id, chassis_id=chassis)
                    volList.append(vol_id)

            for scont in strg['Controllers']:
                for k in range(scont.get('Count', 1)):
                    sctr_id=scont['Id'].format(sctr_count)
                    sctr_count+=1
                    create_storage_controller(rb=g.rest_base, suffix=suffix, storage_id=dsk_id,strCtr_id=sctr_id,suffix_id=suffix_id, chassis_id=chassis)
                    sctrList.append(sctr_id)

            create_system_storage(rb=g.rest_base, suffix=suffix, storage_id=dsk_id,
                                suffix_id=suffix_id, chassis_id=chassis, capacitygb=capacitygb,driList=driList,volList=volList,sctrList=sctrList)


    for eth in template['EthernetInterfaces']:
        for k in range(eth.get('Count', 1)):
            eth_id=eth['Id'].format(eth_count)
            eth_count+=1
            resource_ids['EthernetInterfaces'].append(eth_id)
            CreateEthernetInterface(rb=g.rest_base, suffix=suffix, nic_id=eth_id,
                                    suffix_id=suffix_id, chassis_id=chassis,
                                    speedmbps=eth.get('SpeedMbps', 1000))

    for na in template['NetworkAdapter']:
        for k in range(na.get('Count', 1)):

            ndfList = []
            portNAList= []
            portFAList = []

            na_id=na['Id'].format(na_count)
            na_count+=1
            resource_ids['NetworkAdapter'].append(na_id)          

            for ndf in na['NetworkDeviceFunction']:
                for k in range(ndf.get('Count', 1)):
                    ndf_id=ndf['Id'].format(ndf_count)
                    ndf_count+=1
                    create_network_device_function(rb=g.rest_base, suffix=suffix, na_id=na_id,ndf_id=ndf_id,suffix_id=suffix_id, chassis_id=chassis)
                    ndfList.append(ndf_id)

            for port in na['Ports']:
                for k in range(port.get('Count', 1)):
                    port_id=port['Id'].format(port_count)
                    port_count+=1
                    create_port(rb=g.rest_base, suffix=suffix, adapter='NetworkAdapter',adapter_id=na_id,port_id=port_id,suffix_id=suffix_id, chassis_id=chassis)
                    portNAList.append(port_id)

            create_network_adapter(rb=g.rest_base, suffix=suffix, na_id=na_id,
                                    suffix_id=suffix_id, chassis_id=chassis, ndfList=ndfList,portNAList=portNAList)

    for fa in template['FabricAdapters']:
        for k in range(fa.get('Count', 1)):
            fa_id=fa['Id'].format(fa_count)
            fa_count+=1
            resource_ids['FabricAdapters'].append(fa_id)
            

            for port in fa['Ports']:
                for k in range(port.get('Count', 1)):
                    port_id=port['Id'].format(port_count)
                    port_count+=1
                    create_port(rb=g.rest_base, suffix=suffix,adapter='FabricAdapters', adapter_id=fa_id,port_id=port_id,suffix_id=suffix_id, chassis_id=chassis)
                    portFAList.append(port_id)

            create_fabric_adapter(rb=g.rest_base, suffix=suffix, fa_id=fa_id,
                                    suffix_id=suffix_id, chassis_id=chassis,portFAList=portFAList)

    for gc in template['GraphicsController']:
        for k in range(gc.get('Count', 1)):
            gc_id=gc['Id'].format(gc_count)
            gc_count+=1
            resource_ids['GraphicsController'].append(gc_id)
            create_graphics_gontroller(rb=g.rest_base, suffix=suffix, gc_id=gc_id,
                                    suffix_id=suffix_id, chassis_id=chassis)

    for vm in template['VirtualMedia']:
        for k in range(vm.get('Count', 1)):
            vm_id=vm['Id'].format(vm_count)
            vm_count+=1
            resource_ids['VirtualMedia'].append(vm_id)
            create_virtualmedia(rb=g.rest_base, suffix=suffix, vm_id=vm_id,
                                    suffix_id=suffix_id, chassis_id=chassis)

    for pcle in template['PCIeDevice']:
        for k in range(pcle.get('Count', 1)):
            pcie_id=pcle['Id'].format(pcle_count)
            pcle_count+=1
            resource_ids['PCIeDevice'].append(pcie_id)
            create_pcie_device(rb=g.rest_base, suffix=suffix, pcie_id=pcie_id,
                                    suffix_id=suffix_id, chassis_id=chassis)

    for sen in template['Sensor']:
        for k in range(sen.get('Count', 1)):
            sen_id=sen['Id'].format(sen_count)
            sen_count+=1
            resource_ids['Sensor'].append(sen_id)
            create_sensor(rb=g.rest_base, suffix=suffix, sen_id=sen_id,
                                    suffix_id=suffix_id, chassis_id=chassis)


    return resource_ids

def populate(cfg):
    #cfg = 10
    if type(cfg) is int:
        return n_populate(cfg)
    cs_count = 0
    rb_count = 0
    chassis_count = 0
    zones = {}
    metricDef_template = {}
    metricRepDef_template = {}
    for chassi_template in cfg['Chassis']:
        for i in range(chassi_template.get('Count', 1)):
            chassis_count += 1
            chassis = chassi_template['Id'].format(chassis_count)
            bmc = 'BMC-{}'.format(chassis_count)
            sys_ids = []
            rb_ids = []

            for compsys_template in chassi_template['Links'].get('ComputerSystems',[]):
                for j in range(compsys_template.get('Count', 1)):
                    cs_count += 1
                    compSys = compsys_template['Id'].format(cs_count)
                    sys_ids.append(compSys)
                    CreateComputerSystem(
                        resource_class_kwargs={'rb': g.rest_base, 'linkChassis': [chassis], 'linkStorage': bmc, 'linkMgr': bmc}).put(
                        compSys)
                    create_resources(compsys_template, chassis, 'Systems', compSys)

            for rb_template in chassi_template['Links'].get('ResourceBlocks',[]):
                for j in range(rb_template.get('Count', 1)):
                    rb_count += 1
                    rb_id = rb_template['Id'].format(rb_count)
                    rb_ids.append(rb_id)
                    rb_zones = rb_template['ResourceZones']
                    for zone in rb_zones:
                        if zone not in zones:
                            zones[zone]=[]
                        zones[zone].append(rb_id)
                    rb=CreateResourceBlock(resource_class_kwargs={'rb': g.rest_base})
                    rb.put(rb_id)
                    rb.post(g.rest_base,rb_id,'linkChassis',chassis)
                    [rb.post(g.rest_base,rb_id,'linkZone',x) for x in rb_zones]
                    resource_ids=create_resources(rb_template, chassis, 'CompositionService/ResourceBlocks', rb_id)
                    for resource_name in resource_ids:
                        for resource_id in resource_ids[resource_name]:
                            rb.post(g.rest_base,rb_id,resource_name,resource_id)

            CreateChassis(resource_class_kwargs={
                'rb': g.rest_base, 'linkSystem': sys_ids, 'linkResourceBlocks':rb_ids, 'linkStorage': bmc, 'linkMgr': bmc}).put(chassis)
            CreatePower(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
            CreateThermal(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
            CreateManager(resource_class_kwargs={
                'rb': g.rest_base, 'linkSystem': sys_ids, 'linkChassis': chassis, 'linkInChassis': chassis}).put(bmc)
            CreatePowerSubsystem(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis, 'chassis_count':chassis_count}).put(chassis,chassis_count)

    for zone in zones:
        z=CreateResourceZone(resource_class_kwargs={'rb': g.rest_base})
        z.put(zone)
        [z.post(g.rest_base,zone,'ResourceBlocks',x) for x in zones[zone]]

    for metricDef_template in cfg['MetricDefinitions']:
        metricDef = metricDef_template['Id'].format(0)
        CreateMetricDefinitions(resource_class_kwargs={'rb': g.rest_base, 'ChassisID':'Chassis-1','id': metricDef}).put(metricDef)

    for metricRepDef_template in cfg['MetricReportDefinitions']:
        metricRepDef = metricRepDef_template['Id'].format(0)
        CreateMetricReportDefinitions(resource_class_kwargs = metricRepDef_template).put(metricRepDef)
        

def d_populate(cfg, power_link):

    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path += os.sep + TEST_DATA

    if os.path.isfile(file_path):
        with open(file_path, encoding="utf-8") as open_file:
            parameter = json.load(open_file)

    resource = []
    resource_ids = {'Processors': [], 'Memory': [], 'SimpleStorage': [], 'Storage': [], 'NetworkInterfaces': [], 'NetworkDeviceFunctions': [], 'FabricAdapter': [],
                    'EthernetInterfaces': [], 'PCIeDevice': [], 'GraphicControllers': []}
    chassis_count = proc_count = gc_count = 0

    rb_ids = []
    create_dev_ids = []

    sys_ids = []
    proc_ids = []
    dri_ids = []

    CreateSessionAccount(rb=g.rest_base, user_name="user", password="pass")
    create_manager_account(rb=g.rest_base, user_name="user", password="pass")
    create_role_account(rb=g.rest_base)

    chassis_count += 1
    bmc = 'BMC-{}'.format(chassis_count)
    chassis = 'Chassis-{0}'.format(chassis_count)
    zones = {'GlobalZone': []}

    if 'cpu' in cfg:
        resource.append('Processors')
        for cpu_template in cfg['cpu']:
            proc_count += 1
            compSys = 'System-{0}'.format(proc_count)
            sys_ids.append(compSys)

            processor_id = cpu_template.get('deviceID')
            proc_id = 'PROC-{0}'.format(processor_id)
            resource_ids['Processors'].append(proc_id)
            rb_id = _next_resource_block_id(rb_ids, compSys)
            rb_idevs = [('Processors', proc_id)]

            if power_link:
                reset_action = "invalid"
            else:
                reset_action = None

            for indevice in cpu_template.get('link'):
                indevice_id = indevice.get('deviceID')

                if indevice_id.startswith("10"):
                    if 'memory' in cfg:
                        resource.append('Memory')
                        for memory_template in cfg['memory']:
                            if memory_template.get('deviceID') == indevice_id:
                                mem_id = 'MEM-{0}'.format(indevice_id)
                                mem_sereal = indevice_id
                                resource_ids['Memory'].append(mem_id)

                                pcie_id = 'PCIe-{0}'.format(indevice_id)
                                pcie_f_id = 'PCIeF-{0}'.format(indevice_id)
                                resource_ids['PCIeDevice'].append(pcie_id)
                                
                                mem_sensor_id = 'SENS-MEM-{0}'.format(indevice_id)

                                mem_model = memory_template.get('model')
                                if indevice_id in parameter:
                                    dev_param = parameter[indevice_id]
                                else:
                                    dev_param['capacityMiB'] = 4096
                                    dev_param['operatingSpeedMHz'] = 3200
                                    dev_param['state'] = "Enabled"
                                    dev_param['health'] = "OK"
                                    dev_param['sensingInterval'] = "PT3S"

                                create_chassis_memory(rb=g.rest_base, suffix='Systems', memory_id=mem_id, sensor_id=mem_sensor_id, dev_param=dev_param,
                                                    suffix_id=compSys, chassis_id=chassis, linkProcessors=[proc_id], mem_sereal=mem_sereal, model=mem_model, reset_action=reset_action)
                                create_chassis_memory(rb=g.rest_base, suffix='Chassis', memory_id=mem_id, sensor_id=mem_sensor_id, dev_param=dev_param,
                                                    suffix_id=chassis, chassis_id=chassis, linkProcessors=[proc_id], mem_sereal=mem_sereal, model=mem_model, reset_action=reset_action)
                                rb_idevs.append(('Memory', mem_id))
                                create_dev_ids.append(indevice_id)

                if indevice_id.startswith("20"):
                    if 'storage' in cfg:
                        resource.append('Drive')
                        for storage_template in cfg['storage']:
                            if indevice_id == storage_template.get('deviceID'):
                                str_id = 'STR-{0}'.format(indevice_id)
                                dri_id = 'DRI-{0}'.format(indevice_id)
                                volume_id = 'VOL-{0}'.format(indevice_id)
                                strCtr_id = 'STRCTR-{0}'.format(indevice_id)
                                dri_sensor_id = 'SENS-DRI-{0}'.format(indevice_id)
                                stoc_sensor_id = 'SENS-STOC-{0}'.format(indevice_id)
                                dri_sereal = indevice_id

                                resource_ids['Storage'].append(str_id)

                                pcie_id = 'PCIe-{0}'.format(indevice_id)
                                pcie_f_id = 'PCIeF-{0}'.format(indevice_id)
                                cxl_id = 'CXL-{0}'.format(indevice_id)
                                port_id = 'PORT-{0}'.format(indevice_id)
                                resource_ids['PCIeDevice'].append(pcie_id)

                                dri_model = storage_template.get('model')

                                if indevice_id in parameter:
                                    dev_param = parameter[indevice_id]
                                else:
                                    dev_param['volumeCapacityBytes'] = 4096
                                    dev_param['driveCapableSpeedGbs'] = 3200
                                    dev_param['driveCapacityBytes'] = 4096
                                    dev_param['state'] = "Enabled"
                                    dev_param['health'] = "OK"
                                    dev_param['sensingInterval'] = "PT3S"

                                driList = []
                                volList = []
                                sctrList = []
                                driList.append(dri_id)
                                volList.append(volume_id)
                                sctrList.append(strCtr_id)
                                dri_ids.append(dri_id)

                                create_drive(rb=g.rest_base, suffix='Systems', storage_id=str_id, drive_id=dri_id, dri_sereal=dri_sereal, suffix_id=compSys, sensor_id=dri_sensor_id, pcie_f_id=pcie_f_id, pcie_id=pcie_id,
                                            volume_id=volume_id, capacitygb=storage_template.get('size', 8192), model=dri_model, chassis_id=chassis, dev_param=dev_param, reset_action=reset_action)
                                create_drive(rb=g.rest_base, suffix='Chassis', storage_id=str_id, drive_id=dri_id,dri_sereal=dri_sereal,suffix_id=chassis,sensor_id = dri_sensor_id,volume_id=volume_id,
                                            capacitygb=storage_template.get('size', 8192),model=dri_model,pcie_f_id=pcie_f_id,pcie_id=pcie_id,chassis_id=chassis,dev_param=dev_param, reset_action=reset_action)
                                create_volume(rb=g.rest_base, suffix='Systems', storage_id=str_id, volume_id=volume_id, suffix_id=compSys, chassis_id=chassis, drive_id=dri_id, dri_sereal=dri_sereal,
                                             capacitygb=dev_param['volumeCapacityBytes'], spec={'CapableSpeedGbs': dev_param['driveCapableSpeedGbs']})
                                create_storage_controller(rb=g.rest_base, suffix='Systems', storage_id=str_id, strCtr_id=strCtr_id, suffix_id=compSys, chassis_id=chassis, sensor_id=stoc_sensor_id, interval=dev_param['sensingInterval'])
                                create_system_storage(rb=g.rest_base, suffix='Systems', storage_id=str_id,
                                                    suffix_id=compSys, chassis_id=chassis, capacitygb=storage_template.get('size', 8192), driList=driList, volList=volList, sctrList=sctrList)
                                create_pcie_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, pcie_f_id=pcie_f_id,
                                                 SerialNumber=storage_template.get('PCIeDeviceSerialNumber'), suffix_id=compSys, chassis_id=chassis)
                                create_pcie_function(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, pcie_f_id=pcie_f_id,
                                                   pcie_d_id=storage_template.get('PCIeDeviceID'), pcie_v_id=storage_template.get('PCIeVendorID'), suffix_id=compSys, chassis_id=chassis)
                                create_cxl_logical_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, cxl_id=cxl_id, suffix_id=compSys, chassis_id=chassis)
                                create_port(suffix='Systems', adapter='Controllers', adapter_id=strCtr_id, storage_id=str_id, port_id=port_id, suffix_id=compSys, chassis_id=chassis)
                                rb_idevs.append(('Drives', dri_id))
                                create_dev_ids.append(indevice_id)

                if indevice_id.startswith("30"):
                    if 'networkInterface' in cfg:
                        resource.append('NetworkAdapter')
                        for nic_template in cfg['networkInterface']:
                            if indevice_id == nic_template.get('deviceID'):
                                ndfList = []
                                portNAList = []
                                ni_id = 'NETI-{0}'.format(indevice_id)
                                nic_id = 'NIC-{0}'.format(indevice_id)
                                port_id = 'PORT-{0}'.format(indevice_id)
                                ndf_id = 'NICF-{0}'.format(indevice_id)
                                nic_sensor_id = 'SENS-NIC-{0}'.format(indevice_id)
                                si_id = "SI-{0}".format(indevice_id)
                                ei_id = 'EI-{0}'.format(indevice_id)
                                neta_sereal = indevice_id

                                resource_ids['NetworkInterfaces'].append(nic_id)
                                resource_ids['NetworkDeviceFunctions'].append({"nic": nic_id, "ndf": ndf_id})

                                pcie_id = 'PCIe-{0}'.format(indevice_id)
                                pcie_f_id = 'PCIeF-{0}'.format(indevice_id)
                                cxl_id = 'CXL-{0}'.format(indevice_id)
                                resource_ids['PCIeDevice'].append(pcie_id)

                                nic_model = nic_template.get('model')

                                if indevice_id in parameter:
                                    dev_param = parameter[indevice_id]
                                else:
                                    dev_param['bitRate'] = 12000
                                    dev_param['state'] = "Enabled"
                                    dev_param['health'] = "OK"
                                    dev_param['sensingInterval'] = "PT3S"

                                create_network_interface(rb=g.rest_base, suffix='Systems', ni_id=ni_id, na_id=nic_id, suffix_id=compSys, chassis_id=chassis)
                                create_port(rb=g.rest_base, suffix='Chassis', adapter='NetworkAdapters', adapter_id=nic_id, port_id=port_id, suffix_id=chassis, chassis_id=chassis, dev_param=dev_param)
                                portNAList.append(port_id)
                                create_network_device_function(rb=g.rest_base, suffix='Chassis', na_id=nic_id, ndf_id=ndf_id, suffix_id=compSys, chassis_id=chassis, portNAList=portNAList, pcie_f_id=pcie_f_id, mac=nic_template.get('mac'))
                                ndfList.append(ndf_id)
                                create_network_adapter(rb=g.rest_base, suffix='Chassis', na_id=nic_id, neta_sereal=neta_sereal, sensor_id=nic_sensor_id, dev_param=dev_param, pcie_id=pcie_id,
                                                     suffix_id=compSys, chassis_id=chassis, ndfList=ndfList, portNAList=portNAList, model=nic_model, reset_action=reset_action)
                                create_pcie_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, pcie_f_id=pcie_f_id, SerialNumber=nic_template.get('PCIeDeviceSerialNumber'), suffix_id=compSys, chassis_id=chassis)
                                create_pcie_function(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, pcie_f_id=pcie_f_id,
                                                   pcie_d_id=nic_template.get('PCIeDeviceID'), pcie_v_id=nic_template.get('PCIeVendorID'), suffix_id=compSys, chassis_id=chassis)
                                create_cxl_logical_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, cxl_id=cxl_id, suffix_id=compSys, chassis_id=chassis)
                                create_dev_ids.append(indevice_id)
                                CreateEthernetInterface(rb=g.rest_base, suffix='Chassis', nic_id=nic_id, ndf_id=ndf_id, ei_id=ei_id, schema_id=compSys,
                                                        suffix_id=compSys, chassis_id=chassis, ndfList=ndfList, portNAList=portNAList, speedmbps=1000, mac=nic_template.get('mac'))
                                rb_idevs.append(('EthernetInterfaces', ei_id))

                if indevice_id.startswith("50"):
                    if 'gpu' in cfg:
                        resource.append('Processors')
                        for gpu_template in cfg['gpu']:
                            if indevice_id == gpu_template.get('deviceID'):
                                pro_id = 'PROC-{0}'.format(indevice_id)
                                gpu_sensor_id = 'SENS-PROC-{0}'.format(indevice_id)
                                gpu_sereal = indevice_id

                                resource_ids['Processors'].append(pro_id)

                                pcie_id = 'PCIe-{0}'.format(indevice_id)
                                pcie_f_id = 'PCIeF-{0}'.format(indevice_id)
                                cxl_id = 'CXL-{0}'.format(indevice_id)
                                port_id = 'PORT-{0}'.format(indevice_id)
                                resource_ids['PCIeDevice'].append(pcie_id)

                                model = gpu_template.get('model')
                                if indevice_id in parameter:
                                    dev_param = parameter[indevice_id]
                                else:
                                    dev_param['manufacturer'] = "Intel(R) Corporation"
                                    dev_param['state'] = "Enabled"
                                    dev_param['health'] = "OK"
                                    dev_param['sensingInterval'] = "PT3S"
                
                                create_processor(rb=g.rest_base, suffix='Systems', sys_id=compSys, processor_id=pro_id, sensor_id=gpu_sensor_id, gpu_sereal=gpu_sereal, pcie_id=pcie_id, port_id=port_id,
                                                suffix_id=compSys, chassis_id=chassis, model=model, dev_param=dev_param, manufacturer=dev_param['manufacturer'], processorType='GPU', reset_action=reset_action)
                                create_processor(rb=g.rest_base, suffix='Chassis', suffix_id=chassis, sys_id=compSys, processor_id=pro_id, sensor_id=gpu_sensor_id, gpu_sereal=gpu_sereal, pcie_id=pcie_id,
                                                chassis_id=chassis, model=model, dev_param=dev_param, manufacturer=dev_param['manufacturer'], processorType='GPU', reset_action=reset_action)
                                create_pcie_device(rb=g.rest_base, suffix='Systems', suffix_id=compSys, pcie_id=pcie_id, pcie_f_id=pcie_f_id, SerialNumber=gpu_template.get('PCIeDeviceSerialNumber'), chassis_id=chassis)
                                create_pcie_function(rb=g.rest_base, suffix='Systems', suffix_id=compSys, pcie_id=pcie_id, pcie_f_id=pcie_f_id,
                                                   pcie_d_id=gpu_template.get('PCIeDeviceID'), pcie_v_id=gpu_template.get('PCIeVendorID'), chassis_id=chassis)
                                create_cxl_logical_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, cxl_id=cxl_id, suffix_id=compSys, chassis_id=chassis)
                                rb_idevs.append(('Processors', pro_id))
                                create_dev_ids.append(indevice_id)

                if indevice_id.startswith("60"):
                    if 'graphicController' in cfg:
                        resource.append('GraphicControllers')
                        for graph_template in cfg['graphicController']:
                            if indevice_id == graph_template.get('deviceID'):

                                gc_id = 'GC-{0}'.format(indevice_id)
                                gc_sereal = indevice_id
                                resource_ids['GraphicControllers'].append(gc_id)

                                model = graph_template.get('model')
                                if indevice_id in parameter:
                                    dev_param = parameter[indevice_id]
                                else:
                                    dev_param['state'] = "Enabled"
                                    dev_param['health'] = "OK"
                                create_graphics_controller(rb=g.rest_base, suffix='Systems', gc_id=gc_id, gc_sereal=gc_sereal,
                                        suffix_id=compSys, chassis_id=chassis, model=model, dev_param=dev_param)
                                create_dev_ids.append(indevice_id)
        
            pcie_id = 'PCIe-{0}'.format(processor_id)
            pcie_f_id = 'PCIeF-{0}'.format(processor_id)
            cxl_id = 'CXL-{0}'.format(processor_id)
            port_id = 'PORT-{0}'.format(processor_id)
            resource_ids['PCIeDevice'].append(pcie_id)
            proc_sensor_id = 'SENS-PROC-{0}'.format(processor_id)
            model = cpu_template.get('model')
            manufacturer = cpu_template.get('manufacturer')
            if processor_id in parameter:
                dev_param = parameter[processor_id]
            else:
                dev_param[processor_id]['totalEnabledCores'] = 4
                dev_param[processor_id]['operatingSpeedMHz'] = 3200

            rb_ids.append(_create_resource_block(rb_id, rb_idevs, chassis, zones, compSys))

            proc_ids.append(proc_id)
            create_processor(rb=g.rest_base, suffix='Systems', processor_id=proc_id, sensor_id=proc_sensor_id, dev_param=dev_param, power_link=power_link, port_id=port_id,
                            suffix_id=compSys, sys_id=compSys, chassis_id=chassis, linkProcs=resource_ids['Processors'], linkMemorys=resource_ids['Memory'], linkNicDfuncs=resource_ids['NetworkDeviceFunctions'],
                            linkFabrics=resource_ids['FabricAdapter'], pcie_id=pcie_id, model=model, manufacturer=manufacturer, serialNumber=cpu_template.get('serialNumber', 8), processorType='CPU')
            create_processor(rb=g.rest_base, suffix='Chassis', processor_id=proc_id, sensor_id=proc_sensor_id, dev_param=dev_param, power_link=power_link, port_id=port_id,
                            suffix_id=chassis, sys_id=compSys, chassis_id=chassis, linkProcs=resource_ids['Processors'], linkMemorys=resource_ids['Memory'], linkNicDfuncs=resource_ids['NetworkDeviceFunctions'],
                            linkFabrics=resource_ids['FabricAdapter'], pcie_id=pcie_id, model=model, manufacturer=manufacturer, serialNumber=cpu_template.get('serialNumber', 8), processorType='CPU')
            create_pcie_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, pcie_f_id=pcie_f_id, suffix_id=compSys, chassis_id=chassis)
            create_pcie_function(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, pcie_f_id=pcie_f_id, suffix_id=compSys, chassis_id=chassis)
            create_cxl_logical_device(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id, cxl_id=cxl_id, suffix_id=compSys, chassis_id=chassis)
            create_port(suffix='Systems', adapter='Processors', adapter_id=proc_id, port_id=port_id, suffix_id=compSys, chassis_id=chassis)

            CreateComputerSystem(resource_class_kwargs={
                'rb': g.rest_base, 'linkChassis': [chassis], 'linkStorage': bmc, 'linkMgr': bmc, 'linkResource': resource_ids, 'BlockId': rb_id}).put(compSys)
            vm_id = 'VM-{0}'.format(proc_count)
            create_virtual_media(rb=g.rest_base, suffix='Systems', suffix_id=compSys, vm_id=vm_id)

            resource_ids['Processors'].clear()
            resource_ids['Memory'].clear()
            resource_ids['Storage'].clear()
            resource_ids['NetworkInterfaces'].clear()
            resource_ids['NetworkDeviceFunctions'].clear()
            resource_ids['FabricAdapter'].clear()
            resource_ids['GraphicControllers'].clear()
            resource_ids['PCIeDevice'].clear()

    if 'memory' in cfg:
        resource.append('Memory')
        for memory_template in cfg['memory']:
            memory_id = memory_template.get('deviceID')
            if memory_id not in create_dev_ids:
                mem_id = 'MEM-{0}'.format(memory_id)
                mem_sereal = memory_id
                pcie_id = 'PCIe-{0}'.format(memory_id)
                pcie_f_id = 'PCIeF-{0}'.format(memory_id)
                cxl_id = 'CXL-{0}'.format(memory_id)
                mem_sensor_id = 'SENS-MEM-{0}'.format(memory_id)
                mem_model = memory_template.get('model')
                if memory_id in parameter:
                    dev_param = parameter[memory_id]
                else:
                    dev_param['capacityMiB'] = 4096
                    dev_param['operatingSpeedMHz'] = 3200
                    dev_param['state'] = "Enabled"
                    dev_param['health'] = "OK"
                    dev_param['sensingInterval'] = "PT3S"
            
                if not memory_id.startswith("10"):
                    rb_id = _next_resource_block_id(rb_ids)
                    rb_ids.append(_create_resource_block(rb_id, [('Memory', mem_id)], chassis, zones))
                create_chassis_memory(rb=g.rest_base, suffix='Chassis', memory_id=mem_id,sensor_id = mem_sensor_id,dev_param=dev_param,
                     suffix_id=chassis, chassis_id=chassis, linkProcessors=None,pcie_id=pcie_id,mem_sereal=mem_sereal,model=mem_model)
                create_pcie_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,pcie_f_id=pcie_f_id,suffix_id=chassis, chassis_id=chassis)
                create_pcie_function(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,pcie_f_id=pcie_f_id,suffix_id=chassis, chassis_id=chassis)
                create_cxl_logical_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,cxl_id=cxl_id,suffix_id=chassis, chassis_id=chassis)
                create_dev_ids.append(memory_id)	

    if 'storage' in cfg:
        resource.append('Drive')
        for storage_template in cfg['storage']:
            storage_id = storage_template.get('deviceID')
            if storage_id not in create_dev_ids:
                str_id = 'STR-{0}'.format(storage_id)
                dri_id = 'DRI-{0}'.format(storage_id)
                volume_id = 'VOL-{0}'.format(storage_id)
                strCtr_id = 'STRCTR-{0}'.format(storage_id)
                pcie_id = 'PCIe-{0}'.format(storage_id)
                pcie_f_id = 'PCIeF-{0}'.format(storage_id)
                cxl_id = 'CXL-{0}'.format(storage_id)
                dri_sensor_id = 'SENS-DRI-{0}'.format(storage_id)
                stoc_sensor_id = 'SENS-STOC-{0}'.format(storage_id)
                port_id = 'PORT-{0}'.format(storage_id)
                dri_model = storage_template.get('model')
                dri_sereal = storage_id

                if storage_id in parameter:
                    dev_param = parameter[storage_id]
                else:
                    dev_param['volumeCapacityBytes'] = 4096
                    dev_param['driveCapableSpeedGbs'] = 3200
                    dev_param['driveCapacityBytes'] = 4096
                    dev_param['state'] = "Enabled"
                    dev_param['health'] = "OK"
                    dev_param['sensingInterval'] = "PT3S"
                driList = []
                volList = []
                sctrList = []
                driList.append(dri_id)
                volList.append(volume_id)
                sctrList.append(strCtr_id)
                dri_ids.append(dri_id)

                if not storage_id.startswith("20"):
                    rb_id = _next_resource_block_id(rb_ids)
                    rb_ids.append(_create_resource_block(rb_id, [('Drives', dri_id)], chassis, zones))
                create_drive(rb=g.rest_base, suffix='Chassis', storage_id=str_id, drive_id=dri_id,dri_sereal=dri_sereal,suffix_id=chassis,sensor_id = dri_sensor_id,volume_id=volume_id,
                            capacitygb=storage_template.get('size', 8192),model=dri_model,pcie_f_id=pcie_f_id,pcie_id=pcie_id,chassis_id=chassis,dev_param=dev_param)
                create_volume(rb=g.rest_base, suffix='Chassis', storage_id=str_id,volume_id=volume_id,suffix_id=chassis, chassis_id=chassis,drive_id=dri_id, dri_sereal=dri_sereal,capacitygb=dev_param['volumeCapacityBytes'], spec={'CapableSpeedGbs':dev_param['driveCapableSpeedGbs']})
                create_storage_controller(rb=g.rest_base, suffix='Chassis', storage_id=str_id,strCtr_id=strCtr_id,suffix_id=chassis, chassis_id=chassis,sensor_id = stoc_sensor_id,interval=dev_param['sensingInterval'])
                url = g.rest_base +'Storage/' + str_id
                CreateStorage(resource_class_kwargs={'rb': g.rest_base,'url':url, 'chassis_id':chassis, 'id': str_id, 'sctrList':sctrList, 'volList':volList, 'driList':driList}).put(str_id)
                create_pcie_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,pcie_f_id=pcie_f_id,
                            SerialNumber=storage_template.get('PCIeDeviceSerialNumber'),suffix_id=chassis, chassis_id=chassis)
                create_pcie_function(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,pcie_f_id=pcie_f_id,
                            pcie_d_id = storage_template.get('PCIeDeviceID'),pcie_v_id = storage_template.get('PCIeVendorID'),suffix_id=chassis, chassis_id=chassis)
                create_cxl_logical_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,cxl_id=cxl_id,suffix_id=chassis, chassis_id=chassis)
                create_port(suffix='Storage', adapter='Controllers',adapter_id=strCtr_id,storage_id=str_id, port_id=port_id,suffix_id=str_id, chassis_id=chassis)

    if 'networkInterface' in cfg:
        resource.append('NetworkAdapter')
        for nic_template in cfg['networkInterface']:
            ndfList = []
            portNAList= []

            network_id = nic_template.get('deviceID')
            if network_id not in create_dev_ids:
                nic_id = 'NIC-{0}'.format(network_id)
                port_id= 'PORT-{0}'.format(network_id)
                ndf_id= 'NICF-{0}'.format(network_id)
                pcie_id='PCIe-{0}'.format(network_id)
                pcie_f_id = 'PCIeF-{0}'.format(network_id)
                cxl_id = 'CXL-{0}'.format(network_id)
                nic_sensor_id =  'SENS-NIC-{0}'.format(network_id)
                si_id = 'SI-{0}'.format(network_id)
                ei_id = 'EI-{0}'.format(network_id)
                nic_model = nic_template.get('model')
                neta_sereal = network_id

                if network_id in parameter:
                    dev_param = parameter[network_id]
                else:
                    dev_param['bitRate'] = 12000
                    dev_param['state'] = "Enabled"
                    dev_param['health'] = "OK"
                    dev_param['sensingInterval'] = "PT3S"

                create_port(rb=g.rest_base, suffix='Chassis', adapter='NetworkAdapters',adapter_id=nic_id,neta_sereal=neta_sereal,port_id=port_id,suffix_id=chassis, chassis_id=chassis, dev_param=dev_param)
                portNAList.append(port_id)
                create_network_device_function(rb=g.rest_base, suffix='Chassis', na_id=nic_id,ndf_id=ndf_id,suffix_id=chassis, chassis_id=chassis,portNAList=portNAList,pcie_f_id=pcie_f_id,mac=nic_template.get('mac'))
                ndfList.append(ndf_id)
                create_network_adapter(rb=g.rest_base, suffix='Chassis', na_id=nic_id,sensor_id = nic_sensor_id,neta_sereal=neta_sereal,
                                    suffix_id=chassis, chassis_id=chassis,pcie_id=pcie_id, ndfList=ndfList,portNAList=portNAList,model=nic_model, dev_param=dev_param)
                create_pcie_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,pcie_f_id=pcie_f_id,SerialNumber=nic_template.get('PCIeDeviceSerialNumber'),suffix_id=chassis, chassis_id=chassis)
                create_pcie_function(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,pcie_f_id=pcie_f_id,
                        pcie_d_id = nic_template.get('PCIeDeviceID'),pcie_v_id = nic_template.get('PCIeVendorID'),suffix_id=chassis, chassis_id=chassis)
                create_cxl_logical_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,cxl_id=cxl_id,suffix_id=chassis, chassis_id=chassis)
                CreateEthernetInterface(rb=g.rest_base, suffix='Chassis', nic_id=nic_id,ndf_id=ndf_id,ei_id=ei_id,schema_id=ndf_id,
                                    suffix_id=None, chassis_id=chassis, ndfList=ndfList,portNAList=portNAList,
                                    speedmbps=1000, mac=nic_template.get('mac'))
                if not network_id.startswith("30"):
                    rb_id = _next_resource_block_id(rb_ids)
                    rb_ids.append(_create_resource_block(rb_id, [('EthernetInterfaces', ei_id)], chassis, zones))

    if 'gpu' in cfg:
        resource.append('Processors')
        for gpu_template in cfg['gpu']:
            gpu_id = gpu_template.get('deviceID')
            if gpu_id not in create_dev_ids:

                pro_id='PROC-{0}'.format(gpu_id)
                gpu_sensor_id =  'SENS-PROC-{0}'.format(gpu_id)

                pcie_id='PCIe-{0}'.format(gpu_id)
                pcie_f_id = 'PCIeF-{0}'.format(gpu_id)
                cxl_id = 'CXL-{0}'.format(gpu_id)
                gpu_sereal = gpu_id

                model = gpu_template.get('model')
                if gpu_id in parameter:
                    dev_param = parameter[gpu_id]
                else:
                    dev_param['manufacturer'] = "Intel(R) Corporation"
                    dev_param['state'] = "Enabled"
                    dev_param['health'] = "OK"
                    dev_param['sensingInterval'] = "PT3S"
                
                if not gpu_id.startswith("50"):
                    rb_id = _next_resource_block_id(rb_ids)
                    rb_ids.append(_create_resource_block(rb_id, [('Processors', pro_id)], chassis, zones))
                create_processor(rb=g.rest_base, suffix='Chassis', suffix_id=chassis,sys_id = None,processor_id=pro_id,sensor_id = gpu_sensor_id,gpu_sereal=gpu_sereal,
                            chassis_id=chassis,pcie_id=pcie_id,model=model,dev_param=dev_param,manufacturer=dev_param['manufacturer'],processorType='GPU')
                create_pcie_device(rb=g.rest_base,suffix='Chassis', suffix_id=chassis, pcie_id=pcie_id,pcie_f_id=pcie_f_id,SerialNumber=gpu_template.get('PCIeDeviceSerialNumber'),
                    chassis_id=chassis)
                create_pcie_function(rb=g.rest_base, suffix='Chassis', suffix_id=chassis,pcie_id=pcie_id,pcie_f_id=pcie_f_id,
                      pcie_d_id = gpu_template.get('PCIeDeviceID'),pcie_v_id = gpu_template.get('PCIeVendorID'), chassis_id=chassis)
                create_cxl_logical_device(rb=g.rest_base, suffix='Chassis', pcie_id=pcie_id,cxl_id=cxl_id,suffix_id=chassis, chassis_id=chassis)

    if 'graphicController' in cfg:
        resource.append('GraphicControllers')
        for graph_template in cfg['graphicController']:
            graph_id = graph_template.get('deviceID')
            if graph_id not in create_dev_ids:
                gc_id='GC-{0}'.format(graph_id)
                gc_sereal = graph_id
                gc_count += 1
                compSys = 'System-{0}'.format(gc_count)
                sys_ids.append(compSys)
                resource_ids_2 = {'GraphicControllers':[]}
                resource_ids_2['GraphicControllers'].append(gc_id)

                model =  graph_template.get('model')
                if graph_id in parameter:
                    dev_param = parameter[graph_id]
                else:
                    dev_param['state'] = "Enabled"
                    dev_param['health'] = "OK"
                create_graphics_controller(rb=g.rest_base, suffix='Systems', gc_id=gc_id,gc_sereal=gc_sereal,dev_param=dev_param,
                                        suffix_id=compSys, chassis_id=chassis,model=model)
                CreateComputerSystem(resource_class_kwargs={
                'rb': g.rest_base, 'linkChassis': [chassis], 'linkStorage': bmc, 'linkMgr': bmc, 'linkResource': resource_ids_2}).put(compSys)

    fab_port_id = 'PORT-FABRIC'
    fa_id = 'FABRIC'
    portFAList = []
    create_port(rb=g.rest_base, suffix='Chassis',adapter='FabricAdapters', adapter_id=fa_id,port_id=fab_port_id,suffix_id=chassis, chassis_id=chassis)
    portFAList.append(fab_port_id)
    create_fabric_adapter(rb=g.rest_base, suffix='Chassis', fa_id=fa_id,
                                    suffix_id=chassis, chassis_id=chassis,portFAList=portFAList)

    fabric_id = "CXL"
    create_fabric(fabric_id)
    portnum = (len(sys_ids), len(rb_ids)-len(sys_ids))
    if 'switch' in cfg:
        for swt in cfg['switch']:
            swid = f'SWITCH-{swt["deviceID"]}'
            create_switch(fabric_id, swid, chassis, swt, portnum)
            portnum = (0, 0)

    create_serial_interface(rb=g.rest_base,manager_id=bmc,si_id='SI-1')
    CreateManager(resource_class_kwargs={
                'rb': g.rest_base, 'linkSystem': sys_ids, 'linkChassis': chassis, 'linkInChassis': chassis}).put(bmc)

    chassis_sensor_id = 'SENS-{0}'.format(chassis)
    CreateChassis(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': sys_ids, 'linkResourceBlocks':rb_ids, 'linkProcessor': proc_ids,'linkDrive': dri_ids, 'linkMgr': bmc, 'linkResource': resource, 'interval':'"PT3S"', 'sensor_id':chassis_sensor_id}).put(chassis)

    zone = CreateResourceZone(resource_class_kwargs={'rb': g.rest_base})
    zone.put('GlobalZone')
    [zone.post(g.rest_base, 'GlobalZone', 'ResourceBlocks', x) for x in zones['GlobalZone']]

def n_populate(num):
    # populate with some example infrastructure
    for i in range(num):
        chassis = 'Chassis-{0}'.format(i + 1)
        compSys = 'System-{0}'.format(i + 1)
        bmc = 'BMC-{0}'.format(i + 1)
        # create chassi
        CreateChassis(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': [compSys], 'linkStorage': bmc, 'linkMgr': bmc}).put(chassis)
        # create chassi subordinate sustems
        CreatePower(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
        CreateThermal(resource_class_kwargs={'rb': g.rest_base, 'ch_id': chassis}).put(chassis)
        # create ComputerSystem
        CreateComputerSystem(resource_class_kwargs={
            'rb': g.rest_base, 'linkChassis': [chassis], 'linkStorage': bmc, 'linkMgr': bmc}).put(compSys)
        # subordinates, note that .put does not need to be called here
        ResetAction_API(resource_class_kwargs={'rb': g.rest_base, 'sys_id': compSys})
        ResetActionInfo_API(resource_class_kwargs={'rb': g.rest_base, 'sys_id': compSys})
        create_processor(rb=g.rest_base, suffix='Systems', processor_id='CPU0', linkMemorys=[],suffix_id=compSys, chassis_id=chassis)
        create_processor(rb=g.rest_base, suffix='Systems', processor_id='CPU1', linkMemorys=[],suffix_id=compSys, chassis_id=chassis)
        create_memory(rb=g.rest_base, suffix='Systems', memory_id='DRAM1', suffix_id=compSys, chassis_id=chassis)
        create_memory(rb=g.rest_base, suffix='Systems', memory_id='NVRAM1', suffix_id=compSys, chassis_id=chassis,
                     capacitymb=65536, devicetype='DDR4', type='NVDIMM_N', operatingmodes=['PMEM'])
        CreateSimpleStorage(rb=g.rest_base, suffix='Systems', suffix_id=compSys, storage_id='controller-1', drives=2,
                            capacitygb=512, chassis_id=chassis)
        CreateSimpleStorage(rb=g.rest_base, suffix='Systems', suffix_id=compSys, storage_id='controller-2', drives=2,
                            capacitygb=512, chassis_id=chassis)
        CreateStorage(rb=g.rest_base, suffix='Systems', suffix_id=compSys, storage_id='controller-1', drives=2,
                            capacitygb=512, chassis_id=chassis)
        CreateEthernetInterface(rb=g.rest_base, suffix='Systems', suffix_id=compSys, nic_id='NIC-1',
                                speedmbps=40000, vlan_id=4095, chassis_id=chassis)
        CreateEthernetInterface(rb=g.rest_base, suffix='Systems', suffix_id=compSys, nic_id='NIC-2',
                                speedmbps=40000, vlan_id=4095, chassis_id=chassis)
        # create manager
        CreateManager(resource_class_kwargs={
            'rb': g.rest_base, 'linkSystem': compSys, 'linkChassis': chassis, 'linkInChassis': chassis}).put(bmc)

        # create Resource Block

        RB = 'RB-{0}'.format(i + 1)
        config = CreateResourceBlock(resource_class_kwargs={'rb': g.rest_base})
        config.put(RB)

        config.post(g.rest_base, RB, "linkSystem", "CS_%d" % i)
        config.post(g.rest_base, RB, "linkChassis", "Chassis-%d" % i)
        config.post(g.rest_base, RB, "linkZone", "ResourceZone-%d" % i)

        for j in range(2):
            # create ResourceBlock Processor (1)
            create_processor(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', processor_id='CPU-%d' % (i + 1),
                            suffix_id=RB, chassis_id=chassis, linkMemorys=[])
            config.post(g.rest_base, RB, "Processors", 'CPU-%d' % (j + 1))

            # create ResourceBlock Memory (1)
            create_memory(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', memory_id='MEM-%d' % (i + 1),
                         suffix_id=RB, chassis_id=chassis)
            config.post(g.rest_base, RB, "Memory", 'MEM-%d' % (j + 1))
            create_memory(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', memory_id='MEM-%d' % (i + 3),
                         suffix_id=RB, chassis_id=chassis,
                         capacitymb=65536, devicetype='DDR4', type='NVDIMM_N', operatingmodes='PMEM')
            config.post(g.rest_base, RB, "Memory", 'MEM-%d' % (j + 2))

            CreateSimpleStorage(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', suffix_id=RB,
                                storage_id='SS-%d' % (j + 1), drives=2,
                                capacitygb=512, chassis_id=chassis)
            config.post(g.rest_base, RB, "SimpleStorage", 'SS-%d' % (j + 1))

            CreateStorage(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', suffix_id=RB,
                                storage_id='SS-%d' % (j + 1), drives=2,
                                capacitygb=512, chassis_id=chassis)
            config.post(g.rest_base, RB, "Storage", 'STR-%d' % (j + 1))

            CreateEthernetInterface(rb=g.rest_base, suffix='CompositionService/ResourceBlocks', suffix_id=RB,
                                    nic_id='EI-%d' % (j + 1),
                                    speedmbps=40000, vlan_id=4095, chassis_id=chassis)
            config.post(g.rest_base, RB, "EthernetInterfaces", 'EI-%d' % (j + 1))

        # create Resource Zone

        RZ = 'RZ-{0}'.format(i + 1)

        config = CreateResourceZone(resource_class_kwargs={'rb': g.rest_base})

        config.put(RZ)
        config.post(g.rest_base, RZ, "ResourceBlocks", 'RB-%d' % (j + 1))
        config.post(g.rest_base, RZ, "ResourceBlocks", 'RB-%d' % (j + 2))

        #create
        MD = (i + 1)
        config = CreateMetricDefinitions(resource_class_kwargs={'rb': g.rest_base,'ChassisID':'Chassis-1','id': MD})
        config.put('PowerWatts')
        config.post(g.rest_base, MD, "MetricDefinitions", 'MD-%d' % (j + 1))
