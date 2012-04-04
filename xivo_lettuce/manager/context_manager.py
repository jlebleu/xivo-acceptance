# -*- coding: utf-8 -*-

import json

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from xivo_lettuce.common import *

WS = get_webservices('context')


def delete_context(name):
    WS.delete(name)


def check_context_interval(context_name, label, start, end):
    open_url('context', 'edit', {'id': context_name})
    go_to_tab_href(label)
    tbl_user = world.browser.find_element_by_id('contextnumbers-%s' % label)
    try:
        tbl_user.find_element_by_xpath("//input[@value='%s']" % start)
        tbl_user.find_element_by_xpath("//input[@value='%s']" % end)
    except NoSuchElementException:
        return False
    return True


def check_context_number_in_interval(context_name, label, number):
    open_url('context', 'edit', {'id': context_name})
    go_to_tab_href(label)
    sel_list_interval = world.browser.find_elements_by_xpath("//input[contains(@name, 'contextnumbers[%s]')]" % label)
    if sel_list_interval:
        number = int(number)
        list_interval = interval = []
        for obj in sel_list_interval:
            value = obj.get_attribute("value")
            if not value:
                value = 0
            value = int(value)
            if number == value:
                return True
            interval.append(value)
            if len(interval) == 2:
                list_interval.append(interval)
                if number >= interval[0] and number <= interval[1]:
                    return True
                interval = []
    create_interval_for_number(label, number)


def create_interval_for_number(label, number):
    add_button = world.browser.find_element_by_xpath("//div[@id='sb-part-%s']//a[@id='add_line_button']" % label)
    add_button.click()
    tbody = world.browser.find_elements_by_xpath("//tbody[@id='contextnumbers-%s']" % label)
    for tr in tbody:
        start_field = tr.find_elements_by_xpath(".//input[@name='contextnumbers[%s][numberbeg][]']" % (label))[-1]
        start_field.clear()
        start_field.send_keys(number)
        end_field = tr.find_elements_by_xpath(".//input[@name='contextnumbers[%s][numberend][]']" % (label))[-1]
        end_field.clear()
        end_field.send_keys(number)
        if label == 'incall':
            did_length_select = tr.find_elements_by_xpath(
                './/select[@name="contextnumbers[incall][didlength][]"]//option[@value="%s"]' % len(str(number)))[-1]
            did_length_select.click()
    submit_form()


def add_context_user(name, displayname, numberbeg, numberend):
    contextnumbers_user = '"user": [{"numberbeg": "%s", "numberend": "%s"}]' % (numberbeg, numberend)
    return _add_context(name, displayname, 'internal', contextnumbers_user=contextnumbers_user)


def add_context_incall(name, displayname, numberbeg, numberend, didlength):
    contextnumbers_incall = '"incall": [{"numberbeg": "%s", "numberend": "%s", didlength: "%s"}]' % (numberbeg, numberend, didlength)
    return _add_context(name, displayname, 'incall', contextnumbers_incall=contextnumbers_incall)


def _add_context(name, displayname, contexttype, 
                 contextnumbers_user='', 
                 contextnumbers_group='', 
                 contextnumbers_meetme='', 
                 contextnumbers_queue='', 
                 contextnumbers_incall=''):
    var_context = {
                  "name": name,
                  "displayname" : displayname,
                  "entity" : 'avencall',
                  "contexttype": contexttype,
                  "contextinclude": '[]',
                  "contextnumbers_user": '',
                  "contextnumbers_group": '',
                  "contextnumbers_meetme": '',
                  "contextnumbers_queue": '',
                  "contextnumbers_incall": ''
                  }
    
    # '"user": [{"numberbeg": "600", "numberend": "699"}]'
    if contextnumbers_user:
        var_context["contextnumbers_user"] = contextnumbers_user 
    if contextnumbers_group:
        var_context["contextnumbers_group"] = contextnumbers_group 
    if contextnumbers_meetme:
        var_context["contextnumbers_meetme"] = contextnumbers_meetme 
    if contextnumbers_queue:
        var_context["contextnumbers_queue"] = contextnumbers_queue 
    if contextnumbers_incall:
        var_context["contextnumbers_incall"] = contextnumbers_incall 
    
    jsonfilecontent = WS.get_json_file_content('context');
    jsonstr = jsonfilecontent % (var_context)
    content = json.loads(jsonstr)

    response = WS.view(var_context['name'])
    if response:
        WS.delete(var_context['name'])

    return WS.add(content)