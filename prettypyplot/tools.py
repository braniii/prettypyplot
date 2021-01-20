"""Helper functions.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt


def parse_figratio(figratio):
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
    if is_number(figratio):
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
                '{0}].'.format(', '.join(figratios.keys)),
            )
        figratio = figratios.get(figratio, None)
    return figratio


def parse_figsize(figsize, figratio):
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
    if isinstance(figsize, (list, tuple, np.ndarray)):
        if len(figsize) == 1:
            sizetuple = figsize[0]
        elif len(figsize) >= 2:
            sizetuple = None

    if is_number(figsize):
        # check figratio
        figratio = parse_figratio(figratio)
        sizetuple = (float(figsize), float(figsize) / figratio)
    else:
        sizetuple = None

    if sizetuple is None:
        raise ValueError(
            'figsize needs to be an numeric value or a tuple, not ' +
            '{0}.'.format(figsize),
        )
    return sizetuple


def is_number(number):
    """Check if argument can be interpreated as number.

    Parameters
    ----------
    number : string, float, int
        Variable to be check if it can be casted to float.

    Returns
    -------
    is_number : bool
        Return if argument can be casted to float.

    """
    try:
        float(number)
    except (ValueError, TypeError):
        return False
    return True


def invert_sign(num):
    """Change sign of number or add/remove leading sign of str."""
    if is_number(num):
        return -1 * num
    elif isinstance(num, str):
        if num.startswith('-'):
            return num[1:]
        return '-{0}'.format(num)


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
