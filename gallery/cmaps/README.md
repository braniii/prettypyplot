# Colormaps

This module defines some perceptually uniform sequential and several
qualitative colormaps. All of them can be loaded into matplotlib by
`prettypyplot.colors.load_cmaps` or simply using the setup function
`prettypyplot.plot.setup_pyplot`.

.. warning::
    `macaw`, `pastel5`, `pastel6`, `ufcd` and `turbo` will be only modified
    slightly in future relases. All others will probably change dramatically.

`viridis` and `jet` are only included here for comparsion. Both, `macaw`
and `bownair` are modified versions of `viridis`. While `turbo` tries to be
a better `jet` (see [here](https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html)).

![Perceptually Uniform Sequential](../gallery/cmaps/Perceptually Uniform Sequential.png)
![Qualitative](../gallery/cmaps/Qualitative.png)

For more colormaps see [matplolib colormaps](https://matplotlib.org/tutorials/colors/colormaps.html).
