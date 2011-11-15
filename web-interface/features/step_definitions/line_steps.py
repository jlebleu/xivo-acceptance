from lettuce.decorators import step
from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

LINE_ADD_URL = 'service/ipbx/index.php/pbx_settings/lines/?act=add&proto='

@step(u'When I create a (.*) line in context (.*)')
def when_i_create_a_line_in_context(step, protocol, context):
    world.browser.get('%s%s%s' % (world.url, LINE_ADD_URL, protocol.lower()))
    world.waitFor('it-protocol-context', 'Line form not loaded')
    input_context = world.browser.find_element_by_id('it-protocol-context')
    select_context = Select(input_context)
    select_context.select_by_value(context)
    # Get the id to reference the line
    world.id = world.browser.find_element_by_id('it-protocol-name').get_attribute('value')
    world.browser.find_element_by_id('it-submit').click()

@step(u'Then the list of lines has the lines:')
def then_the_list_of_lines_has_the_lines(step):
    world.waitFor('table-main-listing', 'Line list not loaded')
    assert world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % world.id) is not None

@step(u'When I remove this line')
def when_i_remove_this_line(step):
    delete_button = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]//a[@title='Delete']" % world.id)
    delete_button.click()
    alert = world.browser.switch_to_alert()
    alert.accept()

def _line_not_in_list():
    world.waitFor('table-main-listing', 'Line list not loaded')
    try:
        line = world.browser.find_element_by_xpath("//table[@id='table-main-listing']//tr[contains(.,'%s')]" % world.id)
        return line is None
    except NoSuchElementException:
        return True

@step(u'Then this line is not displayed in the list')
def then_this_line_is_not_displayed_in_the_list(step):
    assert _line_not_in_list()