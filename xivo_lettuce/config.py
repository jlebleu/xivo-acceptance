# -*- coding: utf-8 -*-

# Copyright (C) 2014 Avencall
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

import ConfigParser
import os
import sys
import xivo_ws
import logging

from sqlalchemy.exc import OperationalError
from execnet.multi import makegateway

from xivo_dao.helpers import config as dao_config
from xivo_dao.helpers import db_manager
from xivo_lettuce.ssh import SSHClient
from xivo_lettuce.ws_utils import RestConfiguration, WsUtils
from xivo_lettuce import postgres
from provd.rest.client.client import new_provisioning_client

logger = logging.getLogger('acceptance')


_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_CONFIG_DIR = os.path.join(_ROOT_DIR, 'config')
_ASSETS_DIR = os.path.join(_ROOT_DIR, 'assets')
_GLOBAL_CONFIG_DIR = os.path.join(sys.prefix, 'etc', 'xivo-acceptance')
_GLOBAL_ASSETS_DIR = os.path.join(sys.prefix, 'share', 'xivo-acceptance', 'assets')


def read_config():
    config_dir = _find_first_existing_path(_CONFIG_DIR, _GLOBAL_CONFIG_DIR)

    print 'Using configuration dir %s' % config_dir

    config_dird = os.path.join(config_dir, 'conf.d')
    config_file_default = os.path.join(config_dir, 'default.ini')

    config = ConfigParser.RawConfigParser()

    with open(config_file_default) as fobj:
        config.readfp(fobj)

    config_file_extra_absolute = os.getenv('LETTUCE_CONFIG', 'invalid_file_name')
    config_file_extra_in_dird = os.path.join(config_dird, os.getenv('LETTUCE_CONFIG', 'invalid_file_name'))
    config_file_extra_default = os.path.join(config_dird, 'default')
    config_file_extra_local = '%s.local' % config_file_extra_default
    config_file_extra = _find_first_existing_path(config_file_extra_absolute,
                                                  config_file_extra_in_dird,
                                                  config_file_extra_local,
                                                  config_file_extra_default)

    print 'Using extra configuration file %s' % config_file_extra

    with open(config_file_extra) as fobj:
        config.readfp(fobj)

    return config


def _find_first_existing_path(*args):
    for path in args:
        if path and os.path.exists(path):
            return path
    raise Exception('Directories do not exist: %s' % ' '.join(args))


class XivoAcceptanceConfig(object):

    def __init__(self, raw_config):
        self._config = raw_config
        logger.info("Configuring xivo-acceptance...")

        self.asset_dir = _find_first_existing_path(_ASSETS_DIR, _GLOBAL_ASSETS_DIR)

        self.dao_engine = None
        self.rest_provd = None
        self.provd_client = None
        self.ws_utils = None
        self.confd_utils_1_1 = None
        self.xivo_configured = None

        self.xivo_host = self._config.get('xivo', 'hostname')

        self.ssh_login = self._config.get('ssh_infos', 'login')

        self.browser_enable = self._config.getboolean('browser', 'enable')
        self.browser_visible = self._config.getboolean('browser', 'visible')
        self.browser_timeout = self._config.getint('browser', 'timeout')
        self.browser_resolution = self._config.get('browser', 'resolution')

        self.webi_url = 'https://%s' % self.xivo_host
        self.webi_login = self._config.get('login_infos', 'login')
        self.webi_password = self._config.get('login_infos', 'password')

        self.rest_username = self._config.get('webservices_infos', 'login')
        self.rest_passwd = self._config.get('webservices_infos', 'password')
        self.rest_protocol = self._config.get('confd', 'protocol')
        self.rest_port = self._config.getint('confd', 'port')

        self.xc_login_timeout = self._config.getint('xivo_client', 'login_timeout')

        self.kvm_hostname = self._config.get('kvm_infos', 'hostname')
        self.kvm_login = self._config.get('kvm_infos', 'login')
        self.kvm_vm_name = self._config.get('kvm_infos', 'vm_name')
        self.kvm_shutdown_timeout = int(self._config.get('kvm_infos', 'shutdown_timeout'))
        self.kvm_boot_timeout = int(self._config.get('kvm_infos', 'boot_timeout'))

        self.linphone_sip_port_range = self._config.get('linphone', 'sip_port_range')
        self.linphone_rtp_port_range = self._config.get('linphone', 'rtp_port_range')

        self.linphone_debug = self._config.getboolean('debug', 'linphone')
        self.browser_debug = self._config.getboolean('debug', 'selenium')

        self.subnets = self._config.get('prerequisites', 'subnets').split(',')

    def setup(self):
        self._setup_dao()
        self._setup_ssh_client()
        self._setup_ws()
        self._setup_provd()
        self._setup_webi()

    def _setup_webi(self):
        try:
            command = ['test', '-e', '/var/lib/xivo/configured']
            self.ssh_client_xivo.check_call(command)
        except Exception:
            self.xivo_configured = False
        else:
            self.xivo_configured = True

    def _setup_dao(self):
        dao_config.DB_URI = 'postgresql://asterisk:proformatique@%s/asterisk' % self.xivo_host
        db_manager.reinit()
        try:
            self.dao_engine = db_manager._dao_engine
        except OperationalError:
            logging.exception('PGSQL ERROR: could not connect to server')

    def _setup_ssh_client(self):
        self.ssh_client_xivo = SSHClient(self.xivo_host, self.ssh_login)

    def _setup_ws(self):
        rest_config_dict = {
            'protocol': self.rest_protocol,
            'hostname': self.xivo_host,
            'port': self.rest_port,
            'auth_username': self.rest_username,
            'auth_passwd': self.rest_passwd
        }

        rest_config_dict.update({'api_version': '1.1'})
        self.confd_config_1_1 = RestConfiguration(**rest_config_dict)

        self.ws_utils = xivo_ws.XivoServer(self.xivo_host,
                                           self.rest_username,
                                           self.rest_passwd)
        self.confd_utils_1_1 = WsUtils(self.confd_config_1_1)

    def _setup_provd(self):
        provd_rest_port = 8667
        try:
            query = 'SELECT * FROM "provisioning" WHERE id = 1;'
            result = postgres.exec_sql_request(query).fetchone()
            provd_rest_port = result['http_port']
        except OperationalError:
            pass

        provd_config_obj = RestConfiguration(protocol='http',
                                             hostname=self.xivo_host,
                                             port=provd_rest_port,
                                             content_type='application/vnd.proformatique.provd+json')
        self.rest_provd = WsUtils(provd_config_obj)

        provd_url = "http://%s:%s/provd" % (self.xivo_host, provd_rest_port)
        self.provd_client = new_provisioning_client(provd_url)

    @property
    def execnet_gateway(self):
        try:
            return self._execnet_gateway
        except AttributeError:
            self._execnet_gateway = makegateway('ssh=%s@%s' % (self.ssh_login, self.xivo_host))
            return self._execnet_gateway
