# -*- coding: utf-8 -*-
"""Tests for the text module.

BSD 3-Clause License
Copyright (c) 2020, Daniel Nagel
All rights reserved.

"""
import numpy as np
import pytest

import prettypyplot


@pytest.mark.parametrize('contour, refcontour, error', [
    (True, {'contourwidth', 'contourcolor'}, None),
    (False, None, None),
    (5, None, TypeError),
    ('as', None, TypeError),
    ((5, 7), {'contourwidth': 5, 'contourcolor': 7}, None),
    ((1.2, 2.4), {'contourwidth': 1.2, 'contourcolor': 2.4}, None),
])
def test__parse_contour(contour, refcontour, error):
    """Test parsing figratio."""
    if error is None:
        kwargs = prettypyplot.texts._parse_contour(contour)
        if isinstance(refcontour, set):
            assert refcontour == set(kwargs.keys())
        else:
            assert refcontour == kwargs
    else:
        with pytest.raises(error):
            prettypyplot.texts._parse_contour(contour)
