import os
import sys
import inspect

import astroid
from pylint.checkers.variables import VariablesChecker
import pylint
import pytest


def _is_pytest_mark_usefixtures(decorator):
    # expecting @pytest.mark.usefixture(...)
    try:
        if isinstance(decorator, astroid.Call):
            if decorator.func.attrname == 'usefixtures' and \
                    decorator.func.expr.attrname == 'mark' and \
                    decorator.func.expr.expr.name == 'pytest':
                return True
    except AttributeError:
        pass
    return False


def _is_pytest_fixture(decorator):
    attr = None

    try:
        if isinstance(decorator, astroid.Attribute):
            # expecting @pytest.fixture
            attr = decorator

        if isinstance(decorator, astroid.Call):
            # expecting @pytest.fixture(scope=...)
            attr = decorator.func

        if attr and attr.attrname in ('fixture', 'yield_fixture') \
                and attr.expr.name == 'pytest':
            return True
    except AttributeError:
        pass

    return False


def _can_use_fixture(function):
    if isinstance(function, astroid.FunctionDef):

        # test_*, *_test
        if function.name.startswith('test_') or function.name.endswith('_test'):
            return True

        if function.decorators:
            for decorator in function.decorators.nodes:
                # usefixture
                if _is_pytest_mark_usefixtures(decorator):
                    return True

                # fixture
                if _is_pytest_fixture(decorator):
                    return True

    return False


def _is_same_module(fixtures, import_node, fixture_name):
    '''Comparing pytest fixture node with astroid.ImportFrom'''
    try:
        for fixture in fixtures[fixture_name]:
            for import_from in import_node.root().globals[fixture_name]:
                if inspect.getmodule(fixture.func).__file__ == \
                        import_from.parent.import_module(import_from.modname,
                                                         False,
                                                         import_from.level).file:
                    return True
    except:  # pylint: disable=bare-except
        pass
    return False


# pylint: disable=protected-access
class FixtureCollector:
    fixtures = {}

    def pytest_sessionfinish(self, session):
        self.fixtures = session._fixturemanager._arg2fixturedefs


ORIGINAL = {}


def unregister():
    VariablesChecker.add_message = ORIGINAL['add_message']
    del ORIGINAL['add_message']
    VariablesChecker.visit_functiondef = ORIGINAL['visit_functiondef']
    del ORIGINAL['visit_functiondef']
    VariablesChecker.visit_module = ORIGINAL['visit_module']
    del ORIGINAL['visit_module']


# pylint: disable=protected-access
def register(_):
    '''Patch VariablesChecker to add additional checks for pytest fixtures
    '''
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def patched_visit_module(self, node):
        '''
        - only run once per module
        - invoke pytest session to collect available fixtures
        - create containers for the module to store args and fixtures
        '''
        # storing all fixtures discovered by pytest session
        self._pytest_fixtures = {}  # Dict[List[_pytest.fixtures.FixtureDef]]

        # storing all used function arguments
        self._invoked_with_func_args = set()  # Set[str]

        # storing all invoked fixtures through @pytest.mark.usefixture(...)
        self._invoked_with_usefixtures = set()  # Set[str]

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
                self._pytest_fixtures = fixture_collector.fixtures
        finally:
            # restore output devices
            sys.stdout, sys.stderr = stdout, stderr

        ORIGINAL['visit_module'](self, node)
    ORIGINAL['visit_module'] = VariablesChecker.visit_module
    VariablesChecker.visit_module = patched_visit_module
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def patched_visit_functiondef(self, node):
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
            for arg in node.args.args:
                self._invoked_with_func_args.add(arg.name)

        ORIGINAL['visit_functiondef'](self, node)
    ORIGINAL['visit_functiondef'] = VariablesChecker.visit_functiondef
    VariablesChecker.visit_functiondef = patched_visit_functiondef
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def patched_add_message(self, msgid, line=None, node=None, args=None,
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
            elif fixture_name in self._invoked_with_func_args \
                    and fixture_name in self._pytest_fixtures:
                if _is_same_module(fixtures=self._pytest_fixtures,
                                   import_node=node,
                                   fixture_name=fixture_name):
                    return

            # fixture is referenced in @pytest.mark.usefixtures
            elif fixture_name in self._invoked_with_usefixtures \
                    and fixture_name in self._pytest_fixtures:
                if _is_same_module(fixtures=self._pytest_fixtures,
                                   import_node=node,
                                   fixture_name=fixture_name):
                    return

        # check W0613 unused-argument
        if msgid == 'unused-argument' and \
                _can_use_fixture(node.parent.parent) and \
                isinstance(node.parent, astroid.Arguments) and \
                node.name in self._pytest_fixtures:
            return

        # check W0621 redefined-outer-name
        if msgid == 'redefined-outer-name' and \
                _can_use_fixture(node.parent.parent) and \
                isinstance(node.parent, astroid.Arguments) and \
                node.name in self._pytest_fixtures:
            return

        if int(pylint.__version__.split('.')[0]) >= 2:
            ORIGINAL['add_message'](
                self, msgid, line, node, args, confidence, col_offset)
        else:
            # python2 + pylint1.9 backward compatibility
            ORIGINAL['add_message'](
                self, msgid, line, node, args, confidence)
    ORIGINAL['add_message'] = VariablesChecker.add_message
    VariablesChecker.add_message = patched_add_message
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
