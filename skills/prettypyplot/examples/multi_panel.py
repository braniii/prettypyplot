"""Grid of subplots with shared axes and one legend for all panels."""

import numpy as np
from matplotlib import pyplot as plt

import prettypyplot as pplt

# for a grid of subplots, figsize is the size of a single panel
pplt.use_style(figsize=1.6)

t = np.linspace(0, 2 * np.pi, 200)
frequencies = [1, 2, 3]

# set the spacing with gridspec_kw, fig.subplots_adjust() has no effect
fig, axs = plt.subplots(
    2,
    2,
    sharex=True,
    sharey=True,
    gridspec_kw={'wspace': 0.1, 'hspace': 0.1},
)
for ax, freq in zip(axs.flat, frequencies):
    pplt.plot(t, np.sin(freq * t), ax=ax, label='sine')
    pplt.plot(t, np.cos(freq * t), ax=ax, label='cosine')
    ax.set_xlabel('phase')
    ax.set_ylabel('amplitude')

# hide the unused fourth panel, then keep tick labels and axis labels only
# on the outer panels
pplt.hide_empty_axes(axs)
pplt.label_outer(axs)

# one legend spanning all panels, entries repeated per panel are merged
pplt.legend(axs=axs, outside='top')

pplt.savefig('multi_panel.pdf')
