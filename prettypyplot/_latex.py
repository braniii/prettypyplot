"""
Set-up latex preamble for advanced functionality.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.pyplot as plt


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def load_latex_preamble(contour=True):
    r"""
    Load additional latex packages.

    Parameters
    ----------
    contour : bool, optional
        Creates a command similar to the contour package, but suitable for
        XeLaTeX. Use it with `\contour{text}` or by specifying the width
        `\contour[width]{text}`.

    """
    if contour:
        _latex_contour()


def _latex_contour():
    """Add more packages to preamble."""
    # add contour support
    contour_str = (
        r'\usepackage{xcolor}'
        r'\def\rgbtoarray#1,#2,#3\null{[#1 #2 #3]}'
        r'\def\csvtoarray#1{'
        r'  \expandafter\rgbtoarray#1\null'
        r'}'
        r'\newcommand{\extractrgb}[2]{'
        r'  \extractcolorspecs{#1}{\model}{\mycolor}'
        r'  \convertcolorspec{\model}{\mycolor}{rgb}{\printcol}'
        r'  \edef#2{\printcol}'
        r'}'
        r'\newcommand*{\fillstroke}[4]{'
        r'  \extractrgb{#1}{\colorvector}'
        r'  \extractrgb{#2}{\strokevector}'
        r'  \special{pdf:bcolor'
        r'    \csvtoarray{\colorvector}'
        r'    \csvtoarray{\strokevector}'
        r'  }'
        r'  \special{pdf:literal direct #3 w 2 Tr}'
        r'  #4'
        r'  \special{pdf:ecolor}'
        r'  \special{pdf:literal direct 0 Tr}'
        r'}'
        r'\newcommand*{\contour}[2][0.5]{'
        r'  \fillstroke{black}{white}{#1}{#2}'
        r'}'
    )
    plt.rcParams['text.latex.preamble'] += contour_str
