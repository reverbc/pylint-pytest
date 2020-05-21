import pytest
from base_tester import BasePytestFixtureChecker


class TestRegression(BasePytestFixtureChecker):
    '''Covering some behaviors that shouldn't get impacted by the plugin'''
    MSG_ID = 'regression'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_import_twice(self, enable_plugin):
        '''catch a coding error when using fixture + if + inline import'''
        self.run_linter(enable_plugin)
        self.verify_messages(2, msg_id='unused-import')
        self.verify_messages(1, msg_id='redefined-outer-name')
