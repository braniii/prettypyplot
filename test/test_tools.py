# -*- coding: utf-8 -*-
"""Tests for the tools module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import matplotlib as mpl
import numpy as np
import pytest
from matplotlib import pyplot as plt

import prettypyplot


@pytest.mark.parametrize('figratio, refratio, error', [
    ('sqrt(2)', 1.4142135623730951, None),
    (2, 2, None),
    (2.0, 2, None),
    ('golden', 1.618033988749895, None),
    ('error', None, ValueError),
])
def test_parse_figratio(figratio, refratio, error):
    """Test parsing figratio."""
    if error is None:
        figratio = prettypyplot.tools.parse_figratio(figratio)
        np.testing.assert_almost_equal(figratio, refratio)
    else:
        with pytest.raises(error):
            prettypyplot.tools.parse_figratio(figratio)


@pytest.mark.parametrize('figsize, figratio, refsize, error', [
    ((1, 2), None, (1, 2), None),
    ([1, 2], None, (1, 2), None),
    (np.array([1, 2]), None, (1, 2), None),
    (1, 0.5, (1, 2), None),
    ((1, ), 0.5, (1, 2), None),
    ([1, ], 0.5, (1, 2), None),
    ((1, 2, 3), None, None, ValueError),
    ('a', None, None, ValueError),
    (('a', 2), None, None, ValueError),
])
def test_parse_figsize(figsize, figratio, refsize, error):
    """Test parsing figsize."""
    if error is None:
        figsize = prettypyplot.tools.parse_figsize(figsize, figratio)
        np.testing.assert_array_almost_equal(figsize, refsize)
    else:
        with pytest.raises(error):
            prettypyplot.tools.parse_figsize(figsize, figratio)


@pytest.mark.parametrize('number, kwargs, is_number', [
    (1, {}, True),
    (1.5, {}, True),
    (1.5, {'dtype': int}, False),
    (1.5, {'dtype': np.int32}, False),
    (True, {}, True),
    (False, {}, True),
    ('a', {}, False),
    ((1, 2), {}, False),
])
def test_is_number(number, kwargs, is_number):
    """Test is_number."""
    assert is_number == prettypyplot.tools.is_number(number, **kwargs)


@pytest.mark.parametrize('number, refnumber, error', [
    (1, -1, None),
    (-1, 1, None),
    ('-1', '1', None),
    ('5%', '-5%', None),
    ((1, 2), None, ValueError),
])
def test_invert_sign(number, refnumber, error):
    """Test inverting sign."""
    if error is None:
        assert refnumber == prettypyplot.tools.invert_sign(number)
    else:
        with pytest.raises(error):
            prettypyplot.tools.invert_sign(number)


def test_parse_axes():
    """Ensure, that gca returns always an axes instance."""
    fig, ax = plt.subplots()

    # parse correct ax in ax
    argsref = (1, 'a', np.arange(2))
    argsax = prettypyplot.tools.parse_axes(*argsref, ax=ax)
    assert all(
        isinstance(ref, type(parse))
        for ref, parse in zip(argsref, argsax[0])
    )
    assert ax is argsax[1]

    # multiple axes
    with pytest.raises(ValueError):
        prettypyplot.tools.parse_axes(ax, ax=ax)
    with pytest.raises(ValueError):
        prettypyplot.tools.parse_axes(1, ax, ax=ax)
    with pytest.raises(ValueError):
        prettypyplot.tools.parse_axes(ax, ax, 1, ax=None)

    argsax = prettypyplot.tools.parse_axes(ax, ax=None)
    assert ax is argsax[1]

    argsax = prettypyplot.tools.parse_axes(ax=ax)
    assert ax is argsax[1]


def test_gca():
    """Ensure, that gca returns always an axes instance."""
    fig, ax = plt.subplots()
    assert isinstance(prettypyplot.tools.gca(None), mpl.axes.Axes)
    assert isinstance(prettypyplot.tools.gca(plt.gca()), mpl.axes.Axes)


def test_get_axes():
    """Ensure, that get_axes returns always an axes instance."""
    fig, axs = plt.subplots()
    assert all(
        isinstance(ax, mpl.axes.Axes)
        for ax in prettypyplot.tools.get_axes(axs)
    )
    assert all(
        isinstance(ax, mpl.axes.Axes)
        for ax in prettypyplot.tools.get_axes(None)
    )
    with pytest.raises(TypeError):
        prettypyplot.tools.get_axes(fig)
