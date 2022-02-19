import pytest

def describe_stuff():
    @pytest.fixture()
    def fix():
        pass

    def context_more():
        def run(fix):
            pass