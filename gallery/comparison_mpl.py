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

# ~~~ DEFINE DATA ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
np.random.seed(1337)

n = 1000000
x = np.random.standard_normal(n)
y = x + .5 * np.random.standard_normal(n)
hist, xedges, yedges = np.histogram2d(x, y, bins=100, density=True)
hist[hist == 0] = None

t = np.linspace(0, 3 * np.pi, 1000)
style = 'mpl'

# ~~~ PLOT LINEAR ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig, ax = plt.subplots()
plt.plot(t, np.sin(t), t, np.cos(t), t, 2 * np.cos(t))
plt.tight_layout()
plt.savefig(f'gallery/{style}_plot.png')
plt.close()

# legend
fig, ax = plt.subplots()
plt.plot(t, np.sin(t), label='sin')
plt.plot(t, np.cos(t), label='cos')
plt.plot(t, 2 * np.cos(t), label='2cos')
plt.legend(title='function:')
plt.tight_layout()
plt.savefig(f'gallery/{style}_plot_legend.png')
plt.close()

# mulitple subgallery
fig, axs = plt.subplots(3, 1, sharex=True, gridspec_kw={'hspace': 0.000})
axs[0].plot(t, np.sin(t))
axs[1].plot(t[::20], np.cos(t[::20]), 'o-')
axs[2].plot(t, 2 * np.cos(t), t, np.sin(t))
plt.tight_layout()
plt.savefig(f'gallery/{style}_plot_multiple.png')
plt.close()

# ~~~ PLOT IMSHOW ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig, ax = plt.subplots()
plt.imshow(hist)
plt.tight_layout()
plt.savefig(f'gallery/{style}_imshow.png')
plt.close()

# cbar
fig, ax = plt.subplots()
im = plt.imshow(hist)
plt.colorbar(im)
plt.tight_layout()
plt.savefig(f'gallery/{style}_imshow_cbar.png')
plt.close()
