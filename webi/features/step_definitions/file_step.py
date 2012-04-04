# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager import file_manager


@step(u'Given a recording file with name "([^"]*)"')
def given_a_recording_file_with_name(step, filename):
    file_manager.check_recordings_file(filename)


@step(u'Given a musiconhold file with name "([^"]*)"')
def given_a_musiconhold_file_with_name(step, filename):
    file_manager.check_musiconhold_file(filename)