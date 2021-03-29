"""Create Matplotlib inspired logo.

This script is taken from
https://matplotlib.org/gallery/misc/logos2.html#sphx-glr-gallery-misc-logos2-py
an heavily simplified to fit the spirit of prettypyplot.

"""
import matplotlib.pyplot as plt
import logo

import prettypyplot as pplt


pplt.use_style(latex=False)

fig, ax = logo.make_logo(height_px=120)

pplt.figtext(
    1.4,
    1.15,
    'prettypyplot',
    va='top',
    ha='left',
    fontsize=8,
    weight='bold',
    fontname='Roboto',
)

_, clight, _, _ = pplt.categorical_color(4, 'pplt:gray')
pplt.figtext(
    1.4,
    0.6,
    'Publication ready\nmatplotlib figures\nmade simple',
    va='top',
    ha='left',
    fontsize=5,
    color=clight,
    fontname='Roboto',
)

pplt.savefig('gallery/logo_large.png')
