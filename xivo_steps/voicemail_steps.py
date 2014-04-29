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

from hamcrest import *
from lettuce import step, world

from xivo_acceptance.helpers import voicemail_helper, user_helper
from xivo_acceptance.action.restapi import voicemail_action_restapi
from xivo_acceptance.action.restapi import voicemail_link_action_restapi
from xivo_lettuce.xivo_hamcrest import assert_has_dicts_in_order, assert_does_not_have_any_dicts
from xivo_lettuce import func


@step(u'Given there is no voicemail with number "([^"]*)" and context "([^"]*)"')
def given_there_is_no_voicemail_with_number_and_context(step, voicemail_number, context):
    voicemail_helper.delete_voicemail_with_number_context(voicemail_number, context)


@step(u'Given I have no voicemail with id "([^"]*)"')
def given_i_have_no_voicemail_with_id_group1(step, voicemail_id):
    voicemail_helper.delete_voicemail_with_id(voicemail_id)


@step(u'Given I have the following voicemails:')
def given_have_the_following_voicemails(step):
    for row in step.hashes:
        voicemail_info = _extract_voicemail_info_to_restapi(row)
        voicemail_helper.add_or_replace_voicemail(voicemail_info)


@step(u'When I request voicemail with id "([^"]*)"')
def when_i_request_voicemail_with_id_group1(step, voicemail_id):
    world.response = voicemail_action_restapi.get_voicemail(voicemail_id)


@step(u'When I send a request for the voicemail "([^"]*)", using its id')
def when_i_send_a_request_for_the_voicemail_with_number_group1_using_its_id(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_id = voicemail_helper.find_voicemail_id_with_number(number, context)
    world.response = voicemail_action_restapi.get_voicemail(voicemail_id)


@step(u'When I create an empty voicemail via RESTAPI:')
def when_i_create_an_empty_voicemail(step):
    world.response = voicemail_action_restapi.create_voicemail({})


@step(u'When I edit voicemail "([^"]*)" via RESTAPI:')
def when_i_edit_voicemail_via_restapi(step, extension):
    parameters = _extract_voicemail_info_to_restapi(step.hashes[0])
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_id = voicemail_helper.find_voicemail_id_with_number(number, context)
    world.response = voicemail_action_restapi.edit_voicemail(voicemail_id, parameters)


@step(u'When I delete voicemail "([^"]*)" via RESTAPI')
def when_i_delete_voicemail_with_number_group1_via_restapi(step, extension):
    number, context = func.extract_number_and_context_from_extension(extension)
    voicemail_id = voicemail_helper.find_voicemail_id_with_number(number, context)
    world.response = voicemail_action_restapi.delete_voicemail(voicemail_id)


@step(u'When I create the following voicemails via RESTAPI:')
def when_i_create_voicemails_with_the_following_parameters(step):
    for row in step.hashes:
        voicemail = _extract_voicemail_info_to_restapi(row)
        world.response = voicemail_action_restapi.create_voicemail(voicemail)


@step(u'When I request the list of voicemails via RESTAPI')
def when_i_request_the_list_of_voicemails(step):
    world.response = voicemail_action_restapi.voicemail_list()


@step(u'When I request the list of voicemails with the following parameters via RESTAPI:')
def when_i_request_the_list_of_voicemails_with_the_following_parameters(step):
    parameters = _extract_voicemail_info_to_restapi(step.hashes[0])
    world.response = voicemail_action_restapi.voicemail_list(parameters)


@step(u'When I link user "([^"]*)" with voicemail "([^"]*)" via RESTAPI')
def when_i_link_user_group1_with_voicemail_group2_via_restapi(step, fullname, voicemail):
    firstname, lastname = fullname.split(" ")
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    number, context = func.extract_number_and_context_from_extension(voicemail)
    voicemail_id = voicemail_helper.find_voicemail_id_with_number(number, context)

    world.response = voicemail_link_action_restapi.link_voicemail(user.id, voicemail_id)


@step(u'When I link user "([^"]*)" with voicemail id "([^"]*)" via RESTAPI')
def when_i_link_user_group1_with_voicemail_id_group2_via_restapi(step, fullname, voicemail_id):
    firstname, lastname = fullname.split(" ")
    user = user_helper.get_by_firstname_lastname(firstname, lastname)
    world.response = voicemail_link_action_restapi.link_voicemail(user.id, voicemail_id)


@step(u'When I request the voicemail associated to user "([^"]*)" "([^"]*)" via RESTAPI')
def when_i_request_the_voicemail_associated_to_user_group1_group2_via_restapi(step, firstname, lastname):
    user = user_helper.find_by_firstname_lastname(firstname, lastname)
    world.response = voicemail_link_action_restapi.get_voicemail_link(user['id'])


@step(u'When I request the voicemail associated to user with id "([^"]*)" via RESTAPI')
def when_i_request_the_voicemail_associated_to_user_with_id_group1_via_restapi(step, user_id):
    world.response = voicemail_link_action_restapi.get_voicemail_link(int(user_id))


@step(u'When I dissociate user "([^"]*)" "([^"]*)" from his voicemail via RESTAPI')
def when_i_dissociate_user_group1_from_his_voicemail_via_restapi(step, firstname, lastname):
    user = user_helper.find_by_firstname_lastname(firstname, lastname)
    world.response = voicemail_link_action_restapi.delete_voicemail_link(user['id'])


@step(u'When I dissociate user with id "([^"]*)" from his voicemail via RESTAPI')
def when_i_dissociate_user_with_id_group1_from_his_voicemail_via_restapi(step, user_id):
    world.response = voicemail_link_action_restapi.delete_voicemail_link(int(user_id))


@step(u'Then I have the following voicemails via RESTAPI:')
def then_the_voicemail_has_the_following_parameters(step):
    expected_voicemail = _extract_voicemail_info_to_restapi(step.hashes[0])

    assert_that(world.response.data, has_entries(expected_voicemail))


@step(u'Then I get a list containing the following voicemails via RESTAPI:')
def then_i_get_a_list_containing_the_following_voicemails(step):
    assert_that(world.response.data, has_entries(
        'total', instance_of(int),
        'items', instance_of(list)))

    voicemail_list = world.response.data['items']

    for voicemail in step.hashes:
        voicemail = _extract_voicemail_info_to_restapi(voicemail)
        assert_that(voicemail_list, has_item(has_entries(voicemail)))


@step(u'Then I get a list of voicemails in the following order via RESTAPI:')
def then_i_get_a_list_of_voicemails_in_the_following_order(step):
    all_voicemails = world.response.data['items']
    expected_voicemails = [_extract_voicemail_info_to_restapi(v) for v in step.hashes]
    assert_has_dicts_in_order(all_voicemails, expected_voicemails)


@step(u'Then I have a list with (\d+) of (\d+) results')
def then_i_have_a_list_with_n_of_n_results(step, nb_list, nb_total):
    nb_list = int(nb_list)
    nb_total = int(nb_total)
    assert_that(world.response.data, all_of(
        has_entry('total', equal_to(nb_total)),
        has_entry('items', has_length(nb_list))))


@step(u'Then I have a list with (\d+) results$')
def then_i_have_a_list_with_n_results(step, nb_list):
    nb_list = int(nb_list)
    assert_that(world.response.data, has_entry('items', has_length(nb_list)))


@step(u'Then the list contains the same total voicemails as on the server')
def then_the_list_contains_the_same_total_voicemails_as_on_the_server(step):
    total_server = voicemail_helper.total_voicemails()
    total_response = world.response.data['total']
    assert_that(total_server, equal_to(total_response))


@step(u'Then I do not have the following voicemails in the list:')
def then_i_dot_not_have_the_following_voicemails_in_the_list(step):
    all_voicemails = world.response.data['items']
    not_expected_voicemails = [_extract_voicemail_info_from_restapi(v) for v in step.hashes]

    assert_does_not_have_any_dicts(all_voicemails, not_expected_voicemails)


@step(u'Then voicemail with number "([^"]*)" no longer exists')
def then_voicemail_with_number_group1_no_longer_exists(step, number):
    response = voicemail_action_restapi.voicemail_list({'search': number})
    voicemails = response.data['items']

    assert_that(voicemails, is_not(has_item(has_entry('number', number))))


@step(u'Then I get a response with a voicemail id')
def then_i_get_a_response_with_a_voicemail_id(step):
    assert_that(world.response.data,
                has_entry('voicemail_id', instance_of(int)))


def _extract_voicemail_info_to_restapi(row):
    voicemail = dict(row)

    if 'max_messages' in voicemail and voicemail['max_messages'] is not None and voicemail['max_messages'].isdigit():
        voicemail['max_messages'] = int(voicemail['max_messages'])

    for key in ['attach_audio', 'delete_messages', 'ask_password']:
        if key in voicemail:
            voicemail[key] = (voicemail[key] == 'true')

    return voicemail


def _extract_voicemail_info_from_restapi(row):
    voicemail = dict(row)

    if 'max_messages' in voicemail and voicemail['max_messages'] is not None:
        voicemail['max_messages'] = str(voicemail['max_messages'])

    for key in ['attach_audio', 'delete_messages', 'ask_password']:
        if key in voicemail and isinstance(voicemail[key], bool):
            voicemail[key] = str(voicemail[key]).lower()

    return voicemail
