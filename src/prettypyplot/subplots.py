# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2020-2023, Daniel Nagel
# All rights reserved.
"""Wrapper for matplotlib functions for subplots."""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as mpl  # mpl = dm.tryImport('matplotlib')
import numpy as np
from matplotlib import pyplot as plt

from prettypyplot import tools


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def hide_empty_axes(axs=None):
    """Hide empty axes.

    Loop over all axes and hide empty ones.

    Parameters
    ----------
    axs : mpl.axes.Axes or list of
        Specify [matplotlib.axes.Axes][] to check for empty state. Default use
        all of current figure.

    """
    # check for single axes
    axs = tools.get_axes(axs)

    # loop over all axes and hide empty ones
    for ax in axs:
        if _is_empty_axes(ax):
            ax.axis('off')

    # in case of shared axes, activate outer tick labels
    _activate_outer_ticks(axs)


def _activate_outer_ticks(axs):
    """Activate ticks of outer axes."""
    for ax in axs:
        left_empty, bottom_empty = _is_outer_hidden(axs, ax)
        if left_empty:
            ax.tick_params(axis='y', reset=True)
        if bottom_empty:
            ax.tick_params(axis='x', reset=True)


def label_outer(axs=None):
    """Only show outer labels and tick labels.

    This checks for outest visible axes only. Works only with single Gridspec.

    Parameters
    ----------
    axs : mpl.axes.AxesSubplot or list of
        Specify [matplotlib.axes.Axes][] to check for labeling only outer.
        Default use all of current figure.

    """
    # check for single axes
    if axs is not None:
        axs = tools.get_axes(axs)
        if not all((_is_subplot_axes(arg) for arg in axs)):
            raise TypeError(
                'axs needs to be of type matplotlib.axes.AxesSuplot.',
            )
    else:
        axs = [ax for ax in plt.gcf().get_axes() if _is_subplot_axes(ax)]

    for ax in axs:
        ss = ax.get_subplotspec()
        if hasattr(ss, 'is_last_row'):  # pragma: no cover # noqa: WPS421
            # for mpl >= 3.4
            lastrow = ss.is_last_row()
            firstcol = ss.is_first_col()
        elif hasattr(ax, 'is_last_row'):  # pragma: no cover # noqa: WPS421
            lastrow = ax.is_last_row()
            firstcol = ax.is_first_col()
        else:
            raise TypeError(f'{ax!r} is not a valid axes.')

        # check if axes below, left is hidden
        left_empty, bottom_empty = _is_outer_hidden(axs, ax)
        _label_outer(ax, lastrow or bottom_empty, firstcol or left_empty)


def _is_subplot_axes(ax):
    """Check is is subplot axes."""
    return (
        isinstance(ax, mpl.axes.Axes) and
        hasattr(ax, 'get_subplotspec')  # noqa: WPS421
    )


def _is_outer_hidden(axs, ax):
    """Check if lefter/lower axes is empty."""
    left_hidden, bottom_hidden = False, False
    for axes in np.ravel(axs):
        if _is_left_neighbor(axes, ax):
            left_hidden = left_hidden or not axes.axison
        elif _is_bottom_neighbor(axes, ax):
            bottom_hidden = bottom_hidden or not axes.axison
    return left_hidden, bottom_hidden


def _is_left_neighbor(ax1, ax2):
    """Check if ax1 is left ax2."""
    return _has_neighbor_distance(ax1, ax2, col_offset=1)


def _is_bottom_neighbor(ax1, ax2):
    """Check if ax1 is below ax2."""
    return _has_neighbor_distance(ax1, ax2, row_offset=-1)


def _has_neighbor_distance(ax1, ax2, row_offset=0, col_offset=0):
    """Check if two SubpotAxes have the given offset distance."""
    if not _is_subplot_axes(ax1) or not _is_subplot_axes(ax2):
        return False

    ss1, ss2 = ax1.get_subplotspec(), ax2.get_subplotspec()
    return (
        any((
            row + row_offset in list(ss2.rowspan) for row in list(ss1.rowspan)
        )) and any((
            col + col_offset in list(ss2.colspan) for col in list(ss1.colspan)
        ))
    )


def _label_outer(ax, lastrow, firstcol):
    """See mpl.axes.Axes.label_outer()."""
    if not lastrow:
        for xlabel in ax.get_xticklabels(which='both'):
            xlabel.set_visible(False)
        ax.xaxis.get_offset_text().set_visible(False)
        ax.set_xlabel('')
    if not firstcol:
        for ylabel in ax.get_yticklabels(which='both'):
            ylabel.set_visible(False)
        ax.yaxis.get_offset_text().set_visible(False)
        ax.set_ylabel('')


def _is_empty_axes(ax):
    """Return if axes is empty."""
    return (
        not any([
            ax.lines, ax.collections, ax.patches, ax.texts, ax.images,
        ])
    )


def subplot_labels(*, fig=None, xlabel=None, ylabel=None):
    """Add global labels for subplots.

    This method adds shared x- and y-labels for a grid of subplots. These can
    be created by, e.g. `fig, axs = plt.subplots(...)`.

    Parameters
    ----------
    fig : matplotlib figure, optional
        If `None` the current figure will be used instead.
    xlabel : str, optional
        String of x label.
    ylabel : str, optional
        String of y label.

    """
    # if no label passed, nothing to do
    if xlabel is None and ylabel is None:
        return

    # get active axes to restore it later on
    ca = plt.gca()

    if fig is None:
        fig = plt.gcf()

    _subplot_labels(fig, xlabel, ylabel)

    # reset current axes
    plt.sca(ca)


def _subplot_labels(fig, xlabel, ylabel):
    """Add global labels for subplots."""
    # add subplot spanning the complete figure
    ax = fig.add_subplot(111, frameon=False)  # noqa: WPS432

    # hide axes
    ax.tick_params(
        labelcolor='none',
        color='none',
        grid_alpha=0,
        which='both',
        top=False,
        bottom=False,
        left=False,
        right=False,
    )
    # remove ticks to get no artificial padding
    ax.set_yticks([])
    # TODO: align_labels seems not to work for xlabels, hence it can not be
    # removed
    ax.set_xticks([0])
    # remove ticks
    ax.xaxis.set_ticks_position('none')

    ax.grid(False)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    fig.align_labels()
