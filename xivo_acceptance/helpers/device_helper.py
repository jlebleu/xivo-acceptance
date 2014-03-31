# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import json
import requests

from hamcrest import assert_that, equal_to

from lettuce.registry import world
from xivo_acceptance.action.restapi import device_action_restapi as device_action

AUTOPROV_URL = 'https://%s/xivo/configuration/json.php/restricted/provisioning/autoprov?act=configure'
HEADERS = {'Content-Type': 'application/json'}


def find_devices_with(key, value):
    devices = [device
               for device in device_action.device_list({key: value}).data['items']
               if device[key] == value]
    return devices


def find_device_with(key, value):
    devices = find_devices_with(key, value)
    return devices[0] if devices else None


def provision_device_using_webi(provcode, device_ip):
    data = json.dumps({'code': provcode, 'ip': device_ip})
    requests.post(url=AUTOPROV_URL % world.config.xivo_host,
                  headers=HEADERS,
                  auth=_prepare_auth(),
                  data=data,
                  verify=False)


def _prepare_auth():
    auth = requests.auth.HTTPBasicAuth(world.config.rest_username, world.config.rest_passwd)
    return auth


def create_dummy_devices(nb_devices):
    for i in range(nb_devices):
        create_dummy_device()


def create_dummy_device():
    return device_action.create_device({})


def delete_device_with(key, value):
    for device in find_devices_with(key, value):
        delete_device(device['id'])


def delete_device(device_id):
    device_action.reset_to_autoprov(device_id)
    device_action.delete_device(device_id)


def remove_devices_over(nb_devices):
    devices = device_action.device_list().data['items']
    for device in devices[nb_devices:]:
        delete_device(device['id'])


def total_devices():
    response = device_action.device_list()
    return response.data['total']


def add_or_replace_device(device):
    remove_device(device)

    response = device_action.create_device(device)
    assert_that(response.status, equal_to(201), response.data)

    return response.data


def remove_device(device):
    if 'mac' in device:
        delete_device_with('mac', device['mac'])
    if 'ip' in device:
        delete_device_with('ip', device['ip'])
