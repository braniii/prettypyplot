# -*- coding: utf-8 -*-
"""Tests for the color module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import numpy as np
import pytest
from matplotlib import colors as clr

import prettypyplot


@pytest.mark.parametrize('num, kwargs, error', [
    (1, {}, None),
    (2, {'high': 2}, None),
    (2, {}, ValueError),
    ('a', {}, TypeError),
    ((1, 2), {}, TypeError),
])
def test__is_number_in_range(num, kwargs, error):
    """Test if number is in range."""
    if error is None:
        prettypyplot.colors._is_number_in_range(num, **kwargs)
    else:
        with pytest.raises(error):
            prettypyplot.colors._is_number_in_range(num, **kwargs)


@pytest.mark.parametrize('L1, L2, refcontrast', [
    (1, 0, 21), (0.5, 0.5, 1),
])
def test__contrast(L1, L2, refcontrast):
    """Test contrast."""
    for l1, l2 in ((L1, L2), (L2, L1)):
        contrast = prettypyplot.colors._contrast(l1, l2)
        assert contrast == refcontrast


@pytest.mark.parametrize('rgb, refluminace', [
    ((1, 1, 1), 1),
    ((1, 0, 0), 0.2126),
    ((0, 1, 0), 0.7152),
    ((0, 0, 0), 0),
])
def test__relative_luminance(rgb, refluminace):
    """Test luminance."""
    luminance = prettypyplot.colors._relative_luminance(rgb)
    assert luminance == refluminace


@pytest.mark.parametrize('bgcolor, kwargs, refcolor, error', [
    ('w', {}, '#000000', None),
    ('b', {}, '#ffffff', None),
    ('w', {'colors': ('r', 'w', 'k')}, clr.to_rgb('k'), None),
    ('w', {'colors': ('r', 'w')}, clr.to_rgb('r'), None),
    ('#505050', {}, '#ffffff', None),
    ('#a0a0a0', {}, '#000000', None),
    ('notAColorCode', {}, None, ValueError),
    ('w', {'colors': ('notAColorCode')}, None, ValueError),
])
def test_text_color(bgcolor, kwargs, refcolor, error):
    """Test estimate text color."""
    if error is None:
        color = prettypyplot.colors.text_color(bgcolor, **kwargs)
        assert clr.to_rgb(color) == clr.to_rgb(refcolor)
    else:
        with pytest.raises(error):
            prettypyplot.colors.text_color(bgcolor, **kwargs)


@pytest.mark.parametrize('color, refbool, error', [
    ('k', True, None),
    ('w', True, None),
    ('r', False, None),
    ('#212121', True, None),
    ('#212122', False, None),
    ('NoColorCode', None, ValueError),
])
def test_is_grayshade(color, refbool, error):
    """Test if color is gray shade."""
    if error is None:
        assert refbool == prettypyplot.colors.is_greyshade(color)
    else:
        with pytest.raises(error):
            prettypyplot.colors.is_greyshade(color)


@pytest.mark.parametrize('nsc, color, kwargs, refcolors, error', [
    (2, 'k', {}, [[0, 0, 0], [0.75, 0.75, 0.75]], None),
    (2, 'k', {'return_hex': False}, ['#000000', '#bfbfbf'], None),
    (2, 'k', {'return_hex': True}, ['#000000', '#bfbfbf'], None),
    (3, 'r', {}, ['#ff0000', '#ff6060', '#ffbfbf'], None),
    (3, 'NoColorCoder', {}, None, ValueError),
    (1.2, 'k', {}, None, TypeError),
    ('s', 'k', {}, None, TypeError),
    (0, 'k', {}, None, ValueError),
    (-5, 'k', {}, None, ValueError),
])
def test_categorical_color(nsc, color, kwargs, refcolors, error):
    """Test categorical color."""
    if error is None:
        colors = prettypyplot.colors.categorical_color(nsc, color, **kwargs)
        # convert colors to hex
        if 'return_hex' not in kwargs or not kwargs['return_hex']:
            colors = [clr.to_hex(c) for c in colors]
        assert all(
            c == clr.to_hex(rc) for c, rc in zip(colors, refcolors)
        )
    else:
        with pytest.raises(error):
            prettypyplot.colors.categorical_color(nsc, color, **kwargs)


@pytest.mark.parametrize('nc, nsc, kwargs, ref, error', [
    (
        2,
        2,
        {'cmap': 'tab10'},
        [
            [0.12, 0.47, 0.71],
            [0.75, 0.9, 1.0],
            [1.0, 0.5, 0.06],
            [1.0, 0.87, 0.75],
        ],
        None,
    ),
    (
        2,
        2,
        {},
        [
            [0.12, 0.47, 0.71],
            [0.75, 0.9, 1.0],
            [1.0, 0.5, 0.06],
            [1.0, 0.87, 0.75],
        ],
        None,
    ),
    (
        2,
        2,
        {'return_colors': True},
        [
            [0.12, 0.47, 0.71],
            [0.75, 0.9, 1.0],
            [1.0, 0.5, 0.06],
            [1.0, 0.87, 0.75],
        ],
        None,
    ),
    (
        1,
        2,
        {'cmap': 'jet'},
        [[0.0, 0.0, 0.5], [0.75, 0.75, 1.0]],
        None,
    ),
    (2, 2, {'cmap': 'NoColorMap'}, None, ValueError),
    (20, 2, {'cmap': 'tab10'}, None, ValueError),
    (-2, 2, {}, None, ValueError),
    (2, -2, {}, None, ValueError),
    (2, -2, {}, None, ValueError),
])
def test_categorical_cmap(nc, nsc, kwargs, ref, error):
    """Test categorical cmap."""
    if error is None:
        colors = prettypyplot.colors.categorical_cmap(nc, nsc, **kwargs)
        # convert colors to hex
        if 'return_colors' in kwargs and kwargs['return_colors']:
            colors = colors.reshape(-1, 3)
        else:
            colors = colors.colors
        np.testing.assert_array_almost_equal(colors, ref, decimal=2)
    else:
        with pytest.raises(error):
            prettypyplot.colors.categorical_cmap(nc, nsc, **kwargs)


# dummy coverage tests
def test_load_colors():
    """Check that no error get raised."""
    prettypyplot.colors.load_colors()


def test_load_cmaps():
    """Check that no error get raised."""
    prettypyplot.colors.load_cmaps()
