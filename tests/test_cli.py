"""The installed maintenance command must fail closed and explain repairs."""

from __future__ import annotations

import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path

import pytest

from rsimodel import (
    baseline_runner,
    cli,
    coverage_gate,
    deep_runner,
    evidence_cli,
    external_links,
    integrated_runner,
    manifest_cli,
    math_font_gate,
    notation_gate,
    package_gate,
    part2_runner,
    prose_gate,
    provenance_cli,
    publication_cli,
    release_cli,
    release_manifest,
)

ROOT = Path(__file__).resolve().parents[1]
type CommandMain = Callable[[Sequence[str] | None], int]


@pytest.mark.parametrize(
    "entrypoint",
    [
        coverage_gate.coverage_main,
        evidence_cli.main,
        external_links.main,
        manifest_cli.main,
        math_font_gate.main,
        notation_gate.main,
        prose_gate.main,
        provenance_cli.main,
        publication_cli.main,
        release_cli.main,
        release_manifest.main,
        baseline_runner.baseline_main,
        deep_runner.deep_main,
        part2_runner.part2_main,
    ],
)
def test_installed_command_help_is_available(entrypoint: CommandMain) -> None:
    with pytest.raises(SystemExit) as exc:
        entrypoint(["--help"])
    assert exc.value.code == 0


def test_installed_command_invalid_inputs_fail_closed(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert notation_gate.main(["--project-root", str(tmp_path)]) == 2
    assert prose_gate.main(["--project-root", str(tmp_path)]) == 2
    assert math_font_gate.main(["--project-root", str(tmp_path)]) == 1
    assert external_links.main(["--manuscript", str(tmp_path / "missing.md")]) == 2
    assert provenance_cli.main(["--project-root", str(tmp_path)]) == 2
    assert release_cli.main(["--project-root", str(tmp_path)]) == 2
    assert release_manifest.main(["--project-root", str(tmp_path)]) == 2
    assert manifest_cli.main(["--project-root", str(tmp_path)]) == 2
    assert "not" in capsys.readouterr().err


def test_installed_command_inexpensive_success_paths(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert prose_gate.main(["--project-root", str(ROOT)]) == 0
    assert notation_gate.main(["--project-root", str(ROOT)]) == 0
    assert math_font_gate.main(["--project-root", str(ROOT)]) == 0

    empty_manuscript = tmp_path / "empty.md"
    empty_manuscript.write_text("# Empty\n", encoding="utf-8")
    assert external_links.main(["--manuscript", str(empty_manuscript)]) == 0

    evidence_template = tmp_path / "evidence.json"
    assert evidence_cli.main(["process_closure", "--write-template", str(evidence_template)]) == 0
    assert evidence_template.is_file()

    publication_template = tmp_path / "publication.json"
    assert publication_cli.main(["--write-authorization-template", str(publication_template)]) == 0
    release_template = tmp_path / "release.json"
    assert (
        release_cli.main(
            [
                "--project-root",
                str(ROOT),
                "--write-authorization-template",
                str(release_template),
            ]
        )
        == 0
    )
    assert publication_template.is_file()
    assert release_template.is_file()
    assert "PASS" in capsys.readouterr().out


def test_publication_preflight_explains_missing_release_metadata(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    authorization = tmp_path / "release.json"
    authorization.write_text("{}\n", encoding="utf-8")
    for variable in ("RELEASE_DATE", "VERSION_DOI", "CANONICAL_URL"):
        monkeypatch.delenv(variable, raising=False)
    assert (
        release_cli.main(
            [
                "--project-root",
                str(ROOT),
                "--mode",
                "publication",
                "--authorization-record",
                str(authorization),
            ]
        )
        == 2
    )
    error = capsys.readouterr().err
    assert "invalid publication metadata" in error
    assert "requires RELEASE_DATE, VERSION_DOI, and CANONICAL_URL" in error


@pytest.mark.parametrize(
    "entrypoint",
    [
        baseline_runner.baseline_main,
        deep_runner.deep_main,
        part2_runner.part2_main,
    ],
)
def test_expensive_generator_config_smoke_is_isolated(
    entrypoint: CommandMain,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output = tmp_path / "generated"
    assert entrypoint(["--output-dir", str(output), "--check-config"]) == 0
    assert "PASS" in capsys.readouterr().out
    assert not output.exists()
    with pytest.raises(SystemExit) as exc:
        entrypoint(["--output-dir"])
    assert exc.value.code == 2


def test_dependency_cli_help_is_a_normal_argparse_exit() -> None:
    with pytest.raises(SystemExit) as exc:
        cli.check_dependencies_main(["--help"])
    assert exc.value.code == 0


def test_package_cli_help_and_invalid_project(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        package_gate.package_main(["--help"])
    assert exc.value.code == 0
    assert package_gate.package_main(["--project-root", str(tmp_path)]) == 2
    assert "not a locked Python project" in capsys.readouterr().err


def test_integrated_cli_help_invalid_input_and_config_only(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        integrated_runner.integrated_main(["--help"])
    assert exc.value.code == 0

    assert (
        integrated_runner.integrated_main(["--project-root", str(tmp_path), "--check-config"]) == 2
    )
    assert "parameter file is missing" in capsys.readouterr().err

    params = tmp_path / "params"
    params.mkdir()
    (params / "integrated_model.yaml").write_text("schema_version: 1\n", encoding="utf-8")
    output = tmp_path / "generated"
    assert (
        integrated_runner.integrated_main(
            [
                "--project-root",
                str(tmp_path),
                "--output-dir",
                str(output),
                "--ensemble-size",
                "1",
                "--check-config",
            ]
        )
        == 0
    )
    assert "ensemble=1" in capsys.readouterr().out
    assert not output.exists()


def test_project_metadata_loader_validates_shape(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not found"):
        cli._load_project(tmp_path)

    metadata = tmp_path / "pyproject.toml"
    metadata.write_text("[tool.example]\nvalue = 1\n", encoding="utf-8")
    with pytest.raises(ValueError, match=r"no \[project\] table"):
        cli._load_project(tmp_path)

    metadata.write_text("[project]\nname = 'rsi-model'\n", encoding="utf-8")
    assert cli._load_project(tmp_path)["name"] == "rsi-model"


def test_uv_resolution_and_version_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli.shutil, "which", lambda _name: None)
    with pytest.raises(ValueError, match="unavailable"):
        cli._uv_executable()

    monkeypatch.setattr(cli, "_uv_executable", lambda: "/opt/uv")
    monkeypatch.setattr(
        cli.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(
            args=["uv", "--version"],
            returncode=0,
            stdout="uv 0.9.18\n",
            stderr="",
        ),
    )
    assert cli._uv_version() == "0.9.18"

    monkeypatch.setattr(
        cli.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(
            args=["uv", "--version"],
            returncode=1,
            stdout="",
            stderr="failed",
        ),
    )
    with pytest.raises(ValueError, match="failed"):
        cli._uv_version()

    monkeypatch.setattr(
        cli.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(
            args=["uv", "--version"],
            returncode=0,
            stdout="unexpected\n",
            stderr="",
        ),
    )
    with pytest.raises(ValueError, match="unexpected uv version"):
        cli._uv_version()


def test_lock_check_reports_missing_and_stale(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(ValueError, match="checked lock not found"):
        cli._check_lock(tmp_path)

    (tmp_path / "uv.lock").write_text("version = 1\n", encoding="utf-8")
    monkeypatch.setattr(cli, "_uv_executable", lambda: "/opt/uv")
    monkeypatch.setattr(
        cli.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(
            args=["uv", "lock"],
            returncode=1,
            stdout="",
            stderr="lock mismatch",
        ),
    )
    with pytest.raises(ValueError, match="lock mismatch"):
        cli._check_lock(tmp_path)


def test_installed_distribution_check_reports_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def missing_import(_name: str) -> None:
        raise ModuleNotFoundError

    monkeypatch.setattr(cli, "import_module", missing_import)
    with pytest.raises(ValueError, match="missing locked dependencies"):
        cli._installed_versions()


def test_dependency_cli_success_and_aggregated_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        cli,
        "_load_project",
        lambda _root: {"name": "rsi-model", "requires-python": ">=3.13,<3.14"},
    )
    monkeypatch.setattr(cli, "_uv_version", lambda: cli.EXPECTED_UV)
    monkeypatch.setattr(cli, "_check_lock", lambda _root: None)
    monkeypatch.setattr(cli, "_installed_versions", lambda: ["numpy==2.1.3"])
    assert cli.check_dependencies_main(["--project-root", str(ROOT)]) == 0
    assert "PASS dependencies" in capsys.readouterr().out

    def invalid_project(_root: Path) -> dict[str, object]:
        raise ValueError("invalid metadata")

    def invalid_uv() -> str:
        raise ValueError("uv unavailable")

    def invalid_lock(_root: Path) -> None:
        raise ValueError("stale lock")

    def missing_distributions() -> list[str]:
        raise ValueError("missing packages")

    monkeypatch.setattr(cli, "_load_project", invalid_project)
    monkeypatch.setattr(cli, "_uv_version", invalid_uv)
    monkeypatch.setattr(cli, "_check_lock", invalid_lock)
    monkeypatch.setattr(cli, "_installed_versions", missing_distributions)
    monkeypatch.setattr(cli.sys, "prefix", cli.sys.base_prefix)
    assert cli.check_dependencies_main(["--project-root", str(ROOT)]) == 1
    errors = capsys.readouterr().err
    assert "invalid metadata" in errors
    assert "uv unavailable" in errors
    assert "stale lock" in errors
    assert "missing packages" in errors
    assert "managed environment" in errors
