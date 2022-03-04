import pytest

from base_tester import BasePytestTester
from pylint_pytest.checkers.fixture import FixtureChecker


class TestDeprecatedPytestFixtureScopeAsPositionalParam(BasePytestTester):
    CHECKER_CLASS = FixtureChecker
    MSG_ID = 'deprecated-positional-argument-for-pytest-fixture'

    @pytest.fixture
    def enable_plugin(self):
        return True

    def test_with_args_scope(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(1)

    def test_with_kwargs_scope(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0)

    def test_without_scope(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0)
