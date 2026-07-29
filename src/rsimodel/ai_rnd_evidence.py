"""Validated cross-lab evidence registry for AI-enabled R&D."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Final, NotRequired, TypedDict, cast

ROOT: Final = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE: Final = ROOT / "params" / "ai_rnd_evidence_registry.json"
DEFAULT_BENCHMARK_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "ai_rnd_benchmark_registry.csv"
)
DEFAULT_CROSSWALK_OUTPUT: Final = (
    ROOT / "outputs" / "integrated" / "tables" / "ai_rnd_evidence_crosswalk.csv"
)


class RefreshSource(TypedDict):
    sourceId: str
    url: str
    expectedMarkers: NotRequired[list[str]]
    expectedSha256: NotRequired[str]


class EvidenceRecord(TypedDict):
    evidenceId: str
    organization: str
    sourceRef: str
    sourceVersion: str
    sourceDate: str
    sourceUrl: str
    evidenceClass: str
    recordType: str
    construct: str
    unitOfEvaluation: str
    model: str
    harness: str
    computeToolAccess: str
    scaffolding: str
    humanRole: str
    baseline: str
    thresholdOrComparator: str
    scoringRule: str
    publishedStatus: str
    evaluatorIndependence: str
    limitations: str
    stages: list[str]
    analyticGates: list[str]
    doesNotEstablish: str
    coefficientUse: str
    crossLabComparison: str


class EvidenceRegistry(TypedDict):
    schemaVersion: int
    asOf: str
    stages: list[str]
    analyticGates: list[str]
    refreshSources: list[RefreshSource]
    entries: list[EvidenceRecord]


RECORD_FIELDS: Final[tuple[str, ...]] = (
    "evidenceId",
    "organization",
    "sourceRef",
    "sourceVersion",
    "sourceDate",
    "sourceUrl",
    "evidenceClass",
    "recordType",
    "construct",
    "unitOfEvaluation",
    "model",
    "harness",
    "computeToolAccess",
    "scaffolding",
    "humanRole",
    "baseline",
    "thresholdOrComparator",
    "scoringRule",
    "publishedStatus",
    "evaluatorIndependence",
    "limitations",
    "stages",
    "analyticGates",
    "doesNotEstablish",
    "coefficientUse",
    "crossLabComparison",
)
STRING_FIELDS: Final = tuple(
    field for field in RECORD_FIELDS if field not in {"stages", "analyticGates"}
)
REQUIRED_STAGES: Final = {
    "task_selection_research_taste",
    "hypothesis_generation",
    "implementation",
    "experiment_execution",
    "debugging",
    "compute_kernel_optimization",
    "training_post_training",
    "evaluation",
    "safety_verification",
    "deployment",
    "measured_successor_model_gain",
}
REQUIRED_GATES: Final = {
    "assistant_equivalent_capability",
    "realized_rnd_acceleration",
    "broad_rnd_automation",
    "verified_recursive_closure",
}
UNQUALIFIED_COMPONENT_PHRASES: Final = (
    "latest model",
    "rsi benchmark",
    "fully autonomous",
    "recursive self-improvement",
)


def _mapping(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a non-empty string array")
    strings = cast(list[str], value)
    if len(strings) != len(set(strings)):
        raise ValueError(f"{label} must not contain duplicates")
    return strings


def load_ai_rnd_evidence(path: Path = DEFAULT_SOURCE) -> EvidenceRegistry:
    """Load and validate the versioned AI-R&D evidence registry."""
    root = _mapping(json.loads(path.read_text(encoding="utf-8")), "registry")
    expected_root = {
        "schemaVersion",
        "asOf",
        "stages",
        "analyticGates",
        "refreshSources",
        "entries",
    }
    if set(root) != expected_root:
        raise ValueError(
            f"registry field mismatch; missing={sorted(expected_root - set(root))}, "
            f"unknown={sorted(set(root) - expected_root)}"
        )
    if root["schemaVersion"] != 1:
        raise ValueError("registry schemaVersion must be 1")
    as_of = root["asOf"]
    if not isinstance(as_of, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of):
        raise ValueError("registry asOf must use YYYY-MM-DD")
    stages = _string_list(root["stages"], "registry.stages")
    gates = _string_list(root["analyticGates"], "registry.analyticGates")
    if set(stages) != REQUIRED_STAGES:
        raise ValueError("registry.stages must define the complete canonical loop")
    if set(gates) != REQUIRED_GATES:
        raise ValueError("registry.analyticGates must define the four distinct gates")

    raw_refresh = root["refreshSources"]
    if not isinstance(raw_refresh, list) or not raw_refresh:
        raise ValueError("registry.refreshSources must be a non-empty array")
    refresh_sources: list[RefreshSource] = []
    seen_refresh: set[str] = set()
    for index, raw in enumerate(cast(list[object], raw_refresh)):
        item = _mapping(raw, f"refreshSources[{index}]")
        required_refresh = {"sourceId", "url"}
        optional_refresh = {"expectedMarkers", "expectedSha256"}
        if not required_refresh <= set(item) or set(item) - required_refresh - optional_refresh:
            raise ValueError(f"refreshSources[{index}] has an invalid field set")
        source_id = item["sourceId"]
        url = item["url"]
        if not isinstance(source_id, str) or not source_id:
            raise ValueError(f"refreshSources[{index}].sourceId must be non-empty")
        if source_id in seen_refresh:
            raise ValueError(f"duplicate refresh sourceId: {source_id}")
        seen_refresh.add(source_id)
        if not isinstance(url, str) or not url.startswith("https://"):
            raise ValueError(f"{source_id}: refresh URL must use HTTPS")
        refresh_source: RefreshSource = {"sourceId": source_id, "url": url}
        if "expectedMarkers" in item:
            refresh_source["expectedMarkers"] = _string_list(
                item["expectedMarkers"],
                f"refreshSources[{index}].expectedMarkers",
            )
        if "expectedSha256" in item:
            expected_hash = item["expectedSha256"]
            if not isinstance(expected_hash, str) or not re.fullmatch(
                r"[0-9a-f]{64}",
                expected_hash,
            ):
                raise ValueError(f"{source_id}: expectedSha256 must be lowercase SHA-256")
            refresh_source["expectedSha256"] = expected_hash
        if not ({"expectedMarkers", "expectedSha256"} & set(refresh_source)):
            raise ValueError(f"{source_id}: at least one refresh expectation is required")
        refresh_sources.append(refresh_source)

    raw_entries = root["entries"]
    if not isinstance(raw_entries, list) or not raw_entries:
        raise ValueError("registry.entries must be a non-empty array")
    entries: list[EvidenceRecord] = []
    seen_entries: set[str] = set()
    observed_stages: set[str] = set()
    observed_gates: set[str] = set()
    for index, raw in enumerate(cast(list[object], raw_entries)):
        item = _mapping(raw, f"entries[{index}]")
        missing = sorted(set(RECORD_FIELDS) - set(item))
        unknown = sorted(set(item) - set(RECORD_FIELDS))
        if missing or unknown:
            raise ValueError(
                f"entries[{index}] field mismatch; missing={missing}, unknown={unknown}"
            )
        for field in STRING_FIELDS:
            value = item[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"entries[{index}] string fields must all be non-empty")
        record = cast(EvidenceRecord, item)
        evidence_id = record["evidenceId"]
        if evidence_id in seen_entries:
            raise ValueError(f"duplicate evidenceId: {evidence_id}")
        seen_entries.add(evidence_id)
        if not all(re.fullmatch(r"S\d+", ref) for ref in record["sourceRef"].split(";")):
            raise ValueError(f"{evidence_id}: sourceRef must contain manuscript source IDs")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["sourceDate"]):
            raise ValueError(f"{evidence_id}: sourceDate must use YYYY-MM-DD")
        if not record["sourceUrl"].startswith("https://"):
            raise ValueError(f"{evidence_id}: sourceUrl must use HTTPS")
        record_stages = _string_list(record["stages"], f"{evidence_id}.stages")
        record_gates = _string_list(record["analyticGates"], f"{evidence_id}.analyticGates")
        if not set(record_stages) <= set(stages):
            raise ValueError(f"{evidence_id}: unknown loop stage")
        if not set(record_gates) <= set(gates):
            raise ValueError(f"{evidence_id}: unknown analytic gate")
        if record["coefficientUse"] != "none_observational_only":
            raise ValueError(f"{evidence_id}: evidence must not set simulation coefficients")
        if record["crossLabComparison"] != "not_permitted":
            raise ValueError(f"{evidence_id}: cross-lab score comparison is not commensurable")
        if record["recordType"] == "component_measurement":
            measured_text = " ".join(
                (record["construct"], record["publishedStatus"], record["doesNotEstablish"])
            ).lower()
            for phrase in UNQUALIFIED_COMPONENT_PHRASES:
                if phrase in measured_text:
                    raise ValueError(
                        f"{evidence_id}: component measurement uses unqualified phrase {phrase!r}"
                    )
        observed_stages.update(record_stages)
        observed_gates.update(record_gates)
        entries.append(record)
    if observed_stages != set(stages):
        missing_stages = sorted(set(stages) - observed_stages)
        raise ValueError(f"registry leaves loop stages unmapped: {missing_stages}")
    if observed_gates != set(gates):
        missing_gates = sorted(set(gates) - observed_gates)
        raise ValueError(f"registry leaves analytic gates unmapped: {missing_gates}")

    return {
        "schemaVersion": 1,
        "asOf": as_of,
        "stages": stages,
        "analyticGates": gates,
        "refreshSources": refresh_sources,
        "entries": entries,
    }


def write_ai_rnd_evidence_csvs(
    benchmark_output: Path = DEFAULT_BENCHMARK_OUTPUT,
    crosswalk_output: Path = DEFAULT_CROSSWALK_OUTPUT,
    source: Path = DEFAULT_SOURCE,
) -> tuple[Path, Path]:
    """Write the evidence registry and normalized stage/gate crosswalk."""
    registry = load_ai_rnd_evidence(source)
    benchmark_output.parent.mkdir(parents=True, exist_ok=True)
    benchmark_headers = (
        "as_of",
        *(field for field in RECORD_FIELDS if field not in {"stages", "analyticGates"}),
        "stages",
        "analyticGates",
    )
    with benchmark_output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=benchmark_headers, lineterminator="\n")
        writer.writeheader()
        for record in registry["entries"]:
            row = {
                key: value
                for key, value in record.items()
                if key not in {"stages", "analyticGates"}
            }
            row["as_of"] = registry["asOf"]
            row["stages"] = ";".join(record["stages"])
            row["analyticGates"] = ";".join(record["analyticGates"])
            writer.writerow(row)

    crosswalk_output.parent.mkdir(parents=True, exist_ok=True)
    crosswalk_headers = (
        "as_of",
        "evidenceId",
        "organization",
        "sourceRef",
        "evidenceClass",
        "mappingType",
        "mappedConstruct",
        "relationship",
        "coefficientUse",
        "doesNotEstablish",
    )
    with crosswalk_output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(crosswalk_headers)
        for record in registry["entries"]:
            for stage in record["stages"]:
                writer.writerow(
                    (
                        registry["asOf"],
                        record["evidenceId"],
                        record["organization"],
                        record["sourceRef"],
                        record["evidenceClass"],
                        "loop_stage",
                        stage,
                        "directly_informs",
                        record["coefficientUse"],
                        record["doesNotEstablish"],
                    )
                )
            for gate in record["analyticGates"]:
                relationship = (
                    "defines_threshold"
                    if record["recordType"] == "framework_threshold"
                    else "informs_but_does_not_prove"
                )
                writer.writerow(
                    (
                        registry["asOf"],
                        record["evidenceId"],
                        record["organization"],
                        record["sourceRef"],
                        record["evidenceClass"],
                        "analytic_gate",
                        gate,
                        relationship,
                        record["coefficientUse"],
                        record["doesNotEstablish"],
                    )
                )
    return benchmark_output, crosswalk_output


def check_source_refresh(path: Path = DEFAULT_SOURCE, timeout: float = 30.0) -> list[str]:
    """Fetch version-sensitive pages and report changed identifying markers."""
    registry = load_ai_rnd_evidence(path)
    failures: list[str] = []
    curl = shutil.which("curl")
    if curl is None:
        return ["curl is required for source-refresh checks"]
    for source in registry["refreshSources"]:
        result = subprocess.run(  # noqa: S603 - fixed command; URL is one validated argument
            [
                curl,
                "--fail",
                "--location",
                "--max-time",
                str(max(1, round(timeout))),
                "--silent",
                "--show-error",
                "--user-agent",
                "rsi-model-source-refresh/1.0",
                source["url"],
            ],
            capture_output=True,
            check=False,
        )
        if result.returncode:
            failures.append(
                f"{source['sourceId']}: fetch failed with curl {result.returncode}: "
                f"{result.stderr.decode('utf-8', errors='replace').strip()}"
            )
            continue
        if "expectedSha256" in source:
            actual_hash = hashlib.sha256(result.stdout).hexdigest()
            if actual_hash != source["expectedSha256"]:
                failures.append(
                    f"{source['sourceId']}: source bytes changed: "
                    f"expected {source['expectedSha256']}, found {actual_hash}"
                )
        if "expectedMarkers" in source:
            body = result.stdout.decode("utf-8", errors="replace")
            normalized = re.sub(r"\s+", " ", body).casefold()
            missing = [
                marker
                for marker in source["expectedMarkers"]
                if re.sub(r"\s+", " ", marker).casefold() not in normalized
            ]
            if missing:
                failures.append(
                    f"{source['sourceId']}: expected version marker(s) absent: {missing}"
                )
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    """Validate the registry or check its version-sensitive upstream pages."""
    parser = argparse.ArgumentParser(prog="python -m rsimodel.ai_rnd_evidence")
    parser.add_argument("--registry", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--source-refresh", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.source_refresh and args.write:
        parser.error("--source-refresh and --write are mutually exclusive")
    try:
        registry = load_ai_rnd_evidence(args.registry)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    if args.source_refresh:
        failures = check_source_refresh(args.registry)
        if failures:
            print("AI-R&D source refresh failed:\n- " + "\n- ".join(failures), file=sys.stderr)
            return 1
        print(f"AI-R&D source refresh: {len(registry['refreshSources'])} sources unchanged")
    elif args.write:
        benchmark, crosswalk = write_ai_rnd_evidence_csvs(source=args.registry)
        print(benchmark)
        print(crosswalk)
    else:
        print(
            f"AI-R&D evidence: {len(registry['entries'])} records, "
            f"{len(registry['stages'])} stages, {len(registry['analyticGates'])} gates"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
