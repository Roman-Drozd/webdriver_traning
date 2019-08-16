from selenium.webdriver.support.wait import WebDriverWait


class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.instance.get('http://localhost/litecart/en/')
        return self

    @property
    def products(self):
        return self.driver.instance.find_elements_by_class_name("product")
