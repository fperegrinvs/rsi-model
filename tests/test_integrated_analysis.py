"""Focused tests for the r4.0 analysis layer.

These pin the analysis layer to the declared central architecture: the
frontier's f = 1 point must coincide with the canonical aggregate-doubling
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

from rsimodel.integrated import (load_integrated_params, seed_ensemble,
                             simulate_capacity_growth, size_seed)
from rsimodel.integrated_analysis import (ablation_suite,
                                      allocation_repair_suite,
                                      capacity_regime_summary,
                                      ensemble_diagnostics,
                                      environment_effect_suite,
                                      electronics_architecture_suite,
                                      import_stock_composition,
                                      infeasibility_certificate,
                                      knowledge_regime_suite,
                                      material_limited_steps,
                                      oversize_frontier,
                                      pareto_seed_designs,
                                      policy_robustness_sweep,
                                      simulate_symmetric_economics,
                                      terminal_endpoints)


@pytest.fixture(scope="module")
def params():
    return load_integrated_params()


@pytest.fixture(scope="module")
def bridge(params):
    seed = size_seed(params, "lunar_strategic_material_bridge")
    run = simulate_capacity_growth(params, seed)
    return seed, run


def test_initial_cells_default_is_identity(params, bridge):
    seed, run = bridge
    again = simulate_capacity_growth(params, seed, initial_cells=1.0)
    assert np.array_equal(run.operating_cells, again.operating_cells)
    assert run.aggregate_doubling_year == again.aggregate_doubling_year


def test_frontier_f1_matches_canonical_metric(params):
    seed = size_seed(params, "moon_asteroid_network")
    run = simulate_capacity_growth(params, seed)
    rows = oversize_frontier(params, "moon_asteroid_network",
                             factors=(1.0, 2.0))
    assert rows[0].oversize_factor == 1.0
    assert rows[0].time_to_one_additional_cell == run.aggregate_doubling_year
    assert rows[0].installed_mass_t == pytest.approx(seed.total_seed_mass_t)
    # The cohort-resolved baseline reaches one additional cell; a larger
    # installed seed remains a distinct, heavier point on the frontier.
    assert rows[1].installed_mass_t > rows[0].installed_mass_t
    assert rows[0].time_to_one_additional_cell is not None
    assert rows[1].time_to_one_additional_cell is not None


def test_terminal_endpoints_bridge_is_contracting(params, bridge):
    seed, run = bridge
    e = terminal_endpoints(params, seed, run)
    assert not e.retained_at_horizon
    assert not e.terminal_window_expanding  # contracting over the last 5 yr


def test_import_stock_composition_sums_to_stock(params, bridge):
    seed, run = bridge
    rows = import_stock_composition(params, seed, run)
    assert rows
    total = sum(r.initial_stock_t for r in rows)
    assert total == pytest.approx(float(seed.import_stock_mass_t), rel=1e-9)
    assert sum(r.share_of_import_stock for r in rows) == pytest.approx(1.0)


def test_ablations_expose_material_and_coupling_regimes(params, bridge):
    seed, run = bridge
    limited, steps = material_limited_steps(params, seed, run)
    assert limited > 0.8 * steps
    bridge_rows = ablation_suite(params, "lunar_strategic_material_bridge")
    frozen = next(
        r for r in bridge_rows if r.variant == "seed_sized_at_base_autonomy"
    )
    assert not frozen.feasible  # bridge needs its declared AI-enabled coverage

    network_rows = ablation_suite(params, "moon_asteroid_network")
    baseline = next(r for r in network_rows if r.variant == "baseline")
    uncoupled = next(r for r in network_rows if r.variant == "fully_uncoupled")
    assert baseline.operating_at_horizon > uncoupled.operating_at_horizon
    assert uncoupled.growth_share_of_baseline < 0.7


def test_capacity_regime_counts_are_exhaustive(params, bridge):
    seed, run = bridge
    summary = capacity_regime_summary(params, seed, run)
    assert (
        summary.material_limited
        + summary.service_limited
        + summary.order_rate_limited
        == summary.total_steps
    )
    assert summary.material_limited == 146


def test_allocation_repair_suite_exposes_policy_and_recovery(params):
    rows = allocation_repair_suite(
        params,
        "lunar_strategic_material_bridge",
    )
    assert len(rows) == 4
    balanced = rows[0]
    independent = rows[1]
    repair = rows[2]
    shock = rows[3]
    assert independent.policy == "maximin_sector"
    assert independent.operating_at_horizon > balanced.operating_at_horizon
    assert repair.cumulative_repaired_capacity > 0.0
    assert shock.shock != "none"
    assert shock.shock_recovery_year is not None


def test_named_operational_regimes_are_reachable(params):
    rows = {
        row.variant: row
        for row in knowledge_regime_suite(params, "moon_asteroid_network")
    }
    assert rows["communication_outage_years10_12"].autonomy_steps > 0
    assert rows["verification_outage_years10_12"].verification_steps > 0
    assert rows["compute_outage_years10_12"].compute_steps > 0
    assert (
        rows["repair_after_advanced_logic_90pct_loss_year5"].repair_steps
        > 0
    )


def test_environment_effects_change_binding_and_feasibility(params):
    rows = environment_effect_suite(
        params,
        "lunar_strategic_material_bridge",
    )
    identity, nominal, adverse = rows
    assert identity.feasible and nominal.feasible
    assert nominal.seed_mass_t > identity.seed_mass_t
    assert nominal.top_binding_constraint != identity.top_binding_constraint
    assert not adverse.feasible


def test_policy_robustness_sweep_covers_declared_dimensions(params):
    rows = policy_robustness_sweep(
        params,
        "lunar_strategic_material_bridge",
    )
    assert len(rows) == 95
    assert {r.sweep_dimension for r in rows} == {
        "knockout_fraction",
        "event_time_year",
        "horizon_years",
        "retained_import_stock_fraction",
        "initial_surplus_cells",
        "obsolescence_multiplier",
    }
    assert {r.policy for r in rows} == {
        "balanced",
        "maximin_sector",
        "surplus_preserving",
        "shock_aware",
        "perfect_foresight",
    }
    assert any(r.survived and r.terminal_window_expanding for r in rows)


def test_electronics_architectures_track_shelf_life_and_tier_shortfalls(params):
    rows = electronics_architecture_suite(
        params,
        "moon_asteroid_network",
    )
    assert len(rows) == 4 * 7
    assert {r.architecture for r in rows} == {
        "frontier_local",
        "permanent_import",
        "mature_repairable",
        "cannibalization_based",
    }
    assert any(r.expired_inventory_capacity > 0.0 for r in rows)
    assert any(r.imported_mass_t > 0.0 for r in rows)
    assert all(r.measurement_priority for r in rows)
    failed_tiers = {r.tier for r in rows if not r.viable}
    assert "advanced_logic_memory" in failed_tiers
    assert "process_equipment_metrology" in failed_tiers


def test_symmetric_economics_can_block_physical_capacity(params):
    seed = size_seed(params, "moon_asteroid_network")
    run = simulate_capacity_growth(params, seed)
    commodity = simulate_symmetric_economics(
        params,
        seed,
        run,
        "commodity_compute",
    )
    native = simulate_symmetric_economics(
        params,
        seed,
        run,
        "space_native_services",
    )
    assert commodity.technical_space_capacity[-1] > 1.0
    assert (
        commodity.funded_space_capacity[-1]
        < commodity.technical_space_capacity[-1]
    )
    assert commodity.earth_capacity[-1] > commodity.funded_space_capacity[-1]
    assert commodity.space_finance_constrained_steps > 0
    assert (
        native.funded_space_capacity[-1]
        > commodity.funded_space_capacity[-1]
    )


def test_pareto_search_changes_routes_sources_and_marks_frontier(params):
    rows = pareto_seed_designs(params)
    assert len(rows) == 3 * 4 * 3
    assert len({r.route for r in rows}) == 3
    assert len({r.redundancy for r in rows}) == 4
    assert len({r.source_portfolio for r in rows}) == 3
    frontier = [r for r in rows if r.non_dominated]
    assert frontier
    assert any(r.robust_candidate for r in frontier)
    assert any(r.source_portfolio == "asteroid_reserve" for r in frontier)
    assert any(r.route == "mature_node" for r in frontier)


def test_diagnostics_reproduce_ensemble_counts(params):
    d = ensemble_diagnostics(
        params, "lunar_strategic_material_bridge", n_runs=200,
                             seed=404, years=40.0, dt=0.5)
    e = seed_ensemble(
        params, "lunar_strategic_material_bridge", n_runs=200, seed=404,
                      years=40.0, dt=0.5)
    assert d.n_feasible == e.n_feasible
    assert sum(d.failure_histogram.values()) == 200 - e.n_feasible


def test_strict_lunar_certificate_is_material_cut(params):
    rows = infeasibility_certificate(params, "lunar_strict")
    assert rows
    assert all(r.constraint.startswith("element:") for r in rows)
    assert all(r.minimum_violation > 0 for r in rows)
    # A feasible scenario yields an empty certificate.
    assert infeasibility_certificate(
        params, "lunar_strategic_material_bridge"
    ) == ()
