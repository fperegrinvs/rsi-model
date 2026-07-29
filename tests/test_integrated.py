import re
from pathlib import Path

import numpy as np
import pytest
import yaml

from rsimodel.integrated import (
    compare_compute_regimes,
    load_integrated_params,
    process_profile,
    seed_ensemble,
    simulate_capacity_growth,
    simulate_debris,
    simulate_seed_deployment,
    simulate_shell_debris,
    size_seed,
)


def test_integrated_parameter_graph_is_mass_conserving_and_decomposed() -> None:
    p = load_integrated_params()
    assert p.n == 18
    assert p.m == 17
    assert p.B.shape == (p.m, p.n)
    assert p.A.shape == (p.n, p.n)
    assert np.all(p.B >= 0) and np.all(p.A >= 0)
    assert np.all(p.B.sum(axis=0) > 0)
    assert p.lunar_yield.sum() <= 1.0
    assert p.asteroid_yield.sum() <= 1.0
    for tier in (
        "interconnects_boards",
        "passives_power",
        "sensors_control",
        "packaging_test",
        "mature_logic",
        "advanced_logic_memory",
        "process_equipment_metrology",
    ):
        assert tier in p.sectors


def test_embodiment_hardware_is_in_material_and_replacement_graphs() -> None:
    p = load_integrated_params()
    with open(
        Path(__file__).resolve().parents[1] / "params" / "integrated_model.yaml",
        encoding="utf-8",
    ) as handle:
        raw = yaml.safe_load(handle)

    sector_rows = {row["name"]: row for row in raw["sectors"]}
    sector_idx = {name: index for index, name in enumerate(p.sectors)}
    element_idx = {name: index for index, name in enumerate(p.elements)}
    base_service = raw["base_service_recipe"]
    items = raw["embodiment_bom"]["items"]

    expected_B = np.column_stack(
        [
            np.array(
                [
                    float(sector_rows[sector].get("bom_t", {}).get(element, 0.0))
                    for element in p.elements
                ]
            )
            for sector in p.sectors
        ]
    )
    expected_A = np.column_stack(
        [
            np.array(
                [
                    float(base_service.get(producer, 0.0))
                    + float(sector_rows[target].get("recipe_additions", {}).get(producer, 0.0))
                    for producer in p.sectors
                ]
            )
            for target in p.sectors
        ]
    )
    for item in items.values():
        producer = sector_idx[item["producer_sector"]]
        material = item["material_bom_t_per_target_capacity"]
        replacement = float(item["replacement_service_units_per_target_capacity_year"])
        for target_name in item["target_sectors"]:
            target = sector_idx[target_name]
            for element, mass in material.items():
                expected_B[element_idx[element], target] += float(mass)
            expected_A[producer, target] += replacement / p.q[target]

    assert np.allclose(p.B, expected_B)
    assert np.allclose(p.A, expected_A)
    assert p.B[:, sector_idx["mining"]].sum() > sum(sector_rows["mining"]["bom_t"].values())


def test_gravity_is_process_specific_not_global() -> None:
    p = load_integrated_params()
    profile = process_profile(p, "lunar_strategic_material_bridge")
    mining = p.sector_idx("mining")
    advanced = p.sector_idx("advanced_logic_memory")
    assert profile.centrifuge_rpm[mining] == 0.0
    assert profile.centrifuge_rpm[advanced] > 0.0
    assert profile.centrifuge_mass_t[advanced] > 0.0
    assert profile.B_effective[:, advanced].sum() > p.B[:, advanced].sum()
    nominal = process_profile(
        p,
        "lunar_strategic_material_bridge",
        environment_profile="lunar_nominal",
    )
    assert nominal.q_effective[mining] < profile.q_effective[mining]
    assert nominal.environment_depreciation_multiplier[mining] > 1.0


def test_knowledge_package_and_observable_autonomy_are_explicit() -> None:
    p = load_integrated_params()
    package = p.knowledge_autonomy["knowledge_package_t"]
    assert sum(package.values()) == p.seed["fixed_digital_seed_mass_t"]
    profile = process_profile(p, "moon_asteroid_network")
    for values in (
        profile.named_task_completion_rate,
        profile.fault_diagnosis_fraction,
        profile.process_yield,
        profile.repair_success_fraction,
    ):
        assert np.all((values >= 0.0) & (values <= 1.0))
    assert np.all(profile.verification_throughput_per_year > 0.0)
    assert np.all(profile.engineering_cycle_years > 0.0)
    assert np.all(profile.mean_time_to_recovery_days > 0.0)
    assert np.all(profile.stop_line_task_pass)


def test_seed_sizing_distinguishes_import_stock_from_strict_lunar_closure() -> None:
    p = load_integrated_params()
    bridge = size_seed(p, "lunar_strategic_material_bridge")
    strict = size_seed(p, "lunar_strict")
    network = size_seed(p, "moon_asteroid_network")
    bridge_total, _, bridge_import = bridge.required_masses()
    _, _, network_import = network.required_masses()
    assert bridge.feasible and bridge_import > 0
    assert not strict.feasible
    assert network.feasible and network_import == 0
    assert network.asteroid_feed_t_per_year > 0
    assert bridge_total > bridge.digital_seed_mass_t
    assert (
        network.minimum_task_coverage
        >= p.scenarios["moon_asteroid_network"]["minimum_task_coverage"]
    )


def test_seed_objectives_expose_no_current_design_tradeoff() -> None:
    p = load_integrated_params()
    for scenario in (
        "terrestrial_rehearsal",
        "lunar_strategic_material_bridge",
        "moon_asteroid_network",
    ):
        seeds = [
            size_seed(p, scenario, objective=objective)
            for objective in (
                "installed_mass",
                "earth_import_mass",
                "intervention_hours",
            )
        ]
        assert all(seed.feasible for seed in seeds)
        for seed in seeds[1:]:
            assert np.allclose(seed.capacities, seeds[0].capacities)
            assert np.allclose(seed.import_stock_t, seeds[0].import_stock_t)
    with np.testing.assert_raises(ValueError):
        size_seed(p, "terrestrial_rehearsal", objective="unknown")


def test_aggregate_capacity_doubling_and_intelligence_coupling() -> None:
    p = load_integrated_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_capacity_growth(p, seed, years=60, dt=0.25)
    assert run.survived
    assert run.aggregate_doubling_year == 35.25
    assert run.aggregate_doubling_year is not None
    i = int(np.searchsorted(run.t, run.aggregate_doubling_year))
    assert run.operating_cells[i] >= 2.0
    assert run.intelligence[-1] > run.intelligence[0]
    assert np.all(run.verified_loop_throughput >= 0.0)
    assert np.all(np.isfinite(run.intelligence_marginal_gain_per_loop))
    assert run.intelligence[-1] < p.intelligence["maximum_level"]
    assert run.local_compute[-1] > run.local_compute[0]
    assert run.asteroid_material_t > 0


def test_capacity_growth_state_remains_sector_resolved() -> None:
    p = load_integrated_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_capacity_growth(p, seed, years=40, dt=0.25)
    assert run.installed_sector_capacity.shape == (len(run.t), p.n)
    assert run.operating_sector_capacity.shape == (len(run.t), p.n)
    assert run.ordered_sector_capacity.shape == (len(run.t), p.n)
    assert run.commissioned_sector_capacity.shape == (len(run.t), p.n)
    assert run.activated_sector_capacity.shape == (len(run.t), p.n)
    normalized = run.operating_sector_capacity / seed.capacities
    assert np.allclose(run.operating_cells, normalized.min(axis=1))
    assert np.any(np.ptp(normalized, axis=1) > 1e-6)
    assert np.all(run.operating_sector_capacity <= run.installed_sector_capacity + 1e-12)
    assert run.commissioned_sector_capacity.sum() > 0.0
    assert run.activated_sector_capacity.sum() > 0.0


def test_independent_allocation_repair_and_shock_states_are_explicit() -> None:
    p = load_integrated_params()
    seed = size_seed(p, "lunar_strategic_material_bridge")
    run = simulate_capacity_growth(
        p,
        seed,
        allocation_policy="maximin_sector",
        repair_enabled=True,
        shock_events=((20.0, "advanced_logic_memory", 0.5),),
    )
    normalized_orders = np.divide(
        run.ordered_sector_capacity,
        seed.capacities,
        out=np.zeros_like(run.ordered_sector_capacity),
        where=seed.capacities > 1e-12,
    )
    assert np.any(np.ptp(normalized_orders, axis=1) > 1e-6)
    assert run.repaired_sector_capacity.sum() > 0.0
    assert run.shock_loss_sector_capacity.sum() > 0.0
    assert run.allocation_policy == "maximin_sector"
    assert run.repair_enabled


def test_delivered_seed_has_distinct_states_and_recovers_startup_failures() -> None:
    p = load_integrated_params()
    seed = size_seed(p, "moon_asteroid_network")
    deployment = simulate_seed_deployment(p, seed)
    assert deployment.delivered_seed_mass_t > deployment.installed_seed_mass_t
    assert deployment.logistics_mass_t > 0.0
    assert deployment.startup_energy_mwh > 0.0
    assert deployment.first_operating_year is not None
    assert deployment.full_operating_seed_year is not None
    assert deployment.recovered_startup_failure_t > 0.0
    assert deployment.success
    # Core mass occupies exactly one workflow state, apart from cumulative
    # commissioned mass whose operating/backlog partition is tracked below.
    assert deployment.delivered_core_t[-1] == 0.0
    assert deployment.staged_core_t[-1] == 0.0
    assert deployment.installed_core_t[-1] == 0.0
    np.testing.assert_allclose(
        deployment.operating_core_t[-1],
        deployment.installed_seed_mass_t,
        rtol=0.0,
        atol=1e-8,
    )


def test_earth_fed_orbit_is_rate_limited_and_endogenous_case_compounds() -> None:
    p = load_integrated_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_capacity_growth(p, seed, years=40, dt=0.25)
    curves = compare_compute_regimes(p, run)
    exogenous = curves.earth_fed_orbit["base"]
    assert np.all(np.diff(exogenous) <= 0.5 * 0.25 + 1e-12)
    assert curves.endogenous[-1] > exogenous[-1]
    assert curves.endogenous_orbit[-1] <= curves.endogenous[-1]


def test_debris_condition_changes_with_topology_and_mitigation() -> None:
    p = load_integrated_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_capacity_growth(p, seed, years=40, dt=0.25)
    curves = compare_compute_regimes(p, run)
    dense = simulate_debris(p, curves.endogenous, curves.t, "weak_mitigation", label="dense")
    distributed = simulate_debris(
        p,
        curves.endogenous_orbit,
        curves.t,
        "distributed_heliocentric",
        label="distributed",
    )
    assert not dense.subcritical
    assert dense.creation_clearance_ratio > 1.0
    assert distributed.subcritical
    assert distributed.fragments[-1] < dense.fragments[-1]


def test_shell_debris_has_finite_mass_conservation_and_capacity_feedback() -> None:
    p = load_integrated_params()
    t = np.arange(0.0, 40.25, 0.25)
    requested_capacity = np.linspace(1.0, 100.0, len(t))
    result = simulate_shell_debris(p, requested_capacity, t)
    assert result.active_capacity.shape == (len(t), 3)
    assert result.trackable_fragments.shape == (len(t), 3)
    assert result.untrackable_fragments.shape == (len(t), 3)
    assert result.deployment_shortfall_units.sum() > 0.0
    assert np.all(np.diff(result.uncaptured_reservoir_t) <= 1e-12)
    # Reservoir + accessible orbital mass changes only through Earth import
    # and declared unrecoverable loss; capture is an internal transfer.
    accounted = result.uncaptured_reservoir_t + result.accessible_orbital_mass_t
    residual = np.diff(accounted) - result.earth_imported_t[1:] + result.unrecoverable_loss_t[1:]
    assert np.max(np.abs(residual)) < 1e-8
    assert np.all(result.branching_ratio_by_shell >= 0.0)
    assert result.replacement_and_import_cost_usd > 0.0


def test_governance_threats_have_controls_verification_and_residual_risk() -> None:
    root = Path(__file__).resolve().parents[1]
    governance = yaml.safe_load((root / "params" / "governance_controls.yaml").read_text())
    assert set(governance["communication_states"]) == {
        "normal",
        "delayed",
        "lost",
    }
    controls = governance["controls"]
    assert len(governance["threats"]) >= 8
    for control in controls.values():
        assert control["verification"]
        assert control["rollback"]
        assert control["status"] == "requirement_unvalidated"
    for threat in governance["threats"].values():
        assert threat["controls"]
        assert threat["physical_state_trigger"]
        assert threat["residual_risk"]
        assert set(threat["controls"]) <= set(controls)


def test_integrated_ensemble_is_reproducible() -> None:
    p = load_integrated_params()
    a = seed_ensemble(p, "moon_asteroid_network", n_runs=8, seed=77, dt=0.5)
    b = seed_ensemble(p, "moon_asteroid_network", n_runs=8, seed=77, dt=0.5)
    assert a == b
    assert 0 <= a.n_feasible <= a.n_runs
    assert a.n_survived <= a.n_feasible


def test_integrated_html_has_intact_inline_math_and_release_candidate_metadata() -> None:
    root = Path(__file__).resolve().parents[1]
    source = (root / "docs" / "Recursive_Industrial_Intelligence_r4.0.md").read_text(
        encoding="utf-8"
    )
    html = (root / "docs" / "Recursive_Industrial_Intelligence_r4.0.html").read_text(
        encoding="utf-8"
    )

    assert r"\(" not in source and r"\)" not in source
    assert html.count("<math") >= 80
    rendered_html = re.sub(
        r"<script\b[^>]*>.*?</script>",
        "",
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for malformed in (
        '<span class="citation"',
        "(_",
        "()/",
        "(t+t)",
        "T_{I,}",
        "C</em>{DC}",
    ):
        assert malformed not in rendered_html

    # An untagged candidate must not pretend mutable main is canonical or
    # present the all-versions concept DOI as the version-specific DOI.
    assert (
        '<link rel="canonical" href="https://github.com/fperegrinvs/rsi-model/blob/main'
    ) not in html
    assert 'name="citation_doi"' not in html
    assert 'name="citation_publication_date"' not in html

    ids = re.findall(r'\bid="([^"]+)"', rendered_html)
    assert len(ids) == len(set(ids))
    targets = set(ids)
    internal_hrefs = re.findall(r'\bhref="#([^"]+)"', rendered_html)
    assert all(target in targets for target in internal_hrefs)


def test_integrated_public_artifacts_use_r40_claim_vocabulary() -> None:
    root = Path(__file__).resolve().parents[1]
    glossary = yaml.safe_load((root / "params" / "claim_glossary.yaml").read_text())
    paths = (
        root / "docs" / "Recursive_Industrial_Intelligence_r4.0.md",
        root / "outputs" / "integrated" / "report.md",
        root / "outputs" / "integrated" / "tables" / "scenario_summary.csv",
        root / "outputs" / "integrated" / "tables" / "terminal_endpoints.csv",
    )
    public_text = "\n".join(p.read_text(encoding="utf-8") for p in paths)
    deprecated = {"r4.1", "lunar_vitamin_bridge"}
    for section in ("metrics", "material_terms"):
        for entry in glossary[section].values():
            deprecated.update(entry.get("deprecated", []))
    for deprecated_phrase in sorted(deprecated):
        assert deprecated_phrase not in public_text
    for entry in glossary["metrics"].values():
        assert entry["preferred"] in public_text


def test_publication_set_has_short_result_led_abstracts_and_boundaries() -> None:
    root = Path(__file__).resolve().parents[1]
    papers = (
        root / "papers" / "TECHNICAL_PAPER_r4.0.md",
        root / "papers" / "ORBITAL_COMPUTE_ECONOMICS_r4.0.md",
        root / "papers" / "STRATEGY_GOVERNANCE_CASE_STUDY_r4.0.md",
    )
    for paper in papers:
        text = paper.read_text(encoding="utf-8")
        abstract = text.split("## Abstract", 1)[1].split("\n## ", 1)[0]
        assert len(re.findall(r"\b[\w$.–-]+\b", abstract)) <= 250
        assert re.search(r"\bP[1-4][ab]?\b", text)
        assert "does not" in text.lower()
    readme = (root / "papers" / "README.md").read_text(encoding="utf-8")
    for paper in papers:
        assert paper.name in readme


@pytest.mark.integration
@pytest.mark.slow
def test_integrated_pipeline_writes_complete_artifact_set_to_explicit_workspace(
    tmp_path: Path,
) -> None:
    """Exercise the artifact boundary without mutating checked-in outputs."""
    from rsimodel.integrated_pipeline import run as run_integrated_pipeline
    from rsimodel.run_config import IntegratedRunConfig

    project_root = Path(__file__).resolve().parents[1]
    output_directory = tmp_path / "integrated"
    run_integrated_pipeline(
        IntegratedRunConfig(
            project_root=project_root,
            parameters=project_root / "params" / "integrated_model.yaml",
            output_directory=output_directory,
            ensemble_size=1,
            ensemble_seed=404,
        ).validated()
    )

    tables = sorted((output_directory / "tables").glob("*.csv"))
    figures = sorted((output_directory / "figures").glob("*.png"))
    assert len(tables) >= 100
    assert {path.name for path in figures} == {
        "compute_growth_regimes.png",
        "debris_regimes.png",
        "operating_capacity.png",
        "oversize_frontier.png",
        "seed_mass_ensemble.png",
        "spacexai_threshold_tornado.png",
    }
    assert (output_directory / "report.md").stat().st_size > 10_000
    manifest = (output_directory / "MANIFEST.md").read_text(encoding="utf-8")
    assert "`OUTPUT/report.md`" in manifest
    for path in (*tables, *figures):
        assert f"`OUTPUT/{path.relative_to(output_directory)}`" in manifest
