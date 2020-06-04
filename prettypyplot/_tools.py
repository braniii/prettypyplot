"""
Helper functions.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def _parse_figratio(figratio):
    """Parse the figratio value."""
    if _is_number(figratio):
        figratio = float(figratio)
    elif figratio == 'sqrt(2)':
        figratio = np.sqrt(2)
    elif figratio == 'golden':
        figratio = (1 + np.sqrt(5)) / 2
    elif figratio == 'sqrt(3)':
        figratio = np.sqrt(3)
    return figratio


def _parse_figsize(figsize, figratio):
    """Parse the figsize value."""
    if isinstance(figsize, (list, tuple, np.ndarray)):
        if len(figsize) == 1:
            figsize = (float(figsize[0]), float(figsize[0]) / figratio)
        elif len(figsize) == 2:
            pass
    elif _is_number(figsize) and _is_number(figratio):
        figsize = (float(figsize), float(figsize) / figratio)
    else:
        figsize = None
    return figsize


def _is_number(val):
    """
    Check if argument can be interpreated as number.

    Parameters
    ----------
    val : string, float, int
        Variable to be check if it can be casted to float.

    Returns
    -------
    is_number : bool
        Return if argument can be casted to float.

    """
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False


def _invert_sign(num):
    """Change sign of number or add/remove leading sign of str."""
    if _is_number(num):
        return -1 * num
    elif type(num) == str:
        if num[0] == '-':
            return num[1:]
        else:
            return '-' + num


def _parse_axes(*args, ax):
    """Extract axes from ax, args or returns args and current axes."""
    if any((isinstance(arg, mpl.axes.Axes) for arg in args)):
        if isinstance(ax, mpl.axes.Axes):
            raise ValueError('Multiple axes provided')
        ax = [arg for arg in args if isinstance(arg, mpl.axes.Axes)][0]
        args = tuple(arg for arg in args if not isinstance(arg, mpl.axes.Axes))
    else:
        ax = _gca(ax)
    return args, ax


def _gca(ax):
    """Return ax if axes, else pyplot.gca()."""
    if isinstance(ax, mpl.axes.Axes):
        return ax
    else:
        return plt.gca()
