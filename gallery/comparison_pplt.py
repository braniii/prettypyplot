"""
Show difference between pyplot and prettypyplot.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# ~~~ DEFINE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
np.random.seed(1337)

n = 1000000
x = np.random.standard_normal(n)
y = x + .5 * np.random.standard_normal(n)
hist, xedges, yedges = np.histogram2d(x, y, bins=100, density=True)
hist[hist == 0] = None

t = np.linspace(0, 3 * np.pi, 1000)

for style in ['default', 'minimal']:
    pplt.use_style(style=style)

    # ~~~ PLOT LINEAR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    fig, ax = plt.subplots()
    pplt.plot(t, np.sin(t), t, np.cos(t), t, 2 * np.cos(t))
    pplt.savefig(f'gallery/{style}_plot.png')
    plt.close()

    # legend
    fig, ax = plt.subplots()
    pplt.plot(t, np.sin(t), label='sin')
    pplt.plot(t, np.cos(t), label='cos')
    pplt.plot(t, 2 * np.cos(t), label='2cos')
    pplt.legend(title='function:')
    pplt.savefig(f'gallery/{style}_plot_legend.png')
    plt.close()

    # legend outside
    for outside in ['top', 'bottom', 'left', 'right']:
        fig, ax = plt.subplots()
        pplt.plot(t, np.sin(t), label='sin')
        pplt.plot(t, np.cos(t), label='cos')
        pplt.plot(t, 2 * np.cos(t), label='2cos')

        pplt.legend(title='function:', outside=outside)
        pplt.savefig(f'gallery/{style}_plot_legend_{outside}.png')
        plt.close()

    # mulitple subgallery
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(3, 1),
                            gridspec_kw={'hspace': 0.000})
    pplt.plot(axs[0], t, np.sin(t), 'C0', label='sin t')
    pplt.plot(axs[1], t[::20], np.cos(t[::20]), 'C1o-', label='cos t')
    pplt.plot(axs[2], t, np.cos(2 * t), 'C2', label='cos 2t')
    pplt.legend(title='function:', ax=axs[0], axs=axs, outside='top')
    pplt.savefig(f'gallery/{style}_plot_multiple.png')
    plt.close()

    # ~~~ PLOT IMSHOW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    fig, ax = plt.subplots()
    pplt.imshow(hist)
    pplt.savefig(f'gallery/{style}_imshow.png')
    plt.close()

    # cbar
    fig, ax = plt.subplots()
    im = pplt.imshow(hist)
    pplt.colorbar(im)
    pplt.savefig(f'gallery/{style}_imshow_cbar.png')
    plt.close()
