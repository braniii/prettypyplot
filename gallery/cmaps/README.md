# Colormaps

This module defines some perceptually uniform sequential and several
qualitative colormaps. All of them can be loaded into matplotlib by
`prettypyplot.colors.load_cmaps` or simply using the setup function
`prettypyplot.style.use_style`. With `prettypyplot.colors.load_colors`
the colors of `pastel5` (`'pplt:blue'`, `'pplt:red'`, `'pplt:green'`,
`'pplt:orange'`, `'pplt:lightblue'`), axes `'pplt:axes'`, grid
`'pplt:grid'` and textcolor `'pplt:text'` can be accessed easily.

The qualitative colors `'pastel_autumn'`, `'pastel_spring'`, 
`'pastel_rainbow'` are neither cbf friendly nor suited for black-white.

.. warning::
    `macaw`, `pastel5`, `pastel6`, `ufcd` and `turbo` will be only modified
    slightly in future relases. All others will probably change dramatically.

`viridis` and `jet` are only included here for comparsion. Both, `macaw`
and `bownair` are modified versions of `viridis`. While `turbo` tries to be
a better `jet` (see [here](https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html)).

![Perceptually Uniform Sequential](../gallery/cmaps/Perceptually Uniform Sequential.png)
![Qualitative](../gallery/cmaps/Qualitative.png)

For more colormaps see [matplolib colormaps](https://matplotlib.org/tutorials/colors/colormaps.html).
