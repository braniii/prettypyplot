# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2020-2023, Daniel Nagel
# All rights reserved.
"""Set-up matplotlib environment."""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from enum import Enum, auto
from os import path as ospath

import numpy as np
from matplotlib import pyplot as plt
from decorit import copy_doc_params, deprecated

import prettypyplot as _pplt
from prettypyplot import tools
from prettypyplot import colors as pclr


# ~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Style(Enum):
    """Enum for all styles defined in pplt."""
    DEFAULT = auto()
    # default style, good for scientific usage
    MINIMAL = auto()
    # minimal style, good for slides, posters and co.
    NONE = auto()
    # do not change matplotlib style

    @classmethod
    def keys_list(cls):
        """Return list of available Style names."""
        return list(cls.__members__.keys())


class Mode(Enum):
    """Enum for all modes defined in pplt."""
    DEFAULT = auto()
    # default font size, good for monitor use
    PRINT = auto()
    # slightly larger fonts compared to default
    BEAMER = auto()
    # large fonts, good for slides
    POSTER = auto()
    # large fonts, good for A0 posters

    @classmethod
    def keys_list(cls):
        """Return list of available Mode names."""
        return list(cls.__members__.keys())


# set default mode and style
if _pplt.MODE is None:
    _pplt.MODE = Mode.DEFAULT
if _pplt.STYLE is None:
    _pplt.STYLE = Style.DEFAULT


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_style(
    interactive=None,
    colors=None,
    cmap=None,
    ncs=None,
    figsize=None,
    figratio=None,
    mode=None,
    style=None,
    ipython=None,
    true_black=None,
    latex=None,
    sf=None,
):
    """Update alternative matplotlib style.

    This function updates specified parameters of `use_style` without changing
    other.

    Parameters
    ----------
    interactive : bool, optional
        Set interactive mode.
    colors : string, optional
        Set the default color cycler from continuous or discrete maps. Use any
        of matplotlibs defaults or specified in the colors submodule.
    cmap : string, optional
        Set the default colormap.
    ncs : int, optional
        Number of colors if continuous cmap is selected.
    figsize : int or int tuple, optional
        Give size of default figure in inches, either as tuple (x, y) or a
        single float for the x-axis. The y-axis will be determined by figratio.
    figratio : str or float, optional
        Set ratio of figsize x:y to 1:1/'option', where 'option' is one
        of `['sqrt(2)', 'golden', 'sqrt(3)']` or any number. Golden stands for
        the golden ratio (1.618). This option is ignored if figsize is used
        with tuple.
    mode : str, optional
        One of the following modes:
        `'default'`: use matplotlib defaults
        `'beamer'`: extra large fontsize
        `'print'`: default sizes
        `'poster'`: for Din A0 posters
    style : str, optional
        One of the following styles:
        `'default'`: enables grid and upper and right spines
        `'minimal'`: removes all unneeded lines
        `'none'`: no changes to style
    ipython : bool, optional
        Deactivate high-res in jpg/png for compatibility with IPyhton, e.g.
        jupyter notebook/lab.
    true_black : bool, optional
        If true black will be used for labels and co., else a dark grey.
    latex : bool, optional
        If true LaTeX font will be used.
    sf : bool, optional
        Use sans-serif font for text and latex math environment.

    """
    # set selected mode and style
    if style is not None:
        if isinstance(style, Style):
            pass
        elif isinstance(style, str) and style.upper() in Style.keys_list():
            style = Style[style.upper()]
        else:
            raise ValueError(
                'Style "{st}" is not supported, use one of {sts}.'.format(
                    st=style,
                    sts=Style.keys_list(),
                ),
            )
        _pplt.STYLE = style

    if mode is not None:
        if isinstance(mode, Mode):
            pass
        elif isinstance(mode, str) and mode.upper() in Mode.keys_list():
            mode = Mode[mode.upper()]
        else:
            raise ValueError(
                'Mode "{mode}" is not supported, use one of {modes}.'.format(
                    mode=mode,
                    modes=Mode.keys_list(),
                ),
            )

        _pplt.MODE = mode

    # set style variables in dictionary
    for key, val in (
        ('interactive', interactive),
        ('colors', colors),
        ('cmap', cmap),
        ('ncs', ncs),
        ('figsize', figsize),
        ('figratio', figratio),
        ('ipython', ipython),
        ('true_black', true_black),
        ('latex', latex),
        ('sf', sf),
    ):
        if val is not None:
            _pplt.STYLE_DICT[key] = val

    if _pplt.STYLE is Style.NONE:
        _reset_style()
    else:
        # load static rcParams
        _apply_style('stylelib/default.mplstyle')
        if _pplt.STYLE is Style.MINIMAL:
            _apply_style('stylelib/minimal.mplstyle')

        # set color cycle and cmap
        _set_rc_colors(
            colors=colors, cmap=cmap, ncs=ncs, true_black=true_black,
        )

        # set figsize
        if figsize is not None:
            _set_rc_figsize(figratio=figratio, figsize=figsize)

        # increase dpi if not in iypthon
        _set_rc_dpi(ipython)

        # set interactive mode
        _set_ineractive_mode(interactive=interactive)

        # setup LaTeX font
        # plt.style.use can not be used.
        if latex:
            _apply_style('stylelib/latex.mplstyle')

        if sf:
            _set_rc_sansserif()

    if mode is not None:
        # change widths and fontsize depending on MODE
        _set_rc_widths(mode)


@copy_doc_params(update_style)
def use_style(
    interactive=None,
    colors='pastel5',
    cmap='macaw',
    ncs=10,
    figsize=(3,),
    figratio='golden',
    mode=_pplt.MODE,
    style=_pplt.STYLE,
    ipython=False,
    true_black=False,
    latex=True,
    sf=False,
):
    """Define alternative matplotlib style.

    This function restores first the matplolib default values and finally
    changes depicted values to achieve a more appealing appearence.
    It additionally loads pplts colormaps and colors in matplolib.

    See [update_style][prettypyplot.update_style] for parameters.

    """
    # restore matplotlib defaults
    _reset_style()

    # register own continuous and discrete cmaps
    pclr.load_cmaps()

    # update style
    update_style(
        interactive=interactive,
        colors=colors,
        cmap=cmap,
        ncs=ncs,
        figsize=figsize,
        figratio=figratio,
        mode=mode,
        style=style,
        ipython=ipython,
        true_black=true_black,
        latex=latex,
        sf=sf,
    )

    # register used colors
    pclr.load_colors()


@copy_doc_params(update_style)
@deprecated(
    msg=r'Use prettypyplot.use_style instead.', since='0.4', remove='0.11',
)
def setup_pyplot(
    ssh=None,
    colors='pastel5',
    cmap='macaw',
    ncs=10,
    figsize=(3,),
    figratio='golden',
    mode=_pplt.MODE,
    style=_pplt.STYLE,
    ipython=False,
    true_black=False,
    latex=True,
):
    """Define alternative matplotlib style.

    This function restores first the matplolib default values and finally
    changes depicted values to achieve a more appealing appearence.

    !!! deprecated
        This is deprecated since version 0.4, please use `use_style` instead.

    """
    interactive = ssh
    if interactive is not None:
        interactive = not interactive

    use_style(
        interactive=interactive,
        colors=colors,
        cmap=cmap,
        ncs=ncs,
        figsize=figsize,
        figratio=figratio,
        mode=mode,
        style=style,
        ipython=ipython,
        true_black=true_black,
        latex=latex,
        sf=False,
    )


def _set_rc_colors(colors, cmap, true_black, ncs):
    """Set rcParams colors."""
    # set color cycle and cmap
    if colors is not None or ncs is not None:
        # use values of previous call in case of None
        colors = colors if colors is not None else _pplt.STYLE_DICT['colors']
        ncs = ncs if ncs is not None else _pplt.STYLE_DICT['ncs']

        clrs = plt.get_cmap(colors)
        plt.rcParams['axes.prop_cycle'] = plt.cycler(
            color=(
                clrs.colors if tools.is_discrete_cmap(colors) else
                clrs(np.linspace(0, 1, ncs))
            ),
        )

    if cmap is not None:
        plt.rcParams['image.cmap'] = cmap

    if true_black is not None:
        # change default colors
        if true_black:
            grays = pclr.black_grays
        else:
            grays = pclr.default_grays

        plt.rcParams.update({
            'axes.edgecolor': grays.dark,
            'axes.labelcolor': grays.dark,
            'text.color': grays.dark,
            'patch.edgecolor': grays.dark,
            'xtick.color': grays.dark,
            'ytick.color': grays.dark,
            'grid.color': grays.light,
        })


def _set_rc_figsize(figratio, figsize):
    """Set rcParams figsize."""
    # setup figsize
    figsize = _parse_figsize(figsize, figratio)

    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize


def _set_rc_widths(mode):
    """Set rcParams widths and fontsizes according to mode."""
    scales = _get_scale(mode)
    if scales is not None:
        for scale, rcParamsVal in [
            [
                'small_scale',
                [
                    ['axes.linewidth', 0.8],
                    ['grid.linewidth', 0.8],
                    ['xtick.major.width', 0.8],
                    ['xtick.minor.width', 0.6],
                ],
            ],
            [
                'tick_scale',
                [
                    ['xtick.major.size', 3.5],
                    ['xtick.minor.size', 2.0],
                    ['xtick.major.pad', 3.5],
                    ['xtick.minor.pad', 3.4],
                ],
            ],
            [
                'medium_scale',
                [
                    ['patch.linewidth', 1.0],
                    ['hatch.linewidth', 1.0],
                    ['boxplot.flierprops.markeredgewidth', 1.0],
                    ['boxplot.flierprops.linewidth', 1.0],
                    ['boxplot.boxprops.linewidth', 1.0],
                    ['boxplot.whiskerprops.linewidth', 1.0],
                    ['boxplot.capprops.linewidth', 1.0],
                    ['boxplot.medianprops.linewidth', 1.0],
                    ['boxplot.meanprops.linewidth', 1.0],
                    ['lines.markeredgewidth', 1.0],
                ],
            ],
            [
                'large_scale',
                [
                    ['lines.linewidth', 1.5],
                    ['boxplot.whiskers', 1.5],
                    ['lines.markersize', 6],
                ],
            ],
            ['fontsize', [['font.size', 1]]],
        ]:
            scale = scales[scale]
            for rcParam, val in rcParamsVal:
                plt.rcParams[rcParam] = scale * val
                # apply all changes to yticks as well
                if rcParam.startswith('xtick'):
                    plt.rcParams[
                        'y{0}'.format(rcParam[1:])
                    ] = plt.rcParams[rcParam]


def _set_rc_dpi(ipython, dpi=384):
    """Set rcParams dpi."""
    if ipython is not None and not ipython:
        plt.rcParams['figure.dpi'] = dpi


def _set_rc_sansserif():
    """Set sans serif font."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': 'Helvetica',
    })
    plt.rcParams['text.latex.preamble'] += r'\usepackage[helvet]{sfmath}'


def _set_ineractive_mode(interactive):
    """Set interative mode."""
    if interactive is not None:
        if interactive:
            plt.ion()
        else:
            plt.ioff()


def _get_scale(mode: Mode):
    """Get the scaling factors."""
    scale_dict = {
        Mode.DEFAULT: {
            'large_scale': 1.0,
            'medium_scale': 1.0,
            'small_scale': 1.0,
            'tick_scale': 1.0,
            'fontsize': 10.0,
        },
        Mode.PRINT: {
            'large_scale': 1.5,
            'medium_scale': 1.7,
            'small_scale': 1.7,
            'tick_scale': 1.7,
            'fontsize': 12.0,
        },
        Mode.POSTER: {
            'large_scale': 4.0,
            'medium_scale': 4.0,
            'small_scale': 4.0,
            'tick_scale': 4.0,
            'fontsize': 28.0,
        },
        Mode.BEAMER: {
            'large_scale': 4.0,
            'medium_scale': 4.0,
            'small_scale': 4.0,
            'tick_scale': 4.0,
            'fontsize': 28.0,
        },
    }
    return scale_dict.get(mode, scale_dict[Mode.DEFAULT])


def _reset_style():
    """Restore default matplotlib style."""
    plt.rcdefaults()


def _apply_style(path):
    """Load mplstyle file at given relative path to this file."""
    module_dir = ospath.dirname(__file__)
    path = ospath.join(module_dir, path)

    # load and apply style
    plt.style.use(path)


def _parse_figratio(figratio):
    """Parse the figratio value.

    Parameters
    ----------
    figratio : float or one of ['sqrt(2)', 'sqrt(3)', 'golden']
        Parse the figratio to an numeric value.

    Returns
    -------
    figratio : float
        Numeric figratio.

    """
    if figratio is None:
        figratio = _pplt.STYLE_DICT['figratio']
    elif tools.is_number(figratio):
        figratio = float(figratio)
    else:
        figratios = {
            'sqrt(2)': np.sqrt(2),
            'sqrt(3)': np.sqrt(3),
            'golden': (1 + np.sqrt(5)) / 2,
        }
        if figratio not in figratios:
            raise ValueError(
                'figratio needs to be an numeric value or one of [' +
                '{0}].'.format(', '.join(figratios.keys())),
            )
        figratio = figratios.get(figratio, None)
    return figratio


def _parse_figsize(figsize, figratio):
    """Parse the figsize value.

    Parameters
    ----------
    figsize : float or tuple of floats
        Parse the figsize (in inches) to an numeric value. If only a single
        value is given, the figratio will be used for the second dimension.
    figratio : float or one of ['sqrt(2)', 'sqrt(3)', 'golden'], optional
        Parse the figratio to an numeric value, see `parse_figsize`.

    Returns
    -------
    figsize : tuple
        Tuple of figsize in inches (x, y).

    """
    figsize = tuple(np.atleast_1d(figsize))
    if not all(tools.is_number(size) for size in figsize):
        sizetuple = None
    elif len(figsize) == 1 and figratio is None:
        raise ValueError(
            'using single value for `figsize` requires `figratio` but was not'
            ' specified yet.',
        )
    elif len(figsize) == 1:
        figratio = _parse_figratio(figratio)
        figsize = float(figsize[0])
        sizetuple = (figsize, figsize / figratio)
    elif len(figsize) == 2:
        sizetuple = figsize
    else:
        sizetuple = None

    if sizetuple is None:
        raise ValueError(
            'figsize needs to be an numeric value or a tuple, not ' +
            '{0}.'.format(figsize),
        )
    return sizetuple
