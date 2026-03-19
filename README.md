# Redfish Interface Emulator

## Table of Contents
- [Overview](#overview)
- [Source of DMTF Redfish Interface Emulator](#source-of-dmtf-redfish-interface-emulator)
- [Setting up the Execution Environment](#setting-up-the-execution-environment)
  - [Startup Method](#startup-method)
  - [Setup Procedure](#setup-procedure)
  - [Configuration Items](#configuration-items)
  - [Creating Devices](#creating-devices)
  - [Adding Resources](#adding-resources)
  - [Device Definition Files](#device-definition-files)
  - [Setting Return Data Values](#setting-return-data-values)
- [Usage](#usage)
  - [Available Resources](#available-resources)
    - [Retrieve](#retrieve)
    - [Operations](#operations)
      - [Power Operations](#power-operations)
      - [Load State Operations](#load-state-operations)
    - [Supported Devices](#supported-devices)
- [File List](#file-list)

## Overview
The Redfish Interface Emulator is designed to provide an environment for evaluating device information retrieval functionality.

The Redfish Interface Emulator is a tool capable of emulating Redfish interface resources.
It allows performing GET, PUT, POST, DELETE, and PATCH operations by preparing JSON files in advance and loading them.

The Redfish Interface Emulator extends the DMTF Redfish Interface Emulator by adding code to an installation of the DMTF Redfish Interface Emulator code.  
The Redfish Interface Emulator code is maintained on GitHub by the NEC Corporation, and the DMTF Redfish Interface Emulator code is maintained on GitHub by the DMTF.

## Source of DMTF Redfish Interface Emulator
[DMTF/Redfish-Interface-Emulator](https://github.com/DMTF/Redfish-Interface-Emulator)  
Using version 1.1.7 at the Releases point in time.

## Setting up the Execution Environment
* Version of the constructed environment  
  Python 3.11.9

### Startup Method
1. Move to the directory where this file is located.  
2. Create a Docker image from the Dockerfile.  
   `ex. $ docker build . -t redfish-emulator:v1.0.test`
3. Start the docker image.  
   `ex. $ docker run -p 5000:5000 -it redfish-emulator:v1.0.test`
4. Check if information retrieval is possible.  
   `ex. $ curl http://localhost:5000/redfish/v1/`  
   * Confirm that information is returned.

### Setup Procedure
1. Prepare the device definition file.  
   * Refer to [Device Definition Files](#device-definition-files) below.
2. Edit the configuration file.
   * Refer to [Configuration Items](#configuration-items) below.
3. Start the Redfish Interface Emulator.
   * Refer to [Startup Method](#startup-method).

### Configuration Items
Configuration file name
* emulator-config_device_populate.json
  
If not using a device definition file, use "emulator-config_dynamic_populate.json".   
Modify lines 43-44 of emulator.py  
``` ex.
        CONFIG = 'emulator-config_dynamic_populate.json' // Use this one
        #CONFIG = 'emulator-config_device_populate.json' // Comment out the configuration file for using the device definition file
```

About each item.  
For this Redfish Interface Emulator, configure as follows.  
Refer to the README at [Source of DMTF Redfish Interface Emulator](#source-of-dmtf-redfish-interface-emulator) for details on each item.

| Item | Description | Setting Value |
|:--|:--|:--|
| MODE | Specify the port to be used. If the value is "Local", the port is assigned with the default command line or the port parameter value of 5000. | Local |
| HTTPS | Use HTTPS | Disable |
| TRAYS | Paths to resources constituting the initial resource pool. Multiple trays can be specified. If TRAYS is specified, it is retrieved from TRAYS when creating the device. The detailed usage is unknown as there is no place it is used currently. | Not used |
| POPULATE | Elements at emulator startup. Specify the device definition file. | ../simulatorDeviceList.json |
| DEVICE_SPEC | Whether to create a device using a device definition file. Be sure to specify it if using a device definition file. | true |
| SPEC | Whether the computer system is represented as Redfish ComputerSystem or as another schema. Used when setting the system path. | Redfish |
| MOCKUPFOLDERS | The storage location of the mockup folder. The folder stores JSON files used when returning static data (mockup) that is not changed or operated on. | Redfish |
| POWER_LINK | Synchronize the power state of the CPU with GPUs, memory, storage, and NICs present in the same ComputerSystem. | true |

### Creating Devices
Set the device information to be returned from the Redfish Interface Emulator.

Creating an existing device type
1. Edit the device definition file
      * Refer to [Device Definition Files](#device-definition-files) below.
2. If you want to specify initial values for the device, set the return data values.
      * Refer to [Setting Return Data Values](#setting-return-data-values) below.
3. Start the emulator.

Adding a new device type
1. Edit the device definition file
      * Refer to [Device Definition Files](#device-definition-files) below.
2. If you want to specify initial values for the device, set the return data values.
      * Refer to [Setting Return Data Values](#setting-return-data-values) below.
3. Modify the file for creating devices
      * File for device creation: Redfish_Simulator/infragen/populate.py
        * Function: d_populate
     1. Retrieve the list of newly added device types from the device definition file
     2. Set IDs and other necessary items for creating devices, and create the device
        * If the schema does not exist in the emulator, perform [Adding Resources](#adding-resources)
        * If a response is needed for a new URL, add a description in resource_manager.py
        `ex. g.api.add_resource(StorageCollectionAPI, '/redfish/v1/Storage')`
4. Start the emulator

Sample of how to write d_populate
``` ex.
        if 'cpu' in cfg:
		      resource.append('Processors')
		      for cpu_template in cfg['cpu']: // Retrieve the list of device types from the device definition file

            // Set the IDs and other items necessary for creating the device
			      processor_id = cpu_template.get('deviceID')
			      proc_id='PROC-{0}'.format(processor_id)
			      resource_ids['Processors'].append(proc_id)

            // Create linked device if any
                  for mem in cpu_template.get('link'):
                  // Omitted

            // Omitted, set IDs and other items necessary for creating the device

            // Create a resource block used for configuration changes
			      rb_ids.append(_create_resource_block(rb_id, rb_idevs, chassis, zones, compSys))

            // Set initial values from the return data
			      model =  cpu_template.get('model')
			      manufacturer =  cpu_template.get('manufacturer')
			      tec = parameter[processor_id]['totalEnabledCores']
			      cpu_osm = parameter[processor_id]['operatingSpeedMHz']

            // Create the device
			      CreateProcessor(rb=g.rest_base, suffix='Systems', processor_id=proc_id,sensor_id = proc_sensor_id, suffix_id=compSys, chassis_id=chassis, linkMemorys=resource_ids['Memory'],pcie_id=pcie_id,model=model,manufacturer=manufacturer,tec=tec,cpu_osm=cpu_osm,serialNumber=cpu_template.get('serialNumber', 8), processorType='CPU')
		
            // Create associated schema if any to create the device
			      CreatePCIeDevice(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id,pcie_f_id=pcie_f_id,suffix_id=compSys, chassis_id=chassis)
			      CreatePCIeFunction(rb=g.rest_base, suffix='Systems', pcie_id=pcie_id,pcie_f_id=pcie_f_id,suffix_id=compSys, chassis_id=chassis)

```
※Omission of other code details

### Adding Resources
In the case of adding new resources (schema) to be managed by the emulator, create the corresponding resource files.  
※Resources in the Redfish Interface Emulator are data objects that mock the hardware and settings accessed through the Redfish API.

1. Create a template file and API file for resources
    1. Create a template file  
      Execute the following command in the Redfish_Simulator/codegen folder  
      `ex. $ python codegen_template.py [mockup]`
        * mockup: Resource name
        * Place the created file in the ./Redfish_Simulator/api_emulator/redfish/template directory
    2. Create an API file  
       Execute the following command in the Redfish_Simulator/codegen folder  
      `ex. $ python codegen_api.py [mockup]`
        * mockup: Resource name_api
        * Place the created file in the `./Redfish_Simulator/api_emulator/redfish` directory
2. Describe the response JSON file and the content of the API
    * Delete unnecessary processes such as PATCH or DELETE
    * Refer to HowTo - Develop Redfish Emulator 1.1a for details
3. Edit Redfish_Simulator/emulator.py for resources on the service route

### Device Definition Files
File name
* simulatorDeviceList.json

A file to set the type, number, and initial values for some properties of a device.  
  * Do not create types ignored by the Redfish Interface Emulator during [Device Creation](#creating-devices)
    * Do not conduct "Add a new device type and create a device"
  * List the properties used by both OOB and FM within this definition file
    * Refer to the default device definition file for which properties to record
* Place the device definition file in the directory with this file
* Must abide by the following rules
   * Specify a unique string for deviceID
   * At least one linked built-in memory and built-in storage is needed for the CPU
   * A link with the CPU is required for the graphics controller
  
Example of writing a device definition file
``` ex.
        "cpu": [
            {
              "deviceID": "0001",
              "serialNumber": "PROCESSOR1",
              "model": "cpu_1",
              "manufacturer": "Intel(R) Corporation",
              "link": [
                {
                  "deviceID": "1001"
                }
              ]
            }
        ]
```

### Setting Return Data Values
Configuration file name  
* Redfish_Simulator/infragen/test_device_parameter.json

A file to set the initial values handled by the Redfish Interface Emulator alone.  
Associate the parameters and values to be specified with the deviceID and configure.  

Example of writing the configuration file
``` ex.
　      "0001": {
          "totalEnabledCores": 4,
          "operatingSpeedMHz": 3200
        }
```

#### Settable Return Data Values
■ Processor
| Parameter | Target Schema | Target Property Name | Description |
|:--|:--|:--|:--|
| totalEnabledCores | Processor | TotalEnabledCores | Total number of enabled cores in this processor |
| operatingSpeedMHz | Processor | OperatingSpeedMHz | Clock speed (MHz) during processor operation |
| totalCores | Processor | TotalCores | Total number of cores included in this processor |
| capacityMiB | Processor | ProcessorMemory.CapacityMiB | Memory capacity (MiB) installed in or integrated into this processor. |
| state | Processor | Status.State | Resource State |
| health | Processor | Status.Health | Health state of the resource |
| socketNum | Processor | Socket | Number of processors |
| processorArchitecture | Processor | ProcessorArchitecture | Processor architecture |
| sensingInterval | Sensor | SensingInterval | Time interval (seconds) between sensor readings |

■ Memory
| Parameter | Target Schema | Target Property Name | Description |
|:--|:--|:--|:--|
| capacityMiB | Memory | CapacityMiB | Memory capacity (MiB) |
| OperatingSpeedMHz | Memory | OperatingSpeedMHz | Memory operating speed (MHz) |
| state | Memory | Status.State | Resource State |
| health | Memory | Status.Health | Health state of the resource |
| sensingInterval | Sensor | SensingInterval | Time interval (seconds) between sensor readings |

■ Storage
| Parameter | Target Schema | Target Property Name | Description |
|:--|:--|:--|:--|
| volumeCapacityBytes | Volume | CapacityBytes | Size of this volume in bytes |
| driveCapableSpeedGbs | Drive | CapableSpeedGbs | Speed at which this drive communicates with storage in ideal conditions |
| driveCapacityBytes | Drive | CapacityBytes | Size of this drive in bytes |
| state | Drive | Status.State | Resource State |
| health | Drive | Status.Health | Health state of the resource |
| sensingInterval | Sensor | SensingInterval | Time interval (seconds) between sensor readings |

■ NIC
| Parameter | Target Schema | Target Property Name | Description |
|:--|:--|:--|:--|
| bitRate | SerialInterface | BitRate | Rate of data flow (bit/s) (used to calculate metrics) |
| maxSpeedGbps | Port | MaxSpeedGbps | Maximum speed of the port (Gbit/s) |
| state | NetworkAdapter | Status.State | Resource State |
| health | NetworkAdapter | Status.Health | Health state of the resource |
| sensingInterval | Sensor | SensingInterval | Time interval (seconds) between sensor readings |

■ Graphics Controller
| Parameter | Target Schema | Target Property Name | Description |
|:--|:--|:--|:--|
| state | GraphicController | Status.State | Resource State |
| health | GraphicController | Status.Health | Health state of the resource |

## Usage

### Available Resources
If the Redfish Interface Emulator can respond, it returns HTTP status code 200 and JSON data for the methods below.

### Retrieve
Get the information of the specified device.
1. Retrieve the manager information list and get manager information  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Managers`  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Managers/BMC-1`
2. Depending on the device you want to retrieve, get information from ComputerSystem or Chassis  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Systems/System-1`  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Chassis/Chassis-1`
1. Get a list of devices for the target device type  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Systems/System-1/Processors`
2. Get the target device information  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Systems/System-1/Processors/PROC-0001`

The schemas that can be obtained by GET processing are as follows.  
※ The XXXX part is the ID set in the device definition file.

| Schema Name | URL | ID |
|:--|:--|:--|
| Manager | /redfish/v1/Managers/{ManagerId} | BMC-1 |
| ComputerSystem | /redfish/v1/Systems/{ComputerSystemId} | System-x (x is set from 1 to the number of CPUs depending on the CPU count) |
| Chassis | /redfish/v1/Chassis/{ChassisId} | Chassis-1 |
| Processor | /redfish/v1/Systems/{ComputerSystemId}/Processors/{ProcessorId} | PROC-XXXX |
| Memory | /redfish/v1/Chassis/{ChassisId}/Memory/{MemoryId} | MEM-XXXX |
| Drive | /redfish/v1/Chassis/{ChassisId}/Drives/{DriveId} | DRI-XXXX |
| Storage | /redfish/v1/Storage/{StorageId} | STR-XXXX |
| StorageController | /redfish/v1/Storage/{StorageId}/Controllers/{ControllerId} | STRCTR-XXXX |
| Volume | /redfish/v1/Storage/{StorageId}/Volumes/{VolumeId} | VOL-XXXX |
| NetworkAdapter | /redfish/v1/Chassis/{ChassisId}/NetworkAdapters/{NetworkAdapterId} | NIC-XXXX |
| NetworkDeviceFunction | /redfish/v1/Chassis/{ChassisId}/NetworkAdapters/{NetworkAdapterId}/NetworkDeviceFunctions/{NetworkDeviceFunctionId} | NICF-XXXX |
| NetworkInterfaces | /redfish/v1/Systems/{ComputerSystemId}/NetworkInterfaces/{NetworkInterfaceId} | NETI-XXXX |
| Port | /redfish/v1/Chassis/{ChassisId}/NetworkAdapters/{NetworkAdapterId}/Ports/{PortId} | PORT-XXXX |
| PCIeDevice | /redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId} | PCIe-XXXX |
| PCIeFunction | /redfish/v1/Chassis/{ChassisId}/PCIeDevices/{PCIeDeviceId}/PCIeFunctions/{PCIeFunctionId} | PCIeF-XXXX |
| SerialInterfaces | /redfish/v1/Managers/{ManagerId}/SerialInterfaces/{SerialInterfaceId} | SI-XXXX |
| ProcessorMetrics | /redfish/v1/Systems/{ComputerSystemId}/Processors/{ProcessorId}/ProcessorMetrics | - |
| MemoryMetrics | /redfish/v1/Chassis/{ChassisId}/Memory/{MemoryId}/MemoryMetrics | - |
| EnvironmentMetrics | /redfish/v1/Systems/{ComputerSystemId}/Processors/{ProcessorId}/EnvironmentMetrics<br>/redfish/v1/Chassis/{ChassisId}/Memory/{MemoryId}/EnvironmentMetrics<br>/redfish/v1/Chassis/{ChassisId}/Drives/{DriveId}/EnvironmentMetrics<br>/redfish/v1/Chassis/{ChassisId}/NetworkAdapters/{NetworkAdapterId}/EnvironmentMetrics | - |
| Sensor | /redfish/v1/Chassis/{ChassisId}/Sensors/{SensorId} | SENS-PROC-XXXX,SENS-MEM-XXXX,SENS-DRI-XXXX,SENS-STOC-XXXX,SENS-NIC-XXXX |
| GraphicsController | /redfish/v1/Systems/{ComputerSystemId}/GraphicsControllers/{ControllerId} | GC-XXXX |
| ResourceBlock | /redfish/v1/CompositionService/ResourceBlocks/{BlockId} | ComputeBlock-x,DeviceBlock-x (x is a unique integer) |
| ResourceZone | /redfish/v1/CompositionService/ResourceZones/{ZoneId} | GlobalZone |
| Fabric | /redfish/v1/Fabrics/{FabricId} | CXL |
| Switch | /redfish/v1/Fabrics/{FabricId}/Switches/{SwitchId} | SWITCH-XXXX |

Details of the returned information are as follows.  
※ Only some major information is provided below.

| Schema Name | Property | Value | Remarks |
| --- | --- | --- | --- |
| Processor, Memory, Drive, NetworkAdapter | PowerState | On<br>Off | The status indicating the power state. Currently, only ON/OFF is set. ON/OFF changes through power operations for the target device. If POWER_LINK setting is true, the power state of the embedded device associated with the CPU is linked. |
| Processor, Memory, Drive, NetworkAdapter | Status.State | Enabled | The status indicating if the resource is enabled. Currently, only Enabled is set. |

### Operations
The following Actions can be operated by POST processing.

#### Power Operations
Change the power state of the specified device.  
Upon successful operation, the PowerState property changes.

The device types capable of power operations are as follows.

| Device Type | Operating Schema |
| --- | --- |
| CPU | Processor |
| GPU | Processor |
| Memory | Memory |
| Storage | Drive |

##### Executing Power Operations

1. Retrieve the information of the target device you want to perform power operations on  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Systems/System-1/Processors/PROC-0001`
2. Confirm the existence of the Actions property and obtain the URI specified by the target property of `[Operating Schema].Reset` in Actions
   * Example of Actions property description  
    ``` ex.
          "Actions": {
            "#Processor.Reset": {
              "target": "/redfish/v1/Systems/System-1/Processors/PROC-0001/Actions/Processor.Reset",
              "ResetType@Redfish.AllowableValues": [
                "On",
                "ForceOff",
                "GracefulShutdown",
                "GracefulRestart",
                "ForceRestart",
                "ForceOn"
              ]
            }
          }
    ```
3. Execute POST processing for the obtained URL
   * Specify ResetType in the data  
    `ex. $ curl -X POST -H "Content-Type: application/json" -d '{"ResetType": "On"}' http://127.0.0.0:5000/redfish/v1/Systems/System-1/Processors/PROC-0001`
    * ResetTypes that can be specified
      | ResetType | Operation |
      | --- | --- |
      | On | Power On (Normal) |
      | ForceOn | Power On (Force) |
      | GracefulShutdown | Power Off (Normal) |
      | ForceOff | Power Off (Force) |
      | GracefulRestart | Reset (Normal) |
      | ForceRestart | Reset (Force) |

* The following restrictions exist
  * The number of devices whose power state can be changed in one request varies depending on the setting value of POWER_LINK
    * true: If the CPU is specified, the power state of the devices embedded in it is also changed
    * false: Only the device specified in the request is targeted. Devices linked to the specified device are excluded
  * The power state is changed at the timing when the power operation is performed (there is no status such as changing)

#### Load State Operations
Change the load state of the specified device.  
If the operation is successful, a random value within the range corresponding to the load state is set.

The device types capable of load state operations are as follows.
| Device Type | Operating Schema |
| --- | --- |
| CPU | Processor |
| GPU | Processor |
| Memory | Memory |
| Storage | Drive |
| NIC | NetworkAdapter |

##### Executing Load State Operations

1. Retrieve the information of the target device you want to perform load state operations on  
    `ex. $ curl http://127.0.0.0:5000/redfish/v1/Systems/System-1/Processors/PROC-0001`
2. Confirm the existence of the Actions property and obtain the URI specified by the target property of `[Operating Schema].MetricState` in Actions
   * As it is a proprietary Action operation, it is defined within the Oem schema
   * Example of Actions property description
    ``` ex.
          "Actions": {
            "Oem": {
              "#Processor.MetricState": {
                "target": "/redfish/v1/Systems/System-1/Processors/PROC-0001/Actions/Processor.MetricState",
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
    ```
3. Execute POST processing for the obtained URL
  * Specify StateType in the data  
    `ex. $ curl -X POST -H "Content-Type: application/json" -d '{"StateType": "off"}' http://127.0.0.0:5000/redfish/v1/Systems/System-1/Processors/PROC-0001`
    * StateTypes that can be specified
      | StateType | State | Remarks |
      | --- | --- | --- |
      | off | Power Off | Reproduces the state of the device when the power is off. It can be specified even when the actual power is on |
      | steady | Normal | Reproduces the state of the device during normal circumstances |
      | low | Low Load | Reproduces the state of the device under low load |
      | high | High Load | Reproduces the state of the device under high load |
      | action | During Operation | Reproduces the state during power operations, etc. |

* The following restrictions exist
  * In one request, only the specified device will have its load state changed
    * Devices linked to the specified device are excluded
  * When a power operation is performed, the load state becomes "action" and is maintained for 5 seconds. It then transitions to "off" or "steady" status based on the power state after the power operation.

* Parameters that change depending on the load state are as follows
  | Schema | Parameter | Description |
  | --- | --- | --- |
  | ProcessorMetrics | BandwidthPercent | Bandwidth usage rate of the processor |
  | MemoryMetrics | BandwidthPercent | Bandwidth usage rate of memory |
  | EnvironmentMetrics | EnergyJoules.Reading | Energy consumption |
  | Volume | RemainingCapacityPercent | Capacity remaining on this volume |
  | NetworkAdapterMetrics | HostBusRXPercent | RX usage rate of the host bus such as PCIe |
  | NetworkAdapterMetrics | HostBusTXPercent | TX usage rate of the host bus such as PCIe |

* The range of values that change according to the load state is as follows. Values are set according to the specification
  | Load State | Specification | Value (%) | Value (J) | 
  | --- | --- | --- | --- |
  | Power Off | Low | 0 | 0 |
  | Power Off | Middle | 0 | 0 |
  | Power Off | High | 0 | 0 |
  | Normal | Low | 0～40 | 0～10 |
  | Normal | Middle | 0～20 | 0～20 |
  | Normal | High | 0～10 | 0～30 |
  | Low Load | Low | 40～60 | 10～30 |
  | Low Load | Middle | 20～40 | 20～40 |
  | Low Load | High | 10～30 | 40～60 |
  | High Load | Low | 80～100 | 40～60 |
  | High Load | Middle | 70～90 | 70～90 |
  | High Load | High | 60～80 | 90～110 |
  | Operation | Low | 60～80 | 30～50 |
  | Operation | Middle | 50～70 | 50～70 |
  | Operation | High | 40～60 | 70～90 |

  ※ The unit of values is %, and the unit of energy consumption is J.

### Supported Devices
| Device Type | deviceType | Device ID |
|:--|:--|:--|
| CPU | CPU | 000001～000010 |
| GPU | GPU | Built-in GPU：500001～500010<br>External GPU：550001～550010 |
| Memory | memory | Built-in Memory：100001～100010<br>External Memory：150001～150010 |
| Storage | storage | Built-in Storage：200001～200010<br>External Storage：250001～250010 |
| NIC | networkInterface | Built-in NIC：300001～300010<br>External NIC：350001～350010 |
| Graphic Controller | graphicController | 600001～ |

* The first byte from the left in the Device ID is assigned to the device type.  
* The second byte from the left in the Device ID indicates the device location: "0" means a built-in device, and any other value means an external device.  
* The third byte from the left and onwards in the Device ID are assigned as a consecutive device number (the lower 4 digits).  
  * The current maximum value has been changed to 9999. 

## File List
※ Only major files are listed

```
 simulatorDeviceList.json ... Device definition file
 Redfish_Simulator ... Project Root
　├ api_emulator
　│　├ __init__.py
　│　├ redfish
　│　│　├ static ... Static mockup file
　│　│　├ templates ... Response template file
　│　│　│　├ AccountService.py ... Account Service
　│　│　│　├ Chassis.py ... Chassis
　│　│　│　├ ComputerSystem.py ... Computer System
　│　│　│　├ CXLLogicalDevice.py ... CXL Logical Device within PCIe Device
　│　│　│　├ Drive.py ... Drive
　│　│　│　├ DriveMetrics.py ... Drive Metrics
　│　│　│　├ EnvironmentMetrics.py ... Device Environment Metrics
　│　│　│　├ ethernetinterface.py ... Ethernet Interface
　│　│　│　├ FabricAdapter.py ... Fabric Adapter
　│　│　│　├ fabric.py ... Fabric
　│　│　│　├ GraphicsController.py ... Graphic Controller
　│　│　│　├ Manager.py ... Manager
　│　│　│　├ ManagerAccount.py ... Manager Account
　│　│　│　├ memory.py ... Memory
　│　│　│　├ MemoryMetrics.py ... Memory Metrics
　│　│　│　├ NetworkAdapter.py ... Network Adapter
　│　│　│　├ NetworkAdapterMetrics.py ... Network Adapter Metrics
　│　│　│　├ NetworkDeviceFunction.py ... Logical interface that Network Adapter exposes
　│　│　│　├ NetworkDeviceFunctionMetrics.py ... Network Device Function Metrics
　│　│　│　├ NetworkInterface.py ... Network Interface
　│　│　│　├ PCIeDevice.py ... PCIe Device
　│　│　│　├ PCIeFunction.py ... PCIe Function
　│　│　│　├ Port.py ... Port
　│　│　│　├ PowerSubsystem.py ... Power Subsystem of Chassis
　│　│　│　├ PowerSupply.py ... Power Supply Unit
　│　│　│　├ Processor.py ... Processor
　│　│　│　├ ProcessorMetrics.py ... Processor Metrics
　│　│　│　├ ResourceBlock.py ... Resource Block
　│　│　│　├ ResourceZone.py ... Resource Zone
　│　│　│　├ Role.py ... Role
　│　│　│　├ Sensor.py ... Sensor
　│　│　│　├ SerialInterface.py ... Serial Interface
　│　│　│　├ SessionService.py ... Session Service
　│　│　│　├ Storage.py ... Storage
　│　│　│　├ StorageController.py ... Storage Controller
　│　│　│　├ StorageControllerMetrics.py ... Storage Controller Metrics
　│　│　│　├ switch.py ... Switch
　│　│　│　├ VirtualMedia.py ... Virtual Media
　│　│　│　├ Volume.py ... Volume
　│　│　│　└ VolumeMetrics.py ... Volume Metrics
　│　│　├ account_service_api.py ... API configuration for Account Service
　│　│　├ Chassis_api.py ... API configuration for Chassis
　│　│　├ ComputerSystem_api.py ... API configuration for Computer Systems
　│　│　├ cxl_logical_device_api.py ... API configuration for CXL Logical Device
　│　│　├ drive_api.py ... API configuration for Drive
　│　│　├ drive_metrics_api.py ... API configuration for Drive Metrics
　│　│　├ environment_metrics_api.py ... API configuration for Device Environment Metrics
　│　│　├ ethernetinterface.py ... API configuration for Ethernet Interface
　│　│　├ fabric_adapter_api.py ... API configuration for Fabric Adapter
　│　│　├ fabric_api.py ... API configuration for Fabric
　│　│　├ graphics_controller_api.py ... API configuration for Graphic Controller
　│　│　├ manager_account_api.py ... API configuration for Manager Account
　│　│　├ Manager_api.py ... API configuration for Manager
　│　│　├ memory_api.py ... API configuration for Memory
　│　│　├ memory_metrics_api.py ... API configuration for Memory Metrics
　│　│　├ metric_state_api.py ... API configuration for Metric Value Management
　│　│　├ network_adapter_api.py ... API configuration for Network Adapter
　│　│　├ network_adapter_metrics_api.py ... API configuration for Network Adapter Metrics
　│　│　├ network_device_function_api.py ... API configuration for Network Device Function
　│　│　├ network_device_function_metrics_api.py ... API configuration for Network Device Function Metrics
　│　│　├ network_interface_api.py ... API configuration for Network Interface
　│　│　├ pcie_device_api.py ... API configuration for PCIe Device
　│　│　├ pcie_function_api.py ... API configuration for PCIe Function
　│　│　├ port_api.py ... API configuration for Port
　│　│　├ processor_api.py ... API configuration for Processor
　│　│　├ processor_metrics_api.py ... API configuration for Processor Metrics
　│　│　├ ResetAction_api.py ... API configuration for Power Operations
　│　│　├ ResourceBlock_api.py ... API configuration for Resource Block
　│　│　├ ResourceZone_api.py ... API configuration for Resource Zone
　│　│　├ resourceobject.py ... API configuration for processors, memory, drives, ethernet interfaces belonging to Resource Block
　│　│　├ role_api.py ... API configuration for Role
　│　│　├ sensor.py ... API configuration for Sensor
　│　│　├ serial_interface.py ... API configuration for Sensor
　│　│　├ storage_api.py ... API configuration for Storage
　│　│　├ storage_controller_api.py ... API configuration for Storage Controller
　│　│　├ storage_controller_metrics_api.py ... API configuration for Storage Controller Metrics
　│　│　├ switch_api.py ... API configuration for Switch
　│　│　├ virtual_media_api.py ... API configuration for Virtual Media
　│　│　├ volume_api.py ... API configuration for Volume
　│　│　└ volume_metrics_api.py ... API configuration for Volume Metrics
　│　├ resource_manager.py ... Resource root configuration
  ├ codegen
  │　├ codegen_api.py ... For writing API files
  │　├ codegen_template.py ... For writing template files
  │　└ index.json ... Template for template files
  ├ doc
  │　├ HowTo - Develop Redfish Emulator 1.1a.pdf
  │　└ HowTo - Use Redfish Emulator - v0.3.4.pdf
  ├ infragen
  │　├ populate.py ... Create Devices
  │　├ populate-config.json ... Default device creation file
  │　└ test_device_parameter.json ... File for initial value setting of device parameters
  ├ packageSets
  │　└ Env-Local-Python3.9.1_requirements.txt ... Package list
  ├ emulator-config_device_populate.json ... Default configuration file
  ├ emulator-config_dynamic_populate.json ... Configuration file for using the device definition file
  └  emulator.py ... Root file
```
