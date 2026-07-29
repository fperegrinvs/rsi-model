"""Typed loader for the physical-autonomy governance control register."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, TypedDict

from .yaml_adapter import (
    load_yaml_mapping,
    require_mapping,
    require_number,
    require_string,
    require_string_sequence,
)

ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE_PATH = ROOT / "params" / "governance_controls.yaml"


class TrustBoundary(TypedDict):
    between: tuple[str, ...]
    failure_modes: tuple[str, ...]


class CommunicationState(TypedDict):
    authority: str
    maximum_new_capacity_fraction_per_year: float


class GovernanceControl(TypedDict):
    action: str
    verification: str
    rollback: str
    status: str


class GovernanceThreat(TypedDict):
    class_: str
    path: str
    affected_assets: tuple[str, ...]
    physical_state_trigger: str
    controls: tuple[str, ...]
    residual_risk: str


class GovernanceConfig(TypedDict):
    version: str
    status: str
    source_class: str
    actors: tuple[str, ...]
    assets: tuple[str, ...]
    trust_boundaries: Mapping[str, TrustBoundary]
    communication_states: Mapping[str, CommunicationState]
    controls: Mapping[str, GovernanceControl]
    threats: Mapping[str, GovernanceThreat]


class RecordParser[Record](Protocol):
    def __call__(self, value: object, *, label: str) -> Record: ...


def _trust_boundary(value: object, *, label: str) -> TrustBoundary:
    record = require_mapping(value, label=label)
    return {
        "between": require_string_sequence(record.get("between"), label=f"{label}.between"),
        "failure_modes": require_string_sequence(
            record.get("failure_modes"),
            label=f"{label}.failure_modes",
        ),
    }


def _communication_state(value: object, *, label: str) -> CommunicationState:
    record = require_mapping(value, label=label)
    return {
        "authority": require_string(record.get("authority"), label=f"{label}.authority"),
        "maximum_new_capacity_fraction_per_year": require_number(
            record.get("maximum_new_capacity_fraction_per_year"),
            label=f"{label}.maximum_new_capacity_fraction_per_year",
        ),
    }


def _control(value: object, *, label: str) -> GovernanceControl:
    record = require_mapping(value, label=label)
    return {
        "action": require_string(record.get("action"), label=f"{label}.action"),
        "verification": require_string(
            record.get("verification"),
            label=f"{label}.verification",
        ),
        "rollback": require_string(record.get("rollback"), label=f"{label}.rollback"),
        "status": require_string(record.get("status"), label=f"{label}.status"),
    }


def _threat(value: object, *, label: str) -> GovernanceThreat:
    record = require_mapping(value, label=label)
    return {
        "class_": require_string(record.get("class"), label=f"{label}.class"),
        "path": require_string(record.get("path"), label=f"{label}.path"),
        "affected_assets": require_string_sequence(
            record.get("affected_assets"),
            label=f"{label}.affected_assets",
        ),
        "physical_state_trigger": require_string(
            record.get("physical_state_trigger"),
            label=f"{label}.physical_state_trigger",
        ),
        "controls": require_string_sequence(
            record.get("controls"),
            label=f"{label}.controls",
        ),
        "residual_risk": require_string(
            record.get("residual_risk"),
            label=f"{label}.residual_risk",
        ),
    }


def _parse_named_records[Record](
    value: object,
    *,
    label: str,
    parser: RecordParser[Record],
) -> dict[str, Record]:
    source = require_mapping(value, label=label)
    return {name: parser(item, label=f"{label}.{name}") for name, item in source.items()}


def load_governance_controls(path: Path | None = None) -> GovernanceConfig:
    """Load and structurally validate the complete governance register."""
    source_path = path or GOVERNANCE_PATH
    raw = load_yaml_mapping(source_path)
    config: GovernanceConfig = {
        "version": require_string(raw.get("version"), label="governance.version"),
        "status": require_string(raw.get("status"), label="governance.status"),
        "source_class": require_string(
            raw.get("source_class"),
            label="governance.source_class",
        ),
        "actors": require_string_sequence(raw.get("actors"), label="governance.actors"),
        "assets": require_string_sequence(raw.get("assets"), label="governance.assets"),
        "trust_boundaries": _parse_named_records(
            raw.get("trust_boundaries"),
            label="governance.trust_boundaries",
            parser=_trust_boundary,
        ),
        "communication_states": _parse_named_records(
            raw.get("communication_states"),
            label="governance.communication_states",
            parser=_communication_state,
        ),
        "controls": _parse_named_records(
            raw.get("controls"),
            label="governance.controls",
            parser=_control,
        ),
        "threats": _parse_named_records(
            raw.get("threats"),
            label="governance.threats",
            parser=_threat,
        ),
    }
    unknown_controls = {
        control
        for threat in config["threats"].values()
        for control in threat["controls"]
        if control not in config["controls"]
    }
    if unknown_controls:
        raise ValueError(
            f"governance.threats: unknown control references {sorted(unknown_controls)}"
        )
    return config


__all__ = [
    "GOVERNANCE_PATH",
    "CommunicationState",
    "GovernanceConfig",
    "GovernanceControl",
    "GovernanceThreat",
    "TrustBoundary",
    "load_governance_controls",
]
