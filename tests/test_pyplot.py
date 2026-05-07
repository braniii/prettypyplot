# -*- coding: utf-8 -*-
"""Tests for the plot module.

BSD 3-Clause License
Copyright (c) 2020-2021, Daniel Nagel
All rights reserved.

"""

import matplotlib as mpl
import numpy as np
import pytest
from matplotlib import patches as mpatches
from matplotlib import pyplot as plt

import prettypyplot
from prettypyplot.pyplot import _legend_handle_color, _legend_handle_key


@pytest.mark.parametrize(
    'data, ticks',
    (
        (np.arange(10), None),
        (np.arange(10), np.arange(10)),
        (np.arange(10), np.arange(2)),
    ),
)
def test__reduce_ticks(data, ticks):
    # check that the number of ticks is not reduced when setting the ticks
    # explicitly
    fig, ax = plt.subplots()
    ax.plot(data)

    if ticks is not None:
        ax.set_xticks(ticks)

    nticks = len(ax.get_xticks())

    prettypyplot.pyplot._reduce_ticks(fig)

    if ticks is None:
        assert nticks >= len(ax.get_xticks())
    else:
        assert nticks == len(ax.get_xticks())


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize(
    'data, style, kwargs',
    (
        (np.arange(25).reshape(-1, 5), 'default', {}),
        (np.arange(25).reshape(-1, 5), 'default', {'zorder': 0}),
        (np.arange(25).reshape(-1, 5), 'minimal', {}),
        (np.arange(25).reshape(-1, 5), 'minimal', {'zorder': 0}),
    ),
)
def test_imshow(data, style, kwargs):
    """Test imshow."""
    prettypyplot.use_style(style=style)

    fig, ax = plt.subplots()
    # activate grid to see influence of zorder
    ax.grid(True)

    im = prettypyplot.imshow(data, **kwargs)
    assert isinstance(im, mpl.image.AxesImage)

    # allow plotting grid behind image
    ax.set_axisbelow(True)

    return fig


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize(
    'data, style, args, kwargs',
    (
        ((np.arange(25), np.sin(np.arange(25))), 'default', (), {}),
        ((np.arange(25), np.cos(np.arange(25))), 'default', ('bo',), {}),
        ((np.arange(25), np.sin(np.arange(25))), 'minimal', (), {}),
        ((np.arange(25), np.cos(np.arange(25))), 'minimal', ('bo',), {}),
    ),
)
def test_plot(data, style, args, kwargs):
    """Test imshow."""
    prettypyplot.use_style(style=style)

    fig, ax = plt.subplots()

    _ = prettypyplot.plot(*data, *args, **kwargs)

    return fig


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize(
    'style',
    ('default', 'minimal'),
)
def test_legend_dedup(style):
    """Test that duplicate handles+labels are removed from the legend."""
    np.random.seed(42)
    T = np.linspace(0, 2 * np.pi, 100)
    X1 = np.sin(T)
    X2 = np.cos(T)

    prettypyplot.use_style(style=style)
    fig, axs = plt.subplots(1, 2)

    for ax in axs:
        prettypyplot.plot(T, X1, ax=ax, label='sin')
        prettypyplot.plot(T, X2, ax=ax, label='cos')

    # axs collects 4 entries (sin+cos from each panel); dedup reduces to 2
    leg = prettypyplot.legend(outside='right', ax=axs[-1], axs=axs)
    assert len(leg.get_texts()) == 2

    return fig


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize(
    'style',
    ('default', 'minimal'),
)
def test_legend_dedup_handle_types(style):
    """Test dedup across scatter, errorbar, and bar/hatch handle types."""
    np.random.seed(42)
    x = np.arange(5, dtype=float)
    y = np.array([1.0, 2.0, 1.5, 3.0, 2.5])

    prettypyplot.use_style(style=style)
    fig, axs = plt.subplots(1, 2, gridspec_kw={'wspace': 0})

    for ax in axs:
        ax.scatter(x, y, marker='s', color='C0', label='scatter')
        ax.errorbar(x, y + 1, yerr=0.3, color='C1', label='errorbar')
        ax.bar(x, y, color='C2', hatch='//', label='bar')

    # 9 entries total (3 per axis × 2 axes); dedup should reduce to 3
    leg = prettypyplot.legend(
        outside='top',
        ax=axs[0],
        axs=axs,
        bbox_to_anchor=(0.0, 1.0, len(axs), 0.01),
        frameon=False,
    )
    assert len(leg.get_texts()) == 3

    return fig


def test_legend_deduplicate_false():
    """With deduplicate=False all handles are kept, even visual duplicates."""
    T = np.linspace(0, 2 * np.pi, 50)
    prettypyplot.use_style()
    fig, axs = plt.subplots(1, 2)
    for ax in axs:
        prettypyplot.plot(T, np.sin(T), ax=ax, label='sin')
        prettypyplot.plot(T, np.cos(T), ax=ax, label='cos')

    leg = prettypyplot.legend(outside='right', ax=axs[-1], axs=axs, deduplicate=False)
    assert len(leg.get_texts()) == 4
    plt.close(fig)


def test_legend_background_outside():
    """Legend outside the axes should have a transparent background."""
    prettypyplot.use_style()
    fig, ax = plt.subplots()
    prettypyplot.plot([0, 1], [0, 1], ax=ax, label='a')
    leg = prettypyplot.legend(outside='right', ax=ax)
    assert leg.get_frame().get_alpha() == 0.0
    plt.close(fig)


def test_legend_handle_key_patch():
    """Test _legend_handle_key for a bare Patch handle (fill_between)."""
    fig, ax = plt.subplots()
    _ = ax.fill_between([0, 1], [0, 0], [1, 1], color='C3', label='fill')
    plt.close(fig)

    # fill_between returns a PolyCollection (PathCollection subclass) on some
    # mpl versions, but we can also test a plain Patch directly.
    patch = mpatches.Patch(facecolor='red', edgecolor='blue', hatch='/')
    key = _legend_handle_key(patch)
    assert isinstance(key, tuple)
    assert len(key) == 3


def test_legend_handle_key_fallback():
    """Test _legend_handle_key fallback for an unknown handle type."""
    key = _legend_handle_key('not-a-handle')
    assert isinstance(key, str)
    assert 'not-a-handle' in key


def test_legend_dedup_same_color_different_patches():
    """Same label + same color but different handle types → single filled square."""
    prettypyplot.use_style()
    fig, ax = plt.subplots()
    color = 'C0'
    ax.plot([0, 1], [0, 1], color=color, label='data')
    ax.scatter([0, 1], [0.5, 0.5], color=color, label='data')
    ax.bar([0], [1], color=color, label='data')

    leg = prettypyplot.legend(ax=ax)
    assert len(leg.get_texts()) == 1
    handle = leg.legend_handles[0]
    assert isinstance(handle, mpatches.Patch)
    plt.close(fig)


def test_legend_handle_color_line2d():
    """_legend_handle_color returns RGBA tuple for Line2D."""
    fig, ax = plt.subplots()
    (line,) = ax.plot([0, 1], [0, 1], color='red')
    plt.close(fig)
    color = _legend_handle_color(line)
    assert isinstance(color, tuple)
    assert len(color) == 4


def test_legend_handle_color_unknown():
    """_legend_handle_color returns None for unknown handle types."""
    assert _legend_handle_color('not-a-handle') is None


def test_legend_handle_color_invalid_color_returns_none():
    """_to_rgba fallback: a Line2D whose color cannot be parsed returns None."""
    from matplotlib import lines as mlines

    line = mlines.Line2D([0, 1], [0, 1])
    line.get_color = lambda: 'definitely-not-a-color'
    assert _legend_handle_color(line) is None


def test_legend_handle_color_patch():
    """_legend_handle_color returns the facecolor of a Patch."""
    patch = mpatches.Patch(facecolor='red')
    color = _legend_handle_color(patch)
    assert color == (1.0, 0.0, 0.0, 1.0)


def test_legend_handle_color_path_collection_empty():
    """_legend_handle_color returns None when PathCollection has no facecolor."""
    from matplotlib.collections import PathCollection

    pc = PathCollection([], facecolors='none')
    pc.get_facecolor = lambda: np.empty((0, 4))
    assert _legend_handle_color(pc) is None


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize('outside', ('top', 'bottom', 'right', 'left'))
def test_legend_spanning(outside):
    """Test figure-level legend spanning two rows of a 3×2 grid."""
    np.random.seed(0)
    T = np.linspace(0, 2 * np.pi, 100)

    prettypyplot.use_style()
    fig, all_axs = plt.subplots(
        3,
        2,
        gridspec_kw={
            'wspace': 0.2,
            'hspace': 0.3,
            'height_ratios': [1, 1.5, 2],
            'width_ratios': [1, 2],
        },
    )

    used_axs = all_axs[:2, :].ravel()

    for ax in all_axs.ravel():
        prettypyplot.plot(T, np.sin(T), ax=ax, label='sin')
        prettypyplot.plot(T, np.cos(T), ax=ax, label='cos')

    leg = prettypyplot.legend(outside=outside, axs=used_axs)
    assert len(leg.get_texts()) == 2

    return fig


def test_legend_spanning_requires_outside():
    """axs without ax must have outside set."""
    fig, axs = plt.subplots(1, 2)
    for ax in axs:
        ax.plot([0, 1], label='a')
    with pytest.raises(ValueError, match='outside'):
        prettypyplot.legend(axs=axs)
    plt.close(fig)


@pytest.mark.parametrize('outside', ('top', 'bottom', 'right', 'left'))
def test_legend_spanning_figure_level(outside):
    """Legend placed via axs-only mode is attached to the figure."""
    T = np.linspace(0, 2 * np.pi, 50)
    fig, axs = plt.subplots(1, 2)
    for ax in axs:
        ax.plot(T, np.sin(T), label='sin')
        ax.plot(T, np.cos(T), label='cos')

    leg = prettypyplot.legend(outside=outside, axs=axs)

    # figure.legends contains figure-level legends; axes.get_legend() should be None
    assert leg in fig.legends
    for ax in axs:
        assert ax.get_legend() is None
    assert len(leg.get_texts()) == 2
    plt.close(fig)


def test_legend_spanning_top_width():
    """For outside='top', legend bbox covers the full axes span."""
    T = np.linspace(0, 2 * np.pi, 50)
    fig, axs = plt.subplots(1, 3, figsize=(9, 3))
    for ax in axs:
        ax.plot(T, np.sin(T), label='sin')

    leg = prettypyplot.legend(outside='top', axs=axs)

    fig.canvas.draw()
    positions = [ax.get_position() for ax in axs]
    expected_x0 = min(p.x0 for p in positions)
    expected_x1 = max(p.x1 for p in positions)
    # bbox_to_anchor stores (x0, y1, width, height) in figure coords
    anchor = leg.get_bbox_to_anchor()
    # anchor is a Bbox in display coords; convert to figure fraction
    fig_w = fig.get_size_inches()[0] * fig.dpi
    tol = 0.01
    assert abs(anchor.x0 / fig_w - expected_x0) < tol
    assert abs(anchor.x1 / fig_w - expected_x1) < tol
    plt.close(fig)


def test_legend_spanning_right_center():
    """For outside='right', legend is vertically centred across all axes."""
    T = np.linspace(0, 2 * np.pi, 50)
    fig, axs = plt.subplots(2, 1, figsize=(4, 6))
    for ax in axs:
        ax.plot(T, np.sin(T), label='sin')

    leg = prettypyplot.legend(outside='right', axs=axs)

    fig.canvas.draw()
    positions = [ax.get_position() for ax in axs]
    y0 = min(p.y0 for p in positions)
    y1 = max(p.y1 for p in positions)
    expected_center = (y0 + y1) / 2

    anchor = leg.get_bbox_to_anchor()
    fig_h = fig.get_size_inches()[1] * fig.dpi
    tol = 0.02
    actual_center = anchor.y0 / fig_h
    assert abs(actual_center - expected_center) < tol
    plt.close(fig)


def test_legend_spanning_left_center():
    """For outside='left', legend is vertically centred and to the left of the axes."""
    T = np.linspace(0, 2 * np.pi, 50)
    fig, axs = plt.subplots(2, 1, figsize=(4, 6))
    for ax in axs:
        ax.plot(T, np.sin(T), label='sin')

    leg = prettypyplot.legend(outside='left', axs=axs)

    fig.canvas.draw()
    positions = [ax.get_position() for ax in axs]
    x0 = min(p.x0 for p in positions)
    y0 = min(p.y0 for p in positions)
    y1 = max(p.y1 for p in positions)
    expected_center = (y0 + y1) / 2

    anchor = leg.get_bbox_to_anchor()
    fig_w = fig.get_size_inches()[0] * fig.dpi
    fig_h = fig.get_size_inches()[1] * fig.dpi
    tol = 0.02
    assert anchor.x0 / fig_w < x0
    assert abs(anchor.y0 / fig_h - expected_center) < tol
    plt.close(fig)


def test_legend_spanning_bottom_width():
    """For outside='bottom', legend bbox covers the full axes span."""
    T = np.linspace(0, 2 * np.pi, 50)
    fig, axs = plt.subplots(1, 3, figsize=(9, 3))
    for ax in axs:
        ax.plot(T, np.sin(T), label='sin')

    leg = prettypyplot.legend(outside='bottom', axs=axs)

    fig.canvas.draw()
    positions = [ax.get_position() for ax in axs]
    expected_x0 = min(p.x0 for p in positions)
    expected_x1 = max(p.x1 for p in positions)

    anchor = leg.get_bbox_to_anchor()
    fig_w = fig.get_size_inches()[0] * fig.dpi
    tol = 0.01
    assert abs(anchor.x0 / fig_w - expected_x0) < tol
    assert abs(anchor.x1 / fig_w - expected_x1) < tol
    plt.close(fig)


@pytest.mark.mpl_image_compare(remove_text=True)
@pytest.mark.parametrize(
    'data, style, args, ylog',
    (
        ((np.arange(25), np.arange(25)), 'default', (True,), False),
        ((np.arange(25), np.arange(25)), 'default', (), False),
        ((np.arange(25), np.arange(25)), 'default', (False,), False),
        ((np.arange(25), 2 + np.arange(25) ** 2), 'default', (True,), True),
        ((np.arange(25), np.arange(25)), 'minimal', (True,), False),
        ((np.arange(25), np.arange(25)), 'minimal', (False,), False),
        ((np.arange(25), np.arange(25)), 'minimal', (), False),
        ((np.arange(25), 2 + np.arange(25) ** 2), 'minimal', (True,), True),
    ),
)
def test_grid(data, style, args, ylog):
    """Test grid."""
    prettypyplot.use_style(style=style)

    fig, ax = plt.subplots()

    _ = prettypyplot.plot(*data)
    _ = prettypyplot.grid(*args)

    if ylog:
        ax.set_yscale('log')

    return fig
