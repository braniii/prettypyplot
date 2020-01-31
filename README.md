# prettypyplot

This is a wrapper package for matplotlib to achieve more easily pretty figures.
If you are looking for something complete, this project is nothing for you
but maybe [seaborn](https://seaborn.pydata.org/). The main aspect of this
project is to help me syncing my rcParams files and to stop copy-pasting so
much code.

The aim of this project is to simplify the generation of some simple
pre-defined figures. Almost all code is inspired or taken from the
[matplotlib gallery](https://matplotlib.org/gallery/index.html). If you are a
power user or interested in generating complex figures, this packages is not
ment for you and you should better take a look in the matplotlib gallery
directly.

This project is in an alpha stage, hence it is neither stable nor ready for
production.
> **CAUTION**:
> Starting from version 1.0.0 (which is far in the future) API-breaking
> changes will be made only in major releases. Until then, it can be changed
> in every minor release (see [changelog](#changelog)).

## Features

The most notable features are:

- figsize specifies size of canvas. So labels, ticks or colorbars are not counted.
- Nice top-aligned outter legends
- New colors

## Usage

This package uses an syntax very close to matplotlib. Hence, it should be
straight forward to use it. Instead of calling a function on the axes itself,
one needs to pass here the axes as an argument (args or kwargs).

### Installation

```python
python3 -m pip install prettypyplot
```

### Usage

```python
import matplotlib.pyplot as plt
import prettypyplot as pplt

pplt.setup_pyplot()
fig, ax = plt.subplots()
...
pplt.plot(ax=ax, x, y)
pplt.savefig(output)
```

### Known Bugs

- `plt.subplots_adjust()` does not work with `pplt.savefig(use_canvas_size=True)`
If you find one, please open an issue.
- `pplt.savefig(use_canvas_size=True)` is not compatible with a grid of subplots

### Known Workarounds

The method `pyplot.subplots_adjust()` is not compatible with the option
`use_canvas_size` in `prettypyplot.plot.savefig`,
use instead:
```python
# this doesn't work, use instead gridspec
fig.subplots_adjust(hspace=0)
# use this instead
fig, axs = plt.subplots(..., gridspec_kw={'hspace': 0.000})
```

## Comparison to `matplotlib`

<table>
    <tr width="700" valign="top">
        <td>
            <code>matplotlib.pyplot.plot</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/mpl_plot.png" width="350">
        </td>
        <td>
            <code>prettypyplot.plot</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/default_plot.png" width="350">
        </td>
    </tr>
    <tr width="700" valign="top">
        <td>
            <code>matplotlib.pyplot.legend</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/mpl_plot_legend.png" width="350">
        </td>
        <td>
            <code>prettypyplot.legend</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/default_plot_legend.png" width="350">
        </td>
    </tr>
    <tr width="700" valign="top">
        <td>
            <code>matplotlib.pyplot.imshow</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/mpl_imshow.png" width="350">
        </td>
        <td>
            <code>prettypyplot.imshow</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/default_imshow.png" width="350">
        </td>
    </tr>
    <tr width="700" valign="top">
        <td>
            <code>matplotlib.pyplot.colorbar</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/mpl_imshow_cbar.png" width="350">
        </td>
        <td>
            <code>prettypyplot.colorbar</code><br>
            <img src="https://braniii.gitlab.io/prettypyplot/gallery/default_imshow_cbar.png" width="350">
        </td>
    </tr>
</table>

## Changelog and Roadmap:

### Changelog

- tba:
    - added gallery
    - refactored all submodules
    - added docs
    - many small bugfixes
- v0.1:
    - intial release

### Roadmap:

The following list is sorted from *near future* to *hopefully ever*.

- enforce simplicity by refactoring
- add countour line plot
- add [axes_grid](https://matplotlib.org/3.1.1/tutorials/toolkits/axes_grid.html) examples
- add more gallery entries
- improve `plt.suplots()` behaviour together with `pplt.savefig()`
- setup widths and scaling factors for beamer and poster mode
- tweak all function to enable `STYLE='minimal'`
- create own logo
- add pytest
- add search functionality in doc
- implement tufte style

## Building Documentation:

The doc is based on [pdoc](https://pdoc3.github.io/pdoc/) and can be created by
simply running `bash create_doc.sh` from the docs folder.

## Similar Projects

- [seaborn](https://seaborn.pydata.org/)

## Credits:

In alphabetical order:

- [colorcyclepicker](https://colorcyclepicker.mpetroff.net/)
- [matplotlib](https://matplotlib.org/)
- [prettyplotlib](https://github.com/olgabot/prettyplotlib)
- [realpython](https://realpython.com/)
- [viscm](https://github.com/matplotlib/viscm)
