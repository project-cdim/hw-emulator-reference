# Copyright Notice:
# Copyright 2025 NEC Corporation All rights reserved.
# License: BSD 3-Clause License. For full text see link: https://github.com/project-cdim/hw-emulator-reference/LICENSE


import copy

_TEMPLATE = {
    "@odata.type": "#NetworkDeviceFunction.v1_9_2.NetworkDeviceFunction",
    "Id": "{ndf_id}",
    "Name": "Network Device Function View",
    "NetDevFuncType": "Ethernet",
    "DeviceEnabled": True,
    "NetDevFuncCapabilities": ["Ethernet", "FibreChannel"],
    "Status": {
        "State": "Enabled",
        "Health": "OK",
    },
    "Ethernet": {
        "PermanentMACAddress": "00:0C:29:9A:98:ED",
        "MACAddress": "00:0C:29:9A:98:ED",
        "MTUSize": 1500,
        "VLAN": {"VLANEnable": True, "VLANId": 101},
        "MTUSizeMaximum": 5000,
        "EthernetInterfaces": {
            "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{ndf_id}/EthernetInterfaces"
        },
    },
    "iSCSIBoot": {
        "IPAddressType": "IPv4",
        "InitiatorIPAddress": "16.0.11.6",
        "InitiatorName": "iqn.2005-03.com.acme:database-server",
        "InitiatorDefaultGateway": "169.0.16.1",
        "InitiatorNetmask": "255.255.252.0",
        "TargetInfoViaDHCP": False,
        "PrimaryTargetName": "iqn.2005-03.com.acme:image-server",
        "PrimaryTargetIPAddress": "169.0.15.1",
        "PrimaryTargetTCPPort": 3260,
        "PrimaryLUN": 5,
        "PrimaryVLANEnable": True,
        "PrimaryVLANId": 1001,
        "PrimaryDNS": "16.0.10.21",
        "SecondaryTargetName": "iqn.2005-03.com.acme:image-server",
        "SecondaryTargetIPAddress": "16.0.11.5",
        "SecondaryTargetTCPPort": 3260,
        "SecondaryLUN": 5,
        "SecondaryVLANEnable": True,
        "SecondaryVLANId": 1002,
        "SecondaryDNS": "169.0.10.22",
        "IPMaskDNSViaDHCP": False,
        "RouterAdvertisementEnabled": False,
        "AuthenticationMethod": "CHAP",
        "CHAPUsername": "yosemite",
        "CHAPSecret": "usrpasswd",
        "MutualCHAPUsername": "yosemite",
        "MutualCHAPSecret": "usrpasswd",
    },
    "FibreChannel": {
        "PermanentWWPN": "10:00:B0:5A:DD:BB:74:E0",
        "PermanentWWNN": "10:00:B0:5A:DD:BB:A1:B3",
        "WWPN": "10:00:B0:5A:DD:BB:74:E0",
        "WWNN": "10:00:B0:5A:DD:C4:D3:BB",
        "WWNSource": "ConfiguredLocally",
        "FCoELocalVLANId": 1001,
        "AllowFIPVLANDiscovery": True,
        "FCoEActiveVLANId": 2001,
        "BootTargets": [
            {"WWPN": "10:00:B0:5A:DD:BB:74:FA", "LUNID": "3", "BootPriority": 0}
        ],
    },
    "Limits": [
        {
            "BurstBytesPerSecond": 80,
            "BurstPacketsPerSecond": 12,
            "Direction": "Ingress",
            "SustainedBytesPerSecond": 20,
            "SustainedPacketsPerSecond": 10,
        }
    ],
    "AssignablePhysicalNetworkPorts": [],
    "BootMode": "Disabled",
    "VirtualFunctionsEnabled": True,
    "MaxVirtualFunctions": 16,
    "Metrics": {
        "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{ndf_id}/Metrics"
    },
    "Links": {
        "PCIeFunction": {
            "@odata.id": "/redfish/v1/Systems/1/PCIeDevices/NIC/PCIeFunctions/{pcie_f_id}"
        }
    },
    "@odata.id": "/redfish/v1/Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{ndf_id}",
}


def format_NetworkDeviceFunction_template(**kwargs):
    c = copy.deepcopy(_TEMPLATE)

    c["Id"] = c["Id"].format(**kwargs)
    c["@odata.id"] = c["@odata.id"].format(**kwargs)

    c["Ethernet"]["EthernetInterfaces"]["@odata.id"] = c["Ethernet"][
        "EthernetInterfaces"
    ]["@odata.id"].format(**kwargs)
    c["Links"]["PCIeFunction"]["@odata.id"] = c["Links"]["PCIeFunction"][
        "@odata.id"
    ].format(**kwargs)
    c["Metrics"]["@odata.id"] = c["Metrics"]["@odata.id"].format(**kwargs)

    if "portNAList" in kwargs:
        port = [
            {
                "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{na_id}/NetworkDeviceFunctions/{ndf_id}/Ports/{linkPort}".format(
                    rb=kwargs["rb"],
                    chassis_id=kwargs["chassis_id"],
                    na_id=kwargs["na_id"],
                    ndf_id=kwargs["ndf_id"],
                    linkPort=x,
                )
            }
            for x in kwargs["portNAList"]
        ]
        c["AssignablePhysicalNetworkPorts"] = port

    if "mac" in kwargs:
        c["Ethernet"]["PermanentMACAddress"] = "{mac}".format(**kwargs)
        c["Ethernet"]["MACAddress"] = "{mac}".format(**kwargs)
    return c
