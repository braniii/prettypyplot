# -*- coding: utf-8 -*-
"""Tests for the command line interface.

BSD 3-Clause License
Copyright (c) 2026, Daniel Nagel
All rights reserved.

"""

import re
import subprocess
import sys

import pytest
from click.testing import CliRunner

import prettypyplot
from prettypyplot.__main__ import main


def _api(*names):
    """Invoke `prettypyplot api` with the given names."""
    return CliRunner().invoke(main, ['api', *names])


def _functions(output):
    """Return names of all functions in a reference."""
    return re.findall(r'^### `pplt\.(\w+)`$', output, re.MULTILINE)


def test_api_complete():
    """Without names, all public functions and the colormaps are printed."""
    result = _api()
    assert result.exit_code == 0
    assert prettypyplot.__version__ in result.output
    assert sorted(_functions(result.output)) == sorted(prettypyplot.__all__)
    assert '| `macaw` | continuous | - |' in result.output
    # mkdocs cross references are converted to plain text
    assert '][' not in result.output


@pytest.mark.parametrize(
    'names',
    (['legend'], ['colorbar', 'legend'], ['legend', 'legend']),
)
def test_api_functions(names):
    """Only the given functions are printed, each once."""
    result = _api(*names)
    assert result.exit_code == 0
    assert _functions(result.output) == list(dict.fromkeys(names))
    assert 'Registered colormaps' not in result.output


def test_api_colormaps():
    """The name colormaps prints only the table of colormaps."""
    result = _api('colormaps')
    assert result.exit_code == 0
    assert '## Registered colormaps' in result.output
    assert not _functions(result.output)


def test_api_unknown_name():
    """Unknown names are rejected with the available ones."""
    result = _api('legend', 'not_a_function')
    assert result.exit_code != 0
    assert 'not_a_function' in result.output
    assert 'colormaps' in result.output


def test_api_signature_and_docstring():
    """Long signatures are wrapped and docstrings are dedented."""
    output = _api('use_style').output
    assert 'pplt.use_style(\n    interactive: bool | None = None,\n' in output
    # parameters copied by decorit.copy_doc_params, before Python 3.13 the
    # runtime docstring mixes indentation levels
    assert '\nParameters\n----------\ninteractive : bool, optional\n' in output


def test_api_links():
    """Relative links of the docs point to the online documentation."""
    output = _api('legend').output
    assert '(https://braniii.github.io/prettypyplot/gallery/legend)' in output


def test_module_entry_point():
    """The interface runs with `python -m prettypyplot`."""
    result = subprocess.run(
        [sys.executable, '-m', 'prettypyplot', 'api', 'legend'],
        capture_output=True,
        text=True,
        check=True,
    )
    assert _functions(result.stdout) == ['legend']
