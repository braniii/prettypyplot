# -*- coding: utf-8 -*-
"""Tests for the cmaps module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
from matplotlib.colors import LinearSegmentedColormap, ListedColormap

from prettypyplot import cmaps


def test_bownair():
    """Test bownair cmap."""
    assert isinstance(
        cmaps._bownair._bownair(), LinearSegmentedColormap,
    )


def test_macaw():
    """Test macaw cmap."""
    assert isinstance(
        cmaps._macaw._macaw(), LinearSegmentedColormap,
    )


def test_turbo():
    """Test turbo cmap."""
    assert isinstance(
        cmaps._turbo._turbo(), LinearSegmentedColormap,
    )


def test_discrete():
    """Test discrete cmaps."""
    for cmap in (
        cmaps._discrete._pastel5(),
        cmaps._discrete._pastel6(),
        cmaps._discrete._cbf4(),
        cmaps._discrete._cbf5(),
        cmaps._discrete._cbf8(),
        cmaps._discrete._pastel_rainbow(),
        cmaps._discrete._pastel_spring(),
        cmaps._discrete._pastel_autunm(),
        cmaps._discrete._ufcd(),
        cmaps._discrete._paula(),
    ):
        assert isinstance(cmap, ListedColormap)
