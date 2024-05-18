# Changelog

All notable changes to this project will be documented in this file. The format is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and [Element](https://github.com/vector-im/element-android) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[//]: # (Available sections in changelog)
[//]: # (### API changes warning ⚠️:)
[//]: # (### Added Features and Improvements 🙌:)
[//]: # (### Bugfix 🐛:)
[//]: # (### Other changes:)

## [Unreleased]
### API changes warning ⚠️:
- The cmap `pastel_autunm` was renamed to `pastel_autumn`
- Use `latex` font only if available

### Added Features and Improvements 🙌:
- Added tox setup with pytests against mpl 3.2-3.8 and py 3.8-3.12

### Other changes:
- Move to new git repository: Welcome to Github🎉


## [0.10.1] - 2023-11-27
### Bugfix 🐛:
- Fixed bug when using `style='minimal'` that lead to altering custom ticks, see #1


## [0.10.0] - 2023-03-09
### API changes warning ⚠️:
- Renamed submodule `plot` to `pyplot` to avoid shadowing with function `pplt.plot`
- Method `pplt.activate_axis` needs to be called via `pplt.pyplot.activate_axis`

### Added Features and Improvements 🙌:
- Moved from pdoc to an all new `mkdocs` documentation 🎉

### Bugfix 🐛:
- Fixed bug with `label_outer` with mpl >= 3.7
- Fixed bug due deprecation in mpl>=3.6, where the kwarg `b` in `ax.grid` was renamed to `visibile`

### Other changes:
- Some submodules, used to add additional pages in pdoc, were removed
- Remove deprecated usage of `mpl.cm.get_cmaps` and `mpl.cm.register_cmap`


## [0.9.0] - 2022-04-28
### API changes warning ⚠️:
- define `pip install prettypyplot[testing/docs/all]` to bundle installation
- The methods `pplt.tools.parse_figsize` and `pplt.tools.parse_figaratio` are moved to `pplt.style._parse_figsize` and `pplt.style._parse_figratio`, respectively

### Added Features and Improvements 🙌:
- Store all variables of `pplt.use_style`. This enables calling `pplt.update_style` without repeating all arguments remaining the same.
- Moved from `flat` to recommended `src` layout and moved tests from `test` to `tests`

### Bugfix 🐛:
- Fix coverage CI
- Fix identifying continuos cmaps in `pplt.use_style(colors=...)`, e.g., `turbo`, `viridis`.
- Fix calling `pplt.update_style` without specifying `figratio` and/or `figsize`
- Fix including `LICENSE` file in pypi package and exclude tests, this allows publishing to conda-forge

### Other changes:
- Increase `decorit>=0.2.0` to remove annoying PEP warnings


## [0.8.0] - 2022-04-03
### API changes warning ⚠️:
- gray colors can not be accessed anymore via `default_grays['dark']` but instead via `default_grays.dark`

### Added Features and Improvements 🙌:
- Added cmap `summertimes`
- Scales markers and boxplots according to mode
- Added testing of plotting functionality pytest-mpl
- `MODE` and `STYLE` are now of `Enum` class
- Major code improvements, see commits

### Bugfix 🐛:
- Fix treating images (`imshow`) as none empty images
- Fix handling non subplot axes correctly by `pplt.hide_empty_axes`
- Fix to activate minor and major grid for `mpl >= 3.3` by calling `pplt.grid()`
- Fix CI building docs
- Fix using wrong style/mode in `plot` submodule


## [0.7.1] - 2021-02-18
- Fix uploading wrong package to PyPi


## [0.7.0] - 2021-02-17
### Added Features and Improvements 🙌:
- Added tests for basic functions (no figure comparisons)
- Major code clean up and refactoring

### Bugfix 🐛:
- Fix restoring labels of outer axes when applying `pplt.hide_empty_axes`


## [0.6.0] - 2021-01-14
### Added Features and Improvements 🙌:
- Add `pplt.subplot_labels` for adding shared labels for grid subplots
- Add pplt colors `pplt:lightgray` and `pplt:gray`
- Added new gallery figure of subplots

## [0.5.0] - 2020-10-19
### Added Features and Improvements 🙌:
- new refreshing colormap `paula`
- Add `pplt.label_outer` which respects empty axes
- Add `pplt.hide_empty_axes` for hiding empty axes

### Bugfix 🐛:
- Make cmaps compatible with `maptlitlib 3.5+`

### Other changes:
- Enforce wemake-python-styleguide (WIP)
- Upgrade doc to `pdoc 0.9` and automatize it


## [0.4.2] - 2020-07-06
### Added Features and Improvements 🙌:
- Add option `sf` to activate sans-serif font with `pplt.use_style`
- simplify usage of contour option

### Other changes:
- some code clean up
- skipped version due to error


## [0.4.0] - 2020-04-21
### Added Features and Improvements 🙌:
- Added Decorators
- Added 3 new discrete color options `'pastel_rainbow'`, `'pastel_spring'`, `'pastel_autumn'`
- Refactor style settings. Added `pplt.update_style` and renamed `pplt.setup_pyplot` to `pplt.use_style`
- Add text module with `pplt.text`, `pplt.figtext` and `pplt.add_contour`. With centered text and contour parameter

### Bugfix 🐛:
- Minor bug fixes

### Other changes:
- Updated pydoc to 0.8.1
- Updated documentation and readme


## [0.3.0] - 2020-10-30
### Added Features and Improvements 🙌:
- Colors of `pastel5`, axes, grid and text are now accessible directly

### Bugfix 🐛:

### Other changes:
- Increase simplification threshold to reduce figure size
- Minor changes


## [0.2.3] - 2020-02-04
- Include mplstyle


## [0.2.2] - 2020-01-31
- Fix PyPi setup


## [0.2.1] - 2020-01-31
### Added Features and Improvements 🙌:
- added gallery
- added docs

### Bugfix 🐛:
- many small bugfixes

### Other changes:
- refactored all submodules


[Unreleased]: https://github.com/braniii/prettypyplot/compare/v0.10.1...master
[0.10.1]: https://gitlab.com/braniii/prettypyplot/compare/v0.10.0...v0.10.1
[0.10.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.9.0...v0.10.0
[0.9.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.8.0...v0.9.0
[0.8.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.7.1...v0.8.0
[0.7.1]: https://gitlab.com/braniii/prettypyplot/compare/v0.7.0...v0.7.1
[0.7.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.6.0...v0.7.0
[0.6.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.5.0...v0.6.0
[0.5.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.4.2...v0.5.0
[0.4.2]: https://gitlab.com/braniii/prettypyplot/compare/v0.4.0...v0.4.2
[0.4.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.3.0...v0.4.0
[0.3.0]: https://gitlab.com/braniii/prettypyplot/compare/v0.2.3...v0.3.0
[0.2.3]: https://gitlab.com/braniii/prettypyplot/compare/v0.2.2...v0.2.3
[0.2.2]: https://gitlab.com/braniii/prettypyplot/compare/v0.2.1...v0.2.2
[0.2.1]: https://gitlab.com/braniii/prettypyplot/tree/v0.2.1
