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

from hamcrest import assert_that, is_not, none
from lettuce import world

from xivo_acceptance.action.restapi import user_action_restapi as user_action
from xivo_acceptance.action.restapi import user_line_action_restapi as user_line_action
from xivo_acceptance.helpers import group_helper, device_helper, line_helper, voicemail_helper, func_key_helper
from xivo_lettuce import postgres
from xivo_ws import User, UserLine, UserVoicemail
from xivo_ws.exception import WebServiceRequestError


def add_or_replace_user(user):
    if 'id' in user:
        delete_user(user['id'])
    if 'firstname' in user and 'lastname' in user:
        delete_users_with_firstname_lastname(user['firstname'], user['lastname'])
    create_user(user)


def user_exists(user_id):
    response = user_action.get_user(user_id)
    return response.status == 200


def get_user(user_id):
    response = user_action.get_user(user_id)
    return response.resource()


def find_all_by_firstname_lastname(firstname, lastname):
    fullname = "%s %s" % (firstname, lastname)
    response = user_action.user_search(fullname)
    matching = [user
                for user in response.items()
                if user['firstname'] == firstname and user['lastname'] == lastname]
    return matching


def find_by_firstname_lastname(firstname, lastname):
    users = find_all_by_firstname_lastname(firstname, lastname)
    return users[0] if users else None


def get_by_firstname_lastname(firstname, lastname):
    user = find_by_firstname_lastname(firstname, lastname)
    assert_that(user, is_not(none()), "user %s %s not found" % (firstname, lastname))
    return user


def find_user_id_with_firstname_lastname(firstname, lastname):
    user = get_by_firstname_lastname(firstname, lastname)
    return user['id']


def find_line_id_for_user(user_id):
    response = user_line_action.get_user_line(user_id)
    items = response.items()
    if items:
        return items[0]['line_id']


def create_user(userinfo):
    response = user_action.create_user(userinfo)
    response.check_status()


def delete_users_with_firstname_lastname(firstname, lastname):
    users = find_all_by_firstname_lastname(firstname, lastname)
    for user in users:
        delete_user(user['id'])


def delete_user(user_id):
    if user_exists(user_id):
        _delete_associations(user_id)

        template_id = func_key_helper.find_template_for_user(user_id)
        _delete_user(user_id)
        func_key_helper.delete_template_and_func_keys(template_id)


def _delete_associations(user_id):
    _delete_line_associations(user_id)
    voicemail_helper.delete_voicemail_with_user_id(user_id)
    func_key_helper.delete_func_keys_with_user_destination(user_id)


def _delete_line_associations(user_id):
    line_id = find_line_id_for_user(user_id)
    if line_id:
        line_helper.delete_line_associations(line_id)


def _delete_user(user_id):
    response = user_action.delete_user(user_id)
    response.check_status()


def add_user(data_dict):
    '''
        #TODO refactor to use dao
    '''
    user = User()

    if 'id' in data_dict:
        user.id = data_dict['id']

    user.firstname = data_dict['firstname']

    if 'lastname' in data_dict:
        user.lastname = data_dict['lastname']
    if 'agentid' in data_dict:
        user.agent_id = int(data_dict['agentid'])
    if 'language' in data_dict:
        user.language = data_dict['language']
    if 'enable_client' in data_dict:
        user.enable_client = bool(data_dict['enable_client'])
    if 'client_username' in data_dict:
        user.client_username = data_dict['client_username']
    if 'client_password' in data_dict:
        user.client_password = data_dict['client_password']
    if 'client_profile' in data_dict:
        user.client_profile = data_dict['client_profile']
    if 'bsfilter' in data_dict:
        user.bsfilter = data_dict['bsfilter']

    if 'line_number' in data_dict and 'line_context' in data_dict:
        user.line = UserLine()
        user.line.number = data_dict['line_number']
        user.line.context = data_dict['line_context']
        if 'protocol' in data_dict:
            user.line.protocol = data_dict['protocol']
        if 'device' in data_dict:
            device = device_helper.find_device_with('mac', data_dict['device'])
            user.line.device_id = device['id']

    if 'voicemail_name' in data_dict and 'voicemail_number' in data_dict:
        user.voicemail = UserVoicemail()
        user.voicemail.name = data_dict['voicemail_name']
        user.voicemail.number = data_dict['voicemail_number']

    if 'mobile_number' in data_dict:
        user.mobile_number = data_dict['mobile_number']

    try:
        ret = world.ws.users.add(user)
    except WebServiceRequestError as e:
        raise Exception('Could not add user %s %s: %s' % (user.firstname, user.lastname, e))
    if not ret:
        return False

    return int(ret)


def user_id_is_in_group_name(group_name, user_id):
    group = group_helper.get_group_with_name(group_name)
    for id in group.user_ids:
        if id == user_id:
            return True
    return False


def disable_cti_client(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        user.enable_client = False
        world.ws.users.edit(user)


def enable_cti_client(firstname, lastname):
    users = _search_users_with_firstname_lastname(firstname, lastname)
    for user in users:
        user.enable_client = True
        world.ws.users.edit(user)


def has_enabled_transfer(firstname, lastname):
    for user in _search_users_with_firstname_lastname(firstname, lastname):
        return user.enable_transfer
    return False


def _search_users_with_firstname_lastname(firstname, lastname):
    users = world.ws.users.search('%s %s' % (firstname, lastname))
    return [user for user in users if
            user.firstname == firstname and
            user.lastname == lastname]


def count_linefeatures(user_id):
    return _count_table_with_cond("user_line", {'"user_id"': user_id})


def count_rightcallmember(user_id):
    return _count_table_with_cond("rightcallmember", {'"type"': "'user'", '"typeval"': "'%s'" % user_id})


def count_dialaction(user_id):
    return _count_table_with_cond("dialaction", {'"category"': "'user'", '"categoryval"': "'%s'" % user_id})


def count_phonefunckey(user_id):
    return _count_table_with_cond("phonefunckey", {'"iduserfeatures"': user_id})


def count_callfiltermember(user_id):
    return _count_table_with_cond("callfiltermember", {'"type"': "'user'", '"typeval"': "'%s'" % user_id})


def count_queuemember(user_id):
    return _count_table_with_cond("queuemember", {'"usertype"': "'user'", '"userid"': user_id})


def count_schedulepath(user_id):
    return _count_table_with_cond("schedule_path", {'"path"': "'user'", '"pathid"': user_id})


def _count_table_with_cond(table, cond_dict):
    return postgres.exec_count_request(table, **cond_dict)
