# Changelog

## [Unreleased]
### Fixed
- Fix fixtures defined with `@pytest.yield_fixture` decorator still showing FP

## [0.1.1] - 2020-05-19
### Fixed
- Fix crashes when `*args` or `**kwargs` is used in FuncDef

## [0.1] - 2020-05-18
### Added
- Suppressing FP `unused-import` with tests
- Suppressing FP `unused-argument` with tests
- Suppressing FP `redefined-outer-scope` with tests
- Add CI/CD configuration with Travis CI
