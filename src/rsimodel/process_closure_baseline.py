"""Generate the honest failed public-evidence process-closure baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from rsimodel.process_closure import (
    ProcessClosureContract,
    evaluate_process_closure_bundle,
    load_process_closure_contract,
    validate_process_closure_contract,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE_NOTE = Path("docs/sources/process-closure-public-evidence-2026-07-29.md")
PORTFOLIO_REGISTER = Path("params/portfolio_sector_coverage.json")
CLAIM_PROVENANCE = Path("params/claim_provenance.yaml")
QUERY_CODE = Path("src/rsimodel/process_closure_baseline.py")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_portfolio_records(root: Path) -> list[dict[str, object]]:
    value: object = json.loads((root / PORTFOLIO_REGISTER).read_text(encoding="utf-8"))
    if not isinstance(value, Mapping):
        raise ValueError("portfolio sector register must contain a records array")
    value_mapping = cast(Mapping[object, object], value)
    records_value = value_mapping.get("records")
    if not isinstance(records_value, list):
        raise ValueError("portfolio sector register must contain a records array")
    records: list[dict[str, object]] = []
    for index, raw_record in enumerate(cast(list[object], records_value)):
        if not isinstance(raw_record, Mapping):
            raise ValueError(f"portfolio sector record {index} must be an object")
        record_mapping = cast(Mapping[object, object], raw_record)
        if not all(isinstance(key, str) for key in record_mapping):
            raise ValueError(f"portfolio sector record {index} keys must be strings")
        record = {str(key): child for key, child in record_mapping.items()}
        if not isinstance(record.get("sector"), str):
            raise ValueError(f"portfolio sector record {index} is missing sector")
        records.append(record)
    return records


def _unknown(reason: str) -> dict[str, object]:
    return {
        "evidence_status": "not_disclosed_or_not_measured",
        "reason": reason,
    }


def _edge(
    *,
    edge_id: str,
    input_node: str,
    output_node: str,
    process_stage: str,
    boundary: str,
) -> dict[str, object]:
    unknown = _unknown(boundary)
    return {
        "edge_id": edge_id,
        "input_node": input_node,
        "output_node": output_node,
        "process_stage": process_stage,
        "stoichiometry_or_bom": unknown,
        "quantity_and_units": unknown,
        "yield_distribution": unknown,
        "energy_distribution": unknown,
        "contamination_and_rework": unknown,
        "consumables_and_tool_wear": unknown,
        "capacity_and_cycle_time": unknown,
        "evidence_record": "EVIDENCE_PUBLIC_GAP_BASELINE",
    }


def _artifact_index(root: Path) -> tuple[dict[str, dict[str, str]], dict[Path, str]]:
    paths = (SOURCE_NOTE, PORTFOLIO_REGISTER, CLAIM_PROVENANCE, QUERY_CODE)
    digests = {path: _sha256(root / path) for path in paths}
    return (
        {
            path.stem.replace(".", "_"): {
                "path": path.as_posix(),
                "sha256": digest,
            }
            for path, digest in digests.items()
        },
        digests,
    )


def process_closure_public_baseline_bundle(
    root: Path = ROOT,
    contract: ProcessClosureContract | None = None,
) -> dict[str, object]:
    """Build a complete graph shape whose failed gates expose public-data gaps."""
    if contract is None:
        contract = load_process_closure_contract()
    validate_process_closure_contract(contract)
    portfolio_records = _load_portfolio_records(root)
    artifact_files, digests = _artifact_index(root)

    source_id = "SOURCE_EARTH_PUBLIC_SUPPLY_CHAIN_2026"
    fleet_id = "FLEET_PUBLICLY_UNCLOSED_TRANSPORT_2026"
    source_node_id = "NODE_SOURCE_EARTH_PUBLIC_SUPPLY_CHAIN"
    transport_node_id = "NODE_TRANSPORT_PUBLICLY_UNCLOSED"
    waste_node_id = "NODE_WASTE_PUBLICLY_UNCLOSED"

    source_records = [
        {
            "source_id": source_id,
            "named_body_or_defensible_source_class": (
                "Earth industrial supply chain represented by USGS terrestrial "
                "production/reserve statistics; not an autonomous off-world source"
            ),
            "mineral_form": "multiple terrestrial ores, concentrates, and traded products",
            "composition_distribution": _unknown(
                "USGS commodity records are not one assayed campaign source lot"
            ),
            "grade_distribution": _unknown(
                "commodity summaries do not supply one process-resolved grade distribution"
            ),
            "accessible_and_recoverable_reserve": _unknown(
                "terrestrial reserves do not establish lunar or asteroid recoverability"
            ),
            "spatial_variability": _unknown("no selected off-world site has been assayed"),
            "uncertainty_and_detection_limit": _unknown(
                "not harmonized across all required materials"
            ),
            "depletion_and_failed_source_rule": (
                "external imports remain explicit; loss of the Earth supply boundary "
                "breaks every dependent route"
            ),
        }
    ]
    fleet_records = [
        {
            "fleet_id": fleet_id,
            "delta_v_and_transfer_windows": _unknown(
                "no reproducible source-to-factory off-world fleet is evidenced"
            ),
            "transit_and_turnaround_time": _unknown("architecture and source are unresolved"),
            "vehicle_payload_and_dry_mass": _unknown(
                "no verified fleet is bound to this process graph"
            ),
            "propellant_and_consumables": _unknown(
                "no closed propellant and consumables route is demonstrated"
            ),
            "excavation_and_processing_rate": _unknown(
                "NASA oxygen experiments do not establish fleet production rate"
            ),
            "fleet_manufacture_and_replacement_bom": _unknown(
                "vehicles and parent tools remain external"
            ),
            "reliability_and_failed_missions": _unknown("no applicable operating campaign exists"),
            "reserve_and_inventory_accounting": _unknown(
                "no assayed off-world reserve is connected to a reproducing fleet"
            ),
        }
    ]

    nodes: list[dict[str, object]] = [
        {
            "node_id": source_node_id,
            "node_type": "source_lot",
            "source_record_id": source_id,
            "body_or_site": "Earth public industrial-supply boundary",
            "mineral_form": "heterogeneous terrestrial supply",
            "grade_distribution": _unknown("not a single assayed lot"),
            "accessibility": "available only through an external mature economy",
            "recoverable_reserve": _unknown("not transferable to an off-world source claim"),
            "uncertainty": _unknown("commodity-specific and not graph-harmonized"),
            "depletion_state": "external dependency",
        },
        {
            "node_id": transport_node_id,
            "node_type": "transport_leg",
            "fleet_record_id": fleet_id,
            "origin": "external Earth supply boundary",
            "destination": "candidate industrial system",
            "delta_v": _unknown("destination/source architecture unresolved"),
            "transfer_window": _unknown("destination/source architecture unresolved"),
            "transit_time": _unknown("destination/source architecture unresolved"),
            "payload": _unknown("no verified manifest"),
            "propellant": _unknown("no closed route"),
            "cycle_time": _unknown("no operating campaign"),
            "loss_rate": _unknown("no operating campaign"),
        },
        {
            "node_id": waste_node_id,
            "node_type": "waste_or_recycle_stream",
            "species_and_grade": "all unresolved process losses",
            "quantity": _unknown("species mass balance is incomplete"),
            "recoverable_fraction": _unknown("no full-chain recycling campaign"),
            "treatment_route": _unknown("not demonstrated"),
            "disposal_route": _unknown("not demonstrated"),
        },
    ]

    grade_nodes: dict[str, str] = {}
    for grade_id, grade in contract["required_material_grades"].items():
        node_id = f"NODE_MATERIAL_{grade_id.upper()}"
        grade_nodes[grade_id] = node_id
        nodes.append(
            {
                "node_id": node_id,
                "node_type": "material_or_species",
                "chemical_identity": "multiple required species; unresolved by public evidence",
                "material_grade": grade["acceptance"],
                "grade_id": grade_id,
                "assay": _unknown(f"no graph-wide {grade_id} assay dataset"),
                "contamination_limits": _unknown(f"no complete named specification for {grade_id}"),
                "physical_form": _unknown(f"route-specific {grade_id} form not demonstrated"),
            }
        )

    process_nodes: dict[str, str] = {}
    for stage in contract["required_process_stages"]:
        node_id = f"NODE_PROCESS_{stage.upper()}"
        process_nodes[stage] = node_id
        nodes.append(
            {
                "node_id": node_id,
                "node_type": "process_unit",
                "equipment_family": stage,
                "operating_envelope": _unknown("no integrated campaign envelope"),
                "batch_or_continuous": _unknown("route not selected and demonstrated"),
                "throughput": _unknown("no measured full-chain throughput"),
                "energy": _unknown("no metered full-chain energy dataset"),
                "consumables": _unknown("external and undisclosed consumables remain"),
                "tool_life": _unknown("no measured parent-tool campaign"),
            }
        )

    part_nodes: dict[str, str] = {}
    for requirement_id, requirement in contract["critical_part_families"].items():
        node_id = f"NODE_PART_{requirement_id.upper()}"
        part_nodes[requirement_id] = node_id
        nodes.append(
            {
                "node_id": node_id,
                "node_type": "part_family",
                "requirement_id": requirement_id,
                "specification": requirement["acceptance"],
                "acceptable_substitutes": ["explicit external import"],
                "service_life": _unknown("no applicable closed-system fleet history"),
                "failure_modes": ["supply loss", "qualification failure", "parent-tool loss"],
                "inspection": _unknown("no independently witnessed acceptance campaign"),
            }
        )

    equipment_nodes: dict[str, str] = {}
    for record in portfolio_records:
        sector = cast(str, record["sector"])
        node_id = f"NODE_EQUIPMENT_SECTOR_{sector.upper()}"
        equipment_nodes[sector] = node_id
        nodes.append(
            {
                "node_id": node_id,
                "node_type": "production_equipment",
                "bom": {
                    "upstream_suppliers": record.get("upstreamSuppliers"),
                    "closure_gap": record.get("residualClosureGap"),
                },
                "parent_tool": record.get("requiredParentTools")
                or "not disclosed in portfolio register",
                "calibration_artifacts": _unknown(
                    f"no reproducible calibration chain for {sector}"
                ),
                "software_and_controls": record.get("initiative")
                or "not disclosed in portfolio register",
                "maintenance_inputs": _unknown(f"no closed maintenance history for {sector}"),
            }
        )

    edges: list[dict[str, object]] = []

    def add_edge(input_node: str, output_node: str, stage: str, boundary: str) -> None:
        edges.append(
            _edge(
                edge_id=f"EDGE_PUBLIC_{len(edges) + 1:03d}",
                input_node=input_node,
                output_node=output_node,
                process_stage=stage,
                boundary=boundary,
            )
        )

    current = source_node_id
    for stage in contract["required_process_stages"]:
        target = process_nodes[stage]
        add_edge(current, target, stage, "full-chain measurements are unavailable")
        current = target

    add_edge(
        source_node_id,
        transport_node_id,
        "excavation_and_size_reduction",
        "transport fleet is not reproduced by the source portfolio",
    )
    for grade_id, node_id in grade_nodes.items():
        add_edge(
            current,
            node_id,
            "purification_and_contamination_control",
            f"{grade_id} progression remains uncalibrated",
        )
    for requirement_id, node_id in part_nodes.items():
        add_edge(
            grade_nodes["bulk"],
            node_id,
            "component_fabrication_and_packaging",
            f"{requirement_id} remains imported or unsupported",
        )
    for sector, node_id in equipment_nodes.items():
        add_edge(
            grade_nodes["structural_alloy"],
            node_id,
            "assembly_calibration_and_acceptance",
            f"{sector} parent-tool ancestry is not closed",
        )
    add_edge(
        current,
        waste_node_id,
        "maintenance_repair_and_recycling",
        "waste and recovery flows are not species-balanced",
    )

    evidence_record = {
        "record_id": "EVIDENCE_PUBLIC_GAP_BASELINE",
        "source_or_experiment": (
            "NASA lunar ISRU and replicating-systems reports; NIST semiconductor "
            "metrology projects; USGS MCS 2026; public portfolio register"
        ),
        "organization_or_authors": "NASA; NIST; U.S. Geological Survey; rsi-model",
        "title_or_protocol": "Process-closure public-evidence baseline",
        "date": "2026-07-29",
        "exact_locator": SOURCE_NOTE.as_posix(),
        "persistent_identifier_or_archive_hash": digests[SOURCE_NOTE],
        "extracted_value_and_units": (
            "15-20% demonstrated lunar-simulant oxygen yield; all other graph-wide "
            "coefficients remain undisclosed or unmeasured"
        ),
        "denominator_and_boundary": (
            "selected public terrestrial and lunar-process evidence; not an integrated "
            "source-to-reproduction campaign"
        ),
        "transformation": (
            "Map evidenced capability and every explicit gap to typed graph nodes; "
            "do not impute missing numerical fields"
        ),
        "uncertainty_and_detection_limit": (
            "source-specific values retained; no graph-wide uncertainty fit exists"
        ),
        "source_class": "mixed_primary_source_negative_evidence_audit",
        "independent_review_status": (
            "not independently audited; every closure gate remains failed"
        ),
    }
    query_digest = digests[QUERY_CODE]
    witness_digest = digests[SOURCE_NOTE]
    gate_results = {
        gate_id: {
            "status": "fail",
            "evidence_query_sha256": query_digest,
            "evaluator_id": "rsi-model-process-public-baseline-v1",
            "witness_hash": witness_digest,
        }
        for gate_id in contract["acceptance_gates"]
    }
    return {
        "template_status": "completed_negative_public_evidence_baseline",
        "contract_id": contract["contract_id"],
        "graph_version": "public-evidence-gap-graph-v1",
        "archive_sha256": witness_digest,
        "artifact_files": artifact_files,
        "source_records": source_records,
        "fleet_records": fleet_records,
        "nodes": nodes,
        "edges": edges,
        "evidence_records": [evidence_record],
        "gate_results": gate_results,
    }


def write_process_closure_public_baseline(
    *,
    root: Path = ROOT,
    bundle_path: Path | None = None,
    evaluation_path: Path | None = None,
) -> tuple[Path, Path]:
    bundle_path = bundle_path or (
        root / "outputs/integrated/evidence/process_closure_public_baseline.json"
    )
    evaluation_path = evaluation_path or (
        root / "outputs/integrated/evidence/process_closure_public_baseline_evaluation.json"
    )
    bundle = process_closure_public_baseline_bundle(root)
    evaluation = evaluate_process_closure_bundle(bundle, archive_root=root)
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    evaluation_path.parent.mkdir(parents=True, exist_ok=True)
    evaluation_path.write_text(
        json.dumps(evaluation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return bundle_path, evaluation_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rsi-write-process-baseline")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--evaluation", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    try:
        bundle_path, evaluation_path = write_process_closure_public_baseline(
            root=root,
            bundle_path=args.bundle,
            evaluation_path=args.evaluation,
        )
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    print(bundle_path)
    print(evaluation_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
