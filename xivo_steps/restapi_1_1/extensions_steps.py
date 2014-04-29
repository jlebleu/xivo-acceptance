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

from xivo_acceptance.action.restapi import extension_action_restapi
from xivo_acceptance.helpers import extension_helper


@step(u'Given I have no extension with exten "(\d+)@([\w-]+)"')
def given_i_have_no_extension_with_exten_group1(step, exten, context):
    extension = extension_helper.find_by_exten(exten, context)
    if extension:
        extension_helper.delete_extension(extension['id'])


@step(u'Given I have the following extensions:')
def given_i_have_the_following_extensions(step):
    for exteninfo in step.hashes:
        extension = _extract_extension_parameters(exteninfo)
        extension_helper.add_or_replace_extension(extension)


@step(u'When I access the list of extensions')
def when_i_access_the_list_of_extensions(step):
    world.response = extension_action_restapi.all_extensions()


@step(u'When I access a fake extension id')
def when_i_access_a_fake_extension_id(step):
    world.response = extension_action_restapi.get_extension(999999999)


@step(u'When I access the extension with exten "(\d+)@([\w-]+)"')
def when_i_access_the_extension_with_exten_group1(step, exten, context):
    extension = extension_helper.get_by_exten(exten, context)
    world.response = extension_action_restapi.get_extension(extension['id'])


@step(u'When I create an empty extension$')
def when_i_create_an_empty_extension(step):
    world.response = extension_action_restapi.create_extension({})


@step(u'When I create an extension with the following parameters:')
def when_i_create_an_extension_with_the_following_parameters(step):
    parameters = _extract_extension_parameters(step.hashes[0])
    world.response = extension_action_restapi.create_extension(parameters)


@step(u'When I update a fake extension')
def when_i_update_a_fake_extension(step):
    world.response = extension_action_restapi.update(999999999, {})


@step(u'When I update the extension with exten "(\d+)@([\w-]+)" using the following parameters:')
def when_i_update_the_extension_with_id_group1_using_the_following_parameters(step, exten, context):
    extension = extension_helper.get_by_exten(exten, context)
    extensioninfo = _extract_extension_parameters(step.hashes[0])
    world.response = extension_action_restapi.update(extension['id'], extensioninfo)


@step(u'When I delete a fake extension')
def when_i_delete_a_fake_extension(step):
    world.response = extension_action_restapi.delete_extension(999999999)


@step(u'When I delete extension with exten "(\d+)@([\w-]+)"')
def when_i_delete_extension_group1(step, exten, context):
    extension = extension_helper.get_by_exten(exten, context)
    world.response = extension_action_restapi.delete_extension(extension['id'])


@step(u'Then I get a list containing the following extensions:')
def then_i_get_a_list_containing_the_following_extensions(step):
    expected_extensions = step.hashes
    extensions = _filter_out_default_extensions()

    entries = [has_entries(e) for e in expected_extensions]
    assert_that(extensions, has_items(*entries))


@step(u'Then I have an extension with the following parameters:')
def then_i_have_an_extension_with_the_following_parameters(step):
    parameters = _extract_extension_parameters(step.hashes[0])
    extension = world.response.data

    assert_that(extension, has_entries(parameters))


@step(u'Then the extension with exten "(\d+)@([\w-]+)" no longer exists')
def then_the_extension_group1_no_longer_exists(step, exten, context):
    extension = extension_helper.find_by_exten(exten, context)
    assert_that(extension, none())


def _filter_out_default_extensions():
    assert_that(world.response.data, has_key('items'))
    extensions = [e for e in world.response.data['items'] if e['context'] != 'xivo-features']
    return extensions


def _extract_extension_parameters(parameters):

    if 'id' in parameters:
        parameters['id'] = int(parameters['id'])

    if 'commented' in parameters:
        parameters['commented'] = (parameters['commented'] == 'true')

    return parameters
