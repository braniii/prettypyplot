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
