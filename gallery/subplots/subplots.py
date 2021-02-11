"""Show options of subplots module.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# ~~~ DEFINE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
np.random.seed(1337)
N = 500
T = np.linspace(0, 3 * np.pi, N)

pplt.use_style(figsize=.8)

for nfigs in (8, 9):
    xs = [
        np.sin(T + np.pi * np.random.rand()) + 0.1 * np.random.rand(N)
        for _ in range(nfigs)
    ]

    fig, axs = plt.subplots(
        3,
        3,
        sharex=True,
        sharey=True,
        gridspec_kw={'hspace': 0, 'wspace': 0},
    )

    for idx, (ax, x) in enumerate(zip(axs.flatten(), xs)):
        pplt.plot(T, xs[0], ax=ax)
        ax.grid(False)

    pplt.hide_empty_axes()
    pplt.label_outer()

    pplt.subplot_labels(xlabel=r'$x$', ylabel=r'sinus $f(x)$')

    pplt.savefig(f'gallery/subplots/subplots_{nfigs}figs.png')
    plt.close()
