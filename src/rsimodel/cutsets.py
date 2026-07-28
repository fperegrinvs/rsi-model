"""Minimum-cut-set analysis over the A matrix + import profile.

The review requirement: closure kappa is a VECTOR, and feasibility statements
must name the minimal sets of external dependencies whose loss kills
self-expansion — not report a scalar closure fraction.

Two probes:
- import cut sets: minimal subsets of import lines (sectors with
  import_profile > 0) whose permanent loss (cutoff at t=0) prevents
  self-expansion by the horizon. Monotone (more cutting never helps), so the
  subset lattice is enumerated by size with superset pruning.
- indispensable sectors: sectors whose near-total capacity knockout at t=0 the
  system cannot rebuild its way out of by the horizon.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from .model import Params, load_params, run


@dataclass
class CutSetResult:
    baseline_expanding: bool
    minimal_cuts: list[tuple[str, ...]]   # minimal import cut sets, by name
    indispensable: list[str]              # capacity-knockout failures
    horizon: float
    n_sims: int


def _expands(p: Params, horizon: float, dt: float,
             cutoff_sectors: list[str] | None = None,
             K0: np.ndarray | None = None) -> bool:
    r = run(p, K0=K0, years=horizon + 2 * dt, dt=dt,
            cutoff_year=(0.0 if cutoff_sectors is not None else None),
            cutoff_sectors=cutoff_sectors)
    return r.self_expanding_at(horizon)


def find_cut_sets(p: Params, horizon: float = 30.0, dt: float = 0.5,
                  max_size: int | None = None) -> CutSetResult:
    imported = [s for s, w in zip(p.sectors, p.import_profile) if w > 0]
    n_sims = 1
    baseline = _expands(p, horizon, dt)
    minimal: list[tuple[str, ...]] = []
    if baseline:
        top = len(imported) if max_size is None else min(max_size, len(imported))
        for size in range(1, top + 1):
            for combo in combinations(imported, size):
                if any(set(c) <= set(combo) for c in minimal):
                    continue  # superset of a known cut: cut by monotonicity, not minimal
                n_sims += 1
                if not _expands(p, horizon, dt, cutoff_sectors=list(combo)):
                    minimal.append(combo)

    indispensable = []
    for j, name in enumerate(p.sectors):
        K0 = np.ones(p.n)
        K0[j] = 1e-6
        n_sims += 1
        if not _expands(p, horizon, dt, K0=K0):
            indispensable.append(name)

    return CutSetResult(baseline, minimal, indispensable, horizon, n_sims)


@dataclass
class RetoolingResult:
    """Part IV's promised output: retooling speed as a first-class metric
    alongside doubling time (Scenario 3, paradigm-shift stranding).

    A fraction of one sector's capacity is destroyed at t0 (the stranded-fab
    scenario); the maximin allocator then reallocates. Because the allocator
    maximizes *relative* worst-case growth, sector proportions are maintained
    rather than rebuilt, so the honest system-level metrics are:
    knocked_share — fraction of total capacity destroyed; stall_years — how
    long the worst-case growth rate stays negative after the knockout;
    years_lost — the integrated worst-case-growth deficit versus the
    unknocked counterfactual continuation, expressed in years at the
    terminal growth rate: (∫g_cf − ∫g_knocked) / g_cf(T). Measured on the
    g-trajectories, which the LP objective pins uniquely, rather than on
    total capacity, which is polluted by surplus-build vertex indeterminacy
    (pinning surplus would need a third lexicographic stage — flagged in
    ROADMAP). years_lost=None = MODEL-FATAL, a horizon-relative label: the
    knocked system's worst-case growth has not returned positive within the
    tested horizon while the counterfactual's stays positive. It is NOT a
    proof of permanent impossibility — a longer horizon, different import
    policy, plant design, or initial surplus could change the outcome.
    Deterministic dynamics (no shocks) for clean measurement; the import ramp
    is time-shifted exactly via its memoryless exponential (Mars pulse phase
    is approximated by restarting the synodic clock at the knockout)."""
    set_name: str
    environment: str
    sector: str
    knock_fraction: float
    t0: float
    knocked_share: float
    stall_years: float
    years_lost: float | None   # None = model-fatal: no rejoin within tested horizon
    policy: str = "myopic"


def retooling_time(set_name: str = "central", env: str = "lunar",
                   sector: str = "electronics", knock_fraction: float = 0.9,
                   t0: float = 10.0, horizon: float = 20.0,
                   dt: float = 0.25, policy: str = "myopic") -> RetoolingResult:
    """policy='myopic' uses the model's one-step maximin; policy='horizon'
    uses the receding-horizon allocator (policies.py). Sector stranding is
    the one case where the two are expected to differ: restoring a destroyed
    sector is an investment whose payoff the myopic objective cannot see."""
    from dataclasses import replace as dc_replace

    from .policies import run_policy

    p = load_params(set_name, env=env)
    pre = run(p, years=t0, dt=dt)
    K_pre = pre.K[-1].copy()
    j = p.idx(sector)
    K0 = K_pre.copy()
    K0[j] *= (1.0 - knock_fraction)
    # exponential import ramp is memoryless: offsetting t0 = scaling budget0
    p2 = dc_replace(p, import_budget0=p.import_budget0
                    * float(np.exp(-t0 / p.import_decay_years)))
    r = run_policy(p2, policy=policy, K0=K0, years=horizon, dt=dt)
    cf = run_policy(p2, policy=policy, K0=K_pre.copy(), years=horizon, dt=dt)
    neg = r.g < 0
    stall = float(np.argmin(neg) * dt) if neg[0] else 0.0
    if neg.all():
        stall = float(horizon)
    knocked_share = float(knock_fraction * K_pre[j] / K_pre.sum())
    # fatal only relative to the counterfactual: it grows while the knocked
    # system declines (both declining = systemic late-time aging, not damage)
    if cf.g[-1] > 0 and r.g[-1] <= 0:
        years_lost = None
    else:
        deficit = float(np.sum(cf.g - r.g) * dt)   # terminal log-gap, worst case
        tail = max(1, int(round(2.0 / dt)))
        g_ref = float(np.mean(cf.g[-tail:]))       # denominator: recent cf growth
        years_lost = max(0.0, deficit / g_ref) if g_ref > 1e-4 else None
    return RetoolingResult(set_name, env, sector, knock_fraction, t0,
                           knocked_share, stall, years_lost, policy)


@dataclass
class CutProbability:
    """Cut-set fatality over the MC ensemble, not just at central anchor values.

    Cut sets appear only near the feasibility margin, so the central-value
    answer ('no import line is load-bearing') understates dependency risk;
    this reports, per candidate cut, P(fatal | baseline would have expanded).
    """
    label: str
    environment: str
    n_runs: int
    horizon: float
    p_baseline: float                       # P(expanding with imports on ramp)
    p_fatal: dict[tuple[str, ...], float]   # candidate -> P(fatal | baseline ok)


def cut_probability(set_name: str = "central", env: str = "lunar",
                    n_runs: int = 30, horizon: float = 30.0, dt: float = 0.5,
                    candidates: list[tuple[str, ...]] | None = None,
                    q_spread: float = 0.10, seed: int = 0) -> CutProbability:
    """Sampled-anchor cut analysis. Deterministic dynamics per draw (no shocks):
    this isolates the structural dependency question from event noise."""
    from .montecarlo import sample_params

    rng = np.random.default_rng(seed)
    p0 = load_params(set_name, env=env)
    imported = tuple(s for s, w in zip(p0.sectors, p0.import_profile) if w > 0)
    if candidates is None:
        candidates = [(s,) for s in imported] + [imported]

    n_base = 0
    fatal = {tuple(c): 0 for c in candidates}
    for _ in range(n_runs):
        p = sample_params(set_name, env, rng, q_spread)
        if not _expands(p, horizon, dt):
            continue
        n_base += 1
        for c in candidates:
            if not _expands(p, horizon, dt, cutoff_sectors=list(c)):
                fatal[tuple(c)] += 1
    p_fatal = {c: (k / n_base if n_base else float("nan"))
               for c, k in fatal.items()}
    return CutProbability(set_name, env, n_runs, horizon,
                          n_base / n_runs, p_fatal)
