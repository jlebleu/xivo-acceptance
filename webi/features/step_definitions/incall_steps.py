# -*- coding: utf-8 -*-

from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.common import *
from xivo_lettuce.manager import context_manager as ctx_man
from xivo_lettuce.manager import incall_manager as incall_man


@step(u'Given there is no incall with DID "([^"]*)"')
def given_there_is_no_incall_with_did(step, did):
    incall_man.remove_incall_with_did(did)


@step(u'When I create an incall with DID "([^"]*)"')
def when_i_create_incall_with_did(step, incall_did):
    ctx_man.check_context_number_in_interval('from-extern', 'incall', incall_did)
    open_url('incall', 'add')
    incall_man.type_incall_did(incall_did)
    submit_form()


@step(u'When incall "([^"]*)" is removed')
def when_incall_is_removed(step, incall_did):
    incall_man.remove_incall_with_did(incall_did)