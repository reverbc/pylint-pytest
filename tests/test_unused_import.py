import pytest
from pylint.checkers.variables import VariablesChecker
from base_tester import BasePytestChecker


class TestUnusedImport(BasePytestChecker):
    CHECKER_CLASS = VariablesChecker
    MSG_ID = 'unused-import'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_smoke(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0 if enable_plugin else 1)

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_caller_yield_fixture(self, enable_plugin):
        self.run_linter(enable_plugin)
        self.verify_messages(0 if enable_plugin else 1)

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_same_name_arg(self, enable_plugin):
        '''an unused import (not a fixture) just happened to have the same
        name as fixture - should still raise unused-import warning'''
        self.run_linter(enable_plugin)
        self.verify_messages(1)

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_same_name_decorator(self, enable_plugin):
        '''an unused import (not a fixture) just happened to have the same
        name as fixture - should still raise unused-import warning'''
        self.run_linter(enable_plugin)
        self.verify_messages(1)
