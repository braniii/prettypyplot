"""Show options of legend."""

import numpy as np
import prettypyplot as pplt
from matplotlib import pyplot as plt

# define random data to plot
np.random.seed(1337)
N = 500
T = np.linspace(0, 3 * np.pi, N)
X1, X2 = [
    np.sin(T + np.pi * np.random.rand()) + 0.1 * np.random.rand(N) for _ in range(2)
]

# loop over  random data to plot
for style in ['default', 'minimal']:
    pplt.use_style(style=style, figsize=1.2)

    fig, axs = plt.subplots(1, 3, gridspec_kw={'wspace': 0.25})

    # legend
    for i, outside in enumerate(['top', False, 'right']):
        ax = axs.flatten()[i]
        pplt.plot(T, X1, ax=ax, label='$x_1$')
        pplt.plot(T, X2, ax=ax, label='$x_2$')

        pplt.legend(title='title', ax=ax, outside=outside)

    pplt.savefig(f'images/legend_{style}.svg')


# generate thumbnail
pplt.use_style(figsize=1.4)
fig, ax = plt.subplots()

# legend
pplt.plot(T, X1, ax=ax, label='$x_1$')
pplt.plot(T, X2, ax=ax, label='$x_2$')
pplt.legend(title='title', ax=ax, outside='top')
pplt.savefig(f'images/legend_preview.svg')
