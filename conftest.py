import datetime

from selenium import webdriver
import pytest
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


class DriverManager:

    def __init__(self):
        self._instance = None

    def start(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        self._instance = EventFiringWebDriver(webdriver.Chrome(options=options), MyListener())
        return self._instance

    @property
    def instance(self):
        if not self._instance:
            self.start()
        return self._instance

    def stop(self):
        self._instance.close()


@pytest.fixture(scope="module")
def driver():
    return DriverManager()


