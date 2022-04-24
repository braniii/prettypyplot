"""
Definition of colour schemes for lines and maps that also work for colour-blind
people. See https://personal.sron.nl/~pault/ for background information and
best usage of the schemes.

Copyright (c) 2021, Paul Tol
All rights reserved.

License:  Standard 3-clause BSD

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from matplotlib import colors as clr

# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
BRIGHT_ARRAY = [
    '#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377',
]
HIGH_CONTRAST_ARRAY = ['#004488', '#DDAA33', '#BB5566', '#000000']
VIBRANT_ARRAY = [
    '#EE7733', '#0077BB', '#33BBEE', '#EE3377', '#CC3311', '#009988',
]
MUTED_ARRAY = [
    '#CC6677',
    '#332288',
    '#DDCC77',
    '#117733',
    '#88CCEE',
    '#882255',
    '#44AA99',
    '#999933',
    '#AA4499',
]
MEDIUM_CONTRAST_ARRAY = [
    '#6699CC', '#004488', '#EECC66', '#994455', '#997700', '#EE99AA',
]
LIGHT_ARRAY = [
    '#77AADD',
    '#EE8866',
    '#EEDD88',
    '#FFAABB',
    '#99DDFF',
    '#44BB99',
    '#BBCC33',
    '#AAAA00',
]


def _tol_bright():
    return clr.ListedColormap(BRIGHT_ARRAY, 'tol:bright')


def _tol_high_contrast():
    return clr.ListedColormap(HIGH_CONTRAST_ARRAY, 'tol:high_contrast')


def _tol_vibrant():
    return clr.ListedColormap(VIBRANT_ARRAY, 'tol:vibrant')


def _tol_muted():
    return clr.ListedColormap(MUTED_ARRAY, 'tol:muted')


def _tol_medium_contrast():
    return clr.ListedColormap(MEDIUM_CONTRAST_ARRAY, 'tol:medium_contrast')


def _tol_light():
    return clr.ListedColormap(LIGHT_ARRAY, 'tol:light')
