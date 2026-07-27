import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np

from rsimodel.fourth import (
    compare_compute_regimes,
    load_fourth_params,
    process_profile,
    seed_ensemble,
    simulate_debris,
    simulate_reproduction,
    size_seed,
)


def test_fourth_parameter_graph_is_mass_conserving_and_decomposed():
    p = load_fourth_params()
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


def test_gravity_is_process_specific_not_global():
    p = load_fourth_params()
    profile = process_profile(p, "lunar_vitamin_bridge")
    mining = p.sector_idx("mining")
    advanced = p.sector_idx("advanced_logic_memory")
    assert profile.centrifuge_rpm[mining] == 0.0
    assert profile.centrifuge_rpm[advanced] > 0.0
    assert profile.centrifuge_mass_t[advanced] > 0.0
    assert profile.B_effective[:, advanced].sum() > p.B[:, advanced].sum()


def test_seed_sizing_distinguishes_vitamins_from_strict_lunar_closure():
    p = load_fourth_params()
    bridge = size_seed(p, "lunar_vitamin_bridge")
    strict = size_seed(p, "lunar_strict")
    network = size_seed(p, "moon_asteroid_network")
    assert bridge.feasible and bridge.vitamin_stock_mass_t > 0
    assert not strict.feasible
    assert network.feasible and network.vitamin_stock_mass_t == 0
    assert network.asteroid_feed_t_per_year > 0
    assert bridge.total_seed_mass_t > bridge.digital_seed_mass_t
    assert network.minimum_task_coverage >= p.scenarios[
        "moon_asteroid_network"
    ]["minimum_task_coverage"]


def test_explicit_second_cell_commissioning_and_intelligence_coupling():
    p = load_fourth_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_reproduction(p, seed, years=40, dt=0.25)
    assert run.survived
    assert run.second_cell_year is not None
    i = int(np.searchsorted(run.t, run.second_cell_year))
    assert run.operating_cells[i] >= 2.0
    assert run.intelligence[-1] > run.intelligence[0]
    assert run.local_compute[-1] > run.local_compute[0]
    assert run.asteroid_material_t > 0


def test_earth_fed_orbit_is_rate_limited_and_endogenous_case_compounds():
    p = load_fourth_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_reproduction(p, seed, years=40, dt=0.25)
    curves = compare_compute_regimes(p, run)
    exogenous = curves.earth_fed_orbit["base"]
    assert np.all(np.diff(exogenous) <= 0.5 * 0.25 + 1e-12)
    assert curves.endogenous[-1] > exogenous[-1]
    assert curves.endogenous_orbit[-1] <= curves.endogenous[-1]


def test_debris_condition_changes_with_topology_and_mitigation():
    p = load_fourth_params()
    seed = size_seed(p, "moon_asteroid_network")
    run = simulate_reproduction(p, seed, years=40, dt=0.25)
    curves = compare_compute_regimes(p, run)
    dense = simulate_debris(
        p, curves.endogenous, curves.t, "weak_mitigation", label="dense"
    )
    distributed = simulate_debris(
        p,
        curves.endogenous_orbit,
        curves.t,
        "distributed_heliocentric",
        label="distributed",
    )
    assert not dense.subcritical
    assert dense.reproduction_ratio > 1.0
    assert distributed.subcritical
    assert distributed.fragments[-1] < dense.fragments[-1]


def test_fourth_ensemble_is_reproducible():
    p = load_fourth_params()
    a = seed_ensemble(p, "moon_asteroid_network", n_runs=8, seed=77, dt=0.5)
    b = seed_ensemble(p, "moon_asteroid_network", n_runs=8, seed=77, dt=0.5)
    assert a == b
    assert 0 <= a.n_feasible <= a.n_runs
    assert a.n_survived <= a.n_feasible


def test_fourth_html_has_intact_inline_math_and_release_candidate_metadata():
    root = Path(__file__).resolve().parents[1]
    source = (
        root / "docs" / "Recursive_Industrial_Intelligence_4th_Ed_r4.0.md"
    ).read_text(encoding="utf-8")
    html = (
        root / "docs" / "Recursive_Industrial_Intelligence_4th_Ed_r4.0.html"
    ).read_text(encoding="utf-8")

    assert r"\(" not in source and r"\)" not in source
    assert html.count("<math") >= 80
    for malformed in (
        "<span class=\"citation\"",
        "(_",
        "()/",
        "(t+t)",
        "T_{I,}",
        "C</em>{DC}",
    ):
        assert malformed not in html

    # An untagged candidate must not pretend mutable main is canonical or
    # present the all-versions concept DOI as the edition-specific DOI.
    assert (
        '<link rel="canonical" '
        'href="https://github.com/fperegrinvs/rsi-model/blob/main'
    ) not in html
    assert 'name="citation_doi"' not in html
    assert 'name="citation_publication_date"' not in html

    ids = re.findall(r'\bid="([^"]+)"', html)
    assert len(ids) == len(set(ids))
    targets = set(ids)
    internal_hrefs = re.findall(r'\bhref="#([^"]+)"', html)
    assert all(target in targets for target in internal_hrefs)
