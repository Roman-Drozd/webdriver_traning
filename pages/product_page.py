from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def select_product_size(self):
        if len(self.driver.find_elements_by_tag_name('select')) != 0:
            Select(self.driver.find_element_by_tag_name('select')).select_by_value('Small')

    @property
    def add_to_cart_button(self):
        return self.driver.find_element_by_css_selector('[name=add_cart_product]')

    def close_product_alert(self):
        alert = self.wait.until(EC.alert_is_present())
        alert.dismiss()
