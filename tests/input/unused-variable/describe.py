import pytest

def describe_stuff():
    @pytest.fixture()
    def fix():
        pass

    def run(fix):
        pass