from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HeaderMenu:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver.instance, 10)

    @property
    def checkout_button(self):
        return self.driver.instance.find_element_by_xpath("//a[contains(text(), 'Checkout »')]")

    @property
    def items_in_cart(self):
        return self.driver.instance.find_element_by_css_selector('#cart .quantity')

    def is_item_in_cart_increase(self, items_in_cart):
        self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#cart .quantity'), str(items_in_cart + 1)))
