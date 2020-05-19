import pytest
from base_tester import BasePytestFixtureChecker


class TestUnusedImport(BasePytestFixtureChecker):
    MSG_ID = 'unused-import'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_smoke(self, enable_plugin):
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=0 if enable_plugin else 1,
        )

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_same_name_arg(self, enable_plugin):
        '''an unused import (not a fixture) just happened to have the same
        name as fixture - should still raise unused-import warning'''
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=1,
        )

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_same_name_decorator(self, enable_plugin):
        '''an unused import (not a fixture) just happened to have the same
        name as fixture - should still raise unused-import warning'''
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=1,
        )
