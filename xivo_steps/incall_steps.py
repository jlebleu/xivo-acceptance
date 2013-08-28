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

from lettuce import step

from xivo_lettuce import form
from xivo_lettuce import common
from xivo_lettuce.common import open_url
from xivo_lettuce.manager import incall_manager as incall_man
from xivo_lettuce.manager_ws import incall_manager_ws


@step(u'Given there is no incall "([^"]*)"$')
def given_there_is_no_incall(step, search):
    common.remove_element_if_exist('incall', search)


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)"$')
def given_there_is_an_incall_group1_in_context_group2_to(step, did, context, dst_type, dst_name):
    incall_manager_ws.delete_incalls_with_did(did)
    incall_manager_ws.add_incall(did, context, dst_type, dst_name)


@step(u'Given there is an incall "([^"]*)" in context "([^"]*)" to the "([^"]*)" "([^"]*)" with caller id name "([^"]*)" number "([^"]*)"')
def given_there_is_an_incall_group1_in_context_group2_to_the_queue_group3(step, did, context, dst_type, dst_name, cid_name, cid_num):
    caller_id = '"%s" <%s>' % (cid_name, cid_num)
    incall_manager_ws.delete_incalls_with_did(did)
    incall_manager_ws.add_incall(did, context, dst_type, dst_name, caller_id)


@step(u'When I create an incall with DID "([^"]*)" in context "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did, context):
    open_url('incall', 'add')
    incall_man.type_incall_did(incall_did)
    incall_man.type_incall_context(context)
    form.submit.submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    incall_man.remove_incall_with_did(incall_did)
