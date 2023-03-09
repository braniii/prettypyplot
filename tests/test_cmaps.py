# -*- coding: utf-8 -*-
"""Tests for the cmaps module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from prettypyplot import _cmaps as cmaps


def test_bownair():
    """Test bownair cmap."""
    assert isinstance(
        cmaps.bownair._bownair(), LinearSegmentedColormap,
    )


def test_macaw():
    """Test macaw cmap."""
    assert isinstance(
        cmaps.macaw._macaw(), LinearSegmentedColormap,
    )


def test_turbo():
    """Test turbo cmap."""
    assert isinstance(
        cmaps.turbo._turbo(), LinearSegmentedColormap,
    )


def test_discrete():
    """Test discrete cmaps."""
    for cmap in (
        cmaps.discrete._pastel5(),
        cmaps.discrete._pastel6(),
        cmaps.discrete._cbf4(),
        cmaps.discrete._cbf5(),
        cmaps.discrete._cbf8(),
        cmaps.discrete._pastel_rainbow(),
        cmaps.discrete._pastel_spring(),
        cmaps.discrete._pastel_autunm(),
        cmaps.discrete._ufcd(),
        cmaps.discrete._paula(),
        cmaps.discrete._summertimes(),
    ):
        assert isinstance(cmap, ListedColormap)
