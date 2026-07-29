"""Run the publication notation audit under the normal test suite."""

from pathlib import Path

from rsimodel.notation_gate import main

ROOT = Path(__file__).resolve().parents[1]


def test_notation_audit_passes() -> None:
    assert main(["--project-root", str(ROOT)]) == 0
