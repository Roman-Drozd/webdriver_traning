import datetime

from selenium import webdriver
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from steps.cart_steps import CartSteps
from steps.registration_steps import CustomerSteps


class MyListener(AbstractEventListener):
    def before_find(self, by, value, driver):
        print(by, value)

    def after_find(self, by, value, driver):
        print(by, value, "found")

    def on_exception(self, exception, driver):
        print(exception)
        now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        driver.get_screenshot_as_file(('screenshots/{}_screen_{}.png'.format(__name__, now)))


class Application:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.driver = EventFiringWebDriver(webdriver.Chrome(options=self.options), MyListener())
        self.registration_steps = CustomerSteps(self)
        self.cart_steps = CartSteps(self)

    def is_valid(self):
        try:
            self.driver.current_url
            return True
        except:
            return False

    def quit(self):
        self.driver.quit()


