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

from xivo_lettuce.postgres import exec_sql_request
from xivo_lettuce.remote_py_cmd import remote_exec_with_result
from xivo_acceptance.action.restapi import extension_action_restapi as extension_action
from xivo_acceptance.helpers import dialpattern_helper, user_helper, \
    group_helper, incall_helper, meetme_helper, queue_helper, line_helper


def find_by_exten(exten, context='default'):
    extensions = all_extensions()

    found = [extension for extension in extensions
             if extension['exten'] == exten and extension['context'] == context]

    return found[0] if found else None


def get_by_exten(exten, context='default'):
    extension = find_by_exten(exten, context)
    assert_that(extension, is_not(none()), "extension %s@%s does not exist" % (exten, context))
    return extension


def all_extensions():
    response = extension_action.all_extensions()
    return response.items()


def find_line_id_for_extension(extension_id):
    return remote_exec_with_result(_find_line_id_for_extension, extension_id=extension_id)


def _find_line_id_for_extension(channel, extension_id):
    from xivo_dao.data_handler.line_extension import services as line_extension_services

    line_extension = line_extension_services.find_by_extension_id(extension_id)
    if line_extension:
        channel.send(line_extension.line_id)
    else:
        channel.send(None)


def add_or_replace_extension(extension):
    if 'exten' in extension:
        delete_extension_with_exten(extension['exten'],
                                    extension.get('context', 'default'))
    if 'id' in extension:
        delete_extension(extension['id'])

    create_extension(extension)


def create_extension(extension):
    response = extension_action.create_extension(extension)
    response.check_status()


def delete_extension(extension_id):
    _delete_extension_associations(extension_id)
    _delete_extension(extension_id)


def _delete_extension_associations(extension_id):
    _delete_line_associations(extension_id)
    _delete_type_associations(extension_id)


def _delete_line_associations(extension_id):
    line_id = find_line_id_for_extension(extension_id)
    if line_id:
        line_helper.delete_line_associations(line_id)


def _delete_type_associations(extension_id):
    exten, extension_type, typeval = _fetch_extension_info(extension_id)

    if extension_type == 'user':
        user_helper.delete_user(int(typeval))
    elif extension_type == 'queue':
        queue_helper.delete_queues_with_number(exten)
    elif extension_type == 'group':
        group_helper.delete_groups_with_number(exten)
    elif extension_type == 'incall':
        incall_helper.delete_incalls_with_did(exten)
    elif extension_type == 'meetme':
        meetme_helper.delete_meetme_with_confno(exten)
    elif extension_type == 'outcall':
        dialpattern_helper.delete(int(typeval))


def _fetch_extension_info(extension_id):
    query = "SELECT exten, type, typeval FROM extensions where id = :extension_id"
    row = exec_sql_request(query, extension_id=extension_id).first()
    return row[0], row[1], row[2]


def _delete_extension(extension_id):
    response = extension_action.delete_extension(extension_id)
    response.check_status()


def delete_extension_with_exten(exten, context='default'):
    extension = find_by_exten(exten, context)
    if extension:
        delete_extension(extension['id'])
