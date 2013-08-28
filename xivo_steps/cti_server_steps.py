# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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

import time
from lettuce import step, world
from hamcrest import assert_that, equal_to
from xivo_lettuce import common
from xivo_lettuce.manager import profile_manager


@step(u'Given there is no CTI profile "([^"]*)"$')
def given_there_is_no_cti_profile(step, search):
    common.remove_element_if_exist('CTI profile', search)


@step(u'Then the profile "([^"]*)" has default services activated')
def then_the_profile_1_has_default_services_activated(step, profile_name):
    common.open_url('profile', 'list')
    common.edit_line(profile_name)
    time.sleep(world.timeout)  # wait for the javascript to load

    expected_services = [
        'Enable DND',
        'Unconditional transfer to a number',
        'Transfer on busy',
        'Transfer on no-answer',
    ]
    selected_services = profile_manager.selected_services()

    assert_that(selected_services, equal_to(expected_services))
