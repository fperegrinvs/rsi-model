"""Allocation-policy robustness: is the electronics/location story an artifact
of the myopic one-step maximin LP?

The concern (external review): a myopic maximin allocator may under-invest in
future capacity (power, machine tools, stockpiles) that a forward-looking
operator would build. Because the dynamics K_{t+1} = K_t + dt(x_t + u_t -
delta K_t) and all balances are linear, a multi-period lookahead is an exact
LP, not an approximation — so the comparison is clean.

Policies:
- 'myopic'    — the model's lexicographic one-step maximin (allocate_step).
- 'horizon'   — receding-horizon maximin: solve an H-step LP maximizing the
                worst-case sector growth over the whole window, apply the
                first step, roll forward. Deterministic lookahead (imports
                known; shocks unforeseen).
- 'aggregate' — maximize total capacity growth subject to no sector
                shrinking; falls back to myopic maximin when the floor is
                infeasible (decline regimes).

Comparison metric is the *realized* worst-case growth min_j dK_j/K_j, computed
identically for every policy, so P(expanding) is apples-to-apples. The
binding-sector diagnostic is the SAME unit-invariant one-percent finite
response as model.run — evaluated at the current state
(a state property, independent of which policy produced the state) — so the
policy table tests whether the manuscript's binding-sector classification
survives alternative policies, not a different statistic (review correction:
this previously used argmin dK_j/K_j, which is a different concept).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .array_types import BoolArray, FloatArray, IntArray
from .model import (
    AllocationAction,
    Params,
    RunResult,
    allocate_step,
    imports_at,
    recoverable_retirement,
    replacement_demand,
)
from .solver_adapter import solve_linear_program


def _horizon_step(
    p: Params,
    K: FloatArray,
    S: FloatArray,
    t: float,
    dt: float,
    H: int,
    cutoff_year: float | None,
    cutoff_idx: IntArray | None,
) -> AllocationAction | None:
    """Solve the H-step lookahead LP; return first-step action, or None if the
    solver fails (caller falls back to myopic)."""
    n = p.n
    iw, ir = p.idx("recycling"), p.idx("repair")
    nx = 3 * n + 1  # x, u, d, w per step
    nv = H * nx + H * n + H * n + 1  # + K_1..K_H, S_1..S_H, g

    def xi(s: int, j: int) -> int:
        return s * nx + j  # x_{s,j}

    def ui(s: int, j: int) -> int:
        return s * nx + n + j  # u_{s,j}

    def di(s: int, j: int) -> int:
        return s * nx + 2 * n + j  # d_{s,j}

    def wi(s: int) -> int:
        return s * nx + 3 * n  # w_s

    def Ki(s: int, j: int) -> int:
        return H * nx + (s - 1) * n + j  # K_{s,j}, s = 1..H

    def Si(s: int, j: int) -> int:
        return H * nx + H * n + (s - 1) * n + j

    gi = nv - 1

    def Kcol(s: int, j: int) -> tuple[int | None, float]:
        """(coeff-array index, fixed-part) for K_{s,j}: s=0 is a constant."""
        return (None, float(K[j])) if s == 0 else (Ki(s, j), 0.0)

    def Scol(s: int, j: int) -> tuple[int | None, float]:
        return (None, float(S[j])) if s == 0 else (Si(s, j), 0.0)

    equality_rows: list[FloatArray] = []
    equality_rhs: list[float] = []
    inequality_rows: list[FloatArray] = []
    inequality_rhs: list[float] = []
    delta, wear = p.delta, p.wear
    # import schedules over the window (deterministic lookahead)
    direct_imports: list[FloatArray] = []
    stock_inflows: list[FloatArray] = []
    next_pulse = (
        (0.0 if t <= 1e-12 else np.ceil(t / p.pulse_years) * p.pulse_years)
        if p.pulse_years is not None
        else None
    )
    for s in range(H):
        ts = t + s * dt
        m = imports_at(p, ts, cutoff_year, cutoff_idx)
        m_stock = np.where(p.stockable, m, 0.0)
        direct_imports.append(m - m_stock)
        if p.pulse_years is None:
            stock_inflows.append(m_stock * dt)
        else:
            inf = np.zeros(n)
            if next_pulse is not None and ts + dt > next_pulse - 1e-9:
                inf = m_stock * p.pulse_years
                next_pulse += p.pulse_years
            stock_inflows.append(inf)

    for s in range(H):
        # capacity dynamics: K_{s+1} - K_s - dt(x_s + u_s - delta K_s) = 0
        for j in range(n):
            row = np.zeros(nv)
            row[Ki(s + 1, j)] = 1.0
            ci, cfix = Kcol(s, j)
            fixed = 0.0
            if ci is None:
                fixed -= (1.0 - dt * delta[j]) * cfix
            else:
                row[ci] -= 1.0 - dt * delta[j]
            row[xi(s, j)] = -dt
            row[ui(s, j)] = -dt
            equality_rows.append(row)
            equality_rhs.append(-fixed)
        # stock dynamics: S_{s+1} - (1 - dt/shelf) S_s + dt d_s = inflow_s
        for j in range(n):
            row = np.zeros(nv)
            row[Si(s + 1, j)] = 1.0
            keep = 1.0 - dt / p.shelf_life[j]
            ci, cfix = Scol(s, j)
            fixed = float(stock_inflows[s][j])
            if ci is None:
                fixed += keep * cfix
            else:
                row[ci] -= keep
            row[di(s, j)] = dt
            equality_rows.append(row)
            equality_rhs.append(fixed)
        # wear cap: u_{s,j} <= wear_j K_{s,j}
        for j in range(n):
            row = np.zeros(nv)
            row[ui(s, j)] = 1.0
            ci, cfix = Kcol(s, j)
            rhs = wear[j] * cfix if ci is None else 0.0
            if ci is not None:
                row[ci] = -wear[j]
            inequality_rows.append(row)
            inequality_rhs.append(float(rhs))
        # drawdown bound: dt * d_{s,j} <= S_{s,j}
        for j in range(n):
            row = np.zeros(nv)
            row[di(s, j)] = dt
            ci, cfix = Scol(s, j)
            rhs = cfix if ci is None else 0.0
            if ci is not None:
                row[ci] = -1.0
            inequality_rows.append(row)
            inequality_rhs.append(float(rhs))
        # material balance at step s
        for i in range(n):
            row = np.zeros(nv)
            for j in range(n):
                row[xi(s, j)] += p.A[i, j]
                row[ui(s, j)] += p.repair_spares_fraction * p.A[i, j]
            if i == ir:
                for j in range(n):
                    row[ui(s, j)] += 1.0 / p.repair_eff
            row[wi(s)] += (1.0 if i == iw else 0.0) + p.recycle_opex[i] - p.recycle_profile[i]
            row[di(s, i)] -= 1.0
            ci, cfix = Kcol(s, i)
            rhs = float(direct_imports[s][i] + (p.q[i] * cfix if ci is None else 0.0))
            if ci is not None:
                row[ci] = -p.q[i]
            inequality_rows.append(row)
            inequality_rhs.append(rhs)
        # Scrap cap: only physically recoverable retirement components enter.
        row = np.zeros(nv)
        row[wi(s)] = 1.0
        rhs = 0.0
        recoverable_delta = sum(
            (p.salvage_factors[comp] * delta_comp for comp, delta_comp in p.delta_comps.items()),
            start=np.zeros(n, dtype=float),
        )
        for j in range(n):
            row[ui(s, j)] = p.scrap_recovery * p.salvage_factors["wear"][j]
            ci, cfix = Kcol(s, j)
            if ci is None:
                rhs += p.scrap_recovery * recoverable_delta[j] * cfix
            else:
                row[ci] -= p.scrap_recovery * recoverable_delta[j]
        inequality_rows.append(row)
        inequality_rhs.append(float(rhs))
        # stock capacity: S_{s+1,j} <= cap_years * (A @ (delta K_{s+1}))_j
        for j in range(n):
            if not p.stockable[j]:
                continue
            row = np.zeros(nv)
            row[Si(s + 1, j)] = 1.0
            for k in range(n):
                row[Ki(s + 1, k)] -= p.stock_capacity_years * p.A[j, k] * delta[k]
            inequality_rows.append(row)
            inequality_rhs.append(0.0)

    # objective: maximize g with K_{H,j} >= K0_j (1 + g T)
    T = H * dt
    for j in range(n):
        row = np.zeros(nv)
        row[Ki(H, j)] = -1.0
        row[gi] = T * K[j]
        inequality_rows.append(row)
        inequality_rhs.append(-float(K[j]))
    c = np.zeros(nv)
    c[gi] = -1.0
    bounds: list[tuple[float | None, float | None]] = [(0.0, None) for _ in range(nv - 1)]
    bounds.append((None, None))
    # non-stockable sectors cannot draw
    for s in range(H):
        for j in range(n):
            if not p.stockable[j]:
                bounds[di(s, j)] = (0, 0)
    res = solve_linear_program(
        c,
        a_ub=np.asarray(inequality_rows, dtype=float),
        b_ub=np.asarray(inequality_rhs, dtype=float),
        a_eq=np.asarray(equality_rows, dtype=float),
        b_eq=np.asarray(equality_rhs, dtype=float),
        bounds=bounds,
    )
    if not res.success:
        return None
    z = res.x
    return {
        "x": z[[xi(0, j) for j in range(n)]],
        "u": z[[ui(0, j) for j in range(n)]],
        "w": float(z[wi(0)]),
        "d": z[[di(0, j) for j in range(n)]],
    }


def _aggregate_step(
    p: Params, K: FloatArray, m_direct: FloatArray, stock_avail: FloatArray
) -> AllocationAction | None:
    """Maximize total dK subject to dK_j >= 0; None if the floor is infeasible."""
    n = p.n
    iw, ir = p.idx("recycling"), p.idx("repair")
    nv = 3 * n + 1
    sx, su, swv, sd = 0, n, 2 * n, 2 * n + 1
    c = np.zeros(nv)
    c[sx : sx + n] = -1.0
    c[su : su + n] = -1.0
    rows: list[FloatArray] = []
    rhs: list[float] = []
    for j in range(n):  # floor: x_j + u_j >= delta_j K_j
        r = np.zeros(nv)
        r[sx + j] = -1.0
        r[su + j] = -1.0
        rows.append(r)
        rhs.append(-float(p.delta[j] * K[j]))
    for j in range(n):  # wear cap
        r = np.zeros(nv)
        r[su + j] = 1.0
        rows.append(r)
        rhs.append(float(p.wear[j] * K[j]))
    supply = p.q * K + m_direct
    for i in range(n):
        r = np.zeros(nv)
        r[sx : sx + n] = p.A[i]
        r[su : su + n] = p.repair_spares_fraction * p.A[i]
        if i == ir:
            r[su : su + n] += 1.0 / p.repair_eff
        if i == iw:
            r[swv] += 1.0
        r[swv] += p.recycle_opex[i] - p.recycle_profile[i]
        r[sd + i] = -1.0
        rows.append(r)
        rhs.append(float(supply[i]))
    r = np.zeros(nv)
    r[swv] = 1.0
    r[su : su + n] = p.scrap_recovery * p.salvage_factors["wear"]
    rows.append(r)
    rhs.append(p.scrap_recovery * recoverable_retirement(p, K))
    bounds: list[tuple[float | None, float | None]] = [(0.0, None)] * nv
    for i in range(n):
        bounds[sd + i] = (0, float(stock_avail[i]) if p.stockable[i] else 0.0)
    res = solve_linear_program(
        c,
        a_ub=np.asarray(rows, dtype=float),
        b_ub=np.asarray(rhs, dtype=float),
        bounds=bounds,
    )
    if not res.success:
        return None
    z = res.x
    return {
        "x": z[sx : sx + n],
        "u": z[su : su + n],
        "w": float(z[swv]),
        "d": z[sd : sd + n],
    }


def run_policy(
    p: Params,
    policy: str = "myopic",
    K0: FloatArray | None = None,
    years: float = 40.0,
    dt: float = 0.25,
    horizon_steps: int = 12,
    cutoff_year: float | None = None,
    cutoff_sectors: list[str] | None = None,
    rng: np.random.Generator | None = None,
) -> RunResult:
    """model.run with a pluggable allocation policy. g is the REALIZED
    worst-case growth min_j dK_j / K_j (identical across policies); the
    binding sector is the model's one-percent response diagnostic evaluated at the current
    state via allocate_step — the same definition as model.run, so binding
    histograms are comparable across the baseline and every policy."""
    n = p.n
    capacity = np.full(n, 1.0) if K0 is None else K0.astype(float).copy()
    initial_capacity = capacity.copy()
    cutoff_idx = (
        None if cutoff_sectors is None else np.array([p.idx(s) for s in cutoff_sectors], int)
    )
    stock = np.where(
        p.stockable,
        p.stock_initial_years * replacement_demand(p, capacity),
        0.0,
    )
    steps = round(years / dt)
    times: list[float] = []
    capacities: list[FloatArray] = []
    realized_growth: list[float] = []
    allocated_growth: list[float] = []
    binding_sectors: list[int] = []
    co_binding_masks: list[BoolArray] = []
    stock_history: list[FloatArray] = []
    shock_log: list[tuple[float, str, float]] = []
    next_pulse = 0.0
    for s_i in range(steps):
        t = s_i * dt
        m = imports_at(p, t, cutoff_year, cutoff_idx)
        m_stock = np.where(p.stockable, m, 0.0)
        m_direct = m - m_stock
        if p.pulse_years is None:
            inflow = m_stock * dt
        else:
            inflow = np.zeros(n)
            if t + dt > next_pulse - 1e-9:
                inflow = m_stock * p.pulse_years
                next_pulse += p.pulse_years

        a: AllocationAction | None = None
        if policy == "horizon":
            a = _horizon_step(
                p,
                capacity,
                stock,
                t,
                dt,
                horizon_steps,
                cutoff_year,
                cutoff_idx,
            )
        elif policy == "aggregate":
            a = _aggregate_step(p, capacity, m_direct, stock / dt)
        elif policy != "myopic":
            raise ValueError(f"unknown allocation policy {policy!r}")
        # binding diagnostic: always the maximin LP's one-percent responses at this
        # state (same definition as model.run), regardless of acting policy
        diag = allocate_step(p, capacity, m_direct, stock / dt)
        if a is None:  # fallback / 'myopic'
            a = diag
        binding = diag["binding"]

        previous_capacity = capacity.copy()
        capacity_change = a["x"] + a["u"] - p.delta * capacity
        g_alloc = float(np.min(capacity_change / capacity))
        capacity = np.maximum(capacity + dt * capacity_change, 1e-9)
        stock = stock + inflow - a["d"] * dt - stock * dt / p.shelf_life
        if rng is not None:
            for sh in p.shocks:
                for _ in range(rng.poisson(sh.rate_per_year * dt)):
                    frac = rng.uniform(*sh.fraction_lost)
                    capacity[sh.sector_idx] *= 1.0 - frac
                    shock_log.append((t + dt, sh.name, frac))
        cap = p.stock_capacity_years * replacement_demand(p, capacity)
        stock = np.clip(
            stock,
            0.0,
            np.where(p.stockable, np.maximum(cap, 1e-9), 0.0),
        )
        g_real = float(
            np.min((capacity - previous_capacity) / (dt * np.maximum(previous_capacity, 1e-30)))
        )
        times.append(t + dt)
        capacities.append(capacity.copy())
        realized_growth.append(g_real)
        allocated_growth.append(g_alloc)
        binding_sectors.append(binding)
        co_binding_masks.append(diag["binding_mask"].copy())
        stock_history.append(stock.copy())
    return RunResult(
        np.asarray(times, dtype=float),
        np.asarray(capacities, dtype=float),
        np.asarray(realized_growth, dtype=float),
        np.asarray(binding_sectors, dtype=np.int64),
        np.asarray(stock_history, dtype=float),
        shock_log,
        g_alloc=np.asarray(allocated_growth, dtype=float),
        co_binding=np.asarray(co_binding_masks, dtype=bool),
        params=p,
        K0=initial_capacity,
    )


@dataclass
class PolicyComparison:
    set_name: str
    environment: str
    n_runs: int
    # policy -> (n_expanding, share, top limiting sector, its share of steps)
    results: dict[str, tuple[int, float, str, float]]


def compare_policies(
    set_name: str,
    env: str,
    policies: tuple[str, ...] = ("myopic", "horizon", "aggregate"),
    n_runs: int = 30,
    years: float = 32.0,
    horizon: float = 30.0,
    dt: float = 0.5,
    horizon_steps: int = 12,
    q_spread: float = 0.10,
    seed: int = 0,
) -> PolicyComparison:
    """Same sampled draws for every policy (paired comparison, shocks off)."""
    from .montecarlo import sample_params

    if n_runs <= 0:
        raise ValueError("n_runs must be positive")
    out: dict[str, tuple[int, float, str, float]] = {}
    for pol in policies:
        rng = np.random.default_rng(seed)  # reset: identical draws per policy
        expanding = 0
        binding_counts: FloatArray | None = None
        base: Params | None = None
        for _ in range(n_runs):
            p = sample_params(set_name, env, rng, q_spread)
            base = p
            r = run_policy(p, policy=pol, years=years, dt=dt, horizon_steps=horizon_steps)
            if r.self_expanding_at(horizon):
                expanding += 1
            if r.co_binding is None:
                raise RuntimeError("policy run did not return co-binding diagnostics")
            co = np.asarray(r.co_binding, float)
            credits = np.sum(co / np.maximum(co.sum(axis=1, keepdims=True), 1.0), axis=0)
            binding_counts = credits if binding_counts is None else binding_counts + credits
        if binding_counts is None or base is None:
            raise RuntimeError("positive n_runs produced no policy result")
        counts = binding_counts
        top = int(np.argmax(counts))
        out[pol] = (expanding, expanding / n_runs, base.sectors[top], counts[top] / counts.sum())
    return PolicyComparison(set_name, env, n_runs, out)
