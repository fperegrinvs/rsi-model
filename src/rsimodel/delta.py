"""Decomposed capacity-loss rates and anchored-parameter resolution.

delta = wear + catastrophic + obsolescence + logistics, per sector, assembled
from params/environments.yaml. Entries either reference an anchored range in
params/anchors.yaml, a named company scenario in
params/orbital_ai_scenario_registry.json, or are bare ASSUMPTION-class floats.
Every resolved value carries a provenance record (source_class, anchor name,
note) so reports can print a full provenance table.

Anchored ranges resolve to their geometric mid deterministically; under Monte
Carlo each anchor is drawn once per run (loguniform over [low, high]) and shared
by every entry referencing it — parameter-level common-cause correlation.

Draw-stream stability: each anchor's draw is derived from a per-run
entropy integer mixed with crc32 of the anchor's NAME, not from one sequential
stream over the anchor list. Consequence: adding an anchor to anchors.yaml
never changes any other anchor's draw or the caller's RNG stream — MC results
are stable under anchor-list growth. (The sequential scheme re-rolled every
Part I cell whenever a Part II anchor was added.) This re-baselined all MC
numbers once, at introduction.
"""

from __future__ import annotations

import math
import zlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Final, NotRequired, Required, TypedDict, cast

import numpy as np

from .array_types import FloatArray, IntArray
from .yaml_adapter import (
    load_yaml,
    require_mapping,
    require_number,
    require_sequence,
    require_string,
)

PARAMS_DIR = Path(__file__).resolve().parents[2] / "params"


@lru_cache(maxsize=8)
def _load_yaml(path_str: str) -> dict[str, object]:
    """Parse-once cache; callers must treat the returned mapping as read-only."""
    return require_mapping(load_yaml(Path(path_str)), label=path_str)


DELTA_COMPONENTS: Final = ("wear", "catastrophic", "obsolescence", "logistics")


class AnchorRecord(TypedDict, total=False):
    source_class: Required[str]
    low: Required[float]
    high: Required[float]
    note: str
    value: float


class AnchorReference(TypedDict):
    anchor: str
    scale: NotRequired[float]


type ScalarEntry = float | AnchorReference
type AnchorMap = dict[str, AnchorRecord]


@dataclass(frozen=True, slots=True)
class ImportConfig:
    profile: tuple[float, ...] | None
    budget_scale: float
    decay_scale: float
    pulse_years: float | None


@dataclass(frozen=True, slots=True)
class ShockConfig:
    name: str
    rate_per_year: float
    fraction_lost: tuple[float, float]
    sectors: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EnvironmentConfig:
    note: str
    q_scale: tuple[ScalarEntry, ...]
    delta_components: dict[str, tuple[ScalarEntry, ...]]
    salvage_factors: dict[str, ScalarEntry | tuple[ScalarEntry, ...]]
    import_config: ImportConfig
    shocks: tuple[ShockConfig, ...]


@dataclass
class Provenance:
    quantity: str  # e.g. "delta.wear[power]"
    value: float
    source_class: (
        str  # peer_reviewed | technical_report | company_statement | reporting | ASSUMPTION
    )
    anchor: str | None = None
    note: str = ""


@dataclass
class Shock:
    name: str
    rate_per_year: float
    fraction_lost: tuple[float, float]  # (low, high), sampled per event
    sector_idx: IntArray = field(
        repr=False,
        default_factory=lambda: np.empty(0, dtype=np.int64),
    )


def _parse_anchor_record(value: object, *, label: str) -> AnchorRecord:
    mapping = require_mapping(value, label=label)
    source_class = require_string(mapping.get("source_class"), label=f"{label}.source_class")
    note_value = mapping.get("note", "")
    if not isinstance(note_value, str):
        raise ValueError(f"{label}.note: expected a string")
    record: AnchorRecord = {
        "source_class": source_class,
        "note": note_value,
        "low": 0.0,
        "high": 0.0,
    }
    if "value" in mapping:
        point = require_number(mapping["value"], label=f"{label}.value")
        record.update(value=point, low=point, high=point)
    elif "low" in mapping and "high" in mapping:
        low = require_number(mapping["low"], label=f"{label}.low")
        high = require_number(mapping["high"], label=f"{label}.high")
        if low > high:
            raise ValueError(f"{label}: low must not exceed high")
        record["low"] = low
        record["high"] = high
    else:
        raise ValueError(f"{label}: expected value or low/high")
    return record


def _parse_anchor_groups(groups: Mapping[str, object], *, label: str) -> AnchorMap:
    flattened: AnchorMap = {}
    for group_name, raw_entries in groups.items():
        entries = require_mapping(raw_entries, label=f"{label}.{group_name}")
        for name, raw_entry in entries.items():
            key = f"{group_name}.{name}"
            flattened[key] = _parse_anchor_record(raw_entry, label=f"{label}.{key}")
    return flattened


def load_anchors(path: Path | None = None) -> AnchorMap:
    """Flatten the generic and named-scenario registries into one anchor map."""
    anchor_path = path or PARAMS_DIR / "anchors.yaml"
    anchors = _parse_anchor_groups(_load_yaml(str(anchor_path)), label=str(anchor_path))
    if path is None or anchor_path.resolve() == (PARAMS_DIR / "anchors.yaml").resolve():
        from .orbital_ai_scenarios import scenario_anchor_tree

        scenario_groups: dict[str, object] = {}
        scenario_groups.update(scenario_anchor_tree())
        scenario_anchors = _parse_anchor_groups(
            scenario_groups,
            label="orbital_ai_scenario_registry",
        )
        overlap = set(anchors) & set(scenario_anchors)
        if overlap:
            raise ValueError(
                f"named scenario anchors must not also appear in anchors.yaml: {sorted(overlap)}"
            )
        anchors.update(scenario_anchors)
    return anchors


def anchor_value(entry: AnchorRecord, rng: np.random.Generator | None = None) -> float:
    """Central value or one bounded draw.

    Positive ranges use the established geometric-mid/log-uniform convention.
    Ranges that include zero use an arithmetic midpoint/uniform draw because a
    logarithmic distribution is undefined there (for example, zero residual
    value for an unrecoverable disposable spacecraft).
    """
    if "value" in entry:
        return float(entry["value"])
    lo, hi = float(entry["low"]), float(entry["high"])
    if lo <= 0:
        if rng is None:
            return 0.5 * (lo + hi)
        return float(rng.uniform(lo, hi))
    if rng is None:
        return float(np.sqrt(lo * hi))
    return math.exp(float(rng.uniform(math.log(lo), math.log(hi))))


def anchor_child_rng(entropy: int, name: str) -> np.random.Generator:
    """Per-anchor generator keyed by (run entropy, anchor NAME) — the draw for
    one anchor depends only on these two values, never on which other anchors
    exist or the order they appear in."""
    return np.random.default_rng([entropy, zlib.crc32(name.encode())])


def draw_anchors(anchors: AnchorMap, rng: np.random.Generator | None = None) -> dict[str, float]:
    """One value per anchor — a single shared draw per MC run.

    Consumes exactly ONE integer from `rng` per call (the run entropy),
    regardless of how many anchors exist; each anchor then draws from its own
    name-keyed child generator. See the module docstring."""
    if rng is None:
        return {name: anchor_value(entry) for name, entry in anchors.items()}
    entropy = int(rng.integers(0, 2**63))
    return {
        name: anchor_value(entry, anchor_child_rng(entropy, name))
        for name, entry in anchors.items()
    }


def resolve_entry(
    entry: ScalarEntry,
    draws: Mapping[str, float],
    anchors: AnchorMap,
    quantity: str,
) -> tuple[float, Provenance]:
    """Resolve a params-file entry: bare float = ASSUMPTION, dict = anchored."""
    return _resolve(entry, draws, anchors, quantity)


def _resolve(
    entry: ScalarEntry,
    draws: Mapping[str, float],
    anchors: AnchorMap,
    quantity: str,
) -> tuple[float, Provenance]:
    if isinstance(entry, dict):
        name = entry["anchor"]
        scale = float(entry.get("scale", 1.0))
        v = draws[name] * scale
        a = anchors[name]
        return v, Provenance(quantity, v, a["source_class"], name, a.get("note", ""))
    v = float(entry)
    return v, Provenance(quantity, v, "ASSUMPTION", None, "environments.yaml")


def _parse_scalar_entry(value: object, *, label: str) -> ScalarEntry:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    mapping = require_mapping(value, label=label)
    anchor = require_string(mapping.get("anchor"), label=f"{label}.anchor")
    entry: AnchorReference = {"anchor": anchor}
    if "scale" in mapping:
        entry["scale"] = require_number(mapping["scale"], label=f"{label}.scale")
    return entry


def _parse_scalar_entries(value: object, *, label: str) -> tuple[ScalarEntry, ...]:
    return tuple(
        _parse_scalar_entry(entry, label=f"{label}[{index}]")
        for index, entry in enumerate(require_sequence(value, label=label))
    )


def _parse_environment(value: object, *, label: str) -> EnvironmentConfig:
    mapping = require_mapping(value, label=label)
    note_value = mapping.get("note", "")
    if not isinstance(note_value, str):
        raise ValueError(f"{label}.note: expected a string")
    q_scale = _parse_scalar_entries(mapping.get("q_scale"), label=f"{label}.q_scale")

    raw_components = require_mapping(
        mapping.get("delta_components"),
        label=f"{label}.delta_components",
    )
    components = {
        component: _parse_scalar_entries(
            raw_components.get(component),
            label=f"{label}.delta_components.{component}",
        )
        for component in DELTA_COMPONENTS
    }

    raw_salvage = require_mapping(
        mapping.get("salvage_factors", {}),
        label=f"{label}.salvage_factors",
    )
    salvage: dict[str, ScalarEntry | tuple[ScalarEntry, ...]] = {}
    for component, raw_value in raw_salvage.items():
        salvage[component] = (
            _parse_scalar_entries(
                cast(object, raw_value),
                label=f"{label}.salvage_factors.{component}",
            )
            if isinstance(raw_value, list)
            else _parse_scalar_entry(raw_value, label=f"{label}.salvage_factors.{component}")
        )

    raw_import = require_mapping(mapping.get("import", {}), label=f"{label}.import")
    raw_profile = raw_import.get("profile")
    profile = (
        None
        if raw_profile is None
        else tuple(
            require_number(item, label=f"{label}.import.profile[{index}]")
            for index, item in enumerate(
                require_sequence(raw_profile, label=f"{label}.import.profile")
            )
        )
    )
    import_config = ImportConfig(
        profile=profile,
        budget_scale=require_number(
            raw_import.get("budget_scale", 1.0),
            label=f"{label}.import.budget_scale",
        ),
        decay_scale=require_number(
            raw_import.get("decay_scale", 1.0),
            label=f"{label}.import.decay_scale",
        ),
        pulse_years=(
            None
            if "pulse_years" not in raw_import
            else require_number(
                raw_import["pulse_years"],
                label=f"{label}.import.pulse_years",
            )
        ),
    )

    shocks: list[ShockConfig] = []
    raw_shocks: object = mapping.get("shocks", [])
    for index, raw_shock in enumerate(require_sequence(raw_shocks, label=f"{label}.shocks")):
        shock_label = f"{label}.shocks[{index}]"
        shock = require_mapping(raw_shock, label=shock_label)
        fractions = require_sequence(
            shock.get("fraction_lost"),
            label=f"{shock_label}.fraction_lost",
        )
        if len(fractions) != 2:
            raise ValueError(f"{shock_label}.fraction_lost: expected two bounds")
        sectors = tuple(
            require_string(item, label=f"{shock_label}.sectors[{sector_index}]")
            for sector_index, item in enumerate(
                require_sequence(shock.get("sectors"), label=f"{shock_label}.sectors")
            )
        )
        shocks.append(
            ShockConfig(
                name=require_string(shock.get("name"), label=f"{shock_label}.name"),
                rate_per_year=require_number(
                    shock.get("rate_per_year"),
                    label=f"{shock_label}.rate_per_year",
                ),
                fraction_lost=(
                    require_number(fractions[0], label=f"{shock_label}.fraction_lost[0]"),
                    require_number(fractions[1], label=f"{shock_label}.fraction_lost[1]"),
                ),
                sectors=sectors,
            )
        )
    return EnvironmentConfig(
        note=note_value,
        q_scale=q_scale,
        delta_components=components,
        salvage_factors=salvage,
        import_config=import_config,
        shocks=tuple(shocks),
    )


def load_environment(env: str, path: Path | None = None) -> EnvironmentConfig:
    source = path or PARAMS_DIR / "environments.yaml"
    raw = _load_yaml(str(source))
    envs = require_mapping(raw.get("environments"), label=f"{source}.environments")
    if env not in envs:
        raise KeyError(f"unknown environment {env!r}; have {sorted(envs)}")
    return _parse_environment(envs[env], label=f"{source}.environments.{env}")


def assemble_delta(
    env_cfg: EnvironmentConfig,
    sectors: list[str],
    anchors: AnchorMap,
    draws: Mapping[str, float] | None = None,
) -> tuple[dict[str, FloatArray], list[Provenance]]:
    """Per-component delta vectors for one environment + provenance records."""
    if draws is None:
        draws = draw_anchors(anchors)
    n = len(sectors)
    comps: dict[str, FloatArray] = {}
    prov: list[Provenance] = []
    for comp in DELTA_COMPONENTS:
        entries = env_cfg.delta_components[comp]
        if len(entries) != n:
            raise ValueError(f"{comp}: expected {n} entries, got {len(entries)}")
        vec = np.empty(n)
        for i, entry in enumerate(entries):
            vec[i], p = _resolve(entry, draws, anchors, f"delta.{comp}[{sectors[i]}]")
            prov.append(p)
        comps[comp] = vec
    return comps, prov


def load_shocks(
    env_cfg: EnvironmentConfig,
    sectors: list[str],
    rng: np.random.Generator | None = None,
) -> list[Shock]:
    """Common-cause shock definitions; rates jittered ±30% under MC (ASSUMPTION)."""
    out: list[Shock] = []
    for shock in env_cfg.shocks:
        rate = shock.rate_per_year
        if rng is not None:
            rate *= float(rng.uniform(0.7, 1.3))
        idx = np.array([sectors.index(name) for name in shock.sectors], dtype=np.int64)
        out.append(Shock(shock.name, rate, shock.fraction_lost, idx))
    return out
