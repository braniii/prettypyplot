"""Create Matplotlib inspired logo.

This script is taken from
https://matplotlib.org/gallery/misc/logos2.html#sphx-glr-gallery-misc-logos2-py
an heavily simplified to fit the spirit of prettypyplot.

"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

import prettypyplot as pplt


def create_icon_axes(fig):
    """
    Create a polar axes containing the radar plot.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to draw into.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The created Axes.
    """
    ax = fig.add_axes((0, 0, 1, 1), projection='polar')

    N = 7
    arc = 2. * np.pi
    theta = np.arange(0.0, arc, arc / N)
    radii = np.array([3, 6, 8, 7, 4, 5, 8])
    bars = ax.bar(theta, radii, width=arc / N, bottom=0.0, align='edge',
                  edgecolor=plt.rcParams['text.color'])
    for r, bar in zip(radii, bars):
        val = (r - radii.min()) / (radii.max() - radii.min())
        color = plt.get_cmap('macaw')(val)
        bar.set_facecolor(color)

    ax.tick_params(labelbottom=False, labeltop=False,
                   labelleft=False, labelright=False)
    ax.set_rmax(9.5)

    # the actual visible background - extends a bit beyond the axis
    ax.add_patch(Rectangle((0, 0), arc, 10.5,
                           facecolor='white', zorder=0,
                           clip_on=False, in_layout=False))
    return ax


def make_logo(height_px):
    """
    Create a figure with the prettypyplot logo.

    Parameters
    ----------
    height_px : int
        Height of the figure in pixel.

    """
    dpi = plt.rcParams['figure.dpi']
    height = height_px / dpi
    figsize = (height, height)
    fig = plt.figure(figsize=figsize)

    ax = create_icon_axes(fig)

    return fig, ax


pplt.setup_pyplot()

fig, ax = make_logo(height_px=120)

pplt.savefig('gallery/logo.png')
