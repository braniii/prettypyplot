"""Show options of legend.

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
X1, X2, X3 = [
    np.sin(T + np.pi * np.random.rand()) + 0.1 * np.random.rand(N)
    for _ in range(3)
]

for style in ['default', 'minimal']:
    for mode in ['default', 'print', 'beamer']:
        pplt.use_style(style=style, mode=mode, figsize=2)

        fig, axs = plt.subplots(
            3, 1, gridspec_kw={'hspace': 0.4},
        )

        # legend
        for i, outside in enumerate(['top', 'right', False]):
            ax = axs.flatten()[i]
            pplt.plot(T, X1, ax=ax, label='$x_1$')
            pplt.plot(T, X2, ax=ax, label='$x_2$')
            pplt.plot(T, X3, ax=ax, label='$x_3$')

            pplt.legend(title='function:', ax=ax, outside=outside)

        pplt.savefig(f'gallery/legend/{style}_{mode}_plot_legend.png')
        plt.close()
