# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2020-2023, Daniel Nagel
# All rights reserved.
"""Set-up matplotlib environment."""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from collections import namedtuple

import matplotlib as mpl
import numpy as np
from matplotlib import colors as clr
from matplotlib import pyplot as plt

# importing colormaps
from prettypyplot._cmaps.bownair import _bownair
from prettypyplot._cmaps.discrete import (
    _argon,
    _cbf4,
    _cbf5,
    _cbf8,
    _pastel5,
    _pastel6,
    _pastel_autunm,
    _pastel_rainbow,
    _pastel_spring,
    _paula,
    _summertimes,
    _ufcd,
)
from prettypyplot._cmaps.macaw import _macaw
from prettypyplot._cmaps.tol_discrete import (
    _tol_bright,
    _tol_high_contrast,
    _tol_light,
    _tol_medium_contrast,
    _tol_muted,
    _tol_vibrant,
)
from prettypyplot._cmaps.turbo import _turbo
from prettypyplot.tools import is_number


# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class GrayTones(namedtuple('GrayTones', 'dark light')):
    """Class for holding light and dark gray tone."""


black_grays = GrayTones('#000000', '#dddfe5')
black_grays_darkmode = GrayTones('#ffffff', '#22201a')
default_grays = GrayTones('#4d4f53', '#dddfe5')
default_grays_darkmode = GrayTones('#b2b0ac', '#22201a')


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def _get_cmap(cmap):
    """Wrapper for get_cmap with mpl <=3.6 and >=3.7."""
    if hasattr(mpl, 'colormaps') and hasattr(mpl.colormaps, 'get_cmap'):
        mpl.colormaps.get_cmap(cmap)
    else:
        mpl.cm.get_cmap(cmap)


def _register_cmap(cmap):
    """Wrapper for register_cmap with mpl <=3.6 and >=3.7."""
    if hasattr(mpl, 'colormaps') and hasattr(mpl.colormaps, 'register'):
        mpl.colormaps.register(cmap)
    else:
        mpl.cm.register_cmap(cmap=cmap)


def load_cmaps():
    """Load and include custom colormaps to matplotlib.

    Add sequential colormaps `pastel5`, `pastel6`, `cbf4`, `cbf5`, `cbf8`,
    and `ufcd` as an corporate design. Except of `ufcd` all palettes should be
    'color-blind-friendly'.

    Add continuous colormaps macaw, Turbo. The Copyright of those are given on
    top of the data.

    !!! see
        Choosing an [cmaps](../../gallery/cmaps).

    """
    colormaps = (
        _argon(),
        _pastel5(),
        _pastel6(),
        _cbf4(),
        _cbf5(),
        _cbf8(),
        _pastel_autunm(),
        _pastel_rainbow(),
        _pastel_spring(),
        _paula(),
        _summertimes(),
        _tol_bright(),
        _tol_high_contrast(),
        _tol_light(),
        _tol_medium_contrast(),
        _tol_muted(),
        _tol_vibrant(),
        _ufcd(),
        _turbo(),
        _macaw(),
        _bownair(),
    )
    # register own continuous and discrete cmaps
    for colormap in colormaps:
        # add cmap and reverse cmap
        for cmap in (colormap, colormap.reversed()):
            try:
                _get_cmap(cmap.name)
            except ValueError:
                _register_cmap(cmap=cmap)


def load_colors():
    """Load and include custom colors to matplotlib.

    Add colors of `pastel5` which can be accessed via `pplt:blue`, `pplt:red`,
    `pplt:green`, `pplt:orange`, `pplt:lightblue`, `pplt:gray` and
    `pplt:lightgray`. Further, the current colors will be added `pplt:axes`,
    `pplt:text`, `pplt:grid`.

    !!! see
        Choosing an [cmaps](../../gallery/cmaps).

    """
    # register own colors
    pplt_colors = {
        'pplt:blue': _pastel5().colors[0],
        'pplt:red': _pastel5().colors[1],
        'pplt:green': _pastel5().colors[2],
        'pplt:orange': _pastel5().colors[3],
        'pplt:lightblue': _pastel5().colors[4],
        'pplt:gray': default_grays.dark,
        'pplt:grey': default_grays.dark,
        'pplt:lightgray': default_grays.light,
        'pplt:lightgrey': default_grays.light,
        'pplt:axes': plt.rcParams['axes.edgecolor'],
        'pplt:text': plt.rcParams['text.color'],
        'pplt:grid': plt.rcParams['grid.color'],
    }
    clr._colors_full_map.update(pplt_colors)  # noqa: WPS437


def categorical_cmap(nc, nsc, *, cmap=None, return_colors=False):
    """Generate categorical colors of given cmap.

    Exract from a predefined colormap colors and generate for each the desired
    number of shades.

    Parameters
    ----------
    nc : int
        Number of colors
    nsc : int
        Number of shades per colors
    cmap : `matplotlib.colors.Colormap` or str, optional
        Matplotlib colormap to take colors from. The default is the active
        color cycle.
    return_colors : bool, optional
        Return an array of rgb colors. Each color together with its shades are
        in an own row.

    Returns
    -------
    scolors : `matplotlib.colors.Colormap` or np.ndarray
        Return discrete colormap. If return_colors, a 2d representation will
        be returned instead.

    """
    # check correct data type
    _is_number_in_range(
        nc, name='nc', dtype=int, low=1, high=np.iinfo(int).max,
    )
    _is_number_in_range(
        nsc, name='nsc', dtype=int, low=1, high=np.iinfo(int).max,
    )
    nc, nsc = int(nc), int(nsc)

    # get cmap
    if cmap is not None:
        cmap = plt.get_cmap(cmap)
    else:
        cmap = clr.ListedColormap(
            plt.rcParams['axes.prop_cycle'].by_key()['color'],
        )
    if nc > cmap.N:
        raise ValueError('Too many categories for colormap.')

    # extract colors from cmap
    if isinstance(cmap, clr.LinearSegmentedColormap):
        colors = cmap(np.linspace(0, 1, nc))
    elif isinstance(cmap, clr.ListedColormap):
        colors = cmap(np.arange(nc, dtype=int))

    # get shades of colors
    scolors = np.empty((nc, nsc, 3))
    for idx, color in enumerate(colors):
        scolors[idx] = categorical_color(nsc, color)

    if return_colors:
        return scolors
    return clr.ListedColormap(np.concatenate(scolors))


def categorical_color(nsc, color, *, return_hex=False):
    """Generate categorical shades of given colors.

    Generate for each provided color the number of specified shades. The shaded
    colors are interpolated linearly in HSV colorspace. This function is based
    on following post: https://stackoverflow.com/a/47232942

    Parameters
    ----------
    nsc : int
        Number of shades per color.
    color : RGB color or matplotlib predefined color
        Color used for generating shades.
    return_hex : bool, optional
        Return colors in hex format instead of rgb.

    Returns
    -------
    colors_rgb : list of RGB colors
        A list containing shaded colors. Where the list is sorted from the
        original color at the beginning to the most shaded one at the end.
        The default color encoding is rgb and hex if specified.

    """
    # check correct data type
    color = clr.to_rgb(color)
    _is_number_in_range(
        nsc, name='nsc', dtype=int, low=1, high=np.iinfo(int).max,
    )
    nsc = int(nsc)

    # genrate shades of colors
    color_hsv = clr.rgb_to_hsv(color)
    colors_hsv = np.tile(color_hsv, nsc).reshape(nsc, 3)
    colors_hsv[:, 1] = np.linspace(color_hsv[1], 1 / 4, nsc)
    colors_hsv[:, 2] = np.linspace(color_hsv[2], 1, nsc)
    colors_rgb = clr.hsv_to_rgb(colors_hsv)

    # check if color is greyscale value, need to fix arbitrary hue value of 0
    if is_greyshade(color):
        colors_rgb[:, 0] = colors_rgb[:, 1]

    if return_hex:
        return [clr.to_hex(color) for color in colors_rgb]
    return colors_rgb


def text_color(bgcolor, colors=('#000000', '#ffffff')):
    """Select textcolor with maximal contrast on background.

    All parameters needs to be colors accepted by matplotlib, see
    [matplotlib.colors](https://matplotlib.org/api/colors_api.html).
    The formulas are taken from W3C [WCAG 2.1](https://www.w3.org/TR/WCAG21)
    (Web Content Accessibility Guidelines).

    Parameters
    ----------
    bgcolor : matplotlib color
        Background color to which the contrast is maximized.
    colors : list of matplotlib colors, optional
        Selection of textcolors to choose from.

    Returns
    -------
    color : matplotlib color
        Color of colors which has the highest contrast on the given bgcolor.

    """
    # check input by casting to matplotlib colors
    bgcolor = clr.to_rgb(bgcolor)
    colors_rgb = [clr.to_rgb(color) for color in colors]

    # calculate the (luminances)
    bgL = _relative_luminance(bgcolor)
    Ls = [_relative_luminance(color) for color in colors_rgb]

    # calculate contrast between bgcolor and all colors
    contrast = [_contrast(bgL, Luminance) for Luminance in Ls]

    # return color corresponding to greatest contrast
    idx = contrast.index(max(contrast))
    return colors[idx]


def _channel_transf(channel):
    """Transform channel for luminance calculation."""
    if channel < 0.03928:
        return channel / 12.92
    return ((channel + 0.055) / 1.055)**2.4


def _relative_luminance(color):
    """Calculate luminance from rgb color, each channel [0, 1]."""
    for rgbc in color:
        _is_number_in_range(rgbc, name='RGB channel')
    rgb = np.array([_channel_transf(channel) for channel in color])
    rgb_weights = np.array([0.2126, 0.7152, 0.0722])
    return np.sum(rgb_weights * rgb)


def _contrast(L1, L2):
    """L1 and L2 should be luminances [0, 1]."""
    for lum in (L1, L2):
        _is_number_in_range(lum, name='Luminace')
    L1, L2 = float(L1), float(L2)

    L_offset = 0.05
    if L1 < L2:
        L1, L2 = L2, L1
    return (L1 + L_offset) / (L2 + L_offset)


def _is_number_in_range(num, *, dtype=float, name='Variable', low=0, high=1):
    """Check if number is in range [low, high]."""
    if not is_number(num, dtype=dtype):
        raise TypeError(
            '{0} needs to be {1} but given '.format(name, dtype.__name__) +
            '{num}'.format(num=num),
        )
    num = dtype(num)
    if num < low or num > high:
        raise ValueError(
            '{name} needs to be within [{low}'.format(name=name, low=low) +
            ', {high}] but given {num}'.format(high=high, num=num),
        )


def is_greyshade(color):
    """Check if color is a greyscale value including bw."""
    # check if color is greyscale value, need to fix arbitrary hue value
    color = clr.to_rgb(color)
    if np.min(color) == np.max(color):
        return True
    return False
