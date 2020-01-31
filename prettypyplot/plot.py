"""
Set-up matplotlib environment.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os.path

import matplotlib as mpl  # mpl = dm.tryImport('matplotlib')
import matplotlib.legend as mlegend
import matplotlib.pyplot as plt
import mpl_toolkits.axes_grid1
import numpy as np  # np = dm.tryImport('numpy')

import prettypyplot.colors
from prettypyplot import _tools

# ~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__MODE = 'default'  # default mode
__STYLE = 'default'  # default style


def _apply_style(path):
    """Load mplstyle file at given relative path to this file."""
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, path)

    # load and apply style
    plt.style.use(path)


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def setup_pyplot(ssh=False, colors='pastel5', cmap='macaw', ncs=10,
                 figsize=(3,), figratio='golden', mode=__MODE, style=__STYLE,
                 ipython=False, true_black=False):
    """
    Define default matplotlib style.

    Parameters
    ----------
    ssh : bool, optional
        Disables interactive display for ssh usage

    colors : matplotlib colormap, optional
        Set the default color cycler from continuous or discrete maps. Use any
        of matplotlibs defaults or specified in the colors submodule.

    cmap : matplotlib colormap, optional
        Set the default colormap.

    ncs : int, optional
        Number of colors if continuous cmap is selected.

    figsize : int or int tuple, optional
        Give size of default figure in inches, either as tuple (x, y) or a
        single float for the x-axis. The y-axis will be determined by figratio.

    figratio : str or float, optional
        Set ratio of figsize x:y to 1:1/'option', where 'option' is one
        of ['sqrt(2)', 'golden', 'sqrt(3)'] or any number. Golden stands for
        the golden ratio (1.618). This option is ignored if figsize is used
        with tuple.

    mode : str, optional
        One of the following modes.
        default: use matplotlib defaults
        beamer: extra large fontsize
        print: default sizes
        poster: for Din A0 posters

    style : str, optional
        One of the following styles.
        default: enables grid and upper and right spines
        minimal: removes all unneeded lines
        none: no changes to style

    ipython : bool, optional
        Deactivate high-res in jpg/png for compatibility with IPyhton, e.g.
        jupyter notebook/lab.

    true_black : bool, optional
        If true black will be used for labels and co., else a dark grey.

    """
    # set selected mode and style
    global __MODE
    __MODE = mode
    global __STYLE
    __STYLE = style

    if ssh:
        mpl.use('Agg')
        plt.ioff()

    # setup LaTeX font
    # plt.style.use can not be used.
    _apply_style('stylelib/latex.mplstyle')

    # register own continuous and discrete cmaps
    prettypyplot.colors.load_cmaps()

    # convert figratio to value
    figratio = _tools._parse_figratio(figratio)

    # setup figsize
    figsize = _tools._parse_figsize(figsize, figratio)

    if style != 'none':
        # load static rcParams
        _apply_style('stylelib/default.mplstyle')
        if style == 'minimal':
            _apply_style('stylelib/minimal.mplstyle')

        # set color cycle and cmap
        try:
            # try if discrete cmap was selected
            color_cycler = plt.cycler(color=plt.get_cmap(colors).colors)
        except AttributeError:
            color_cycler = plt.cycler(
                color=plt.get_cmap(colors)(np.linspace(0, 1, ncs)))

        plt.rcParams['axes.prop_cycle'] = color_cycler
        plt.rcParams['image.cmap'] = cmap

        # change default colors
        if true_black:
            gray_dark = prettypyplot.colors.black_grays['dark']
            gray_light = prettypyplot.colors.black_grays['light']
        else:
            gray_dark = prettypyplot.colors.default_grays['dark']
            gray_light = prettypyplot.colors.default_grays['light']

        plt.rcParams['axes.edgecolor'] = gray_dark
        plt.rcParams['axes.labelcolor'] = gray_dark
        plt.rcParams['text.color'] = gray_dark
        plt.rcParams['patch.edgecolor'] = gray_dark
        plt.rcParams['xtick.color'] = gray_dark
        plt.rcParams['ytick.color'] = gray_dark
        plt.rcParams['patch.edgecolor'] = gray_dark
        plt.rcParams['grid.color'] = gray_light

        # set figure
        plt.rcParams['figure.figsize'] = figsize

        # change widths depending on MODE
        for scale, rcParamsVal in [
                ['small_scale', [['axes.linewidth', 0.8],
                                 ['grid.linewidth', 0.8],
                                 ['xtick.major.width', 0.8],
                                 ['xtick.minor.width', 0.6]]],
                ['tick_scale', [['xtick.major.size', 3.5],
                                ['xtick.minor.size', 2.0],
                                ['xtick.major.pad', 3.5],
                                ['xtick.minor.pad', 3.4]]],
                ['medium_scale', [['patch.linewidth', 1.0],
                                  ['hatch.linewidth', 1.0]]],
                ['large_scale', [['lines.linewidth', 1.5]]],
                ['fontsize', [['font.size', 1]]]]:
            scale = __get_scale()[scale]
            for rcParam, val in rcParamsVal:
                plt.rcParams[rcParam] = scale * val
                # apply all changes to yticks as well
                if rcParam.startswith('xtick'):
                    plt.rcParams['y' + rcParam[1:]] = plt.rcParams[rcParam]

        if not ipython:
            plt.rcParams['figure.dpi'] = 384


def imshow(*args, ax=None, **kwargs):
    """
    Display an image, i.e. data on a 2D regular raster.

    This is a wrapper of pyplot.imshow(). In contrast to the original function
    the default value of `zorder` is increased to `1`.

    Parameters
    ----------
    ax : matplotlib axes, optional
        Matplotlib axes to plot in.

    args, kwargs
        See [pyplot.imshow()](MPL_DOC.pyplot.imshow.html)

    """
    args, ax = _tools._parse_axes(*args, ax=ax)

    if 'zorder' not in kwargs:
        kwargs['zorder'] = 1

    # plot
    im = ax.imshow(*args, **kwargs)

    return im


def plot(*args, ax=None, **kwargs):
    """
    Plot simple lineplot.

    Wrapping pyplot.plot() to adjust to style. For more information on the
    arguments see in matplotlib documentation.
    If STYLE='minimal', spines will be limited to plotting range.

    Parameters
    ----------
    ax : matplotlib axes
        Matplotlib axes to plot in.

    args, kwargs
        See [pyplot.plot()](MPL_DOC.pyplot.plot.html)

    """
    # parse axes
    args, ax = _tools._parse_axes(*args, ax=ax)

    # plot
    axes = ax.plot(*args, **kwargs)

    if __STYLE == 'minimal':
        # TODO: change this to function
        xminmax = __xminmax(ax)
        xticks = ax.get_xticks()
        if xticks.size:
            ax.spines['bottom'].set_bounds(xminmax[0], xminmax[1])
            ax.spines['top'].set_bounds(xminmax[0], xminmax[1])
            # firsttick = np.compress(xticks >= min(ax.get_xlim()), xticks)[0]
            # lasttick = np.compress(xticks <= max(ax.get_xlim()), xticks)[-1]
            # ax.spines['bottom'].set_bounds(firsttick, lasttick)
            # ax.spines['top'].set_bounds(firsttick, lasttick)
            # newticks = xticks.compress(xticks <= lasttick)
            # newticks = newticks.compress(newticks >= firsttick)
            # ax.set_xticks(newticks)

        yminmax = __yminmax(ax)
        yticks = ax.get_yticks()
        if yticks.size:
            ax.spines['left'].set_bounds(yminmax[0], yminmax[1])
            ax.spines['right'].set_bounds(yminmax[0], yminmax[1])
            # firsttick = np.compress(yticks >= min(ax.get_ylim()), yticks)[0]
            # lasttick = np.compress(yticks <= max(ax.get_ylim()), yticks)[-1]
            # ax_i.spines['left'].set_bounds(firsttick, lasttick)
            # ax_i.spines['right'].set_bounds(firsttick, lasttick)
            # newticks = yticks.compress(yticks <= lasttick)
            # newticks = newticks.compress(newticks >= firsttick)
            # ax.set_yticks(newticks)

    return axes


def savefig(fname, use_canvas_size=True, **kwargs):
    """
    Save figure as png and pdf.

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
    fig, ax = plt.gcf(), plt.gcf().get_axes()[0]
    figsize = fig.get_size_inches()

    set_figsize = figsize

    if __STYLE == 'minimal':
        # reduce number of ticks by factor 1.5 if more than 4
        for axes in plt.gcf().get_axes():
            if len(axes.get_xticks()) > 4:
                axes.locator_params(tight=False, axis='x',
                                    nbins=len(axes.get_xticks()) / 1.5)
            if len(axes.get_yticks()) > 4:
                axes.locator_params(tight=False, axis='y',
                                    nbins=len(axes.get_yticks()) / 1.5)

    if __MODE == 'poster':
        fig.set_size_inches((3 * figsize[0], 3 * figsize[1]))
    elif __MODE == 'beamer':
        fig.set_size_inches((3 * figsize[0], 3 * figsize[1]))

    fig.tight_layout(pad=0.20, h_pad=0.00, w_pad=0.00)

    # convert figsize to canvas size
    if use_canvas_size:
        x0, y0, width, height = ax.get_position().bounds
        figsize = (figsize[0] / width, figsize[1] / height)
        fig.set_size_inches(figsize)

    # save as pdf if not specified
    if 'format' not in kwargs:
        fmt = os.path.splitext(fname)[1][1:]
        if format == '':
            fmt = 'pdf'
            fname = '{0}.{1}'.format(fname, fmt)

    # save fig
    plt.savefig(fname, **kwargs)

    # reset figsize, if user calls this function multiple times on same figure
    fig.set_size_inches(set_figsize)


def legend(*args, outside=False, ax=None, axs=None, **kwargs):
    """
    Generate a nice legend.

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

    args, kwargs
        See [pyplot.legend()](MPL_DOC.pyplot.legend.html)

    Returns
    -------
    leg
        Matplotlib legend handle.

    Examples
    --------
    .. include:: ../gallery/legend/README.md

    """
    if outside not in [False, 'top', 'right', 'left', 'bottom']:
        raise ValueError('Use for outside one of [False, "top", "right", '
                         '"left", "bottom"]')

    # parse axes
    args, ax = _tools._parse_axes(*args, ax=ax)

    # parse axs
    if axs is None:
        axs = [ax]
    elif not all((isinstance(arg, mpl.axes.Axes) for arg in axs)):
        raise TypeError('axs needs to be of type matplotlib.axes.Axes.')

    # shift axis to opposite side.
    if outside:
        activate_axis(__opposite_side(outside))

    # set anchor, mode and location
    if outside == 'top':
        kwargs.setdefault('bbox_to_anchor', (0., 1.0, 1., .01))
        kwargs.setdefault('mode', 'expand')
        kwargs.setdefault('loc', 'lower left')
    elif outside == 'bottom':
        kwargs.setdefault('bbox_to_anchor', (0., 0., 1., .01))
        kwargs.setdefault('mode', 'expand')
        kwargs.setdefault('loc', 'upper left')
    elif outside == 'right':
        kwargs.setdefault('bbox_to_anchor', (1.03, .5))
        kwargs.setdefault('loc', 'center left')
    elif outside == 'left':
        kwargs.setdefault('bbox_to_anchor', (-.03, 0.5))
        kwargs.setdefault('loc', 'center right')

    # get handles and labels of selected axes
    handles, labels = mlegend._get_legend_handles_labels(axs)

    # set number of ncol to the number of items
    if outside in ['top', 'bottom']:
        kwargs.setdefault('ncol', len(labels))

    # generate legend
    leg = ax.legend(handles, labels, *args, **kwargs)
    if __STYLE == 'minimal':
        leg.get_frame().set_linewidth(0.)
    elif __STYLE == 'default':
        leg.get_frame().set_linewidth(__get_scale()['small_scale'] * 0.8)

    # shift title to the left if on top or bottom
    # taken from: https://stackoverflow.com/a/53329898
    if outside in ['top', 'bottom']:
        c = leg.get_children()[0]
        title = c.get_children()[0]
        hpack = c.get_children()[1]
        c._children = [hpack]
        hpack._children = [title] + hpack.get_children()

    return leg


def __opposite_side(pos):
    """Return opposite of 'top', 'bottom', 'left', 'right'."""
    if pos == 'top':
        return 'bottom'
    elif pos == 'bottom':
        return 'top'
    elif pos == 'right':
        return 'left'
    elif pos == 'left':
        return 'right'
    raise ValueError('Only "top", "bottom", "left", "right" are accepted.')


def activate_axis(pos, ax=None):
    """
    Shift the specified axis to the opposite side.

    Parameters
    ----------
    pos : str or list of str
        Specify axis to flip, one of ['left', 'right', 'top', 'bottom'].

    ax : matplotlib axes
        Matplotlib axes to flip axis.

    """
    # get axes
    ax = _tools._gca(ax)

    # convert string to list of strings
    if isinstance(pos, str):
        pos = [pos]

    # move axes ticks and labels to opposite side of position
    for p in pos:
        if p in ['bottom', 'top']:
            ax.xaxis.set_ticks_position(p)
            ax.xaxis.set_label_position(p)
        elif p in ['left', 'right']:
            ax.yaxis.set_ticks_position(p)
            ax.yaxis.set_label_position(p)


def __get_scale():
    """Get the scaling factors."""
    if __MODE == 'default':
        return {'large_scale': 1.,
                'medium_scale': 1.,
                'small_scale': 1.,
                'tick_scale': 1.,
                'fontsize': 10.}
    elif __MODE == 'print':
        return {'large_scale': 1.5,
                'medium_scale': 1.7,
                'small_scale': 1.7,
                'tick_scale': 1.7,
                'fontsize': 12.}
    elif __MODE == 'poster':
        return {'large_scale': 4.,
                'medium_scale': 4.,
                'small_scale': 4.,
                'tick_scale': 4.,
                'fontsize': 28.}
    elif __MODE == 'beamer':
        return {'large_scale': 4.,
                'medium_scale': 4.,
                'small_scale': 4.,
                'tick_scale': 4.,
                'fontsize': 28.}


def colorbar(im, width='7%', pad='0%', position='right', label=None, **kwargs):
    """
    Generate colorbar of same height as image.

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

    """
    orientation = 'vertical'
    if position in ['top', 'bottom']:
        orientation = 'horizontal'

    # get axes
    ax = im.axes

    # generate divider
    divider = mpl_toolkits.axes_grid1.make_axes_locatable(ax)
    cax = divider.append_axes(position, width, pad=pad)

    cbar = plt.colorbar(im, cax=cax, orientation=orientation)
    if label:
        cbar.set_label(label)

    # set ticks and label of ticks to the outside
    activate_axis(position, ax=cax)
    # set the axis opposite to the colorbar to active
    activate_axis(__opposite_side(position), ax=ax)

    # invert width and pad
    pad_inv, width_inv = _tools._invert_sign(pad), _tools._invert_sign(width)
    cax_reset = divider.append_axes(position, width_inv, pad=pad_inv)
    cax_reset.set_visible(False)

    return cbar


def grid(*args, ax=None, **kwargs):
    """
    Generate grid.

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
    args, ax = _tools._parse_axes(*args, ax=ax)

    if __STYLE == 'default':
        gr_maj = ax.grid(which='major', linestyle='--', **kwargs)
        gr_min = ax.grid(which='minor', linestyle='dotted', **kwargs)
        ax.set_axisbelow(True)
        return (gr_maj, gr_min)
    else:
        return


def __xminmax(ax):
    """Get xrange of plotted data."""
    return __minmax(lim=ax.get_xlim(), rcparam='axes.xmargin')


def __yminmax(ax):
    """Get yrange of plotted data."""
    return __minmax(lim=ax.get_ylim(), rcparam='axes.ymargin')


def __minmax(lim, rcparam):
    """Get range of plotted data."""
    width = lim[1] - lim[0]
    margin = plt.rcParams[rcparam]
    minmax = [lim[0] + (margin + i) / (1 + 2 * margin) * width for i in [0, 1]]
    return minmax
