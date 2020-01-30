"""
Show options of colorbar.

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

n = 1000000
x = np.random.standard_normal(n)
y = x + .5 * np.random.standard_normal(n)
hist, xedges, yedges = np.histogram2d(x, y, bins=100, density=True)
hist[hist == 0] = None

for style in ['default', 'minimal']:
    pplt.setup_pyplot(style=style)

    # legend
    for position in ['top', 'bottom', 'left', 'right']:
        fig, ax = plt.subplots()
        im = pplt.imshow(hist, extent=[x.min(), x.max(), y.min(), y.max()])

        pplt.colorbar(im, label=r'$P(x,y)$', position=position)
        pplt.savefig(f'gallery/colorbar/{style}_plot_colorbar_{position}.png')
        plt.close()
