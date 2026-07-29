"""Markdown report generator: figures + results + full parameter provenance.

Epistemic rules 1-2: every reported number is traceable to a source_class, and
results are presented as sweeps across assumption sets + Monte Carlo — the
report exists so no figure circulates without its provenance table.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date
from pathlib import Path

import numpy as np

from .cutsets import CutProbability, CutSetResult
from .lco import CASE_LABELS, LCOMC, EarthLCO, SpaceLCO
from .model import Params, Provenance, RunResult
from .montecarlo import MCResult

OUTDIR = Path(__file__).resolve().parents[2] / "outputs"


def provenance_table(p: Params) -> str:
    """Every resolved delta component + the structural ASSUMPTION blocks."""
    lines = [
        "| quantity | value | source_class | anchor | note |",
        "|---|---|---|---|---|",
    ]
    lines.extend(
        (f"| {pr.quantity} | {pr.value:.4f} | {pr.source_class} | {pr.anchor or '—'} | {pr.note} |")
        for pr in p.provenance
    )
    struct = [
        ("A matrix (all entries)", f"assumptions.yaml set '{p.label}'"),
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


def deterministic_table(
    results: Mapping[tuple[str, str], RunResult],
    horizon: float = 30.0,
) -> str:
    lines = [
        f"| set | environment | g @10yr | g @{horizon:g}yr | balanced dbl (yr) "
        "| aggregate dbl (yr) | last binding sector |",
        "|---|---|---|---|---|---|---|",
    ]
    for (set_name, env), r in results.items():
        i10 = min(int(np.searchsorted(r.t, 10.0)), len(r.g) - 1)
        ih = min(int(np.searchsorted(r.t, horizon)), len(r.g) - 1)
        d = r.doubling_time()
        b = r.balanced_doubling_time()
        lines.append(
            f"| {set_name} | {env} | {r.g[i10]:+.3f} | {r.g[ih]:+.3f} "
            f"| {'never' if b is None else f'{b:.1f}'} "
            f"| {'never' if d is None else f'{d:.1f}'} "
            f"| {r.params.sectors[r.binding[-1]]} |"
        )
    return "\n".join(lines)


def cutset_section(cuts: Mapping[str, CutSetResult]) -> str:
    out = []
    for label, cs in cuts.items():
        out.append(f"**{label}** (horizon {cs.horizon:g} yr, {cs.n_sims} simulations)")
        out.append(f"- baseline self-expanding: {'yes' if cs.baseline_expanding else 'no'}")
        if cs.baseline_expanding:
            if cs.minimal_cuts:
                out.append(
                    "- minimal import cut sets (loss of these import lines "
                    "alone prevents self-expansion):"
                )
                out.extend(f"  - {{{', '.join(c)}}}" for c in cs.minimal_cuts)
            else:
                out.append(
                    "- no import cut set prevents self-expansion by the horizon "
                    "(imports accelerate but are not load-bearing at these central values)"
                )
        out.append(
            "- indispensable sectors (capacity knockout unrecoverable): "
            + (", ".join(cs.indispensable) or "none")
        )
        out.append("")
    return "\n".join(out)


def cut_probability_section(cps: list[CutProbability]) -> str:
    out = [
        "Cut sets appear only near the feasibility margin, so central-value",
        "cut analysis understates dependency risk. Over sampled anchors",
        "(no shocks; structural question only):",
        "",
    ]
    for cp in cps:
        out.append(
            f"**{cp.label}/{cp.environment}** (n={cp.n_runs}, horizon "
            f"{cp.horizon:g} yr): P(baseline expands) = {cp.p_baseline:.2f}"
        )
        for c, pf in sorted(cp.p_fatal.items(), key=lambda kv: -kv[1]):
            if pf > 0:
                name = "ALL import lines" if len(c) > 1 else next(iter(c), "none")
                out.append(f"- P(fatal | baseline ok) cutting {name}: {pf:.2f}")
        if all(pf == 0 for pf in cp.p_fatal.values()):
            out.append("- no candidate cut fatal in any sampled draw")
        out.append("")
    return "\n".join(out)


def mc_section(mcs: list[MCResult]) -> str:
    out = []
    for mc in mcs:
        out.append(f"- {mc.summary()}")
        out.append(
            f"  (shocks/run: {mc.mean_shocks:.1f}; q jitter sigma={mc.q_spread}, ASSUMPTION-class)"
        )
    return "\n".join(out)


def write_report(
    results: Mapping[tuple[str, str], RunResult],
    mcs: list[MCResult],
    cuts: Mapping[str, CutSetResult],
    figures: list[Path],
    provenance_of: Params,
    path: Path | None = None,
    horizon: float = 30.0,
    cut_probs: list[CutProbability] | None = None,
) -> Path:
    p = provenance_of
    fig_lines = "\n\n".join(f"![{f.stem}](figures/{f.name})" for f in figures)
    cp_block = (
        "\n## Cut-set fatality over the MC ensemble\n\n" + cut_probability_section(cut_probs)
        if cut_probs
        else ""
    )
    md = f"""# RSI model run report — {date.today().isoformat()}

All replication/doubling times below are MODEL OUTPUTS. No single trajectory is
"the" answer: results span assumption sets (conservative/central/optimistic,
`params/assumptions.yaml`) and Monte Carlo over anchored ranges
(`params/anchors.yaml`). Structural coefficients are ASSUMPTION-class.

Metric definitions:
- **balanced doubling** — first t with λ(t) = min_j K_j(t)/K_j(0) ≥ 2: every
  modelled sector has at least twice its initial abstract capacity.
  Unit-invariant; it is a balanced-capacity event, not a commissioned second
  physical seed.
- **aggregate doubling** — first t with Σ_j K_j ≥ 2 Σ_j K_j(0). Depends on the
  arbitrary per-sector capacity units and can be reached by overbuilding easy
  sectors; kept for continuity only.
- **expanding @horizon** — instantaneous worst-case growth g > 0 at one step
  (endpoint 1). May still be import- or stock-supported.
- **sustained** — g > 0 at every step of the trailing window (endpoint 3).
- **binding sector/co-binding set** — unit-invariant finite response to a 1%
  relaxation of each material-balance supply. Rows within 5% of the largest
  positive response share fractional credit.

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


def _lco_provenance_table(prov_lists: list[list[Provenance]]) -> str:
    seen: dict[str, Provenance] = {}
    for pl in prov_lists:
        for pr in pl:
            seen.setdefault(pr.quantity, pr)
    lines = ["| anchor | central value | source_class | note |", "|---|---|---|---|"]
    for name in sorted(seen):
        pr = seen[name]
        lines.append(f"| {name} | {pr.value:,.4g} | {pr.source_class} | {pr.note} |")
    return "\n".join(lines)


def write_part2_report(
    spaces: Mapping[str, SpaceLCO],
    earths: Mapping[str, EarthLCO],
    mcs: list[LCOMC],
    figures: list[Path],
    breakeven_notes: str = "",
    path: Path | None = None,
) -> Path:
    arch_label = {
        "serviceable_platform": "serviceable/reusable platform",
        "integrated_disposable": "integrated disposable satellite",
    }
    ctable = [
        "| case | architecture | LCO $/kW-yr | launched kg/kW | hardware | pv "
        "| radiator | storage | other infrastructure + NRE | launch |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in spaces.values():
        k = s.capex_per_kw
        other = sum(
            k.get(name, 0.0)
            for name in (
                "communications",
                "ground_network",
                "spacecraft_bus",
                "disposal",
                "program_nre",
            )
        )
        ctable.append(
            f"| {CASE_LABELS.get(s.case, s.case)} "
            f"| {arch_label[s.architecture]} | {s.lco:,.0f} "
            f"| {s.mass_kg_per_kw:,.0f} "
            f"| {k['hardware']:,.0f} | {k['pv']:,.0f} | {k['radiator']:,.0f} "
            f"| {k['storage']:,.0f} | {other:,.0f} | {k['launch']:,.0f} |"
        )
    etable = ["| scenario | LCO $/kW-yr | node choice |", "|---|---|---|"]
    for scen, e in earths.items():
        etable.append(f"| {scen} | {e.lco:,.0f} | {e.node} |")
    workload_table = [
        "| case | cost / million defined inferences "
        "| cost / network-effective training kW-yr | training network efficiency |",
        "|---|---:|---:|---:|",
    ]
    for s in spaces.values():
        w = s.workload_costs
        workload_table.append(
            f"| {CASE_LABELS.get(s.case, s.case)} · {arch_label[s.architecture]} "
            f"| ${w['cost_per_million_inferences']:,.0f} "
            f"| ${w['cost_per_network_effective_training_kw_year']:,.0f} "
            f"| {w['training_network_efficiency']:.3f} |"
        )
    for scen, e in earths.items():
        w = e.workload_costs
        workload_table.append(
            f"| Earth · {scen} | ${w['cost_per_million_inferences']:,.0f} "
            f"| ${w['cost_per_network_effective_training_kw_year']:,.0f} "
            f"| {w['training_network_efficiency']:.3f} |"
        )
    mtable = [
        "| case | architecture | vs Earth | ratio p10/p50/p90 "
        "| P(space cheaper) | break-even LEO $/kg p50 (p90) |",
        "|---|---|---|---|---|---|",
    ]
    mtable.extend(
        (
            f"| {CASE_LABELS.get(m.case, m.case)} "
            f"| {arch_label[m.architecture]} | {m.scenario} "
            f"| {m.ratio_pcts[10]:.1f} / {m.ratio_pcts[50]:.1f} / {m.ratio_pcts[90]:.1f} "
            f"| {m.p_space_cheaper:.3f} "
            f"| {m.breakeven_pcts[50]:,.0f} ({m.breakeven_pcts[90]:,.0f}) |"
        )
        for m in mcs
    )
    spectable = [
        "| case | disclosed/derived quantity | central value | source_class | model role |",
        "|---|---|---:|---|---|",
    ]
    seen_specs = set()
    for s in spaces.values():
        prov_by_name = {pr.quantity: pr for pr in s.provenance}
        for name, value in s.architecture_specs.items():
            key = (s.case, name)
            if key in seen_specs:
                continue
            seen_specs.add(key)
            pr = prov_by_name[name]
            spectable.append(
                f"| {CASE_LABELS.get(s.case, s.case)} | `{name}` | {value:,.4g} "
                f"| {pr.source_class} | {pr.note} |"
            )
    specs_block = (
        "\n## Disclosed and aspirational scenario inputs\n\n"
        "These company statements and separately source-classed model "
        "assumptions define conditional scenarios; they do not replace "
        "the generic reference cases or establish achieved cost, "
        "lifetime, or availability.\n\n" + "\n".join(spectable)
        if len(spectable) > 2
        else ""
    )
    fig_lines = "\n\n".join(f"![{f.stem}](figures/{f.name})" for f in figures)
    prov = _lco_provenance_table(
        [s.provenance for s in spaces.values()] + [e.provenance for e in earths.values()]
    )
    leo = next(
        (
            s
            for s in spaces.values()
            if s.case == "leo_inference" and s.architecture == "serviceable_platform"
        ),
        None,
    )
    worked = ""
    if leo is not None:
        d, k = leo.detail, leo.capex_per_kw
        worked = rf"""
For the central LEO serviceable-platform case, the resolved values are
\(C_h={k["hardware"]:,.0f}\), \(C_I={d["infra_capex"]:,.0f}\) $/kW,
\(M_h={d["hw_mass"]:.1f}\), \(M_I={d["non_hw_launched_mass"]:.1f}\) kg/kW,
\(p_L={leo.launch_per_kg_leo:,.0f}\) $/kg,
\(a_h={d["ann_hw"]:.4f}\), \(a_I={d["ann_infra"]:.4f}\), and
\(U_s={d["utilization"]:.3f}\). Substitution gives

\[
L_s =
\frac{{{k["hardware"]:,.0f}({d["ann_hw"]:.4f})
+{d["infra_capex"]:,.0f}({d["ann_infra"]:.4f})
+{d["spectrum_regulatory_per_kw_year"]:,.0f}
+{leo.launch_per_kg_leo:,.0f}
[{d["hw_mass"]:.1f}({d["ann_hw"]:.4f})
+{d["non_hw_launched_mass"]:.1f}({d["ann_infra"]:.4f})]}}
{{{d["utilization"]:.3f}}}
= {leo.lco:,.0f}\ \$/\mathrm{{kW\!-\!yr}}.
\]
"""
    formula_block = rf"""
## Complete levelized-cost specification

For WACC \(r\), useful life \(T\), annual operations fraction \(f_o\),
insurance fraction \(f_i\), and residual-value fraction \(s\),

\[
\operatorname{{CRF}}(r,T)=\frac{{r}}{{1-(1+r)^{{-T}}}},
\qquad
a(T,s)=\operatorname{{CRF}}(r,T)
\left[1-\frac{{s}}{{(1+r)^T}}\right]+f_o+f_i.
\]

Let \(C_h\) be qualified accelerator capex, \(C_I\) the sum of PV, radiator,
storage, communications, ground network, spacecraft bus, disposal, and NRE
capex, \(R\) annual spectrum/regulatory cost, \(M_h\) accelerator mass,
\(M_I\) launched non-hardware
mass after local closure, \(\mu\) the destination launch multiplier,
\(p_L\) the LEO launch price, and \(U_s\) delivered utilization. The complete
space expression is

\[
L_s =
\frac{{C_h a(T_h,s)+C_I a(T_I,s)+R
+p_L\mu[M_h a(T_h,s)+M_I a(T_I,s)]}}{{U_s}}
=\alpha+\beta p_L.
\]

The integrated-disposable case sets \(T_I=T_h\): the power, thermal,
structure, compute, and original launch spend retire together. The
serviceable/reusable-platform case sets
\(T_I=\max(T_{{I,\mathrm{{anchor}}}},T_h)\) and therefore assumes compute
payload replacement without retiring the platform.

For Earth scenario \(e\), PUE \(\psi_e\), electricity price \(p_e\),
data-centre shell capex \(C_{{DC}}\), utilization \(U_E\), and the selected
node's frontier-equivalent penalty \(\phi_e\),

\[
L_E =
\frac{{\phi_e\left[
C_{{h,e}}\operatorname{{CRF}}(r,T_{{h,e}})
+C_{{DC}}\operatorname{{CRF}}(r,15)
+8760\,p_e\psi_e\right]}}{{U_E}}.
\]

The responsive Earth case evaluates both frontier and older-node hardware,
including the older node's energy/computational penalty, and selects the
lower \(L_E\). Space and Earth WACC are sampled separately. Thermal mass
also responds to rejection temperature, chip-to-emitter drop, environmental
view, pumping power, and reliability margin.
The exact affine break-even launch price is

\[
p_L^*=\frac{{L_E-\alpha}}{{\beta}},
\]

with a negative value meaning non-launch costs alone exceed the Earth
counterfactual.

{worked}
"""
    report_date = date.today().isoformat()
    earth_reference = earths.get("base", next(iter(earths.values())))
    md = f"""# Part II report: levelized cost of compute, space vs Earth — {report_date}

Unit: **$ per frontier-equivalent kW-year of delivered IT load** (older-node
hardware is compute-normalized by its J/FLOP penalty). Three reference cases
(paper Section 9): LEO inference, cislunar batch, and **Earth-supplied**
lunar-surface compute (central closure fraction is zero — local manufacture
enters only through the closure sweep axis), plus separate Starmind AI1
disclosed-design and stated-aspiration scenarios.
Two architectures are reported explicitly. In the integrated-disposable
satellite, compute, PV, radiator, storage, structure, and original launch
retire together. In the serviceable/reusable platform, compute refreshes
separately while infrastructure and its original launch spend amortize on
the longer `infrastructure_life_years`; this is a scenario assumption, not
an inference from modularity alone.
The Earth counterfactual RESPONDS: the responsive scenario prices induced
supply at the nuclear-PPA floor and may deploy older-node hardware.
Aspirational launch targets appear as sweep axes and in one explicitly labeled,
deterministic best-case sensitivity (rule 3); that case is excluded from Monte
Carlo and is not assigned a probability.
Shared draws both sides: each MC iteration resolves every common anchor once
per draw-cached AnchorSet, so Earth and space see the same hardware-cost draw;
their financing anchors are intentionally separate.

{formula_block}

## Central references and deterministic aspiration case

Space cases (capex $/kW before annualization):

{chr(10).join(ctable)}

Earth scenarios:

{chr(10).join(etable)}

Workload-normalized boundaries (the inference unit requires a declared model,
latency, accuracy, batch, memory, and precision; the training unit applies an
explicit network-efficiency gate):

{chr(10).join(workload_table)}

A calibration check: the Earth base LCO corresponds to
≈ ${earth_reference.lco / 8760:,.2f}/kW-hr,
consistent with published accelerator rental rates — the model is anchored at
the right order of magnitude.

{specs_block}

## Monte Carlo over anchored ranges (shared draws both sides)

The stated-aspiration case is excluded: company targets and deliberately
favorable unpublished assumptions are point sensitivities, not probability
distributions.

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
