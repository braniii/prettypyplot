"""Shades per category and readable labels on a heatmap."""

import numpy as np
from matplotlib import pyplot as plt

import prettypyplot as pplt

pplt.use_style(figsize=2.4)

# 3 groups with 3 shades each, row i holds the shades of group i
shades = pplt.categorical_cmap(3, 3, return_colors=True)

fig, ax = plt.subplots()
x = np.linspace(0, 1, 50)
for group, group_shades in enumerate(shades):
    for exponent, color in enumerate(group_shades, start=1):
        pplt.plot(
            x,
            x**exponent + group,
            ax=ax,
            color=color,
            label=f'group {group + 1}' if exponent == 1 else None,
        )
ax.set_xlabel('$x$')
ax.set_ylabel('$x^n$ + offset')
pplt.legend(ax=ax, outside='top')

# pplt.savefig acts on the current figure, so save before creating the next
pplt.savefig('categorical_shades.pdf')

# heatmap of a matrix, figsize of plt.subplots overrides the style default
fig, ax = plt.subplots(figsize=(1.6, 1.6))
data = np.arange(16).reshape(4, 4)
# origin='upper' shows row 0 at the top, pplt defaults to 'lower'
im = pplt.imshow(data, ax=ax, origin='upper')
for (row, col), value in np.ndenumerate(data):
    background = im.cmap(im.norm(value))
    pplt.text(col, row, str(value), ax=ax, color=pplt.text_color(background))
ax.grid(False)
ax.set_xticks(range(4))
ax.set_yticks(range(4))

pplt.savefig('categorical_heatmap.pdf')
