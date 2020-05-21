import sys
import os
from pylint.testutils import CheckerTestCase
from pylint.checkers.variables import VariablesChecker
import astroid
from pylint_pytest import register, unregister


class BasePytestFixtureChecker(CheckerTestCase):
    CHECKER_CLASS = VariablesChecker
    MSG_ID = None

    def _verify(self, module, msg_count, msg_id=None):
        self.walk(module)  # run all checkers
        messages = self.linter.release_messages()
        msg_id = msg_id or self.MSG_ID

        matched_count = 0
        for message in messages:
            print(message)
            # only care about ID and count, not the content
            if message.msg_id == msg_id:
                matched_count += 1

        assert matched_count == msg_count

    def run_test(self, msg_count, enable_plugin, msg_id=None):
        # pylint: disable=protected-access
        file = sys._getframe(1).f_code.co_name.replace('test_', '', 1) + '.py'
        full_file_path = os.path.join(
            os.getcwd(), 'tests', 'input', self.MSG_ID, file)
        with open(full_file_path) as fin:
            content = fin.read()
            module = astroid.parse(content)
            module.file = fin.name

            if enable_plugin:
                register(None)

            try:
                self._verify(
                    module=module,
                    msg_count=msg_count,
                    msg_id=msg_id,
                )
            finally:
                if enable_plugin:
                    unregister()
