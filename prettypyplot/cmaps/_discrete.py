"""
Set-up matplotlib environment.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

Author: Daniel Nagel

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import matplotlib.colors as clr

# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# created with https://medialab.github.io/iwanthue/
cbf5_array = ['#b94663', '#6fac5d', '#697ed5', '#bc7d39', '#9350a1']

# created with https://colorcyclepicker.mpetroff.net/
cbf4_array = ['#1878b1', '#dd6688', '#2dd9cc', '#feeaae']
cbf8_array = ['#0c4daa', '#b70226', '#238494', '#d2651e', '#88a8ba',
              '#2ad5ad', '#fbb5fe', '#faf018']
pastel5_array = ['#3362b0', '#cc3164', '#1ea69c', '#f78746', '#9dd2e7']
pastel6_array = ['#2452c7', '#c42f22', '#2aa069', '#67b2cf', '#f8a7ae',
                 '#a6f89c']

# Uni Corporate Design
# copyright by Albert-Ludwigs-Universität Freiburg
ufcd_array = ['#2a6ebb', '#de3831', '#739600', '#e98300', '#a7c1e3']


def __pastel5():
    return clr.ListedColormap(pastel5_array, 'pastel5')


def __pastel6():
    return clr.ListedColormap(pastel6_array, 'pastel6')


def __cbf4():
    return clr.ListedColormap(cbf4_array, 'cbf4')


def __cbf5():
    return clr.ListedColormap(cbf5_array, 'cbf5')


def __cbf8():
    return clr.ListedColormap(cbf8_array, 'cbf8')


def __ufcd():
    return clr.ListedColormap(ufcd_array, 'ufcd')
