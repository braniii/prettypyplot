"""Generate overview figures of all added colormaps.

This script is taken from the matplotlib documentation
https://matplotlib.org/tutorials/colors/colormaps.html

"""
import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# run setuo
pplt.use_style()
plt.rcParams['figure.dpi'] = 600

cmaps = {}
cmaps['Perceptually Uniform Sequential'] = ['macaw', 'viridis', 'bownair',
                                            'turbo', 'jet']
cmaps['Qualitative'] = ['pastel5', 'pastel6', 'pastel_autunm', 'pastel_spring',
                        'pastel_rainbow', 'cbf4', 'cbf5', 'cbf8', 'ufcd']

gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, cmap_list):
    """Generate colormap plot."""
    fig, axes = plt.subplots(nrows=len(cmap_list), figsize=(3.2, 0.15))
    axes[0].set_title(cmap_category + ' colormaps')

    # for similar absolute width of figures
    fig.text(0, .5, r'.', c='w')

    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.01
        y_text = pos[1] + pos[3] / 2
        name = name.replace('_', r'\textunderscore{}')
        fig.text(x_text, y_text, name, va='center', ha='right')

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()

    return fig


for cmap_category, cmap_list in cmaps.items():
    fig = plot_color_gradients(cmap_category, cmap_list)
    pplt.savefig(f'gallery/cmaps/{cmap_category}.png')
