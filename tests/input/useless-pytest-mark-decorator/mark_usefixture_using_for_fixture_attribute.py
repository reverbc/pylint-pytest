import pytest


@pytest.fixture
def first():
    return "OK"


@pytest.fixture
@pytest.mark.usefixtures("first")
def second():
    return "NOK"


@pytest.mark.usefixtures("first")
@pytest.fixture
def third():
    return "NOK"
