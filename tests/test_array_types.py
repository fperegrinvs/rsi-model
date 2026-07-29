"""Runtime shape checks complement NumPy's dtype-only static aliases."""

from __future__ import annotations

import numpy as np
import pytest

from rsimodel.array_types import validate_shape


def test_validate_shape_accepts_exact_and_wildcard_dimensions() -> None:
    matrix = np.zeros((2, 3), dtype=float)
    assert validate_shape(matrix, (2, 3), name="matrix") is matrix
    assert validate_shape(matrix, (None, 3), name="matrix") is matrix


def test_validate_shape_rejects_dimension_and_axis_mismatches() -> None:
    vector = np.zeros(3, dtype=float)
    with pytest.raises(ValueError, match="expected 2 dimensions"):
        validate_shape(vector, (1, 3), name="vector")
    with pytest.raises(ValueError, match="expected shape 4"):
        validate_shape(vector, (4,), name="vector")
