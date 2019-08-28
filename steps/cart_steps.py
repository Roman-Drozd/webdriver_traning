from pages.cart_page import CartPage
from pages.header_menu import HeaderMenu
from pages.main_page import MainPage
from pages.product_page import ProductPage


class CartSteps:
    def __init__(self, app):
        self.app = app
        self.main_page = MainPage(self.app.driver)
        self.product_page = ProductPage(self.app.driver)
        self.header_menu = HeaderMenu(self.app.driver)
        self.cart_page = CartPage(self.app.driver)

    def add_product_to_cart(self):
        self.main_page.open()
        items_in_cart_old = int(self.header_menu.items_in_cart.text)
        self.main_page.products[0].click()
        self.product_page.select_product_size()
        self.product_page.add_to_cart_button.click()
        self.product_page.close_product_alert()
        self.app.driver.refresh()
        self.header_menu.is_item_in_cart_increase(items_in_cart_old)

    def get_product_number_in_cart(self):
        self.cart_page.open()
        return len(self.cart_page.cart_items)

    def remove_product_from_cart(self):
        self.cart_page.open()
        return self.cart_page.remove_item_from_cart()
