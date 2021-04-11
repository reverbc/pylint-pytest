import pytest


@pytest.fixture
def first():
    return "OK"


@pytest.mark.usefixtures("first")
class TestFirst:
    @staticmethod
    def do():
        return True

    def test_first(self):
        assert self.do() is True
