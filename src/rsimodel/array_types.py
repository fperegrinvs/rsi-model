"""Shared NumPy dtype aliases; runtime code still validates dimensions and shapes."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

type FloatArray = NDArray[np.float64]
type IntArray = NDArray[np.int64]
type Int32Array = NDArray[np.int32]
type BoolArray = NDArray[np.bool_]
type ShapeSpec = tuple[int | None, ...]


def validate_shape[ArrayT: (FloatArray, IntArray, Int32Array, BoolArray)](
    array: ArrayT,
    shape: ShapeSpec,
    *,
    name: str,
) -> ArrayT:
    """Fail closed when a typed numerical array has the wrong dimensionality.

    ``None`` marks a dimension whose length is intentionally unconstrained.
    Dtype aliases help the static checker; this runtime check protects the
    shape relationships that the type system cannot express.
    """
    if array.ndim != len(shape):
        raise ValueError(f"{name}: expected {len(shape)} dimensions, got {array.ndim}")
    mismatches = [
        (axis, expected, actual)
        for axis, (expected, actual) in enumerate(zip(shape, array.shape, strict=True))
        if expected is not None and actual != expected
    ]
    if mismatches:
        expected_text = "×".join("*" if value is None else str(value) for value in shape)
        actual_text = "×".join(str(value) for value in array.shape)
        raise ValueError(f"{name}: expected shape {expected_text}, got {actual_text}")
    return array


__all__ = [
    "BoolArray",
    "FloatArray",
    "Int32Array",
    "IntArray",
    "ShapeSpec",
    "validate_shape",
]
