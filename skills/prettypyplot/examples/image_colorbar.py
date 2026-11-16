"""2D histogram shown as image with a colorbar and an annotation."""

import numpy as np
from matplotlib import pyplot as plt

import prettypyplot as pplt

# figratio=1 gives square axes
pplt.use_style(figsize=2.4, figratio=1)

rng = np.random.default_rng(1337)
x = rng.standard_normal(100_000)
y = x + rng.standard_normal(x.size) / 2
hist, xedges, yedges = np.histogram2d(x, y, bins=60, density=True)
hist[hist == 0] = np.nan  # empty bins stay transparent

fig, ax = plt.subplots()
# pplt sets image.origin='lower', so row 0 of the array is at the bottom.
# histogram2d returns hist[x, y], transpose it to get x along the horizontal
im = pplt.imshow(
    hist.T,
    extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    aspect='auto',
    ax=ax,
)
# pass the image, the axes keeps its size
pplt.colorbar(im, label='density $P(x, y)$')

pplt.text(-2.2, 2.6, 'correlated', ax=ax)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')

pplt.savefig('image_colorbar.pdf')
