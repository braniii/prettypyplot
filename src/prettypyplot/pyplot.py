# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2020-2023, Daniel Nagel
# All rights reserved.
"""Wrapper for matplotlib plotting functions."""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings
from os import path

import numpy as np
from matplotlib import legend as mlegend
from matplotlib import pyplot as plt
from matplotlib import ticker as mticker
from mpl_toolkits import axes_grid1 as mpl_axes_grid1

import prettypyplot as _pplt
from prettypyplot import tools
from prettypyplot.style import Mode, Style


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def imshow(*args, ax=None, **kwargs):
    """Display an image, i.e. data on a 2D regular raster.

    This is a wrapper of pyplot.imshow(). In contrast to the original function
    the default value of `zorder` is increased to `1`.

    Parameters
    ----------
    ax : Axes, optional
        [matplotlib.axes.Axes][] to plot in.
    args, kwargs
        See [matplotlib.pyplot.imshow][].

    Returns
    -------
    im : AxesImage
        Reference to plotted image [matplotlib.image.AxesImage][]

    """
    args, ax = tools.parse_axes(*args, ax=ax)

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 1

    # plot
    return ax.imshow(*args, **kwargs)


def plot(*args, ax=None, **kwargs):
    """Plot simple lineplot.

    Wrapping pyplot.plot() to adjust to style. For more information on the
    arguments see in matplotlib documentation.
    If `STYLE='minimal'`, spines will be limited to plotting range.

    Parameters
    ----------
    ax : Axes
        [matplotlib.axes.Axes][] to plot in.
    args, kwargs
        See [matplotlib.pyplot.plot][].

    Returns
    -------
    lines : list of Line2D
        A list of [matplotlib.lines.Line2D][] representing the plotted data.

    """
    # parse axes
    args, ax = tools.parse_axes(*args, ax=ax)

    # plot
    lines = ax.plot(*args, **kwargs)

    if _pplt.STYLE == Style.MINIMAL:
        _set_spine_bounds(ax)

    return lines


def savefig(fname, use_canvas_size=True, **kwargs):
    """Save figure as png and pdf.

    This methods corrects figsize for poster/beamer mode.

    Parameters
    ----------
    fname : str
        Output filename. If no file ending, pdf will be used.
    use_canvas_size : bool, optional
        If True the specified figsize will be used as canvas size.
    kwargs
        See [matplotlib.pyplot.savefig][].

    """
    fig = plt.gcf()
    ax = fig.get_axes()[0]
    figsize = fig.get_size_inches()

    # store figsize to reset it later
    set_figsize = figsize

    if _pplt.STYLE == Style.MINIMAL:
        _reduce_ticks(fig)

    if _pplt.MODE in {Mode.POSTER, Mode.BEAMER}:
        fig.set_size_inches(
            (3 * figsize[0], 3 * figsize[1]),
        )

    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        fig.tight_layout()

    # convert figsize to canvas size
    if use_canvas_size:
        x0, y0, width, height = ax.get_position().bounds
        figsize = (figsize[0] / width, figsize[1] / height)
        fig.set_size_inches(figsize)

    # save as pdf if not specified
    if 'format' not in kwargs:
        if path.splitext(fname)[1][1:] == '':
            fname = '{0}.pdf'.format(fname)

    # save fig
    plt.savefig(fname, **kwargs)

    # reset figsize, if user calls this function multiple times on same figure
    fig.set_size_inches(set_figsize)


def _reduce_ticks(fig):
    """Reduce number of ticks by factor 1.5 if more than 4."""
    # TODO: replace this by mpl built-in class
    tick_reduc = 1.5
    for axes in fig.get_axes():
        custom_xticks = isinstance(
            axes.xaxis.get_major_locator(), mticker.FixedLocator,
        )
        custom_yticks = isinstance(
            axes.yaxis.get_major_locator(), mticker.FixedLocator,
        )
        if len(axes.get_xticks()) > 4 and not custom_xticks:
            axes.locator_params(
                tight=False,
                axis='x',
                nbins=len(axes.get_xticks()) / tick_reduc,
            )
        if len(axes.get_yticks()) > 4 and not custom_yticks:
            axes.locator_params(
                tight=False,
                axis='y',
                nbins=len(axes.get_yticks()) / tick_reduc,
            )


def _legend_default_kwargs():
    """Return default values of given outside positions."""
    return {
        'top': {
            'bbox_to_anchor': (0.0, 1.0, 1.0, 0.01),
            'mode': 'expand',
            'loc': 'lower left',
        },
        'bottom': {
            'bbox_to_anchor': (0.0, 0.0, 1.0, 0.01),
            'mode': 'expand',
            'loc': 'upper left',
        },
        'right': {
            'bbox_to_anchor': (1.03, 0.5),
            'loc': 'center left',
        },
        'left': {
            'bbox_to_anchor': (-0.03, 0.5),
            'loc': 'center right',
        },
    }


def legend(*args, outside=False, ax=None, axs=None, **kwargs):
    """Generate a nice legend.

    This is a wrapper of pyplot.legend(). Take a look there for the default
    arguments and options. The ticks and labels are moved to the opposite side.
    For `top` and `bottom` the default value of columns is set to the number of
    labels, for all other options to 1. In case of many labels this parameter
    needs to be adjusted.

    !!! note
        Use handles and labels from *args if provided

    !!! example
        Checkout the gallery for [an example](../../gallery/legend).

    Parameters
    ----------
    outside : str or bool
        False, 'top', 'right', 'bottom' or 'left'.
    axs : list of Axes
        List of [matplotlib.axes.Axes][] which are used for extracting all
        labels.
    ax : Axes
        [matplotlib.axes.Axes][] which is used for placing legend.
    args, kwargs
        See [matplotlib.pyplot.legend][].

    Returns
    -------
    leg : Legend
        [matplotlib.legend.Legend] legend handle.

    """
    default_kwargs = _legend_default_kwargs()
    if outside not in {False, *default_kwargs}:
        raise ValueError(
            'Use for outside one of [False, {0}]'.format(
                ', '.join(['"{0}"'.format(dr) for dr in default_kwargs]),
            ),
        )

    # parse axes
    args, ax = tools.parse_axes(*args, ax=ax)

    # parse axs
    if axs is None:
        axs = [ax]
    else:
        axs = tools.get_axes(axs)

    # shift axis to opposite side.
    if outside:
        activate_axis(_opposite_side(outside))

    # set anchor, mode and location
    kwargs = {**default_kwargs.get(outside, {}), **kwargs}

    # get handles and labels of selected axes
    handles, labels = mlegend._get_legend_handles_labels(axs)  # noqa: WPS437

    # set number of ncol to the number of items
    if outside in {'top', 'bottom'}:
        kwargs.setdefault('ncol', len(labels))

    # generate legend
    leg = ax.legend(handles, labels, *args, **kwargs)
    if _pplt.STYLE == Style.MINIMAL:
        leg.get_frame().set_linewidth(0.0)
    elif _pplt.STYLE == Style.DEFAULT:
        leg.get_frame().set_linewidth(plt.rcParams['axes.linewidth'])

    # shift title to the left if on top or bottom
    if outside in {'top', 'bottom'}:
        _shift_legend_title(leg)

    return leg


def _shift_legend_title(leg):
    """Shift title to the left of the labels."""
    # taken from: https://stackoverflow.com/a/53329898
    child = leg.get_children()[0]
    title = child.get_children()[0]
    hpack = child.get_children()[1]
    child._children = [hpack]  # noqa: WPS437
    hpack._children = [title] + hpack.get_children()  # noqa: WPS437


def _opposite_side(pos):
    """Return opposite of 'top', 'bottom', 'left', 'right'."""
    opposite = {
        'top': 'bottom',
        'bottom': 'top',
        'right': 'left',
        'left': 'right',
    }
    if pos not in opposite:
        raise ValueError(
            'Pos needs to be one of [{0}].'.format(
                ', '.join('"{0}"'.format(position) for position in opposite),
            ),
        )

    return opposite[pos]


def activate_axis(position, ax=None):
    """Shift the specified axis to the opposite side.

    Parameters
    ----------
    position : str or list of str
        Specify axis to flip, one of `['left', 'right', 'top', 'bottom']`.
    ax : Axes
        [matplotlib.axes.Axes][] axes to flip axis.

    """
    # get axes
    ax = tools.gca(ax)

    # convert string to list of strings
    if isinstance(position, str):
        position = [position]

    # allowed values
    positions = {'bottom', 'top', 'left', 'right'}

    # move axes ticks and labels to opposite side of position
    for pos in position:
        if pos not in positions:
            raise ValueError(
                '{0:!r} is not a valid value for {1}; supported values are {2}'
                .format(pos, 'position', ', '.join(positions))
            )

        if pos in {'bottom', 'top'}:
            axis = ax.xaxis
        elif pos in {'left', 'right'}:
            axis = ax.yaxis
        axis.set_ticks_position(pos)
        axis.set_label_position(pos)


def colorbar(im, width='7%', pad='0%', position='right', label=None, **kwargs):
    """Generate colorbar of same height as image.

    Wrapper around pyplot.colorbar which corrects the height.

    !!! example
        Checkout the gallery for [an example](../../gallery/colorbar).

    Parameters
    ----------
    im : matplotlib.axes.AxesImage
        Specify the object the colorbar belongs to, e.g. the return value of
        [matplotlib.pyplot.imshow][].
    width : str or float, optional
        The width between figure and colorbar stated relative as string ending
        with '%' or absolute value in inches.
    pad : str or float, optional
        The width between figure and colorbar stated relative as string ending
        with '%' or absolute value in inches.
    position : str, optional
        Specify the position relative to the image where the colorbar is
        plotted, choose one of ['left', 'top', 'right', 'bottom']
    label : str, optional
        Specify the colorbar label.
    kwargs
        Colorbar properties of, [matplotlib.pyplot.colorbar][].

    Returns
    -------
    colorbar : Colorbar
        [matplotlib.colorbar.Colorbar][] instance.

    """
    orientation = 'vertical'
    if position in {'top', 'bottom'}:
        orientation = 'horizontal'

    # get axes
    if hasattr(im, 'axes'):  # noqa: WPS421
        ax = im.axes
    elif hasattr(im, 'ax'):  # noqa: WPS421
        ax = im.ax
    else:
        ax = plt.gca()

    # generate divider
    divider = mpl_axes_grid1.make_axes_locatable(ax)
    cax = divider.append_axes(position, width, pad=pad)

    cbar = plt.colorbar(im, cax=cax, orientation=orientation, **kwargs)
    if label:
        cbar.set_label(label)

    # set ticks and label of ticks to the outside
    activate_axis(position, ax=cax)
    # set the axis opposite to the colorbar to active
    activate_axis(_opposite_side(position), ax=ax)

    # invert width and pad
    pad_inv, width_inv = tools.invert_sign(pad), tools.invert_sign(width)
    cax_reset = divider.append_axes(position, width_inv, pad=pad_inv)
    cax_reset.set_visible(False)

    return cbar


def grid(*args, ax=None, **kwargs):
    """Generate grid.

    This function will add a major and minor grid in case of STYLE='default',
    a major grid in case of 'none' and otherwise nothing.

    Parameters
    ----------
    ax : Axes
        [matplotlib.axes.Axes] axes to plot grid.
    args, kwargs
        See [matplotlib.pyplot.grid][].

    """
    # parse axes
    args, ax = tools.parse_axes(*args, ax=ax)

    if 'visible' in kwargs:  # mpl >= 3.6
        show_grid = kwargs['visible']
    elif 'b' in kwargs:  # mpl <=3.5
        show_grid = kwargs['b']
    else:
        boolargs = [arg for arg in args if isinstance(arg, bool)]
        show_grid = boolargs[0] if len(boolargs) >= 1 else True

    if _pplt.STYLE != Style.MINIMAL and show_grid:
        gr_maj = ax.grid(show_grid, which='major', linestyle='--', **kwargs)
        gr_min = ax.grid(
            show_grid, which='minor', linestyle='dotted', **kwargs
        )
    else:
        gr_maj = ax.grid(False, which='major')
        gr_min = ax.grid(False, which='minor')

    ax.set_axisbelow(True)
    return (gr_maj, gr_min)


def _xminmax(ax):
    """Get xrange of plotted data."""
    return _minmax(lim=ax.get_xlim(), rcparam='axes.xmargin')


def _yminmax(ax):
    """Get yrange of plotted data."""
    return _minmax(lim=ax.get_ylim(), rcparam='axes.ymargin')


def _minmax(lim, rcparam):
    """Get range of plotted data."""
    width = lim[1] - lim[0]
    margin = plt.rcParams[rcparam]
    return lim[0] + np.array([  # min max
        (margin + idx) / (1 + 2 * margin) * width
        for idx in (0, 1)
    ])


def _set_spine_bounds(ax):
    """Limit spines to data range, keeping ticks unchanged."""
    for minmax, ticks, poss in (
        (_xminmax(ax), ax.get_xticks(), ('bottom', 'top')),
        (_yminmax(ax), ax.get_yticks(), ('left', 'right')),
    ):
        if ticks.size:
            for pos in poss:
                ax.spines[pos].set_bounds(*minmax)
