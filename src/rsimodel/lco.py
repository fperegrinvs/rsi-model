"""Part II: levelized cost of compute, space vs. a responding Earth.

Three reference cases (paper r2.8 Section 9): LEO inference service,
high-orbit/cislunar batch compute, lunar-surface compute on locally
manufactured power. Unit: $ per frontier-equivalent kW-year of delivered IT
load (older-node hardware is penalized by its J/FLOP disadvantage so all
numbers are compute-normalized).

All inputs resolve from params/anchors.yaml Part II sections with provenance;
central values are geometric mids, Monte Carlo samples the ranges (one shared
draw per anchor, same discipline as Part I). Aspirational launch targets are
sweep axes only — never inputs (epistemic rule 3).

lco_space is affine in launch $/kg, so break-even launch prices are exact,
not root-found.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .delta import Provenance, anchor_value, load_anchors

EARTH_UTILIZATION = 0.90   # ASSUMPTION: mature DC availability x duty factor
LUNAR_PV_OVERSIZE = 2.2    # ASSUMPTION: day-only collection duty ~0.45
LUNAR_STORAGE_HOURS = 40.0  # ASSUMPTION: partial night ops, consistent w/ utilization_lunar
STORAGE_COST_PER_KWH = 250.0  # ASSUMPTION: pack-level $/kWh, space-qualified margin


@dataclass
class CaseConfig:
    name: str
    kg_multiplier_anchor: str | None   # $/kg multiplier vs LEO (None = 1.0)
    utilization_anchor: str
    pv_oversize: float = 1.0
    storage_hours: float = 0.0
    # closure: fraction of NON-hw launched mass manufactured locally
    # (chips are always imported — the Part I vitamin gap)
    closure_fraction: float = 0.0


CASES = {
    "leo_inference": CaseConfig("leo_inference", None, "compute.utilization_leo"),
    "cislunar_batch": CaseConfig("cislunar_batch", "launch.cislunar_multiplier",
                                 "compute.utilization_cislunar"),
    "lunar_surface": CaseConfig("lunar_surface", "launch.lunar_surface_multiplier",
                                "compute.utilization_lunar",
                                pv_oversize=LUNAR_PV_OVERSIZE,
                                storage_hours=LUNAR_STORAGE_HOURS,
                                closure_fraction=0.0),
}


class AnchorSet:
    """Resolved anchor values with provenance tracking of what was used."""

    def __init__(self, rng: np.random.Generator | None = None,
                 overrides: dict[str, float] | None = None):
        self.anchors = load_anchors()
        self.rng = rng
        self.overrides = overrides or {}
        self.used: list[Provenance] = []

    def __call__(self, name: str) -> float:
        if name in self.overrides:
            v = self.overrides[name]
            self.used.append(Provenance(name, v, "OVERRIDE", None, "scenario/sweep override"))
            return v
        e = self.anchors[name]
        v = anchor_value(e, self.rng)
        self.used.append(Provenance(name, v, e["source_class"], name, e.get("note", "")))
        return v


def crf(wacc: float, life_years: float) -> float:
    """Capital recovery factor: $/yr per $ of upfront capex."""
    return wacc / (1.0 - (1.0 + wacc) ** -life_years)


@dataclass
class SpaceLCO:
    case: str
    lco: float                     # $ per frontier-equiv kW-yr delivered
    launch_per_kg_leo: float
    mass_kg_per_kw: float          # launched mass per kW IT (after closure)
    capex_per_kw: dict[str, float]
    # affine decomposition: lco = alpha + beta * launch_per_kg_leo
    alpha: float
    beta: float
    provenance: list[Provenance] = field(repr=False, default_factory=list)


def lco_space(case: str, a: AnchorSet | None = None,
              launch_per_kg_leo: float | None = None,
              closure_fraction: float | None = None,
              life_years: float | None = None,
              chip_efficiency_advantage: float = 1.0) -> SpaceLCO:
    """Levelized cost for one space reference case.

    launch_per_kg_leo / closure_fraction / life_years override anchors for
    sweeps (targets and counterfactuals are axes, not inputs).

    chip_efficiency_advantage: relative FLOPS/W vs the reference accelerator
    (r2.10 §16: off Earth, efficiency is a MASS multiplier — every watt not
    computed must be radiated, and radiator/PV/structure are launched mass, so
    efficiency and launch price enter the crossover multiplicatively). A value
    e scales the entire power side (PV, radiator, storage, their structure and
    launch mass) by 1/e per unit of delivered compute; hardware $/compute is
    left unchanged (efficiency advantages are typically priced in).
    """
    cfg = CASES[case]
    a = a or AnchorSet()
    launch = a("launch.leo_per_kg") if launch_per_kg_leo is None else launch_per_kg_leo
    mult = a(cfg.kg_multiplier_anchor) if cfg.kg_multiplier_anchor else 1.0
    closure = cfg.closure_fraction if closure_fraction is None else closure_fraction
    life = a("compute.life_years_space") if life_years is None else life_years

    # kW of power (and thus heat to reject) per frontier-equivalent kW of compute
    power_kw = a("compute.power_overhead_space") / chip_efficiency_advantage
    pv_kw = power_kw * cfg.pv_oversize
    pv_mass = pv_kw * 1000.0 / a("power_systems.pv_specific_power_w_per_kg")
    radiator_mass = a("power_systems.radiator_kg_per_kw") * power_kw
    hw_mass = a("compute.hw_mass_kg_per_kw")
    storage_kwh = cfg.storage_hours * power_kw
    storage_mass = storage_kwh * a("power_systems.lunar_storage_kg_per_kwh") \
        if storage_kwh else 0.0
    subtotal = hw_mass + pv_mass + radiator_mass + storage_mass
    structure_mass = a("power_systems.structure_overhead_fraction") * subtotal
    non_hw_mass = pv_mass + radiator_mass + storage_mass + structure_mass
    # closure removes launched mass for locally made items, never the chips
    launched = hw_mass + non_hw_mass * (1.0 - closure)

    capex = {
        "hardware": a("compute.hw_per_kw_it") * a("compute.space_qual_multiplier"),
        "pv": a("power_systems.pv_cost_per_kw") * pv_kw,
        "radiator": a("power_systems.radiator_cost_per_kw") * power_kw,
        "storage": STORAGE_COST_PER_KWH * storage_kwh,
        "launch": launch * mult * launched,
    }
    wacc = a("earth.wacc")
    util = a(cfg.utilization_anchor)
    annualize = crf(wacc, life) + a("compute.ops_fraction_per_year")
    fixed = sum(v for k, v in capex.items() if k != "launch")
    alpha = fixed * annualize / util
    beta = mult * launched * annualize / util
    return SpaceLCO(case, alpha + beta * launch, launch, launched, capex,
                    alpha, beta, a.used)


@dataclass
class EarthLCO:
    scenario: str
    lco: float                     # $ per frontier-equiv kW-yr delivered
    node: str                      # "frontier" or "older"
    detail: dict[str, float]
    provenance: list[Provenance] = field(repr=False, default_factory=list)


def lco_earth(scenario: str = "base", a: AnchorSet | None = None) -> EarthLCO:
    """Terrestrial counterfactual that RESPONDS (epistemic requirement: the
    alternative is not frozen while space costs fall).

    - tight:      scarcity pricing — high-end power and DC capex, frontier hw only
                  (the politics-binds branch: permitting/climate commitments hold)
    - base:       anchors as drawn/central
    - responsive: induced supply — power at the cheapest firm floor (nuclear PPA
                  or the politically-conditional gas floor, whichever is lower),
                  low-end DC capex, and the older-node option (cheaper $/kW,
                  J/FLOP penalty) taken whenever it wins on compute-normalized cost
    """
    a = a or AnchorSet()
    hi = {"earth.power_price_kwh": a.anchors["earth.power_price_kwh"]["high"],
          "earth.dc_capex_per_kw_it": a.anchors["earth.dc_capex_per_kw_it"]["high"]}
    lo = {"earth.dc_capex_per_kw_it": a.anchors["earth.dc_capex_per_kw_it"]["low"]}
    if scenario == "tight":
        a.overrides = {**a.overrides, **hi}
    elif scenario == "responsive":
        a.overrides = {**a.overrides, **lo}
    elif scenario != "base":
        raise ValueError(f"unknown scenario {scenario!r}")

    wacc = a("earth.wacc")
    life = a("compute.life_years_earth")
    pue = a("earth.pue")
    dc = a("earth.dc_capex_per_kw_it")
    power = a("earth.power_price_kwh")
    if scenario == "responsive":
        # induced supply: firm generation buildable at the cheapest permitted floor
        power = min(power, a("earth.nuclear_ppa_kwh"),
                    a("earth.gas_power_price_floor_kwh"))
    energy_per_kwyr = power * 8760.0 * pue

    def total(hw_per_kw: float, penalty: float) -> float:
        # DC shell amortizes on a longer life than the hw refresh
        cap = hw_per_kw * crf(wacc, life) + dc * crf(wacc, 15.0)
        return penalty * (cap + energy_per_kwyr) / EARTH_UTILIZATION

    frontier = total(a("compute.hw_per_kw_it"), 1.0)
    variants = {"frontier": frontier}
    if scenario == "responsive":
        variants["older"] = total(a("earth.older_node_hw_per_kw"),
                                  a("earth.older_node_energy_penalty"))
    node = min(variants, key=variants.get)
    return EarthLCO(scenario, variants[node], node,
                    {"energy_per_kwyr": energy_per_kwyr, **variants}, a.used)


def breakeven_launch_price(case: str, earth_lco: float,
                           a: AnchorSet | None = None,
                           closure_fraction: float | None = None) -> float:
    """LEO launch $/kg at which the space case matches a given Earth LCO.
    Exact from the affine form; negative means never competitive (fixed costs
    alone exceed the Earth cost)."""
    s = lco_space(case, a=a, launch_per_kg_leo=0.0,
                  closure_fraction=closure_fraction)
    return (earth_lco - s.alpha) / s.beta


@dataclass
class LCOMC:
    case: str
    scenario: str
    lco_pcts: dict[int, float]         # space $/kW-yr percentiles
    earth_pcts: dict[int, float]
    ratio_pcts: dict[int, float]       # space/earth
    breakeven_pcts: dict[int, float]   # $/kg LEO
    p_space_cheaper: float
    n: int
    ratio_samples: np.ndarray = field(repr=False, default=None)
    breakeven_samples: np.ndarray = field(repr=False, default=None)


def lco_mc(case: str, scenario: str = "base", n: int = 2000,
           closure_fraction: float | None = None, seed: int = 0) -> LCOMC:
    rng = np.random.default_rng(seed)
    sp, ea, be = np.empty(n), np.empty(n), np.empty(n)
    for i in range(n):
        a = AnchorSet(rng)
        s = lco_space(case, a=a, closure_fraction=closure_fraction)
        e = lco_earth(scenario, a=a)      # shared draw: correlated hw/wacc both sides
        sp[i], ea[i] = s.lco, e.lco
        be[i] = (e.lco - s.alpha) / s.beta
    pct = lambda x: {p: float(np.percentile(x, p)) for p in (10, 50, 90)}
    return LCOMC(case, scenario, pct(sp), pct(ea), pct(sp / ea), pct(be),
                 float(np.mean(sp < ea)), n, sp / ea, be)


def crossover_grid(case: str, launch_prices: np.ndarray, other_axis: str,
                   other_values: np.ndarray, earth_lco: float) -> np.ndarray:
    """Ratio space/earth over (other_axis x launch price); <1 = space cheaper.

    other_axis is 'closure_fraction', 'life_years', 'chip_efficiency_advantage',
    or any full anchor name (e.g. 'power_systems.radiator_kg_per_kw',
    'compute.space_qual_multiplier') which is overridden pointwise; other
    anchors stay at central values.
    """
    out = np.empty((len(other_values), len(launch_prices)))
    for i, val in enumerate(other_values):
        kw, overrides = {}, {}
        if other_axis in ("closure_fraction", "life_years", "chip_efficiency_advantage"):
            kw[other_axis] = float(val)
        else:
            overrides[other_axis] = float(val)
        s = lco_space(case, a=AnchorSet(overrides=overrides),
                      launch_per_kg_leo=0.0, **kw)
        out[i] = (s.alpha + s.beta * launch_prices) / earth_lco
    return out
