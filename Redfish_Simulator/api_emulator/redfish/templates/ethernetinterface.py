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
from random import randint

_TEMPLATE = {
    "@odata.context": "{rb}$metadata#EthernetInterface.EthernetInterface",
    "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{nic_id}/NetworkDeviceFunctions/{ndf_id}/EthernetInterfaces/{ei_id}",
    "@odata.type": "#EthernetInterface.v1_12_3.EthernetInterface",
    "AutoNeg": True,
    "Description": "Ethernet Interface",
    "FQDN": "default.local",
    "FullDuplex": True,
    "HostName": "default",
    "IPv4Addresses": [
        {
            "Address": "",
            "AddressOrigin": "IPv4LinkLocal",
            "Gateway": "0.0.0.0",
            "SubnetMask": "255.255.0.0",
        }
    ],
    "IPv6Addresses": [
        {
            "Address": "fe80::1ec1:deff:fe6f:1e24",
            "PrefixLength": 64,
            "AddressOrigin": "SLAAC",
            "AddressState": "Preferred",
        }
    ],
    "Id": "{ei_id}",
    "InterfaceEnabled": True,
    "LinkStatus": "LinkUp",
    "EthernetInterfaceType": "Physical",
    "Links": {
        "Chassis": {"@odata.id": "{rb}Chassis/{chassis_id}"},
        "NetworkDeviceFunctions": [],
        "Ports": [],
    },
    "MACAddress": "",
    "MTUSize": 1500,
    "Name": "Ethernet Interface",
    "NameServers": ["8.8.8.8"],
    "PermanentMACAddress": "':'.join(['%02x'%randint(0,255) for x in range(6)])",
    "SpeedMbps": 10000,
    "Status": {"Health": "OK", "State": "Enabled"},
    "VLAN": {"VLANId": 0},
}


def format_nic_template(**kwargs):
    """
    Format the processor template -- returns the template
    """
    # params:
    defaults = {
        "rb": "/redfish/v1/",
        "suffix": "Systems",
        "speedmbps": 10000,
        "vlanid": 0,
    }

    defaults.update(kwargs)

    c = deepcopy(_TEMPLATE)
    c["@odata.context"] = c["@odata.context"].format(**defaults)
    c["@odata.id"] = c["@odata.id"].format(**defaults)
    c["Id"] = c["Id"].format(**defaults)
    c["Links"]["Chassis"]["@odata.id"] = c["Links"]["Chassis"]["@odata.id"].format(
        **defaults
    )
    c["SpeedMbps"] = defaults["speedmbps"]
    for ip in c["IPv4Addresses"]:
        ip["Address"] = "172.16.{ip1}.{ip2}".format(
            ip1=(randint(1, 255)), ip2=(randint(1, 255))
        )
    if "mac" in kwargs:
        c["PermanentMACAddress"] = "{mac}".format(**kwargs)
        c["MACAddress"] = "{mac}".format(**kwargs)
    c["VLAN"]["VLANId"] = defaults["vlanid"]
    ndf = [
        {
            "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{nic_id}/NetworkDeviceFunctions/{linkNdf}".format(
                rb=defaults["rb"],
                chassis_id=defaults["chassis_id"],
                nic_id=defaults["nic_id"],
                linkNdf=x,
            )
        }
        for x in defaults["ndfList"]
    ]
    c["Links"]["NetworkDeviceFunctions"] = ndf
    port = [
        {
            "@odata.id": "{rb}Chassis/{chassis_id}/NetworkAdapters/{nic_id}/Ports/{linkPort}".format(
                rb=defaults["rb"],
                chassis_id=defaults["chassis_id"],
                nic_id=defaults["nic_id"],
                linkPort=x,
            )
        }
        for x in defaults["portNAList"]
    ]
    c["Links"]["Ports"] = port
    return c
