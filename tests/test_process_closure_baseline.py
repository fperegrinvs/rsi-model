"""The public-evidence graph must fail honestly and reproducibly."""

import json
from collections.abc import Mapping
from pathlib import Path

from rsimodel.process_closure import (
    evaluate_process_closure_bundle,
    load_process_closure_contract,
)
from rsimodel.process_closure_baseline import (
    process_closure_public_baseline_bundle,
    write_process_closure_public_baseline,
)

ROOT = Path(__file__).resolve().parents[1]


def test_public_baseline_is_complete_shape_but_all_gates_fail() -> None:
    contract = load_process_closure_contract()
    bundle = process_closure_public_baseline_bundle()
    assert bundle == process_closure_public_baseline_bundle()

    result = evaluate_process_closure_bundle(bundle, archive_root=ROOT)
    assert result["overall_status"] == "failed"
    gate_status = result["gate_status"]
    assert isinstance(gate_status, Mapping)
    assert set(gate_status) == set(contract["acceptance_gates"])
    assert set(gate_status.values()) == {"fail"}
    node_count = result["node_count"]
    edge_count = result["edge_count"]
    assert isinstance(node_count, int)
    assert isinstance(edge_count, int)
    assert node_count >= (
        len(contract["required_material_grades"])
        + len(contract["required_process_stages"])
        + len(contract["critical_part_families"])
    )
    assert edge_count >= len(contract["required_process_stages"])


def test_public_baseline_preserves_every_unknown_instead_of_imputing() -> None:
    bundle = process_closure_public_baseline_bundle()
    serialized = json.dumps(bundle)
    assert "not_disclosed_or_not_measured" in serialized
    assert "completed_negative_public_evidence_baseline" in serialized
    assert '"status": "pass"' not in serialized


def test_public_baseline_writer_matches_generator(tmp_path: Path) -> None:
    bundle_path = tmp_path / "bundle.json"
    evaluation_path = tmp_path / "evaluation.json"
    assert write_process_closure_public_baseline(
        bundle_path=bundle_path,
        evaluation_path=evaluation_path,
    ) == (bundle_path, evaluation_path)
    assert json.loads(bundle_path.read_text(encoding="utf-8")) == (
        process_closure_public_baseline_bundle()
    )
    assert json.loads(evaluation_path.read_text(encoding="utf-8"))["overall_status"] == "failed"
