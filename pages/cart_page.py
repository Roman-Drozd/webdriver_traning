from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver.instance, 10)

    def open(self):
        self.driver.instance.get('http://localhost/litecart/en/checkout')
        return self

    @property
    def cart_items(self):
        return self.driver.instance.find_elements_by_css_selector('td.item')

    def remove_item_from_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[value=Remove]'))).click()
        self.wait.until(EC.staleness_of(self.cart_items[0]))
        return len(self.cart_items)
