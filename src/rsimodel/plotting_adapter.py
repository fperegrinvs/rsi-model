"""Typed, headless plotting boundary for generated publication figures."""

from __future__ import annotations

from collections.abc import Sequence
from typing import cast

import matplotlib

matplotlib.use("Agg")

from matplotlib import pyplot
from matplotlib.axes import Axes
from matplotlib.colors import TwoSlopeNorm
from matplotlib.figure import Figure
from matplotlib.patches import Patch


def use_style(name: str) -> None:
    pyplot.style.use(name)


def single_axes(*, figsize: tuple[float, float]) -> tuple[Figure, Axes]:
    figure, raw_axes = pyplot.subplots(figsize=figsize)
    if not isinstance(raw_axes, Axes):
        raise RuntimeError("Matplotlib returned a non-scalar axes layout")
    return figure, raw_axes


def axes_row(
    columns: int,
    *,
    figsize: tuple[float, float],
    sharey: bool = False,
) -> tuple[Figure, tuple[Axes, ...]]:
    if columns <= 0:
        raise ValueError("plot columns must be positive")
    figure, raw_axes = pyplot.subplots(1, columns, figsize=figsize, sharey=sharey)
    if isinstance(raw_axes, Axes):
        return figure, (raw_axes,)
    flattened = tuple(raw_axes.flat)
    if not all(isinstance(axis, Axes) for axis in flattened):
        raise RuntimeError("Matplotlib returned an invalid axes layout")
    return figure, cast(tuple[Axes, ...], flattened)


def new_figure(
    *,
    figsize: tuple[float, float],
    layout: str | None = None,
) -> Figure:
    return pyplot.figure(figsize=figsize, layout=layout)


def close_figure(figure: Figure) -> None:
    pyplot.close(figure)


def diverging_norm(*, vmin: float, vcenter: float, vmax: float) -> TwoSlopeNorm:
    return TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)


def legend_patch(
    *,
    facecolor: str,
    alpha: float,
    label: str,
) -> Patch:
    return Patch(facecolor=facecolor, alpha=alpha, label=label)


def close_figures(figures: Sequence[Figure]) -> None:
    """Close several figures after a multi-artifact generation phase."""
    for figure in figures:
        close_figure(figure)


__all__ = [
    "Axes",
    "Figure",
    "axes_row",
    "close_figure",
    "close_figures",
    "diverging_norm",
    "legend_patch",
    "new_figure",
    "single_axes",
    "use_style",
]
