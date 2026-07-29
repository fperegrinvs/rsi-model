"""Contracts for the ordered, generated manuscript source boundary."""

import re
from pathlib import Path

from rsimodel.lco import lco_earth, lco_space

ROOT = Path(__file__).resolve().parents[1]
FRAGMENT_DIR = ROOT / "docs" / "manuscript"
MONOLITH = ROOT / "docs" / "Recursive_Industrial_Intelligence_r4.0.md"
EXPECTED = [
    "00-front-matter.md",
    "10-part-i-foundations.md",
    "11-part-i-depreciation-closure.md",
    "12-part-i-model-results.md",
    "20-part-ii-comparative-economics.md",
    "30-part-iii-strategy-governance.md",
    "40-part-iv-conclusion-limitations.md",
    "50-appendices-a-b.md",
    "51-appendix-c-reproducibility.md",
    "52-appendix-d-model-specification.md",
    "53-notation-register.md",
    "60-glossary.md",
    "70-sources.md",
]


def _fragments() -> list[Path]:
    return [FRAGMENT_DIR / name for name in EXPECTED]


def test_fragment_set_is_exact_and_ordered() -> None:
    assert sorted(path.name for path in FRAGMENT_DIR.glob("*.md")) == EXPECTED
    assert all(path.is_file() for path in _fragments())


def test_monolithic_markdown_is_generated_without_content_drift() -> None:
    assembled = "\n".join(path.read_text(encoding="utf-8") for path in _fragments())
    assert assembled == MONOLITH.read_text(encoding="utf-8")


def test_fragment_boundaries_follow_top_level_document_sections() -> None:
    expected_starts = [
        "# Recursive Industrial Intelligence",
        "# Part I — Technical Feasibility",
        "## I.4 Depreciation: the harsh term",
        "## I.7 The multisector model",
        "# Part II — Comparative Economics",
        "# Part III — Strategy Interpretation and Governance",
        "# Part IV — Conclusion, and Speculative Terminal Scenarios",
        "# Appendix A: Parameter Anchors",
        "# Appendix C: Reproducibility",
        "# Appendix D: Complete model specification",
        "## D.3 Consolidated notation",
        "# Glossary",
        "# Sources",
    ]
    actual = [path.read_text(encoding="utf-8").splitlines()[0] for path in _fragments()]
    assert all(
        line.startswith(f"{heading} {{#")
        for line, heading in zip(actual, expected_starts, strict=True)
    )


def test_reader_facing_opening_precedes_release_housekeeping() -> None:
    front = (FRAGMENT_DIR / "00-front-matter.md").read_text(encoding="utf-8")
    abstract = front.index("## Abstract {#abstract}")
    executive = front.index("## Executive Summary {#executive-summary}")
    scope = front.index("## Scope, Claims, and Evidence {#scope-claims-and-evidence}")
    how_to = front.index("## How to read this document {#how-to-read-this-document}")

    assert abstract < executive < scope < how_to
    opening = front[:abstract]
    for operational_residue in (
        "> **Status.**",
        "release candidate",
        "dirty worktree",
        "Linux CI",
        "TODO",
        "regeneration command",
    ):
        assert operational_residue not in opening
    assert '<span id="scope-and-status"></span>' in front


def test_source_definitions_are_unique_and_contiguous() -> None:
    text = MONOLITH.read_text(encoding="utf-8")
    source_ids = [
        int(match)
        for match in re.findall(
            r"^\[\*\*\[S(\d+)\]\*\*\]\{#source-s\d+ "
            r"\.source-entry-label\}",
            text,
            flags=re.MULTILINE,
        )
    ]
    assert source_ids
    assert len(source_ids) == len(set(source_ids))
    assert source_ids == list(range(1, max(source_ids) + 1))


def test_chip_efficiency_narrative_is_generated_result_consistent() -> None:
    earth = lco_earth("base").lco
    ratio_3000 = lco_space("leo_inference", launch_per_kg_leo=3000.0).lco / earth
    ratio_efficiency = (
        lco_space(
            "leo_inference",
            launch_per_kg_leo=3000.0,
            chip_efficiency_advantage=2.0,
        ).lco
        / earth
    )
    ratio_half_launch = lco_space("leo_inference", launch_per_kg_leo=1500.0).lco / earth
    benefit_fraction = (ratio_3000 - ratio_efficiency) / (ratio_3000 - ratio_half_launch)
    fragment = (FRAGMENT_DIR / "20-part-ii-comparative-economics.md").read_text(encoding="utf-8")
    expected = (
        f"about {benefit_fraction:.0%} of the benefit of halving launch price "
        f"(ratio {ratio_efficiency:.1f} vs\n{ratio_half_launch:.1f} at "
        f"$3,000/kg, both from {ratio_3000:.1f})"
    )
    assert expected in fragment
    assert "~39%" not in fragment
