import pytest

from base_tester import BasePytestTester
from pylint_pytest.checkers.fixture import FixtureChecker


class TestPytestMarkUsefixtures(BasePytestTester):
    CHECKER_CLASS = FixtureChecker
    MSG_ID = 'useless-pytest-mark-decorator'

    @pytest.fixture
    def enable_plugin(self):
        return True

    def test_mark_usefixture_using_for_test(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0)

    def test_mark_usefixture_using_for_class(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0)

    def test_mark_usefixture_using_for_fixture_attribute(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(2)

    def test_mark_usefixture_using_for_fixture_function(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(2)

    def test_other_marks_using_for_fixture(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(4)

    def test_not_pytest_marker(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0)
