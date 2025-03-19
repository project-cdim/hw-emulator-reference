#!/usr/bin/env python2
#
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

# Python unittests for the Redfish Interface Emulator

import argparse
import json
import logging
import os
import sys
import unittest
import requests

class TestRedfishEmulator(unittest.TestCase):
    MODE=None
    #global address
    CONFIG = 'emulator-config_device_populate.json'
    with open(CONFIG, 'r') as f:
        config = json.load(f)

    MODE = config['MODE']
    address = sys.argv[2]
    base_url = 'http://{0}/redfish/v1/'.format(address)

    log_file = None
    log_fmt = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)-8s: %(message)s',
        datefmt='%H:%M:%S %m-%d-%y')

    devconfig = {}
    file_path = config['POPULATE']
    if os.path.isfile(file_path):
        with open(file_path, encoding='utf-8') as open_file:
            devconfig = json.load(open_file)
    uspnum = len(devconfig['cpu'])
    dspnum = (sum(len(v) for k, v in devconfig.items() if k in
                  ['memory', 'storage', 'networkInterface', 'gpu']) -
             (sum(len(c['link']) for c in devconfig['cpu']) - len(devconfig['graphicController'])))
    usprange = range(1, uspnum + 1)
    dsprange = range(uspnum + 1, uspnum + dspnum + 1)
    targetdevice = {x: False for x in ['cpu', 'memory', 'storage', 'networkInterface', 'gpu']}

    def assert_status(self, r, expected, logger):
        try:
            assert r.status_code == expected, 'Request failed: See log "{0}"'.format(self.log_file)
        except AssertionError:
            # Catching assertion to log the response from the REST server
            # then re-raising the exception
            logger.error('Request Failed:\n' + r.text)
            raise

    def url(self, url):
        """
        Appends the base_url to the beginning of the given URL
        """
        return self.base_url + url

    def odata_id_url(self, url):
        """
        Appends http://<address>/ to the given url
        """
        return 'http://{0}{1}'.format(self.address, url)

    def get(self, logger, url, getting):
        """
        Helper function to do a get request and log it to the specified logger
        """
        r = requests.get(url)
        self.assert_status(r, 200, logger)
        logger.info('PASS: GET of {0} successful (response below)\n {1}'.format(getting, r.text))

    def get_logger(self, name, log_file):
        """
        Helper function to create a logger object
        """
        logger = logging.getLogger(name)
        fh = logging.FileHandler(log_file, mode='w')
        fh.setFormatter(self.log_fmt)
        logger.setLevel(logging.INFO)
        logger.addHandler(fh)
        return logger

    def do_gets(self, params, logger):
        """
        Helper function to call the get() member function with the given params.
        Params must be a list of parameters to give to the get()method.
        """
        for param in params:
            self.get(logger, *param)

    def test_redfish_get_collections(self):
        """
        Unit test to get resource of a system instance

        NOTE: The emulator must be in the redfish mode to run this test
        """
        self.log_file = 'test-get-collection.log'
        logger = self.get_logger('test-get-collection', self.log_file)

        # Parameters for the get requests
        params = [
            (self.url('Chassis'), 'ChassiCollection'),
            (self.url('Chassis/Chassis-1'), 'Chassis instance'),
            (self.url('Chassis/Chassis-1/PCIeDevices'), 'PCIeDevicesCollection'),
            (self.url('Chassis/Chassis-1/FabricAdapters'), 'FabricAdaptersCollection'),

            (self.url('Systems'), 'SystemCollection'),
            (self.url('CompositionService'), 'CompositionService'),
            (self.url('CompositionService/ResourceBlocks'), 'ResourceBlockCollection'),
            (self.url('CompositionService/ResourceZones'), 'ResourceZoneCollection'),
            (self.url('CompositionService/ResourceZones/GlobalZone'), 'ResourceZone member')]

        self.do_gets(params, logger)

    def _get_device_from_config(self, devid: str, devtype=None) -> dict | None:
        for key, value in self.devconfig.items():
            if devtype and devtype != key:
                continue
            for dev in value:
                if dev['deviceID'] == devid:
                    return dev
        return None

    def _get_and_response(self, logger, url: str, fullpath: bool = False) -> dict:
        if fullpath:
            getting = self.odata_id_url(url)
        else:
            getting = self.url(url)
        resp = requests.get(getting, timeout=1.0)
        self.assert_status(resp, 200, logger)
        data = json.loads(resp.text)
        logger.info(f'PASS: GET of {getting} successful (response below)\n{data}')
        return data

    def _is_same_hexadigit(self, svalue1, svalue2):
        try:
            _ivalue1 = int(svalue1, base=16)
            _ivalue2 = int(svalue2, base=16)
        except (TypeError, ValueError):
            return False
        return _ivalue1 == _ivalue2

    def _check_system_link(self, data: dict, logger):
        """Check from ResourceBlock data((Required features for FM plugin)"""
        fullurl = data.get('@odata.id')
        assert fullurl, f'invalid format {data}. See log {self.log_file}'
        syslink = [x.get('@odata.id') for x in data.get('Links', {}).get('ComputerSystems', [])]
        assert len(syslink) == 1, f'{fullurl} invalid system link: {syslink}\n{data}'
        linkname = fullurl.replace('CompositionService/ResourceBlocks/ComputeBlock', 'Systems/System')
        assert linkname == syslink[0], f'{syslink[0]} != {linkname} create by {fullurl}'
        system = self._get_and_response(logger, syslink[0], True)
        blocks = [x.get('@odata.id') for x in system.get('Links', {}).get('ResourceBlocks', [])]
        assert fullurl in blocks, f'{syslink[0]} invalid resource block {blocks}\n{system}'

    def _check_cpu_device(self, data: dict):
        """Check CPU device information from Processor data (Required features for FM plugin)"""
        fullurl = data.get('@odata.id')
        assert fullurl, f'invalid format {data}. See log {self.log_file}'
        devid = fullurl.split('-')[-1]
        device = self._get_device_from_config(devid, 'cpu')
        assert device, f'{devid} config data not found. See log {self.log_file}'
        assert device['manufacturer'] == data['Manufacturer'], f'{device} manufacturer != {data}'
        assert device['model'] == data['Model'], f'{device} model != {data}'
        assert device['serialNumber'] == data['SerialNumber'], f'{device} model != {data}'

    def _check_pcie_device(self, devid, rtype, logger):
        """Check to get PCIeDevice/PCIeFunction from device id (Required features for FM plugin)"""
        device = self._get_device_from_config(devid, rtype)
        assert device, f'{devid} not in config file {self.devconfig}'

        if rtype == 'memory':
            return

        url = f'Chassis/Chassis-1/PCIeDevices/PCIe-{devid}'
        data = self._get_and_response(logger, url)
        assert self._is_same_hexadigit(device['PCIeDeviceSerialNumber'], data['SerialNumber']),\
            f'{device} serialnumber != {data}'

        url = f'Chassis/Chassis-1/PCIeDevices/PCIe-{devid}/PCIeFunctions/PCIeF-{devid}'
        data = self._get_and_response(logger, url)
        assert self._is_same_hexadigit(device['PCIeDeviceID'], data['DeviceId']), f'{device} deviceid != {data}'
        assert self._is_same_hexadigit(device['PCIeVendorID'], data['VendorId']), f'{device} vendorid != {data}'

    def _check_resource_zone(self, rbdata, logger):
        """Check ResourceBlock has 1 ResourceZone (Required features for FM plugin)"""
        url = rbdata.get('@odata.id')
        zones = rbdata.get('Links', {}).get('Zones', [])
        for zone in zones:
            path = zone.get('@odata.id')
            assert path is not None, f'{url} zone {zones} invalid. See log {self.log_file}'
            zone_data = self._get_and_response(logger, path, True)
            blocks = [x.get('@odata.id') for x in zone_data.get('Links', {}).get('ResourceBlocks', [])]
            assert url in blocks, f'{url} not in {path}. See log {self.log_file}'
        assert 1 == len(zones)

    def _check_resource_block_target_device(self, url, num, logger):
        """Check ResourceBlock has num device (Required features for FM plugin)"""
        data = self._get_and_response(logger, url)

        isusp = False
        if url.split('/')[-1].startswith('ComputeBlock-'):
            isusp = True
            self._check_system_link(data, logger)
        self._check_resource_zone(data, logger)
        data = self._get_and_response(logger, url)

        cnt = 0
        cpu = 0
        devtypes = {'Processors': 'gpu', 'Memory': 'memory', 'Drives': 'storage',
                    'EthernetInterfaces': 'networkInterface'}
        for rtype, devtype in devtypes.items():
            for odata in data.get(rtype, []):
                path = odata.get('@odata.id')
                assert path is not None, f'{url} device {rtype} not found. See log {self.log_file}'
                devdata = self._get_and_response(logger, path, True)
                if isusp:
                    if rtype == 'Processors' and devdata['ProcessorType'] == 'CPU':
                        cpu = cpu + 1
                        self._check_cpu_device(devdata)
                        self.targetdevice['cpu'] = True
                else:
                    self._check_pcie_device(path.split('-')[-1], devtype, logger)
                    self.targetdevice[devtype] = True

                cnt = cnt + 1
        assert cnt == num, f'{url} device count is {cnt} not {num}. See log {self.log_file}'
        if isusp:
            assert cpu == 1, f'{url} cpu count is {cpu} not 1. See log {self.log_file}'

    def test_resource_block_links(self):
        """ResourceBlock Tests (Required features for FM plugin)"""
        self.log_file = 'test-get-resourceblock.log'
        logger = self.get_logger('test-get-resourceblock', self.log_file)

        self.targetdevice = {x: False for x in self.targetdevice}
        rblocks = []
        for _i in self.usprange:
            url = f'CompositionService/ResourceBlocks/ComputeBlock-{_i}'
            rblocks.append(f'/redfish/v1/{url}')
            devnum = len([x for x in self.devconfig['cpu'][_i-1]['link'] if x not in
                         [{'deviceID': y['deviceID']} for y in self.devconfig['graphicController']]]) + 1
            self._check_resource_block_target_device(url, devnum, logger)

        for _i in self.dsprange:
            url = f'CompositionService/ResourceBlocks/DeviceBlock-{_i}'
            rblocks.append(f'/redfish/v1/{url}')
            self._check_resource_block_target_device(url, 1, logger)

        for key, value in self.targetdevice.items():
            assert value, f'{key} device not found, test not execute'

        data = self._get_and_response(logger, 'CompositionService/ResourceBlocks')
        members = [x['@odata.id'] for x in data.get('Members', [])]
        assert set(members) == set(rblocks), f'resource block not same\n{members}\n{rblocks}'

    def _check_resource_block_in_system_link(self, sysid, links, logger):
        """Check ComputeSystem's ResourceBlock link"""
        url = f'Systems/System-{sysid}'
        data = self._get_and_response(logger, url)
        count = data.get('Links', {}).get('ResourceBlocks@odata.count', -1)
        assert count == len(links), f'ResourceBlocks {count}. See log {self.log_file}'
        cnt = 0
        block1 = '/redfish/v1/CompositionService/ResourceBlocks/ComputeBlock-'
        block2 = '/redfish/v1/CompositionService/ResourceBlocks/DeviceBlock-'
        for odata in data.get('Links', {}).get('ResourceBlocks', []):
            path = odata.get('@odata.id').replace(block1, '').replace(block2, '')
            assert path in links, f'{path} not in {links}. See log {self.log_file}'
            links.remove(path)
            data = self._get_and_response(logger, odata.get('@odata.id'), True)

            cnt = cnt + 1
        assert cnt == count, f'{url} link count is {cnt}. See log {self.log_file}'

    def _check_system_in_resource_block_link(self, blkid, links, logger):
        """Check ResourceBlock's ComputeSystem link (Required features for FM plugin)"""
        url = f'CompositionService/ResourceBlocks/DeviceBlock-{blkid}'
        data = self._get_and_response(logger, url)
        syslink = data.get('Links', {}).get('ComputerSystems')
        assert [f'/redfish/v1/Systems/System-{x}' for x in links] == [x.get('@odata.id') for x in syslink]

    def _patch_and_response(self, sysid: str, payload: dict, status: int, logger):
        """Execute patch ComputeSystem and check response"""

        patching = self.url(f'Systems/System-{sysid}')
        headers = {'Content-Type': 'application/json'}
        resp = requests.patch(patching, data=json.dumps(payload), headers=headers, timeout=1.0)
        self.assert_status(resp, status, logger)
        logger.info(f'PASS: PATCH {payload} to {patching} status {status} (response below)\n{resp.text}')

    def do_patch(self, sysid, links, logger):
        """Execute patch ComputeSystem"""
        block = '/redfish/v1/CompositionService/ResourceBlocks/DeviceBlock-'
        payload = {'Links': {'ResourceBlocks': [{'@odata.id': f'{block}{x}'} for x in links if x != sysid]}}
        compute = f'/redfish/v1/CompositionService/ResourceBlocks/ComputeBlock-{sysid}'
        payload['Links']['ResourceBlocks'].append({'@odata.id': compute})
        self._patch_and_response(sysid, payload, 200, logger)
        self._check_resource_block_in_system_link(sysid, links, logger)

    def _check_normal_composition(self, logger):
        """Cases in which configuration changes are successful (Required features for FM plugin)"""

        # Connect all DSPs to the first USP
        self.do_patch('1', ['1'] + [str(_i) for _i in self.dsprange], logger)
        # Verify that all DSPs are connected to the first USP
        for _i in self.dsprange:
            self._check_system_in_resource_block_link(str(_i), ['1'], logger)

        # Disconnect all DSPs from the first USP
        self.do_patch('1', ['1'], logger)
        # Verify that all DSPs are not connected to USPs
        for _i in self.dsprange:
            self._check_system_in_resource_block_link(str(_i), [], logger)

        # Connect num DSPs to all USPs.
        num = int(self.dspnum / self.uspnum)
        for _i in self.usprange:
            link = [str(_i+(self.uspnum*(_j))) for _j in range(num + 1)]
            self.do_patch(str(_i), link, logger)
        # Verify that the DSP is connected to the specified USP.
        for _i in self.usprange:
            for _j in range(num):
                self._check_system_in_resource_block_link(str(_i+(self.uspnum*(_j+1))), [str(_i)], logger)

        # Initialize the connection state.
        for _i in self.usprange:
            self.do_patch(str(_i), [str(_i)], logger)

    def _check_invalid_composition(self, logger):
        """Cases where configuration changes fail (Required features for FM plugin)"""

        # Check that POST and DELETE are not supported.
        headers = {'Content-Type': 'application/json'}
        targets = ['ComputeBlock-1', 'DeviceBlock-1']
        blocks = [{'@odata.id': f'/redfish/v1/CompositionService/ResourceBlocks/{x}'} for x in targets]
        payload = {'Name': 'Composed-1', 'Links': {'ResourceBlocks': blocks}}
        resp = requests.post(self.url('Systems'), data=payload, headers=headers, timeout=1.0)
        self.assert_status(resp, 405, logger)

        resp = requests.delete(self.url('Systems/System-1'), timeout=1.0)
        self.assert_status(resp, 405, logger)

        # Initialize the connection state.
        for _i in self.usprange:
            self.do_patch(str(_i), [str(_i)], logger)

        rbbase = '/redfish/v1/CompositionService/ResourceBlocks/'
        block1 = f'{rbbase}ComputeBlock-1'
        block2 = f'{rbbase}DeviceBlock-{str(self.uspnum+1)}'
        notexist = f'{rbbase}DeviceBlock-1'
        payload = {'Links': {'ResourceBlocks': [{'@odata.id': block1}]}}
        # invalid payload
        self._patch_and_response('1', {}, 400, logger)
        self._patch_and_response('1', {'Links': block1}, 400, logger)
        self._patch_and_response('1', {'Links': []}, 400, logger)
        self._patch_and_response('1', {'Links': {}}, 400, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': {}}}, 406, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': block1}}, 400, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': []}}, 406, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': [{}]}}, 400, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': [block1]}}, 400, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': [{"notodata": block1}]}}, 400, logger)
        self._patch_and_response('1', {'Links': {'ResourceBlocks': [{"@odata.id": block2}]}}, 406, logger)

        # not exist system
        self._patch_and_response(str(self.uspnum + 1), payload, 404, logger)
        # not exist block
        self._patch_and_response('1', {'Links': {'ResourceBlocks': [{'@odata.id': notexist}]}}, 404, logger)

        self.do_patch('2', ['2', block2.rsplit('-', maxsplit=1)[-1]], logger)
        # conflict
        payload = {'Links': {'ResourceBlocks': [{'@odata.id': block1}, {'@odata.id': block2}]}}
        self._patch_and_response('1', payload, 409, logger)

        self.do_patch('2', ['2'], logger)

    def test_composition_service(self):
        """Composition Servive Tests (Required features for FM plugin)"""
        self.log_file = 'test-composition-service.log'
        logger = self.get_logger('test-composition-service', self.log_file)
        self._check_invalid_composition(logger)
        self._check_normal_composition(logger)

    def test_fabric_and_switch(self):
        """Fabric and Switch Tests (Required features for FM plugin)"""
        self.log_file = 'test-get-fabric-switch.log'
        logger = self.get_logger('test-get-fabric-switch', self.log_file)

        data = self._get_and_response(logger, 'Fabrics')
        assert len(data['Members']) >= 1
        for member in data.get('Members', []):
            fdata = self._get_and_response(logger, member.get('@odata.id'), True)
            sdata = self._get_and_response(logger, fdata.get('Switches', {}).get('@odata.id'), True)
            for smember in sdata.get('Members', []):
                self._get_and_response(logger, smember.get('@odata.id'), True)

        data = self._get_and_response(logger, 'Fabrics/CXL/Switches')
        assert len(data['Members']) == len(self.devconfig.get('switch', []))
        for member in data.get('Members', []):

            data = self._get_and_response(logger, member.get('@odata.id'), True)
            devid = data['@odata.id'].split('-')[-1]
            device = self._get_device_from_config(devid, 'switch')
            assert device, f'{devid} config data not found. See log {self.log_file}'
            assert device['manufacturer'] == data['Manufacturer'], f'{device} manufacturer != {data}'
            assert device['model'] == data['Model'], f'{device} model != {data}'
            assert device['serialNumber'] == data['SerialNumber'], f'{device} model != {data}'

    def _check_recursive_invocation(self, members: dict, logger):
        """Check all links recursively(Not a requirement for FM plugin)"""
        for obj in members.values():
            if isinstance(obj, str):
                if 'CompositionService/ResourceBlocks' in obj:
                    getting = self.odata_id_url(obj)
                    resp = requests.get(getting, timeout=1.0)
                    assert resp.status_code in [200, 405], f'{getting} {resp}: See log {self.log_file}'
                elif '/redfish/v1' in obj and '$metadata' not in obj:
                    getting = self.odata_id_url(obj)
                    resp = requests.get(getting, timeout=1.0)
                    if resp.status_code not in [200, 405]:
                        print(f'Unexpect: {getting} response {resp.status_code}')
            elif isinstance(obj, list):
                self._check_recursive_invocation(dict(enumerate(obj)), logger)
            elif isinstance(obj, dict):
                self._check_recursive_invocation(obj, logger)

    def _check_power_action(self, logger, req: str, target: str):
        """Verify that the power states are linked.(Not a requirement for FM plugin)"""
        blkid = target.split('/')[0]
        rscname = target.split('/')[1]
        rscid = target.split('/')[-1]
        base_url = f'Chassis/Chassis-1/{rscname}/{rscid}'
        action_url = f'{base_url}/Actions/{rscname.rstrip("s")}.Reset'
        check_url = base_url.replace('Chassis/Chassis-1', f'CompositionService/ResourceBlocks/{blkid}')
        data = json.dumps({'ResetType': req})
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(self.url(action_url), data=data, headers=headers, timeout=1.0)
        self.assert_status(resp, 200, logger)
        data = json.loads(resp.text)
        assert data['PowerState'] == req, f'Power set {action_url} {req} {data}: See log {self.log_file}'
        data = self._get_and_response(logger, base_url)
        assert data['PowerState'] == req, f'Power get {base_url} {req} {data}: See log {self.log_file}'
        data = self._get_and_response(logger, check_url)
        assert data['PowerState'] == req, f'Power get {check_url} {req} {data}: See log {self.log_file}'

    def test_resource_objects(self):
        """ResourceObject Tests (Not a requirement for FM plugin)"""

        self.log_file = 'test-get-resourceobject.log'
        logger = self.get_logger('test-get-resourceobject', self.log_file)
        blocks = self._get_and_response(logger, 'CompositionService/ResourceBlocks')
        for url in [x.get('@odata.id') for x in blocks.get('Members', [])]:
            data = self._get_and_response(logger, url, True)
            for rtype in ['Processors', 'Memory', 'Drives', 'EthernetInterfaces']:
                for odata in [x.get('@odata.id') for x in data.get(rtype, [])]:
                    objdata = self._get_and_response(logger, odata, True)
                    assert objdata['@odata.id'] == odata, f'{odata} not equal @odata.id of {objdata}'
                    self._check_recursive_invocation(objdata, logger)

                    if rtype == 'EthernetInterfaces':
                        continue
                    target_dev = odata.replace('/redfish/v1/CompositionService/ResourceBlocks/', '')
                    self._check_power_action(logger, 'Off', target_dev)
                    self._check_power_action(logger, 'On', target_dev)
                    chassis = f'/redfish/v1/Chassis/Chassis-1/{target_dev.partition("/")[2]}'
                    cdata = self._get_and_response(logger, chassis, True)
                    assert cdata['@odata.id'] == chassis, f'{chassis} not equal @odata.id of {cdata}'

if __name__ == '__main__':
    #main(sys.argv[2:])
    parser = argparse.ArgumentParser()
    parser.add_argument('spec', choices=['Redfish', 'Chinook'], type=str,
                        help='Specification used for pooled node definition'
                             ' by the emulator')

    parser.add_argument('address', metavar='address', type=str, nargs=1,
                        help='Address to access the emulator')
    args = parser.parse_args()
    print('Testing interface at:', sys.argv[2])
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRedfishEmulator)
    runner = unittest.TextTestRunner(verbosity=2)

    sub_str = 'chinook'

    if args.spec == 'Chinook':
        sub_str = 'redfish'

    for t in suite:
        if sub_str in t.id():
            setattr(t, 'setUp', lambda: t.skipTest('Emulator running using the {0} spec'.format(args.spec)))
    runner.run(suite)
