from base_tester import BasePytestTester
from pylint_pytest.checkers.fixture import FixtureChecker


class TestPytestMarkUsefixtures(BasePytestTester):
    CHECKER_CLASS = FixtureChecker
    MSG_ID = 'useless-pytest-usefixtures-decorator'

    def test_mark_usefixture_uses_for_test(self):
        self.run_linter(enable_plugin=True)
        self.verify_messages(0)

    def test_mark_usefixture_uses_for_class(self):
        self.run_linter(enable_plugin=True)
        self.verify_messages(0)

    def test_mark_usefixture_uses_for_fixture_attribute(self):
        self.run_linter(enable_plugin=True)
        self.verify_messages(2)

    def test_mark_usefixture_uses_for_fixture_function(self):
        self.run_linter(enable_plugin=True)
        self.verify_messages(2)
