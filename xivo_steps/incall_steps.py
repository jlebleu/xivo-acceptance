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

from lettuce import step
from hamcrest import *

from xivo_acceptance.action.webi import incall as incall_action_webi
from xivo_acceptance.helpers import incall_helper
from xivo_lettuce import form, common


@step(u'Given there is no incall "([^"]*)"$')
def given_there_is_no_incall(step, did):
    incall_helper.delete_incalls_with_did(did)


@step(u'Given there is no incall "([^"]*)" in context "([^"]*)"$')
def given_there_is_no_incall_in_context(step, did, context):
    incall_helper.delete_incalls_with_did(did, context)


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)"$')
def given_there_is_an_incall_group1_in_context_group2_to(step, did, context, dst_type, dst_name):
    incall_helper.delete_incalls_with_did(did)
    incall_helper.add_incall(did, context, dst_type, dst_name)


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)" with caller id name "([^"]*)" number "([^"]*)"')
def given_there_is_an_incall_group1_in_context_group2_to_the_queue_group3(step, did, context, dst_type, dst_name, cid_name, cid_num):
    caller_id = '"%s" <%s>' % (cid_name, cid_num)
    incall_helper.delete_incalls_with_did(did)
    incall_helper.add_incall(did, context, dst_type, dst_name, caller_id)


@step(u'When I create an incall with DID "([^"]*)" in context "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did, context):
    common.open_url('incall', 'add')
    incall_action_webi.type_incall_did(incall_did)
    incall_action_webi.type_incall_context(context)
    form.submit.submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    incall_action_webi.remove_incall_with_did(incall_did)


@step(u'Then incall "([^"]*)" is associated to nothing')
def then_incall_group1_is_associated_to_nothing(step, did):
    incall = _find_incall_with_did(did)
    assert_that(incall.destination, none())


@step(u'Then I see the incall "([^"]*)" exists$')
def then_i_see_the_element_exists(step, name):
    common.open_url('incall')
    line = common.find_line(name)
    assert line is not None, 'incall: %s does not exist' % name


@step(u'Then I see the incall "([^"]*)" not exists$')
def then_i_see_the_element_not_exists(step, name):
    common.open_url('incall')
    line = common.find_line(name)
    assert line is None, 'incall: %s exist' % name


def _find_incall_with_did(did):
    incalls = incall_helper.find_incalls_with_did(did)
    assert_that(incalls, has_length(1), "more that one incall with DID %s found" % did)
    return incalls[0]
