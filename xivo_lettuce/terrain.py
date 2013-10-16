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

import sys
import tempfile

from lettuce import before, after, world
from xivobrowser import XiVOBrowser

from xivo_acceptance.helpers import asterisk_helper
from xivo_lettuce.common import webi_login_as_default, webi_logout
from xivo_lettuce.config import XivoAcceptanceConfig


@before.all
def xivo_lettuce_before_all():
    print 'Configuring...'
    initialize()


@before.each_scenario
def xivo_lettuce_before_each_scenario(scenario):
    world.voicemailid = None
    world.userid = None
    world.number = None
    world.lineid = None
    if world.config.browser_enable and _webi_configured():
        _check_webi_login_root()


@after.each_step
def xivo_lettuce_after_each_step(step):
    sys.stdout.flush()


@after.each_scenario
def xivo_lettuce_after_each_scenario(scenario):
    _logout_agents()


@after.all
def xivo_lettuce_after_all(total):
    deinitialize()


def initialize():
    world.config = XivoAcceptanceConfig()
    world.config.setup()
    _setup_ssh_client()
    _setup_ws()
    _setup_provd()
    _setup_browser()
    world.logged_agents = []
    world.dummy_ip_address = '10.99.99.99'


def _setup_ssh_client():
    world.ssh_client_xivo = world.config.ssh_client_xivo
    world.ssh_client_callgen = world.config.ssh_client_callgen


def _setup_ws():
    world.ws = world.config.ws_utils
    world.restapi_utils_1_0 = world.config.restapi_utils_1_0
    world.restapi_utils_1_1 = world.config.restapi_utils_1_1


def _setup_provd():
    world.rest_provd = world.config.rest_provd
    world.provd_client = world.config.provd_client


def _setup_browser():
    if not world.config.browser_enable:
        return

    from pyvirtualdisplay import Display
    browser_size = width, height = tuple(world.config.browser_resolution.split('x', 1))
    world.display = Display(visible=world.config.browser_visible, size=browser_size)
    world.display.start()
    world.browser = XiVOBrowser()
    world.browser.set_window_size(width, height)
    world.timeout = world.config.browser_timeout

    if _webi_configured():
        webi_login_as_default()


def _webi_configured():
    try:
        command = ['test', '-e', '/var/lib/pf-xivo/configured']
        world.ssh_client_xivo.check_call(command)
    except Exception:
        return False
    else:
        return True


def _logout_agents():
    asterisk_helper.logoff_agents(world.logged_agents)
    world.logged_agents = []


def _check_webi_login_root():
    element = world.browser.find_element_by_xpath('//h1[@id="loginbox"]/span[contains(.,"Login")]/b')
    username = element.text
    if username != "root":
        webi_logout()
        webi_login_as_default()


def deinitialize():
    if world.config.browser_enable:
        _teardown_browser()


def _teardown_browser():
    world.browser.quit()
    world.display.stop()


@world.absorb
def dump_current_page(filename='lettuce.html'):
    """Use this if you want to debug your test
       Call it with world.dump_current_page()"""
    dump_dir = tempfile.mkdtemp(prefix='lettuce-')
    source_file_name = '%s/lettuce-dump.html' % dump_dir
    with open(source_file_name, 'w') as fobj:
        fobj.write(world.browser.page_source.encode('utf-8'))
    image_file_name = '%s/lettuce-dump.png' % dump_dir
    world.browser.save_screenshot(image_file_name)
    print
    print 'Screenshot dumped in %s' % dump_dir
    print
