"""Typed boundary around SciPy, OSQP, and SciPy's bundled HiGHS binding.

The scientific libraries intentionally expose flexible, partly dynamic APIs.
Model modules consume only the stable records and methods defined here, so
unknown third-party types cannot propagate into model calculations.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from importlib import import_module
from importlib.metadata import version
from typing import Any, Protocol, cast, overload

import numpy as np

from .array_types import FloatArray, Int32Array, IntArray

type Bound = tuple[float | None, float | None]

_OSQP: Any = import_module("osqp")
_SCIPY_OPTIMIZE: Any = import_module("scipy.optimize")
_SCIPY_SPARSE: Any = import_module("scipy.sparse")
_SCIPY_STATS: Any = import_module("scipy.stats")


class SparseMatrix(Protocol):
    """Sparse operations used by the allocation solvers."""

    data: FloatArray
    indices: IntArray
    indptr: IntArray

    @overload
    def __matmul__(self, other: FloatArray, /) -> FloatArray: ...

    @overload
    def __matmul__(self, other: SparseMatrix, /) -> SparseMatrix: ...

    def tocsr(self) -> SparseMatrix: ...


@dataclass(frozen=True, slots=True)
class LinearProgramResult:
    success: bool
    x: FloatArray
    message: str
    inequality_marginals: FloatArray | None


@dataclass(frozen=True, slots=True)
class QuadraticProgramResult:
    x: FloatArray
    status: str
    status_value: int


@dataclass(frozen=True, slots=True)
class MinimizeResult:
    success: bool
    x: FloatArray
    message: str


@dataclass(frozen=True, slots=True)
class HighsSolution:
    columns: FloatArray
    row_duals: FloatArray


def sparse_csc(values: object) -> SparseMatrix:
    """Construct a CSC matrix and narrow its public array surface."""
    return cast(SparseMatrix, _SCIPY_SPARSE.csc_matrix(values))


def sparse_diagonal(values: FloatArray) -> SparseMatrix:
    return cast(SparseMatrix, _SCIPY_SPARSE.diags(values, format="csc"))


def sparse_identity(size: int) -> SparseMatrix:
    return cast(SparseMatrix, _SCIPY_SPARSE.eye(size, format="csc"))


def sparse_vstack(matrices: Sequence[object]) -> SparseMatrix:
    return cast(SparseMatrix, _SCIPY_SPARSE.vstack(list(matrices), format="csc"))


def solve_linear_program(
    objective: FloatArray,
    *,
    a_ub: object,
    b_ub: FloatArray,
    bounds: Sequence[Bound],
    a_eq: FloatArray | None = None,
    b_eq: FloatArray | None = None,
    options: Mapping[str, object] | None = None,
) -> LinearProgramResult:
    """Run HiGHS through SciPy and return a closed, typed result."""
    raw: Any = _SCIPY_OPTIMIZE.linprog(
        objective,
        A_ub=a_ub,
        b_ub=b_ub,
        A_eq=a_eq,
        b_eq=b_eq,
        bounds=list(bounds),
        method="highs",
        options=None if options is None else dict(options),
    )
    inequality_marginals: FloatArray | None = None
    raw_inequality: Any = getattr(raw, "ineqlin", None)
    raw_marginals: Any = getattr(raw_inequality, "marginals", None)
    if raw_marginals is not None:
        inequality_marginals = np.asarray(raw_marginals, dtype=float)
    raw_x: Any = getattr(raw, "x", None)
    x = np.asarray(raw_x, dtype=float) if raw_x is not None else np.empty(0, dtype=np.float64)
    return LinearProgramResult(
        success=bool(getattr(raw, "success", False)),
        x=x,
        message=str(getattr(raw, "message", "")),
        inequality_marginals=inequality_marginals,
    )


def solve_identity_quadratic_program(
    constraint_matrix: SparseMatrix,
    lower: FloatArray,
    upper: FloatArray,
    warm_start: FloatArray,
) -> QuadraticProgramResult:
    """Minimize ``0.5 * ||x||²`` under sparse linear bounds with OSQP."""
    size = len(warm_start)
    solver: Any = _OSQP.OSQP()
    solver.setup(
        P=_SCIPY_SPARSE.eye(size, format="csc"),
        q=np.zeros(size),
        A=cast(Any, constraint_matrix),
        l=lower,
        u=upper,
        verbose=False,
        polishing=True,
        eps_abs=1e-5,
        eps_rel=1e-5,
        max_iter=4_000,
    )
    solver.warm_start(x=warm_start)
    raw: Any = solver.solve(raise_error=False)
    raw_info: Any = raw.info
    return QuadraticProgramResult(
        x=np.asarray(raw.x, dtype=float),
        status=str(raw_info.status),
        status_value=int(raw_info.status_val),
    )


def minimize_diagonal_quadratic(
    diagonal: FloatArray,
    initial: FloatArray,
    lower_bounds: FloatArray,
    upper_bounds: FloatArray,
    constraint_matrix: SparseMatrix,
    constraint_lower: FloatArray,
    constraint_upper: FloatArray,
) -> MinimizeResult:
    """SLSQP fallback for a diagonal quadratic with bounded linear rows."""

    def objective(candidate: FloatArray) -> float:
        return 0.5 * float(np.dot(diagonal, candidate * candidate))

    def gradient(candidate: FloatArray) -> FloatArray:
        return diagonal * candidate

    raw: Any = _SCIPY_OPTIMIZE.minimize(
        cast(Callable[[FloatArray], float], objective),
        initial,
        jac=cast(Callable[[FloatArray], FloatArray], gradient),
        method="SLSQP",
        bounds=_SCIPY_OPTIMIZE.Bounds(lower_bounds, upper_bounds),
        constraints=[
            _SCIPY_OPTIMIZE.LinearConstraint(
                cast(Any, constraint_matrix),
                constraint_lower,
                constraint_upper,
            )
        ],
        options={"ftol": 1e-9, "maxiter": 200},
    )
    return MinimizeResult(
        success=bool(getattr(raw, "success", False)),
        x=np.asarray(raw.x, dtype=float),
        message=str(getattr(raw, "message", "")),
    )


def spearman_correlation(left: FloatArray, right: FloatArray) -> float:
    """Return a scalar Spearman coefficient from SciPy's union-shaped API."""
    raw: Any = _SCIPY_STATS.spearmanr(left, right)
    statistic: Any = getattr(raw, "statistic", raw[0])
    return float(statistic)


def _load_highs_core() -> Any | None:
    try:
        return import_module("scipy.optimize._highspy._core")
    except Exception:  # pragma: no cover - guarded optional optimization
        return None


_HIGHS_CORE: Any | None = _load_highs_core()


def persistent_highs_available() -> bool:
    return _HIGHS_CORE is not None


def scipy_version() -> str:
    """Return the installed SciPy version without exposing its module object."""
    return version("scipy")


class PersistentLinearProgram:
    """Narrow facade over SciPy's private warm-started HiGHS interface."""

    def __init__(
        self,
        *,
        objective: FloatArray,
        column_lower: FloatArray,
        column_upper: FloatArray,
        row_lower: FloatArray,
        row_upper: FloatArray,
        matrix: SparseMatrix,
    ) -> None:
        core: Any = _HIGHS_CORE
        if core is None:
            raise RuntimeError("SciPy's bundled HiGHS interface is unavailable")
        self._core: Any = core
        self.infinity = float(core.kHighsInf)
        lp: Any = core.HighsLp()
        lp.num_col_, lp.num_row_ = len(column_lower), len(row_lower)
        lp.sense_ = core.ObjSense.kMinimize
        lp.col_cost_ = objective
        lp.col_lower_, lp.col_upper_ = column_lower, column_upper
        lp.row_lower_, lp.row_upper_ = row_lower, row_upper
        sparse: Any = core.HighsSparseMatrix()
        sparse.format_ = core.MatrixFormat.kColwise
        sparse.num_col_, sparse.num_row_ = len(column_lower), len(row_lower)
        sparse.start_ = matrix.indptr.astype(np.int32)
        sparse.index_ = matrix.indices.astype(np.int32)
        sparse.value_ = matrix.data.copy()
        lp.a_matrix_ = sparse
        self._model: Any = core._Highs()
        self._model.setOptionValue("output_flag", False)
        if self._model.passModel(lp) != core.HighsStatus.kOk:
            raise RuntimeError("HiGHS passModel failed")

    def change_coefficient(self, row: int, column: int, value: float) -> None:
        self._model.changeCoeff(row, column, value)

    def change_row_bounds(self, row: int, lower: float, upper: float) -> None:
        self._model.changeRowBounds(row, lower, upper)

    def change_column_bounds(self, column: int, lower: float, upper: float) -> None:
        self._model.changeColBounds(column, lower, upper)

    def change_costs(self, columns: Int32Array, costs: FloatArray) -> None:
        self._model.changeColsCost(len(columns), columns, costs)

    def run(self) -> None:
        self._model.run()

    def is_optimal(self) -> bool:
        return bool(self._model.getModelStatus() == self._core.HighsModelStatus.kOptimal)

    def status(self) -> str:
        value: Any = self._model.getModelStatus()
        return str(self._model.modelStatusToString(value))

    def solution(self) -> HighsSolution:
        raw: Any = self._model.getSolution()
        return HighsSolution(
            columns=np.asarray(raw.col_value, dtype=float),
            row_duals=np.asarray(raw.row_dual, dtype=float),
        )


__all__ = [
    "Bound",
    "HighsSolution",
    "LinearProgramResult",
    "MinimizeResult",
    "PersistentLinearProgram",
    "QuadraticProgramResult",
    "SparseMatrix",
    "minimize_diagonal_quadratic",
    "persistent_highs_available",
    "scipy_version",
    "solve_identity_quadratic_program",
    "solve_linear_program",
    "sparse_csc",
    "sparse_diagonal",
    "sparse_identity",
    "sparse_vstack",
    "spearman_correlation",
]
