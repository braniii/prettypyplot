---
name: prettypyplot
description: Write, fix and review matplotlib figures that use prettypyplot (`import prettypyplot as pplt`). Use whenever code imports prettypyplot or calls `pplt.*`, or the user asks for figures in prettypyplot style. Covers `use_style` setup, the `ax=` calling convention, legends outside the axes, colorbars, figure sizing with `pplt.savefig`, LaTeX text, colormaps and common pitfalls.
license: BSD-3-Clause
---

# prettypyplot

prettypyplot is a thin layer over matplotlib:

1. `pplt.use_style()` sets rcParams (fonts, line widths, colors, grid, spines)
   and registers extra colormaps and named colors.
2. A few wrappers add what matplotlib lacks, e.g. legends outside the axes or
   colorbars that keep the height of the axes.
3. `pplt.savefig` and `pplt.show` resize the figure so that `figsize` is the
   size of the axes, not of the whole figure.

Everything else is plain matplotlib: create figures with `plt.subplots`, set
labels with `ax.set_xlabel`, call `ax.scatter`, `ax.bar`, `ax.fill_between`,
`ax.hist` directly. Don't invent `pplt` functions, the complete list is below.

Written for prettypyplot 0.13. Until 1.0 the API may change in any minor
release, so check the reference of the installed version (see
[Functions](#functions)) if something does not match.

## Minimal example

```python
import numpy as np
from matplotlib import pyplot as plt

import prettypyplot as pplt

pplt.use_style(figsize=2.4)  # once, before creating any figure

x = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots()
pplt.plot(x, np.sin(x), ax=ax, label='sine')
pplt.plot(x, np.cos(x), ax=ax, label='cosine')
ax.set_xlabel('time $t$')
ax.set_ylabel('signal')
pplt.legend(ax=ax, outside='top')

pplt.savefig('signal.pdf')
```

## Rules

1. **Call `pplt.use_style()` once before creating figures.** It first resets
   all rcParams to the matplotlib defaults, so put your own
   `plt.rcParams[...]` changes after it. `pplt.update_style(...)` changes
   single options without the reset. Both only affect figures created
   afterwards.
2. **Pass the axes to the wrapper.** Write `pplt.plot(x, y, ax=ax)`, not
   `ax.plot(x, y)`, to get the style-specific behavior. `pplt.plot(ax, x, y)`
   works too, and without an axes the current one (`plt.gca()`) is used.
   `pplt.plot(ax=ax, x, y)` is a SyntaxError, keyword arguments go last.
3. **Save with `pplt.savefig(...)` and show with `pplt.show()`**, not with
   `fig.savefig`, `plt.savefig` or `plt.show`. Only the pplt versions apply the
   canvas sizing, the beamer/poster scaling and the tick reduction of the
   minimal style. Both act on the *current* figure (`plt.gcf()`), so save each
   figure before creating the next one, or activate it first with
   `plt.figure(fig.number)`.
4. **`figsize` is the size of the axes** (the canvas). `pplt.savefig` calls
   `fig.tight_layout()` and then grows the figure until the first axes (or
   `reference_ax`) has exactly `figsize`. Labels, ticks, legends and colorbars
   are added around it. A single number sets the width and the height follows
   from `figratio` (golden ratio by default): `use_style(figsize=3)` gives axes
   of 3 x 1.85 inches. `plt.subplots(figsize=(w, h))` overrides it per figure.
   - **Subplots:** `figsize` becomes the size of a single panel, and the gaps
     between panels are scaled up as well. A 1x3 row with default spacing ends
     up about 16 inches wide. Always set the spacing explicitly,
     `plt.subplots(1, 3, gridspec_kw={'wspace': 0.3})`, and use a small
     per-panel `figsize`.
   - `fig.subplots_adjust(...)` has no effect, because `pplt.savefig` runs
     `tight_layout`. Use `gridspec_kw={'wspace': ..., 'hspace': ...}`. Don't
     use `layout='constrained'` or call `tight_layout` yourself.
   - For an exact size of the whole figure, see
     [references/style.md](references/style.md#exact-figure-size).
5. **LaTeX depends on the machine.** `use_style()` defaults to `latex=True`,
   which enables `text.usetex` only if a `latex` executable is on the PATH. In
   that case `%` silently drops the rest of the string (`'50%'` renders as
   `50`), and `&`, `#`, `^` or a single `$` raise `RuntimeError: latex was not
   able to process the following string`. With LaTeX inactive, escaped strings
   like `r'50\%'` show the backslash. Therefore:
   - Use `pplt.use_style(latex=False)` when labels come from data or user
     input, or when the output must look the same on every machine.
   - Math in raw strings, `r'$\alpha_1$'`, works in both modes.
   - `plt.rcParams['text.usetex']` tells you which mode is active. A helper
     that escapes only when needed is in
     [references/style.md](references/style.md#latex).
6. **Jupyter:** `use_style()` sets `figure.dpi = 384`, which makes inline
   figures huge. Use `pplt.use_style(ipython=True)` in notebooks.

## Defaults that differ from matplotlib

After `use_style()`:

- `image.origin = 'lower'`: `imshow` puts row 0 of the array at the bottom.
  Pass `origin='upper'` for photos and matrices that should read top-down.
- `savefig.transparent = True`: PNGs get a transparent background. Pass
  `transparent=False` for an opaque white one.
- `savefig.format = 'pdf'`: a file name without extension is saved as PDF.
  PNG resolution is `figure.dpi` (384, or 100 with `ipython=True`) unless you
  pass `dpi=`.
- `savefig.bbox = 'tight'` and `hist.bins = 50`.
- The color cycle is `pastel5`, which has **only 5 colors**: the sixth line
  reuses the first color. For more series use e.g. `use_style(colors='cbf8')`
  or a continuous colormap with `ncs=n`.
- The default colormap is `macaw`.

## Styles and modes

- `style='default'`: dashed grid, all four spines. `style='minimal'`: no
  grid, no top and right spines, spines limited to the data range by
  `pplt.plot`, fewer ticks, legends without frame. `style='none'`: plain
  matplotlib defaults.
- `mode='default'` (10 pt), `'print'` (12 pt, thicker lines), `'beamer'` and
  `'poster'` (28 pt, 4x line widths). Beamer and poster need a large
  `figsize`, about 6 to 10 inches.
- To switch style or mode, call `pplt.use_style(...)` again before creating
  the next figure.

## Functions

All functions live at the top level of `pplt`.

| Function | What it adds over matplotlib |
| --- | --- |
| `use_style(...)`, `update_style(...)` | set up rcParams, colormaps and colors |
| `plot(*args, ax=None, **kwargs)` | minimal style: spines limited to the data range |
| `imshow(*args, ax=None, **kwargs)` | `zorder=1`, so the image covers the grid (with `ax.imshow` the grid is drawn on top) |
| `legend(*args, outside=False, ax=None, axs=None, deduplicate=True, **kwargs)` | legend outside the axes, one legend for several axes, merged duplicates |
| `colorbar(im, width='7%', pad='0%', position='right', label=None, **kwargs)` | colorbar with the height of the axes, the axes keeps its size |
| `grid(*args, ax=None, **kwargs)` | style default: dashed major and dotted minor grid, style minimal: no grid |
| `savefig(fname, reference_ax=None, use_canvas_size=True, **kwargs)` | canvas sizing, see rule 4 |
| `show(reference_ax=None, use_canvas_size=True, **kwargs)` | same sizing as `savefig` |
| `text(x, y, s, *, contour=None, ax=None, **kwargs)`, `figtext(...)` | centered alignment by default, optional outline with `contour=True` |
| `add_contour(txt, contourwidth, contourcolor='w')` | outline for an existing text |
| `subplot_labels(*, fig=None, xlabel=None, ylabel=None)` | one centered x and y label for a whole subplot grid |
| `hide_empty_axes(axs=None)`, `label_outer(axs=None)` | hide empty panels, show tick labels and axis labels only on outer panels |
| `categorical_cmap(nc, nsc, *, cmap=None, return_colors=False)` | `nc` colors with `nsc` shades each |
| `categorical_color(nsc, color, *, return_hex=False)` | `nsc` shades of one color |
| `text_color(bgcolor, colors=('#000000', '#ffffff'))` | text color with the best contrast on a background |

Signatures and docstrings of the installed version are printed by
`python -m prettypyplot api NAME ...`. Run it in the environment of the
project, e.g. `uv run python -m prettypyplot api legend colorbar`, before
using a parameter that is not shown here. `api colormaps` lists all registered
colormaps with their number of colors, `api` without names prints everything.
prettypyplot <= 0.13.3 has no such command, use `help(pplt.legend)` instead.

### Legends

- `outside` is one of `False`, `'top'`, `'bottom'`, `'left'`, `'right'`. The
  tick labels of that side move to the opposite side, e.g.
  `outside='right'` with ticks on the right moves them to the left.
- `'top'` and `'bottom'` put all entries in one row (`ncol` = number of
  entries) spread over the axes width. Pass `ncol=` when there are many
  entries.
- One legend for several axes: `pplt.legend(axs=axs, outside='top')` without
  `ax`. Here `outside` must be `'top'`, `'bottom'` or `'right'`. The legend is
  placed relative to the bounding box of all given axes.
- Entries with the same label and look are merged, entries with the same label
  and color but a different look (line and markers) become one filled square.
  `deduplicate=False` keeps all entries.
- Other arguments go to `ax.legend`, e.g. `title=`, `frameon=False`, or
  explicit handles and labels.

### Colorbars

```python
fig, ax = plt.subplots()
im = pplt.imshow(np.random.default_rng(0).random((8, 8)), ax=ax)
pplt.colorbar(im, label='value')  # pass the image, not the axes
pplt.savefig('image.pdf')
```

The mappable can be anything with a colormap: `ax.pcolormesh(...)`,
`ax.scatter(..., c=values)`, `ax.contourf(...)`. Don't use `plt.colorbar` or
`fig.colorbar`, they shrink the axes. With `position='left'` the y tick labels
of the axes move to the right.

### Subplots

- Spacing via `gridspec_kw` (rule 4), panels with `sharex=True, sharey=True`.
- Unused panels: `pplt.hide_empty_axes(axs)`, then `pplt.label_outer(axs)`
  keeps tick labels and axis labels only on the outer panels, including panels
  above a hidden one.
- `pplt.subplot_labels(xlabel=..., ylabel=...)` adds one centered label per
  axis for the whole grid, drawn by an invisible helper axes. Call it after
  `hide_empty_axes()` and `label_outer()`, which otherwise treat the helper as
  an empty panel and hide the labels.

### Colors

- Named colors: `'pplt:blue'`, `'pplt:red'`, `'pplt:green'`, `'pplt:orange'`,
  `'pplt:lightblue'`, `'pplt:gray'`, `'pplt:lightgray'`, and the colors of the
  current style `'pplt:axes'`, `'pplt:text'`, `'pplt:grid'`.
- Color cycles: `use_style(colors=...)` takes any discrete colormap, e.g.
  `'pastel5'`, `'pastel6'`, `'cbf8'`, `'tol:bright'`, `'tol:muted'`,
  `'gdv:palette'`. Continuous colormaps: `'macaw'` (default), `'bownair'`,
  `'paula2'`, `'turbo'`, all matplotlib colormaps, and `'<name>_r'`.
- Annotating cells of a heatmap: `color=pplt.text_color(im.cmap(im.norm(value)))`.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `RuntimeError: latex was not able to process the following string` | LaTeX is active, escape `& # $ ^` or use `use_style(latex=False)` (rule 5) |
| `%` and the text after it are missing | LaTeX is active, write `r'\%'` or use `latex=False` |
| Saved figure is far too wide, huge gaps between panels | subplots without explicit `gridspec_kw` spacing (rule 4) |
| `subplots_adjust` is ignored | use `gridspec_kw` (rule 4) |
| Image upside down | `image.origin` is `'lower'`, pass `origin='upper'` |
| PNG looks black or empty in a viewer | transparent background, pass `transparent=False` |
| Colors repeat after 5 lines | `pastel5` cycle, choose a larger palette |
| Wrong figure saved | `pplt.savefig` saves `plt.gcf()` (rule 3) |
| `IndexError` in `pplt.savefig` | the current figure has no axes |
| `No module named prettypyplot.__main__` | prettypyplot <= 0.13.3, use `help(pplt.<name>)` instead of `python -m prettypyplot api` |
| `TypeError: unhashable type: 'numpy.ndarray'` in `pplt.legend` | prettypyplot <= 0.13.3 with array colors, pass `color=tuple(color)` |
| Legend of `pplt.legend(axs=...)` not aligned with the panels | prettypyplot <= 0.13.3 when the layout changes afterwards, e.g. with `subplot_labels`. Set the axis labels on every panel and call `pplt.label_outer(axs)` instead |
| `TypeError: ... _draw_text_as_path() missing ... 'mtext'` | matplotlib 3.11.0 with LaTeX and `contour`, upgrade matplotlib or drop `contour` |

## References

- `python -m prettypyplot api [NAME ...]`: every public function of the
  installed version with signature and docstring, and with `colormaps` all
  registered colormaps with number of colors.
- [references/style.md](references/style.md): choosing size, mode, style and
  colors for papers, slides and posters, exact figure sizes, LaTeX-safe text.
- Runnable examples: [examples/line_plot.py](examples/line_plot.py),
  [examples/multi_panel.py](examples/multi_panel.py),
  [examples/image_colorbar.py](examples/image_colorbar.py),
  [examples/categorical_colors.py](examples/categorical_colors.py).
