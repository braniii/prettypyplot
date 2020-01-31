"""
Set-up matplotlib environment.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.colors as clr
import matplotlib.pyplot as plt
import numpy as np

# import colormaps
from .cmaps._bownair import __bownair
from .cmaps._discrete import (
    __cbf4,
    __cbf5,
    __cbf8,
    __pastel5,
    __pastel6,
    __ufcd,
)
from .cmaps._macaw import __macaw
from .cmaps._turbo import __turbo


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_cmaps():
    """
    Load and include custom colormaps to matplotlib.

    Add sequential colormaps 'pastel5', 'pastel6', 'cbf4', 'cbf5', 'cbf8',
    and 'ufcd' as an corporate design. Except of 'ufcd' all palettes should be
    'color-blind-friendly'.

    Add continuous colormaps macaw, Turbo. The Copyright of
    those are given on top of the data.

    .. see:: `prettypyplot.cmaps`

    """
    # register own continuous and discrete cmaps
    for colormap in [__pastel5(), __pastel6(), __cbf4(), __cbf5(), __cbf8(),
                     __ufcd(), __turbo(), __macaw(), __bownair()]:
        # add cmap
        if colormap.name not in plt.cm.cmap_d:
            plt.register_cmap(cmap=colormap)
        # add reversed cmap
        if colormap.reversed().name not in plt.cm.cmap_d:
            plt.register_cmap(cmap=colormap.reversed())


def categorical_cmap(nc,
                     nsc,
                     cmap=None,
                     return_colors=False):
    """
    Generate categorical colors of given cmap.

    Exract from a predefined colormap colors and generate for each the desired
    number of shades.

    Parameters
    ----------
    nc : int
        Number of colors

    nsc : int
        Number of shades per colors

    cmap : mpl colormap, optional
        Matplotlib colormap to take colors from. The default is the active
        color cycle.

    return_colors : bool, optional
        Return an array of rgb colors. Each color together with its shades are
        in an own row.

    Returns
    -------
    scolors : mpl colormap
        Return discrete colormap. If return_colors, a 2d representation will
        be returned instead.

    """
    # check correct data type
    if int(nc) != nc or int(nsc) != nsc:
        raise TypeError('nc and nsc need to be an integer.')
    nc, nsc = int(nc), int(nsc)

    # get cmap
    if cmap is not None:
        cmap = plt.get_cmap(cmap)
    else:
        cmap = clr.ListedColormap(plt.rcParams['axes.prop_cycle']
                                  .by_key()['color'])
    if nc > cmap.N:
        raise ValueError('Too many categories for colormap.')

    # extract colors from cmap
    if type(cmap) == clr.LinearSegmentedColormap:
        colors = cmap(np.linspace(0, 1, nc))
    elif type(cmap) == clr.ListedColormap:
        colors = cmap(np.arange(nc, dtype=int))

    # get shades of colors
    scolors = np.empty((nc, nsc, 3))
    for i, c in enumerate(colors):
        scolors[i] = categorical_color(nsc, c)

    # return colors
    if return_colors:
        return scolors
    else:
        return clr.ListedColormap(np.concatenate(scolors))


def categorical_color(nsc, color, return_hex=False):
    """
    Generate categorical shades of given colors.

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
    if not clr.is_color_like(color):
        raise TypeError('{c} can not be interpreted as color.'.format(c=color))
    if int(nsc) != nsc:
        raise TypeError('nsc need to be an integer.')
    nsc = int(nsc)

    # genrate shades of colors
    color_hsv = clr.rgb_to_hsv(clr.to_rgb(color))
    colors_hsv = np.tile(color_hsv, nsc).reshape(nsc, 3)
    colors_hsv[:, 1] = np.linspace(color_hsv[1], 0.25, nsc)
    colors_hsv[:, 2] = np.linspace(color_hsv[2], 1, nsc)
    colors_rgb = clr.hsv_to_rgb(colors_hsv)

    if return_hex:
        return [clr.to_hex(c) for c in colors_rgb]
    else:
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
    def channel_transf(channel):
        """Transform channel for luminance calculation."""
        if channel < 0.03928:
            return channel / 12.92
        else:
            return ((channel + 0.055) / 1.055)**2.4

    def relative_luminance(color):
        """Calculate luminance from rgb color, each channel [0, 1]."""
        r, g, b = [channel_transf(c) for c in color]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def contrast(L1, L2):
        """L1 and L2 should be luminances [0, 1]."""
        if L1 < L2:
            L1, L2 = L2, L1
        return (L1 + 0.05) / (L2 + 0.05)

    # check input by casting to matplotlib colors
    bgcolor = clr.to_rgb(bgcolor)
    colors_rgb = [clr.to_rgb(c) for c in colors]

    # calculate the (luminances)
    bgL = relative_luminance(bgcolor)
    Ls = [relative_luminance(c) for c in colors_rgb]

    # calculate contrast between bgcolor and all colors
    C = [contrast(bgL, L) for L in Ls]

    # return color corresponding to greatest contrast
    idx = C.index(max(C))
    return colors[idx]


# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# gray tones
black_grays = {'dark': '#000000', 'light': '#dddfe5'}
default_grays = {'dark': '#4d4f53', 'light': '#dddfe5'}
