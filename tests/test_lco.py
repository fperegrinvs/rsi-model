import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import numpy as np
import pytest

from rsimodel.lco import (CASES, AnchorSet, breakeven_launch_price, crf,
                          crossover_grid, lco_earth, lco_mc, lco_space)


def test_crf_sane():
    assert crf(0.10, 5.0) == pytest.approx(0.2638, abs=1e-3)
    assert crf(0.10, 1.0) == pytest.approx(1.10, abs=1e-9)


def test_space_lco_affine_in_launch_price():
    s0 = lco_space("leo_inference", launch_per_kg_leo=0.0)
    s1 = lco_space("leo_inference", launch_per_kg_leo=1000.0)
    assert s1.lco == pytest.approx(s0.alpha + s0.beta * 1000.0, rel=1e-9)
    assert s1.lco > s0.lco


def test_breakeven_exact():
    e = lco_earth("base")
    be = breakeven_launch_price("leo_inference", e.lco)
    s = lco_space("leo_inference", launch_per_kg_leo=be)
    assert s.lco == pytest.approx(e.lco, rel=1e-9)


def test_lunar_closure_reduces_cost():
    lo = lco_space("lunar_surface", closure_fraction=0.0)
    hi = lco_space("lunar_surface", closure_fraction=0.9)
    assert hi.lco < lo.lco
    assert hi.mass_kg_per_kw < lo.mass_kg_per_kw
    # chips are never closed: launched mass keeps at least the hw share
    assert hi.mass_kg_per_kw >= 0.99 * lo.capex_per_kw["hardware"] * 0  # guard trivially
    a = AnchorSet()
    hw_mass = a("compute.hw_mass_kg_per_kw")
    assert hi.mass_kg_per_kw > hw_mass * 0.99


def test_earth_scenarios_ordered():
    t, b, r = (lco_earth(s).lco for s in ("tight", "base", "responsive"))
    assert t >= b >= r


def test_responsive_uses_older_node_only_when_cheaper():
    e = lco_earth("responsive")
    assert e.node in ("frontier", "older")
    assert e.lco == pytest.approx(min(e.detail["frontier"],
                                      e.detail.get("older", np.inf)), rel=1e-12)


def test_earth_lco_matches_rental_order_of_magnitude():
    # $/kW-yr / 8760 ~ $/kW-hr; published accelerator rentals are ~$1-3/hr per ~kW
    e = lco_earth("base")
    assert 0.5 < e.lco / 8760.0 < 5.0


def test_mc_percentiles_ordered_and_reproducible():
    m1 = lco_mc("leo_inference", "base", n=100, seed=5)
    m2 = lco_mc("leo_inference", "base", n=100, seed=5)
    assert m1.ratio_pcts == m2.ratio_pcts
    assert m1.lco_pcts[10] <= m1.lco_pcts[50] <= m1.lco_pcts[90]
    assert 0.0 <= m1.p_space_cheaper <= 1.0


def test_crossover_grid_monotone_in_launch_price():
    lp = np.array([50.0, 500.0, 5000.0])
    g = crossover_grid("leo_inference", lp, "life_years",
                       np.array([5.0]), lco_earth("base").lco)
    assert g[0, 0] < g[0, 1] < g[0, 2]


def test_crossover_anchor_axis():
    lp = np.array([100.0])
    g = crossover_grid("leo_inference", lp, "compute.space_qual_multiplier",
                       np.array([1.0, 3.0]), lco_earth("base").lco)
    assert g[0, 0] < g[1, 0]   # cheaper qualification -> lower ratio


def test_provenance_recorded_with_source_classes():
    s = lco_space("leo_inference")
    classes = {p.source_class for p in s.provenance}
    assert "ASSUMPTION" in classes and classes & {"reporting", "technical_report",
                                                  "company_statement"}
    names = {p.quantity for p in s.provenance}
    assert "launch.leo_per_kg" in names and "compute.hw_per_kw_it" in names


def test_chip_efficiency_is_a_mass_multiplier():
    # r2.10 §16: efficiency scales the power side of launched mass, not the chips
    base = lco_space("leo_inference", launch_per_kg_leo=1000.0)
    eff2 = lco_space("leo_inference", launch_per_kg_leo=1000.0,
                     chip_efficiency_advantage=2.0)
    assert eff2.lco < base.lco
    a = AnchorSet()
    hw_mass = a("compute.hw_mass_kg_per_kw")
    struct = a("power_systems.structure_overhead_fraction")
    # power-side launched mass (excluding hw and its structure share) halves
    power_side = lambda s: s.mass_kg_per_kw - hw_mass * (1 + struct)
    assert power_side(eff2) == pytest.approx(power_side(base) / 2.0, rel=1e-9)
    # and the effect on the ratio compounds with launch price (multiplicative):
    # the absolute saving grows with launch price
    cheap_b = lco_space("leo_inference", launch_per_kg_leo=100.0)
    cheap_e = lco_space("leo_inference", launch_per_kg_leo=100.0,
                        chip_efficiency_advantage=2.0)
    assert (base.lco - eff2.lco) > (cheap_b.lco - cheap_e.lco)


def test_anchor_draws_within_ranges():
    rng = np.random.default_rng(0)
    a = AnchorSet(rng)
    for name in ("launch.leo_per_kg", "compute.hw_per_kw_it", "earth.pue"):
        v = a(name)
        e = a.anchors[name]
        assert e["low"] <= v <= e["high"]
