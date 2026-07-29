#!/usr/bin/env python3
"""Audit the manuscript's equation inventory and consolidated notation table."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import cast

# These relations intentionally introduce no new model symbol. Their symbols
# are already registered at the first substantive equation named in the reason.
NO_NEW_SYMBOL_EQUATIONS = {
    "eq:appendix-material-balance": "duplicates eq:material-balance",
    "eq:digital-capability-rate": "reuses the digital-loop state and gain symbols",
    "eq:hardware-net-growth": "reuses the conceptual hardware-growth account",
    "eq:space-cost-substitution": "is a numerical substitution into eq:space-lifecycle-cost",
}

EQUATION_RE = re.compile(
    r"::: \{#(?P<id>eq:[A-Za-z0-9_.:-]+) \.equation[^}]*\}\n"
    r"\$\$\n(?P<body>.*?)\n\$\$\n:::",
    flags=re.DOTALL,
)
REFERENCE_RE = re.compile(r"@(?P<id>eq:[A-Za-z0-9_.:-]+)")
RELATION_TYPES = {
    "definition",
    "accounting identity",
    "constraint",
    "conceptual relation",
    "calibrated relation",
    "numerical substitution",
    "implemented model equation",
}


def report_failures(messages: Sequence[str]) -> int:
    for message in messages:
        print(f"FAIL {message}", file=sys.stderr)
    return 1


def manuscript_text(fragments: Path) -> str:
    return "".join(path.read_text(encoding="utf-8") for path in sorted(fragments.glob("*.md")))


def notation_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    for line in text.splitlines():
        if (
            line
            == "| symbol | meaning | units or admissible domain | first equation | model layer |"
        ):
            in_table = True
            continue
        if not in_table:
            continue
        if line.startswith("|---"):
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def read_json_object(file: Path, root: Path, failures: list[str]) -> dict[str, object]:
    try:
        loaded: object = json.loads(file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        failures.append(f"{file.relative_to(root)} cannot be read: {error}")
        return {}
    if not isinstance(loaded, dict):
        failures.append(f"{file.relative_to(root)} must contain a JSON object")
        return {}
    value = cast(dict[str, object], loaded)
    if value.get("schemaVersion") != 1:
        failures.append(f"{file.relative_to(root)} schemaVersion must be 1")
    return value


def validate_explanatory_prose(
    equations: Sequence[re.Match[str]],
    manuscript: str,
    failures: list[str],
) -> None:
    """Require nearby prose after every displayed equation."""
    for index, match in enumerate(equations):
        end = equations[index + 1].start() if index + 1 < len(equations) else len(manuscript)
        following = manuscript[match.end() : end]
        following = re.split(r"\n#{1,6} ", following, maxsplit=1)[0]
        prose = re.sub(r"[`$*_{}\[\]():,.;—–-]", " ", following)
        words = re.findall(r"[A-Za-z][A-Za-z0-9]*", prose)
        if len(words) < 8:
            failures.append(f"{match.group('id')} lacks nearby explanatory prose")


def main(argv: Sequence[str] | None = None) -> int:
    """Audit equation and notation metadata under an explicit project root."""
    parser = argparse.ArgumentParser(prog="rsi-check-notation")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    root = args.project_root.resolve()
    fragments = root / "docs" / "manuscript"
    register = fragments / "53-notation-register.md"
    notation_registry = root / "params" / "notation_registry.json"
    explanation_registry = root / "params" / "equation_explanations.json"
    required_inputs = (register, notation_registry, explanation_registry)
    if not fragments.is_dir() or any(not path.is_file() for path in required_inputs):
        print(f"not an rsi-model manuscript tree: {root}", file=sys.stderr)
        return 2

    text = manuscript_text(fragments)
    equations = list(EQUATION_RE.finditer(text))
    equation_ids = [match.group("id") for match in equations]
    failures: list[str] = []
    duplicates = sorted(
        {equation_id for equation_id in equation_ids if equation_ids.count(equation_id) > 1}
    )
    if duplicates:
        failures.append(f"duplicate equation IDs: {', '.join(duplicates)}")
    causal_code = re.findall(r"(?m)^\s{4,}\S[^\n]*(?:→|->)[^\n]*$", text)
    if causal_code:
        failures.append(
            "modeled causal arrows must be numbered equations or prose references: "
            + " | ".join(line.strip() for line in causal_code)
        )

    register_text = register.read_text(encoding="utf-8")
    rows = notation_rows(register_text)
    if not rows:
        failures.append("notation table is missing or empty")
    bad_width = [index + 1 for index, row in enumerate(rows) if len(row) != 5]
    if bad_width:
        failures.append(f"notation rows do not have five columns: {bad_width}")

    symbols: dict[str, tuple[str, str, str]] = {}
    registered_first_equations: set[str] = set()
    equation_set = set(equation_ids)
    for index, row in enumerate(rows, start=1):
        if len(row) != 5:
            continue
        symbol, meaning, units, first_equation, layer = row
        if not all((symbol, meaning, units, first_equation, layer)):
            failures.append(f"notation row {index} has an empty field")
        definition = (meaning, units, layer)
        if symbol in symbols and symbols[symbol] != definition:
            failures.append(f"notation symbol {symbol} has incompatible duplicate definitions")
        symbols[symbol] = definition
        refs = REFERENCE_RE.findall(first_equation)
        if len(refs) != 1:
            failures.append(f"notation row {index} must name exactly one first equation")
            continue
        equation_id = refs[0]
        registered_first_equations.add(equation_id)
        if equation_id not in equation_set:
            failures.append(f"notation row {index} references missing equation {equation_id}")

    notation_document = read_json_object(notation_registry, root, failures)
    notation_terms = notation_document.get("terms", [])
    if not isinstance(notation_terms, list):
        failures.append("params/notation_registry.json terms must be an array")
        notation_terms = []
    typed_notation_terms = cast(list[object], notation_terms)
    if len(typed_notation_terms) != len(rows):
        failures.append(
            "structured notation registry and Markdown table have different row counts: "
            f"{len(typed_notation_terms)} versus {len(rows)}"
        )
    term_keys: set[str] = set()
    term_first_equations: dict[str, str] = {}
    for index, (row, raw_value) in enumerate(
        zip(rows, typed_notation_terms, strict=False), start=1
    ):
        if len(row) != 5 or not isinstance(raw_value, dict):
            failures.append(f"structured notation term {index} is malformed")
            continue
        value = cast(dict[str, object], raw_value)
        key = value.get("key")
        if not isinstance(key, str) or not key:
            failures.append(f"structured notation term {index} has no stable key")
            continue
        if key in term_keys:
            failures.append(f"duplicate structured notation term key: {key}")
        term_keys.add(key)
        refs = REFERENCE_RE.findall(row[3])
        expected_first = refs[0] if len(refs) == 1 else ""
        expected = {
            "symbol": row[0],
            "meaning": row[1],
            "unitsOrDomain": row[2],
            "firstEquation": expected_first,
            "modelLayer": row[4],
        }
        for field, expected_value in expected.items():
            if value.get(field) != expected_value:
                failures.append(
                    f"structured notation term {key} field {field} differs from Markdown"
                )
        term_first_equations[key] = expected_first

    explanation_document = read_json_object(explanation_registry, root, failures)
    explanations = explanation_document.get("equations", [])
    if not isinstance(explanations, list):
        failures.append("params/equation_explanations.json equations must be an array")
        explanations = []
    typed_explanations = cast(list[object], explanations)
    explanation_ids: list[str] = []
    explanation_terms: dict[str, set[str]] = {}
    required_string_fields = (
        "id",
        "title",
        "interpretation",
        "relationType",
        "modelLayer",
        "implementationStatus",
    )
    required_array_fields = ("termKeys", "indices", "operators", "assumptions")
    for index, raw_value in enumerate(typed_explanations, start=1):
        if not isinstance(raw_value, dict):
            failures.append(f"equation explanation {index} is not an object")
            continue
        value = cast(dict[str, object], raw_value)
        failures.extend(
            f"equation explanation {index} has invalid {field}"
            for field in required_string_fields
            if not (isinstance(field_value := value.get(field), str) and field_value.strip())
        )
        for field in required_array_fields:
            entries = value.get(field)
            raw_entries = cast(list[object], entries) if isinstance(entries, list) else []
            if not isinstance(entries, list) or not all(
                isinstance(entry, str) and entry.strip() for entry in raw_entries
            ):
                failures.append(f"equation explanation {index} has invalid {field}")
        equation_id = value.get("id")
        if not isinstance(equation_id, str):
            continue
        explanation_ids.append(equation_id)
        declared_terms = value.get("termKeys")
        if not isinstance(declared_terms, list):
            continue
        typed_declared_terms = cast(list[object], declared_terms)
        if not typed_declared_terms:
            failures.append(f"{equation_id} declares no canonical terms")
        string_terms = [term for term in typed_declared_terms if isinstance(term, str)]
        if len(typed_declared_terms) != len(set(string_terms)):
            failures.append(f"{equation_id} repeats canonical term keys")
        unknown_terms = sorted(
            str(term)
            for term in typed_declared_terms
            if not isinstance(term, str) or term not in term_keys
        )
        if unknown_terms:
            failures.append(f"{equation_id} has unknown term keys: {unknown_terms}")
        explanation_terms[equation_id] = set(string_terms)
        if value.get("relationType") not in RELATION_TYPES:
            failures.append(f"{equation_id} has unknown relation type")

    duplicate_explanations = sorted(
        {equation_id for equation_id in explanation_ids if explanation_ids.count(equation_id) > 1}
    )
    if duplicate_explanations:
        failures.append(f"duplicate equation explanations: {', '.join(duplicate_explanations)}")
    missing_explanations = equation_set - set(explanation_ids)
    stale_explanations = set(explanation_ids) - equation_set
    if missing_explanations:
        failures.append(
            f"equations missing explanations: {', '.join(sorted(missing_explanations))}"
        )
    if stale_explanations:
        failures.append(f"stale equation explanations: {', '.join(sorted(stale_explanations))}")
    if explanation_ids != equation_ids:
        failures.append("equation explanation order differs from manuscript order")
    for key, first_equation in term_first_equations.items():
        if key not in explanation_terms.get(first_equation, set()):
            failures.append(f"{first_equation} omits first-use canonical term {key}")

    stale_exceptions = set(NO_NEW_SYMBOL_EQUATIONS) - equation_set
    if stale_exceptions:
        failures.append("stale no-new-symbol exceptions: " + ", ".join(sorted(stale_exceptions)))
    uncovered = equation_set - registered_first_equations - set(NO_NEW_SYMBOL_EQUATIONS)
    if uncovered:
        failures.append(
            "equations introduce no registered first-use symbol: " + ", ".join(sorted(uncovered))
        )

    validate_explanatory_prose(equations, text, failures)

    if failures:
        return report_failures(failures)
    print(
        f"PASS notation audit: {len(equations)} equations, "
        f"{len(rows)} canonical term groups, {len(typed_explanations)} explanations, "
        f"{len(NO_NEW_SYMBOL_EQUATIONS)} explicit no-new-symbol cases"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
