import pytest
from app.application import Application


fixture = None


@pytest.fixture
def app():
    global fixture
    if fixture is None:
        fixture = Application()
    elif not fixture.is_valid():
        fixture = Application()
    return fixture


@pytest.fixture(scope='session', autouse=True)
def stop(request):
    def fin():
        fixture.quit()
    request.addfinalizer(fin)
    return fixture
