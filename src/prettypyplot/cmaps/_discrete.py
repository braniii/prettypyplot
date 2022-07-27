"""Set-up matplotlib environment.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from matplotlib import colors as clr

# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# created with https://medialab.github.io/iwanthue/
CBF5_ARRAY = ['#b94663', '#6fac5d', '#697ed5', '#bc7d39', '#9350a1']

# created with https://colorcyclepicker.mpetroff.net/
CBF4_ARRAY = ['#1878b1', '#dd6688', '#2dd9cc', '#feeaae']
CBF8_ARRAY = [
    '#0c4daa',
    '#b70226',
    '#238494',
    '#d2651e',
    '#88a8ba',
    '#2ad5ad',
    '#fbb5fe',
    '#faf018',
]
PASTEL5_ARRAY = ['#3362b0', '#cc3164', '#1ea69c', '#f78746', '#9dd2e7']
PASTEL6_ARRAY = [
    '#2452c7', '#c42f22', '#2aa069', '#67b2cf', '#f8a7ae', '#a6f89c',
]

# Coolors Exported Palette
# https://coolors.co/f94144-f3722c-f8961e-f9c74f-90be6d-43aa8b-577590
RAINBOW_ARRAY = [
    '#f94144',
    '#f3722c',
    '#f8961e',
    '#f9c74f',
    '#90be6d',
    '#43aa8b',
    '#577590',
]
# https://coolors.co/ef476f-ffd166-06d6a0-118ab2-073b4c
SPRING_ARRAY = ['#ef476f', '#ffd166', '#06d6a0', '#118ab2', '#073b4c']
# https://coolors.co/264653-2a9d8f-e9c46a-f4a261-e76f51
AUTUNM_ARRAY = ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51']

# Uni Corporate Design
# copyright by Albert-Ludwigs-Universität Freiburg
UFCD_ARRAY = ['#2a6ebb', '#de3831', '#739600', '#e98300', '#a7c1e3']

# own creation
PAULA_ARRAY = ['#fec21f', '#ed6a0c', '#df0712', '#df017b', '#4a287d']
ARGON_ARRAY = [
    '#252b3b', '#406558', '#628d79', '#cda901', '#e26b00', '#cb1a26',
]

SUMMER_ARRAY = [
    '#002661',
    '#38a1ae',
    '#ffbc42',
    '#e3170a',
    '#38a75d',
    '#a11963',
]


def _pastel5():
    return clr.ListedColormap(PASTEL5_ARRAY, 'pastel5')


def _pastel6():
    return clr.ListedColormap(PASTEL6_ARRAY, 'pastel6')


def _cbf4():
    return clr.ListedColormap(CBF4_ARRAY, 'cbf4')


def _cbf5():
    return clr.ListedColormap(CBF5_ARRAY, 'cbf5')


def _cbf8():
    return clr.ListedColormap(CBF8_ARRAY, 'cbf8')


def _pastel_rainbow():
    return clr.ListedColormap(RAINBOW_ARRAY, 'pastel_rainbow')


def _pastel_spring():
    return clr.ListedColormap(SPRING_ARRAY, 'pastel_spring')


def _pastel_autunm():
    return clr.ListedColormap(AUTUNM_ARRAY, 'pastel_autunm')


def _ufcd():
    return clr.ListedColormap(UFCD_ARRAY, 'ufcd')


def _paula():
    return clr.ListedColormap(PAULA_ARRAY, 'paula')


def _argon():
    return clr.ListedColormap(ARGON_ARRAY, 'argon')


def _summertimes():
    return clr.ListedColormap(SUMMER_ARRAY, 'summertimes')
