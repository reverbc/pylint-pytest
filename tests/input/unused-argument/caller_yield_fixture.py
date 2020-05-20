import pytest
from conftest import conftest_fixture_attr


@pytest.yield_fixture
def caller_yield_fixture(conftest_fixture_attr):
    assert True
