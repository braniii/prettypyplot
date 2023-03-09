# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2020-2023, Daniel Nagel
# All rights reserved.
"""Helper functions for plotting text."""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as mpl
import matplotlib.colors as clr
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt

from prettypyplot import tools


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def text(x, y, s, *, contour=None, ax=None, **kwargs):
    """Generate text object at (x,y).

    Wrapper around pyplot.text. The default alignment is changed to centered.

    Parameters
    ----------
    x, y : scalars
        The position to place the text. By default, this is in data
        coordinates. The coordinate system can be changed using the
        *transform* parameter.
    s : str
        The text.
    contour : bool or tuple(scalar, color)
        Add a contour to the text. Either use a boolean for default values,
        or give a tuple with linewidth and linecolor.
    ax : matplotlib axes
        Matplotlib axes to plot in.
    kwargs
        Text properties of [matplotlib.pyplot.text][]

    """
    # parse axes
    ax = tools.gca(ax)

    # change default alignment
    if 'va' not in kwargs and 'verticalalignment' not in kwargs:
        kwargs['va'] = 'center'
    if 'ha' not in kwargs and 'horizontalalignment' not in kwargs:
        kwargs['ha'] = 'center'

    # plot text
    txt = ax.text(x=x, y=y, s=s, **kwargs)

    # generate contour
    if contour is not None:
        contour_kwargs = _parse_contour(contour)
        if contour_kwargs is not None:
            add_contour(txt, **contour_kwargs)

    return txt


def figtext(x, y, s, *, contour=None, **kwargs):
    """Generate text object at figure position (x,y).

    Wrapper around pyplot.figtext. The default alignment is changed to
    centered.

    Parameters
    ----------
    x, y : scalars
        The position to place the text. By default, this is in data
        coordinates. The coordinate system can be changed using the
        `transform` parameter.
    s : str
        The text.
    contour : bool or tuple(scalar, color)
        Add a contour to the text. Either use a boolean for default values,
        or give a tuple with linewidth and linecolor.
    ax : matplotlib axes
        Matplotlib axes to plot in.
    kwargs
        Text properties of [matplotlib.pyplot.figtext][]

    """
    # change default alignment
    if 'va' not in kwargs and 'verticalalignment' not in kwargs:
        kwargs['va'] = 'center'
    if 'ha' not in kwargs and 'horizontalalignment' not in kwargs:
        kwargs['ha'] = 'center'

    # plot text
    txt = plt.figtext(x=x, y=y, s=s, **kwargs)

    # generate contour
    if contour is not None:
        contour_kwargs = _parse_contour(contour)
        if contour_kwargs is not None:
            add_contour(txt, **contour_kwargs)

    return txt


def add_contour(txt, contourwidth, contourcolor='w'):
    r"""Draw contour around txt.

    Parameters
    ----------
    txt : mpl Text
        Instance of [matplotlib.text.Text][]. Can be obtained by, e.g.,
        `txt = plt.text()` or `txt = plt.figtext()`.
    contourwidth : scalar
        Width of contour.
    contourcolor : RGB color or matplotlib predefined color, optional
        Color of contour, default is white.

    """
    # check if is text object
    if not isinstance(txt, mpl.text.Text):
        raise TypeError(
            'txt needs to be "matplotlib.text.Text", but ' +
            'is {t}'.format(t=txt),
        )
    # check if number
    if not tools.is_number(contourwidth):
        raise TypeError(
            'contourwidth={w} needs to be a number.'.format(w=contourwidth),
        )

    # check if color
    if not clr.is_color_like(contourcolor):
        raise TypeError(
            'contourcolor={c} can not be '.format(c=contourcolor) +
            'interpreted as color.',
        )

    path_args = [path_effects.withStroke(
        linewidth=contourwidth, foreground=contourcolor,
    )]
    txt.set_path_effects(path_args)


def _parse_contour(contour):
    """Parse contour tuple argument to kwargs."""
    if isinstance(contour, bool) and int(contour) in {0, 1}:
        if contour:
            return {
                'contourwidth': plt.rcParams['lines.linewidth'],
                'contourcolor': 'w',
            }
        return None
    elif isinstance(contour, (list, tuple)) and len(contour) == 2:
        lw, lc = contour
        if not clr.is_color_like(lc):
            raise ValueError(
                'contourcolor={c} can not be '.format(c=lc) +
                'interpreted as color.',
            )
        return {'contourwidth': lw, 'contourcolor': lc}
    raise TypeError(
        'contour needs to be a boolean or a tuple/list, but given was: ' +
        '{c}.'.format(c=contour),
    )
