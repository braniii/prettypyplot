# -*- coding: utf-8 -*-
"""Tests for the plot module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import numpy as np
import pytest

import prettypyplot


@pytest.mark.parametrize('figratio, refratio, error', [
    ('sqrt(2)', 1.4142135623730951, None),
    (2, 2, None),
    (2.0, 2, None),
    ('golden', 1.618033988749895, None),
    ('error', None, ValueError),
])
def test_parse__figratio(figratio, refratio, error):
    """Test parsing figratio."""
    if error is None:
        figratio = prettypyplot.style._parse_figratio(figratio)
        np.testing.assert_almost_equal(figratio, refratio)
    else:
        with pytest.raises(error):
            prettypyplot.style._parse_figratio(figratio)


@pytest.mark.parametrize('figsize, figratio, refsize, error', [
    ((1, 2), None, (1, 2), None),
    ([1, 2], None, (1, 2), None),
    (np.array([1, 2]), None, (1, 2), None),
    (1, 0.5, (1, 2), None),
    ((1, ), 0.5, (1, 2), None),
    ([1, ], 0.5, (1, 2), None),
    ((1, 2, 3), None, None, ValueError),
    ('a', None, None, ValueError),
    (('a', 2), None, None, ValueError),
])
def test_parse__figsize(figsize, figratio, refsize, error):
    """Test parsing figsize."""
    if error is None:
        figsize = prettypyplot.style._parse_figsize(figsize, figratio)
        np.testing.assert_array_almost_equal(figsize, refsize)
    else:
        with pytest.raises(error):
            prettypyplot.style._parse_figsize(figsize, figratio)


@pytest.mark.parametrize('kwargs, error', (
    ({}, None),
    ({'style': 'default'}, None),
    ({'mode': 'default'}, None),
    ({'figsize': 10}, None),
    ({'figsize': 10, 'figratio': 2}, None),
    ({'figsize': 10, 'figratio': 'golden'}, None),
    ({'figratio': 'golden'}, None),
    ({'style': 'errorstyle'}, ValueError),
    ({'mode': 'errormode'}, ValueError),
))
def test_use_stlyle(kwargs, error):
    """Test use_style. Functionality is tested in the plot module."""
    if error is None:
        prettypyplot.use_style(**kwargs)
    else:
        with pytest.raises(error):
            prettypyplot.use_style(**kwargs)
