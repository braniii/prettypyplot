# -*- coding: utf-8 -*-
"""Tests for the subplots module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""
import numpy as np
import pytest
from matplotlib import collections
from matplotlib import patches
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

import prettypyplot


@pytest.mark.parametrize('ij1, ij2, kwargs, refdist', [
    ((0, 0), (1, 1), {'row_offset': 1, 'col_offset': 1}, True),
    ((0, 0), (1, 1), {'row_offset': 1}, False),
    ((1, 2), (1, 2), {}, True),
])
def test__has_neighbor_distance(ij1, ij2, kwargs, refdist):
    """Test neighbor distance."""
    fig, axs = plt.subplots(4, 4)
    assert prettypyplot.subplots._has_neighbor_distance(
        axs[ij1], axs[ij2], **kwargs,
    ) == refdist


@pytest.mark.parametrize('ij1, ij2, refneighbor', [
    ((1, 1), (2, 1), False),
    ((2, 1), (1, 1), True),
    ((1, 2), (1, 2), False),
])
def test__is_bottom_neighbor(ij1, ij2, refneighbor):
    """Test is bottom neighbor."""
    fig, axs = plt.subplots(4, 4)

    assert prettypyplot.subplots._is_bottom_neighbor(
        axs[ij1], axs[ij2],
    ) == refneighbor


@pytest.mark.parametrize('ij1, ij2, refneighbor', [
    ((1, 1), (1, 1), False),
    ((1, 1), (1, 2), True),
    ((1, 2), (1, 2), False),
])
def test__is_left_neighbor(ij1, ij2, refneighbor):
    """Test is left neighbor."""
    fig, axs = plt.subplots(4, 4)

    assert prettypyplot.subplots._is_left_neighbor(
        axs[ij1], axs[ij2],
    ) == refneighbor


def test__is_subplot_axes():
    """Test is subplot axes."""
    fig, ax = plt.subplots()
    assert prettypyplot.subplots._is_subplot_axes(ax)
    assert not prettypyplot.subplots._is_subplot_axes(fig)


def test__is_empty_axes():
    """Test is axes empty."""
    fig, axs = plt.subplots(1, 4)
    for axempty in axs.flatten():
        assert prettypyplot.subplots._is_empty_axes(axempty)

    # add artists
    axs[0].plot([0, 1], [0, 1])
    axs[1].text(0, 1, 'text')
    axs[2].add_collection(
        collections.LineCollection(
            [
                [(0, 0), (1, 1)],
                [(0, 0), (-1, -1)],
            ],
        ),
    )
    axs[3].add_patch(
        patches.Rectangle((0, 0), 1, 1),
    )

    for axfull in axs.flatten():
        assert not prettypyplot.subplots._is_empty_axes(axfull)


@pytest.mark.mpl_image_compare
def test__subplot_labels():
    """Test subplot labels."""
    num = 4
    fig, axs = plt.subplots(num, num)

    assert len(fig.get_axes()) == num**2
    prettypyplot.subplots.subplot_labels()
    assert len(fig.get_axes()) == num**2
    prettypyplot.subplots.subplot_labels(fig=fig)
    assert len(fig.get_axes()) == num**2
    prettypyplot.subplots.subplot_labels(ylabel='y', xlabel='x')
    assert len(fig.get_axes()) == num**2 + 1

    for ax in axs.flatten():
        ax.set_yticks([])
        ax.set_xticks([])

    return fig


def test__is_outer_hidden():
    """Test subplot labels."""
    fig, axs = plt.subplots(3, 3)
    for ax in axs[:2, 1:].flatten():
        ax.plot([0, 1], [0, 1])
    axs[0, 0].plot([0, 1], [0, 1])
    axs[2, 2].plot([0, 1], [0, 1])
    for ax in axs[(1, 2, 2), (0, 0, 1)]:
        ax.axis('off')

    for ij, left_empty, right_empty in (
        ((0, 1), False, False),
        ((1, 1), True, True),
        ((2, 1), True, False),
        ((1, 0), False, True),
        ((1, 2), False, False),
        ((0, 2), False, False),
    ):
        le, re = prettypyplot.subplots._is_outer_hidden(axs, axs[ij])
        assert le == left_empty and re == right_empty


@pytest.mark.parametrize('plotmask', [
    [True, False, True],
    [[True, True], [True, True]],
    [[False, True], [False, True]],
])
def test_hide_empty_axes(plotmask):
    """Test hide empty axes."""
    plotmask = np.atleast_2d(plotmask)
    fig, axs = plt.subplots(*plotmask.shape, squeeze=False)

    for ax, shouldplot in zip(np.ravel(axs), np.ravel(plotmask)):
        if shouldplot:
            ax.plot([0, 1], [0, 1])

    prettypyplot.subplots.hide_empty_axes(axs=axs)

    for ax, nothidden in zip(np.ravel(axs), np.ravel(plotmask)):
        assert ax.axison == nothidden


@pytest.mark.mpl_image_compare(remove_text=True)
def test_hide_empty_axes_mpl():
    """Test hide empty axes."""
    plotmask = np.array([[False, True], [True, False]])
    fig, axs = plt.subplots(*plotmask.shape, squeeze=False)

    for ax, shouldplot in zip(np.ravel(axs), np.ravel(plotmask)):
        if shouldplot:
            ax.plot([0, 1], [0, 1])

    prettypyplot.subplots.hide_empty_axes(axs=axs)
    return fig


@pytest.mark.parametrize('plotmask', [
    [True, False, True],
    [[True, True], [True, True]],
    [[False, True], [False, True]],
])
def test_label_outer(plotmask):
    """Check that no error occurs at labeling outer axes."""
    plotmask = np.atleast_2d(plotmask)
    fig, axs = plt.subplots(*plotmask.shape, squeeze=False)

    for ax, shouldplot in zip(np.ravel(axs), np.ravel(plotmask)):
        if shouldplot:
            ax.plot([0, 1], [0, 1])
    prettypyplot.subplots.hide_empty_axes(axs=axs)
    prettypyplot.subplots.label_outer(axs=axs)
    prettypyplot.subplots.label_outer()

    grid = ImageGrid(fig, 111, (2, 2))
    with pytest.raises(TypeError):
        prettypyplot.subplots.label_outer(axs=grid)


@pytest.mark.mpl_image_compare()
def test_label_outer_mpl():
    """Test hide empty axes."""
    plotmask = np.array([[True, True], [True, False], [False, True]])
    fig, axs = plt.subplots(*plotmask.shape, squeeze=False)

    for ax, shouldplot in zip(np.ravel(axs), np.ravel(plotmask)):
        if shouldplot:
            ax.plot([0, 1], [0, 1])

    prettypyplot.subplots.hide_empty_axes()
    prettypyplot.subplots.label_outer()
    return fig
