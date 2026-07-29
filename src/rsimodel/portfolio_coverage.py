"""Validate and publish the portfolio-to-industrial-sector evidence crosswalk."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Final, TypedDict, cast

ROOT: Final = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE: Final = ROOT / "params" / "portfolio_sector_coverage.json"
DEFAULT_ROW_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "portfolio_sector_coverage.csv"
)
DEFAULT_SUMMARY_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "portfolio_sector_coverage_summary.csv"
)
DEFAULT_GROUP_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "portfolio_sector_group_summary.csv"
)

SECTORS: Final[tuple[str, ...]] = (
    "power",
    "mining",
    "refining",
    "robotics",
    "machine_tools",
    "construction",
    "thermal",
    "transport",
    "repair",
    "recycling",
    "interconnects_boards",
    "passives_power",
    "sensors_control",
    "packaging_test",
    "mature_logic",
    "advanced_logic_memory",
    "process_equipment_metrology",
    "compute",
)
SECTOR_GROUPS: Final[tuple[str, ...]] = (
    "bulk_material",
    "industrial_equipment",
    "electronics",
    "operations_maintenance",
    "intelligence_compute",
)
EXPECTED_GROUP: Final[dict[str, str]] = {
    "power": "bulk_material",
    "mining": "bulk_material",
    "refining": "bulk_material",
    "robotics": "industrial_equipment",
    "machine_tools": "industrial_equipment",
    "construction": "industrial_equipment",
    "thermal": "industrial_equipment",
    "transport": "operations_maintenance",
    "repair": "operations_maintenance",
    "recycling": "bulk_material",
    "interconnects_boards": "electronics",
    "passives_power": "electronics",
    "sensors_control": "electronics",
    "packaging_test": "electronics",
    "mature_logic": "electronics",
    "advanced_logic_memory": "electronics",
    "process_equipment_metrology": "industrial_equipment",
    "compute": "intelligence_compute",
}
EVIDENCE_TIERS: Final[tuple[str, ...]] = (
    "documented_operating",
    "demonstrated_but_not_scaled",
    "announced_or_under_development",
    "adjacent_capability_only",
    "no_evidence",
)
EXPECTED_TIER_COUNTS: Final[dict[str, int]] = {
    "documented_operating": 12,
    "demonstrated_but_not_scaled": 0,
    "announced_or_under_development": 5,
    "adjacent_capability_only": 0,
    "no_evidence": 1,
}


class NegativeEvidenceProtocol(TypedDict):
    searched: list[str]
    excludedAsSufficientEvidence: list[str]
    meaningOfNoEvidence: str


class PortfolioRecord(TypedDict):
    sector: str
    sectorGroup: str
    entities: str
    initiative: str
    demonstratedOutput: str
    location: str
    scale: str
    upstreamSuppliers: str
    requiredParentTools: str
    offWorldRelevance: str
    evidenceTier: str
    sourceRefs: str
    sourceLocatorDate: str
    residualClosureGap: str
    capabilityExists: bool
    operationalTerrestrialScale: bool
    spaceQualified: bool
    demonstratedOffWorld: bool
    inputsLocallySourced: bool
    productionEquipmentLocallyReproducible: bool
    repairVerificationLocallySupported: bool
    offWorldReproductivelyClosed: bool
    acceptanceGates: str


ROOT_FIELDS: Final[frozenset[str]] = frozenset(
    {"schemaVersion", "asOf", "scope", "negativeEvidenceProtocol", "records"}
)
TEXT_FIELDS: Final[tuple[str, ...]] = (
    "sector",
    "sectorGroup",
    "entities",
    "initiative",
    "demonstratedOutput",
    "location",
    "scale",
    "upstreamSuppliers",
    "requiredParentTools",
    "offWorldRelevance",
    "evidenceTier",
    "sourceRefs",
    "sourceLocatorDate",
    "residualClosureGap",
    "acceptanceGates",
)
BOOLEAN_FIELDS: Final[tuple[str, ...]] = (
    "capabilityExists",
    "operationalTerrestrialScale",
    "spaceQualified",
    "demonstratedOffWorld",
    "inputsLocallySourced",
    "productionEquipmentLocallyReproducible",
    "repairVerificationLocallySupported",
    "offWorldReproductivelyClosed",
)
RECORD_FIELDS: Final[frozenset[str]] = frozenset((*TEXT_FIELDS, *BOOLEAN_FIELDS))
DIMENSION_FIELDS: Final[tuple[str, ...]] = (
    "capabilityExists",
    "operationalTerrestrialScale",
    "spaceQualified",
    "demonstratedOffWorld",
    "inputsLocallySourced",
    "productionEquipmentLocallyReproducible",
    "repairVerificationLocallySupported",
)
ROW_HEADERS: Final[tuple[str, ...]] = (
    "as_of",
    "sector_order",
    "sector",
    "sector_group",
    "entities",
    "initiative",
    "demonstrated_output",
    "location",
    "scale",
    "upstream_suppliers",
    "required_parent_tools",
    "off_world_relevance",
    "evidence_tier",
    "source_refs",
    "source_locator_date",
    "residual_closure_gap",
    "capability_exists",
    "operational_terrestrial_scale",
    "space_qualified",
    "demonstrated_off_world",
    "inputs_locally_sourced",
    "production_equipment_locally_reproducible",
    "repair_verification_locally_supported",
    "off_world_reproductively_closed",
    "acceptance_gates",
)


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array")
    values = cast(list[object], value)
    if not all(isinstance(item, str) and item for item in values):
        raise ValueError(f"{label} values must be non-empty strings")
    return cast(list[str], values)


def _validate_negative_evidence_protocol(value: object) -> NegativeEvidenceProtocol:
    protocol = _object(value, "negativeEvidenceProtocol")
    expected = {"searched", "excludedAsSufficientEvidence", "meaningOfNoEvidence"}
    if set(protocol) != expected:
        raise ValueError("negativeEvidenceProtocol field mismatch")
    searched = _string_list(protocol["searched"], "negativeEvidenceProtocol.searched")
    excluded = _string_list(
        protocol["excludedAsSufficientEvidence"],
        "negativeEvidenceProtocol.excludedAsSufficientEvidence",
    )
    meaning = protocol["meaningOfNoEvidence"]
    if not isinstance(meaning, str) or not meaning:
        raise ValueError("negativeEvidenceProtocol.meaningOfNoEvidence must be non-empty")
    return {
        "searched": searched,
        "excludedAsSufficientEvidence": excluded,
        "meaningOfNoEvidence": meaning,
    }


def load_portfolio_coverage(
    path: Path = DEFAULT_SOURCE,
) -> tuple[str, str, NegativeEvidenceProtocol, list[PortfolioRecord]]:
    """Load the versioned register and enforce its publication invariants."""
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    root = _object(raw, "portfolio coverage root")
    if set(root) != set(ROOT_FIELDS):
        raise ValueError("portfolio coverage root field mismatch")
    if root.get("schemaVersion") != 1:
        raise ValueError("portfolio coverage schemaVersion must be 1")
    as_of = root.get("asOf")
    scope = root.get("scope")
    if not isinstance(as_of, str) or not as_of:
        raise ValueError("portfolio coverage asOf must be a non-empty string")
    if not isinstance(scope, str) or "separate public company" not in scope:
        raise ValueError("portfolio scope must preserve Tesla's separate-company boundary")
    protocol = _validate_negative_evidence_protocol(root.get("negativeEvidenceProtocol"))

    records_value = root.get("records")
    if not isinstance(records_value, list):
        raise ValueError("portfolio coverage records must be an array")
    records: list[PortfolioRecord] = []
    for index, value in enumerate(cast(list[object], records_value)):
        item = _object(value, f"records[{index}]")
        unknown = sorted(set(item) - RECORD_FIELDS)
        missing = sorted(RECORD_FIELDS - set(item))
        if unknown or missing:
            raise ValueError(
                f"records[{index}] field mismatch; missing={missing}, unknown={unknown}"
            )
        if not all(isinstance(item[field], str) for field in TEXT_FIELDS):
            raise ValueError(f"records[{index}] text fields must be strings")
        if not all(isinstance(item[field], bool) for field in BOOLEAN_FIELDS):
            raise ValueError(f"records[{index}] dimension fields must be booleans")
        record = cast(PortfolioRecord, item)
        sector = record["sector"]
        if record["sectorGroup"] != EXPECTED_GROUP.get(sector):
            raise ValueError(f"{sector}: sectorGroup does not match the canonical crosswalk")
        if record["evidenceTier"] not in EVIDENCE_TIERS:
            raise ValueError(f"{sector}: unknown evidenceTier")
        source_refs = record["sourceRefs"].split(";")
        if not source_refs or any(
            re.fullmatch(r"S[1-9][0-9]*", ref) is None for ref in source_refs
        ):
            raise ValueError(f"{sector}: sourceRefs must be semicolon-separated source IDs")
        if not record["sourceLocatorDate"]:
            raise ValueError(f"{sector}: sourceLocatorDate must be explicit")
        if not record["residualClosureGap"]:
            raise ValueError(f"{sector}: residualClosureGap must be explicit")
        if record["acceptanceGates"] != "C01-C08":
            raise ValueError(f"{sector}: all closure acceptance gates C01-C08 must apply")
        if record["demonstratedOffWorld"] and not record["spaceQualified"]:
            raise ValueError(f"{sector}: off-world demonstration requires space qualification")
        if record["offWorldReproductivelyClosed"] and not all(
            record[field] for field in DIMENSION_FIELDS
        ):
            raise ValueError(f"{sector}: reproductive closure requires all seven dimensions")
        records.append(record)

    if tuple(record["sector"] for record in records) != SECTORS:
        raise ValueError("portfolio coverage must contain the canonical 18 sectors in order")
    tier_counts = Counter(record["evidenceTier"] for record in records)
    if {tier: tier_counts[tier] for tier in EVIDENCE_TIERS} != EXPECTED_TIER_COUNTS:
        raise ValueError("portfolio evidence-tier counts do not match the audited vector")
    if any(record["offWorldReproductivelyClosed"] for record in records):
        raise ValueError("the current evidence register cannot claim off-world closure")
    if records[16]["sector"] != "process_equipment_metrology":
        raise ValueError("the explicit parent-tool/metrology blocker must remain addressable")
    return as_of, scope, protocol, records


def dependency_aware_closure(records: list[PortfolioRecord]) -> bool:
    """Return true only when every indispensable sector is reproductively closed."""
    return len(records) == len(SECTORS) and all(
        record["offWorldReproductivelyClosed"] for record in records
    )


def _boolean_text(value: bool) -> str:
    return "true" if value else "false"


def _write_rows(as_of: str, records: list[PortfolioRecord], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(ROW_HEADERS)
        for order, record in enumerate(records, start=1):
            writer.writerow(
                (
                    as_of,
                    order,
                    record["sector"],
                    record["sectorGroup"],
                    record["entities"],
                    record["initiative"],
                    record["demonstratedOutput"],
                    record["location"],
                    record["scale"],
                    record["upstreamSuppliers"],
                    record["requiredParentTools"],
                    record["offWorldRelevance"],
                    record["evidenceTier"],
                    record["sourceRefs"],
                    record["sourceLocatorDate"],
                    record["residualClosureGap"],
                    *(_boolean_text(record[field]) for field in BOOLEAN_FIELDS),
                    record["acceptanceGates"],
                )
            )


def _write_summary(
    as_of: str,
    scope: str,
    records: list[PortfolioRecord],
    output: Path,
) -> None:
    tier_counts = Counter(record["evidenceTier"] for record in records)
    dimension_counts = {
        field: sum(record[field] for record in records) for field in DIMENSION_FIELDS
    }
    closed_count = sum(record["offWorldReproductivelyClosed"] for record in records)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "as_of",
                "scope",
                "total_sectors",
                *EVIDENCE_TIERS,
                "capability_exists",
                "operational_terrestrial_scale",
                "space_qualified",
                "demonstrated_off_world",
                "inputs_locally_sourced",
                "production_equipment_locally_reproducible",
                "repair_verification_locally_supported",
                "off_world_reproductively_closed",
                "dependency_aware_closure",
                "decisive_public_evidence_blocker",
                "interpretation",
            )
        )
        writer.writerow(
            (
                as_of,
                scope,
                len(records),
                *(tier_counts[tier] for tier in EVIDENCE_TIERS),
                *(dimension_counts[field] for field in DIMENSION_FIELDS),
                closed_count,
                _boolean_text(dependency_aware_closure(records)),
                "process_equipment_metrology",
                "A count such as 17 of 18 is not a closure percentage; one indispensable "
                "missing parent-tool chain breaks reproductive closure.",
            )
        )


def _write_group_summary(as_of: str, records: list[PortfolioRecord], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "as_of",
                "sector_group",
                "sector_count",
                *EVIDENCE_TIERS,
                "demonstrated_off_world",
                "off_world_reproductively_closed",
                "dependency_aware_group_closure",
                "open_sectors",
            )
        )
        for group in SECTOR_GROUPS:
            group_records = [record for record in records if record["sectorGroup"] == group]
            tier_counts = Counter(record["evidenceTier"] for record in group_records)
            closed_count = sum(record["offWorldReproductivelyClosed"] for record in group_records)
            open_sectors = ";".join(
                record["sector"]
                for record in group_records
                if not record["offWorldReproductivelyClosed"]
            )
            writer.writerow(
                (
                    as_of,
                    group,
                    len(group_records),
                    *(tier_counts[tier] for tier in EVIDENCE_TIERS),
                    sum(record["demonstratedOffWorld"] for record in group_records),
                    closed_count,
                    _boolean_text(
                        bool(group_records)
                        and all(record["offWorldReproductivelyClosed"] for record in group_records)
                    ),
                    open_sectors,
                )
            )


def write_portfolio_coverage_csvs(
    row_output: Path = DEFAULT_ROW_OUTPUT,
    summary_output: Path = DEFAULT_SUMMARY_OUTPUT,
    group_output: Path = DEFAULT_GROUP_OUTPUT,
    source: Path = DEFAULT_SOURCE,
) -> tuple[Path, Path, Path]:
    """Generate all reader-facing crosswalk views from one validated source."""
    as_of, scope, _, records = load_portfolio_coverage(source)
    for output in (row_output, summary_output, group_output):
        output.parent.mkdir(parents=True, exist_ok=True)
    _write_rows(as_of, records, row_output)
    _write_summary(as_of, scope, records, summary_output)
    _write_group_summary(as_of, records, group_output)
    return row_output, summary_output, group_output
