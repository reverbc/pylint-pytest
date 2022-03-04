import sys
import os
from pprint import pprint

import astroid
from pylint.testutils import UnittestLinter
try:
    from pylint.utils import ASTWalker
except ImportError:
    # for pylint 1.9
    from pylint.utils import PyLintASTWalker as ASTWalker
from pylint.checkers import BaseChecker
import pytest

import pylint_pytest.checkers.fixture

# XXX: allow all file name
pylint_pytest.checkers.fixture.FILE_NAME_PATTERNS = ('*', )


class BasePytestTester(object):
    CHECKER_CLASS = BaseChecker
    IMPACTED_CHECKER_CLASSES = []
    MSG_ID = None
    MESSAGES = None
    CONFIG = {}

    enable_plugin = True

    def run_linter(self, enable_plugin, file_path=None):
        self.enable_plugin = enable_plugin
        self.CHECKER_CLASS.enable_plugin = enable_plugin

        # pylint: disable=protected-access
        if file_path is None:
            module = sys._getframe(1).f_code.co_name.replace('test_', '', 1)
            file_path = os.path.join(
                os.getcwd(), 'tests', 'input', self.MSG_ID, module + '.py')

        with open(file_path) as fin:
            content = fin.read()
            module = astroid.parse(content, module_name=module)
            module.file = fin.name

        self.walk(module)  # run all checkers
        self.MESSAGES = self.linter.release_messages()

    def verify_messages(self, msg_count, msg_id=None):
        msg_id = msg_id or self.MSG_ID

        matched_count = 0
        for message in self.MESSAGES:
            # only care about ID and count, not the content
            if message.msg_id == msg_id:
                matched_count += 1

        pprint(self.MESSAGES)
        assert matched_count == msg_count, f'expecting {msg_count}, actual {matched_count}'

    @pytest.fixture(scope="function", autouse=True)
    def within(self, request, enable_plugin):
        try:
            request.instance._setup_method(enable_plugin)
            yield request.instance
        finally:
            request.instance._teardown_method(enable_plugin)


    def _setup_method(self, enable_plugin):
        self.linter = UnittestLinter()
        self.impacted_checkers = []

        if enable_plugin:
            self.checker = self.CHECKER_CLASS(self.linter)
            for key, value in self.CONFIG.items():
                setattr(self.checker.config, key, value)
            self.checker.open()

        for checker_class in self.IMPACTED_CHECKER_CLASSES:
            checker = checker_class(self.linter)
            for key, value in self.CONFIG.items():
                setattr(checker.config, key, value)
            checker.open()
            self.impacted_checkers.append(checker)

    def _teardown_method(self, enable_plugin):
        if enable_plugin:
            self.checker.close()
        for checker in self.impacted_checkers:
            checker.close()

    def walk(self, node):
        """recursive walk on the given node"""
        walker = ASTWalker(self.linter)
        if self.enable_plugin:
            walker.add_checker(self.checker)
        for checker in self.impacted_checkers:
            walker.add_checker(checker)
        walker.walk(node)
