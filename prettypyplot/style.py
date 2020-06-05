"""
Set-up matplotlib environment.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os.path

import matplotlib.pyplot as plt
import numpy as np

import prettypyplot.colors
from prettypyplot import _tools
from prettypyplot.decorators import copy_doc_params, deprecated

# ~~~ CONSTANTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
__MODE = 'default'  # default mode
__STYLE = 'default'  # default style


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def update_style(interactive=None, colors=None, cmap=None, ncs=None,
                 figsize=None, figratio=None, mode=None, style=None,
                 ipython=None, true_black=None, latex=None):
    """Update alternative matplotlib style.

    This function updates specified parameters of `use_style` without changing
    other.

    Parameters
    ----------
    interactive : bool, optional
        Set interactive mode.

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

    latex : bool, optional
        If true LaTeX font will be used.

    """
    # set selected mode and style
    if mode is not None:
        global __MODE
        __MODE = mode
    if style is not None:
        global __STYLE
        __STYLE = style

    if style == 'none':
        __reset_style()
    else:
        # load static rcParams
        __apply_style('stylelib/default.mplstyle')
        if style == 'minimal':
            __apply_style('stylelib/minimal.mplstyle')

        # set color cycle and cmap
        __set_rc_colors(colors=colors,
                        cmap=cmap,
                        ncs=ncs,
                        true_black=true_black)

        # set figsize
        __set_rc_figsize(figratio=figratio, figsize=figsize)

        # change widths and fontsize depending on MODE
        __set_rc_widths(mode)

        # increase dpi if not in iypthon
        __set_rc_dpi(ipython)

    # set interactive mode
    __set_ineractive_mode(interactive=interactive)

    # setup LaTeX font
    # plt.style.use can not be used.
    if latex is not None and latex:
        __apply_style('stylelib/latex.mplstyle')


@copy_doc_params(update_style)
def use_style(interactive=None, colors='pastel5', cmap='macaw', ncs=10,
              figsize=(3,), figratio='golden', mode=__MODE, style=__STYLE,
              ipython=False, true_black=False, latex=True):
    """Define alternative matplotlib style.

    This function restores first the matplolib default values and finally
    changes depicted values to achieve a more appealing appearence.
    It additionally loads pplts colormaps and colors in matplolib.

    """
    # restore matplotlib defaults
    __reset_style()

    # register own continuous and discrete cmaps
    prettypyplot.colors.load_cmaps()

    # update style
    update_style(interactive=interactive, colors=colors, cmap=cmap, ncs=ncs,
                 figsize=figsize, figratio=figratio, mode=mode, style=style,
                 ipython=ipython, true_black=true_black, latex=latex)

    # register used colors
    prettypyplot.colors.load_colors()


@copy_doc_params(update_style)
@deprecated(msg=r'Use prettypyplot.use_style instead.',
            since='0.4', remove='1.0')
def setup_pyplot(ssh=None, colors='pastel5', cmap='macaw', ncs=10,
                 figsize=(3,), figratio='golden', mode=__MODE, style=__STYLE,
                 ipython=False, true_black=False, latex=True):
    """Define alternative matplotlib style.

    This function restores first the matplolib default values and finally
    changes depicted values to achieve a more appealing appearence.

    .. deprecated:: 0.4
        use `use_style` instead

    """
    interactive = ssh
    if interactive is not None:
        interactive = not interactive

    use_style(interactive=interactive, colors=colors, cmap=cmap, ncs=ncs,
              figsize=figsize, figratio=figratio, mode=mode, style=style,
              ipython=ipython, true_black=true_black, latex=latex)


def __set_rc_colors(colors, cmap, ncs, true_black):
    """Set rcParams colors."""
    # set color cycle and cmap
    if colors is not None:
        try:
            # try if discrete cmap was selected
            color_cycler = plt.cycler(color=plt.get_cmap(colors).colors)
        except AttributeError:
            color_cycler = plt.cycler(
                color=plt.get_cmap(colors)(np.linspace(0, 1, ncs)))

        # TODO: refactor following code in private function
        plt.rcParams['axes.prop_cycle'] = color_cycler

    if cmap is not None:
        plt.rcParams['image.cmap'] = cmap

    if true_black is not None:
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


def __set_rc_figsize(figratio, figsize):
    """Set rcParams figsize."""
    # convert figratio to value
    figratio = _tools._parse_figratio(figratio)

    # setup figsize
    figsize = _tools._parse_figsize(figsize, figratio)

    if figsize is not None:
        plt.rcParams['figure.figsize'] = figsize


def __set_rc_widths(mode):
    """Set rcParams widths and fontsizes according to mode."""
    scales = __get_scale(mode)
    if scales is not None:
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
            scale = scales[scale]
            for rcParam, val in rcParamsVal:
                plt.rcParams[rcParam] = scale * val
                # apply all changes to yticks as well
                if rcParam.startswith('xtick'):
                    plt.rcParams['y' + rcParam[1:]] = plt.rcParams[rcParam]


def __set_rc_dpi(ipython, dpi=384):
    """Set rcParams dpi."""
    if ipython is not None and not ipython:
        plt.rcParams['figure.dpi'] = dpi


def __set_ineractive_mode(interactive):
    """Set interative mode."""
    if interactive is not None:
        if interactive:
            plt.ion()
        else:
            plt.ioff()


def __get_scale(mode):
    """Get the scaling factors."""
    if mode == 'default':
        return {'large_scale': 1.,
                'medium_scale': 1.,
                'small_scale': 1.,
                'tick_scale': 1.,
                'fontsize': 10.}
    elif mode == 'print':
        return {'large_scale': 1.5,
                'medium_scale': 1.7,
                'small_scale': 1.7,
                'tick_scale': 1.7,
                'fontsize': 12.}
    elif mode == 'poster':
        return {'large_scale': 4.,
                'medium_scale': 4.,
                'small_scale': 4.,
                'tick_scale': 4.,
                'fontsize': 28.}
    elif mode == 'beamer':
        return {'large_scale': 4.,
                'medium_scale': 4.,
                'small_scale': 4.,
                'tick_scale': 4.,
                'fontsize': 28.}
    else:
        return None


def __reset_style():
    """Restore default matplotlib style."""
    plt.rcdefaults()


def __apply_style(path):
    """Load mplstyle file at given relative path to this file."""
    module_dir = os.path.dirname(__file__)
    path = os.path.join(module_dir, path)

    # load and apply style
    plt.style.use(path)
