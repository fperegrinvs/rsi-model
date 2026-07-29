"""Typed boundary around the weakly typed fontTools interface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import cast

from fontTools.ttLib import TTFont


@dataclass(frozen=True, slots=True)
class FontInspection:
    """The small font metadata surface required by the publication gate."""

    tables: frozenset[str]
    family: str | None
    style: str | None
    internal_version: str | None
    flavor: str | None


def inspect_font(path: Path) -> FontInspection:
    """Read the pinned font and return a typed projection."""
    font = TTFont(path, lazy=False)
    names = font["name"]
    return FontInspection(
        tables=frozenset(cast(list[str], font.keys())),
        family=cast(str | None, names.getDebugName(1)),
        style=cast(str | None, names.getDebugName(2)),
        internal_version=cast(str | None, names.getDebugName(5)),
        flavor=cast(str | None, font.flavor),
    )


__all__ = ["FontInspection", "inspect_font"]
