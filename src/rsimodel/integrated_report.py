"""Generated-artifact component for the integrated pipeline."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .integrated_artifacts import (
    SCENARIOS,
    SEED_OBJECTIVES,
    ArtifactWorkspace,
)
from .integrated_artifacts import (
    format_number as fmt,
)
from .integrated_artifacts import (
    format_year as fmt_year,
)
from .integrated_artifacts import (
    percentile_summary as pct,
)
from .integrated_types import (
    AblationResults,
    AllocationRepairResults,
    CapacityRuns,
    CertificateResults,
    ClosureAblations,
    ComputeComparison,
    DebrisRuns,
    DeploymentResults,
    DiagnosticsResults,
    EconomicResults,
    ElectronicsArchitectureResults,
    EndpointResults,
    EnsembleResults,
    EnvironmentEffectResults,
    FrontierResults,
    IntegratedParams,
    KnowledgeRegimeResults,
    LimitedStepResults,
    ObjectiveSeedResults,
    ParetoDesigns,
    PolicyRobustnessResults,
    RegimeResults,
    SeedResults,
    ShellDebrisResult,
)


def write_report(
    workspace: ArtifactWorkspace,
    params: IntegratedParams,
    seeds: SeedResults,
    runs: CapacityRuns,
    extended_runs: CapacityRuns,
    objective_seeds: ObjectiveSeedResults,
    deployments: DeploymentResults,
    ensembles: EnsembleResults,
    compute: ComputeComparison,
    debris_runs: DebrisRuns,
    shell_debris: ShellDebrisResult,
    endpoints: EndpointResults,
    ablations: AblationResults,
    closure_matrix: ClosureAblations,
    frontiers: FrontierResults,
    diags: DiagnosticsResults,
    certs: CertificateResults,
    limited: LimitedStepResults,
    regimes: RegimeResults,
    allocation_repair: AllocationRepairResults,
    knowledge_regimes: KnowledgeRegimeResults,
    environment_effects: EnvironmentEffectResults,
    policy_robustness: PolicyRobustnessResults,
    electronics_architectures: ElectronicsArchitectureResults,
    economics: EconomicResults,
    pareto_designs: ParetoDesigns,
) -> Path:
    lines = [
        "# Current integrated-bootstrap model",
        "",
        f"- model version: `{params.version}`",
        (
            f"- assumption ensemble: n={workspace.ensemble_size} per scenario, "
            f"seed={workspace.ensemble_seed}"
        ),
        "- epistemic status: scenario implications, not measurements or forecasts",
        "",
        "## Headline results",
        "",
        "| scenario | central installed seed mass | Earth strategic-material import stock | "
        "aggregate operating-capacity doubling (80y extension) | "
        "cell-equivalents at year 40 | design-space occupancy | ensemble seed p10/p50/p90 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in SCENARIOS:
        s, e = seeds[name], ensembles[name]
        r = runs.get(name)
        extended = extended_runs.get(name)
        mass_p = pct(e.seed_masses_t)
        mass_text = "—" if mass_p is None else "/".join(f"{v:,.0f}" for v in mass_p) + " t"
        if not s.feasible:
            lines.append(
                f"| {name} | infeasible | — | — | — | {e.n_feasible}/{e.n_runs} | {mass_text} |"
            )
        else:
            lines.append(
                f"| {name} | {fmt(s.total_seed_mass_t)} t | "
                f"{fmt(s.import_stock_mass_t)} t | "
                f"{fmt_year(None if extended is None else extended.aggregate_doubling_year)} | "
                f"{fmt(None if r is None else r.operating_cells[-1], 2)} | "
                f"{e.n_feasible}/{e.n_runs} | {mass_text} |"
            )
    lines += [
        "",
        "The ensemble counts are occupancy under the declared log-uniform "
        "sampling measure. They are neither calibrated probabilities nor "
        "empirical success rates.",
        "",
        "The strict lunar-only case is a structural infeasibility inside the declared "
        "architecture: trace lunar yields cannot supply the configured "
        "electronics and process-equipment stack, in the central case and in every "
        "ensemble draw. It is not a proof that lunar-only "
        "closure is physically impossible; substitution, different recipes, new "
        "processes, or measured richer deposits could change the constraint graph.",
        "",
        "The Moon–asteroid case is likewise conditional. Its `diverse_asteroid_portfolio` "
        "is a deliberately composite source with ASSUMPTION-class recoverable yields. "
        "The model says what those yields would imply; it does not establish that a "
        "specific accessible portfolio has them.",
        "",
        "The aggregate material model is now paired with a process-closure "
        "acceptance contract covering typed source, species, process, part, "
        "parent-tool, transport, and waste nodes; grade progression; critical "
        "part ancestry; source/fleet evidence; and eight binary gates. Every "
        "gap-register row remains `evidence_pending`; no process-feasible "
        "closure is claimed. See "
        "`docs/PROCESS_CLOSURE_ACCEPTANCE_CONTRACT.md` and "
        "`tables/process_closure_gap_register.csv`.",
        "",
        "## What changed from the inherited model",
        "",
        f"- {params.n} sectors, including seven separate electronics tiers.",
        f"- {params.m} element/material categories with explicit bills of material.",
        "- Earth→Moon strategic-material import stock, asteroid→Moon feed, and "
        "Moon→orbit finished-compute arcs.",
        "- Task coverage, intervention demand, lunar-gravity process compatibility, and "
        "centrifuge mass/power overhead.",
        "- Construction lag, commissioning ramp, minimum viable scale, and an explicit "
        "aggregate operating-capacity doubling threshold.",
        "- All 18 sector capacities remain stateful through commissioning, "
        "cohort-resolved ramp, and depreciation; aggregate cell-equivalents are the slowest "
        "normalized operating sector, not the state.",
        "- A diagnostic allocator can build sectors independently, and the "
        "repair diagnostic consumes parts, repair service, intervention "
        "capacity, and queue time before returning failures to operation.",
        "- Delivered, staged, installed, commissioned, failed-startup, "
        "recovered, and operating seed states are explicit; delivered mass "
        "includes logistics hardware, packaging, spares, calibration, and "
        "startup-energy storage.",
        "- Coupled local compute, verified intelligence improvement, autonomy, and productivity.",
        "- Rate-limited Earth and Earth-fed orbital counterfactuals.",
        "- Active, derelict, and fragment stocks with a five-year fragment "
        "creation-to-clearance ratio.",
        "",
        "## Central process and seed diagnostics",
        "",
    ]
    for name in SCENARIOS:
        s = seeds[name]
        lines += [
            f"### {name}",
            "",
            f"- status: {s.status}",
            f"- minimum task coverage: {s.minimum_task_coverage:.3f}",
        ]
        if s.feasible:
            lines += [
                f"- residual intervention: {s.intervention_hours_per_year:,.1f} h/year",
                f"- lunar feed: {s.lunar_feed_t_per_year:,.1f} t/year",
                f"- asteroid feed: {s.asteroid_feed_t_per_year:,.1f} t/year",
                "- tight constraints: "
                + ", ".join(
                    f"`{label}` ({slack:+.2e})" for label, slack in s.binding_constraints[:5]
                ),
            ]
        lines.append("")

    lines += [
        "## Delivered-to-operating seed stage (r4.0)",
        "",
        "The LP mass is an installed-seed quantity. The deployment diagnostic "
        "adds transport packaging, unloading and site equipment, calibration "
        "references, initial spares, and startup-energy storage, then moves "
        "the core seed through distinct states. Eight percent of newly "
        "commissioned core mass enters a declared startup-failure queue and "
        "must consume spares before it can operate. All deployment "
        "coefficients are explicit `ASSUMPTION`s with a bounding argument; "
        "they are not a mission estimate. Machine-readable: "
        "`tables/seed_deployment_trajectory.csv`.",
        "",
        "| scenario | installed seed | delivered seed | logistics increment | "
        "startup energy | first operation | full operating seed | recovered startup failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, d in deployments.items():
        lines.append(
            f"| {name} | {d.installed_seed_mass_t:.1f} t | "
            f"{d.delivered_seed_mass_t:.1f} t | {d.logistics_mass_t:.1f} t | "
            f"{d.startup_energy_mwh:.1f} MWh | "
            f"{fmt_year(d.first_operating_year)} | "
            f"{fmt_year(d.full_operating_seed_year)} | "
            f"{d.recovered_startup_failure_t:.1f} t |"
        )
    lines += [
        "",
        "## Compute regimes at year 40",
        "",
        "| regime | normalized capacity |",
        "|---|---:|",
        f"| off-world endogenous total | {compute.endogenous[-1]:.2f} |",
        f"| Moon→orbit endogenous export | {compute.endogenous_orbit[-1]:.2f} |",
    ]
    for label in ("tight", "base", "responsive"):
        lines.append(f"| Earth-fed orbit, {label} | {compute.earth_fed_orbit[label][-1]:.2f} |")
    lines += [
        "",
        "The endogenous curve compounds only after the seed survives commissioning "
        "and source constraints. Earth-fed orbital capacity remains an affine "
        "deployment process and approaches a depreciation-limited stock at constant "
        "delivery. The terrestrial curves are rate-and-site-ceiling scenarios, not "
        "forecasts of actual buildout.",
        "",
        "## Debris condition",
        "",
        "| case | creation-to-clearance ratio, last 5 yr | "
        "clearance >= creation | fragment index, year 40 |",
        "|---|---:|:---:|---:|",
    ]
    for d in debris_runs:
        lines.append(
            f"| {d.label} | {d.creation_clearance_ratio:.2f} | "
            f"{'yes' if d.subcritical else 'no'} | {d.fragments[-1]:.3f} |"
        )
    lines += [
        "",
        "A dense shell is not licensed by industrial closure alone. In this scenario "
        "record, rapid endogenous deployment creates several times the fragments it "
        "clears under both weak and strong shell mitigation (the ratio is a flow "
        "ratio, not a branching-process reproduction number). The "
        "sparse/distributed topology sits at the "
        "boundary ratio only because its collision kernel is explicitly lower; "
        "that multiplier is an assumption to be replaced by shell- and trajectory-specific data.",
        "",
        "### Finite-mass, shell-resolved diagnostic",
        "",
        "A second diagnostic resolves 400-km LEO, 650-km LEO, and cislunar "
        "regions; active assets, intact derelicts, trackable fragments, and "
        "untrackable fragments; density/volume kernels; avoidance saturation; "
        "cross-shell fragment transport; disposal, natural clearance, "
        "retrieval, and active removal. Requested deployment consumes a finite "
        "feed inventory supplied by time-limited Earth import, depletion of a "
        "finite capture reservoir, and recovered retirements. Collision losses "
        "reduce returned active capacity and enter replacement/import cost.",
        "",
        "| shell | active capacity, year 40 | intact derelicts | trackable | "
        "untrackable | expected hazardous-descendant ratio |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for s, shell in enumerate(shell_debris.shells):
        lines.append(
            f"| {shell} | {shell_debris.active_capacity[-1, s]:.3f} | "
            f"{shell_debris.intact_derelicts[-1, s]:.3f} | "
            f"{shell_debris.trackable_fragments[-1, s]:.3f} | "
            f"{shell_debris.untrackable_fragments[-1, s]:.3f} | "
            f"{shell_debris.branching_ratio_by_shell[s]:.3f} |"
        )
    lines += [
        "",
        f"At year 40 the finite reservoir retains "
        f"{shell_debris.uncaptured_reservoir_t[-1]:.1f} t and feed inventory "
        f"retains {shell_debris.feed_inventory_t[-1]:.1f} t; cumulative "
        f"requested-deployment shortfall is "
        f"{shell_debris.deployment_shortfall_units.sum():.2f} normalized "
        f"units. Replacement/import cost under the declared delivered-mass "
        f"price is ${shell_debris.replacement_and_import_cost_usd / 1e6:.1f}M. "
        "The descendant ratio is a branching-style stress metric rather than "
        "the legacy creation/clearance flow ratio. Machine-readable: "
        "`tables/orbital_mass_balance.csv` and "
        "`tables/shell_debris_trajectory.csv`.",
        "",
        "## Governance threat/control traceability (r4.0)",
        "",
        "The governance model names actors, assets, trust boundaries, "
        "normal/delayed/lost-link authority, threat paths, and "
        "controls with verification, rollback, and residual risk. Controls "
        "map to live build rate, sector floors, repair queues, source flows, "
        "commissioning cohorts, debris state, and independent inventory "
        "measurements. Every control remains `requirement_unvalidated`; this "
        "is not a solved safety case. See `docs/GOVERNANCE_THREAT_MODEL.md` "
        "and `tables/governance_threat_control_traceability.csv`.",
        "",
        "The linked Stage-0 protocol converts those controls into ten binary "
        "acceptance gates, a typed raw-event contract, a fault campaign that "
        "covers every registered threat plus communication loss, and explicit "
        "model-parameter replacement rules. Every checklist row is still "
        "`execution_pending` or `data_pending`: the protocol is executable, "
        "but no physical rehearsal result is claimed. See "
        "`docs/TERRESTRIAL_REHEARSAL_PROTOCOL.md` and "
        "`tables/rehearsal_acceptance_matrix.csv`.",
        "",
        "## Terminal-window operating-capacity endpoints (r4.0)",
        "",
        "Aggregate operating-capacity doubling is a threshold crossing of "
        "the slowest normalized sector; these endpoints separately report "
        "retention and final-five-year direction. The central 80-year "
        "extension is in `tables/long_horizon_endpoints.csv`; the complete "
        "sector trajectory is in `tables/sector_capacity_trajectory.csv`.",
        "",
        "| scenario | aggregate doubling | at year 40 | retained >= 2 | net final-5y | "
        "ensemble retained | ensemble terminal-window expanding |",
        "|---|---:|---:|:---:|---:|---:|---:|",
    ]
    for name, d in diags.items():
        e = endpoints.get(name)
        if e is None:
            lines.append(f"| {name} | — | — | — | — | 0/{d.n_runs} | 0/{d.n_runs} |")
        else:
            lines.append(
                f"| {name} | {fmt_year(e.aggregate_doubling_year)} | "
                f"{e.operating_at_horizon:.2f} | "
                f"{'yes' if e.retained_at_horizon else 'no'} | "
                f"{e.net_capacity_change_final5:+.3f} | "
                f"{d.n_retained}/{d.n_feasible} | "
                f"{d.n_terminal_window_expanding}/{d.n_feasible} |"
            )
    network_endpoint = endpoints["moon_asteroid_network"]
    lines += [
        "",
        "Reading: the terrestrial rehearsal and lunar strategic-material "
        "bridge never reach aggregate doubling in the 80-year extension and "
        "are contracting at year 40. The Moon–asteroid network is "
        f"terminal-window expanding, reaches "
        f"{network_endpoint.operating_at_horizon:.2f} equivalents at year 40, "
        f"and first crosses two at year "
        f"{network_endpoint.aggregate_doubling_year:.2f}. "
        "Import-pool "
        "exhaustion years are per-category first "
        "dips of the pooled inventory (initial Earth stock plus recycled "
        "returns and local production) and are reported in "
        "`tables/import_stock_composition.csv`; pools can refill later from "
        "local production, so a first dip is not permanent depletion.",
        "",
        "## Intelligence-coupling ablations (r4.0)",
        "",
        "Zero/freeze ablations of the declared coupling coefficients; the "
        "seed LP does not read the intelligence block, so dynamics variants "
        "share the central seed. Machine-readable: `tables/ablations.csv`.",
        "",
        "| scenario | variant | aggregate doubling | at year 40 | growth share of baseline |",
        "|---|---|---:|---:|---:|",
    ]
    for name, rows in ablations.items():
        for a in rows:
            doubling = (
                "—" if a.aggregate_doubling_year is None else f"{a.aggregate_doubling_year:.2f} yr"
            )
            endpoint = "infeasible" if not a.feasible else f"{a.operating_at_horizon:.2f}"
            growth_share = (
                "—" if a.growth_share_of_baseline is None else f"{a.growth_share_of_baseline:.0%}"
            )
            lines.append(f"| {name} | {a.variant} | {doubling} | {endpoint} | {growth_share} |")
    lim_text = "; ".join(f"{name}: {lim}/{tot}" for name, (lim, tot) in limited.items())
    regime_text = "; ".join(
        f"{name}: material {r.material_limited}, service {r.service_limited}, "
        f"order-cap {r.order_rate_limited}"
        for name, r in regimes.items()
    )
    network_ablation = {row.variant: row for row in ablations["moon_asteroid_network"]}
    network_baseline = network_ablation["baseline"]
    network_uncoupled = network_ablation["both_couplings_frozen"]
    capital_only_doubling = next(
        row.aggregate_doubling_year
        for row in closure_matrix
        if not row.verified_ai_rd_loop and row.reproductive_capital_loop
    )
    lines += [
        "",
        "Finding: sector resolution separates regimes that a scalar aggregate "
        f"conflates ({lim_text} steps material-limited). The terrestrial "
        "and lunar-bridge trajectories remain overwhelmingly material-limited, "
        "so coupling ablations move their year-40 endpoints by less than a "
        "tenth of one percent. In the Moon–asteroid network, however, the "
        f"fully uncoupled run reaches "
        f"{network_uncoupled.operating_at_horizon:.2f} sector-balanced "
        f"equivalents versus {network_baseline.operating_at_horizon:.2f} at "
        f"baseline, retaining about "
        f"{network_uncoupled.growth_share_of_baseline:.0%} of baseline net "
        "growth. The "
        "dynamic coupling is therefore operative only after the diverse "
        "source vector relaxes the material bottleneck. The declared starting "
        "AI level also remains load-bearing statically: sizing at base "
        "autonomy makes the bridge and network seeds infeasible.",
        "",
        "The orthogonal 2×2 screen in "
        "`tables/closure_loop_ablation_matrix.csv` separates the verified "
        "AI-R&D proxy from reproductive capital. The bounded-controller, "
        "capital-reproducing cell reaches balanced doubling at "
        f"{capital_only_doubling:.2f} years; "
        "the active AI-R&D proxy without capital reproduction never doubles. "
        "Endogenous physical compounding therefore does not logically require "
        "open-ended digital improvement, while digital improvement alone does "
        "not create self-replicating capital.",
        "",
        "The exhaustive primary-constraint classification is "
        f"{regime_text} (160 quarterly steps each). Machine-readable: "
        "`tables/dynamic_regime_summary.csv`.",
        "",
        "## Knowledge and observable autonomy gates (r4.0)",
        "",
        "The 5 t knowledge package is now decomposed into storage/compute, "
        "software/toolchains, calibration references, laboratory equipment, "
        "consumables/recipes, and test articles. Each sector reports named-task "
        "completion, intervention demand, fault diagnosis, verification "
        "throughput, engineering-cycle time, process yield, repair success, "
        "mean time to recovery, and a non-divisible stop-line pass. These are "
        "ASSUMPTION-class diagnostic mappings pending Stage-0 measurements, "
        "not evidence that the capabilities exist. Machine-readable: "
        "`tables/knowledge_autonomy_observables.csv`.",
        "",
        "Two-year zero-capacity windows isolate the autonomy, verification, "
        "and compute regimes; a 90% advanced-logic/memory loss at year 5 "
        "isolates repair. The zero-capacity windows are adversarial boundary "
        "tests, not frequency estimates.",
        "",
        "| scenario | variant | at year 40 | doubling | material | autonomy | "
        "verification | repair | compute | service | order-cap |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, rows in knowledge_regimes.items():
        for r in rows:
            lines.append(
                f"| {name} | {r.variant} | {r.operating_at_horizon:.2f} | "
                f"{fmt_year(r.aggregate_doubling_year)} | "
                f"{r.material_steps} | {r.autonomy_steps} | "
                f"{r.verification_steps} | {r.repair_steps} | "
                f"{r.compute_steps} | {r.service_steps} | "
                f"{r.order_rate_steps} |"
            )
    lines += [
        "",
        "The declared central cases remain material/order-cap limited. The "
        "adversarial windows create the named regimes mechanically and reduce "
        "the Moon–asteroid endpoint; this demonstrates classification and "
        "falsification plumbing, not calibrated outage risk. Machine-readable: "
        "`tables/knowledge_regime_summary.csv`.",
        "",
        "## Operating-environment/process coupling (r4.0)",
        "",
        "The central release remains on the identity `centrifuge_only` profile "
        "for continuity. Separate nominal and adverse lunar profiles apply "
        "process-specific throughput, quality-yield, power-demand, and "
        "depreciation multipliers for dust, traction, reduced convection, "
        "vacuum behavior, radiation, thermal cycling, contamination, and "
        "calibration drift. Every multiplier is an explicit bounding "
        "`ASSUMPTION`; Earth rehearsal results do not transfer to these "
        "profiles automatically.",
        "",
        "| scenario | environment | feasible | seed mass | top binding row | "
        "at year 40 | doubling | survived |",
        "|---|---|:---:|---:|---|---:|---:|:---:|",
    ]
    for name, rows in environment_effects.items():
        for r in rows:
            lines.append(
                f"| {name} | {r.environment_profile} | "
                f"{'yes' if r.feasible else 'no'} | "
                f"{fmt(r.seed_mass_t)} t | "
                f"{r.top_binding_constraint or '—'} | "
                f"{fmt(r.operating_at_horizon, 2)} | "
                f"{fmt_year(r.aggregate_doubling_year)} | "
                f"{'—' if r.survived is None else ('yes' if r.survived else 'no')} |"
            )
    lines += [
        "",
        "The nominal/adverse penalties change seed mass and binding rows; the "
        "adverse lunar bridge becomes LP-infeasible. Some feasible penalized "
        "profiles can improve the year-40 trajectory because the minimum-mass "
        "LP responds by installing more initial capacity. That is an objective "
        "frontier artifact, not evidence that a harsher environment helps. "
        "Machine-readable: `tables/environment_process_effects.csv`.",
        "",
        "## Policy and structural-uncertainty robustness (r4.0)",
        "",
        "A one-factor-at-a-time sweep varies advanced-logic knockout fraction, "
        "event time, horizon, retained initial import stock, initial surplus, "
        "and obsolescence/depreciation. It compares balanced, live maximin, "
        "20%-reserve surplus-preserving, generic shock-aware, and exact "
        "perfect-foresight policies. Counts below are design-case occupancy "
        "over the enumerated deterministic cases, not probabilities.",
        "",
        "| scenario | policy | cases | survived | survived + terminally expanding |",
        "|---|---|---:|---:|---:|",
    ]
    for name, rows in policy_robustness.items():
        for policy in (
            "balanced",
            "maximin_sector",
            "surplus_preserving",
            "shock_aware",
            "perfect_foresight",
        ):
            selected = [r for r in rows if r.policy == policy]
            survived_count = sum(r.survived for r in selected)
            robust_count = sum(r.survived and r.terminal_window_expanding for r in selected)
            lines.append(
                f"| {name} | {policy} | {len(selected)} | {survived_count} | {robust_count} |"
            )
    lines += [
        "",
        "The machine-readable sweep reports minimum live sector margin and "
        "first aggregate doubling for every case, making failure boundaries "
        "inspectable rather than reducing them to one rank correlation. "
        "`tables/policy_robustness_sweep.csv` is authoritative.",
        "",
        "## Tiered electronics closure and inventory life (r4.0)",
        "",
        "The integrated layer no longer uses the inherited scalar electronics "
        "productivity range in its headline analysis. Seven tiers now carry "
        "separate local-producibility, replacement, shelf-life, obsolescence, "
        "and substitution assumptions. Imported tier inventory decays before "
        "use, and the architecture comparison includes frontier-local, "
        "permanent-import, mature/repairable, and cannibalization-based cases.",
        "",
        "| scenario | architecture | viable tiers | total tier shortfall | "
        "gross permanent-import mass | first shortfall |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for name, rows in electronics_architectures.items():
        for architecture in params.electronics_closure["architectures"]:
            selected = [r for r in rows if r.architecture == architecture]
            first = [r.first_shortfall_year for r in selected if r.first_shortfall_year is not None]
            lines.append(
                f"| {name} | {architecture} | "
                f"{sum(r.viable for r in selected)}/{len(selected)} | "
                f"{sum(r.shortfall_capacity for r in selected):.3f} | "
                f"{sum(r.imported_mass_t for r in selected):.1f} t | "
                f"{fmt_year(min(first) if first else None)} |"
            )
    lines += [
        "",
        "Every tested architecture still develops a shortfall in advanced "
        "logic/memory or process-equipment/metrology under the expanding "
        "Moon–asteroid demand path; fixed imports proportional to the initial "
        "seed do not scale with endogenous demand. The most decision-reducing "
        "measurements are therefore demonstrated mature-node wafer yield and "
        "parent-tool/calibration replacement demand, followed by useful life "
        "and permanent-import mass per service-year. The strict-lunar minimum "
        "cut remains tiered in the seed LP and is not erased by these dynamic "
        "inventory cases. Machine-readable: "
        "`tables/electronics_architecture_comparison.csv`.",
        "",
        "The empirical-calibration contract separates the Earth reference, "
        "serviceable space platform, and integrated disposable cases; requires "
        "equal-workload records; binds six evidence packages to current model "
        "parameters; preserves correlated reliability, link, thermal, Earth-"
        "resource, demand, and financing uncertainty; and defines an audited "
        "cash-flow event ledger with chronological holdout validation. All "
        "readiness rows remain `data_pending`. See "
        "`docs/ECONOMIC_CALIBRATION_PROTOCOL.md` and "
        "`tables/economic_calibration_readiness.csv`.",
        "",
        "The publication contract names target and fallback venues for all "
        "three papers and measures each draft against current publisher "
        "requirements. Machine-checkable structure now passes where supplied, "
        "while references, fallback word-count expansion, live-portal fields, "
        "and every author-controlled declaration remain explicitly pending. "
        "See `docs/VENUE_SELECTION_AND_CONFORMANCE.md` and "
        "`tables/publication_readiness.csv`.",
        "",
        "## Symmetric dynamic economics (r4.0)",
        "",
        "Earth and space now use the same reinvestment/debt logic: endogenous "
        "investment, learning, depreciation/obsolescence, regulatory build "
        "queues, debt-to-revenue limits, interest, bridge financing, market "
        "demand, and expanding resource ceilings. Space is additionally capped "
        "by the physical model and pays for its funded share of industrial "
        "orders, source transfer, and intervention. The coefficients are "
        "ASSUMPTION-class scenario mechanics, not a valuation.",
        "",
        "| market | technical space at year 40 | funded space | Earth | "
        "space finance-limited steps | Earth finance-limited steps | "
        "space self-financing | Earth self-financing |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for market, r in economics.items():
        lines.append(
            f"| {market} | {r.technical_space_capacity[-1]:.2f} | "
            f"{r.funded_space_capacity[-1]:.2f} | "
            f"{r.earth_capacity[-1]:.2f} | "
            f"{r.space_finance_constrained_steps} | "
            f"{r.earth_finance_constrained_steps} | "
            f"{fmt_year(r.space_self_financing_year)} | "
            f"{fmt_year(r.earth_self_financing_year)} |"
        )
    lines += [
        "",
        "Physical compounding does not automatically fund deployment. In the "
        "commodity case, finance activates only a small fraction of technically "
        "available space capacity while Earth expands endogenously. A "
        "space-native price premium funds more of the physical path, but the "
        "space case still does not repay its declared external capital inside "
        "40 years. P3b therefore remains a conditional economic proposition, "
        "not a consequence of the physical growth curve. Machine-readable: "
        "`tables/symmetric_dynamic_economics.csv`.",
        "",
        "## Composition-changing robust-seed Pareto search (r4.0)",
        "",
        "The design search now changes process route, sector redundancy, and "
        "lunar/asteroid source allocation instead of merely relabeling one LP "
        "objective or scaling a fixed vector. It minimizes delivered mass, "
        "Earth import, intervention, and doubling time while maximizing "
        "year-40 capacity and capacity after a five-year asteroid-source "
        "outage. Dominance is computed across all six objectives.",
        "",
        "| route | redundancy | source portfolio | delivered mass | doubling | "
        "year 40 | after outage | Pareto | robust |",
        "|---|---|---|---:|---:|---:|---:|:---:|:---:|",
    ]
    for r in pareto_designs:
        if not r.non_dominated:
            continue
        lines.append(
            f"| {r.route} | {r.redundancy} | {r.source_portfolio} | "
            f"{r.delivered_mass_t:.1f} t | "
            f"{fmt_year(r.aggregate_doubling_year)} | "
            f"{r.operating_at_horizon:.2f} | "
            f"{r.source_outage_operating_at_horizon:.2f} | yes | "
            f"{'yes' if r.robust_candidate else 'no'} |"
        )
    robust = [r for r in pareto_designs if r.robust_candidate]
    minimum_robust = min(robust, key=lambda r: r.delivered_mass_t)
    lines += [
        "",
        f"The minimum delivered-mass robust candidate in this enumerated "
        f"design space is `{minimum_robust.route}` / "
        f"`{minimum_robust.redundancy}` / "
        f"`{minimum_robust.source_portfolio}` at "
        f"{minimum_robust.delivered_mass_t:.1f} t. This is an "
        "ASSUMPTION-conditioned discrete frontier, not a globally optimal "
        "mission design. Machine-readable dominated and non-dominated points: "
        "`tables/robust_seed_pareto.csv`.",
        "",
        "## Allocation, repair, and shock-policy comparison (r4.0)",
        "",
        "The published central case retains balanced build packets for "
        "continuity. The structural diagnostic below instead maximizes the "
        "weakest live sector margin, then minimizes installed mass at that "
        "margin. Repair uses the declared ASSUMPTION-class parts, service, "
        "intervention, and lag coefficients. The shock removes 50% of the "
        "advanced-logic/memory sector at year 20; it is a deterministic "
        "stress case, not a frequency estimate. Machine-readable: "
        "`tables/allocation_repair_comparison.csv`.",
        "",
        "| scenario | policy | repair | shock | doubling | at year 40 | "
        "minimum sector margin | survived | shock recovery |",
        "|---|---|:---:|---|---:|---:|---:|:---:|---:|",
    ]
    for name, rows in allocation_repair.items():
        for r in rows:
            lines.append(
                f"| {name} | {r.policy} | "
                f"{'yes' if r.repair_enabled else 'no'} | {r.shock} | "
                f"{fmt_year(r.aggregate_doubling_year)} | "
                f"{r.operating_at_horizon:.2f} | "
                f"{r.minimum_sector_margin_at_horizon:.2f} | "
                f"{'yes' if r.survived else 'no'} | "
                f"{fmt_year(r.shock_recovery_year)} |"
            )
    lines += [
        "",
        "These policy outcomes are not new feasibility claims: the allocator "
        "and repair coefficients expose how strongly the result depends on "
        "construction policy and recoverability. They replace the earlier "
        "implicit claim that only balanced copies can be ordered.",
        "",
        "## Installed-mass versus aggregate-doubling frontier (r4.0)",
        "",
        "A factor-f seed installs f cell-equivalents of the minimum-mass "
        "design (capacities, feeds, strategic import stock scale with f; "
        "the digital package is shared). Time is first passage to one *additional* "
        "operating cell-equivalent, so f = 1 coincides with the canonical "
        "metric. The oversize factor is a sweep axis, not a new assumption. "
        "Machine-readable: `tables/oversize_frontier.csv`; figure: "
        "`figures/oversize_frontier.png`.",
        "",
        "| scenario | factor | installed mass | time to +1 cell | additional cells at year 40 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, rows in frontiers.items():
        for r in rows:
            additional_cell_time = (
                "—"
                if r.time_to_one_additional_cell is None
                else f"{r.time_to_one_additional_cell:.2f} yr"
            )
            lines.append(
                f"| {name} | ×{r.oversize_factor:g} | "
                f"{r.installed_mass_t:,.1f} t | "
                f"{additional_cell_time} | {r.additional_cells_at_horizon:+.2f} |"
            )
    lines += [
        "",
        "The sector-resolved frontier reverses the earlier scalar-state "
        "reading. Neither the terrestrial nor lunar bridge design reaches "
        "one additional balanced cell-equivalent at any tested scale by "
        "year 40. The Moon–asteroid minimum-mass design also misses that "
        "threshold, while 1.25x, 1.5x, and 2x scaled designs reach it at "
        "39.25, 38.5, and 37.25 years. Scaling one fixed composition is "
        "still not a "
        "multi-objective redesign.",
        "",
        "## Alternative seed objectives (r4.0)",
        "",
        "The same seed LP was solved lexicographically for minimum installed "
        "mass, minimum Earth-import mass, and minimum annual intervention, "
        "with installed mass as the secondary tie-break for the latter two. "
        "Machine-readable: `tables/seed_objective_comparison.csv`.",
        "",
        "| scenario | objective | installed mass | import mass | intervention | "
        "capacity-vector distance from mass optimum |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for name, by_objective in objective_seeds.items():
        baseline = by_objective["installed_mass"]
        for objective in SEED_OBJECTIVES:
            seed = by_objective[objective]
            if not seed.feasible:
                lines.append(f"| {name} | {objective} | infeasible | — | — | — |")
                continue
            distance = float(np.abs(seed.capacities - baseline.capacities).sum())
            lines.append(
                f"| {name} | {objective} | {seed.total_seed_mass_t:.1f} t | "
                f"{seed.import_stock_mass_t:.1f} t | "
                f"{seed.intervention_hours_per_year:.1f} h/yr | "
                f"{distance:.3g} |"
            )
    lines += [
        "",
        "All three objectives return the identical central design in every "
        "LP-feasible scenario. This is a negative structural result: the "
        "current variables and constraints do not expose a mass/import/"
        "intervention tradeoff for the optimizer to choose. A genuine Pareto "
        "front requires alternative process routes, sector composition, "
        "redundancy, or deployment decisions; relabeling the objective alone "
        "cannot create it.",
        "",
        "## Ensemble diagnostics (r4.0)",
        "",
        "Per-draw failure reasons, top binding constraints among feasible "
        "draws, and Spearman rank sensitivity of the named multipliers "
        "(machine-readable: `tables/diagnostics_histograms.csv`, "
        "`tables/ensemble_sensitivity.csv`):",
        "",
    ]
    for name, d in diags.items():
        fh = ", ".join(
            f"{k} {v}" for k, v in sorted(d.failure_histogram.items(), key=lambda kv: -kv[1])
        )
        bh = ", ".join(
            f"{k} {v}" for k, v in sorted(d.binding_histogram.items(), key=lambda kv: -kv[1])[:4]
        )
        lines.append(f"- **{name}**: failures — {fh or 'none'}; top binding — {bh or 'n/a'}.")
    lines += [
        "",
        "These are rank screens inside the declared independent multiplier "
        "measure, not causal effects or global sensitivity. Sector resolution "
        "changes both signs and magnitudes relative to the scalar-state run; "
        "the machine-readable table is authoritative and no previous "
        "depreciation-direction claim is carried forward.",
        "",
        "## Strict-lunar infeasibility certificate (r4.0)",
        "",
        "Elastic relaxation of the exact seed LP (every row receives a "
        "nonnegative slack; the slack sum is minimized in row-native "
        "units). This is a minimum total-violation certificate, not a "
        "strict irreducible infeasible subsystem. Machine-readable: "
        "`tables/infeasibility_certificate.csv`.",
        "",
    ]
    for name, rows in certs.items():
        if not rows:
            continue
        lines.append(
            f"**{name}** — unsatisfiable requirement rows (minimum shortfall over the horizon):"
        )
        lines.append("")
        lines.append("| constraint | minimum shortfall | units |")
        lines.append("|---|---:|---|")
        for r in rows:
            lines.append(f"| {r.constraint} | {r.minimum_violation:,.2f} | {r.units} |")
        lines.append("")
    lines += [
        "The strict-lunar cut is material, category-specific, and "
        "quantified: the configured lunar yields cannot supply the Ni, Cu, "
        "C, Co, Cr, rare-earth, Li, and H demands of the declared "
        "electronics and process-equipment stack within the horizon's "
        "throughput and energy limits. Substituting recipes, richer "
        "measured deposits, or a different electronics architecture would "
        "change this table, which is exactly what makes it a useful "
        "engineering target list.",
        "",
        "## Equation-review sensitivity outputs",
        "",
        "Additional deterministic tables keep the newly explicit Part I "
        "relations separate from the calibrated-status claims of the core model:",
        "",
        "- `tables/digital_progress_regimes.csv`: diminishing, saturating-frontier, "
        "and innovation-interrupted trajectories, with experiment, technical-validation, "
        "and internal-adoption throughput plus marginal gain reported separately.",
        "- `tables/internal_public_capability_trajectories.csv`: zero-lag, "
        "slower-publication, and internal-overhang assumption cases with separate "
        "internal/public capability and event clocks.",
        "- `tables/digital_channel_ablations.csv`, "
        "`tables/digital_elasticity_bounds.csv`, and "
        "`tables/digital_loop_bottlenecks.csv`: one-channel freezes, bounded "
        "elasticities with declared correlations, and period-specific loop limits.",
        "- `tables/digital_release_backtest.csv` and "
        "`tables/digital_release_backtest_summary.csv`: coefficients fitted "
        "only on 2020–2022 releases, out-of-time 2023 validation, and a 2024 "
        "holdout for compute-only and compute-plus-data-balance relations.",
        "- `tables/milestone_order_branches.csv`: separate AI-R&D, embodiment, "
        "Earth/space capital-closure, and control-readiness clocks across all "
        "four digital/physical speed combinations and a terrestrial-first "
        "counterfactual.",
        "- `tables/closure_loop_ablation_matrix.csv`: orthogonal verified "
        "AI-R&D-loop and reproductive-capital-loop switches for the central "
        "Moon–asteroid scenario.",
        "- `tables/intergenerational_learning_faults.csv`: repeated and hidden "
        "structural-transfer faults across controller generations with latency, "
        "retention, recurrence, recovery, verification, and regression gates.",
        "- `tables/digital_learning_feedback.csv`: campaign-derived stage-rate "
        "and verified-yield feedback compared with the unadjusted digital loop.",
        "- `tables/matched_lifecycle_cost_contributions.csv`: paired Earth/space "
        "categories with uncertainty intervals, contribution shares, difference "
        "ranks, and explicit omission labels.",
        "- `tables/data_advantage_profile.csv`: seven component values, uncertainty "
        "widths, hard gates, weights, and the assumption-class scalarization.",
        "- `tables/coordination_sensitivity.csv`: dependency topology, complexity, "
        "uncertainty, intelligence, and the irreducible coordination floor.",
        "- `tables/coordination_form_uncertainty.csv` and "
        "`tables/coordination_form_summary.csv`: common-draw power, logarithmic, "
        "and saturating edge responses with one-way schedule, capacity, "
        "reliability, and labor-cost mappings.",
        "- `tables/embodiment_compatibility_matrix.csv`: physical gate failures, "
        "hardware ceilings, intelligence thresholds, verification status, and first "
        "passage by task and hardware portfolio.",
        "- `tables/embodiment_two_direction_sweep.csv` and "
        "`tables/terrestrial_rehearsal_embodiment_faults.csv`: independent "
        "intelligence/hardware sweeps and declared degraded-hardware cases.",
        "- `tables/embodiment_bom_requirements.csv`: sensor, actuator, tooling, "
        "spares, calibration, and control-hardware additions to the material "
        "bill and replacement-service graph.",
        "- `tables/orbital_lifecycle_states.csv`: nine capacity-equivalent lifecycle "
        "stocks plus repair, recycling, retrieval, and irreversible-loss flows.",
        "- `tables/orbital_lifecycle_strategy_comparison.csv`: serviceability and "
        "circular-design portfolios with mass penalties and lifecycle outcomes.",
        "- `tables/orbital_transport_service_network.csv`: four named "
        "origin-destination routes, maturity gates, rocket-equation propellant, "
        "and one-at-a-time service-economics sensitivities.",
        "- `tables/orbital_transport_break_even_surface.csv`: a multi-axis "
        "client, failure, serviceability, fleet, recovery, reuse, route, "
        "propellant-source, and lunar-maturity break-even surface.",
        "- `tables/orbital_service_decision_comparison.csv`: nine service or "
        "disposition actions across six orbit regimes, two asset classes, and "
        "three fleet architectures with separate technical, economic, "
        "governance, and deployable gates.",
        "- `tables/orbital_regime_assumptions.csv`, "
        "`tables/orbital_fleet_amortization.csv`, and "
        "`tables/orbital_governance_constraints.csv`: orbit-specific operating "
        "conditions, fleet fixed-cost sharing, and unresolved legal/authorization "
        "dependencies.",
        "- `tables/orbital_control_policy.csv`: common-cause loss-budget checks, "
        "shell-state triggers, and deterministic mitigation actions.",
        "- `tables/orbital_cluster_layout_optimization.csv`: physical/logical "
        "failure-domain layouts with common-cause, fragment-correlation, "
        "communications, concentration, and Pareto diagnostics.",
        "- `tables/orbital_breakup_cloud_summary.csv` and "
        "`tables/orbital_breakup_cloud_trajectory.csv`: explicit-node Earth/lunar "
        "breakup propagation, losses, maneuvers, interruption, repair, and "
        "restoration.",
        "- `tables/orbital_degraded_control_stress.csv`: tracking, communications, "
        "navigation, and centralized-coordination failures with fallback checks.",
        "- `tables/orbital_mitigation_portfolio_pareto.csv`: 256 portfolios over "
        "eight controls with risk, cost, delivered capacity, and non-dominance.",
        "- `tables/orbital_environment_strategy_comparison.csv` and "
        "`tables/orbital_multi_operator_capacity.csv`: distinct Earth/lunar "
        "operating regimes and shared-shell governance/carrying-capacity gates.",
        "- `tables/partial_closure_metrics.csv`: strict autonomy, mass closure, "
        "external-support intensity, import leverage, and critical residual inputs.",
        "- `tables/partial_closure_support_policies.csv` and "
        "`tables/partial_closure_dashboard.csv`: fixed, proportional, stockpile, "
        "and disrupted import policies with continuous closure and runway metrics.",
        "- `tables/partial_closure_substitution_programs.csv`: discrete dependency "
        "program gates, outcomes, and resource-accounted expansion opportunity cost.",
        "- `tables/partial_closure_supplier_boundary.csv`: resource-specific "
        "external factory, material, labor, energy, finance, transport, reliability, "
        "growth, and utilization constraints.",
        "- `tables/partial_closure_allocation_policies.csv`: immediate expansion, "
        "replacement reserve, balanced, and substitution-first allocation outcomes.",
        "",
        "All coefficients in these tables are `ASSUMPTION`-class scenario inputs "
        "unless a row says otherwise. The tables expose comparative behavior and "
        "falsification targets; they are not empirical forecasts.",
        "",
        "## Reproducibility",
        "",
        "```bash",
        "uv run --locked rsi-run-integrated",
        "pytest tests/test_extensions.py tests/test_integrated.py "
        "tests/test_integrated_analysis.py -q",
        "```",
        "",
        "Every generated table is derived from the same in-memory run. "
        "`outputs/integrated/MANIFEST.md` hashes the parameter file, implementation, "
        "runner, report, tables, and figures.",
    ]
    path = workspace.output_directory / "report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
