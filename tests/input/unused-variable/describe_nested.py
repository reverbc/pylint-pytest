import pytest

def describe_stuff():
    @pytest.fixture()
    def fix():
        pass

    def context_more():
        @pytest.fixture()
        def fix(fix):
            pass

        def run(fix):
            pass