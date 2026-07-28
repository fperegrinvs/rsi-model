"""Validation and public gap register for process-feasible closure."""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any

import yaml

from rsimodel.evidence import (
    SHA256_PLACEHOLDER,
    artifact_files_template,
    binary_results_template,
    require_fields,
    require_list,
    require_mapping,
    require_sha256,
    required_field_template,
    validate_binary_results,
    verify_artifact_files,
)

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "params" / "process_closure_requirements.yaml"
INTEGRATED_PATH = ROOT / "params" / "integrated_model.yaml"


def load_process_closure_contract(
    path: Path | None = None,
) -> dict[str, Any]:
    return yaml.safe_load((path or CONTRACT_PATH).read_text(encoding="utf-8"))


def validate_process_closure_contract(
    contract: dict[str, Any] | None = None,
) -> None:
    """Reject drift or a requirements file that implies unearned closure."""
    contract = contract or load_process_closure_contract()
    errors: list[str] = []

    if contract.get("status") != (
        "acceptance_contract_ready_process_graph_and_calibration_pending"
    ):
        errors.append("status must keep graph construction and calibration pending")
    if contract.get("source_class") != "ASSUMPTION":
        errors.append("contract must remain ASSUMPTION-class")

    integrated = yaml.safe_load(INTEGRATED_PATH.read_text(encoding="utf-8"))
    if contract.get("current_aggregate_categories") != integrated.get("elements"):
        errors.append("current aggregate categories drift from integrated_model.yaml")

    graph = contract.get("graph_schema", {})
    required_nodes = {
        "source_lot",
        "process_unit",
        "material_or_species",
        "part_family",
        "production_equipment",
        "transport_leg",
        "waste_or_recycle_stream",
    }
    if set(graph.get("node_types", {})) != required_nodes:
        errors.append("graph node types are incomplete or unexpected")
    for node_id, node in graph.get("node_types", {}).items():
        if not node.get("required_fields"):
            errors.append(f"{node_id}: required_fields is empty")
    if len(graph.get("edge_required_fields", [])) < 9:
        errors.append("graph edge evidence contract is incomplete")

    required_grades = {
        "bulk",
        "structural_alloy",
        "electronic_grade",
        "semiconductor_grade",
        "ultra_pure_process_input",
    }
    if not required_grades <= set(contract.get("required_material_grades", {})):
        errors.append("minimum material-grade ladder is incomplete")

    required_parts = {
        "process_gases",
        "process_chemicals",
        "masks_and_reticles",
        "resists_and_photochemicals",
        "filters_and_membranes",
        "optics_and_laser_sources",
        "coatings_and_surface_treatments",
        "seals_and_flexible_elements",
        "lubricants_and_working_fluids",
        "bearings_and_precision_motion",
        "calibration_artifacts",
        "metrology_and_test",
        "controls_and_power_electronics",
        "parent_tools",
    }
    if set(contract.get("critical_part_families", {})) != required_parts:
        errors.append("critical part-family register is incomplete")

    gates = contract.get("acceptance_gates", {})
    if set(gates) != {
        "C01_species_mass_balance",
        "C02_energy_and_capacity",
        "C03_grade_progression",
        "C04_part_and_parent_tool_ancestry",
        "C05_source_transport_fleet",
        "C06_failure_and_substitution",
        "C07_empirical_calibration",
        "C08_minimum_external_vector",
    }:
        errors.append("acceptance gates must be the complete C01-C08 set")
    for gate_id, gate in gates.items():
        if not gate.get("test") or not gate.get("evidence"):
            errors.append(f"{gate_id}: incomplete test/evidence")
        unknown = set(gate.get("evidence", [])) - required_nodes
        if unknown:
            errors.append(f"{gate_id}: unknown evidence nodes {sorted(unknown)}")

    source_fleet = contract.get("source_and_fleet_requirements", {})
    if len(source_fleet.get("source_fields", [])) < 8:
        errors.append("source-state requirements are incomplete")
    if len(source_fleet.get("fleet_fields", [])) < 8:
        errors.append("fleet requirements are incomplete")
    if len(contract.get("evidence_record_required_fields", [])) < 12:
        errors.append("evidence-record provenance is incomplete")
    if not contract.get("promotion_rule"):
        errors.append("promotion rule is missing")

    if errors:
        raise ValueError(
            "invalid process-closure contract:\n- " + "\n- ".join(errors)
        )


def render_process_closure_gap_csv(
    contract: dict[str, Any] | None = None,
) -> str:
    """Render all requirements without implying the missing graph exists."""
    contract = contract or load_process_closure_contract()
    validate_process_closure_contract(contract)
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow([
        "record_type",
        "id",
        "requirement",
        "required_evidence_or_fields",
        "readiness",
    ])
    for node_id, node in contract["graph_schema"]["node_types"].items():
        writer.writerow([
            "graph_node_type",
            node_id,
            "versioned node with complete typed fields",
            "; ".join(node["required_fields"]),
            "evidence_pending",
        ])
    for grade_id, grade in contract["required_material_grades"].items():
        writer.writerow([
            "material_grade",
            grade_id,
            grade["acceptance"],
            "assay; specification; uncertainty; upstream and downstream edges",
            "evidence_pending",
        ])
    for family_id, family in contract["critical_part_families"].items():
        writer.writerow([
            "critical_part_family",
            family_id,
            family["acceptance"],
            "BOM; process route; parent tools; calibration; life; substitutes",
            "evidence_pending",
        ])
    for register_id, fields in (
        (
            "source_register",
            contract["source_and_fleet_requirements"]["source_fields"],
        ),
        (
            "fleet_register",
            contract["source_and_fleet_requirements"]["fleet_fields"],
        ),
    ):
        writer.writerow([
            register_id,
            register_id,
            "at least one complete, versioned record linked from the graph",
            "; ".join(fields),
            "evidence_pending",
        ])
    for gate_id, gate in contract["acceptance_gates"].items():
        writer.writerow([
            "acceptance_gate",
            gate_id,
            gate["test"],
            "; ".join(gate["evidence"]),
            "evidence_pending",
        ])
    return stream.getvalue()


def write_process_closure_gap_csv(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_process_closure_gap_csv(), encoding="utf-8")
    return path


def process_closure_bundle_template(
    contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a complete-shape template that is invalid until evidence exists."""
    contract = contract or load_process_closure_contract()
    validate_process_closure_contract(contract)
    source_id = "SOURCE_REPLACE_001"
    fleet_id = "FLEET_REPLACE_001"
    evidence_id = "EVIDENCE_REPLACE_001"

    source_records = [
        required_field_template(
            contract["source_and_fleet_requirements"]["source_fields"],
            {"source_id": source_id},
        )
    ]
    fleet_records = [
        required_field_template(
            contract["source_and_fleet_requirements"]["fleet_fields"],
            {"fleet_id": fleet_id},
        )
    ]

    nodes: list[dict[str, Any]] = []
    for node_type, cfg in contract["graph_schema"]["node_types"].items():
        if node_type in {"material_or_species", "part_family"}:
            continue
        overrides: dict[str, Any] = {
            "node_id": f"NODE_{node_type.upper()}_REPLACE_001",
            "node_type": node_type,
        }
        if node_type == "source_lot":
            overrides["source_record_id"] = source_id
        if node_type == "transport_leg":
            overrides["fleet_record_id"] = fleet_id
        nodes.append(
            required_field_template(cfg["required_fields"], overrides)
        )
    for grade_id in contract["required_material_grades"]:
        nodes.append(
            required_field_template(
                contract["graph_schema"]["node_types"][
                    "material_or_species"
                ]["required_fields"],
                {
                    "node_id": f"NODE_MATERIAL_{grade_id.upper()}",
                    "node_type": "material_or_species",
                    "grade_id": grade_id,
                    "material_grade": grade_id,
                },
            )
        )
    for requirement_id in contract["critical_part_families"]:
        nodes.append(
            required_field_template(
                contract["graph_schema"]["node_types"][
                    "part_family"
                ]["required_fields"],
                {
                    "node_id": f"NODE_PART_{requirement_id.upper()}",
                    "node_type": "part_family",
                    "requirement_id": requirement_id,
                },
            )
        )

    node_ids = {node["node_type"]: node["node_id"] for node in nodes}
    edges = []
    for index, stage in enumerate(contract["required_process_stages"], 1):
        edges.append(
            required_field_template(
                contract["graph_schema"]["edge_required_fields"],
                {
                    "edge_id": f"EDGE_REPLACE_{index:03d}",
                    "input_node": node_ids["source_lot"],
                    "output_node": node_ids["process_unit"],
                    "process_stage": stage,
                    "evidence_record": evidence_id,
                },
            )
        )
    evidence_record = required_field_template(
        contract["evidence_record_required_fields"],
        {"record_id": evidence_id},
    )
    return {
        "template_status": "incomplete_do_not_submit",
        "contract_id": contract["contract_id"],
        "graph_version": None,
        "archive_sha256": SHA256_PLACEHOLDER,
        "artifact_files": artifact_files_template(),
        "source_records": source_records,
        "fleet_records": fleet_records,
        "nodes": nodes,
        "edges": edges,
        "evidence_records": [evidence_record],
        "gate_results": binary_results_template(
            contract["acceptance_gates"]
        ),
    }


def evaluate_process_closure_bundle(
    bundle: dict[str, Any] | None,
    contract: dict[str, Any] | None = None,
    *,
    archive_root: Path | None = None,
) -> dict[str, Any]:
    """Validate a versioned process graph and its binary closure evidence."""
    contract = contract or load_process_closure_contract()
    validate_process_closure_contract(contract)
    if not bundle:
        return {
            "overall_status": "graph_and_evidence_pending",
            "gate_status": {
                gate: "evidence_pending"
                for gate in contract["acceptance_gates"]
            },
        }

    errors: list[str] = []
    if bundle.get("contract_id") != contract["contract_id"]:
        errors.append("contract_id does not match the r4.0 contract")
    require_fields(
        bundle,
        {
            "graph_version",
            "source_records",
            "fleet_records",
            "nodes",
            "edges",
            "evidence_records",
            "gate_results",
        },
        "bundle",
        errors,
    )
    require_sha256(bundle, "archive_sha256", "bundle", errors)
    verify_artifact_files(bundle, archive_root, errors)

    source_fields = contract["source_and_fleet_requirements"]["source_fields"]
    source_records = require_list(
        bundle.get("source_records"), "source_records", errors
    )
    if not source_records:
        errors.append("source_records: no source records supplied")
    source_ids: set[str] = set()
    for index, raw_source in enumerate(source_records):
        label = f"source_records[{index}]"
        source = require_mapping(raw_source, label, errors)
        require_fields(source, source_fields, label, errors)
        source_id = source.get("source_id")
        if source_id in source_ids:
            errors.append(f"{label}: duplicate source_id {source_id}")
        source_ids.add(source_id)

    fleet_fields = contract["source_and_fleet_requirements"]["fleet_fields"]
    fleet_records = require_list(
        bundle.get("fleet_records"), "fleet_records", errors
    )
    if not fleet_records:
        errors.append("fleet_records: no fleet records supplied")
    fleet_ids: set[str] = set()
    for index, raw_fleet in enumerate(fleet_records):
        label = f"fleet_records[{index}]"
        fleet = require_mapping(raw_fleet, label, errors)
        require_fields(fleet, fleet_fields, label, errors)
        fleet_id = fleet.get("fleet_id")
        if fleet_id in fleet_ids:
            errors.append(f"{label}: duplicate fleet_id {fleet_id}")
        fleet_ids.add(fleet_id)

    node_schema = contract["graph_schema"]["node_types"]
    nodes = require_list(bundle.get("nodes"), "nodes", errors)
    node_ids: set[str] = set()
    node_types: dict[str, str] = {}
    observed_grades: set[str] = set()
    observed_parts: set[str] = set()
    for index, raw_node in enumerate(nodes):
        label = f"nodes[{index}]"
        node = require_mapping(raw_node, label, errors)
        require_fields(node, {"node_id", "node_type"}, label, errors)
        node_id, node_type = node.get("node_id"), node.get("node_type")
        if node_id in node_ids:
            errors.append(f"{label}: duplicate node_id {node_id}")
        node_ids.add(node_id)
        if isinstance(node_id, str) and isinstance(node_type, str):
            node_types[node_id] = node_type
        if node_type not in node_schema:
            errors.append(f"{label}: unknown node_type {node_type}")
            continue
        require_fields(
            node,
            node_schema[node_type]["required_fields"],
            label,
            errors,
        )
        if node_type == "material_or_species":
            observed_grades.add(node.get("grade_id"))
        if node_type == "part_family":
            observed_parts.add(node.get("requirement_id"))
        if (
            node_type == "source_lot"
            and node.get("source_record_id") not in source_ids
        ):
            errors.append(f"{label}: unknown source_record_id")
        if (
            node_type == "transport_leg"
            and node.get("fleet_record_id") not in fleet_ids
        ):
            errors.append(f"{label}: unknown fleet_record_id")

    evidence_schema = contract["evidence_record_required_fields"]
    evidence_records = require_list(
        bundle.get("evidence_records"), "evidence_records", errors
    )
    evidence_ids: set[str] = set()
    for index, raw_evidence in enumerate(evidence_records):
        label = f"evidence_records[{index}]"
        evidence = require_mapping(raw_evidence, label, errors)
        require_fields(evidence, evidence_schema, label, errors)
        evidence_id = evidence.get("record_id")
        if evidence_id in evidence_ids:
            errors.append(f"{label}: duplicate record_id {evidence_id}")
        evidence_ids.add(evidence_id)

    edge_schema = contract["graph_schema"]["edge_required_fields"]
    observed_stages: set[str] = set()
    edges = require_list(bundle.get("edges"), "edges", errors)
    edge_ids: set[str] = set()
    adjacency: dict[str, set[str]] = {}
    structured_edge_fields = {
        "stoichiometry_or_bom",
        "quantity_and_units",
        "yield_distribution",
        "energy_distribution",
        "contamination_and_rework",
        "consumables_and_tool_wear",
        "capacity_and_cycle_time",
    }
    for index, raw_edge in enumerate(edges):
        label = f"edges[{index}]"
        edge = require_mapping(raw_edge, label, errors)
        require_fields(edge, {"edge_id", *edge_schema}, label, errors)
        edge_id = edge.get("edge_id")
        if edge_id in edge_ids:
            errors.append(f"{label}: duplicate edge_id {edge_id}")
        edge_ids.add(edge_id)
        if edge.get("input_node") not in node_ids:
            errors.append(f"{label}: unknown input_node")
        if edge.get("output_node") not in node_ids:
            errors.append(f"{label}: unknown output_node")
        if (
            edge.get("input_node") in node_ids
            and edge.get("output_node") in node_ids
        ):
            adjacency.setdefault(edge["input_node"], set()).add(
                edge["output_node"]
            )
        if edge.get("evidence_record") not in evidence_ids:
            errors.append(f"{label}: unknown evidence_record")
        for field in structured_edge_fields:
            if not isinstance(edge.get(field), (dict, list)):
                errors.append(
                    f"{label}: {field} must be a structured object or array"
                )
        observed_stages.add(edge.get("process_stage"))

    required_grades = set(contract["required_material_grades"])
    if not required_grades <= observed_grades:
        errors.append(
            f"nodes: missing material grades "
            f"{sorted(required_grades - observed_grades)}"
        )
    required_parts = set(contract["critical_part_families"])
    if not required_parts <= observed_parts:
        errors.append(
            f"nodes: missing critical part families "
            f"{sorted(required_parts - observed_parts)}"
        )
    required_stages = set(contract["required_process_stages"])
    if not required_stages <= observed_stages:
        errors.append(
            f"edges: missing process stages "
            f"{sorted(required_stages - observed_stages)}"
        )

    reachable = {
        node_id
        for node_id, node_type in node_types.items()
        if node_type == "source_lot"
    }
    frontier = list(reachable)
    while frontier:
        current = frontier.pop()
        for downstream in adjacency.get(current, set()):
            if downstream not in reachable:
                reachable.add(downstream)
                frontier.append(downstream)
    required_reachable = {
        node_id
        for node_id, node_type in node_types.items()
        if node_type in {
            "material_or_species",
            "part_family",
            "process_unit",
            "production_equipment",
            "transport_leg",
        }
    }
    unreachable = required_reachable - reachable
    if unreachable:
        errors.append(
            "graph: required nodes are not reachable from a source lot "
            f"{sorted(unreachable)}"
        )

    gate_results = require_mapping(
        bundle.get("gate_results"), "gate_results", errors
    )
    validate_binary_results(
        gate_results,
        set(contract["acceptance_gates"]),
        "gate_results",
        errors,
    )
    if errors:
        raise ValueError(
            "invalid process-closure evidence bundle:\n- "
            + "\n- ".join(errors)
        )
    statuses = {
        gate: record["status"] for gate, record in gate_results.items()
    }
    return {
        "overall_status": (
            "passed" if all(status == "pass" for status in statuses.values())
            else "failed"
        ),
        "gate_status": statuses,
        "node_count": len(nodes),
        "edge_count": len(bundle["edges"]),
        "evidence_record_count": len(evidence_records),
        "source_record_count": len(source_records),
        "fleet_record_count": len(fleet_records),
    }
