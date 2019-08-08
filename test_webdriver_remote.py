import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)

    def after_find(self, by, value, driver):
        print(by, value, "found")

    def on_exception(self, exception, driver):
        print(exception)
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        driver.get_screenshot_as_file(('screenshots/{}_screen_{}.png'.format(__name__, now)))


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    wd = EventFiringWebDriver(webdriver.Remote("http://192.168.1.148:4444/wd/hub",
                                               desired_capabilities={"browserName": "chrome"},
                                               options=options), MyListener())
    # wd = webdriver.Remote("http://192.168.1.148:4444/wd/hub",
    #                       desired_capabilities={"browserName": "chrome", "platform": "WINDOWS"})
    request.addfinalizer(wd.quit)
    return wd


def test_admin_menu_items(driver):
    driver.implicitly_wait(10)
    driver.get('http://selenium2.org')