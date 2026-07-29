"""Validated register for observed precursors to verified AI-R&D loops."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Final, TypedDict, cast

ROOT: Final = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE: Final = ROOT / "params" / "observed_precursor_telemetry.json"
DEFAULT_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "observed_precursor_telemetry.csv"
)


class PrecursorRecord(TypedDict):
    systemId: str
    sourceRef: str
    sourceClass: str
    sourceVersion: str
    immutableLocator: str
    objectModified: str
    searchTopology: str
    evaluationSignal: str
    attempts: str
    retainedChanges: str
    elapsedComputeOrTime: str
    evaluatorIndependence: str
    transferEvaluation: str
    humanInterventions: str
    failureModes: str
    observedResult: str
    doesNotDemonstrate: str


FIELDS: Final[tuple[str, ...]] = (
    "systemId",
    "sourceRef",
    "sourceClass",
    "sourceVersion",
    "immutableLocator",
    "objectModified",
    "searchTopology",
    "evaluationSignal",
    "attempts",
    "retainedChanges",
    "elapsedComputeOrTime",
    "evaluatorIndependence",
    "transferEvaluation",
    "humanInterventions",
    "failureModes",
    "observedResult",
    "doesNotDemonstrate",
)


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(dict[str, object], value)


def load_precursor_telemetry(path: Path = DEFAULT_SOURCE) -> tuple[str, list[PrecursorRecord]]:
    """Load and validate the versioned telemetry register."""
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    root = _object(raw, "telemetry root")
    if root.get("schemaVersion") != 1:
        raise ValueError("telemetry schemaVersion must be 1")
    as_of = root.get("asOf")
    if not isinstance(as_of, str) or not as_of:
        raise ValueError("telemetry asOf must be a non-empty string")
    records_value = root.get("records")
    if not isinstance(records_value, list) or not records_value:
        raise ValueError("telemetry records must be a non-empty array")

    records: list[PrecursorRecord] = []
    seen: set[str] = set()
    for index, value in enumerate(cast(list[object], records_value)):
        item = _object(value, f"records[{index}]")
        unknown = sorted(set(item) - set(FIELDS))
        missing = sorted(set(FIELDS) - set(item))
        if unknown or missing:
            raise ValueError(
                f"records[{index}] field mismatch; missing={missing}, unknown={unknown}"
            )
        if not all(isinstance(item[field], str) for field in FIELDS):
            raise ValueError(f"records[{index}] fields must all be strings")
        record = cast(PrecursorRecord, item)
        if record["systemId"] in seen:
            raise ValueError(f"duplicate telemetry systemId: {record['systemId']}")
        seen.add(record["systemId"])
        if not record["sourceRef"].startswith("S"):
            raise ValueError(f"{record['systemId']}: sourceRef must be a manuscript source ID")
        if not record["immutableLocator"].startswith("https://"):
            raise ValueError(f"{record['systemId']}: immutableLocator must be HTTPS")
        records.append(record)
    return as_of, records


def write_precursor_telemetry_csv(
    output: Path = DEFAULT_OUTPUT,
    source: Path = DEFAULT_SOURCE,
) -> Path:
    """Write the public CSV from the validated source register."""
    as_of, records = load_precursor_telemetry(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    headers = ("as_of", *FIELDS)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(headers)
        for record in records:
            writer.writerow(
                (
                    as_of,
                    record["systemId"],
                    record["sourceRef"],
                    record["sourceClass"],
                    record["sourceVersion"],
                    record["immutableLocator"],
                    record["objectModified"],
                    record["searchTopology"],
                    record["evaluationSignal"],
                    record["attempts"],
                    record["retainedChanges"],
                    record["elapsedComputeOrTime"],
                    record["evaluatorIndependence"],
                    record["transferEvaluation"],
                    record["humanInterventions"],
                    record["failureModes"],
                    record["observedResult"],
                    record["doesNotDemonstrate"],
                )
            )
    return output
