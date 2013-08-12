# -*- coding: utf-8 -*-
#
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

from lettuce.registry import world


def exec_sql_request(pg_command):
    return world.asterisk_conn.execute(pg_command)


def exec_count_request(table, **cond_dict):
    pg_command = 'SELECT COUNT(*) FROM "%s"' % table
    if len(cond_dict) > 0:
        pg_command += " WHERE "
        cond = []
        for key, value in cond_dict.iteritems():
            cond.append('%s = %s' % (key, value))
        pg_command = '%s%s' % (pg_command, ' AND '.join(cond))

    result = world.asterisk_conn.execute(pg_command)
    row = result.fetchone()
    return int(row[0])
