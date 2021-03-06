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

import logging

import os
import subprocess
import socket
import json
import time
import errno
import uuid

import pprint
from lettuce import before, after, world

logger = logging.getLogger('acceptance')


class XivoClient(object):

    environment_variables = os.environ
    environment_variables['LD_LIBRARY_PATH'] = '.'
    xc_path = os.environ['XC_PATH'] + '/'
    arguments = []
    socket = None
    process = None
    socket_dir = '/tmp'
    socket_name = ''
    socket_path = ''

    def __init__(self, argument='', name='default', debug=False):
        self.arguments.append(argument)
        uid = uuid.uuid4()
        self.socket_name = 'xc-%s-%s.sock' % (name, uid.hex)
        self.socket_path = os.path.join(self.socket_dir, self.socket_name)
        self.debug = debug

    def start(self):
        self.launch()
        # Waiting for the listening socket to open
        time.sleep(1)
        return self.listen_socket()

    def stop(self):
        logger.debug('-------------------- STOP CLIENT ---------------------')
        self.process.terminate()
        self.process = None
        self.socket.close()
        self.socket = None
        try:
            logger.debug('-------------------- REMOVE SOCKET %s ---------------------', self.socket_path)
            os.remove(self.socket_path)
        except OSError:
            pass

    def clean(self):
        self.process.poll()
        if self.process.returncode is None:
            self.exec_command('i_stop_the_xivo_client')
        self.stop()

    def launch(self):
        logger.debug('-------------------- LAUNCHING CLIENT ---------------------')
        try:
            args = ['./xivoclient']
            args.extend(self.arguments)
            args.append('socket:%s' % self.socket_path)
            self.process = subprocess.Popen(args,
                                            cwd=self.xc_path,
                                            env=self.environment_variables)
        except OSError as e:
            if e.errno == errno.ENOENT:
                raise Exception('XiVO Client executable not found')
            else:
                raise

    def listen_socket(self):
        logger.debug('-------------------- LISTENNING SOCKET: %s ---------------------', self.socket_path)
        self.socket = socket.socket(socket.AF_UNIX)
        try:
            self.socket.connect(self.socket_path)
        except socket.error as(error_number, message):
            if error_number == errno.ENOENT:
                msg = 'XiVO Client multiples instance is disabled or'
                msg += ' XiVO Client must be built for functional testing'
                logger.info(msg)
                return False
            else:
                raise Exception(message)
        return True

    def exec_command(self, cmd, *kargs):
        formatted_command = self._format_command(cmd, kargs)
        return self._send_and_receive_command(formatted_command)

    def _format_command(self, function_name, arguments):
        command = {'function_name': function_name,
                   'arguments': arguments}
        formatted_command = json.dumps(command)
        return formatted_command

    def _send_and_receive_command(self, formatted_command):
        self._send_command(formatted_command)
        response_raw = self._receive_command()
        response_decoded = self._decode_response(response_raw)
        return response_decoded

    def _send_command(self, formatted_command):
        logger.debug('-------------------- MSG SENT ---------------------')
        logger.debug(pprint.pformat(formatted_command))
        logger.debug('-------------------- END MSG ----------------------')
        self.socket.send('%s\n' % formatted_command)

    def _receive_command(self):
        socket_buffer = self.socket.makefile()
        response_raw = str(socket_buffer.readline())
        socket_buffer.close()
        logger.debug('------------------ RAW RESPONSE -------------------')
        logger.debug(pprint.pformat((response_raw)))
        logger.debug('------------------ END RESPONSE -------------------')
        return response_raw

    def _decode_response(self, response_raw):
        response_dict = json.loads(response_raw)
        logger.debug('---------------- DECODED RESPONSE -----------------')
        logger.debug(pprint.pformat(response_dict))
        logger.debug('------------------ END RESPONSE -------------------')
        return response_dict


@before.each_scenario
def setup_xivoclient_rc(scenario):
    world.xc_process_dict = {}
    world.xc_instance = None
    world.xc_result = None


@after.each_scenario
def clean_xivoclient_rc(scenario):
    if world.xc_process_dict:
        for xc_name in world.xc_process_dict.iterkeys():
            world.xc_process_dict[xc_name].clean()


def exec_command(cmd, *kargs):
    return world.xc_instance.exec_command(cmd, *kargs)


def start_xivoclient(argument='', name='default'):
    if name not in world.xc_process_dict:
        client_obj = XivoClient(argument, name=name)
        if client_obj.start():
            world.xc_process_dict[name] = client_obj
            if name == 'default':
                world.xc_instance = world.xc_process_dict[name]


def stop_xivoclient(name='default'):
    if name in world.xc_process_dict:
        world.xc_process_dict[name].stop()
        del world.xc_process_dict[name]
