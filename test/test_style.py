# -*- coding: utf-8 -*-
"""Tests for the plot module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import matplotlib as mpl
import numpy as np
import pytest
from matplotlib import pyplot as plt

import prettypyplot


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

