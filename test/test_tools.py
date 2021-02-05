# -*- coding: utf-8 -*-
"""Tests for the tools module.

BSD 3-Clause License
Copyright (c) 2019-2020, Daniel Nagel
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
def test_parse_figratio(figratio, refratio, error):
    """Test parsing figratio."""
    if error is None:
        figratio = prettypyplot.tools.parse_figratio(figratio)
        np.testing.assert_almost_equal(figratio, refratio)
    else:
        with pytest.raises(error):
            figratio = prettypyplot.tools.parse_figratio(figratio)
