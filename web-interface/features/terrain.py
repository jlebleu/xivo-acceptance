# -*- coding: utf-8 -*-
import time

from lettuce import before, after, world
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from xivobrowser import XiVOBrowser

@before.all
def setup_browser():
    from pyvirtualdisplay import Display
    Display(visible=0, size=(1024, 768)).start()
    world.browser = XiVOBrowser()
    world.wait_for_id = _wait_for_id
    world.wait_for_name = _wait_for_name
    world.wait_for_xpath = _wait_for_xpath
    world.wait_for_alert = _wait_for_alert

@before.all
def setup_login_infos():
    world.login = 'root'
    world.password = 'superpass'
    world.host = 'http://skaro-daily.lan-quebec.avencall.com/'

# Use this if you want to debug your test
# Call it with world.dump_current_page()
@world.absorb
def dump_current_page(filename='/tmp/lettuce.html'):
    world.wait_for_id('version-copyright', 'Page not loaded')
    f = open(filename, 'w')
    f.write(world.browser.page_source.encode('utf-8'))
    f.close()

@after.all
def teardown_browser(total):
    world.browser.quit()

def _wait_for_id(elementId, message='', timeout=5):
    try:
        WebDriverWait(world.browser, timeout).until(lambda browser : browser.find_element_by_id(elementId))
        element = world.browser.find_element_by_id(elementId)
        WebDriverWait(world.browser, timeout).until(lambda browser : element.is_displayed())
    except TimeoutException:
        raise Exception(elementId, message)
    finally:
        pass

def _wait_for_name(element_name, message='', timeout=5):
    try:
        WebDriverWait(world.browser, timeout).until(lambda browser : browser.find_element_by_name(element_name))
        element = world.browser.find_element_by_name(element_name)
        WebDriverWait(world.browser, timeout).until(lambda browser : element.is_displayed())
    except TimeoutException:
        raise Exception(element_name, message)
    finally:
        pass

def _wait_for_xpath(xpath, message='', timeout=5):
    try:
        WebDriverWait(world.browser, timeout).until(lambda browser : browser.find_element_by_xpath(xpath))
    except TimeoutException:
        raise Exception(xpath, message)
    finally:
        pass

def _wait_for_alert(message='No alert', timeout=5):
    count = 0
    while count < timeout:
        alert = world.browser.switch_to_alert();
        if alert:
            time.sleep(1)
            return alert
        count += 1
        time.sleep(1)
    raise Exception(message)
