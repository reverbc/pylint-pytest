import pytest
from pylint.checkers.variables import VariablesChecker
from base_tester import BasePytestTester
from pylint_pytest.checkers.fixture import FixtureChecker


class TestUnusedVariable(BasePytestTester):
    CHECKER_CLASS = FixtureChecker
    IMPACTED_CHECKER_CLASSES = [VariablesChecker]
    MSG_ID = 'unused-variable'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_describe(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0 if enable_plugin else 1)

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_describe_nested(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0 if enable_plugin else 2)
