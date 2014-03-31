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

from hamcrest import assert_that, has_entries, has_key, is_not, none

from lettuce import world


def device_config_has_properties(device_id, properties):
    config = get_provd_config(device_id)
    assert_that(config, has_entries(properties))


def get_provd_config(device_id):
    device = _check_device_exists(device_id)
    config = _check_device_has_config(device)
    return config


def _check_device_exists(device_id):
    device = world.provd_client.device_manager().get(device_id)
    assert_that(device, is_not(none()), "Device id %s does not exist" % device_id)
    return device


def _check_device_has_config(device):
    assert_that(device, has_key('config'), "Device does not have config key")

    config = world.provd_client.config_manager().get(device['config'])
    assert_that(config, is_not(none()), "Config %s does not exist" % device['config'])

    return config


def add_or_replace_device_template(properties):
    config_manager = world.provd_client.config_manager()

    if 'id' in properties:
        existing = config_manager.find({'X_type': 'device', 'id': properties['id']})
        if len(existing) > 0:
            return

    default_properties = {
        'X_type': 'device',
        'deletable': True,
        'parent_ids': [],
        'raw_config': {}
    }

    properties.update(default_properties)

    config_manager.add(properties)


def find_by(key, value):
    device_manager = world.provd_client.device_manager()
    devices = device_manager.find({key: value})

    if not devices:
        return None
    return devices[0]
