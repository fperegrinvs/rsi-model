"""Decomposed capacity-loss rates and anchored-parameter resolution.

delta = wear + catastrophic + obsolescence + logistics, per sector, assembled
from params/environments.yaml. Entries either reference an anchored range in
params/anchors.yaml or are bare ASSUMPTION-class floats. Every resolved value
carries a provenance record (source_class, anchor name, note) so reports can
print a full provenance table.

Anchored ranges resolve to their geometric mid deterministically; under Monte
Carlo each anchor is drawn once per run (loguniform over [low, high]) and shared
by every entry referencing it — parameter-level common-cause correlation.

Draw-stream stability (r3.5): each anchor's draw is derived from a per-run
entropy integer mixed with crc32 of the anchor's NAME, not from one sequential
stream over the anchor list. Consequence: adding an anchor to anchors.yaml
never changes any other anchor's draw or the caller's RNG stream — MC results
are stable under anchor-list growth. (The sequential scheme re-rolled every
Part I cell whenever a Part II anchor was added.) This re-baselined all MC
numbers once, at introduction.
"""
from __future__ import annotations

import zlib
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml

PARAMS_DIR = Path(__file__).resolve().parents[2] / "params"


@lru_cache(maxsize=8)
def _load_yaml(path_str: str) -> dict:
    """Parse-once cache; callers must treat the returned dict as read-only."""
    return yaml.safe_load(Path(path_str).read_text())

DELTA_COMPONENTS = ("wear", "catastrophic", "obsolescence", "logistics")


@dataclass
class Provenance:
    quantity: str          # e.g. "delta.wear[power]"
    value: float
    source_class: str      # peer_reviewed | technical_report | company_statement | reporting | ASSUMPTION
    anchor: str | None = None
    note: str = ""


@dataclass
class Shock:
    name: str
    rate_per_year: float
    fraction_lost: tuple[float, float]   # (low, high), sampled per event
    sector_idx: np.ndarray = field(repr=False, default=None)


def load_anchors(path: Path | None = None) -> dict[str, dict]:
    """Flatten anchors.yaml to {'delta.wear_space_solar': {...}, ...}."""
    raw = _load_yaml(str(path or PARAMS_DIR / "anchors.yaml"))
    return {f"{grp}.{name}": entry
            for grp, entries in raw.items()
            for name, entry in entries.items()}


def anchor_value(entry: dict, rng: np.random.Generator | None = None) -> float:
    """Central value (geometric mid of range) or a loguniform draw."""
    if "value" in entry:
        return float(entry["value"])
    lo, hi = float(entry["low"]), float(entry["high"])
    if rng is None:
        return float(np.sqrt(lo * hi))
    return float(np.exp(rng.uniform(np.log(lo), np.log(hi))))


def anchor_child_rng(entropy: int, name: str) -> np.random.Generator:
    """Per-anchor generator keyed by (run entropy, anchor NAME) — the draw for
    one anchor depends only on these two values, never on which other anchors
    exist or the order they appear in (r3.5 draw-stream stability)."""
    return np.random.default_rng([entropy, zlib.crc32(name.encode())])


def draw_anchors(anchors: dict[str, dict],
                 rng: np.random.Generator | None = None) -> dict[str, float]:
    """One value per anchor — a single shared draw per MC run.

    Consumes exactly ONE integer from `rng` per call (the run entropy),
    regardless of how many anchors exist; each anchor then draws from its own
    name-keyed child generator. See the module docstring."""
    if rng is None:
        return {name: anchor_value(entry) for name, entry in anchors.items()}
    entropy = int(rng.integers(0, 2**63))
    return {name: anchor_value(entry, anchor_child_rng(entropy, name))
            for name, entry in anchors.items()}


def resolve_entry(entry, draws: dict[str, float], anchors: dict[str, dict],
                  quantity: str) -> tuple[float, Provenance]:
    """Resolve a params-file entry: bare float = ASSUMPTION, dict = anchored."""
    return _resolve(entry, draws, anchors, quantity)


def _resolve(entry, draws: dict[str, float], anchors: dict[str, dict],
             quantity: str) -> tuple[float, Provenance]:
    if isinstance(entry, dict):
        name = entry["anchor"]
        scale = float(entry.get("scale", 1.0))
        v = draws[name] * scale
        a = anchors[name]
        return v, Provenance(quantity, v, a["source_class"], name, a.get("note", ""))
    v = float(entry)
    return v, Provenance(quantity, v, "ASSUMPTION", None, "environments.yaml")


def load_environment(env: str, path: Path | None = None) -> dict:
    raw = _load_yaml(str(path or PARAMS_DIR / "environments.yaml"))
    envs = raw["environments"]
    if env not in envs:
        raise KeyError(f"unknown environment {env!r}; have {sorted(envs)}")
    return envs[env]


def assemble_delta(env_cfg: dict, sectors: list[str], anchors: dict[str, dict],
                   draws: dict[str, float] | None = None,
                   ) -> tuple[dict[str, np.ndarray], list[Provenance]]:
    """Per-component delta vectors for one environment + provenance records."""
    if draws is None:
        draws = draw_anchors(anchors)
    n = len(sectors)
    comps: dict[str, np.ndarray] = {}
    prov: list[Provenance] = []
    for comp in DELTA_COMPONENTS:
        entries = env_cfg["delta_components"][comp]
        if len(entries) != n:
            raise ValueError(f"{comp}: expected {n} entries, got {len(entries)}")
        vec = np.empty(n)
        for i, entry in enumerate(entries):
            vec[i], p = _resolve(entry, draws, anchors, f"delta.{comp}[{sectors[i]}]")
            prov.append(p)
        comps[comp] = vec
    return comps, prov


def load_shocks(env_cfg: dict, sectors: list[str],
                rng: np.random.Generator | None = None) -> list[Shock]:
    """Common-cause shock definitions; rates jittered ±30% under MC (ASSUMPTION)."""
    out = []
    for s in env_cfg.get("shocks", []):
        rate = float(s["rate_per_year"])
        if rng is not None:
            rate *= float(rng.uniform(0.7, 1.3))
        lo, hi = (float(v) for v in s["fraction_lost"])
        idx = np.array([sectors.index(name) for name in s["sectors"]], int)
        out.append(Shock(s["name"], rate, (lo, hi), idx))
    return out
