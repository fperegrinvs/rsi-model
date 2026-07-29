"""Typed boundary for PyYAML's dynamically typed loader."""

from __future__ import annotations

from pathlib import Path
from typing import cast

import yaml


def load_yaml(path: Path) -> object:
    """Load one YAML document without allowing PyYAML's ``Any`` to escape."""
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    return cast(object, loaded)


def pyyaml_version() -> str:
    """Return the installed PyYAML version without exposing its module object."""
    return str(yaml.__version__)


def load_yaml_mapping(path: Path, *, label: str | None = None) -> dict[str, object]:
    """Load and validate a YAML document whose root must be a string-keyed mapping."""
    return require_mapping(load_yaml(path), label=label or str(path))


def require_mapping(value: object, *, label: str) -> dict[str, object]:
    """Validate an object-valued mapping with string keys."""
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected an object")
    mapping = cast(dict[object, object], value)
    if not all(isinstance(key, str) for key in mapping):
        raise ValueError(f"{label}: every key must be a string")
    return {str(key): item for key, item in mapping.items()}


def require_sequence(value: object, *, label: str) -> list[object]:
    """Validate a YAML sequence while excluding scalar strings."""
    if not isinstance(value, list):
        raise ValueError(f"{label}: expected a list")
    return list(cast(list[object], value))


def require_string(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label}: expected a non-empty string")
    return value


def require_boolean(value: object, *, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label}: expected a boolean")
    return value


def require_number(value: object, *, label: str) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{label}: expected a number")
    return float(value)


def require_string_sequence(value: object, *, label: str) -> tuple[str, ...]:
    """Validate a YAML list containing only non-empty strings."""
    items = require_sequence(value, label=label)
    return tuple(
        require_string(item, label=f"{label}[{index}]") for index, item in enumerate(items)
    )


__all__ = [
    "load_yaml",
    "load_yaml_mapping",
    "pyyaml_version",
    "require_boolean",
    "require_mapping",
    "require_number",
    "require_sequence",
    "require_string",
    "require_string_sequence",
]
