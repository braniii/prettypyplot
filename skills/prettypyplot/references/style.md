# Style guide

How to choose size, mode, style and colors, and how to write text that works
with and without LaTeX. Read [../SKILL.md](../SKILL.md) first.

## Size

`figsize` in `pplt.use_style` (or `plt.subplots(figsize=...)`) is the size of
the axes when saving with `pplt.savefig`. The saved figure is larger by the
space needed for tick labels, axis labels, legends and colorbars, typically
0.5 to 1 inch per side with labels.

| Target | Setup |
| --- | --- |
| paper, single column | `use_style(figsize=2.6)`, about 3.3 inches wide with labels |
| paper, full width | `use_style(figsize=6)`, about 6.8 inches wide with labels |
| one panel of a subplot grid | `use_style(figsize=1.2)` to `figsize=2`, plus `gridspec_kw` spacing |
| square axes, e.g. images | `use_style(figsize=2.4, figratio=1)` |
| slides | `use_style(mode='beamer', style='minimal', figsize=8)` |
| posters | `use_style(mode='poster', style='minimal', figsize=8)` |
| Jupyter | add `ipython=True` |

`figratio` is the width to height ratio of the axes: `'golden'` (default,
1.618), `'sqrt(2)'`, `'sqrt(3)'` or any number. It only applies when
`figsize` is a single number, a tuple `(width, height)` sets both directly.

### Exact figure size

When the whole figure must have an exact size, e.g. a required column width,
give the size of the figure and switch off both the canvas sizing and the
tight bounding box:

```python
import numpy as np
from matplotlib import pyplot as plt

import prettypyplot as pplt

pplt.use_style()
plt.rcParams['savefig.bbox'] = 'standard'  # don't crop to the content

fig, ax = plt.subplots(figsize=(3.3, 2.2))  # size of the whole figure
pplt.plot(np.arange(10), np.arange(10) ** 2, ax=ax)
ax.set_xlabel('$n$')
ax.set_ylabel('$n^2$')
pplt.savefig('exact_size.pdf', use_canvas_size=False)
```

## Mode

| Mode | Font size | Lines | Use |
| --- | --- | --- | --- |
| `'default'` | 10 pt | 1x | screen, papers |
| `'print'` | 12 pt | 1.5x to 1.7x | printed documents |
| `'beamer'` | 28 pt | 4x | slides |
| `'poster'` | 28 pt | 4x | A0 posters |

In `'beamer'` and `'poster'` mode `pplt.savefig` lays out the figure at three
times the size. With a small `figsize` the large fonts overlap the data, so use
about 6 to 10 inches.

## Style

- `'default'`: dashed grid, all four spines, legends with a thin frame. Good
  for papers.
- `'minimal'`: no grid, no top and right spines, spines limited to the data
  range (only with `pplt.plot`), fewer ticks (only with `pplt.savefig`),
  legends without frame. Good for slides and posters.
- `'none'`: matplotlib defaults, only the pplt colormaps and colors are
  registered.

`true_black=True` uses black instead of dark gray for text, spines and ticks.

## Colors

### Color cycle

`use_style(colors=name)` sets the color cycle of lines, bars and scatter
points. A discrete colormap is used as it is, so it limits the number of
distinct colors. A continuous colormap is sampled at `ncs` points (default 10).

- Default: `'pastel5'` with 5 colors.
- Color-blind friendly: `'pastel5'`, `'pastel6'`, `'cbf4'`, `'cbf5'`,
  `'cbf8'`, and Paul Tol's palettes `'tol:bright'`, `'tol:vibrant'`,
  `'tol:muted'`, `'tol:light'`, `'tol:high_contrast'`,
  `'tol:medium_contrast'`.
- More series than colors: pick a palette with enough colors
  (`python -m prettypyplot api colormaps` lists the number), or a continuous
  map, e.g. `use_style(colors='macaw', ncs=12)`.

Explicit colors: `'C0'`, `'C1'`, ... refer to the active cycle, and the named
colors `'pplt:blue'`, `'pplt:red'`, `'pplt:green'`, `'pplt:orange'`,
`'pplt:lightblue'`, `'pplt:gray'`, `'pplt:lightgray'` are always available.
`'pplt:axes'`, `'pplt:text'` and `'pplt:grid'` follow the current style.

### Groups of related series

`pplt.categorical_cmap(nc, nsc)` returns a `ListedColormap` with `nc` colors
and `nsc` shades of each, taken from the active color cycle or `cmap=`. With
`return_colors=True` it returns an array of shape `(nc, nsc, 3)`.

```python
shades = pplt.categorical_cmap(2, 3, return_colors=True)
fig, ax = plt.subplots()
for group, group_shades in enumerate(shades):
    for idx, color in enumerate(group_shades):
        pplt.plot([0, 1], [group, group + idx], ax=ax, color=color)
pplt.savefig('shades.pdf')
```

`pplt.categorical_color(nsc, color)` returns the shades of a single color.

### Colormaps

Continuous colormaps from prettypyplot: `'macaw'` (default for images),
`'bownair'`, `'paula2'`, `'turbo'`. All colormaps also exist reversed as
`'<name>_r'`, and all matplotlib colormaps work as usual. Set the default with
`use_style(cmap=name)` or pass `cmap=` to `pplt.imshow`.

## LaTeX

With `latex=True` (default) and a `latex` executable on the PATH, all text is
rendered by LaTeX with the Latin Modern font and `amsmath` loaded. Without
LaTeX, matplotlib's mathtext renders `$...$` and the rest is plain text.
`sf=True` switches to a sans-serif font.

Text that is valid in both modes:

- plain words, numbers, `-`, `+`, `=`, `(`, `)`, `:`, `/`, `,`, `.`
- math in raw strings: `r'$\alpha$'`, `r'$x^2$'`, `r'$10^{-3}$'`,
  `r'$\mathrm{d}x$'`

Text from data or user input can contain characters that LaTeX treats
specially. Escape them only when LaTeX is active:

```python
TEX_ESCAPES = {
    '\\': r'\textbackslash{}',
    '%': r'\%',
    '&': r'\&',
    '#': r'\#',
    '$': r'\$',
    '_': r'\_',
    '^': r'\textasciicircum{}',
    '~': r'\textasciitilde{}',
    '{': r'\{',
    '}': r'\}',
}


def tex_safe(text):
    """Escape LaTeX special characters if LaTeX rendering is active."""
    if not plt.rcParams['text.usetex']:
        return text
    return ''.join(TEX_ESCAPES.get(char, char) for char in text)


pplt.use_style()
fig, ax = plt.subplots()
pplt.plot([0, 1], [0, 1], ax=ax)
ax.set_xlabel(tex_safe('growth_rate in % (R&D #2)'))
pplt.savefig('escaped.pdf')
```

Alternatively use `pplt.use_style(latex=False)`, then no escaping is needed and
the output is the same on every machine.

Known issue: with matplotlib 3.11.0 and LaTeX active, text with an outline
(`contour=True` or `pplt.add_contour`) raises `TypeError: ...
_draw_text_as_path() missing 1 required positional argument: 'mtext'`. Fixed in
matplotlib 3.11.1.
