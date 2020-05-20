import pytest
from base_tester import BasePytestFixtureChecker


class TestRedefinedOuterName(BasePytestFixtureChecker):
    MSG_ID = 'redefined-outer-name'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_smoke(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=0 if enable_plugin else 1,
        )

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_caller_yield_fixture(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=0 if enable_plugin else 1,
        )

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_caller_not_a_test_func(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=1,
        )

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_args_and_kwargs(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=2,
        )
