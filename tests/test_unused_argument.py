import pytest
from base_tester import BasePytestFixtureChecker


class TestUnusedArgument(BasePytestFixtureChecker):
    MSG_ID = 'unused-argument'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_smoke(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=0 if enable_plugin else 2,
        )

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_caller_not_a_test_func(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=1,
        )
