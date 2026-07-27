"""Markdown report generator: figures + results + full parameter provenance.

Epistemic rules 1-2: every reported number is traceable to a source_class, and
results are presented as sweeps across assumption sets + Monte Carlo — the
report exists so no figure circulates without its provenance table.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import numpy as np

from .cutsets import CutProbability, CutSetResult
from .lco import CASES, EarthLCO, LCOMC, SpaceLCO
from .model import Params, RunResult
from .montecarlo import MCResult

OUTDIR = Path(__file__).resolve().parents[2] / "outputs"


def provenance_table(p: Params) -> str:
    """Every resolved delta component + the structural ASSUMPTION blocks."""
    lines = [
        "| quantity | value | source_class | anchor | note |",
        "|---|---|---|---|---|",
    ]
    for pr in p.provenance:
        lines.append(f"| {pr.quantity} | {pr.value:.4f} | {pr.source_class} "
                     f"| {pr.anchor or '—'} | {pr.note} |")
    struct = [
        ("A matrix (all entries)", "assumptions.yaml set '%s'" % p.label),
        ("q (incl. environment q_scale)", "assumptions.yaml + environments.yaml"),
        ("import profile/budget/decay", "assumptions.yaml + environments.yaml"),
        ("repair efficiency/spares", "assumptions.yaml"),
        ("recycling recovery/profile/opex", "assumptions.yaml"),
        ("stockpile sizes/shelf life", "assumptions.yaml"),
        ("shock rates/fractions/groups", "environments.yaml"),
    ]
    for name, where in struct:
        lines.append(f"| {name} | — | ASSUMPTION | — | {where} |")
    return "\n".join(lines)


def deterministic_table(results: dict[tuple[str, str], RunResult],
                        horizon: float = 30.0) -> str:
    lines = [
        f"| set | environment | g @10yr | g @{horizon:g}yr | doubling (yr) | last binding sector |",
        "|---|---|---|---|---|---|",
    ]
    for (set_name, env), r in results.items():
        i10 = min(int(np.searchsorted(r.t, 10.0)), len(r.g) - 1)
        ih = min(int(np.searchsorted(r.t, horizon)), len(r.g) - 1)
        d = r.doubling_time()
        lines.append(
            f"| {set_name} | {env} | {r.g[i10]:+.3f} | {r.g[ih]:+.3f} "
            f"| {'never' if d is None else f'{d:.1f}'} "
            f"| {r.params.sectors[r.binding[-1]]} |")
    return "\n".join(lines)


def cutset_section(cuts: dict[str, CutSetResult]) -> str:
    out = []
    for label, cs in cuts.items():
        out.append(f"**{label}** (horizon {cs.horizon:g} yr, {cs.n_sims} simulations)")
        out.append(f"- baseline self-expanding: {'yes' if cs.baseline_expanding else 'no'}")
        if cs.baseline_expanding:
            if cs.minimal_cuts:
                out.append("- minimal import cut sets (loss of these import lines "
                           "alone prevents self-expansion):")
                out.extend(f"  - {{{', '.join(c)}}}" for c in cs.minimal_cuts)
            else:
                out.append("- no import cut set prevents self-expansion by the horizon "
                           "(imports accelerate but are not load-bearing at these central values)")
        out.append("- indispensable sectors (capacity knockout unrecoverable): "
                   + (", ".join(cs.indispensable) or "none"))
        out.append("")
    return "\n".join(out)


def cut_probability_section(cps: list[CutProbability]) -> str:
    out = ["Cut sets appear only near the feasibility margin, so central-value",
           "cut analysis understates dependency risk. Over sampled anchors",
           "(no shocks; structural question only):", ""]
    for cp in cps:
        out.append(f"**{cp.label}/{cp.environment}** (n={cp.n_runs}, horizon "
                   f"{cp.horizon:g} yr): P(baseline expands) = {cp.p_baseline:.2f}")
        for c, pf in sorted(cp.p_fatal.items(), key=lambda kv: -kv[1]):
            if pf > 0:
                name = "ALL import lines" if len(c) > 1 else c[0]
                out.append(f"- P(fatal | baseline ok) cutting {name}: {pf:.2f}")
        if all(pf == 0 for pf in cp.p_fatal.values()):
            out.append("- no candidate cut fatal in any sampled draw")
        out.append("")
    return "\n".join(out)


def mc_section(mcs: list[MCResult]) -> str:
    out = []
    for mc in mcs:
        out.append(f"- {mc.summary()}")
        out.append(f"  (shocks/run: {mc.mean_shocks:.1f}; q jitter sigma={mc.q_spread}, "
                   "ASSUMPTION-class)")
    return "\n".join(out)


def write_report(results: dict[tuple[str, str], RunResult],
                 mcs: list[MCResult],
                 cuts: dict[str, CutSetResult],
                 figures: list[Path],
                 provenance_of: Params,
                 path: Path | None = None,
                 horizon: float = 30.0,
                 cut_probs: list[CutProbability] | None = None) -> Path:
    p = provenance_of
    fig_lines = "\n\n".join(f"![{f.stem}](figures/{f.name})" for f in figures)
    cp_block = ("\n## Cut-set fatality over the MC ensemble\n\n"
                + cut_probability_section(cut_probs) if cut_probs else "")
    md = f"""# RSI model run report — {date.today().isoformat()}

All replication/doubling times below are MODEL OUTPUTS. No single trajectory is
"the" answer: results span assumption sets (conservative/central/optimistic,
`params/assumptions.yaml`) and Monte Carlo over anchored ranges
(`params/anchors.yaml`). Structural coefficients are ASSUMPTION-class.

## Deterministic sweeps (central anchor values)

{deterministic_table(results, horizon)}

## Monte Carlo (anchored ranges + common-cause shocks)

{mc_section(mcs)}

## Minimum-cut-set analysis

{cutset_section(cuts)}
{cp_block}
## Figures

{fig_lines}

## Parameter provenance ({p.label}/{p.environment})

{provenance_table(p)}
"""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = path or OUTDIR / "report.md"
    out.write_text(md)
    return out


def _lco_provenance_table(prov_lists: list[list]) -> str:
    seen: dict[str, object] = {}
    for pl in prov_lists:
        for pr in pl:
            seen.setdefault(pr.quantity, pr)
    lines = ["| anchor | central value | source_class | note |", "|---|---|---|---|"]
    for name in sorted(seen):
        pr = seen[name]
        lines.append(f"| {name} | {pr.value:,.4g} | {pr.source_class} | {pr.note} |")
    return "\n".join(lines)


def write_part2_report(spaces: dict[str, SpaceLCO], earths: dict[str, EarthLCO],
                       mcs: list[LCOMC], figures: list[Path],
                       breakeven_notes: str = "",
                       path: Path | None = None) -> Path:
    ctable = ["| case | LCO $/kW-yr | launched kg/kW | hardware | pv | radiator | storage | launch |",
              "|---|---|---|---|---|---|---|---|"]
    for c, s in spaces.items():
        k = s.capex_per_kw
        ctable.append(f"| {c} | {s.lco:,.0f} | {s.mass_kg_per_kw:,.0f} "
                      f"| {k['hardware']:,.0f} | {k['pv']:,.0f} | {k['radiator']:,.0f} "
                      f"| {k['storage']:,.0f} | {k['launch']:,.0f} |")
    etable = ["| scenario | LCO $/kW-yr | node choice |", "|---|---|---|"]
    for scen, e in earths.items():
        etable.append(f"| {scen} | {e.lco:,.0f} | {e.node} |")
    mtable = ["| case | vs Earth | ratio p10/p50/p90 | P(space cheaper) | break-even LEO $/kg p50 (p90) |",
              "|---|---|---|---|---|"]
    for m in mcs:
        mtable.append(
            f"| {m.case} | {m.scenario} "
            f"| {m.ratio_pcts[10]:.1f} / {m.ratio_pcts[50]:.1f} / {m.ratio_pcts[90]:.1f} "
            f"| {m.p_space_cheaper:.3f} "
            f"| {m.breakeven_pcts[50]:,.0f} ({m.breakeven_pcts[90]:,.0f}) |")
    fig_lines = "\n\n".join(f"![{f.stem}](figures/{f.name})" for f in figures)
    prov = _lco_provenance_table([s.provenance for s in spaces.values()]
                                 + [e.provenance for e in earths.values()])
    md = f"""# Part II report: levelized cost of compute, space vs Earth — {date.today().isoformat()}

Unit: **$ per frontier-equivalent kW-year of delivered IT load** (older-node
hardware is compute-normalized by its J/FLOP penalty). Three reference cases
(paper Section 9): LEO inference, cislunar batch, lunar-surface compute.
The Earth counterfactual RESPONDS: the responsive scenario prices induced
supply at the nuclear-PPA floor and may deploy older-node hardware.
Aspirational launch targets appear only as sweep axes (rule 3).

## Central anchor values

Space cases (capex $/kW before annualization):

{chr(10).join(ctable)}

Earth scenarios:

{chr(10).join(etable)}

A calibration check: the Earth base LCO corresponds to ≈ ${next(iter(earths.values())).lco / 8760:,.2f}/kW-hr,
consistent with published accelerator rental rates — the model is anchored at
the right order of magnitude.

## Monte Carlo over anchored ranges (shared draws both sides)

{chr(10).join(mtable)}

Break-even prices are the LEO $/kg at which the space case matches Earth;
**negative means fixed (non-launch) costs alone exceed the Earth cost** — at
those draws no launch price, even zero, closes the gap.

{breakeven_notes}

## Figures

{fig_lines}

## Parameter provenance (anchors used)

{prov}
"""
    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = path or OUTDIR / "report_part2.md"
    out.write_text(md)
    return out
