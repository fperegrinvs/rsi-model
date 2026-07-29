"""Generate a fail-closed economic calibration against available public evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import cast

from rsimodel.economic_calibration import (
    economic_calibration_bundle_template,
    evaluate_economic_calibration_bundle,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE_NOTE = Path("docs/sources/economic-calibration-public-evidence-2026-07-29.md")
STARMIND_NOTE = Path("docs/sources/starmind-ai1-2026-07-27.md")
ECONOMIC_NOTE = Path("docs/sources/spacexai-economic-thesis-2026-07-29.md")
SCENARIO_REGISTER = Path("params/orbital_ai_scenario_registry.json")
QUERY_CODE = Path("src/rsimodel/economic_calibration_baseline.py")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _artifact_index(root: Path) -> tuple[dict[str, dict[str, str]], dict[Path, str]]:
    paths = (SOURCE_NOTE, STARMIND_NOTE, ECONOMIC_NOTE, SCENARIO_REGISTER, QUERY_CODE)
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


def _fill_missing(value: object, key: str = "") -> object:
    if isinstance(value, Mapping):
        raw = cast(Mapping[object, object], value)
        return {
            str(child_key): _fill_missing(child, str(child_key)) for child_key, child in raw.items()
        }
    if isinstance(value, (list, tuple)):
        sequence = cast(Sequence[object], value)
        return [_fill_missing(child, key) for child in sequence]
    if value is not None:
        return value
    if key in {"amount", "failed_and_censored_count"}:
        return 0.0
    return "not_disclosed_within_public_evidence_boundary"


def economic_calibration_public_baseline_bundle(
    root: Path = ROOT,
) -> dict[str, object]:
    """Return a complete negative bundle with no empirical promotions."""
    template = economic_calibration_bundle_template()
    filled = _fill_missing(template)
    if not isinstance(filled, dict):
        raise TypeError("economic template did not produce an object")
    bundle = cast(dict[str, object], filled)
    artifact_files, digests = _artifact_index(root)
    note_digest = digests[SOURCE_NOTE]
    query_digest = digests[QUERY_CODE]
    bundle.update(
        {
            "template_status": "completed_negative_public_evidence_calibration",
            "archive_sha256": note_digest,
            "artifact_files": artifact_files,
        }
    )

    packages = cast(dict[str, object], bundle["evidence_packages"])
    package_findings = {
        "E01_workload_benchmark": {
            "benchmark_id": "PUBLIC_GAP_EQUAL_WORKLOAD_2026",
            "model_and_version": "not matched across Earth and space",
            "measured_energy_kwh": "not disclosed for a matched accepted workload",
            "useful_completed_work": "not disclosed",
        },
        "E02_space_asset_reliability": {
            "asset_and_configuration": (
                "NASA historical spacecraft populations; no architecture-matched orbital AI fleet"
            ),
            "component_and_system_failures": (
                "historical public failures exist but are not configuration-matched"
            ),
            "right_censoring": "NASA studies retain active spacecraft; AI fleet absent",
        },
        "E03_link_and_ground_network": {
            "orbit_and_constellation_geometry": (
                "FCC SAT-LOA-20260108-00016 proposes 500-2000 km orbital data centers"
            ),
            "spectrum_and_regulatory_case": "FCC DA 26-113 accepted for filing",
            "delivered_throughput": "no operating orbital-AI service disclosed",
        },
        "E04_thermal_mass_power": {
            "configuration_and_bom": "Starmind AI1 vehicle-level public specification",
            "measured_it_and_total_power": (
                "120 kW average compute and 150 kW solar nameplate; not an operating measurement"
            ),
            "radiator_area_and_mass": "110 m2 area disclosed; radiator mass not disclosed",
        },
        "E05_earth_resource_buildout": {
            "site_and_grid_region": "United States aggregate; not a matched project site",
            "power_contract_and_grid_charges": (
                "2025 average 13.41 cents/kWh commercial and 8.62 cents/kWh industrial"
            ),
            "achieved_pue_and_availability": "not matched to the orbital workload case",
        },
        "E06_cash_flows_and_financing": {
            "event_id": "PUBLIC_GAP_LEDGER_2026",
            "project_and_architecture": "no complete matched project ledger disclosed",
            "cash_flow_category": "all required event classes represented as missingness rows",
            "committed_and_paid_amount": "not disclosed by project architecture period",
        },
    }
    for package_id, raw_package in packages.items():
        package = cast(dict[str, object], raw_package)
        package["normalized_records_sha256"] = note_digest
        records = cast(list[object], package["records"])
        record = cast(dict[str, object], records[0])
        record.update(package_findings[package_id])
        record["record_status"] = "partial_public_evidence_no_promotion"
        record["source_note_sha256"] = note_digest

    fits = cast(dict[str, object], bundle["correlation_fits"])
    for raw_fit in fits.values():
        fit = cast(dict[str, object], raw_fit)
        fit.update(
            {
                "model": "no joint fit; public evidence is structurally incomplete",
                "calibration_period": "public records through 2025",
                "validation_period": "2026 holdout",
                "diagnostics": {
                    "result": "insufficient architecture-matched observations",
                    "promotion_allowed": False,
                },
                "holdout_status": "fail",
                "fit_query_sha256": query_digest,
            }
        )

    cash_events = cast(list[object], bundle["cash_flow_events"])
    for raw_event in cash_events:
        event = cast(dict[str, object], raw_event)
        event.update(
            {
                "amount": 0.0,
                "architecture_case": "public_evidence_gap",
                "event_time": "2026-07-29",
                "nominal_currency": "USD",
                "price_base_date": "2026-07-29",
                "project_id": "PUBLIC_GAP_NO_AUDITED_LEDGER",
                "quantity_and_units": "missing-data sentinel; not an observed zero",
                "source_document_hash": note_digest,
                "record_status": "evidence_missing",
            }
        )

    decisions = cast(dict[str, object], bundle["promotion_decisions"])
    for raw_decision in decisions.values():
        decision = cast(dict[str, object], raw_decision)
        decision.update(
            {
                "decision": "retain_assumption",
                "estimate": "not promoted",
                "units": "not applicable",
                "uncertainty": "unbounded by a passing architecture-matched holdout",
                "failed_and_censored_count": 1.0,
                "holdout_result": "fail",
                "calibration_query_sha256": query_digest,
                "independent_review_status": "rejected",
            }
        )
    return bundle


def write_economic_calibration_public_baseline(
    *,
    root: Path = ROOT,
    bundle_path: Path | None = None,
    evaluation_path: Path | None = None,
) -> tuple[Path, Path]:
    bundle_path = bundle_path or (
        root / "outputs/integrated/evidence/economic_calibration_public_baseline.json"
    )
    evaluation_path = evaluation_path or (
        root / "outputs/integrated/evidence/economic_calibration_public_baseline_evaluation.json"
    )
    bundle = economic_calibration_public_baseline_bundle(root)
    evaluation = evaluate_economic_calibration_bundle(bundle, archive_root=root)
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
    parser = argparse.ArgumentParser(prog="rsi-write-economic-baseline")
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--bundle", type=Path)
    parser.add_argument("--evaluation", type=Path)
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    try:
        bundle_path, evaluation_path = write_economic_calibration_public_baseline(
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
