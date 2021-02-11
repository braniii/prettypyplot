"""Wrapper for matplotlib plotting functions.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings
from os import path

from matplotlib import legend as mlegend
from matplotlib import pyplot as plt
from mpl_toolkits import axes_grid1 as mpl_axes_grid1

from prettypyplot import tools
from prettypyplot.style import __MODE, __STYLE


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def imshow(*args, ax=None, **kwargs):
    """Display an image, i.e. data on a 2D regular raster.

    This is a wrapper of pyplot.imshow(). In contrast to the original function
    the default value of `zorder` is increased to `1`.

    Parameters
    ----------
    ax : matplotlib axes, optional
        Matplotlib axes to plot in.

    args, kwargs
        See [pyplot.imshow()](MPL_DOC.pyplot.imshow.html)

    Returns
    -------
    im : matplolib.image.AxesImage
        Reference to plotted image.

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
    If STYLE='minimal', spines will be limited to plotting range.

    Parameters
    ----------
    ax : matplotlib axes
        Matplotlib axes to plot in.

    args, kwargs
        See [pyplot.plot()](MPL_DOC.pyplot.plot.html)

    Returns
    -------
    lines : list of matplolib.lines.Line2D
        A list of lines representing the plotted data.

    """
    # parse axes
    args, ax = tools.parse_axes(*args, ax=ax)

    # plot
    lines = ax.plot(*args, **kwargs)

    if __STYLE == 'minimal':
        # TODO: change this to function
        xminmax = _xminmax(ax)
        xticks = ax.get_xticks()
        if xticks.size:
            ax.spines['bottom'].set_bounds(xminmax[0], xminmax[1])
            ax.spines['top'].set_bounds(xminmax[0], xminmax[1])

        yminmax = _yminmax(ax)
        yticks = ax.get_yticks()
        if yticks.size:
            ax.spines['left'].set_bounds(yminmax[0], yminmax[1])
            ax.spines['right'].set_bounds(yminmax[0], yminmax[1])

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
        See [pyplot.savefig()](MPL_DOC.pyplot.savefig.html)

    """
    fig = plt.gcf()
    ax = fig.get_axes()[0]
    figsize = fig.get_size_inches()

    # store figsize to reset it later
    set_figsize = figsize

    if __STYLE == 'minimal':
        _reduce_ticks(fig)

    if __MODE in {'poster', 'beamer'}:
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
    tick_reduc = 1.5
    for axes in fig.get_axes():
        if len(axes.get_xticks()) > 4:
            axes.locator_params(
                tight=False,
                axis='x',
                nbins=len(axes.get_xticks()) / tick_reduc,
            )
        if len(axes.get_yticks()) > 4:
            axes.locator_params(
                tight=False,
                axis='y',
                nbins=len(axes.get_yticks()) / tick_reduc,
            )


def legend(*args, outside=False, ax=None, axs=None, **kwargs):
    """Generate a nice legend.

    This is a wrapper of pyplot.legend(). Take a look there for the default
    arguments and options. The ticks and labels are moved to the opposite side.
    For `top` and `bottom` the default value of columns is set to the number of
    labels, for all other options to 1. In case of many labels this parameter
    needs to be adjusted.

    .. todo::
        Use handles and labels from *args if provided

    Parameters
    ----------
    outside : str or bool
        False, 'top', 'right', 'bottom' or 'left'.

    axs : list of mpl.axes.Axes
        List of axes which are used for extracting all labels.

    ax : mpl.axes.Axes
        Axes which is used for placing legend.

    args, kwargs
        See [pyplot.legend()](MPL_DOC.pyplot.legend.html)

    Returns
    -------
    leg : matplotlib.legend.Legend
        Matplotlib legend handle.

    Examples
    --------
    .. include:: ../gallery/legend/README.md

    """
    default_kwargs = {
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
    if __STYLE == 'minimal':
        leg.get_frame().set_linewidth(0.0)
    elif __STYLE == 'default':
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
        Specify axis to flip, one of ['left', 'right', 'top', 'bottom'].

    ax : matplotlib axes
        Matplotlib axes to flip axis.

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

    Parameters
    ----------
    im : matplotlib.axes.AxesImage
        Specify the object the colorbar belongs to, e.g. the return value of
        pyplot.imshow().

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
        Colorbar properties of
        [pyplot.colorbar()](MPL_DOC.pyplot.colorbar.html)

    Returns
    -------
    colorbar : matplotlib.colorbar.Colorbar
        Colorbar instance.

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

    cbar = plt.colorbar(im, cax=cax, orientation=orientation)
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
    ax : matplotlib axes
        Axes to plot grid.

    args, kwargs
        See [pyplot.grid()](MPL_DOC.pyplot.grid.html)

    """
    # parse axes
    args, ax = tools.parse_axes(*args, ax=ax)

    if __STYLE == 'default':
        gr_maj = ax.grid(which='major', linestyle='--', **kwargs)
        gr_min = ax.grid(which='minor', linestyle='dotted', **kwargs)
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
    return [  # min max
        lim[0] + (margin + idx) / (1 + 2 * margin) * width
        for idx in (0, 1)
    ]
