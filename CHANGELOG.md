# Changelog

## [Unreleased]
### Fixed
- Fix pytest **Module already imported so cannot be rewritten** warning when the package being linted was used by pytest/conftest already (#10)
- Fix missing Python version constraint (#11)

## [1.0.1] - 2021-03-03
### Added
- Suppressing FP `unused-import` when fixtures defined elsewhere are imported into `conftest.py` but not directly used (#2)

## [1.0.0] - 2021-03-02
### Added
- Python 3.9 support

### Removed
- Python 2.7 & 3.5 support

### Fixed
- Fix not able to work with `pytest-xdist` plugin when `--dist loadfile` is set in configuration file (#5)

## [0.3.0] - 2020-08-10
### Added
- W6401 `deprecated-pytest-yield-fixture`: add warning for [yield_fixture functions](https://docs.pytest.org/en/latest/yieldfixture.html)

### Fixed
- Fix incorrect path separator for Windows (#1)

## [0.2.0] - 2020-05-25
### Added
- Suppressing FP `no-member` from [using workaround of accessing cls in setup fixture](https://github.com/pytest-dev/pytest/issues/3778#issuecomment-411899446)

### Changed
- Refactor plugin to group patches and augmentations

## [0.1.2] - 2020-05-22
### Fixed
- Fix fixtures defined with `@pytest.yield_fixture` decorator still showing FP
- Fix crashes when using fixture + if + inline import
- Fix crashes when relatively importing fixtures (`from ..conftest import fixture`)

## [0.1.1] - 2020-05-19
### Fixed
- Fix crashes when `*args` or `**kwargs` is used in FuncDef

## [0.1] - 2020-05-18
### Added
- Suppressing FP `unused-import` with tests
- Suppressing FP `unused-argument` with tests
- Suppressing FP `redefined-outer-scope` with tests
- Add CI/CD configuration with Travis CI
