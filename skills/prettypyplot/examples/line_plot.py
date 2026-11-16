"""Line plot with an uncertainty band and a legend above the axes."""

import numpy as np
from matplotlib import pyplot as plt

import prettypyplot as pplt

# call once before creating figures, figsize is the size of the axes
pplt.use_style(figsize=3)

rng = np.random.default_rng(42)
t = np.linspace(0, 10, 200)
model = np.sin(t)
measured = model + 0.1 * rng.standard_normal(t.size)

fig, ax = plt.subplots()
pplt.plot(t, measured, ax=ax, label='measured')
pplt.plot(t, model, ax=ax, label='model')

# everything without a pplt wrapper is plain matplotlib
ax.fill_between(t, model - 0.2, model + 0.2, color='pplt:gray', alpha=0.2, lw=0)
ax.set_xlabel('time $t$ in s')
ax.set_ylabel('amplitude')

pplt.grid(ax=ax)
pplt.legend(ax=ax, outside='top')

pplt.savefig('line_plot.pdf')
# png is transparent by default, use an opaque background instead
pplt.savefig('line_plot.png', dpi=300, transparent=False)
