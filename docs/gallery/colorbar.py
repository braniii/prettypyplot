"""Show options of colorbar.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import numpy as np
import prettypyplot as pplt
from matplotlib import pyplot as plt


# create random data
np.random.seed(1337)
n = int(1e6)
x = np.random.standard_normal(n)
y = x + np.random.standard_normal(n) / 2
hist, xedges, yedges = np.histogram2d(x, y, bins=100, density=True)
hist[hist == 0] = None

for style in ['default', 'minimal']:
    pplt.use_style(style=style, figsize=(1.6, 1.6))

    # legend
    fig, axs = plt.subplots(1, 2, gridspec_kw={'wspace': 0.3})
    for ax, position in zip (axs, ['top', 'right']):
        im = pplt.imshow(
            hist, extent=[x.min(), x.max(), y.min(), y.max()], ax=ax,
        )

        pplt.colorbar(im, label=r'$P(x,y)$', position=position)
    pplt.savefig(f'images/colorbar_{style}.svg')


# legend preview
pplt.use_style(figsize=(1.4, 1.4))
fig, ax = plt.subplots()
im = pplt.imshow(
    hist, extent=[x.min(), x.max(), y.min(), y.max()], ax=ax,
)

pplt.colorbar(im, label=r'$P(x,y)$', position='right')
pplt.savefig(f'images/colorbar_preview.svg')
