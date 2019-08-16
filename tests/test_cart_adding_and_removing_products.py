import pytest

from app.application import Application
from tests.common import BaseTest
from .data_providers import valid_product_count


class TestProducts(BaseTest):
    @pytest.mark.parametrize("product_count", valid_product_count, ids=[repr(x) for x in valid_product_count])
    def test_can_add_and_remove_products(self, driver, product_count):
        app = Application(driver)
        for i in range(product_count):
            app.add_product_to_cart()

        products_in_cart = app.get_product_number_in_cart()
        for i in range(products_in_cart):
            products_in_cart_new = app.remove_product_from_cart()
            products_in_cart -= 1
            assert products_in_cart == products_in_cart_new
