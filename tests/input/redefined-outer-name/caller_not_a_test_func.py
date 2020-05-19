import pytest


@pytest.fixture
def this_is_a_fixture():
    return True


def not_a_test_function(this_is_a_fixture):
    # invalid test case...
    assert True
