# -*- coding: utf-8 -*-
# BSD 3-Clause License
# Copyright (c) 2020-2023, Daniel Nagel
# All rights reserved.
"""This module contains utility functions used in multiple submodules."""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt


def is_number(number, *, dtype=float):
    """Check if argument can be interpreated as number.

    Parameters
    ----------
    number : string, float, int
        Variable to be check if it can be casted to float.
    dtype : dtype, optional
        Check for different dtypes, so if is float or if it is int.

    Returns
    -------
    is_number : bool
        Return if argument can be casted to float.

    """
    try:
        float(number)
    except (ValueError, TypeError):
        return False
    return float(number) == dtype(number)


def invert_sign(num):
    """Change sign of number or add/remove leading sign of str."""
    if isinstance(num, (float, int)):
        return -1 * num
    elif isinstance(num, str):
        if num.startswith('-'):
            return num[1:]
        return '-{0}'.format(num)
    raise ValueError(
        'Num needs to be numeric value or string, not ' +
        '{0}.'.format(num),
    )


def parse_axes(*args, ax):
    """Extract axes from ax, args or returns args and current axes."""
    axes = [arg for arg in args if isinstance(arg, mpl.axes.Axes)]
    if axes:
        if isinstance(ax, mpl.axes.Axes) or len(axes) > 1:
            raise ValueError('Multiple axes provided')
        ax = axes[0]
        args = tuple(
            arg for arg in args if not isinstance(arg, mpl.axes.Axes)
        )
    else:
        ax = gca(ax)
    return args, ax


def gca(ax):
    """Return ax if it is axes instance, else the current active axes."""
    if isinstance(ax, mpl.axes.Axes):
        return ax
    return plt.gca()


def get_axes(axs):
    """Return axs if it is all axes instances, else the all current axes."""
    if axs is None:
        return plt.gcf().get_axes()

    axs = np.ravel(axs)
    if not all((isinstance(arg, mpl.axes.Axes) for arg in axs)):
        raise TypeError(
            'If `axs` is given, it needs to be of type matplotlib.axes.Axes.' +
            ' or list of',
        )
    return axs


def is_discrete_cmap(cmap: str) -> bool:
    """Return if cmap is discrete or continuos."""
    return plt.get_cmap(cmap).N < 256
