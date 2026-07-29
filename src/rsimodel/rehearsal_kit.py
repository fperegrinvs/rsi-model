"""Generate a deterministic facility handoff kit for the Stage-0 rehearsal."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import cast

from rsimodel.rehearsal import RehearsalProtocol, load_rehearsal_protocol
from rsimodel.rehearsal_archive import NUMERIC_EVENT_FIELDS

ROOT = Path(__file__).resolve().parents[2]


def _write_json(path: Path, value: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rehearsal_event_json_schema(
    protocol: RehearsalProtocol | None = None,
) -> dict[str, object]:
    """Translate the protocol event contract into a portable JSON Schema."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    common = protocol["event_schema"]["common_required_fields"]
    event_types = protocol["event_schema"]["event_types"]
    properties: dict[str, object] = {
        "event_id": {"type": "string", "minLength": 1},
        "event_type": {"enum": sorted(event_types)},
        "timestamp_utc": {"type": "string", "format": "date-time"},
        "monotonic_time_s": {"type": "number", "minimum": 0},
        "cell_id": {"enum": ["cell_0", "cell_1", "site"]},
        "external_witness_hash": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    }
    all_fields = set(common)
    for event_type in event_types.values():
        all_fields.update(event_type["required_fields"])
    for field in sorted(all_fields):
        if field not in properties:
            properties[field] = (
                {"type": "number", "minimum": 0}
                if field in NUMERIC_EVENT_FIELDS
                else {"type": ["string", "number", "boolean", "array", "object"]}
            )

    branches: list[dict[str, object]] = []
    for event_type, config in event_types.items():
        branch: dict[str, object] = {
            "properties": {"event_type": {"const": event_type}},
            "required": sorted({"event_type", *common, *config["required_fields"]}),
        }
        if event_type == "build_state":
            states = sorted(config.get("allowed_states", ()))
            branch["properties"] = {
                "event_type": {"const": event_type},
                "new_state": {"enum": states},
                "prior_state": {"enum": states},
            }
        branches.append(branch)
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://fperegrinvs.github.io/rsi-model/schema/rehearsal-event-r4.0.json",
        "title": "Stage-0 terrestrial autonomous-closure event",
        "type": "object",
        "additionalProperties": True,
        "properties": properties,
        "required": ["event_id", "event_type"],
        "oneOf": branches,
    }


def _event_template(
    event_type: str,
    protocol: RehearsalProtocol,
) -> dict[str, object]:
    config = protocol["event_schema"]["event_types"][event_type]
    fields = {
        *protocol["event_schema"]["common_required_fields"],
        *config["required_fields"],
    }
    event = cast(dict[str, object], dict.fromkeys(sorted(fields)))
    event.update(
        {
            "event_id": f"REPLACE_{event_type.upper()}_ID",
            "event_type": event_type,
            "cell_id": "site" if event_type in {"governance_action", "utility_meter"} else "cell_0",
            "external_witness_hash": "REPLACE_WITH_64_CHARACTER_LOWERCASE_SHA256",
        }
    )
    if event_type == "build_state":
        event["prior_state"] = "delivered"
        event["new_state"] = "staged"
    return event


def _auditor_template(protocol: RehearsalProtocol) -> str:
    gates = "\n".join(
        f"- [ ] `{gate_id}` — {config['acceptance']}"
        for gate_id, config in protocol["acceptance_gates"].items()
    )
    return f"""# Independent Stage-0 auditor report

Protocol: `{protocol["protocol_id"]}`

Campaign ID: `REPLACE`

Raw archive SHA-256: `REPLACE`

Auditor identity/organization: `REPLACE`

Audit date: `REPLACE`

## Independence and custody

Describe appointment, conflicts, observer-controlled instruments, source-lot
custody, inventory reconciliation, energy metering, software/query hashes, and
access to failed/censored trials.

## Gate findings

{gates}

Every checked gate requires a cited immutable query result and discrepancy
disposition. Missing or selectively withheld evidence is a failure.

## Deviations, interventions, and unresolved discrepancies

`REPLACE`

## Attestation

`REPLACE WITH SIGNED EXTERNAL ATTESTATION; THIS TEMPLATE IS NOT AN AUDIT`
"""


def _second_cell_template(protocol: RehearsalProtocol) -> dict[str, object]:
    return {
        "protocol_id": protocol["protocol_id"],
        "campaign_id": None,
        "cell_id": protocol["experimental_units"]["reproduced_cell"]["identity"],
        "record_status": "template_not_evidence",
        "indispensable_subsystems": [
            {
                "subsystem_id": None,
                "sector": None,
                "bom_sha256": None,
                "material_custody_query_sha256": None,
                "construction_event_ids": [],
                "commissioning_event_ids": [],
                "yield_query_sha256": None,
                "service_connection_query_sha256": None,
                "viable_floor_query_sha256": None,
                "retained_operation_query_sha256": None,
                "auditor_disposition": None,
            }
        ],
        "independence_rule": protocol["experimental_units"]["reproduced_cell"]["independence_rule"],
    }


def write_rehearsal_execution_kit(
    output_directory: Path,
    protocol: RehearsalProtocol | None = None,
) -> Path:
    """Write every non-physical execution artifact and a content-addressed manifest."""
    if protocol is None:
        protocol = load_rehearsal_protocol()
    output_directory.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    files.append(
        _write_json(
            output_directory / "rehearsal-event.schema.json",
            rehearsal_event_json_schema(protocol),
        )
    )
    template_directory = output_directory / "event-templates"
    files.extend(
        _write_json(
            template_directory / f"{event_type}.json",
            _event_template(event_type, protocol),
        )
        for event_type in protocol["event_schema"]["event_types"]
    )
    files.append(
        _write_json(
            output_directory / "gate-query-plan.json",
            {
                gate_id: {
                    "acceptance": config["acceptance"],
                    "evidence": list(config["evidence"]),
                    "query_sha256": None,
                    "result": None,
                    "witness_hash": None,
                }
                for gate_id, config in protocol["acceptance_gates"].items()
            },
        )
    )
    files.append(
        _write_json(
            output_directory / "fault-campaign-plan.json",
            {
                case["id"]: {
                    "injection": case["injection"],
                    "expected_controls": list(case["expected_controls"]),
                    "execution_status": "pending_physical_campaign",
                }
                for case in protocol["fault_campaign"]
            },
        )
    )
    files.append(
        _write_json(
            output_directory / "parameter-replacement-plan.json",
            {
                f"P{index:02d}": {
                    "measurement": mapping["measurement"],
                    "events": list(mapping["events"]),
                    "model_paths": list(mapping["model_paths"]),
                    "decision": None,
                    "evidence_query_sha256": None,
                }
                for index, mapping in enumerate(protocol["parameter_replacement_map"], 1)
            },
        )
    )
    files.append(
        _write_json(
            output_directory / "second-cell-build-record.json",
            _second_cell_template(protocol),
        )
    )
    auditor_path = output_directory / "independent-auditor-report.md"
    auditor_path.write_text(_auditor_template(protocol), encoding="utf-8")
    files.append(auditor_path)

    manifest = {
        "protocol_id": protocol["protocol_id"],
        "kit_status": "facility_handoff_ready_physical_execution_pending",
        "warning": (
            "Templates and hashes are not measurements, witness evidence, a signed "
            "campaign, or an acceptance result."
        ),
        "files": {
            path.relative_to(output_directory).as_posix(): _sha256(path) for path in sorted(files)
        },
    }
    manifest_path = output_directory / "campaign-kit-manifest.json"
    _write_json(manifest_path, manifest)
    return manifest_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rsi-write-rehearsal-kit")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "outputs/integrated/evidence/rehearsal_execution_kit",
    )
    args = parser.parse_args(argv)
    try:
        manifest = write_rehearsal_execution_kit(args.output_dir.resolve())
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
