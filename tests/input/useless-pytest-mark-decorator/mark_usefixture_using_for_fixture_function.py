import pytest


@pytest.fixture(scope="session")
def first():
    return "OK"


@pytest.fixture(scope="function")
@pytest.mark.usefixtures("first")
def second():
    return "NOK"


@pytest.mark.usefixtures("first")
@pytest.fixture(scope="function")
def third():
    return "NOK"
