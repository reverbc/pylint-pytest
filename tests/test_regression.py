import pytest
from base_tester import BasePytestFixtureChecker


class TestRegression(BasePytestFixtureChecker):
    '''Covering some behaviors that shouldn't get impacted by the plugin'''
    MSG_ID = 'regression'

    @pytest.mark.parametrize('enable_plugin', [True, False])
    def test_import_twice(self, enable_plugin):
        '''catch a coding error when using fixture + if + inline import'''
        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=2,
            msg_id='unused-import'
        )

        self.run_test(
            enable_plugin=enable_plugin,
            msg_count=1,
            msg_id='redefined-outer-name'
        )
