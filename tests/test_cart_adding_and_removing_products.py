import pytest

from .data_providers import valid_product_count


@pytest.mark.parametrize("product_count", valid_product_count, ids=[repr(x) for x in valid_product_count])
def test_can_add_and_remove_products(app, product_count):
    for i in range(product_count):
        app.cart_steps.add_product_to_cart()

    products_in_cart = app.cart_steps.get_product_number_in_cart()
    for i in range(products_in_cart):
        products_in_cart_new = app.cart_steps.remove_product_from_cart()
        products_in_cart -= 1
        assert products_in_cart == products_in_cart_new
