"""Runtime narrowing for declarative ``TypedDict`` configuration schemas."""

from __future__ import annotations

import types
from collections.abc import Mapping, Sequence
from typing import (
    Any,
    Literal,
    NotRequired,
    Protocol,
    Required,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
    is_typeddict,
)

from .yaml_adapter import require_mapping, require_sequence


class _TypedDictRuntime(Protocol):
    __required_keys__: frozenset[str]


def _narrow(value: object, annotation: object, *, label: str) -> object:
    """Validate one value against the supported configuration type grammar."""
    origin = get_origin(annotation)
    arguments = get_args(annotation)

    if origin in {Required, NotRequired}:
        return _narrow(value, arguments[0], label=label)
    if origin in {types.UnionType, Union}:
        failures: list[str] = []
        for option in arguments:
            try:
                return _narrow(value, option, label=label)
            except ValueError as exc:
                failures.append(str(exc))
        raise ValueError(f"{label}: value does not match any allowed type")
    if origin is Literal:
        if value not in arguments:
            raise ValueError(f"{label}: expected one of {arguments!r}")
        return value
    if is_typeddict(annotation):
        return _typed_dict(value, annotation, label=label)
    if origin in {dict, Mapping}:
        if len(arguments) != 2 or arguments[0] is not str:
            raise TypeError(f"{label}: only Mapping[str, T] is supported")
        raw = require_mapping(value, label=label)
        return {
            key: _narrow(item, arguments[1], label=f"{label}.{key}") for key, item in raw.items()
        }
    if origin in {list, Sequence}:
        if len(arguments) != 1:
            raise TypeError(f"{label}: sequence schema needs one item type")
        return [
            _narrow(item, arguments[0], label=f"{label}[{index}]")
            for index, item in enumerate(require_sequence(value, label=label))
        ]
    if origin is tuple:
        raw_items = require_sequence(value, label=label)
        if len(arguments) == 2 and arguments[1] is Ellipsis:
            return tuple(
                _narrow(item, arguments[0], label=f"{label}[{index}]")
                for index, item in enumerate(raw_items)
            )
        if len(raw_items) != len(arguments):
            raise ValueError(f"{label}: expected {len(arguments)} items")
        return tuple(
            _narrow(item, item_type, label=f"{label}[{index}]")
            for index, (item, item_type) in enumerate(zip(raw_items, arguments, strict=True))
        )
    if annotation is None or annotation is type(None):
        if value is not None:
            raise ValueError(f"{label}: expected null")
        return None
    if annotation is bool:
        if not isinstance(value, bool):
            raise ValueError(f"{label}: expected a boolean")
        return value
    if annotation is int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{label}: expected an integer")
        return value
    if annotation is float:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{label}: expected a number")
        return value
    if annotation is str:
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label}: expected a non-empty string")
        return value
    if annotation is object:
        raise TypeError(f"{label}: object is not a sufficiently precise config type")
    if annotation is Any:
        raise TypeError(f"{label}: Any is forbidden in config schemas")
    raise TypeError(f"{label}: unsupported config annotation {annotation!r}")


def _typed_dict(value: object, schema: object, *, label: str) -> dict[str, object]:
    raw = require_mapping(value, label=label)
    annotations = get_type_hints(schema, include_extras=True)
    required = cast(_TypedDictRuntime, schema).__required_keys__
    result: dict[str, object] = {}
    for field, annotation in annotations.items():
        field_origin = get_origin(annotation)
        is_required = field_origin is not NotRequired and (
            field_origin is Required or field in required
        )
        if field not in raw:
            if is_required:
                raise ValueError(f"{label}.{field}: required field is missing")
            continue
        result[field] = _narrow(raw[field], annotation, label=f"{label}.{field}")
    return result


def parse_typed_config[Config](
    value: object,
    schema: type[Config],
    *,
    label: str,
) -> Config:
    """Validate and narrow an object to one closed ``TypedDict`` schema.

    Unknown documentation-only fields are intentionally dropped. Every field
    that can reach a calculation must be declared in the schema.
    """
    if not is_typeddict(schema):
        raise TypeError("schema must be a TypedDict class")
    return cast(Config, _typed_dict(value, schema, label=label))


__all__ = ["parse_typed_config"]
