"""Validate and publish the dated orbital-AI scenario and closure registries.

The JSON register is the only source for named SpaceXAI inputs, simulation
coverage, and the actor-bounded competitor matrix.  It deliberately keeps
company disclosures, regulatory filings, independent studies, and analyst
completion assumptions in separate fields.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TypedDict, cast

ROOT: Final = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE: Final = ROOT / "params" / "orbital_ai_scenario_registry.json"
DEFAULT_INPUT_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "orbital_ai_scenario_inputs.csv"
)
DEFAULT_COVERAGE_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "simulation_scenario_coverage.csv"
)
DEFAULT_CLOSURE_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "orbital_ai_closure_stack.csv"
)
DEFAULT_CLOSURE_SUMMARY_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "orbital_ai_closure_summary.csv"
)
DEFAULT_RESULTS_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "orbital_ai_scenario_results.csv"
)

SCENARIO_ORDER: Final[tuple[str, ...]] = (
    "generic_reference",
    "independent_reference",
    "spacexai_disclosed_design",
    "spacexai_stated_aspiration",
    "spacexai_affiliate_hybrid",
)
PROGRAM_ORDER: Final[tuple[str, ...]] = (
    "spacexai_bounded_ecosystem",
    "google_planet_suncatcher",
    "starcloud",
    "blue_origin_sunrise",
)
CLOSURE_LAYER_ORDER: Final[tuple[str, ...]] = (
    "launch_transport",
    "spacecraft_manufacturing",
    "power_generation",
    "storage_grid_control",
    "communications",
    "ai_compute",
    "models_data",
    "chip_design",
    "chip_fabrication_packaging",
    "robotics",
    "construction",
    "mining",
    "beneficiation",
    "refining",
    "bulk_material_production",
    "maintenance_repair",
    "recycling",
    "capital_equipment_reproduction",
)
SIMULATION_ORDER: Final[tuple[str, ...]] = (
    "orbital_compute_lifecycle_cost",
    "launch_mass_cadence",
    "vehicle_power_thermal",
    "hardware_life_qualification",
    "communications",
    "deployment_growth",
    "constellation_topology",
    "debris_exposure",
    "repair_replacement",
    "physical_closure_supply",
)
INPUT_ANCHOR_ORDER: Final[tuple[str, ...]] = (
    "starmind.compute_payload_kw_peak",
    "starmind.compute_payload_kw_average",
    "starmind.vehicle_efficiency_kw_per_tonne",
    "starmind.vehicle_mass_kg_per_average_kw",
    "starmind.solar_array_kw",
    "starmind.solar_power_density_w_per_m2",
    "starmind.radiator_area_m2",
    "starmind.deployed_height_m",
    "starmind.wingspan_m",
    "aspirations.starship_leo_cost_per_kg",
    "aspirations.starmind_vehicle_efficiency_kw_per_tonne",
    "aspirations.starmind_vehicle_mass_kg_per_average_kw",
    "aspirations.starship_v3_payload_tonnes",
    "aspirations.starship_v4_payload_tonnes",
    "aspirations.orbital_compute_gw_per_year",
    "aspirations.starmind_qualification_multiplier",
    "aspirations.starmind_life_years",
    "aspirations.starmind_utilization",
)
TRACK_PREFIXES: Final[tuple[str, ...]] = (
    "generic",
    "independent",
    "disclosed",
    "aspiration",
    "hybrid",
)
TRACK_STATUSES: Final[frozenset[str]] = frozenset(
    {"included", "axis_marker", "hybrid_completion", "not_parameterizable"}
)
MATURITY_LEVELS: Final[tuple[str, ...]] = (
    "operational",
    "demonstrated",
    "under_development",
    "stated_aspiration",
    "no_evidence",
)
MATURITY_SCORE: Final[dict[str, float]] = {
    "operational": 1.0,
    "demonstrated": 0.75,
    "under_development": 0.35,
    "stated_aspiration": 0.15,
    "no_evidence": 0.0,
}
SOURCE_ID_PATTERN: Final = re.compile(r"S[1-9][0-9]*")
LCO_COMPONENT_HATCHES: Final[tuple[str, ...]] = (
    "////",
    "\\\\\\\\",
    "....",
    "xxxx",
    "----",
)
LCO_SCENARIO_DISPLAY_LABELS: Final[dict[str, str]] = {
    "leo_inference": "LEO",
    "leo_inference_disposable": "LEO disposable",
    "cislunar_batch": "cislunar",
    "lunar_surface": "lunar",
    "starmind_ai1": "AI1 disclosed\n(company statement)",
    "starmind_ai1_disposable": "AI1 disclosed\n(disposable assumption)",
    "starmind_ai1_aspirational": "AI1 targets +\nmodel assumptions",
}
RATIO_LINE_STYLES: Final[tuple[str, ...]] = ("-", "--", ":", "-.")
RATIO_CASE_LABELS: Final[dict[str, str]] = {
    "leo_inference": "generic LEO",
    "cislunar_batch": "generic cislunar",
    "lunar_surface": "generic lunar",
    "starmind_ai1": "SpaceXAI AI1 disclosed design",
}


class ScenarioRecord(TypedDict):
    scenarioId: str
    label: str
    actorBoundary: str
    evidenceClass: str
    maturityState: str
    sourceRefs: str
    sourceSnapshot: str
    companyParameterCount: int
    requiredParameterCount: int
    parameterCompleteness: float
    boundary: str


class InputRecord(TypedDict):
    anchorKey: str
    scenarioId: str
    value: float | None
    low: float | None
    high: float | None
    unit: str
    denominator: str
    maturityState: str
    evidenceClass: str
    sourceRef: str
    sourceDate: str
    sourceLocator: str
    sourceSnapshot: str
    snapshotSha256: str
    directOrDerived: str
    permittedSimulations: list[str]
    note: str


class ProgramRecord(TypedDict):
    programId: str
    label: str
    coreLegalEntities: str
    partnerOrAffiliateEntities: str
    relationshipToSpacexai: str
    sourceRefs: str
    sourceDate: str
    boundary: str


class SimulationRecord(TypedDict):
    simulationId: str
    runner: str
    outputPaths: list[str]
    relevance: str
    genericStatus: str
    genericBoundary: str
    independentStatus: str
    independentBoundary: str
    disclosedStatus: str
    disclosedBoundary: str
    aspirationStatus: str
    aspirationBoundary: str
    hybridStatus: str
    hybridBoundary: str


class ClosureLayer(TypedDict):
    layerId: str
    label: str
    weight: float
    minimumCut: bool
    defaultMissingDependencies: str


class CapabilityRecord(TypedDict):
    programId: str
    layerId: str
    responsibleLegalEntity: str
    relationship: str
    environmentStatus: str
    maturityLevel: str
    demonstratedCapacity: str
    statedTarget: str
    missingDependencies: str
    sourceRefs: str
    sourceDate: str
    evidenceClass: str
    underCommonControl: bool
    offWorldReproductivelyClosed: bool


class NegativeEvidenceProtocol(TypedDict):
    searched: list[str]
    excludedAsSufficientEvidence: list[str]
    meaningOfNoEvidence: str


@dataclass(frozen=True, slots=True)
class OrbitalAIRegistry:
    """Validated registry with stable ordering and actor boundaries."""

    version: str
    as_of: str
    comparison_class: str
    refresh_protocol: str
    landscape_snapshot: str
    landscape_snapshot_sha256: str
    scenarios: tuple[ScenarioRecord, ...]
    inputs: tuple[InputRecord, ...]
    programs: tuple[ProgramRecord, ...]
    simulations: tuple[SimulationRecord, ...]
    layers: tuple[ClosureLayer, ...]
    capabilities: tuple[CapabilityRecord, ...]
    negative_evidence: NegativeEvidenceProtocol


ROOT_FIELDS: Final[frozenset[str]] = frozenset(
    {
        "schemaVersion",
        "registryVersion",
        "asOf",
        "comparisonClass",
        "releaseRefreshProtocol",
        "landscapeSnapshot",
        "landscapeSnapshotSha256",
        "scenarioOrder",
        "scenarios",
        "inputs",
        "programs",
        "simulationCoverage",
        "closureLayers",
        "capabilities",
        "negativeEvidenceProtocol",
    }
)
SCENARIO_FIELDS: Final[frozenset[str]] = frozenset(ScenarioRecord.__annotations__)
INPUT_FIELDS: Final[frozenset[str]] = frozenset(InputRecord.__annotations__)
PROGRAM_FIELDS: Final[frozenset[str]] = frozenset(ProgramRecord.__annotations__)
SIMULATION_FIELDS: Final[frozenset[str]] = frozenset(SimulationRecord.__annotations__)
LAYER_FIELDS: Final[frozenset[str]] = frozenset(ClosureLayer.__annotations__)
CAPABILITY_FIELDS: Final[frozenset[str]] = frozenset(CapabilityRecord.__annotations__)
PROTOCOL_FIELDS: Final[frozenset[str]] = frozenset(NegativeEvidenceProtocol.__annotations__)


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _array(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return cast(list[object], value)


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _number(value: object, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label} must be numeric")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def _integer(value: object, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    return value


def _boolean(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _text_array(value: object, label: str) -> list[str]:
    values = _array(value, label)
    if not values or not all(isinstance(item, str) and item.strip() for item in values):
        raise ValueError(f"{label} must contain non-empty strings")
    return cast(list[str], values)


def _field_set(item: Mapping[str, object], expected: frozenset[str], label: str) -> None:
    missing = sorted(expected - set(item))
    unknown = sorted(set(item) - expected)
    if missing or unknown:
        raise ValueError(f"{label} field mismatch; missing={missing}, unknown={unknown}")


def _source_refs(value: object, label: str) -> str:
    refs = _text(value, label)
    if any(SOURCE_ID_PATTERN.fullmatch(ref) is None for ref in refs.split(";")):
        raise ValueError(f"{label} must be semicolon-separated manuscript source IDs")
    return refs


def _snapshot_path(source_path: Path, relative_path: str) -> Path:
    root = source_path.resolve().parents[1]
    return root / relative_path


def _validate_scenarios(root: Mapping[str, object]) -> tuple[ScenarioRecord, ...]:
    declared_order = tuple(_text_array(root["scenarioOrder"], "scenarioOrder"))
    if declared_order != SCENARIO_ORDER:
        raise ValueError("scenarioOrder must match the canonical five-track order")
    records: list[ScenarioRecord] = []
    for index, value in enumerate(_array(root["scenarios"], "scenarios")):
        item = _object(value, f"scenarios[{index}]")
        _field_set(item, SCENARIO_FIELDS, f"scenarios[{index}]")
        for field in (
            "scenarioId",
            "label",
            "actorBoundary",
            "evidenceClass",
            "maturityState",
            "sourceRefs",
            "sourceSnapshot",
            "boundary",
        ):
            _text(item[field], f"scenarios[{index}].{field}")
        company_count = _integer(
            item["companyParameterCount"], f"scenarios[{index}].companyParameterCount"
        )
        required_count = _integer(
            item["requiredParameterCount"], f"scenarios[{index}].requiredParameterCount"
        )
        completeness = _number(
            item["parameterCompleteness"], f"scenarios[{index}].parameterCompleteness"
        )
        if company_count < 0 or required_count < 0 or not 0.0 <= completeness <= 1.0:
            raise ValueError(f"scenarios[{index}] has invalid parameter counts")
        if required_count and not math.isclose(
            completeness, company_count / required_count, abs_tol=1e-12
        ):
            raise ValueError(f"scenarios[{index}] parameterCompleteness is inconsistent")
        records.append(cast(ScenarioRecord, item))
    if tuple(record["scenarioId"] for record in records) != SCENARIO_ORDER:
        raise ValueError("scenarios must appear exactly once in canonical order")
    if "excludes Tesla" not in records[2]["actorBoundary"]:
        raise ValueError("the disclosed design must exclude Tesla")
    if "separately identified" not in records[4]["actorBoundary"]:
        raise ValueError("the affiliate hybrid must name separate legal entities")
    return tuple(records)


def _validate_inputs(root: Mapping[str, object], source_path: Path) -> tuple[InputRecord, ...]:
    records: list[InputRecord] = []
    for index, value in enumerate(_array(root["inputs"], "inputs")):
        item = _object(value, f"inputs[{index}]")
        _field_set(item, INPUT_FIELDS, f"inputs[{index}]")
        for field in (
            "anchorKey",
            "scenarioId",
            "unit",
            "denominator",
            "maturityState",
            "evidenceClass",
            "sourceRef",
            "sourceDate",
            "sourceLocator",
            "sourceSnapshot",
            "snapshotSha256",
            "directOrDerived",
            "note",
        ):
            _text(item[field], f"inputs[{index}].{field}")
        _source_refs(item["sourceRef"], f"inputs[{index}].sourceRef")
        permitted = _text_array(
            item["permittedSimulations"], f"inputs[{index}].permittedSimulations"
        )
        if any(simulation not in SIMULATION_ORDER for simulation in permitted):
            raise ValueError(f"inputs[{index}] names an unknown permitted simulation")
        value_number = item["value"]
        low_number = item["low"]
        high_number = item["high"]
        has_value = value_number is not None
        has_range = low_number is not None or high_number is not None
        if has_value == has_range:
            raise ValueError(f"inputs[{index}] must define exactly one value or range")
        if has_value:
            _number(value_number, f"inputs[{index}].value")
            if low_number is not None or high_number is not None:
                raise ValueError(f"inputs[{index}] scalar cannot also define a range")
        else:
            low = _number(low_number, f"inputs[{index}].low")
            high = _number(high_number, f"inputs[{index}].high")
            if low > high:
                raise ValueError(f"inputs[{index}] low exceeds high")
        scenario_id = cast(str, item["scenarioId"])
        if scenario_id not in SCENARIO_ORDER:
            raise ValueError(f"inputs[{index}] has an unknown scenarioId")
        maturity = cast(str, item["maturityState"])
        evidence = cast(str, item["evidenceClass"])
        if maturity == "observed_operation":
            raise ValueError("named design and target inputs cannot claim observed operation")
        if maturity == "hybrid_completion" and evidence != "ASSUMPTION":
            raise ValueError("hybrid-completion inputs must be labelled ASSUMPTION")
        if evidence == "ASSUMPTION" and maturity != "hybrid_completion":
            raise ValueError("analyst completion inputs must use hybrid_completion maturity")
        snapshot = _snapshot_path(source_path, cast(str, item["sourceSnapshot"]))
        if not snapshot.is_file():
            raise ValueError(f"inputs[{index}] source snapshot is missing: {snapshot}")
        digest = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        if digest != item["snapshotSha256"]:
            raise ValueError(f"inputs[{index}] source snapshot hash is stale")
        records.append(cast(InputRecord, item))
    if tuple(record["anchorKey"] for record in records) != INPUT_ANCHOR_ORDER:
        raise ValueError("inputs must contain the canonical 18 anchors in order")
    return tuple(records)


def _validate_programs(root: Mapping[str, object]) -> tuple[ProgramRecord, ...]:
    records: list[ProgramRecord] = []
    for index, value in enumerate(_array(root["programs"], "programs")):
        item = _object(value, f"programs[{index}]")
        _field_set(item, PROGRAM_FIELDS, f"programs[{index}]")
        for field in PROGRAM_FIELDS:
            _text(item[field], f"programs[{index}].{field}")
        _source_refs(item["sourceRefs"], f"programs[{index}].sourceRefs")
        records.append(cast(ProgramRecord, item))
    if tuple(record["programId"] for record in records) != PROGRAM_ORDER:
        raise ValueError("programs must appear exactly once in canonical order")
    if "not controlled" not in records[0]["boundary"]:
        raise ValueError("the SpaceXAI ecosystem boundary must preserve Tesla control status")
    return tuple(records)


def _validate_simulations(root: Mapping[str, object]) -> tuple[SimulationRecord, ...]:
    records: list[SimulationRecord] = []
    output_paths: set[str] = set()
    for index, value in enumerate(_array(root["simulationCoverage"], "simulationCoverage")):
        item = _object(value, f"simulationCoverage[{index}]")
        _field_set(item, SIMULATION_FIELDS, f"simulationCoverage[{index}]")
        for field in (
            "simulationId",
            "runner",
            "relevance",
            *(f"{prefix}Status" for prefix in TRACK_PREFIXES),
            *(f"{prefix}Boundary" for prefix in TRACK_PREFIXES),
        ):
            _text(item[field], f"simulationCoverage[{index}].{field}")
        paths = _text_array(item["outputPaths"], f"simulationCoverage[{index}].outputPaths")
        for output_path in paths:
            path = Path(output_path)
            if not output_path.startswith("outputs/") or path.is_absolute() or ".." in path.parts:
                raise ValueError(f"simulationCoverage[{index}] has an unsafe output path")
            output_paths.add(output_path)
        for prefix in TRACK_PREFIXES:
            status = cast(str, item[f"{prefix}Status"])
            if status not in TRACK_STATUSES:
                raise ValueError(f"simulationCoverage[{index}].{prefix}Status is not canonical")
        records.append(cast(SimulationRecord, item))
    if tuple(record["simulationId"] for record in records) != SIMULATION_ORDER:
        raise ValueError("simulationCoverage must contain all relevant families in order")
    if DEFAULT_RESULTS_OUTPUT.relative_to(ROOT).as_posix() not in output_paths:
        raise ValueError("scenario results must be within the declared coverage boundary")
    return tuple(records)


def _validate_layers(root: Mapping[str, object]) -> tuple[ClosureLayer, ...]:
    records: list[ClosureLayer] = []
    for index, value in enumerate(_array(root["closureLayers"], "closureLayers")):
        item = _object(value, f"closureLayers[{index}]")
        _field_set(item, LAYER_FIELDS, f"closureLayers[{index}]")
        for field in ("layerId", "label", "defaultMissingDependencies"):
            _text(item[field], f"closureLayers[{index}].{field}")
        if _number(item["weight"], f"closureLayers[{index}].weight") <= 0:
            raise ValueError(f"closureLayers[{index}].weight must be positive")
        _boolean(item["minimumCut"], f"closureLayers[{index}].minimumCut")
        records.append(cast(ClosureLayer, item))
    if tuple(record["layerId"] for record in records) != CLOSURE_LAYER_ORDER:
        raise ValueError("closureLayers must contain the canonical 18 layers in order")
    return tuple(records)


def _validate_capabilities(
    root: Mapping[str, object],
    layers: tuple[ClosureLayer, ...],
) -> tuple[CapabilityRecord, ...]:
    valid_layers = {layer["layerId"] for layer in layers}
    records: list[CapabilityRecord] = []
    seen: set[tuple[str, str]] = set()
    for index, value in enumerate(_array(root["capabilities"], "capabilities")):
        item = _object(value, f"capabilities[{index}]")
        _field_set(item, CAPABILITY_FIELDS, f"capabilities[{index}]")
        for field in (
            "programId",
            "layerId",
            "responsibleLegalEntity",
            "relationship",
            "environmentStatus",
            "maturityLevel",
            "demonstratedCapacity",
            "statedTarget",
            "missingDependencies",
            "sourceRefs",
            "sourceDate",
            "evidenceClass",
        ):
            _text(item[field], f"capabilities[{index}].{field}")
        program_id = cast(str, item["programId"])
        layer_id = cast(str, item["layerId"])
        maturity = cast(str, item["maturityLevel"])
        if program_id not in PROGRAM_ORDER or layer_id not in valid_layers:
            raise ValueError(f"capabilities[{index}] has an unknown program or layer")
        if maturity not in MATURITY_LEVELS[:-1]:
            raise ValueError(f"capabilities[{index}] has a noncanonical maturity level")
        _source_refs(item["sourceRefs"], f"capabilities[{index}].sourceRefs")
        common_control = _boolean(
            item["underCommonControl"], f"capabilities[{index}].underCommonControl"
        )
        closed = _boolean(
            item["offWorldReproductivelyClosed"],
            f"capabilities[{index}].offWorldReproductivelyClosed",
        )
        if closed:
            raise ValueError("the current register cannot claim off-world closure")
        entity = cast(str, item["responsibleLegalEntity"])
        if "Tesla" in entity and common_control:
            raise ValueError("Tesla must remain outside SpaceXAI common control")
        key = (program_id, layer_id)
        if key in seen:
            raise ValueError(f"duplicate capability record: {key}")
        seen.add(key)
        records.append(cast(CapabilityRecord, item))
    spacex_layers = {
        record["layerId"]
        for record in records
        if record["programId"] == "spacexai_bounded_ecosystem"
    }
    if spacex_layers != set(CLOSURE_LAYER_ORDER) - {"capital_equipment_reproduction"}:
        raise ValueError("the dated SpaceXAI breadth boundary must remain 17 of 18 layers")
    return tuple(records)


def _validate_negative_evidence(root: Mapping[str, object]) -> NegativeEvidenceProtocol:
    item = _object(root["negativeEvidenceProtocol"], "negativeEvidenceProtocol")
    _field_set(item, PROTOCOL_FIELDS, "negativeEvidenceProtocol")
    _text_array(item["searched"], "negativeEvidenceProtocol.searched")
    _text_array(
        item["excludedAsSufficientEvidence"],
        "negativeEvidenceProtocol.excludedAsSufficientEvidence",
    )
    meaning = _text(item["meaningOfNoEvidence"], "negativeEvidenceProtocol.meaningOfNoEvidence")
    if "not proof" not in meaning:
        raise ValueError("no_evidence must not be treated as proof of absence")
    return cast(NegativeEvidenceProtocol, item)


def load_orbital_ai_registry(source: Path = DEFAULT_SOURCE) -> OrbitalAIRegistry:
    """Load the registry and enforce its evidence, ordering, and actor boundaries."""
    raw: object = json.loads(source.read_text(encoding="utf-8"))
    root = _object(raw, "orbital AI registry")
    _field_set(root, ROOT_FIELDS, "orbital AI registry")
    if root["schemaVersion"] != 1:
        raise ValueError("orbital AI registry schemaVersion must be 1")
    version = _text(root["registryVersion"], "registryVersion")
    as_of = _text(root["asOf"], "asOf")
    if version != as_of:
        raise ValueError("registryVersion and asOf must match")
    comparison_class = _text(root["comparisonClass"], "comparisonClass")
    refresh_protocol = _text(root["releaseRefreshProtocol"], "releaseRefreshProtocol")
    if "every release" not in refresh_protocol:
        raise ValueError("the competitor refresh protocol must apply to every release")
    landscape_snapshot = _text(root["landscapeSnapshot"], "landscapeSnapshot")
    landscape_hash = _text(root["landscapeSnapshotSha256"], "landscapeSnapshotSha256")
    snapshot_path = _snapshot_path(source, landscape_snapshot)
    if not snapshot_path.is_file():
        raise ValueError(f"landscape snapshot is missing: {snapshot_path}")
    if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != landscape_hash:
        raise ValueError("landscape snapshot hash is stale")
    scenarios = _validate_scenarios(root)
    inputs = _validate_inputs(root, source)
    programs = _validate_programs(root)
    simulations = _validate_simulations(root)
    layers = _validate_layers(root)
    capabilities = _validate_capabilities(root, layers)
    negative_evidence = _validate_negative_evidence(root)
    return OrbitalAIRegistry(
        version=version,
        as_of=as_of,
        comparison_class=comparison_class,
        refresh_protocol=refresh_protocol,
        landscape_snapshot=landscape_snapshot,
        landscape_snapshot_sha256=landscape_hash,
        scenarios=scenarios,
        inputs=inputs,
        programs=programs,
        simulations=simulations,
        layers=layers,
        capabilities=capabilities,
        negative_evidence=negative_evidence,
    )


def scenario_anchor_tree(source: Path = DEFAULT_SOURCE) -> dict[str, dict[str, dict[str, object]]]:
    """Return the named scenario inputs in the nested anchors.yaml shape."""
    registry = load_orbital_ai_registry(source)
    tree: dict[str, dict[str, dict[str, object]]] = {}
    for record in registry.inputs:
        group, name = record["anchorKey"].split(".", maxsplit=1)
        entry: dict[str, object] = {
            "source_class": record["evidenceClass"],
            "note": (
                f"{record['note']} Source {record['sourceRef']}; "
                f"{record['sourceDate']}; {record['sourceLocator']}."
            ),
        }
        if record["value"] is not None:
            entry["value"] = record["value"]
        else:
            entry["low"] = record["low"]
            entry["high"] = record["high"]
        tree.setdefault(group, {})[name] = entry
    return tree


def scenario_labels(source: Path = DEFAULT_SOURCE) -> dict[str, str]:
    """Return stable display labels keyed by canonical scenario ID."""
    return {
        record["scenarioId"]: record["label"]
        for record in load_orbital_ai_registry(source).scenarios
    }


def _boolean_text(value: bool) -> str:
    return "true" if value else "false"


def _write_inputs(registry: OrbitalAIRegistry, output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "registry_version",
                "as_of",
                "scenario_order",
                "scenario_id",
                "anchor_key",
                "value",
                "low",
                "high",
                "unit",
                "denominator",
                "maturity_state",
                "evidence_class",
                "source_ref",
                "source_date",
                "source_locator",
                "source_snapshot",
                "snapshot_sha256",
                "direct_or_derived",
                "permitted_simulations",
                "note",
            )
        )
        order = {scenario_id: index for index, scenario_id in enumerate(SCENARIO_ORDER, 1)}
        for record in registry.inputs:
            writer.writerow(
                (
                    registry.version,
                    registry.as_of,
                    order[record["scenarioId"]],
                    record["scenarioId"],
                    record["anchorKey"],
                    "" if record["value"] is None else record["value"],
                    "" if record["low"] is None else record["low"],
                    "" if record["high"] is None else record["high"],
                    record["unit"],
                    record["denominator"],
                    record["maturityState"],
                    record["evidenceClass"],
                    record["sourceRef"],
                    record["sourceDate"],
                    record["sourceLocator"],
                    record["sourceSnapshot"],
                    record["snapshotSha256"],
                    record["directOrDerived"],
                    ";".join(record["permittedSimulations"]),
                    record["note"],
                )
            )


def _write_coverage(registry: OrbitalAIRegistry, output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "registry_version",
                "as_of",
                "simulation_order",
                "simulation_id",
                "runner",
                "output_path",
                "relevance",
                "generic_status",
                "generic_boundary",
                "independent_status",
                "independent_boundary",
                "spacexai_disclosed_status",
                "spacexai_disclosed_boundary",
                "spacexai_aspiration_status",
                "spacexai_aspiration_boundary",
                "spacexai_affiliate_hybrid_status",
                "spacexai_affiliate_hybrid_boundary",
            )
        )
        for simulation_order, record in enumerate(registry.simulations, 1):
            for output_path in record["outputPaths"]:
                writer.writerow(
                    (
                        registry.version,
                        registry.as_of,
                        simulation_order,
                        record["simulationId"],
                        record["runner"],
                        output_path,
                        record["relevance"],
                        record["genericStatus"],
                        record["genericBoundary"],
                        record["independentStatus"],
                        record["independentBoundary"],
                        record["disclosedStatus"],
                        record["disclosedBoundary"],
                        record["aspirationStatus"],
                        record["aspirationBoundary"],
                        record["hybridStatus"],
                        record["hybridBoundary"],
                    )
                )


def expanded_closure_rows(
    registry: OrbitalAIRegistry,
) -> tuple[tuple[ProgramRecord, ClosureLayer, CapabilityRecord | None], ...]:
    """Expand sparse evidence records to the complete 18-by-program matrix."""
    by_key = {(record["programId"], record["layerId"]): record for record in registry.capabilities}
    return tuple(
        (program, layer, by_key.get((program["programId"], layer["layerId"])))
        for program in registry.programs
        for layer in registry.layers
    )


def _write_closure_stack(registry: OrbitalAIRegistry, output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "registry_version",
                "as_of",
                "comparison_class",
                "program_order",
                "program_id",
                "program_label",
                "layer_order",
                "layer_id",
                "layer_label",
                "weight",
                "minimum_cut",
                "responsible_legal_entity",
                "relationship",
                "environment_status",
                "maturity_level",
                "demonstrated_capacity",
                "stated_target",
                "missing_dependencies",
                "source_refs",
                "source_date",
                "evidence_class",
                "under_common_control",
                "off_world_reproductively_closed",
                "program_boundary",
                "negative_evidence_boundary",
            )
        )
        program_order = {program_id: index for index, program_id in enumerate(PROGRAM_ORDER, 1)}
        layer_order = {layer_id: index for index, layer_id in enumerate(CLOSURE_LAYER_ORDER, 1)}
        for program, layer, capability in expanded_closure_rows(registry):
            writer.writerow(
                (
                    registry.version,
                    registry.as_of,
                    registry.comparison_class,
                    program_order[program["programId"]],
                    program["programId"],
                    program["label"],
                    layer_order[layer["layerId"]],
                    layer["layerId"],
                    layer["label"],
                    layer["weight"],
                    _boolean_text(layer["minimumCut"]),
                    "" if capability is None else capability["responsibleLegalEntity"],
                    "" if capability is None else capability["relationship"],
                    "no qualifying public record"
                    if capability is None
                    else capability["environmentStatus"],
                    "no_evidence" if capability is None else capability["maturityLevel"],
                    "" if capability is None else capability["demonstratedCapacity"],
                    "" if capability is None else capability["statedTarget"],
                    layer["defaultMissingDependencies"]
                    if capability is None
                    else capability["missingDependencies"],
                    program["sourceRefs"] if capability is None else capability["sourceRefs"],
                    program["sourceDate"] if capability is None else capability["sourceDate"],
                    "negative_evidence_protocol"
                    if capability is None
                    else capability["evidenceClass"],
                    "false"
                    if capability is None
                    else _boolean_text(capability["underCommonControl"]),
                    "false"
                    if capability is None
                    else _boolean_text(capability["offWorldReproductivelyClosed"]),
                    program["boundary"],
                    registry.negative_evidence["meaningOfNoEvidence"],
                )
            )


def _closure_summary_rows(registry: OrbitalAIRegistry) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    total_weight = sum(layer["weight"] for layer in registry.layers)
    expanded = expanded_closure_rows(registry)
    for program in registry.programs:
        program_rows = [
            (layer, capability)
            for row_program, layer, capability in expanded
            if row_program["programId"] == program["programId"]
        ]
        maturity = Counter(
            "no_evidence" if capability is None else capability["maturityLevel"]
            for _, capability in program_rows
        )
        weighted_breadth = sum(
            layer["weight"]
            * MATURITY_SCORE["no_evidence" if capability is None else capability["maturityLevel"]]
            for layer, capability in program_rows
        )
        minimum_cut_gaps = [
            layer["layerId"]
            for layer, capability in program_rows
            if layer["minimumCut"] and capability is None
        ]
        missing_weights = [
            layer["weight"] for layer, capability in program_rows if capability is None
        ]
        evidenced_count = sum(capability is not None for _, capability in program_rows)
        common_control_count = sum(
            capability is not None and capability["underCommonControl"]
            for _, capability in program_rows
        )
        closed_count = sum(
            capability is not None and capability["offWorldReproductivelyClosed"]
            for _, capability in program_rows
        )
        missing_weight = sum(missing_weights)
        rows.append(
            {
                "program_id": program["programId"],
                "program_label": program["label"],
                "evidenced_layers": evidenced_count,
                **{level: maturity[level] for level in MATURITY_LEVELS},
                "weighted_breadth_score": weighted_breadth / total_weight,
                "under_common_control_evidenced_layers": common_control_count,
                "under_common_control_fraction_of_evidenced": (
                    common_control_count / evidenced_count if evidenced_count else 0.0
                ),
                "minimum_cut_gap_count": len(minimum_cut_gaps),
                "minimum_cut_gaps": ";".join(minimum_cut_gaps),
                "missing_dependency_weight": missing_weight,
                "largest_missing_weight_share": (
                    max(missing_weights) / missing_weight if missing_weights else 0.0
                ),
                "off_world_closed_layers": closed_count,
                "demonstrated_closure_fraction": closed_count / len(registry.layers),
                "dependency_aware_off_world_closure": False,
                "boundary": program["boundary"],
            }
        )
    ranked = sorted(
        rows,
        key=lambda row: (
            -cast(float, row["weighted_breadth_score"]),
            -cast(int, row["evidenced_layers"]),
            cast(str, row["program_id"]),
        ),
    )
    rank = {cast(str, row["program_id"]): index for index, row in enumerate(ranked, 1)}
    for row in rows:
        row["breadth_rank"] = rank[cast(str, row["program_id"])]
    return rows


def _write_closure_summary(registry: OrbitalAIRegistry, output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "registry_version",
                "as_of",
                "program_id",
                "program_label",
                "breadth_rank",
                "total_layers",
                "evidenced_layers",
                *MATURITY_LEVELS,
                "weighted_breadth_score",
                "under_common_control_evidenced_layers",
                "under_common_control_fraction_of_evidenced",
                "minimum_cut_gap_count",
                "minimum_cut_gaps",
                "missing_dependency_weight",
                "largest_missing_weight_share",
                "off_world_closed_layers",
                "demonstrated_closure_fraction",
                "dependency_aware_off_world_closure",
                "interpretation",
                "boundary",
            )
        )
        for row in _closure_summary_rows(registry):
            writer.writerow(
                (
                    registry.version,
                    registry.as_of,
                    row["program_id"],
                    row["program_label"],
                    row["breadth_rank"],
                    len(registry.layers),
                    row["evidenced_layers"],
                    *(row[level] for level in MATURITY_LEVELS),
                    f"{cast(float, row['weighted_breadth_score']):.9f}",
                    row["under_common_control_evidenced_layers"],
                    f"{cast(float, row['under_common_control_fraction_of_evidenced']):.9f}",
                    row["minimum_cut_gap_count"],
                    row["minimum_cut_gaps"],
                    row["missing_dependency_weight"],
                    f"{cast(float, row['largest_missing_weight_share']):.9f}",
                    row["off_world_closed_layers"],
                    f"{cast(float, row['demonstrated_closure_fraction']):.9f}",
                    _boolean_text(cast(bool, row["dependency_aware_off_world_closure"])),
                    "Breadth is an evidence-weighted comparison, not a closure "
                    "percentage. Reproductive closure requires every indispensable "
                    "off-world dependency and remains false for every program.",
                    row["boundary"],
                )
            )


def _write_scenario_results(registry: OrbitalAIRegistry, output: Path) -> None:
    from .lco import AnchorSet, lco_earth, lco_space, orbital_ai_scale

    scenarios = {record["scenarioId"]: record for record in registry.scenarios}
    earth = lco_earth("base").lco
    generic_serviceable = lco_space("leo_inference")
    generic_disposable = lco_space("leo_inference", architecture="integrated_disposable")
    disclosed_serviceable = lco_space("starmind_ai1")
    disclosed_disposable = lco_space("starmind_ai1", architecture="integrated_disposable")
    aspiration_serviceable = lco_space("starmind_ai1_aspirational")
    anchors = AnchorSet()
    target_gw = anchors("aspirations.orbital_compute_gw_per_year")
    target_efficiency = anchors("aspirations.starmind_vehicle_efficiency_kw_per_tonne")
    disclosed_efficiency = anchors("starmind.vehicle_efficiency_kw_per_tonne")
    v3_payload = anchors("aspirations.starship_v3_payload_tonnes")
    v4_payload = anchors("aspirations.starship_v4_payload_tonnes")
    average_vehicle_kw = anchors("starmind.compute_payload_kw_average")
    target_v3 = orbital_ai_scale(target_gw, target_efficiency, v3_payload, average_vehicle_kw)
    target_v4 = orbital_ai_scale(target_gw, target_efficiency, v4_payload, average_vehicle_kw)
    disclosed_eff_v3 = orbital_ai_scale(
        target_gw, disclosed_efficiency, v3_payload, average_vehicle_kw
    )
    independent_marker = anchors("claims.suncatcher_launch_feasibility_per_kg")

    rows: list[tuple[str, str, str, float | None, str, str, str]] = [
        (
            "generic_reference",
            "leo_serviceable_lco",
            "computed",
            generic_serviceable.lco,
            "USD_per_frontier_equivalent_kW_year",
            "central generic anchors",
            "Actor-neutral LEO lifecycle-cost result.",
        ),
        (
            "generic_reference",
            "leo_disposable_lco",
            "computed",
            generic_disposable.lco,
            "USD_per_frontier_equivalent_kW_year",
            "central generic anchors",
            "Infrastructure and compute retire together.",
        ),
        (
            "generic_reference",
            "earth_base_lco",
            "computed",
            earth,
            "USD_per_frontier_equivalent_kW_year",
            "central responding-Earth anchors",
            "Common Earth comparison denominator.",
        ),
        (
            "independent_reference",
            "suncatcher_launch_feasibility_marker",
            "axis_marker",
            independent_marker,
            "USD_per_kg_to_LEO",
            "technical report S32",
            "Launch-versus-electricity feasibility marker; not a full-system crossover.",
        ),
        (
            "spacexai_disclosed_design",
            "ai1_serviceable_lco",
            "hybrid_completion",
            disclosed_serviceable.lco,
            "USD_per_frontier_equivalent_kW_year",
            "AI1 disclosed mass/power plus generic missing cost, life, and utilization",
            "No commissioned AI1 cluster is established.",
        ),
        (
            "spacexai_disclosed_design",
            "ai1_serviceable_lco_ratio_to_earth",
            "hybrid_completion",
            disclosed_serviceable.lco / earth,
            "ratio",
            "same inputs as ai1_serviceable_lco",
            "Comparison against the responsive central Earth case.",
        ),
        (
            "spacexai_disclosed_design",
            "ai1_disposable_lco",
            "hybrid_completion",
            disclosed_disposable.lco,
            "USD_per_frontier_equivalent_kW_year",
            "AI1 disclosed mass/power plus generic missing cost, life, and utilization",
            "Disposable architecture is a model branch, not a disclosed operating mode.",
        ),
        (
            "spacexai_disclosed_design",
            "ai1_mass",
            "hybrid_completion",
            disclosed_serviceable.mass_kg_per_kw,
            "kg_per_average_kW",
            "derived AI1 interpretation range",
            "Central value preserves the peak-versus-average ambiguity.",
        ),
        (
            "spacexai_disclosed_design",
            "ai1_array_to_average_load_ratio",
            "axis_marker",
            anchors("starmind.solar_array_kw") / average_vehicle_kw,
            "ratio",
            "direct AI1 specifications",
            "Nameplate array power divided by average compute payload.",
        ),
        (
            "spacexai_stated_aspiration",
            "aspirational_serviceable_lco",
            "hybrid_completion",
            aspiration_serviceable.lco,
            "USD_per_frontier_equivalent_kW_year",
            "company targets plus three favorable analyst assumptions",
            "Deterministic sensitivity; excluded from Monte Carlo.",
        ),
        (
            "spacexai_stated_aspiration",
            "aspirational_serviceable_lco_ratio_to_earth",
            "hybrid_completion",
            aspiration_serviceable.lco / earth,
            "ratio",
            "same inputs as aspirational_serviceable_lco",
            "Targets and assumptions are point values, not success probabilities.",
        ),
        (
            "spacexai_stated_aspiration",
            "target_deployed_mass_per_year",
            "axis_marker",
            target_v3["mass_tonnes"],
            "metric_tonnes_per_year",
            "100 GW/year and 100 kW/t company targets",
            "Unit conversion, not an achieved production or launch cadence.",
        ),
        (
            "spacexai_stated_aspiration",
            "target_v3_launches_per_year",
            "axis_marker",
            target_v3["launches_per_year"],
            "full_payload_equivalent_launches_per_year",
            "100 GW/year, 100 kW/t, and 100 t V3 targets",
            "Full-payload arithmetic; not an operating trajectory.",
        ),
        (
            "spacexai_stated_aspiration",
            "target_v4_launches_per_year",
            "axis_marker",
            target_v4["launches_per_year"],
            "full_payload_equivalent_launches_per_year",
            "100 GW/year, 100 kW/t, and 200 t V4 targets",
            "Full-payload arithmetic; not an operating trajectory.",
        ),
        (
            "spacexai_stated_aspiration",
            "target_ai1_equivalent_spacecraft_per_year",
            "axis_marker",
            target_v3["spacecraft_count"],
            "AI1_equivalent_spacecraft_per_year",
            "100 GW/year target divided by 120 kW average payload",
            "Unit conversion; manufacturing and commissioning are unresolved.",
        ),
        (
            "spacexai_stated_aspiration",
            "disclosed_efficiency_v3_launches_per_year",
            "axis_marker",
            disclosed_eff_v3["launches_per_year"],
            "full_payload_equivalent_launches_per_year",
            "100 GW/year target, 70 kW/t AI1 design, and 100 t V3 target",
            "Shows the load imposed by the disclosed efficiency instead of the target.",
        ),
        (
            "spacexai_affiliate_hybrid",
            "affiliate_transfer_result",
            "not_parameterizable",
            None,
            "not_applicable",
            "no commensurable guaranteed transfer vector",
            "Tesla adjacency supplies no verified orbital cost, qualification, "
            "availability, or closure parameter.",
        ),
    ]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "registry_version",
                "as_of",
                "scenario_order",
                "scenario_id",
                "scenario_label",
                "evidence_class",
                "maturity_state",
                "source_snapshot",
                "parameter_completeness",
                "boundary",
                "metric_id",
                "metric_status",
                "metric_value",
                "metric_unit",
                "input_composition",
                "interpretation",
            )
        )
        scenario_order = {scenario_id: index for index, scenario_id in enumerate(SCENARIO_ORDER, 1)}
        for (
            scenario_id,
            metric_id,
            status,
            value,
            unit,
            composition,
            interpretation,
        ) in rows:
            scenario = scenarios[scenario_id]
            writer.writerow(
                (
                    registry.version,
                    registry.as_of,
                    scenario_order[scenario_id],
                    scenario_id,
                    scenario["label"],
                    scenario["evidenceClass"],
                    scenario["maturityState"],
                    scenario["sourceSnapshot"],
                    scenario["parameterCompleteness"],
                    scenario["boundary"],
                    metric_id,
                    status,
                    "" if value is None else f"{value:.9f}",
                    unit,
                    composition,
                    interpretation,
                )
            )


def write_orbital_ai_scenario_csvs(
    input_output: Path = DEFAULT_INPUT_OUTPUT,
    coverage_output: Path = DEFAULT_COVERAGE_OUTPUT,
    closure_output: Path = DEFAULT_CLOSURE_OUTPUT,
    closure_summary_output: Path = DEFAULT_CLOSURE_SUMMARY_OUTPUT,
    results_output: Path = DEFAULT_RESULTS_OUTPUT,
    source: Path = DEFAULT_SOURCE,
) -> tuple[Path, Path, Path, Path, Path]:
    """Generate five reader-facing views from the one validated registry."""
    registry = load_orbital_ai_registry(source)
    outputs = (
        input_output,
        coverage_output,
        closure_output,
        closure_summary_output,
        results_output,
    )
    for output in outputs:
        output.parent.mkdir(parents=True, exist_ok=True)
    _write_inputs(registry, input_output)
    _write_coverage(registry, coverage_output)
    _write_closure_stack(registry, closure_output)
    _write_closure_summary(registry, closure_summary_output)
    _write_scenario_results(registry, results_output)
    return outputs
