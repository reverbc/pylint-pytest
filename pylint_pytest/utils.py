import inspect
import re
import astroid
import pytest
import sys


PYTEST_LT_7_0 = getattr(pytest, 'version_tuple', (0, 0)) < (7, 0)


try:
    import pytest_describe
    PYTEST_DESCRIBE = True
except ImportError:
    PYTEST_DESCRIBE = False
    describe_prefixes_option = ()


if PYTEST_DESCRIBE:
    describe_prefix = "describe"
    try:
        import _pytest.config.findpaths
        config = _pytest.config.findpaths.determine_setup([], sys.argv[1:])
        if config:
            if PYTEST_LT_7_0:
                describe_prefix = config[2].config.sections.get('tool:pytest', {}).get('describe_prefixes', describe_prefix)
            else:
                describe_prefix = config[2].get('describe_prefixes', describe_prefix)
    finally:
        describe_prefixes_option = tuple(describe_prefix.split(' '))


describe_prefix_matcher = re.compile(fr'^{"|".join(describe_prefixes_option)}_.+$')


def _is_in_describe_section_when_enabled(node):
    import _pytest.config.findpaths
    describe_prefix = "describe"
    config = _pytest.config.findpaths.determine_setup([], sys.argv[1:])
    if config:
        if PYTEST_LT_7_0:
            describe_prefix = config[2].config.sections.get('tool:pytest', {}).get('describe_prefixes', describe_prefix)
        else:
            describe_prefix = config[2].get('describe_prefixes', describe_prefix)
    return (PYTEST_DESCRIBE and
        (node.parent is not None and isinstance(node.parent, astroid.FunctionDef) and re.match(describe_prefix_matcher, node.parent.name)))


def _is_pytest_mark_usefixtures(decorator):
    # expecting @pytest.mark.usefixture(...)
    try:
        if isinstance(decorator, astroid.Call) and \
                decorator.func.attrname == 'usefixtures' and \
                decorator.func.expr.attrname == 'mark' and \
                decorator.func.expr.expr.name == 'pytest':
            return True
    except AttributeError:
        pass
    return False


def _is_pytest_mark(decorator):
    try:
        deco = decorator  # as attribute `@pytest.mark.trylast`
        if isinstance(decorator, astroid.Call):
            deco = decorator.func  # as function `@pytest.mark.skipif(...)`
        if deco.expr.attrname == 'mark' and deco.expr.expr.name == 'pytest':
            return True
    except AttributeError:
        pass
    return False


def _is_pytest_fixture(decorator, fixture=True, yield_fixture=True):
    attr = None
    to_check = set()

    if fixture:
        to_check.add('fixture')

    if yield_fixture:
        to_check.add('yield_fixture')

    try:
        if isinstance(decorator, astroid.Attribute):
            # expecting @pytest.fixture
            attr = decorator

        if isinstance(decorator, astroid.Call):
            # expecting @pytest.fixture(scope=...)
            attr = decorator.func

        if attr and attr.attrname in to_check \
                and attr.expr.name == 'pytest':
            return True
    except AttributeError:
        pass

    return False


def _is_class_autouse_fixture(function):
    try:
        for decorator in function.decorators.nodes:
            if isinstance(decorator, astroid.Call):
                func = decorator.func

                if func and func.attrname in ('fixture', 'yield_fixture') \
                        and func.expr.name == 'pytest':

                    is_class = is_autouse = False

                    for kwarg in decorator.keywords or []:
                        if kwarg.arg == 'scope' and kwarg.value.value == 'class':
                            is_class = True
                        if kwarg.arg == 'autouse' and kwarg.value.value is True:
                            is_autouse = True

                    if is_class and is_autouse:
                        return True
    except AttributeError:
        pass

    return False


def _can_use_fixture(function):
    if isinstance(function, astroid.FunctionDef):

        # test_*, *_test
        if function.name.startswith('test_') or function.name.endswith('_test') or _is_in_describe_section_when_enabled(function):
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
