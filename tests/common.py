import pytest


class BaseTest(object):

    @pytest.fixture(scope="class", autouse=True)
    def manage_driver(self, request, driver):
        driver.start()
        request.addfinalizer(driver.stop)
