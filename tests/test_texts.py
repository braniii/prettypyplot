# -*- coding: utf-8 -*-
"""Tests for the text module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import pytest
from matplotlib import pyplot as plt

import prettypyplot


def txt_object():
    """Define txt object."""
    return plt.text(0, 0, 'text')


@pytest.mark.parametrize('contour, refcontour, error', [
    (True, {'contourwidth', 'contourcolor'}, None),
    (False, None, None),
    (5, None, TypeError),
    ('as', None, TypeError),
    ((5, 7), {'contourwidth': 5, 'contourcolor': 7}, ValueError),
    ((5, 'k'), {'contourwidth': 5, 'contourcolor': 'k'}, None),
    ((1.2, 2.4), {'contourwidth': 1.2, 'contourcolor': 2.4}, ValueError),
    ((1.2, 'w'), {'contourwidth': 1.2, 'contourcolor': 'w'}, None),
])
def test__parse_contour(contour, refcontour, error):
    """Test parsing figratio."""
    if error is None:
        kwargs = prettypyplot.texts._parse_contour(contour)
        if isinstance(refcontour, set):
            assert refcontour == set(kwargs.keys())
        else:
            assert refcontour == kwargs
    else:
        with pytest.raises(error):
            prettypyplot.texts._parse_contour(contour)


@pytest.mark.parametrize('txt, contourwidth, kwargs, error', [
    (txt_object(), 'a', {'contourcolor': 'b'}, TypeError),
    (txt_object(), 1, {'contourcolor': 'b'}, None),
    (txt_object(), 1, {'contourcolor': 'noColorCode'}, TypeError),
    ('a', 1, {}, TypeError),
])
def test_add_contour(txt, contourwidth, kwargs, error):
    """Test adding contour."""
    if error is None:
        prettypyplot.texts.add_contour(txt, contourwidth, **kwargs)
        assert txt.get_path_effects()
    else:
        with pytest.raises(error):
            prettypyplot.texts.add_contour(txt, contourwidth, **kwargs)


@pytest.mark.parametrize('contour', [
    True, False, (5, 'r'), (1.2, 'y'),
])
def test_figtext(contour):
    """Test figtext."""
    txt = prettypyplot.texts.figtext(0, 1, 'text', contour=contour)
    assert bool(txt.get_path_effects()) == bool(contour)


@pytest.mark.parametrize('contour', [
    True, False, (5, 'r'), (1.2, 'y'),
])
def test_text(contour):
    """Test figtext."""
    txt = prettypyplot.texts.text(0, 1, 'text', contour=contour)
    assert bool(txt.get_path_effects()) == bool(contour)
