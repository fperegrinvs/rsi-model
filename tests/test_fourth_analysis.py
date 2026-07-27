"""Focused tests for the r4.1 additive analysis layer.

These pin the analysis layer to the declared central architecture: the
frontier's f = 1 point must coincide with the canonical first-passage
metric, the diagnostics must reproduce the ensemble's exact feasibility
counts from the same named draws, the strict-lunar certificate must be a
nonempty material cut, and the zero-effect ablation finding must hold as
long as the central trajectories remain material-limited.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rsimodel.fourth import (load_fourth_params, seed_ensemble,
                             simulate_reproduction, size_seed)
from rsimodel.fourth_analysis import (ablation_suite, durable_endpoints,
                                      ensemble_diagnostics,
                                      infeasibility_certificate,
                                      material_limited_steps,
                                      oversize_frontier,
                                      vitamin_composition)


@pytest.fixture(scope="module")
def params():
    return load_fourth_params()


@pytest.fixture(scope="module")
def bridge(params):
    seed = size_seed(params, "lunar_vitamin_bridge")
    run = simulate_reproduction(params, seed)
    return seed, run


def test_initial_cells_default_is_identity(params, bridge):
    seed, run = bridge
    again = simulate_reproduction(params, seed, initial_cells=1.0)
    assert np.array_equal(run.operating_cells, again.operating_cells)
    assert run.second_cell_year == again.second_cell_year


def test_frontier_f1_matches_canonical_metric(params, bridge):
    seed, run = bridge
    rows = oversize_frontier(params, "lunar_vitamin_bridge",
                             factors=(1.0, 2.0))
    assert rows[0].oversize_factor == 1.0
    assert rows[0].time_to_one_additional_cell == run.second_cell_year
    assert rows[0].installed_mass_t == pytest.approx(seed.total_seed_mass_t)
    # Larger installed mass must not slow reproduction.
    assert rows[1].installed_mass_t > rows[0].installed_mass_t
    assert (rows[1].time_to_one_additional_cell
            <= rows[0].time_to_one_additional_cell)


def test_durable_endpoints_bridge_transient(params, bridge):
    seed, run = bridge
    e = durable_endpoints(params, seed, run)
    assert e.retained_at_horizon  # holds >= 2 cell-equivalents at year 40
    assert not e.durable_final5   # ...but is contracting over the last 5 yr


def test_vitamin_composition_sums_to_stock(params, bridge):
    seed, run = bridge
    rows = vitamin_composition(params, seed, run)
    assert rows
    total = sum(r.initial_stock_t for r in rows)
    assert total == pytest.approx(float(seed.vitamin_stock_mass_t), rel=1e-9)
    assert sum(r.share_of_vitamin_stock for r in rows) == pytest.approx(1.0)


def test_ablations_are_material_limited_no_ops(params, bridge):
    seed, run = bridge
    limited, steps = material_limited_steps(params, seed, run)
    assert limited == steps  # coupling multipliers never bind centrally
    rows = ablation_suite(params, "lunar_vitamin_bridge")
    base = next(r for r in rows if r.variant == "baseline")
    for r in rows:
        if r.variant in ("baseline", "seed_sized_at_base_autonomy"):
            continue
        assert r.operating_at_horizon == pytest.approx(
            base.operating_at_horizon)
        assert r.first_passage_year == base.first_passage_year
    frozen = next(r for r in rows if r.variant == "seed_sized_at_base_autonomy")
    assert not frozen.feasible  # bridge needs its declared AI-enabled coverage


def test_diagnostics_reproduce_ensemble_counts(params):
    d = ensemble_diagnostics(params, "lunar_vitamin_bridge", n_runs=200,
                             seed=404, years=40.0, dt=0.5)
    e = seed_ensemble(params, "lunar_vitamin_bridge", n_runs=200, seed=404,
                      years=40.0, dt=0.5)
    assert d.n_feasible == e.n_feasible
    assert sum(d.failure_histogram.values()) == 200 - e.n_feasible


def test_strict_lunar_certificate_is_material_cut(params):
    rows = infeasibility_certificate(params, "lunar_strict")
    assert rows
    assert all(r.constraint.startswith("element:") for r in rows)
    assert all(r.minimum_violation > 0 for r in rows)
    # A feasible scenario yields an empty certificate.
    assert infeasibility_certificate(params, "lunar_vitamin_bridge") == ()
