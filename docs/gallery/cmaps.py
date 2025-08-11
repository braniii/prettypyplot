"""Generate overview figures of all added colormaps.

This script is taken from the matplotlib documentation
https://matplotlib.org/tutorials/colors/colormaps.html

"""

import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# run setuo
pplt.use_style()

cmaps = {}
cmaps['Perceptually Uniform Sequential'] = [
    'macaw',
    'viridis',
    'bownair',
    'turbo',
    'jet',
]
cmaps['Qualitative'] = [
    'pastel5',
    'pastel6',
    'pastel_autumn',
    'pastel_spring',
    'pastel_rainbow',
    'summertimes',
    'cbf4',
    'cbf5',
    'cbf8',
    'ufcd',
    'paula',
    'argon',
]
cmaps['PaulTol'] = [
    'tol:bright',
    'tol:muted',
    'tol:high_contrast',
    'tol:medium_contrast',
    'tol:vibrant',
]
cmaps['GeoDataViz'] = [
    'gdv:rag',
    'gdv:rag_cvd',
    'gdv:palette',
    'gdv:6a',
    'gdv:5a',
    'gdv:4a',
    'gdv:4b',
    'gdv:3a',
    'gdv:3b',
    'gdv:2a',
    'gdv:2b',
    'gdv:s1',
    'gdv:s2',
    'gdv:s3',
    'gdv:m1',
    'gdv:m2',
    'gdv:m3',
    'gdv:d1',
    'gdv:d2',
    'gdv:d3',
    'gdv:d4',
    'gdv:mars',
    'gdv:moon',
]


gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, cmap_list):
    """Generate colormap plot."""
    fig, axes = plt.subplots(nrows=len(cmap_list), figsize=(2.8, 0.1))
    axes[0].set_title(cmap_category + ' colormaps')

    # for similar absolute width of figures
    fig.text(0, 0.5, r'.', c='w')

    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3] / 2
        # this is needed when LaTeX text engine is used
        # name = name.replace('_', r'\textunderscore{}')
        fig.text(x_text, y_text, name, va='center', ha='right')

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()

    return fig


for cmap_category, cmap_list in cmaps.items():
    fig = plot_color_gradients(cmap_category, cmap_list)
    pplt.savefig(f'images/{cmap_category}.svg')
