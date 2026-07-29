from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import cast

import pytest

from rsimodel.portfolio_coverage import (
    EVIDENCE_TIERS,
    SECTORS,
    PortfolioRecord,
    dependency_aware_closure,
    load_portfolio_coverage,
    write_portfolio_coverage_csvs,
)


def test_portfolio_register_preserves_sector_order_and_audited_vector() -> None:
    as_of, scope, protocol, records = load_portfolio_coverage()
    assert as_of == "2026-07-28"
    assert "Tesla remains a separate public company" in scope
    assert tuple(record["sector"] for record in records) == SECTORS
    assert [
        sum(record["evidenceTier"] == tier for record in records) for tier in EVIDENCE_TIERS
    ] == [
        12,
        0,
        5,
        0,
        1,
    ]
    assert sum(record["offWorldReproductivelyClosed"] for record in records) == 0
    assert "job advertisements" in protocol["excludedAsSufficientEvidence"]


def test_dependency_aware_result_rejects_flattering_seventeen_of_eighteen() -> None:
    _, _, _, records = load_portfolio_coverage()
    hypothetical = cast(list[PortfolioRecord], [dict(record) for record in records])
    for record in hypothetical:
        record["offWorldReproductivelyClosed"] = True
    hypothetical[-2]["offWorldReproductivelyClosed"] = False
    assert sum(1 for record in hypothetical if record["offWorldReproductivelyClosed"]) == 17
    assert hypothetical[-2]["sector"] == "process_equipment_metrology"
    assert not dependency_aware_closure(hypothetical)


def test_generated_views_share_one_source_and_expose_the_blocker(tmp_path: Path) -> None:
    row_output, summary_output, group_output = write_portfolio_coverage_csvs(
        tmp_path / "rows.csv",
        tmp_path / "summary.csv",
        tmp_path / "groups.csv",
    )
    rows = list(csv.DictReader(io.StringIO(row_output.read_text(encoding="utf-8"))))
    summary = next(csv.DictReader(io.StringIO(summary_output.read_text(encoding="utf-8"))))
    groups = list(csv.DictReader(io.StringIO(group_output.read_text(encoding="utf-8"))))

    assert len(rows) == 18
    assert summary["documented_operating"] == "12"
    assert summary["announced_or_under_development"] == "5"
    assert summary["no_evidence"] == "1"
    assert summary["off_world_reproductively_closed"] == "0"
    assert summary["dependency_aware_closure"] == "false"
    assert summary["decisive_public_evidence_blocker"] == "process_equipment_metrology"
    assert [row["sector_group"] for row in groups] == [
        "bulk_material",
        "industrial_equipment",
        "electronics",
        "operations_maintenance",
        "intelligence_compute",
    ]


def test_register_rejects_common_ownership_conflation(tmp_path: Path) -> None:
    source = Path("params/portfolio_sector_coverage.json")
    value = json.loads(source.read_text(encoding="utf-8"))
    value["scope"] = "One commonly owned Tesla, SpaceX, and xAI portfolio."
    invalid = tmp_path / "invalid.json"
    invalid.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError, match="separate-company boundary"):
        load_portfolio_coverage(invalid)
