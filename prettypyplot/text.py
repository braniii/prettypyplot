"""
Plot text.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as mpl
import matplotlib.colors as clr
import matplotlib.patheffects as path_effects
import matplotlib.pyplot as plt

from prettypyplot import _tools


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def text(x, y, s, contourwidth=None, contourcolor=None, ax=None, **kwargs):
    """
    Generate text object at (x,y).

    Wrapper around pyplot.text. The default alignment is changed to centered.

    Parameters
    ----------
    x, y : scalars
        The position to place the text. By default, this is in data
        coordinates. The coordinate system can be changed using the
        *transform* parameter.

    s : str
        The text.

    contourwidth : scalar
        The width of the text contour.

    contourcolor : RGB color or matplotlib predefined color
        Color of the contour.

    ax : matplotlib axes
        Matplotlib axes to plot in.

    kwargs
        Text properties of
        [pyplot.text()](MPL_DOC.pyplot.text.html)

    """
    # parse axes
    ax = _tools._gca(ax)

    # change default alignment
    if 'va' not in kwargs and 'verticalalignment' not in kwargs:
        kwargs['va'] = 'center'
    if 'ha' not in kwargs and 'horizontalalignment' not in kwargs:
        kwargs['ha'] = 'center'

    # plot text
    txt = ax.text(x=x, y=y, s=s, **kwargs)

    # generate contour
    if contourwidth:
        add_contour(txt, contourwidth, contourcolor)

    return txt


def figtext(x, y, s, contourwidth=None, contourcolor=None, **kwargs):
    """
    Generate text object at figure position (x,y).

    Wrapper around pyplot.figtext. The default alignment is changed to
    centered.

    Parameters
    ----------
    x, y : scalars
        The position to place the text. By default, this is in data
        coordinates. The coordinate system can be changed using the
        *transform* parameter.

    s : str
        The text.

    contourwidth : scalar
        The width of the text contour.

    contourcolor : RGB color or matplotlib predefined color
        Color of the contour.

    ax : matplotlib axes
        Matplotlib axes to plot in.

    kwargs
        Text properties of
        [pyplot.figtext()](MPL_DOC.pyplot.figtext.html)

    """
    # change default alignment
    if 'va' not in kwargs and 'verticalalignment' not in kwargs:
        kwargs['va'] = 'center'
    if 'ha' not in kwargs and 'horizontalalignment' not in kwargs:
        kwargs['ha'] = 'center'

    # plot text
    txt = plt.figtext(x=x, y=y, s=s, **kwargs)

    # generate contour
    if contourwidth:
        add_contour(txt, contourwidth, contourcolor)

    return txt


def add_contour(txt, contourwidth, contourcolor='w'):
    r"""Draw contour around txt.

    Parameters
    ----------
    txt : matplotlib.text.Text
        Instance of matplotlib text. Can be obtained by, e.g.,
        `txt = plt.text()` or `txt = plt.figtext()`.

    contourwidth : scalar
        Width of contour.

    contourcolor : RGB color or matplotlib predefined color, optional
        Color of contour, default is white.

    """
    # check if is text object
    if not isinstance(txt, mpl.text.Text):
        raise TypeError('txt needs to be "matplotlib.text.Text", but'
                        ' is {t}'.format(t=type(txt)))
    # check if number
    if not _tools._is_number(contourwidth):
        raise TypeError('contourwidth={w} needs to be a number.'
                        .format(w=contourwidth))

    # check if color
    if not clr.is_color_like(contourcolor):
        raise TypeError('contourcolor={c} can not be interpreted as color.'
                        .format(c=contourcolor))

    path_args = [path_effects.withStroke(linewidth=contourwidth,
                                         foreground=contourcolor)]
    txt.set_path_effects(path_args)
