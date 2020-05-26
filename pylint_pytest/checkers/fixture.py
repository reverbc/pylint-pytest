import os
import sys
import astroid
import pylint
from pylint.checkers.variables import VariablesChecker
from pylint.interfaces import IAstroidChecker
import pytest
from ..utils import _can_use_fixture, _is_same_module, _is_pytest_mark_usefixtures, _is_pytest_fixture
from . import BasePytestChecker


class FixtureCollector:
    fixtures = {}

    def pytest_sessionfinish(self, session):
        # pylint: disable=protected-access
        self.fixtures = session._fixturemanager._arg2fixturedefs


class FixtureChecker(BasePytestChecker):
    __implements__ = IAstroidChecker
    msgs = {
        'W6401': (
            'Using a deprecated @pytest.yield_fixture decorator',
            'deprecated-pytest-yield-fixture',
            'Used when using a deprecated pytest decorator that has been deprecated in pytest-3.0'
        ),
    }

    _pytest_fixtures = {}
    _invoked_with_func_args = set()
    _invoked_with_usefixtures = set()
    _original_add_message = callable

    def open(self):
        # patch VariablesChecker.add_message
        FixtureChecker._original_add_message = VariablesChecker.add_message
        VariablesChecker.add_message = FixtureChecker.patch_add_message

    def close(self):
        '''restore & reset class attr for testing'''
        # restore add_message
        VariablesChecker.add_message = FixtureChecker._original_add_message
        FixtureChecker._original_add_message = callable

        # reset fixture info storage
        FixtureChecker._pytest_fixtures = {}
        FixtureChecker._invoked_with_func_args = set()
        FixtureChecker._invoked_with_usefixtures = set()

    def visit_module(self, node):
        '''
        - only run once per module
        - invoke pytest session to collect available fixtures
        - create containers for the module to store args and fixtures
        '''
        # storing all fixtures discovered by pytest session
        FixtureChecker._pytest_fixtures = {}  # Dict[List[_pytest.fixtures.FixtureDef]]

        # storing all used function arguments
        FixtureChecker._invoked_with_func_args = set()  # Set[str]

        # storing all invoked fixtures through @pytest.mark.usefixture(...)
        FixtureChecker._invoked_with_usefixtures = set()  # Set[str]

        try:
            with open(os.devnull, 'w') as devnull:
                # suppress any future output from pytest
                stdout, stderr = sys.stdout, sys.stderr
                sys.stderr = sys.stdout = devnull

                # run pytest session with customized plugin to collect fixtures
                fixture_collector = FixtureCollector()
                pytest.main(
                    [node.file, '--fixtures'],
                    plugins=[fixture_collector],
                )
                FixtureChecker._pytest_fixtures = fixture_collector.fixtures
        finally:
            # restore output devices
            sys.stdout, sys.stderr = stdout, stderr

    def visit_functiondef(self, node):
        '''
        - save invoked fixtures for later use
        - save used function arguments for later use
        '''
        if _can_use_fixture(node):
            if node.decorators:
                # check all decorators
                for decorator in node.decorators.nodes:
                    if _is_pytest_mark_usefixtures(decorator):
                        # save all visited fixtures
                        for arg in decorator.args:
                            self._invoked_with_usefixtures.add(arg.value)
                    if int(pytest.__version__.split('.')[0]) >= 3 and \
                            _is_pytest_fixture(decorator, fixture=False):
                        # raise deprecated warning for @pytest.yield_fixture
                        self.add_message('deprecated-pytest-yield-fixture', node=node)
            for arg in node.args.args:
                self._invoked_with_func_args.add(arg.name)

    # pylint: disable=protected-access,bad-staticmethod-argument
    @staticmethod
    def patch_add_message(self, msgid, line=None, node=None, args=None,
                          confidence=None, col_offset=None):
        '''
        - intercept and discard unwanted warning messages
        '''
        # check W0611 unused-import
        if msgid == 'unused-import':
            # actual attribute name is not passed as arg so...dirty hack
            # message is usually in the form of '%s imported from %s (as %)'
            message_tokens = args.split()
            fixture_name = message_tokens[0]

            # ignoring 'import %s' message
            if message_tokens[0] == 'import' and len(message_tokens) == 2:
                pass

            # imported fixture is referenced in test/fixture func
            elif fixture_name in FixtureChecker._invoked_with_func_args \
                    and fixture_name in FixtureChecker._pytest_fixtures:
                if _is_same_module(fixtures=FixtureChecker._pytest_fixtures,
                                   import_node=node,
                                   fixture_name=fixture_name):
                    return

            # fixture is referenced in @pytest.mark.usefixtures
            elif fixture_name in FixtureChecker._invoked_with_usefixtures \
                    and fixture_name in FixtureChecker._pytest_fixtures:
                if _is_same_module(fixtures=FixtureChecker._pytest_fixtures,
                                   import_node=node,
                                   fixture_name=fixture_name):
                    return

        # check W0613 unused-argument
        if msgid == 'unused-argument' and \
                _can_use_fixture(node.parent.parent) and \
                isinstance(node.parent, astroid.Arguments) and \
                node.name in FixtureChecker._pytest_fixtures:
            return

        # check W0621 redefined-outer-name
        if msgid == 'redefined-outer-name' and \
                _can_use_fixture(node.parent.parent) and \
                isinstance(node.parent, astroid.Arguments) and \
                node.name in FixtureChecker._pytest_fixtures:
            return

        if int(pylint.__version__.split('.')[0]) >= 2:
            FixtureChecker._original_add_message(
                self, msgid, line, node, args, confidence, col_offset)
        else:
            # python2 + pylint1.9 backward compatibility
            FixtureChecker._original_add_message(
                self, msgid, line, node, args, confidence)
