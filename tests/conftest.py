# -*- coding: utf-8 -*-
"""Shared fixtures of the test suite.

BSD 3-Clause License
Copyright (c) 2026, Daniel Nagel
All rights reserved.

"""

import shutil

import pytest

from prettypyplot import style


@pytest.fixture(autouse=True)
def _image_tests_without_latex(request, monkeypatch):
    """Render image comparison tests without LaTeX.

    `use_style` activates LaTeX only if a `latex` executable is found, so the
    images would depend on the machine running the tests.

    """
    if request.node.get_closest_marker('mpl_image_compare') is None:
        return

    shutil_which = shutil.which

    def which(cmd, *args, **kwargs):
        if cmd == 'latex':
            return None
        return shutil_which(cmd, *args, **kwargs)

    monkeypatch.setattr(style.shutil, 'which', which)
