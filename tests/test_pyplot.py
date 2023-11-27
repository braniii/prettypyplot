# -*- coding: utf-8 -*-
"""Tests for the plot module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import matplotlib as mpl
import numpy as np
import pytest
from matplotlib import pyplot as plt

import prettypyplot

@pytest.mark.parametrize('data, ticks', (
    (np.arange(10), None),
    (np.arange(10), np.arange(10)),
    (np.arange(10), np.arange(2)),
))
def test__reduce_ticks(data, ticks):
    # check that the number of ticks is not reduced when setting the ticks
    # explicitly
    fig, ax = plt.subplots()
    ax.plot(data)

    if ticks is not None:
        ax.set_xticks(ticks)

    nticks = len(ax.get_xticks())

    prettypyplot.pyplot._reduce_ticks(fig)

    if ticks is None:
        assert nticks >= len(ax.get_xticks())
    else:
        assert nticks == len(ax.get_xticks())


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize('data, style, kwargs', (
    (np.arange(25).reshape(-1, 5), 'default', {}),
    (np.arange(25).reshape(-1, 5), 'default', {'zorder': 0}),
    (np.arange(25).reshape(-1, 5), 'minimal', {}),
    (np.arange(25).reshape(-1, 5), 'minimal', {'zorder': 0}),
))
def test_imshow(data, style, kwargs):
    """Test imshow."""
    prettypyplot.use_style(style=style)

    fig, ax = plt.subplots()
    # activate grid to see influence of zorder
    ax.grid(True)

    im = prettypyplot.imshow(data, **kwargs)
    assert isinstance(im, mpl.image.AxesImage)

    # allow plotting grid behind image
    ax.set_axisbelow(True)

    return fig


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize('data, style, args, kwargs', (
    ((np.arange(25), np.sin(np.arange(25))), 'default', (), {}),
    ((np.arange(25), np.cos(np.arange(25))), 'default', ('bo', ), {}),
    ((np.arange(25), np.sin(np.arange(25))), 'minimal', (), {}),
    ((np.arange(25), np.cos(np.arange(25))), 'minimal', ('bo', ), {}),
))
def test_plot(data, style, args, kwargs):
    """Test imshow."""
    prettypyplot.use_style(style=style)

    fig, ax = plt.subplots()

    _ = prettypyplot.plot(*data, *args, **kwargs)

    return fig


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize('data, style, args, ylog', (
    ((np.arange(25), np.arange(25)), 'default', (True, ), False),
    ((np.arange(25), np.arange(25)), 'default', (), False),
    ((np.arange(25), np.arange(25)), 'default', (False, ), False),
    ((np.arange(25), 2 + np.arange(25)**2), 'default', (True, ), True),
    ((np.arange(25), np.arange(25)), 'minimal', (True, ), False),
    ((np.arange(25), np.arange(25)), 'minimal', (False, ), False),
    ((np.arange(25), np.arange(25)), 'minimal', (), False),
    ((np.arange(25), 2 + np.arange(25)**2), 'minimal', (True, ), True),
))
def test_grid(data, style, args, ylog):
    """Test grid."""
    prettypyplot.use_style(style=style)

    fig, ax = plt.subplots()

    _ = prettypyplot.plot(*data)
    _ = prettypyplot.grid(*args)

    if ylog:
        ax.set_yscale('log')

    return fig
