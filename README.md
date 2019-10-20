# prettypyplot

This is a wrapper package for matplotlib to achieve more easily pretty figures.
It is in an alpha stage, hence it is neither stable nor ready for production.

# Usage
This package uses an syntax very close to matplotlib. Hence, it should be
streight forward to use it. Instead of calling a function on the axes itself,
one needs to pass here the axes as an argument (args or kwargs).
## Usage
```python
import prettypyplot.plot as pplt
pplt.setup_pyplot(mode=MODE, style=STYLE, ...)
fig, ax = plt.subplots(1,1,...)
...
pplt.plot(ax=ax, x, y)
pplt.savefig(output)
```
## Known Bugs
## Known Workarounds
The method `subplots_adjust` is not compatible with the option `use_canvas_size`,
use instead:
```python
fig.subplots_adjust(hspace=0)  # this doesn't work, use instead gridspec
fig, axs = plt.subplots(..., gridspec_kw={'hspace': 0.000})
```

# Changelog:
- tba:
  - refactored in two submodules (one for colors one for plotting)
- v0.1:
  - intial release

# Roadmap:
- use palettable (https://jiffyclub.github.io/palettable/#)
- setup widths and scaling factors for beamer and poster mode
- implement tufte style
- add https://matplotlib.org/3.1.1/tutorials/toolkits/axes_grid.html examples

# Credits:
- [matplotlib](https://matplotlib.org/)
- [realpython](https://realpython.com/)
