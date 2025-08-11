"""
Definition of colour schemes for geographic data and maps that also work for
colour-blind people. See
https://github.com/OrdnanceSurvey/GeoDataViz-Toolkit/tree/master/Colours
for background information and best usage of the schemes.

Copyright (c) 2025, OS GeoDataViz team
All rights reserved.

License: Open Government Licence 3.0

"""

# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from matplotlib import colors as clr

# ~~~ COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Red Amber Green
RAG_ARRAY = ['#E9002D', '#FFAA00', '#00B000']
RAG_CVD_ARRAY = ['#C40F5B', '#FD8D3C', '#089099']

# qualitative cmaps
PALETTE_ARRAY = [
    '#FF1F5B',
    '#00CD6C',
    '#009ADE',
    '#AF58BA',
    '#FFC61E',
    '#F28522',
    '#A0B1BA',
    '#A6761D',
]
SIXA_ARRAY = ['#FF1F5B', '#00CD6C', '#009ADE', '#AF58BA', '#FFC61E', '#F28522']
FIVEA_ARRAY = ['#FF1F5B', '#009ADE', '#AF58BA', '#FFC61E', '#F28522']
FOURA_ARRAY = ['#FF1F5B', '#009ADE', '#AF58BA', '#FFC61E']
FOURB_ARRAY = ['#00CD6C', '#009ADE', '#AF58BA', '#FFC61E']
THREEA_ARRAY = ['#FF1F5B', '#009ADE', '#FFC61E']
THREEB_ARRAY = ['#00CD6C', '#AF58BA', '#FFC61E']
TWOA_ARRAY = ['#FF1F5B', '#009ADE']
TWOB_ARRAY = ['#00CD6C', '#AF58BA']

# sequential cmaps
S1_ARRAY = [
    '#E4F1F7',
    '#C5E1EF',
    '#9EC9E2',
    '#6CB0D6',
    '#3C93C2',
    '#226E9C',
    '#0D4A70',
]
S2_ARRAY = [
    '#E1F2E3',
    '#CDE5D2',
    '#9CCEA7',
    '#6CBA7D',
    '#40AD5A',
    '#228B3B',
    '#06592A',
]
S3_ARRAY = [
    '#F9D8E6',
    '#F2ACCA',
    '#ED85B0',
    '#E95694',
    '#E32977',
    '#C40F5B',
    '#8F003B',
]
M1_ARRAY = [
    '#B7E6A5',
    '#7CCBA2',
    '#46AEA0',
    '#089099',
    '#00718B',
    '#045275',
    '#003147',
]
M2_ARRAY = [
    '#FCE1A4',
    '#FABF7B',
    '#F08F6E',
    '#E05C5C',
    '#D12959',
    '#AB1866',
    '#6E005F',
]
M3_ARRAY = [
    '#FFF3B2',
    '#FED976',
    '#FEB24C',
    '#FD8D3C',
    '#FC4E2A',
    '#E31A1C',
    '#B10026',
]

# diverging cmaps
D1_ARRAY = [
    '#009392',
    '#39B185',
    '#9CCB86',
    '#E9E29C',
    '#EEB479',
    '#E88471',
    '#CF597E',
]
D2_ARRAY = [
    '#045275',
    '#089099',
    '#7CCBA2',
    '#FCDE9C',
    '#F0746E',
    '#DC3977',
    '#7C1D6F',
]
D3_ARRAY = [
    '#443F90',
    '#685BA7',
    '#A599CA',
    '#F5DDEB',
    '#F492A5',
    '#EA6E8A',
    '#D21C5E',
]
D4_ARRAY = [
    '#008042',
    '#6FA253',
    '#B7C370',
    '#FCE498',
    '#D78287',
    '#BF5688',
    '#7C1D6F',
]

MOON_ARRAY = [
    '#FDFCE8',
    '#F1F3E5',
    '#E4E9E2',
    '#D7DFDF',
    '#CAD5DB',
    '#BDCBD8',
    '#B1C2D5',
    '#A4B8D2',
    '#97AECF',
    '#8AA4CB',
]
MARS_ARRAY = [
    '#E6F1E9',
    '#EAF3E8',
    '#F0F4E6',
    '#F7F6E6',
    '#F5F2DF',
    '#F7E8D5',
    '#EDD5C5',
    '#DCBEB0',
    '#B59790',
    '#D6C2C0',
]


def _gdv_rag():
    return clr.ListedColormap(RAG_ARRAY, 'gdv:rag')


def _gdv_rag_cvd():
    return clr.ListedColormap(RAG_CVD_ARRAY, 'gdv:rag_cvd')


def _gdv_palette():
    return clr.ListedColormap(PALETTE_ARRAY, 'gdv:palette')


def _gdv_6a():
    return clr.ListedColormap(SIXA_ARRAY, 'gdv:6a')


def _gdv_5a():
    return clr.ListedColormap(FIVEA_ARRAY, 'gdv:5a')


def _gdv_4a():
    return clr.ListedColormap(FOURA_ARRAY, 'gdv:4a')


def _gdv_4b():
    return clr.ListedColormap(FOURB_ARRAY, 'gdv:4b')


def _gdv_3a():
    return clr.ListedColormap(THREEA_ARRAY, 'gdv:3a')


def _gdv_3b():
    return clr.ListedColormap(THREEB_ARRAY, 'gdv:3b')


def _gdv_2a():
    return clr.ListedColormap(TWOA_ARRAY, 'gdv:2a')


def _gdv_2b():
    return clr.ListedColormap(TWOB_ARRAY, 'gdv:2b')


def _gdv_s1():
    return clr.ListedColormap(S1_ARRAY, 'gdv:s1')


def _gdv_s2():
    return clr.ListedColormap(S2_ARRAY, 'gdv:s2')


def _gdv_s3():
    return clr.ListedColormap(S3_ARRAY, 'gdv:s3')


def _gdv_m1():
    return clr.ListedColormap(M1_ARRAY, 'gdv:m1')


def _gdv_m2():
    return clr.ListedColormap(M2_ARRAY, 'gdv:m2')


def _gdv_m3():
    return clr.ListedColormap(M3_ARRAY, 'gdv:m3')


def _gdv_d1():
    return clr.ListedColormap(D1_ARRAY, 'gdv:d1')


def _gdv_d2():
    return clr.ListedColormap(D2_ARRAY, 'gdv:d2')


def _gdv_d3():
    return clr.ListedColormap(D3_ARRAY, 'gdv:d3')


def _gdv_d4():
    return clr.ListedColormap(D4_ARRAY, 'gdv:d4')


def _gdv_moon():
    return clr.ListedColormap(MOON_ARRAY, 'gdv:moon')


def _gdv_mars():
    return clr.ListedColormap(MARS_ARRAY, 'gdv:mars')
