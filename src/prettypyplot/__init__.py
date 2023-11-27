"""# Prettypyplot

This package provides helper functions to easen the usage of matplotlib.

The module is structured into the following submodules:

- [**pyplot:**][prettypyplot.pyplot] This submodule contains all methods
  related to plotting inside a single axes, so basically related to
  [matplotlib.pyplot][].

- [**style:**][prettypyplot.style] This module provides only method to load
  and alter the current style.

- [**subplots:**][prettypyplot.subplots] This module provides methods to
  simplify dealing with [matplotlib.pyplot.subplots][] grids.

- [**texts:**][prettypyplot.texts] This module provides methods to
  plot text with the possibility to add a contour.

- [**tools:**][prettypyplot.tools] This module provides uitility methods to.

"""
# both are set in style submodule to default value
MODE = None
STYLE = None

# style dictionary
STYLE_DICT = {}

__all__ = [  # noqa: F405
    'setup_pyplot',
    'update_style',
    'use_style',
    'add_contour',
    'text',
    'figtext',
    'hide_empty_axes',
    'label_outer',
    'subplot_labels',
    'load_cmaps',
    'load_colors',
    'categorical_cmaps',
    'categorical_color',
    'text_color',
]

from .colors import *
from .pyplot import (
    imshow,
    plot,
    savefig,
    legend,
    colorbar,
    grid,
)
from .style import (setup_pyplot, update_style, use_style)
from .texts import (add_contour, figtext, text)
from .subplots import (hide_empty_axes, label_outer, subplot_labels)

__version__ = '0.10.1'
