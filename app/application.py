from selenium import webdriver
from pages.admin_panel_login_page import AdminPanelLoginPage
from pages.cart_page import CartPage
from pages.customer_list_page import CustomerListPage
from pages.header_menu import HeaderMenu
from pages.main_page import MainPage
from pages.product_page import ProductPage
from pages.registration_page import RegistrationPage


class Application:

    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.registration_page = RegistrationPage(self.driver)
        self.admin_panel_login_page = AdminPanelLoginPage(self.driver)
        self.customer_list_page = CustomerListPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.header_menu = HeaderMenu(self.driver)
        self.cart_page = CartPage(self.driver)

    # def quit(self):
    #     self.driver.quit()

    def register_new_customer(self, customer):
        self.registration_page.open()
        self.registration_page.firstname_input.send_keys(customer.firstname)
        self.registration_page.lastname_input.send_keys(customer.lastname)
        self.registration_page.address1_input.send_keys(customer.address)
        self.registration_page.postcode_input.send_keys(customer.postcode)
        self.registration_page.city_input.send_keys(customer.city)
        # self.registration_page.select_country(customer.country)
        # self.registration_page.select_zone(customer.zone)
        self.registration_page.email_input.send_keys(customer.email)
        self.registration_page.phone_input.send_keys(customer.phone)
        self.registration_page.password_input.send_keys(customer.password)
        self.registration_page.confirmed_password_input.send_keys(customer.password)
        self.registration_page.create_account_button.click()

    def get_customer_ids(self):
        if self.admin_panel_login_page.open().is_on_this_page():
            self.admin_panel_login_page.enter_username("admin").enter_password("admin").submit_login()
        return self.customer_list_page.open().get_customer_ids()

    def add_product_to_cart(self):
        self.main_page.open()
        items_in_cart_old = int(self.header_menu.items_in_cart.text)
        self.main_page.products[0].click()
        self.product_page.select_product_size()
        self.product_page.add_to_cart_button.click()
        self.product_page.close_product_alert()
        self.driver.refresh()
        self.header_menu.is_item_in_cart_increase(items_in_cart_old)

    def get_product_number_in_cart(self):
        self.cart_page.open()
        return len(self.cart_page.cart_items)

    def remove_product_from_cart(self):
        self.cart_page.open()
        return self.cart_page.remove_item_from_cart()
