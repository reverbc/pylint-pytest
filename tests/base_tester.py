import sys
import os
from pylint.testutils import CheckerTestCase
from pylint.checkers.variables import VariablesChecker
import astroid
from pylint_pytest import register, unregister


class BasePytestFixtureChecker(CheckerTestCase):
    CHECKER_CLASS = VariablesChecker
    MSG_ID = None
    MESSAGES = None

    def run_linter(self, enable_plugin, file_path=None):
        # pylint: disable=protected-access
        if file_path is None:
            module = sys._getframe(1).f_code.co_name.replace('test_', '', 1)
            file_path = os.path.join(
                os.getcwd(), 'tests', 'input', self.MSG_ID, module + '.py')

        with open(file_path) as fin:
            content = fin.read()
            module = astroid.parse(content)
            module.file = fin.name

            if enable_plugin:
                register(None)

            try:
                self.walk(module)  # run all checkers
                self.MESSAGES = self.linter.release_messages()
            finally:
                if enable_plugin:
                    unregister()

    def verify_messages(self, msg_count, msg_id=None):
        msg_id = msg_id or self.MSG_ID

        matched_count = 0
        for message in self.MESSAGES:
            print(message)
            # only care about ID and count, not the content
            if message.msg_id == msg_id:
                matched_count += 1

        assert matched_count == msg_count
