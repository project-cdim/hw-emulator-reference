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

# Resource Manager Module

# External imports
import os
import json
import urllib3
import urllib.request, urllib.error
from uuid import uuid4
from threading import Thread
import logging
import copy
# Local imports
import g
from . import utils
from .resource_dictionary import ResourceDictionary
from .static_loader import load_static
# Local imports (special case)
from .redfish.computer_system import ComputerSystem
from .redfish.computer_systems import ComputerSystemCollection
from .exceptions import CreatePooledNodeError, RemovePooledNodeError, EventSubscriptionError
from .redfish.event_service import Subscription, EventService, Subscriptions
from .redfish.event import Event
# EventService imports
from .redfish.EventService_api import EventServiceAPI, CreateEventService, EventServiceActions_SubmitTestEventAPI
from .redfish.Subscriptions_api import SubscriptionCollectionAPI, SubscriptionAPI, CreateSubscription
# Chassis imports
from .redfish.Chassis_api import ChassisCollectionAPI, ChassisAPI, CreateChassis, ChassisActions_ResetAPI
from .redfish.power_api import PowerAPI, CreatePower
from .redfish.thermal_api import ThermalAPI, CreateThermal
from .redfish.PowerSubsystem_api import PowerSubsystemAPI, CreatePowerSubsystem
from .redfish.PowerSupply_api import PowerSupplyAPI, PowerSupplyCollectionAPI, PowerSupplyActions_ResetAPI
# Manager imports
from .redfish.Manager_api import ManagerCollectionAPI, ManagerAPI, CreateManager
# EgResource imports
from .redfish.eg_resource_api import EgResourceCollectionAPI, EgResourceAPI, CreateEgResource
from .redfish.eg_subresource_api import EgSubResourceCollectionAPI, EgSubResourceAPI, CreateEgSubResource
# ComputerSystem imports
from .redfish.ComputerSystem_api import ComputerSystemCollectionAPI, ComputerSystemAPI, CreateComputerSystem, state_enabled, state_disabled
from .redfish.processor_api import Processor, Processors, ChassisProcessors, ProcessorActionsResetAPI, ProcessorActionsResetToDefaultsAPI, ProcessorActionsMetricStateAPI
from .redfish.memory_api import Memory, MemoryCollection, ChassisMemoryCollection, MemoryActionsResetAPI, MemoryActionsResetToDefaultsAPI, MemoryActionsMetricStateAPI
from .redfish.simplestorage import SimpleStorage, SimpleStorageCollection
from .redfish.ethernetinterface import EthernetInterfaceCollection, EthernetInterface, EthernetInterface_ndf_Collection, EthernetInterface_ndf
from .redfish.ResetActionInfo_api import ResetActionInfo_API
from .redfish.ResetAction_api import ResetAction_API
# PCIe Switch imports
from .redfish.pcie_switch_api import PCIeSwitchesAPI, PCIeSwitchAPI
# CompositionService imports
from .redfish.CompositionService_api import CompositionServiceAPI
from .redfish.ResourceBlock_api import ResourceBlockCollectionAPI, ResourceBlockAPI
from .redfish.resourceobject import DenyResourceBlockActionAPI, ResourceBlockObjectAPI
from .redfish.ResourceZone_api import ResourceZoneCollectionAPI, ResourceZoneAPI, CreateResourceZone
# Telemetry imports
from .redfish.SessionService_api import SessionServiceAPI
from .redfish.sessions_api import SessionCollectionAPI, SessionAPI
from .redfish.account_service_api import AccountServiceAPI
from .redfish.manager_account_api import ManagerAccountCollectionAPI, ManagerAccountAPI
from .redfish.role_api import RoleCollectionAPI, RoleAPI
# Storage imports
from .redfish.storage_api import StorageAPI, StorageCollectionAPI, StorageSystemAPI, StorageSystemCollectionAPI
from .redfish.drive_api import DriveChassisAPI, DriveSystemsAPI, DriveCollectionAPI, DriveActionsResetAPI, DriveActionsMetricStateAPI
from .redfish.drive_metrics_api import DriveMetricsChassisAPI, DriveMetricsSystemsAPI
from .redfish.volume_api import VolumeChassisAPI, VolumeSystemsAPI, VolumeChassisCollectionAPI, VolumeSystemsCollectionAPI
from .redfish.storage_controller_api import StorageControllerChassisAPI, StorageControllerSystemsAPI, StorageControllerChassisCollectionAPI, StorageControllerSystemsCollectionAPI
from .redfish.storage_controller_metrics_api import StorageControllerMetricsChassisAPI, StorageControllerMetricsSystemsAPI
from .redfish.volume_metrics_api import VolumeMetricsChassisAPI, VolumeMetricsSystemsAPI
# Network imports
from .redfish.serial_interface_api import SerialInterfaceAPI, SerialInterfaceCollectionAPI
from .redfish.network_interface_api import NetworkInterfaceAPI, NetworkInterfaceCollectionAPI
from .redfish.network_adapter_api import NetworkAdapterAPI, NetworkAdapterCollectionAPI, NetworkAdapterActionsMetricStateAPI, NetworkAdapterActionsResetAPI
from .redfish.network_device_function_api import NetworkDeviceFunctionAPI, NetworkDeviceFunctionCollectionAPI
from .redfish.fabric_adapter_api import FabricAdapterAPI, FabricAdapterCollectionAPI
from .redfish.port_api import PortAPI, NetworkAdapterPortCollectionAPI, ProcessorPortCollectionAPI, PortControllerAPI, PortControllerCollectionAPI
#Other imports
from .redfish.graphics_controller_api import GraphicsControllerAPI, GraphicsControllerCollectionAPI
from .redfish.virtual_media_api import VirtualMediaAPI, VirtualMediaCollectionAPI
from .redfish.pcie_device_api import PCIeDeviceAPI, PCIeDeviceCollectionAPI
from .redfish.pcie_function_api import PCIeFunctionAPI, PCIeFunctionCollectionAPI
from .redfish.cxl_logical_device_api import CXLLogicalDeviceAPI, CXLLogicalDeviceCollectionAPI
from .redfish.sensor_api import SensorAPI, SensorCollectionAPI
from .redfish.fabric_api import FabricAPI, FabricCollectionAPI
from .redfish.switch_api import SwitchAPI, SwitchCollectionAPI
# Metrics imports
from .redfish.processor_metrics_api import ProcessorMetricsAPI
from .redfish.memory_metrics_api import MemoryMetricsAPI
from .redfish.environment_metrics_api import EnvironmentMetricsAPI, EnvironmentMetricsChassisAPI, EnvironmentMetricsSystemsAPI
from .redfish.network_adapter_metrics_api import NetworkAdapterMetricsAPI
from .redfish.network_device_function_metrics_api import NetworkDeviceFunctionMetricsAPI

mockupfolders = []

# The ResourceManager __init__ method sets up the static and dynamic
# resources.
#
# When a resource is accessed, the resource is sought in the following
# order:
#   1. Dynamic resources for specific URIs
#   2. Default dynamic resources
#   3. Static resource dictionary
#
# This allows specific resources to be implemented as dynamic resources
# while leaving the remainder of the URI path as static resources.
#
# Static resources are loaded from the ./redfish/static directory.
# This directory is a copy of the one of the ./mockups directories.
#
# Dynamic resources are attached to endpoints using the Flask-restful
# mechanism, not the Flask mechanism.
#   - This involves associating an API class to a resource endpoint.
#     A collection resource requires the association of the collection
#     resource and the member resource(s).
#   - Once the API is added, explicit calls can be made to one or more
#     singleton resources that have been populated.
#   - The EgResource* and EgSubResource* files provide examples of how
#     to add dynamic resources.
#
# Note: There is one additional change that needs to be made in order
# to create multiple instances of a resource. The resource endpoint
# for a second instance will collide with the first, because flask does
# not re-use endpoint names for subordinate resources. This results
# in an assertion error failure:
#   "AssertionError: View function mapping is overwriting an existing
#   endpoint function"
#
# The fix would be to form unique endpoint names and pass them in
# with the call to api_add_resource(), as shown in the following:
#   api.add_resource(Todo, '/todo/<int:todo_id>', endpoint='todo_ep')

class ResourceManager(object):
    """
    ResourceManager Class

    Load static resources and dynamic resources
    Defines ServiceRoot
    """

    def __init__(self, rest_base, spec, mode, trays=None):
        """
        Arguments:
            rest_base - Base URL for the REST interface
            spec      - Which spec to use, Redfish or Chinook
            trays     - (Optional) List of trays to initially load into the
                        resource manager
        When a resource is accessed, the resource is sought in the following order
        1. Dynamic resource for specific URI
        2. Static resource dictionary
        """

        self.rest_base = rest_base

        self.mode = mode
        self.spec = spec
        self.modified = utils.timestamp()
        self.uuid = str(uuid4())
        self.time = self.modified
        self.cs_puid_count = 0

        # Load the static resources into the dictionary

        self.resource_dictionary = ResourceDictionary()
        mockupfolders = copy.copy(g.staticfolders)

        if "Redfish" in mockupfolders:
            logging.info('Loading Redfish static resources')
            self.Registries =       load_static('Registries', 'redfish', mode, rest_base, self.resource_dictionary)
            self.TaskService =      load_static('TaskService', 'redfish', mode, rest_base, self.resource_dictionary)

#        if "Swordfish" in mockupfolders:
#            self.StorageServices = load_static('StorageServices', 'redfish', mode, rest_base, self.resource_dictionary)
#            self.StorageSystems = load_static('StorageSystems', 'redfish', mode, rest_base, self.resource_dictionary)

        # Attach APIs for dynamic resources

        # EventService Resources
        g.api.add_resource(EventServiceAPI, '/redfish/v1/EventService',
                resource_class_kwargs={'rb': g.rest_base, 'id': "EventService"})
        g.api.add_resource(EventServiceActions_SubmitTestEventAPI, '/redfish/v1/EventService/Actions/EventService.SubmitTestEvent',
                resource_class_kwargs={'rb': g.rest_base})
        # EventService SubResources
        g.api.add_resource(SubscriptionCollectionAPI, '/redfish/v1/EventService/Subscriptions')
        g.api.add_resource(SubscriptionAPI, '/redfish/v1/EventService/Subscriptions/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})

        # Chassis Resources
        g.api.add_resource(ChassisCollectionAPI, '/redfish/v1/Chassis')
        g.api.add_resource(ChassisAPI, '/redfish/v1/Chassis/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})
        g.api.add_resource(ChassisActions_ResetAPI, '/redfish/v1/Chassis/<string:ident>/Actions/Chassis.Reset',
                resource_class_kwargs={'rb': g.rest_base})
        # Chassis SubResources
        g.api.add_resource(ThermalAPI, '/redfish/v1/Chassis/<string:ident>/Thermal',
                resource_class_kwargs={'rb': g.rest_base})
        # Chassis SubResources
        g.api.add_resource(PowerAPI, '/redfish/v1/Chassis/<string:ident>/Power',
                resource_class_kwargs={'rb': g.rest_base})

        # Manager Resources
        g.api.add_resource(ManagerCollectionAPI, '/redfish/v1/Managers')
        g.api.add_resource(ManagerAPI, '/redfish/v1/Managers/<string:ident>', resource_class_kwargs={'rb': g.rest_base})

        # EgResource Resources (Example entries for attaching APIs)
        # g.api.add_resource(EgResourceCollectionAPI,
        #     '/redfish/v1/EgResources')
        # g.api.add_resource(EgResourceAPI,
        #     '/redfish/v1/EgResources/<string:ident>',
        #     resource_class_kwargs={'rb': g.rest_base})
        #
        # EgResource SubResources (Example entries for attaching APIs)
        # g.api.add_resource(EgSubResourceCollection,
        #     '/redfish/v1/EgResources/<string:ident>/EgSubResources',
        #     resource_class_kwargs={'rb': g.rest_base})
        # g.api.add_resource(EgSubResource,
        #     '/redfish/v1/EgResources/<string:ident1>/EgSubResources/<string:ident2>',
        #     resource_class_kwargs={'rb': g.rest_base})

        # System Resources
        g.api.add_resource(ComputerSystemCollectionAPI, '/redfish/v1/Systems')
        g.api.add_resource(ComputerSystemAPI, '/redfish/v1/Systems/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})
        # System SubResources
        g.api.add_resource(Processors, '/redfish/v1/Systems/<string:ident>/Processors',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(ChassisProcessors, '/redfish/v1/Chassis/<string:ident>/Processors',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(Processor, '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>',
                '/redfish/v1/Chassis/<string:ident1>/Processors/<string:ident2>')
        g.api.add_resource(ProcessorActionsResetAPI, '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/Actions/Processor.Reset',
                '/redfish/v1/Chassis/<string:ident1>/Processors/<string:ident2>/Actions/Processor.Reset',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(ProcessorActionsResetToDefaultsAPI, '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/Actions/Processor.ResetToDefaults',
                '/redfish/v1/Chassis/<string:ident1>/Processors/<string:ident2>/Actions/Processor.ResetToDefaults',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(ProcessorActionsMetricStateAPI, '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/Actions/Processor.MetricState',
                '/redfish/v1/Chassis/<string:ident1>/Processors/<string:ident2>/Actions/Processor.MetricState',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        # System SubResources
        g.api.add_resource(MemoryCollection, '/redfish/v1/Systems/<string:ident>/Memory',
                 resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(ChassisMemoryCollection, '/redfish/v1/Chassis/<string:ident>/Memory',
                 resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(Memory, '/redfish/v1/Systems/<string:ident1>/Memory/<string:ident2>',
                '/redfish/v1/Chassis/<string:ident1>/Memory/<string:ident2>')
        g.api.add_resource(MemoryActionsResetAPI, '/redfish/v1/Chassis/<string:ident1>/Memory/<string:ident2>/Actions/Memory.Reset',
                '/redfish/v1/Systems/<string:ident1>/Memory/<string:ident2>/Actions/Memory.Reset',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(MemoryActionsResetToDefaultsAPI, '/redfish/v1/Chassis/<string:ident1>/Memory/<string:ident2>/Actions/Memory.ResetToDefaults',
                '/redfish/v1/Systems/<string:ident1>/Memory/<string:ident2>/Actions/Memory.ResetToDefaults',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(MemoryActionsMetricStateAPI, '/redfish/v1/Chassis/<string:ident1>/Memory/<string:ident2>/Actions/Memory.MetricState',
                '/redfish/v1/Systems/<string:ident1>/Memory/<string:ident2>/Actions/Memory.MetricState',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
                

        # System SubResources
        g.api.add_resource(SimpleStorageCollection, '/redfish/v1/Systems/<string:ident>/SimpleStorage',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(SimpleStorage, '/redfish/v1/Systems/<string:ident1>/SimpleStorage/<string:ident2>',
                '/redfish/v1/CompositionService/ResourceBlocks/<string:ident1>/SimpleStorage/<string:ident2>')
        # System SubResources
        g.api.add_resource(StorageSystemCollectionAPI, '/redfish/v1/Systems/<string:ident>/Storage',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(StorageSystemAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>',
                '/redfish/v1/CompositionService/ResourceBlocks/<string:ident1>/Storage/<string:ident2>')
        g.api.add_resource(StorageCollectionAPI, '/redfish/v1/Storage')
        g.api.add_resource(StorageAPI, '/redfish/v1/Storage/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})

        # System SubResources
        g.api.add_resource(EthernetInterfaceCollection, '/redfish/v1/Systems/<string:ident>/EthernetInterfaces',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(EthernetInterface_ndf_Collection, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions/<string:ident3>/EthernetInterfaces',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(EthernetInterface, '/redfish/v1/Systems/<string:ident1>/EthernetInterfaces/<string:ident2>')
        g.api.add_resource(EthernetInterface_ndf, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions/<string:ident3>/EthernetInterfaces/<string:ident4>')
        # System SubResources
        g.api.add_resource(ResetActionInfo_API, '/redfish/v1/Systems/<string:ident>/ResetActionInfo',
                resource_class_kwargs={'rb': g.rest_base})
        g.api.add_resource(ResetAction_API, '/redfish/v1/Systems/<string:ident>/Actions/ComputerSystem.Reset',
                resource_class_kwargs={'rb': g.rest_base})

        g.api.add_resource(FabricCollectionAPI, '/redfish/v1/Fabrics')
        g.api.add_resource(FabricAPI, '/redfish/v1/Fabrics/<string:ident>')
        g.api.add_resource(SwitchCollectionAPI, '/redfish/v1/Fabrics/<string:ident>/Switches')
        g.api.add_resource(SwitchAPI, '/redfish/v1/Fabrics/<string:ident1>/Switches/<string:ident2>')

        # PCIe Switch Resources
        g.api.add_resource(PCIeSwitchesAPI, '/redfish/v1/PCIeSwitches')
        g.api.add_resource(PCIeSwitchAPI, '/redfish/v1/PCIeSwitches/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})

        # Composition Service Resources
        g.api.add_resource(CompositionServiceAPI, '/redfish/v1/CompositionService',
                resource_class_kwargs={'rb': g.rest_base, 'id': "CompositionService"})
        # Composition Service SubResources
        g.api.add_resource(ResourceBlockCollectionAPI, '/redfish/v1/CompositionService/ResourceBlocks')
        g.api.add_resource(ResourceBlockAPI, '/redfish/v1/CompositionService/ResourceBlocks/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})

        # Resource objects contained in the Composition Service resource block
        resource_path = '/redfish/v1/CompositionService/ResourceBlocks'
        g.api.add_resource(ResourceBlockObjectAPI,
                f'{resource_path}/<string:ident1>/<string:ident2>/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base})
        g.api.add_resource(DenyResourceBlockActionAPI,
                f'{resource_path}/<string:ident1>/Processors/<string:ident2>/Actions/Processor.MetricState',
                f'{resource_path}/<string:ident1>/Processors/<string:ident2>/Actions/Processor.Reset',
                f'{resource_path}/<string:ident1>/Processors/<string:ident2>/EnvironmentMetrics',
                f'{resource_path}/<string:ident1>/Processors/<string:ident2>/MemorySummary/MemoryMetrics',
                f'{resource_path}/<string:ident1>/Processors/<string:ident2>/Ports',
                f'{resource_path}/<string:ident1>/Memory/<string:ident2>/Actions/Memory.MetricState',
                f'{resource_path}/<string:ident1>/Memory/<string:ident2>/Actions/Memory.Reset',
                f'{resource_path}/<string:ident1>/Memory/<string:ident2>/MemoryMetrics',
                f'{resource_path}/<string:ident1>/Memory/<string:ident2>/EnvironmentMetrics',
                f'{resource_path}/<string:ident1>/Drives/<string:ident2>/Actions/Drive.MetricState',
                f'{resource_path}/<string:ident1>/Drives/<string:ident2>/Actions/Drive.Reset',
                f'{resource_path}/<string:ident1>/Drives/<string:ident2>/EnvironmentMetrics',
                f'{resource_path}/<string:ident1>/Drives/<string:ident2>/Metrics',
                resource_class_kwargs={'rb': g.rest_base})

        # Composition Service SubResources
        g.api.add_resource(ResourceZoneCollectionAPI, '/redfish/v1/CompositionService/ResourceZones')
        g.api.add_resource(ResourceZoneAPI, '/redfish/v1/CompositionService/ResourceZones/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})

        # SessionService Resources
        g.api.add_resource(SessionServiceAPI, '/redfish/v1/SessionService',
                resource_class_kwargs={'rb': g.rest_base})

        # SessionService Service Resources
        g.api.add_resource(SessionCollectionAPI, '/redfish/v1/SessionService/Sessions')
        g.api.add_resource(SessionAPI, '/redfish/v1/SessionService/Sessions/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})
        
        # AccountService Resources
        g.api.add_resource(AccountServiceAPI, '/redfish/v1/AccountService',
                resource_class_kwargs={'rb': g.rest_base})

        # AccountService ManagerAccount Resources
        g.api.add_resource(ManagerAccountCollectionAPI, '/redfish/v1/AccountService/Accounts')
        g.api.add_resource(ManagerAccountAPI, '/redfish/v1/AccountService/Accounts/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})
        
        # AccountService Roles Resources
        g.api.add_resource(RoleCollectionAPI, '/redfish/v1/AccountService/Roles')
        g.api.add_resource(RoleAPI, '/redfish/v1/AccountService/Roles/<string:ident>',
                resource_class_kwargs={'rb': g.rest_base})

        # Drive Resources
        g.api.add_resource(DriveCollectionAPI, '/redfish/v1/Chassis/<string:ident>/Drives',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(DriveChassisAPI, '/redfish/v1/Chassis/<string:ident1>/Drives/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(DriveSystemsAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Drives/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(DriveActionsResetAPI, '/redfish/v1/Chassis/<string:ident1>/Drives/<string:ident2>/Actions/Drive.Reset',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(DriveActionsMetricStateAPI, '/redfish/v1/Chassis/<string:ident1>/Drives/<string:ident2>/Actions/Drive.MetricState',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        g.api.add_resource(DriveMetricsChassisAPI, '/redfish/v1/Chassis/<string:ident1>/Drives/<string:ident2>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(DriveMetricsSystemsAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Drives/<string:ident3>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # Volume Resources
        g.api.add_resource(VolumeChassisCollectionAPI, '/redfish/v1/Storage/<string:ident>/Volumes',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(VolumeChassisAPI, '/redfish/v1/Storage/<string:ident1>/Volumes/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(VolumeSystemsCollectionAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Volumes',
                resource_class_kwargs={'rb': g.rest_base})
        g.api.add_resource(VolumeSystemsAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Volumes/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        g.api.add_resource(VolumeMetricsChassisAPI, '/redfish/v1/Storage/<string:ident1>/Volumes/<string:ident2>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(VolumeMetricsSystemsAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Volumes/<string:ident3>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # StorageController Resources
        g.api.add_resource(StorageControllerChassisCollectionAPI, '/redfish/v1/Storage/<string:ident>/Controllers',
                resource_class_kwargs={'rb': g.rest_base})
        g.api.add_resource(StorageControllerSystemsCollectionAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Controllers',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(StorageControllerChassisAPI, '/redfish/v1/Storage/<string:ident1>/Controllers/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(StorageControllerSystemsAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Controllers/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        g.api.add_resource(StorageControllerMetricsChassisAPI, '/redfish/v1/Storage/<string:ident1>/Controllers/<string:ident2>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(StorageControllerMetricsSystemsAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Controllers/<string:ident3>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        
        # SerialInterface Resources
        g.api.add_resource(SerialInterfaceCollectionAPI, '/redfish/v1/Managers/<string:ident>/SerialInterfaces',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Managers'})
        g.api.add_resource(SerialInterfaceAPI, '/redfish/v1/Managers/<string:ident1>/SerialInterfaces/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Managers'})

        # NetworkInterface Resources
        g.api.add_resource(NetworkInterfaceCollectionAPI, '/redfish/v1/Systems/<string:ident>/NetworkInterfaces',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(NetworkInterfaceAPI, '/redfish/v1/Systems/<string:ident1>/NetworkInterfaces/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # NetworkAdapter Resources
        g.api.add_resource(NetworkAdapterCollectionAPI, '/redfish/v1/Chassis/<string:ident>/NetworkAdapters',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(NetworkAdapterAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(NetworkAdapterActionsResetAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/Actions/NetworkAdapter.Reset',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(NetworkAdapterActionsMetricStateAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/Actions/NetworkAdapter.MetricState',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
                

        # NetworkDeviceFunction Resources
        g.api.add_resource(NetworkDeviceFunctionCollectionAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions',
                           '/redfish/v1/Systems/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(NetworkDeviceFunctionAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions/<string:ident3>',
                           '/redfish/v1/Systems/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # FabricAdapter Resources
        g.api.add_resource(FabricAdapterCollectionAPI, '/redfish/v1/Chassis/<string:ident>/FabricAdapters',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(FabricAdapterAPI, '/redfish/v1/Chassis/<string:ident1>/FabricAdapters/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        # Port Resources
        g.api.add_resource(NetworkAdapterPortCollectionAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/Ports',
                '/redfish/v1/Chassis/<string:ident1>/FabricAdapters/<string:ident2>/Ports',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(ProcessorPortCollectionAPI, '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/Ports',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(PortControllerCollectionAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Controllers/<string:ident3>/Ports',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(PortAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/Ports/<string:ident3>',
                '/redfish/v1/Chassis/<string:ident1>/FabricAdapters/<string:ident2>/Ports/<string:ident3>',
                '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/Ports/<string:ident3>',
                '/redfish/v1/Storage/<string:ident1>/Controllers/<string:ident2>/Ports/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(PortControllerAPI, '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Controllers/<string:ident3>/Ports/<string:ident4>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        

        # GraphicsController Resources
        g.api.add_resource(GraphicsControllerCollectionAPI, '/redfish/v1/Systems/<string:ident>/GraphicsControllers',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(GraphicsControllerAPI, '/redfish/v1/Systems/<string:ident1>/GraphicsControllers/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # VirtualMedia Resources
        g.api.add_resource(VirtualMediaCollectionAPI, '/redfish/v1/Systems/<string:ident>/VirtualMedia',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})
        g.api.add_resource(VirtualMediaAPI, '/redfish/v1/Systems/<string:ident1>/VirtualMedia/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # PCIeDevice Resources
        g.api.add_resource(PCIeDeviceCollectionAPI, '/redfish/v1/Chassis/<string:ident>/PCIeDevices',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(PCIeDeviceAPI, '/redfish/v1/Chassis/<string:ident1>/PCIeDevices/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        # PCIeFunction Resources
        g.api.add_resource(PCIeFunctionCollectionAPI, '/redfish/v1/Chassis/<string:ident1>/PCIeDevices/<string:ident2>/PCIeFunctions',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(PCIeFunctionAPI, '/redfish/v1/Chassis/<string:ident1>/PCIeDevices/<string:ident2>/PCIeFunctions/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # CXLLogicalDevice Resources
        g.api.add_resource(CXLLogicalDeviceCollectionAPI, '/redfish/v1/Chassis/<string:ident1>/PCIeDevices/<string:ident2>/CXLLogicalDevices',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(CXLLogicalDeviceAPI, '/redfish/v1/Chassis/<string:ident1>/PCIeDevices/<string:ident2>/CXLLogicalDevices/<string:ident3>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # Sensor Resources
        g.api.add_resource(SensorCollectionAPI, '/redfish/v1/Chassis/<string:ident>/Sensors',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(SensorAPI, '/redfish/v1/Chassis/<string:ident1>/Sensors/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        # ProcessorMetrics Resources
        g.api.add_resource(ProcessorMetricsAPI, '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/ProcessorMetrics',
                '/redfish/v1/Chassis/<string:ident1>/Processors/<string:ident2>/ProcessorMetrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        # MemoryMetrics Resources
        g.api.add_resource(MemoryMetricsAPI, '/redfish/v1/Systems/<string:ident1>/Memory/<string:ident2>/MemoryMetrics',
                           '/redfish/v1/Chassis/<string:ident1>/Memory/<string:ident2>/MemoryMetrics',
                           '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/MemorySummary/MemoryMetrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        # NetworkAdapterMetrics Resources
        g.api.add_resource(NetworkAdapterMetricsAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        # NetworkDeviceFunctionMetrics Resources
        g.api.add_resource(NetworkDeviceFunctionMetricsAPI, '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/NetworkDeviceFunctions/<string:ident3>/Metrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        #EnvironmentMetrics Resources
        g.api.add_resource(EnvironmentMetricsAPI, 
                           '/redfish/v1/Systems/<string:ident1>/Processors/<string:ident2>/EnvironmentMetrics',
                '/redfish/v1/Chassis/<string:ident1>/Processors/<string:ident2>/EnvironmentMetrics',
                '/redfish/v1/Systems/<string:ident1>/Memory/<string:ident2>/EnvironmentMetrics',
                '/redfish/v1/Chassis/<string:ident1>/Memory/<string:ident2>/EnvironmentMetrics',
                '/redfish/v1/Chassis/<string:ident1>/Drives/<string:ident2>/EnvironmentMetrics',
                '/redfish/v1/Chassis/<string:ident1>/NetworkAdapters/<string:ident2>/EnvironmentMetrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        g.api.add_resource(EnvironmentMetricsChassisAPI, 
                '/redfish/v1/Chassis/<string:ident1>/EnvironmentMetrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        g.api.add_resource(EnvironmentMetricsSystemsAPI, 
                '/redfish/v1/Systems/<string:ident1>/Storage/<string:ident2>/Drives/<string:ident3>/EnvironmentMetrics',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Systems'})

        #PowerSubsystem Resources
        g.api.add_resource(PowerSubsystemAPI, '/redfish/v1/Chassis/<string:ident>/PowerSubsystem',
                resource_class_kwargs={'rb': g.rest_base})

        #PowerSupplies Resources
        g.api.add_resource(PowerSupplyCollectionAPI, '/redfish/v1/Chassis/<string:ident>/PowerSubsystem/PowerSupplies',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(PowerSupplyAPI, '/redfish/v1/Chassis/<string:ident1>/PowerSubsystem/PowerSupplies/<string:ident2>',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})
        g.api.add_resource(PowerSupplyActions_ResetAPI, '/redfish/v1/Chassis/<string:ident1>/PowerSubsystem/PowerSupplies/<string:ident2>/Actions/PowerSupply.Reset',
                resource_class_kwargs={'rb': g.rest_base,'suffix':'Chassis'})

        

    @property
    def configuration(self):
        """
        Configuration property - Service Root
        """
        config = {
            '@odata.context': self.rest_base + '$metadata#ServiceRoot',
            '@odata.type': '#ServiceRoot.1.0.0.ServiceRoot',
            '@odata.id': "/redfish/v1",
            'Id': 'RootService',
            'Name': 'Root Service',
            'RedfishVersion': '1.0.0',
            'UUID': self.uuid,
            'Chassis': {'@odata.id': self.rest_base + 'Chassis'},
            # 'EgResources': {'@odata.id': self.rest_base + 'EgResources'},
            'Managers': {'@odata.id': self.rest_base + 'Managers'},
            'TaskService': {'@odata.id': self.rest_base + 'TaskService'},
            'SessionService': {'@odata.id': self.rest_base + 'SessionService'},
            'AccountService': {'@odata.id': self.rest_base + 'AccountService'},
            'EventService': {'@odata.id': self.rest_base + 'EventService'},
            'Registries': {'@odata.id': self.rest_base + 'Registries'},
            'Systems': {'@odata.id': self.rest_base + 'Systems'},
            'CompositionService': {'@odata.id': self.rest_base + 'CompositionService'},
            'TelemetryService': {'@odata.id': self.rest_base + 'TelemetryService'}
        }

        return config

    @property
    def available_procs(self):
        return self.max_procs - self.used_procs

    @property
    def available_mem(self):
        return self.max_memory - self.used_memory

    @property
    def available_storage(self):
        return self.max_storage - self.used_storage

    @property
    def available_network(self):
        return self.max_network - self.used_network

    @property
    def num_pooled_nodes(self):
        if self.spec == 'Chinook':
            return self.PooledNodes.count
        else:
            return self.Systems.count

    def _create_redfish(self, rs, action):
        """
        Private method for creating a Redfish based pooled node

        Arguments:
            rs  - The requested pooled node
        """
        try:
            pn = ComputerSystem(rs, self.cs_puid_count + 1, self.rest_base, 'Systems')
            self.Systems.add_computer_system(pn)
        except KeyError as e:
            raise CreatePooledNodeError(
                'Configuration missing key: ' + e.message)
        try:
            # Verifying resources
            assert pn.processor_count <= self.available_procs, self.err_str.format('CPUs')
            assert pn.storage_gb <= self.available_storage, self.err_str.format('storage')
            assert pn.network_ports <= self.available_network, self.err_str.format('network ports')
            assert pn.total_memory_gb <= self.available_mem, self.err_str.format('memory')

            self.used_procs += pn.processor_count
            self.used_storage += pn.storage_gb
            self.used_network += pn.network_ports
            self.used_memory += pn.total_memory_gb
        except AssertionError as e:
            self._remove_redfish(pn.cs_puid)
            raise CreatePooledNodeError(e.message)
        except KeyError as e:
            self._remove_redfish(pn.cs_puid)
            raise CreatePooledNodeError(
                'Requested system missing key: ' + e.message)

        self.resource_dictionary.add_resource('Systems/{0}'.format(pn.cs_puid), pn)
        self.cs_puid_count += 1
        return pn.configuration

    def _remove_redfish(self, cs_puid):
        """
        Private method for removing a Redfish based pooled node

        Arguments:
            cs_puid - CS_PUID of the pooled node to remove
        """
        try:
            pn = self.Systems[cs_puid]

            # Adding back in used resources
            self.used_procs -= pn.processor_count
            self.used_storage -= pn.storage_gb
            self.used_network -= pn.network_ports
            self.used_memory -= pn.total_memory_gb

            self.Systems.remove_computer_system(pn)
            self.resource_dictionary.delete_resource('Systems/{0}'.format(cs_puid))

            if self.Systems.count == 0:
                self.cs_puid_count = 0
        except IndexError:
            raise RemovePooledNodeError(
                'No pooled node with CS_PUID: {0}, exists'.format(cs_puid))

    def get_resource(self, path):
        """
        Call Resource_Dictionary's get_resource
        """
        obj = self.resource_dictionary.get_resource(path)
        return obj



    def remove_pooled_node(self, cs_puid):
        """
        Delete the specified pooled node and free its resources.

        Throws a RemovePooledNodeError Exception if a problem is encountered.

        Arguments:
            cs_puid - CS_PUID of the pooed node to remove
        """
        self.remove_method(cs_puid)

    def update_cs(self,cs_puid,rs):
        """
            Updates the power metrics of Systems/1
        """
        #cs=self.Systems[cs_puid]
        #cs.reboot(rs)
        #return cs.configuration

        event = Event(resourceTypes='ComputerSystem', severity='Notification', message='System updated',
                      messageID='ResourceUpdated.1.0.System', originOfCondition='/redfish/v1/System/{0}'.format(cs_puid))
        self.push_event(event, 'ComputerSystem')

        resp = 200
        return resp

    def update_system(self,rs,c_id):
        """
            Updates selected System
        """
        systemUpdate = rs['Status']['State']

        if systemUpdate == 'Enabled':
            resp = state_enabled(c_id)
        else:
            resp = state_disabled(c_id)

        #state_disabled
        #
        event = Event(resourceTypes='ComputerSystem', severity='Notification', message='System updated',
                      messageID='StatusChange.1.0.System', originOfCondition='/redfish/v1/System/{0}'.format(c_id))
        self.push_event(event, 'ComputerSystem')

        return resp

    def add_event_subscription(self, rs):
        destination = rs['Destination']
        types = rs['Types']
        context = rs['Context']

        allowedTypes = ['StatusChange',
                        'ResourceUpdated',
                        'ResourceAdded',
                        'ResourceRemoved',
                        'Alert']

        for type in types:
            match = False
            for allowedType in allowedTypes:
                if type == allowedType:
                    match = True

            if not match:
                raise EventSubscriptionError('Some of types are not allowed')

        es = self.Subscriptions.add_subscription(destination, types, context)
        es_id = es.configuration['Id']
        self.resource_dictionary.add_resource('EventService/Subscriptions/{0}'.format(es_id), es)
        event = Event()
        self.push_event(event, 'Alert')
        return es.configuration

    def push_event(self, event, type):
        # Retreive subscription list

        checkSubscriptions = SubscriptionCollectionAPI()
        subscribe = checkSubscriptions.get()
        checkSub = subscribe[0]['Links']['Members']
        
        cfg = SubscriptionAPI()

        for sub in checkSub:
           
           # Get event subscription
           eventId =sub['@odata.id'].replace('/redfish/v1/EventService/Subscriptions/', '')
           event_channel = cfg.get(eventId)
           logging.info(event_channel)
           
           resource_types = event_channel[0]['ResourceTypes']
           dest_uri = event_channel[0]['Destination']
           logging.info(resource_types)

            # Check if client subscribes for event type
        #    match = False
           for resource_type in resource_types:
               if resource_type == type:
                   match = True

           if match:
               # Sending event response
               EventWorker(dest_uri, event).start()


class EventWorker(Thread):
    """
    Worker class for sending event messages to clients
    """
    def __init__(self, dest_uri, event):
        super(EventWorker, self).__init__()
        self.dest_uri = dest_uri
        self.event = event

    def run(self):
        logging.info('EventWorker caaaaaaaaalled') 
        try:
            '''
            logging.info(self.dest_uri)
            request = urllib.request.Request(self.dest_uri)
            request.add_header('Content-Type', 'application/json')
            urllib.request.urlopen(request, json.dumps(self.event.configuration), 15)
            '''

            headers = { 'Content-Type': 'application/json' }
            data = json.dumps(self.event.configuration).encode('utf-8')

            req = urllib.request.Request(
                url=self.dest_uri,
                data=data,
                headers=headers)
            with urllib.request.urlopen(req) as res:
                text = res.read().decode('utf-8')
        except Exception:
            pass

