import pytest


@pytest.fixture
def first():
    return "OK"


@pytest.mark.usefixtures("first")
def test_first():
    pass
