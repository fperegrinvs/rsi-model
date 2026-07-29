"""Part II: levelized cost of compute, space vs. a responding Earth.

Three reference cases (paper Part II): LEO inference service,
high-orbit/cislunar batch compute, and lunar-surface compute, plus separate
SpaceXAI AI1 disclosed-design and stated-aspiration scenarios. Unit:
$ per frontier-equivalent kW-year of delivered IT load (older-node hardware
is penalized by its J/FLOP disadvantage so all numbers are compute-normalized).

All inputs resolve from params/anchors.yaml Part II sections with provenance;
central values are geometric mids, Monte Carlo samples the ranges (one shared
draw per anchor, same discipline as Part I). Aspirational launch targets are
sweep axes except in the explicitly quarantined best-case sensitivity, where
company targets and favorable model assumptions are displayed rather than
treated as achieved performance (epistemic rule 3).

lco_space is affine in launch $/kg, so break-even launch prices are exact,
not root-found.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

import numpy as np

from .array_types import FloatArray
from .delta import Provenance, anchor_child_rng, anchor_value, load_anchors
from .orbital_ai_scenarios import scenario_labels

EARTH_UTILIZATION = 0.90  # ASSUMPTION: mature DC availability x duty factor
LUNAR_PV_OVERSIZE = 2.2  # ASSUMPTION: day-only collection duty ~0.45
LUNAR_STORAGE_HOURS = 40.0  # ASSUMPTION: partial night ops, consistent w/ utilization_lunar
STORAGE_COST_PER_KWH = 250.0  # ASSUMPTION: pack-level $/kWh, space-qualified margin


@dataclass
class CaseConfig:
    name: str
    kg_multiplier_anchor: str | None  # $/kg multiplier vs LEO (None = 1.0)
    utilization_anchor: str
    pv_oversize: float = 1.0
    storage_hours: float = 0.0
    # closure: fraction of NON-hw launched mass manufactured locally
    # (chips are always imported — the Part I vitamin gap)
    closure_fraction: float = 0.0
    # Optional disclosed-architecture constraints. The power ratio is the
    # first anchor divided by the second; total_mass_anchor fixes aggregate
    # launched vehicle kg per average kW while the generic component budget
    # supplies only the hw/infrastructure mass split used for amortization.
    power_ratio_anchors: tuple[str, str] | None = None
    total_mass_anchor: str | None = None
    published_spec_anchors: tuple[str, ...] = ()
    launch_price_anchor: str = "launch.leo_per_kg"
    life_anchor: str = "compute.life_years_space"
    qualification_anchor: str = "compute.space_qual_multiplier"


CASES = {
    "leo_inference": CaseConfig("leo_inference", None, "compute.utilization_leo"),
    "cislunar_batch": CaseConfig(
        "cislunar_batch", "launch.cislunar_multiplier", "compute.utilization_cislunar"
    ),
    "lunar_surface": CaseConfig(
        "lunar_surface",
        "launch.lunar_surface_multiplier",
        "compute.utilization_lunar",
        pv_oversize=LUNAR_PV_OVERSIZE,
        storage_hours=LUNAR_STORAGE_HOURS,
        closure_fraction=0.0,
    ),
    # Conditional scenario, not a new measured baseline. SpaceX publishes the
    # power and vehicle-efficiency specifications but not lifetime, achieved
    # availability, capex, qualification cost, or a mass breakdown, so those
    # quantities retain the existing anchored ranges.
    "starmind_ai1": CaseConfig(
        "starmind_ai1",
        None,
        "compute.utilization_leo",
        power_ratio_anchors=("starmind.solar_array_kw", "starmind.compute_payload_kw_average"),
        total_mass_anchor="starmind.vehicle_mass_kg_per_average_kw",
        published_spec_anchors=(
            "starmind.compute_payload_kw_peak",
            "starmind.compute_payload_kw_average",
            "starmind.vehicle_efficiency_kw_per_tonne",
            "starmind.vehicle_mass_kg_per_average_kw",
            "starmind.solar_array_kw",
            "starmind.solar_power_density_w_per_m2",
            "starmind.radiator_area_m2",
            "starmind.deployed_height_m",
            "starmind.wingspan_m",
        ),
    ),
    # Deliberately optimistic sensitivity, not a forecast or MC prior:
    # company targets set launch cost and aggregate vehicle efficiency; the
    # unpublished qualification, useful life, and utilization values are
    # separately source-classed ASSUMPTIONs at the favorable existing bounds.
    "starmind_ai1_aspirational": CaseConfig(
        "starmind_ai1_aspirational",
        None,
        "aspirations.starmind_utilization",
        power_ratio_anchors=("starmind.solar_array_kw", "starmind.compute_payload_kw_average"),
        total_mass_anchor="aspirations.starmind_vehicle_mass_kg_per_average_kw",
        published_spec_anchors=(
            "starmind.compute_payload_kw_peak",
            "starmind.compute_payload_kw_average",
            "starmind.solar_array_kw",
            "aspirations.starmind_vehicle_efficiency_kw_per_tonne",
            "aspirations.starmind_vehicle_mass_kg_per_average_kw",
            "aspirations.starship_leo_cost_per_kg",
            "aspirations.starship_v3_payload_tonnes",
            "aspirations.starship_v4_payload_tonnes",
            "aspirations.orbital_compute_gw_per_year",
            "aspirations.starmind_qualification_multiplier",
            "aspirations.starmind_life_years",
            "aspirations.starmind_utilization",
        ),
        launch_price_anchor="aspirations.starship_leo_cost_per_kg",
        life_anchor="aspirations.starmind_life_years",
        qualification_anchor="aspirations.starmind_qualification_multiplier",
    ),
}

# The aspiration case is a deterministic stress test. Sampling it as though
# company targets and analyst-selected favorable bounds were empirical priors
# would manufacture a meaningless "probability of success."
MONTE_CARLO_CASES = tuple(case for case in CASES if case != "starmind_ai1_aspirational")

# Display names for reports/manuscript. The central lunar reference case has
# closure_fraction = 0: ALL non-hardware mass is launched from Earth, so it is
# Earth-supplied lunar-surface compute, NOT "compute on locally manufactured
# power" (review fix). Local manufacture enters only via the
# closure-fraction sweep axis.
_NAMED_SCENARIO_LABELS = scenario_labels()
CASE_LABELS = {
    "leo_inference": "leo_inference",
    "cislunar_batch": "cislunar_batch",
    "lunar_surface": "lunar_surface (Earth-supplied)",
    "starmind_ai1": _NAMED_SCENARIO_LABELS["spacexai_disclosed_design"],
    "starmind_ai1_aspirational": _NAMED_SCENARIO_LABELS["spacexai_stated_aspiration"],
}


class AnchorSet:
    """Resolved anchor values with provenance tracking of what was used.

    Each anchor is drawn ONCE per AnchorSet and cached: every subsequent
    request returns the same value. This is what makes the Monte Carlo's
    stated shared-draw correlation real — lco_space() and lco_earth() called
    with the same AnchorSet see the same wacc, hardware cost, etc. (review correction:
    previously every request re-sampled, so the correlation was documentation
    only). Overrides bypass the cache so a later scenario override still wins.

    Draws are keyed by (per-instance entropy, anchor name) — the same
    stability scheme as delta.draw_anchors: exactly one integer is consumed
    from `rng` at construction, and each anchor's value is independent of
    which other anchors exist or the order they are requested in.
    """

    def __init__(
        self,
        rng: np.random.Generator | None = None,
        overrides: Mapping[str, float] | None = None,
    ) -> None:
        self.anchors = load_anchors()
        self.rng = rng
        self._entropy = int(rng.integers(0, 2**63)) if rng is not None else None
        self.overrides = dict(overrides or {})
        self.used: list[Provenance] = []
        self._cache: dict[str, float] = {}

    def __call__(self, name: str) -> float:
        if name in self.overrides:
            v = self.overrides[name]
            if not any(pr.quantity == name and pr.source_class == "OVERRIDE" for pr in self.used):
                self.used.append(Provenance(name, v, "OVERRIDE", None, "scenario/sweep override"))
            return v
        if name in self._cache:
            return self._cache[name]
        e = self.anchors[name]
        child = anchor_child_rng(self._entropy, name) if self._entropy is not None else None
        v = anchor_value(e, child)
        self._cache[name] = v
        self.used.append(Provenance(name, v, e["source_class"], name, e.get("note", "")))
        return v


def crf(wacc: float, life_years: float) -> float:
    """Capital recovery factor: $/yr per $ of upfront capex."""
    return wacc / (1.0 - (1.0 + wacc) ** -life_years)


@dataclass
class SpaceLCO:
    case: str
    architecture: str  # serviceable_platform | integrated_disposable
    lco: float  # $ per frontier-equiv kW-yr delivered
    launch_per_kg_leo: float
    mass_kg_per_kw: float  # launched mass per kW IT (after closure)
    capex_per_kw: dict[str, float]
    # affine decomposition: lco = alpha + beta * launch_per_kg_leo
    alpha: float
    beta: float
    architecture_specs: dict[str, float] = field(repr=False, default_factory=dict)
    detail: dict[str, float] = field(repr=False, default_factory=dict)
    provenance: list[Provenance] = field(repr=False, default_factory=list)
    workload_costs: dict[str, float] = field(repr=False, default_factory=dict)


def lco_space(
    case: str,
    a: AnchorSet | None = None,
    launch_per_kg_leo: float | None = None,
    closure_fraction: float | None = None,
    life_years: float | None = None,
    architecture: str = "serviceable_platform",
    chip_efficiency_advantage: float = 1.0,
    total_mass_kg_per_kw: float | None = None,
    complete_costs: bool = True,
) -> SpaceLCO:
    """Levelized cost for one space reference case.

    launch_per_kg_leo / closure_fraction / life_years override anchors for
    sweeps (targets and counterfactuals are axes, not inputs). In the
    ``serviceable_platform`` architecture, life_years is the compute-hardware
    refresh life and power/thermal/structure amortize on the longer
    power_systems.infrastructure_life_years. In ``integrated_disposable``,
    every component and its launch spend retire together on life_years.

    ``total_mass_kg_per_kw`` applies an external system-level mass constraint
    while preserving the model's hardware/infrastructure proportions. It is
    used only for explicitly identified architecture comparisons; it does not
    change the generic prior.

    chip_efficiency_advantage: relative FLOPS/W vs the reference accelerator
    (the paper's efficiency boundary: off Earth, efficiency is a MASS multiplier — every watt not
    computed must be radiated, and radiator/PV/structure are launched mass, so
    efficiency and launch price enter the crossover multiplicatively). A value
    e scales the entire power side (PV, radiator, storage, their structure and
    launch mass) by 1/e per unit of delivered compute; hardware $/compute is
    left unchanged (efficiency advantages are typically priced in).
    """
    if architecture not in ("serviceable_platform", "integrated_disposable"):
        raise ValueError(f"unknown space architecture {architecture!r}")
    cfg = CASES[case]
    a = a or AnchorSet()
    architecture_specs = {name: a(name) for name in cfg.published_spec_anchors}
    launch = a(cfg.launch_price_anchor) if launch_per_kg_leo is None else launch_per_kg_leo
    mult = a(cfg.kg_multiplier_anchor) if cfg.kg_multiplier_anchor else 1.0
    closure = cfg.closure_fraction if closure_fraction is None else closure_fraction
    # component-specific lives (review fix): the compute refresh cycle
    # applies to the accelerators only; PV/radiator/storage/structure and the
    # launch spend that emplaced them amortize on the longer infrastructure
    # life. Replacement chips must be re-launched, so the hw-mass share of
    # launch recurs on the hw life.
    life_hw = a(cfg.life_anchor) if life_years is None else life_years
    anchored_infra_life = max(a("power_systems.infrastructure_life_years"), life_hw)
    life_infra = life_hw if architecture == "integrated_disposable" else anchored_infra_life

    # kW of power (and thus heat to reject) per frontier-equivalent kW of
    # compute. A disclosed design can supply its array/load ratio directly;
    # otherwise the generic space-power-overhead anchor applies.
    if cfg.power_ratio_anchors:
        numerator, denominator = cfg.power_ratio_anchors
        power_kw = architecture_specs[numerator] / architecture_specs[denominator]
    else:
        power_kw = a("compute.power_overhead_space")
    power_kw /= chip_efficiency_advantage
    pumping_fraction = a("space_cost_completion.pumping_power_fraction") if complete_costs else 0.0
    # A disclosed array/load ratio already constrains total available power;
    # adding pumping on top would contradict that specification. Generic
    # cases expose pumping as an additional load.
    if not cfg.power_ratio_anchors:
        power_kw *= 1.0 + pumping_fraction
    pv_kw = power_kw * cfg.pv_oversize
    pv_mass = pv_kw * 1000.0 / a("power_systems.pv_specific_power_w_per_kg")
    if complete_costs:
        rejection_temperature = a("space_cost_completion.radiator_rejection_temperature_k")
        temperature_drop = a("space_cost_completion.chip_to_radiator_temperature_drop_k")
        view_factor = a("space_cost_completion.environmental_view_factor")
        thermal_margin = a("space_cost_completion.thermal_reliability_mass_margin")
        thermal_scale = (360.0 / rejection_temperature) ** 4 * thermal_margin / view_factor
    else:
        rejection_temperature = 360.0
        temperature_drop = 0.0
        view_factor = 1.0
        thermal_margin = 1.0
        thermal_scale = 1.0
    radiator_mass = a("power_systems.radiator_kg_per_kw") * power_kw * thermal_scale
    hw_mass = a("compute.hw_mass_kg_per_kw")
    storage_kwh = cfg.storage_hours * power_kw
    storage_mass = storage_kwh * a("power_systems.lunar_storage_kg_per_kwh") if storage_kwh else 0.0
    subtotal = hw_mass + pv_mass + radiator_mass + storage_mass
    structure_mass = a("power_systems.structure_overhead_fraction") * subtotal
    non_hw_mass = pv_mass + radiator_mass + storage_mass + structure_mass
    if total_mass_kg_per_kw is not None:
        if total_mass_kg_per_kw <= 0.0:
            raise ValueError("total_mass_kg_per_kw must be positive")
        mass_scale = total_mass_kg_per_kw / (hw_mass + non_hw_mass)
        hw_mass *= mass_scale
        non_hw_mass *= mass_scale
    elif cfg.total_mass_anchor:
        # The disclosure constrains total vehicle mass but supplies no component
        # split. Scale the generic engineering mass budget to that total, keeping
        # only its hw-vs-infrastructure proportions for lifecycle accounting.
        disclosed_total_mass = architecture_specs[cfg.total_mass_anchor]
        mass_scale = disclosed_total_mass / (hw_mass + non_hw_mass)
        hw_mass *= mass_scale
        non_hw_mass *= mass_scale
    # closure removes launched mass for locally made items, never the chips
    launched = hw_mass + non_hw_mass * (1.0 - closure)

    capex = {
        "hardware": a("compute.hw_per_kw_it") * a(cfg.qualification_anchor),
        "pv": a("power_systems.pv_cost_per_kw") * pv_kw,
        "radiator": (a("power_systems.radiator_cost_per_kw") * power_kw * thermal_scale),
        "storage": STORAGE_COST_PER_KWH * storage_kwh,
        "launch": launch * mult * launched,
    }
    if complete_costs:
        capex.update(
            {
                "communications": a("space_cost_completion.communications_capex_per_kw"),
                "ground_network": a("space_cost_completion.ground_network_capex_per_kw"),
                "spacecraft_bus": a("space_cost_completion.spacecraft_bus_capex_per_kw"),
                "disposal": a("space_cost_completion.disposal_capex_per_kw"),
            }
        )
        recurring_nonlaunch = sum(value for key, value in capex.items() if key != "launch")
        capex["program_nre"] = recurring_nonlaunch * a("space_cost_completion.program_nre_fraction")
        wacc = a("space_cost_completion.wacc")
        insurance = a("space_cost_completion.insurance_fraction_per_year")
        regulatory = a("space_cost_completion.spectrum_regulatory_per_kw_year")
        residual = a(
            "space_cost_completion.residual_value_fraction_serviceable"
            if architecture == "serviceable_platform"
            else "space_cost_completion.residual_value_fraction_disposable"
        )
    else:
        wacc = a("earth.wacc")
        insurance = 0.0
        regulatory = 0.0
        residual = 0.0
    util = a(cfg.utilization_anchor)
    ops = a("compute.ops_fraction_per_year")
    salvage_hw = crf(wacc, life_hw) * (1.0 - residual / (1.0 + wacc) ** life_hw)
    salvage_infra = crf(wacc, life_infra) * (1.0 - residual / (1.0 + wacc) ** life_infra)
    ann_hw = salvage_hw + ops + insurance
    ann_infra = salvage_infra + ops + insurance
    infra_capex = sum(
        capex.get(name, 0.0)
        for name in (
            "pv",
            "radiator",
            "storage",
            "communications",
            "ground_network",
            "spacecraft_bus",
            "disposal",
            "program_nre",
        )
    )
    alpha = (capex["hardware"] * ann_hw + infra_capex * ann_infra + regulatory) / util
    # launch $ split by what the mass is for: hw-mass share recurs with the
    # chip refresh, infrastructure-mass share with the infrastructure life —
    # still exactly affine in launch $/kg, so break-evens stay exact.
    beta = mult * (hw_mass * ann_hw + non_hw_mass * (1.0 - closure) * ann_infra) / util
    detail = {
        "life_hw": life_hw,
        "life_infra": life_infra,
        "anchored_infra_life": anchored_infra_life,
        "wacc": wacc,
        "utilization": util,
        "ops_fraction": ops,
        "ann_hw": ann_hw,
        "ann_infra": ann_infra,
        "hw_mass": hw_mass,
        "non_hw_launched_mass": non_hw_mass * (1.0 - closure),
        "launch_multiplier": mult,
        "infra_capex": infra_capex,
        "power_kw": power_kw,
        "pumping_power_fraction": pumping_fraction,
        "radiator_rejection_temperature_k": rejection_temperature,
        "chip_temperature_k": rejection_temperature + temperature_drop,
        "environmental_view_factor": view_factor,
        "thermal_reliability_mass_margin": thermal_margin,
        "residual_value_fraction": residual,
        "insurance_fraction_per_year": insurance,
        "spectrum_regulatory_per_kw_year": regulatory,
        "complete_costs": float(complete_costs),
    }
    inference_throughput = (
        a("workloads.inference_requests_per_kwh")
        * 8760.0
        * a("workloads.inference_latency_availability_fraction")
    )
    training_efficiency = a("workloads.training_network_efficiency_space")
    lco = alpha + beta * launch
    workload_costs = {
        "cost_per_million_inferences": (lco / max(inference_throughput, 1e-12) * 1_000_000.0),
        "cost_per_network_effective_training_kw_year": (lco / max(training_efficiency, 1e-12)),
        "inference_requests_per_kw_year": inference_throughput,
        "training_network_efficiency": training_efficiency,
    }
    return SpaceLCO(
        case,
        architecture,
        lco,
        launch,
        launched,
        capex,
        alpha,
        beta,
        architecture_specs,
        detail,
        a.used,
        workload_costs,
    )


@dataclass
class EarthLCO:
    scenario: str
    lco: float  # $ per frontier-equiv kW-yr delivered
    node: str  # "frontier" or "older"
    detail: dict[str, float]
    provenance: list[Provenance] = field(repr=False, default_factory=list)
    workload_costs: dict[str, float] = field(repr=False, default_factory=dict)


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
    hi = {
        "earth.power_price_kwh": a.anchors["earth.power_price_kwh"]["high"],
        "earth.dc_capex_per_kw_it": a.anchors["earth.dc_capex_per_kw_it"]["high"],
    }
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
        power = min(power, a("earth.nuclear_ppa_kwh"), a("earth.gas_power_price_floor_kwh"))
    energy_per_kwyr = power * 8760.0 * pue

    def total(hw_per_kw: float, penalty: float) -> float:
        # DC shell amortizes on a longer life than the hw refresh
        cap = hw_per_kw * crf(wacc, life) + dc * crf(wacc, 15.0)
        return penalty * (cap + energy_per_kwyr) / EARTH_UTILIZATION

    frontier = total(a("compute.hw_per_kw_it"), 1.0)
    variants = {"frontier": frontier}
    if scenario == "responsive":
        variants["older"] = total(
            a("earth.older_node_hw_per_kw"), a("earth.older_node_energy_penalty")
        )
    node = min(variants, key=lambda name: variants[name])
    lco = variants[node]
    if node == "older":
        selected_hw_per_kw = a("earth.older_node_hw_per_kw")
        selected_energy_penalty = a("earth.older_node_energy_penalty")
    else:
        selected_hw_per_kw = a("compute.hw_per_kw_it")
        selected_energy_penalty = 1.0
    inference_throughput = (
        a("workloads.inference_requests_per_kwh")
        * 8760.0
        * a("workloads.inference_latency_availability_fraction")
    )
    training_efficiency = a("workloads.training_network_efficiency_earth")
    workload_costs = {
        "cost_per_million_inferences": (lco / max(inference_throughput, 1e-12) * 1_000_000.0),
        "cost_per_network_effective_training_kw_year": (lco / max(training_efficiency, 1e-12)),
        "inference_requests_per_kw_year": inference_throughput,
        "training_network_efficiency": training_efficiency,
    }
    return EarthLCO(
        scenario,
        lco,
        node,
        {
            "energy_per_kwyr": energy_per_kwyr,
            "wacc": wacc,
            "pue": pue,
            "life_years": life,
            "dc_capex_per_kw_it": dc,
            "selected_hw_per_kw": selected_hw_per_kw,
            "selected_energy_penalty": selected_energy_penalty,
            "utilization": EARTH_UTILIZATION,
            "power_price_per_kwh": power,
            **variants,
        },
        a.used,
        workload_costs,
    )


MATCHED_COST_CATEGORIES = (
    "site_or_access_rights",
    "regulation_and_permitting",
    "transport_and_logistics",
    "energy",
    "feedstock_and_materials",
    "extraction_and_processing",
    "manufacturing_and_hardware",
    "construction_and_commissioning",
    "labor_or_human_intervention",
    "maintenance_replacement_and_insurance",
    "coordination_and_verification",
    "decommissioning_and_disposal",
    "externalities",
    "financing",
    "residual_value_credit",
)


def space_lco_contributions(result: SpaceLCO) -> dict[str, float]:
    """Return an exact matched-category decomposition of one space LCO.

    Categories that the implemented Part II boundary does not price are
    returned as zero rather than silently assigned an advantage. Capital
    recovery is allocated to the asset category; insurance is kept with
    maintenance/risk, and the discounted residual credit is exposed
    separately. The rows sum to ``result.lco``.
    """
    detail = result.detail
    capex = result.capex_per_kw
    utilization = detail["utilization"]
    wacc = detail["wacc"]
    life_hw = detail["life_hw"]
    life_infra = detail["life_infra"]
    residual = detail["residual_value_fraction"]
    crf_hw = crf(wacc, life_hw)
    crf_infra = crf(wacc, life_infra)

    launch_hw = result.launch_per_kg_leo * detail["launch_multiplier"] * detail["hw_mass"]
    launch_infra = (
        result.launch_per_kg_leo * detail["launch_multiplier"] * detail["non_hw_launched_mass"]
    )
    hw_assets = capex["hardware"]
    energy_assets = capex.get("pv", 0.0) + capex.get("storage", 0.0)
    coordination_assets = capex.get("communications", 0.0) + capex.get("ground_network", 0.0)
    construction_assets = (
        capex.get("radiator", 0.0)
        + capex.get("spacecraft_bus", 0.0)
        + capex.get("program_nre", 0.0)
    )
    disposal_assets = capex.get("disposal", 0.0)
    infra_assets = energy_assets + coordination_assets + construction_assets + disposal_assets
    all_assets = hw_assets + infra_assets + launch_hw + launch_infra
    residual_credit = (
        -(
            (hw_assets + launch_hw) * crf_hw * residual / (1.0 + wacc) ** life_hw
            + (infra_assets + launch_infra) * crf_infra * residual / (1.0 + wacc) ** life_infra
        )
        / utilization
    )

    values: dict[str, float] = dict.fromkeys(MATCHED_COST_CATEGORIES, 0.0)
    values.update(
        {
            "regulation_and_permitting": (detail["spectrum_regulatory_per_kw_year"] / utilization),
            "transport_and_logistics": (launch_hw * crf_hw + launch_infra * crf_infra)
            / utilization,
            "energy": energy_assets * crf_infra / utilization,
            "manufacturing_and_hardware": hw_assets * crf_hw / utilization,
            "construction_and_commissioning": (construction_assets * crf_infra / utilization),
            "maintenance_replacement_and_insurance": (
                all_assets
                * (detail["ops_fraction"] + detail["insurance_fraction_per_year"])
                / utilization
            ),
            "coordination_and_verification": (coordination_assets * crf_infra / utilization),
            "decommissioning_and_disposal": (disposal_assets * crf_infra / utilization),
            "residual_value_credit": residual_credit,
        }
    )
    if not np.isclose(sum(values.values()), result.lco, rtol=1e-10, atol=1e-8):
        raise ValueError("space contribution decomposition does not sum to LCO")
    return values


def earth_lco_contributions(result: EarthLCO) -> dict[str, float]:
    """Return the same category schema for the implemented Earth LCO."""
    detail = result.detail
    utilization = detail["utilization"]
    penalty = detail["selected_energy_penalty"]
    values: dict[str, float] = dict.fromkeys(MATCHED_COST_CATEGORIES, 0.0)
    values.update(
        {
            "energy": (penalty * detail["energy_per_kwyr"] / utilization),
            "manufacturing_and_hardware": (
                penalty
                * detail["selected_hw_per_kw"]
                * crf(detail["wacc"], detail["life_years"])
                / utilization
            ),
            "construction_and_commissioning": (
                penalty * detail["dc_capex_per_kw_it"] * crf(detail["wacc"], 15.0) / utilization
            ),
        }
    )
    if not np.isclose(sum(values.values()), result.lco, rtol=1e-10, atol=1e-8):
        raise ValueError("Earth contribution decomposition does not sum to LCO")
    return values


def breakeven_launch_price(
    case: str,
    earth_lco: float,
    a: AnchorSet | None = None,
    closure_fraction: float | None = None,
    life_years: float | None = None,
    architecture: str = "serviceable_platform",
    chip_efficiency_advantage: float = 1.0,
    complete_costs: bool = True,
) -> float:
    """LEO launch $/kg at which the space case matches a given Earth LCO.
    Exact from the affine form; negative means never competitive (fixed costs
    alone exceed the Earth cost)."""
    s = lco_space(
        case,
        a=a,
        launch_per_kg_leo=0.0,
        closure_fraction=closure_fraction,
        life_years=life_years,
        architecture=architecture,
        chip_efficiency_advantage=chip_efficiency_advantage,
        complete_costs=complete_costs,
    )
    return (earth_lco - s.alpha) / s.beta


def orbital_ai_scale(
    compute_gw: float,
    efficiency_kw_per_tonne: float,
    payload_tonnes: float,
    spacecraft_average_kw: float | None = None,
) -> dict[str, float]:
    """Arithmetic implications of an orbital-compute deployment target.

    This is a unit conversion, not a cadence or manufacturability model.
    ``payload_tonnes`` is useful payload per launch, not vehicle dry mass.
    """
    if compute_gw <= 0 or efficiency_kw_per_tonne <= 0 or payload_tonnes <= 0:
        raise ValueError("scale inputs must be positive")
    compute_kw = compute_gw * 1_000_000.0
    mass_tonnes = compute_kw / efficiency_kw_per_tonne
    launches_per_year = mass_tonnes / payload_tonnes
    out = {
        "compute_kw": compute_kw,
        "mass_tonnes": mass_tonnes,
        "launches_per_year": launches_per_year,
        "launches_per_day": launches_per_year / 365.25,
    }
    if spacecraft_average_kw is not None:
        if spacecraft_average_kw <= 0:
            raise ValueError("spacecraft_average_kw must be positive")
        out["spacecraft_count"] = compute_kw / spacecraft_average_kw
    return out


@dataclass
class LCOMC:
    case: str
    scenario: str
    architecture: str
    lco_pcts: dict[int, float]  # space $/kW-yr percentiles
    earth_pcts: dict[int, float]
    ratio_pcts: dict[int, float]  # space/earth
    breakeven_pcts: dict[int, float]  # $/kg LEO
    p_space_cheaper: float
    n: int
    ratio_samples: FloatArray = field(
        repr=False,
        default_factory=lambda: np.empty(0, dtype=np.float64),
    )
    breakeven_samples: FloatArray = field(
        repr=False,
        default_factory=lambda: np.empty(0, dtype=np.float64),
    )


def lco_mc(
    case: str,
    scenario: str = "base",
    n: int = 2000,
    closure_fraction: float | None = None,
    architecture: str = "serviceable_platform",
    seed: int = 0,
) -> LCOMC:
    rng = np.random.default_rng(seed)
    sp, ea, be = np.empty(n), np.empty(n), np.empty(n)
    for i in range(n):
        a = AnchorSet(rng)
        s = lco_space(
            case,
            a=a,
            closure_fraction=closure_fraction,
            architecture=architecture,
        )
        e = lco_earth(scenario, a=a)  # shared draw: correlated hw/wacc both sides
        sp[i], ea[i] = s.lco, e.lco
        be[i] = (e.lco - s.alpha) / s.beta

    def pct(values: FloatArray) -> dict[int, float]:
        return {percentile: float(np.percentile(values, percentile)) for percentile in (10, 50, 90)}

    return LCOMC(
        case,
        scenario,
        architecture,
        pct(sp),
        pct(ea),
        pct(sp / ea),
        pct(be),
        float(np.mean(sp < ea)),
        n,
        sp / ea,
        be,
    )


def crossover_grid(
    case: str,
    launch_prices: FloatArray,
    other_axis: str,
    other_values: FloatArray,
    earth_lco: float,
) -> FloatArray:
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
        s = lco_space(case, a=AnchorSet(overrides=overrides), launch_per_kg_leo=0.0, **kw)
        out[i] = (s.alpha + s.beta * launch_prices) / earth_lco
    return out
