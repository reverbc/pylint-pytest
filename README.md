# pylint-pytest

[![PyPI version fury.io](https://badge.fury.io/py/pylint-pytest.svg)](https://pypi.python.org/pypi/pylint-pytest/)
[![Travis CI](https://travis-ci.org/reverbc/pylint-pytest.svg?branch=master)](https://travis-ci.org/reverbc/pylint-pytest)

A Pylint plugin to suppress pytest-related false positives.

## Installation

Requirements:

- `pylint`
- `pytest>=4.6`

To install:

```bash
$ pip install pylint-pytest
```

## Usage

Enable via command line option `--load-plugins`

```bash
$ pylint --load-plugins pylint_pytest <path_to_your_sources>
```

Or in `pylintrc`:

```ini
[MASTER]
load-plugins=pylint_pytest
```

## Suppressed Pylint Warnings

### `unused-argument`

FP when a fixture is used in an applicable function but not referenced in the function body, e.g.

```python
def test_something(conftest_fixture):  # <- Unused argument 'conftest_fixture'
    assert True
```

### `unused-import`

FP when an imported fixture is used in an applicable function, e.g.

```python
from fixture_collections import imported_fixture  # <- Unused imported_fixture imported from fixture_collections

def test_something(imported_fixture):
    ...
```

### `redefined-outer-name`

FP when an imported/declared fixture is used in an applicable function, e.g.

```python
from fixture_collections import imported_fixture

def test_something(imported_fixture):  # <- Redefining name 'imported_fixture' from outer scope (line 1)
    ...
```

## Changelog

See [CHANGELOG](CHANGELOG.md).

## License

`pylint-pytest` is available under [MIT license](LICENSE).
