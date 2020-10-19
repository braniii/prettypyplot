"""
Show options of legend.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt
import numpy as np

import prettypyplot as pplt

# ~~~ DEFINE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
np.random.seed(1337)
N = 500
t = np.linspace(0, 3 * np.pi, N)
x1, x2, x3 = [np.sin(t + np.pi * np.random.rand()) + 0.1 * np.random.rand(N)
              for _ in range(3)]

for style in ['default', 'minimal']:
    for mode in ['default', 'print', 'beamer']:
        pplt.use_style(style=style, mode=mode, figsize=2)

        fig, axs = plt.subplots(2, 3,
                                gridspec_kw={'hspace': 0.4, 'wspace': 0.6})

        # legend
        for i, outside in enumerate(['top', 'bottom', 'left', 'right', False]):
            ax = axs.flatten()[i]
            pplt.plot(t, x1, ax=ax, label='$x_1$')
            pplt.plot(t, x2, ax=ax, label='$x_2$')
            pplt.plot(t, x3, ax=ax, label='$x_3$')

            pplt.legend(title='function:', ax=ax, outside=outside)

        # disable unused axis
        axs[-1, -1].axis('off')

        pplt.savefig(f'gallery/legend/{style}_{mode}_plot_legend.png')
        plt.close()
