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

from lettuce import world

CONFIGURATION_URL = 'configuration'


def get_live_reload_state():
    return world.confd_utils_1_1.rest_get('/%s/live_reload' % CONFIGURATION_URL)


def disable_live_reload():
    return world.confd_utils_1_1.rest_put('/%s/live_reload' % CONFIGURATION_URL, {'enabled': False})


def enable_live_reload():
    return world.confd_utils_1_1.rest_put('/%s/live_reload' % CONFIGURATION_URL, {'enabled': True})
