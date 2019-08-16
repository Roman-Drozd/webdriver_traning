import pytest

from tests.common import BaseTest
from .data_providers import valid_customers


@pytest.mark.parametrize("customer", valid_customers, ids=[repr(x) for x in valid_customers])
def test_can_register_customer(app, customer):
    old_ids = app.get_customer_ids()

    app.register_new_customer(customer)

    new_ids = app.get_customer_ids()

    assert all([i in new_ids for i in old_ids])
    assert len(new_ids) == len(old_ids) + 1


class TestClass1(BaseTest):
    def test_1_1(self, driver):
        driver.instance.get('http://lessons2.ru')

    def test_1_2(self, driver):
        driver.instance.get('http://automated-testing.info')
