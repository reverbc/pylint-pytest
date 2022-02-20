import pytest

from base_tester import BasePytestTester
from pylint_pytest.checkers.fixture import FixtureChecker


class TestDeprecatedPytestYieldFixture(BasePytestTester):
    CHECKER_CLASS = FixtureChecker
    IMPACTED_CHECKER_CLASSES = []
    MSG_ID = 'deprecated-pytest-yield-fixture'

    @pytest.fixture
    def enable_plugin(self):
        return True

    def test_smoke(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(1)

    def test_func(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(2)
