# Current integrated-bootstrap model

- model version: `integrated-model-1`
- assumption ensemble: n=200 per scenario, seed=404
- epistemic status: scenario implications, not measurements or forecasts

## Headline results

| scenario | central installed seed mass | Earth strategic-material import stock | aggregate operating-capacity doubling (80y extension) | cell-equivalents at year 40 | design-space occupancy | ensemble seed p10/p50/p90 |
|---|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | 206.9 t | 48.1 t | — | 0.47 | 81/200 | 171/201/228 t |
| lunar_strategic_material_bridge | 217.0 t | 58.2 t | — | 0.54 | 126/200 | 181/212/248 t |
| lunar_strict | infeasible | — | — | — | 0/200 | — |
| moon_asteroid_network | 187.9 t | 0.0 t | 35.2 yr | 3.28 | 187/200 | 156/207/322 t |

The ensemble counts are occupancy under the declared log-uniform sampling measure. They are neither calibrated probabilities nor empirical success rates.

The strict lunar-only case is a structural infeasibility inside the declared architecture: trace lunar yields cannot supply the configured electronics and process-equipment stack, in the central case and in every ensemble draw. It is not a proof that lunar-only closure is physically impossible; substitution, different recipes, new processes, or measured richer deposits could change the constraint graph.

The Moon–asteroid case is likewise conditional. Its `diverse_asteroid_portfolio` is a deliberately composite source with ASSUMPTION-class recoverable yields. The model says what those yields would imply; it does not establish that a specific accessible portfolio has them.

The aggregate material model is now paired with a process-closure acceptance contract covering typed source, species, process, part, parent-tool, transport, and waste nodes; grade progression; critical part ancestry; source/fleet evidence; and eight binary gates. Every gap-register row remains `evidence_pending`; no process-feasible closure is claimed. See `docs/PROCESS_CLOSURE_ACCEPTANCE_CONTRACT.md` and `tables/process_closure_gap_register.csv`.

## What changed from the inherited model

- 18 sectors, including seven separate electronics tiers.
- 17 element/material categories with explicit bills of material.
- Earth→Moon strategic-material import stock, asteroid→Moon feed, and Moon→orbit finished-compute arcs.
- Task coverage, intervention demand, lunar-gravity process compatibility, and centrifuge mass/power overhead.
- Construction lag, commissioning ramp, minimum viable scale, and an explicit aggregate operating-capacity doubling threshold.
- All 18 sector capacities remain stateful through commissioning, cohort-resolved ramp, and depreciation; aggregate cell-equivalents are the slowest normalized operating sector, not the state.
- A diagnostic allocator can build sectors independently, and the repair diagnostic consumes parts, repair service, intervention capacity, and queue time before returning failures to operation.
- Delivered, staged, installed, commissioned, failed-startup, recovered, and operating seed states are explicit; delivered mass includes logistics hardware, packaging, spares, calibration, and startup-energy storage.
- Coupled local compute, verified intelligence improvement, autonomy, and productivity.
- Rate-limited Earth and Earth-fed orbital counterfactuals.
- Active, derelict, and fragment stocks with a five-year fragment creation-to-clearance ratio.

## Central process and seed diagnostics

### terrestrial_rehearsal

- status: lexicographic installed_mass optimum within the declared linear seed architecture
- minimum task coverage: 0.720
- residual intervention: 193.2 h/year
- lunar feed: 540.0 t/year
- asteroid feed: 0.0 t/year
- tight constraints: `element:Ni` (-1.78e-15), `element:Cu` (-1.78e-15), `element:Cr` (-4.44e-16), `element:rare_earths` (-2.22e-16), `element:N` (-1.39e-17)

### lunar_strategic_material_bridge

- status: lexicographic installed_mass optimum within the declared linear seed architecture
- minimum task coverage: 0.807
- residual intervention: 130.5 h/year
- lunar feed: 540.0 t/year
- asteroid feed: 0.0 t/year
- tight constraints: `element:Ni` (-5.33e-15), `element:C` (-3.55e-15), `element:Cu` (-3.55e-15), `element:Cr` (-8.88e-16), `element:Li` (-3.33e-16)

### lunar_strict

- status: The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)
- minimum task coverage: 0.894

### moon_asteroid_network

- status: lexicographic installed_mass optimum within the declared linear seed architecture
- minimum task coverage: 0.952
- residual intervention: 31.0 h/year
- lunar feed: 360.3 t/year
- asteroid feed: 179.7 t/year
- tight constraints: `throughput:asteroid_mining` (-2.84e-14), `element:dopants` (-1.39e-17), `throughput:asteroid_transport` (+0.00e+00), `throughput:refining` (+0.00e+00), `autonomy:intervention_budget` (+9.74e-01)

## Delivered-to-operating seed stage (r4.0)

The LP mass is an installed-seed quantity. The deployment diagnostic adds transport packaging, unloading and site equipment, calibration references, initial spares, and startup-energy storage, then moves the core seed through distinct states. Eight percent of newly commissioned core mass enters a declared startup-failure queue and must consume spares before it can operate. All deployment coefficients are explicit `ASSUMPTION`s with a bounding argument; they are not a mission estimate. Machine-readable: `tables/seed_deployment_trajectory.csv`.

| scenario | installed seed | delivered seed | logistics increment | startup energy | first operation | full operating seed | recovered startup failures |
|---|---:|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | 206.9 t | 290.5 t | 83.6 t | 103.5 MWh | 1.5 yr | 5.5 yr | 16.6 t |
| lunar_strategic_material_bridge | 217.0 t | 303.6 t | 86.6 t | 108.5 MWh | 1.5 yr | 5.8 yr | 17.4 t |
| moon_asteroid_network | 187.9 t | 265.8 t | 77.9 t | 94.0 MWh | 1.5 yr | 5.2 yr | 15.0 t |

## Compute regimes at year 40

| regime | normalized capacity |
|---|---:|
| off-world endogenous total | 5.11 |
| Moon→orbit endogenous export | 0.66 |
| Earth-fed orbit, tight | 1.56 |
| Earth-fed orbit, base | 2.81 |
| Earth-fed orbit, responsive | 4.99 |

The endogenous curve compounds only after the seed survives commissioning and source constraints. Earth-fed orbital capacity remains an affine deployment process and approaches a depreciation-limited stock at constant delivery. The terrestrial curves are rate-and-site-ceiling scenarios, not forecasts of actual buildout.

## Debris condition

| case | creation-to-clearance ratio, last 5 yr | clearance >= creation | fragment index, year 40 |
|---|---:|:---:|---:|
| Earth-fed orbit / weak mitigation | 0.61 | yes | 1.602 |
| Earth-fed orbit / strong mitigation | 0.35 | yes | 0.284 |
| dense endogenous / weak mitigation | 4.40 | no | 3.179 |
| dense endogenous / strong mitigation | 3.97 | no | 1.687 |
| distributed endogenous / sparse topology | 1.00 | yes | 0.000 |

A dense shell is not licensed by industrial closure alone. In this scenario record, rapid endogenous deployment creates several times the fragments it clears under both weak and strong shell mitigation (the ratio is a flow ratio, not a branching-process reproduction number). The sparse/distributed topology sits at the boundary ratio only because its collision kernel is explicitly lower; that multiplier is an assumption to be replaced by shell- and trajectory-specific data.

### Finite-mass, shell-resolved diagnostic

A second diagnostic resolves 400-km LEO, 650-km LEO, and cislunar regions; active assets, intact derelicts, trackable fragments, and untrackable fragments; density/volume kernels; avoidance saturation; cross-shell fragment transport; disposal, natural clearance, retrieval, and active removal. Requested deployment consumes a finite feed inventory supplied by time-limited Earth import, depletion of a finite capture reservoir, and recovered retirements. Collision losses reduce returned active capacity and enter replacement/import cost.

| shell | active capacity, year 40 | intact derelicts | trackable | untrackable | expected hazardous-descendant ratio |
|---|---:|---:|---:|---:|---:|
| leo_400 | 0.162 | 0.010 | 0.000 | 0.005 | 0.000 |
| leo_650 | 0.415 | 0.025 | 0.000 | 0.203 | 0.022 |
| cislunar | 0.065 | 0.004 | 0.000 | 0.032 | 0.000 |

At year 40 the finite reservoir retains 220.0 t and feed inventory retains 543.3 t; cumulative requested-deployment shortfall is 0.00 normalized units. Replacement/import cost under the declared delivered-mass price is $326.5M. The descendant ratio is a branching-style stress metric rather than the legacy creation/clearance flow ratio. Machine-readable: `tables/orbital_mass_balance.csv` and `tables/shell_debris_trajectory.csv`.

## Governance threat/control traceability (r4.0)

The governance model names actors, assets, trust boundaries, normal/delayed/lost-link authority, threat paths, and controls with verification, rollback, and residual risk. Controls map to live build rate, sector floors, repair queues, source flows, commissioning cohorts, debris state, and independent inventory measurements. Every control remains `requirement_unvalidated`; this is not a solved safety case. See `docs/GOVERNANCE_THREAT_MODEL.md` and `tables/governance_threat_control_traceability.csv`.

The linked Stage-0 protocol converts those controls into ten binary acceptance gates, a typed raw-event contract, a fault campaign that covers every registered threat plus communication loss, and explicit model-parameter replacement rules. Every checklist row is still `execution_pending` or `data_pending`: the protocol is executable, but no physical rehearsal result is claimed. See `docs/TERRESTRIAL_REHEARSAL_PROTOCOL.md` and `tables/rehearsal_acceptance_matrix.csv`.

## Terminal-window operating-capacity endpoints (r4.0)

Aggregate operating-capacity doubling is a threshold crossing of the slowest normalized sector; these endpoints separately report retention and final-five-year direction. The central 80-year extension is in `tables/long_horizon_endpoints.csv`; the complete sector trajectory is in `tables/sector_capacity_trajectory.csv`.

| scenario | aggregate doubling | at year 40 | retained >= 2 | net final-5y | ensemble retained | ensemble terminal-window expanding |
|---|---:|---:|:---:|---:|---:|---:|
| terrestrial_rehearsal | — | 0.47 | no | -0.022 | 0/81 | 0/81 |
| lunar_strategic_material_bridge | — | 0.54 | no | -0.027 | 0/126 | 0/126 |
| lunar_strict | — | — | — | — | 0/200 | 0/200 |
| moon_asteroid_network | 35.2 yr | 3.28 | yes | +1.323 | 139/187 | 187/187 |

Reading: the terrestrial rehearsal and lunar strategic-material bridge never reach aggregate doubling in the 80-year extension and are contracting at year 40. The Moon–asteroid network is terminal-window expanding, reaches 3.28 equivalents at year 40, and first crosses two at year 35.25. Import-pool exhaustion years are per-category first dips of the pooled inventory (initial Earth stock plus recycled returns and local production) and are reported in `tables/import_stock_composition.csv`; pools can refill later from local production, so a first dip is not permanent depletion.

## Intelligence-coupling ablations (r4.0)

Zero/freeze ablations of the declared coupling coefficients; the seed LP does not read the intelligence block, so dynamics variants share the central seed. Machine-readable: `tables/ablations.csv`.

| scenario | variant | aggregate doubling | at year 40 | growth share of baseline |
|---|---|---:|---:|---:|
| terrestrial_rehearsal | baseline | — | 0.47 | 100% |
| terrestrial_rehearsal | research_automation_frozen | — | 0.47 | 100% |
| terrestrial_rehearsal | task_autonomy_improvement_frozen | — | 0.47 | 100% |
| terrestrial_rehearsal | industrial_productivity_improvement_frozen | — | 0.47 | 100% |
| terrestrial_rehearsal | both_couplings_frozen | — | 0.47 | 100% |
| terrestrial_rehearsal | capital_reproduction_frozen | — | 0.00 | 188% |
| terrestrial_rehearsal | seed_sized_at_base_autonomy | — | 0.47 | 100% |
| lunar_strategic_material_bridge | baseline | — | 0.54 | 100% |
| lunar_strategic_material_bridge | research_automation_frozen | — | 0.54 | 100% |
| lunar_strategic_material_bridge | task_autonomy_improvement_frozen | — | 0.54 | 100% |
| lunar_strategic_material_bridge | industrial_productivity_improvement_frozen | — | 0.54 | 100% |
| lunar_strategic_material_bridge | both_couplings_frozen | — | 0.54 | 100% |
| lunar_strategic_material_bridge | capital_reproduction_frozen | — | 0.00 | 215% |
| lunar_strategic_material_bridge | seed_sized_at_base_autonomy | — | infeasible | — |
| moon_asteroid_network | baseline | 35.25 yr | 3.28 | 100% |
| moon_asteroid_network | research_automation_frozen | 36.75 yr | 2.71 | 75% |
| moon_asteroid_network | task_autonomy_improvement_frozen | 36.00 yr | 3.01 | 88% |
| moon_asteroid_network | industrial_productivity_improvement_frozen | 36.00 yr | 2.95 | 85% |
| moon_asteroid_network | both_couplings_frozen | 36.75 yr | 2.71 | 75% |
| moon_asteroid_network | capital_reproduction_frozen | — | 0.00 | -44% |
| moon_asteroid_network | seed_sized_at_base_autonomy | — | infeasible | — |

Finding: sector resolution separates regimes that a scalar aggregate conflates (terrestrial_rehearsal: 145/160; lunar_strategic_material_bridge: 145/160; moon_asteroid_network: 48/160 steps material-limited). The terrestrial and lunar-bridge trajectories remain overwhelmingly material-limited, so coupling ablations move their year-40 endpoints by less than a tenth of one percent. In the Moon–asteroid network, however, the fully uncoupled run reaches 2.71 sector-balanced equivalents versus 3.28 at baseline, retaining about 75% of baseline net growth. The dynamic coupling is therefore operative only after the diverse source vector relaxes the material bottleneck. The declared starting AI level also remains load-bearing statically: sizing at base autonomy makes the bridge and network seeds infeasible.

The orthogonal 2×2 screen in `tables/closure_loop_ablation_matrix.csv` separates the verified AI-R&D proxy from reproductive capital. The bounded-controller, capital-reproducing cell reaches balanced doubling at 36.75 years; the active AI-R&D proxy without capital reproduction never doubles. Endogenous physical compounding therefore does not logically require open-ended digital improvement, while digital improvement alone does not create self-replicating capital.

The exhaustive primary-constraint classification is terrestrial_rehearsal: material 145, service 0, order-cap 15; lunar_strategic_material_bridge: material 145, service 0, order-cap 15; moon_asteroid_network: material 48, service 0, order-cap 112 (160 quarterly steps each). Machine-readable: `tables/dynamic_regime_summary.csv`.

## Knowledge and observable autonomy gates (r4.0)

The 5 t knowledge package is now decomposed into storage/compute, software/toolchains, calibration references, laboratory equipment, consumables/recipes, and test articles. Each sector reports named-task completion, intervention demand, fault diagnosis, verification throughput, engineering-cycle time, process yield, repair success, mean time to recovery, and a non-divisible stop-line pass. These are ASSUMPTION-class diagnostic mappings pending Stage-0 measurements, not evidence that the capabilities exist. Machine-readable: `tables/knowledge_autonomy_observables.csv`.

Two-year zero-capacity windows isolate the autonomy, verification, and compute regimes; a 90% advanced-logic/memory loss at year 5 isolates repair. The zero-capacity windows are adversarial boundary tests, not frequency estimates.

| scenario | variant | at year 40 | doubling | material | autonomy | verification | repair | compute | service | order-cap |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | declared | 0.47 | — | 145 | 0 | 0 | 0 | 0 | 0 | 15 |
| terrestrial_rehearsal | communication_outage_years10_12 | 0.47 | — | 136 | 8 | 0 | 0 | 0 | 0 | 16 |
| terrestrial_rehearsal | verification_outage_years10_12 | 0.47 | — | 136 | 0 | 8 | 0 | 0 | 0 | 16 |
| terrestrial_rehearsal | compute_outage_years10_12 | 0.47 | — | 136 | 0 | 0 | 0 | 8 | 0 | 16 |
| terrestrial_rehearsal | repair_after_advanced_logic_90pct_loss_year5 | 1.70 | 14.2 yr | 139 | 0 | 0 | 3 | 0 | 0 | 18 |
| lunar_strategic_material_bridge | declared | 0.54 | — | 145 | 0 | 0 | 0 | 0 | 0 | 15 |
| lunar_strategic_material_bridge | communication_outage_years10_12 | 0.54 | — | 136 | 8 | 0 | 0 | 0 | 0 | 16 |
| lunar_strategic_material_bridge | verification_outage_years10_12 | 0.54 | — | 136 | 0 | 8 | 0 | 0 | 0 | 16 |
| lunar_strategic_material_bridge | compute_outage_years10_12 | 0.54 | — | 136 | 0 | 0 | 0 | 8 | 0 | 16 |
| lunar_strategic_material_bridge | repair_after_advanced_logic_90pct_loss_year5 | 2.17 | 18.5 yr | 148 | 0 | 0 | 3 | 0 | 0 | 9 |
| moon_asteroid_network | declared | 3.28 | 35.2 yr | 48 | 0 | 0 | 0 | 0 | 0 | 112 |
| moon_asteroid_network | communication_outage_years10_12 | 2.84 | 36.8 yr | 40 | 8 | 0 | 0 | 0 | 0 | 112 |
| moon_asteroid_network | verification_outage_years10_12 | 2.84 | 36.8 yr | 40 | 0 | 8 | 0 | 0 | 0 | 112 |
| moon_asteroid_network | compute_outage_years10_12 | 2.84 | 36.8 yr | 40 | 0 | 0 | 0 | 8 | 0 | 112 |
| moon_asteroid_network | repair_after_advanced_logic_90pct_loss_year5 | 4.33 | 28.2 yr | 106 | 0 | 0 | 54 | 0 | 0 | 0 |

The declared central cases remain material/order-cap limited. The adversarial windows create the named regimes mechanically and reduce the Moon–asteroid endpoint; this demonstrates classification and falsification plumbing, not calibrated outage risk. Machine-readable: `tables/knowledge_regime_summary.csv`.

## Operating-environment/process coupling (r4.0)

The central release remains on the identity `centrifuge_only` profile for continuity. Separate nominal and adverse lunar profiles apply process-specific throughput, quality-yield, power-demand, and depreciation multipliers for dust, traction, reduced convection, vacuum behavior, radiation, thermal cycling, contamination, and calibration drift. Every multiplier is an explicit bounding `ASSUMPTION`; Earth rehearsal results do not transfer to these profiles automatically.

| scenario | environment | feasible | seed mass | top binding row | at year 40 | doubling | survived |
|---|---|:---:|---:|---|---:|---:|:---:|
| terrestrial_rehearsal | centrifuge_only | yes | 206.9 t | element:Ni | 0.47 | — | no |
| terrestrial_rehearsal | lunar_nominal | yes | 210.6 t | element:Cu | 0.51 | — | yes |
| terrestrial_rehearsal | lunar_adverse | no | — t | — | — | — | — |
| lunar_strategic_material_bridge | centrifuge_only | yes | 217.0 t | element:Ni | 0.54 | — | no |
| lunar_strategic_material_bridge | lunar_nominal | yes | 223.2 t | element:Ni | 0.59 | — | no |
| lunar_strategic_material_bridge | lunar_adverse | no | — t | — | — | — | — |
| lunar_strict | centrifuge_only | no | — t | — | — | — | — |
| lunar_strict | lunar_nominal | no | — t | — | — | — | — |
| lunar_strict | lunar_adverse | no | — t | — | — | — | — |
| moon_asteroid_network | centrifuge_only | yes | 187.9 t | throughput:asteroid_mining | 3.28 | 35.2 yr | yes |
| moon_asteroid_network | lunar_nominal | yes | 195.4 t | element:dopants | 3.43 | 35.0 yr | yes |
| moon_asteroid_network | lunar_adverse | yes | 209.8 t | throughput:refining | 3.61 | 34.5 yr | yes |

The nominal/adverse penalties change seed mass and binding rows; the adverse lunar bridge becomes LP-infeasible. Some feasible penalized profiles can improve the year-40 trajectory because the minimum-mass LP responds by installing more initial capacity. That is an objective frontier artifact, not evidence that a harsher environment helps. Machine-readable: `tables/environment_process_effects.csv`.

## Policy and structural-uncertainty robustness (r4.0)

A one-factor-at-a-time sweep varies advanced-logic knockout fraction, event time, horizon, retained initial import stock, initial surplus, and obsolescence/depreciation. It compares balanced, live maximin, 20%-reserve surplus-preserving, generic shock-aware, and exact perfect-foresight policies. Counts below are design-case occupancy over the enumerated deterministic cases, not probabilities.

| scenario | policy | cases | survived | survived + terminally expanding |
|---|---|---:|---:|---:|
| lunar_strategic_material_bridge | balanced | 19 | 15 | 0 |
| lunar_strategic_material_bridge | maximin_sector | 19 | 18 | 9 |
| lunar_strategic_material_bridge | surplus_preserving | 19 | 18 | 11 |
| lunar_strategic_material_bridge | shock_aware | 19 | 18 | 6 |
| lunar_strategic_material_bridge | perfect_foresight | 19 | 19 | 12 |
| moon_asteroid_network | balanced | 19 | 7 | 7 |
| moon_asteroid_network | maximin_sector | 19 | 18 | 17 |
| moon_asteroid_network | surplus_preserving | 19 | 18 | 17 |
| moon_asteroid_network | shock_aware | 19 | 18 | 18 |
| moon_asteroid_network | perfect_foresight | 19 | 19 | 10 |

The machine-readable sweep reports minimum live sector margin and first aggregate doubling for every case, making failure boundaries inspectable rather than reducing them to one rank correlation. `tables/policy_robustness_sweep.csv` is authoritative.

## Tiered electronics closure and inventory life (r4.0)

The integrated layer no longer uses the inherited scalar electronics productivity range in its headline analysis. Seven tiers now carry separate local-producibility, replacement, shelf-life, obsolescence, and substitution assumptions. Imported tier inventory decays before use, and the architecture comparison includes frontier-local, permanent-import, mature/repairable, and cannibalization-based cases.

| scenario | architecture | viable tiers | total tier shortfall | gross permanent-import mass | first shortfall |
|---|---|---:|---:|---:|---:|
| lunar_strategic_material_bridge | frontier_local | 5/7 | 0.478 | 0.0 t | 2.2 yr |
| lunar_strategic_material_bridge | permanent_import | 7/7 | 0.000 | 110.8 t | — |
| lunar_strategic_material_bridge | mature_repairable | 6/7 | 0.002 | 11.1 t | 11.0 yr |
| lunar_strategic_material_bridge | cannibalization_based | 5/7 | 0.028 | 0.0 t | 7.8 yr |
| moon_asteroid_network | frontier_local | 5/7 | 1.222 | 0.0 t | 2.2 yr |
| moon_asteroid_network | permanent_import | 5/7 | 0.199 | 110.8 t | 33.0 yr |
| moon_asteroid_network | mature_repairable | 5/7 | 0.117 | 11.1 t | 25.5 yr |
| moon_asteroid_network | cannibalization_based | 5/7 | 0.377 | 0.0 t | 16.5 yr |

Every tested architecture still develops a shortfall in advanced logic/memory or process-equipment/metrology under the expanding Moon–asteroid demand path; fixed imports proportional to the initial seed do not scale with endogenous demand. The most decision-reducing measurements are therefore demonstrated mature-node wafer yield and parent-tool/calibration replacement demand, followed by useful life and permanent-import mass per service-year. The strict-lunar minimum cut remains tiered in the seed LP and is not erased by these dynamic inventory cases. Machine-readable: `tables/electronics_architecture_comparison.csv`.

The empirical-calibration contract separates the Earth reference, serviceable space platform, and integrated disposable cases; requires equal-workload records; binds six evidence packages to current model parameters; preserves correlated reliability, link, thermal, Earth-resource, demand, and financing uncertainty; and defines an audited cash-flow event ledger with chronological holdout validation. All readiness rows remain `data_pending`. See `docs/ECONOMIC_CALIBRATION_PROTOCOL.md` and `tables/economic_calibration_readiness.csv`.

The publication contract names target and fallback venues for all three papers and measures each draft against current publisher requirements. Machine-checkable structure now passes where supplied, while references, fallback word-count expansion, live-portal fields, and every author-controlled declaration remain explicitly pending. See `docs/VENUE_SELECTION_AND_CONFORMANCE.md` and `tables/publication_readiness.csv`.

## Symmetric dynamic economics (r4.0)

Earth and space now use the same reinvestment/debt logic: endogenous investment, learning, depreciation/obsolescence, regulatory build queues, debt-to-revenue limits, interest, bridge financing, market demand, and expanding resource ceilings. Space is additionally capped by the physical model and pays for its funded share of industrial orders, source transfer, and intervention. The coefficients are ASSUMPTION-class scenario mechanics, not a valuation.

| market | technical space at year 40 | funded space | Earth | space finance-limited steps | Earth finance-limited steps | space self-financing | Earth self-financing |
|---|---:|---:|---:|---:|---:|---:|---:|
| commodity_compute | 5.11 | 0.60 | 68.97 | 34 | 0 | — | — |
| space_native_services | 5.11 | 3.21 | 25.86 | 0 | 0 | — | 27.2 yr |

Physical compounding does not automatically fund deployment. In the commodity case, finance activates only a small fraction of technically available space capacity while Earth expands endogenously. A space-native price premium funds more of the physical path, but the space case still does not repay its declared external capital inside 40 years. P3b therefore remains a conditional economic proposition, not a consequence of the physical growth curve. Machine-readable: `tables/symmetric_dynamic_economics.csv`.

## Composition-changing robust-seed Pareto search (r4.0)

The design search now changes process route, sector redundancy, and lunar/asteroid source allocation instead of merely relabeling one LP objective or scaling a fixed vector. It minimizes delivered mass, Earth import, intervention, and doubling time while maximizing year-40 capacity and capacity after a five-year asteroid-source outage. Dominance is computed across all six objectives.

| route | redundancy | source portfolio | delivered mass | doubling | year 40 | after outage | Pareto | robust |
|---|---|---|---:|---:|---:|---:|:---:|:---:|
| baseline | minimum | baseline | 265.8 t | 26.5 yr | 8.12 | 5.49 | yes | yes |
| baseline | minimum | asteroid_reserve | 307.5 t | 23.5 yr | 10.67 | 6.41 | yes | yes |
| mature_node | minimum | baseline | 261.3 t | 23.5 yr | 7.14 | 5.28 | yes | yes |
| mature_node | minimum | asteroid_reserve | 301.6 t | 23.5 yr | 8.97 | 6.44 | yes | yes |
| modular_tools | minimum | asteroid_reserve | 307.2 t | 24.0 yr | 10.83 | 5.11 | yes | yes |

The minimum delivered-mass robust candidate in this enumerated design space is `mature_node` / `minimum` / `baseline` at 261.3 t. This is an ASSUMPTION-conditioned discrete frontier, not a globally optimal mission design. Machine-readable dominated and non-dominated points: `tables/robust_seed_pareto.csv`.

## Allocation, repair, and shock-policy comparison (r4.0)

The published central case retains balanced build packets for continuity. The structural diagnostic below instead maximizes the weakest live sector margin, then minimizes installed mass at that margin. Repair uses the declared ASSUMPTION-class parts, service, intervention, and lag coefficients. The shock removes 50% of the advanced-logic/memory sector at year 20; it is a deterministic stress case, not a frequency estimate. Machine-readable: `tables/allocation_repair_comparison.csv`.

| scenario | policy | repair | shock | doubling | at year 40 | minimum sector margin | survived | shock recovery |
|---|---|:---:|---|---:|---:|---:|:---:|---:|
| terrestrial_rehearsal | balanced | no | none | — | 0.47 | 0.47 | no | — |
| terrestrial_rehearsal | maximin_sector | no | none | — | 1.10 | 1.10 | yes | — |
| terrestrial_rehearsal | maximin_sector | yes | none | 19.5 yr | 1.75 | 1.75 | yes | — |
| terrestrial_rehearsal | maximin_sector | yes | advanced_logic_memory:50%@year20 | 19.5 yr | 1.78 | 1.78 | yes | 26.0 yr |
| lunar_strategic_material_bridge | balanced | no | none | — | 0.54 | 0.54 | no | — |
| lunar_strategic_material_bridge | maximin_sector | no | none | 31.0 yr | 1.11 | 1.11 | yes | — |
| lunar_strategic_material_bridge | maximin_sector | yes | none | 16.5 yr | 2.14 | 2.14 | yes | — |
| lunar_strategic_material_bridge | maximin_sector | yes | advanced_logic_memory:50%@year20 | 16.5 yr | 2.12 | 2.12 | yes | 25.2 yr |
| moon_asteroid_network | balanced | no | none | 35.2 yr | 3.28 | 3.28 | yes | — |
| moon_asteroid_network | maximin_sector | no | none | 32.0 yr | 3.36 | 3.36 | yes | — |
| moon_asteroid_network | maximin_sector | yes | none | 28.0 yr | 3.95 | 3.95 | yes | — |
| moon_asteroid_network | maximin_sector | yes | advanced_logic_memory:50%@year20 | 28.2 yr | 4.48 | 4.48 | yes | 23.8 yr |

These policy outcomes are not new feasibility claims: the allocator and repair coefficients expose how strongly the result depends on construction policy and recoverability. They replace the earlier implicit claim that only balanced copies can be ordered.

## Installed-mass versus aggregate-doubling frontier (r4.0)

A factor-f seed installs f cell-equivalents of the minimum-mass design (capacities, feeds, strategic import stock scale with f; the digital package is shared). Time is first passage to one *additional* operating cell-equivalent, so f = 1 coincides with the canonical metric. The oversize factor is a sweep axis, not a new assumption. Machine-readable: `tables/oversize_frontier.csv`; figure: `figures/oversize_frontier.png`.

| scenario | factor | installed mass | time to +1 cell | additional cells at year 40 |
|---|---:|---:|---:|---:|
| terrestrial_rehearsal | ×1 | 206.9 t | — | -0.53 |
| terrestrial_rehearsal | ×1.25 | 257.4 t | — | -0.66 |
| terrestrial_rehearsal | ×1.5 | 307.9 t | — | -0.80 |
| terrestrial_rehearsal | ×2 | 408.9 t | — | -1.06 |
| lunar_strategic_material_bridge | ×1 | 217.0 t | — | -0.46 |
| lunar_strategic_material_bridge | ×1.25 | 270.0 t | — | -0.58 |
| lunar_strategic_material_bridge | ×1.5 | 323.0 t | — | -0.70 |
| lunar_strategic_material_bridge | ×2 | 429.0 t | — | -0.93 |
| moon_asteroid_network | ×1 | 187.9 t | 35.25 yr | +2.28 |
| moon_asteroid_network | ×1.25 | 233.7 t | 34.25 yr | +2.85 |
| moon_asteroid_network | ×1.5 | 279.4 t | 33.50 yr | +3.42 |
| moon_asteroid_network | ×2 | 370.9 t | 32.50 yr | +4.56 |

The sector-resolved frontier reverses the earlier scalar-state reading. Neither the terrestrial nor lunar bridge design reaches one additional balanced cell-equivalent at any tested scale by year 40. The Moon–asteroid minimum-mass design also misses that threshold, while 1.25x, 1.5x, and 2x scaled designs reach it at 39.25, 38.5, and 37.25 years. Scaling one fixed composition is still not a multi-objective redesign.

## Alternative seed objectives (r4.0)

The same seed LP was solved lexicographically for minimum installed mass, minimum Earth-import mass, and minimum annual intervention, with installed mass as the secondary tie-break for the latter two. Machine-readable: `tables/seed_objective_comparison.csv`.

| scenario | objective | installed mass | import mass | intervention | capacity-vector distance from mass optimum |
|---|---|---:|---:|---:|---:|
| terrestrial_rehearsal | installed_mass | 206.9 t | 48.1 t | 193.2 h/yr | 0 |
| terrestrial_rehearsal | earth_import_mass | 206.9 t | 48.1 t | 193.2 h/yr | 0 |
| terrestrial_rehearsal | intervention_hours | 206.9 t | 48.1 t | 193.2 h/yr | 0 |
| lunar_strategic_material_bridge | installed_mass | 217.0 t | 58.2 t | 130.5 h/yr | 0 |
| lunar_strategic_material_bridge | earth_import_mass | 217.0 t | 58.2 t | 130.5 h/yr | 0 |
| lunar_strategic_material_bridge | intervention_hours | 217.0 t | 58.2 t | 130.5 h/yr | 0 |
| lunar_strict | installed_mass | infeasible | — | — | — |
| lunar_strict | earth_import_mass | infeasible | — | — | — |
| lunar_strict | intervention_hours | infeasible | — | — | — |
| moon_asteroid_network | installed_mass | 187.9 t | 0.0 t | 31.0 h/yr | 0 |
| moon_asteroid_network | earth_import_mass | 187.9 t | 0.0 t | 31.0 h/yr | 0 |
| moon_asteroid_network | intervention_hours | 187.9 t | 0.0 t | 31.0 h/yr | 0 |

All three objectives return the identical central design in every LP-feasible scenario. This is a negative structural result: the current variables and constraints do not expose a mass/import/intervention tradeoff for the optimizer to choose. A genuine Pareto front requires alternative process routes, sector composition, redundancy, or deployment decisions; relabeling the objective alone cannot create it.

## Ensemble diagnostics (r4.0)

Per-draw failure reasons, top binding constraints among feasible draws, and Spearman rank sensitivity of the named multipliers (machine-readable: `tables/diagnostics_histograms.csv`, `tables/ensemble_sensitivity.csv`):

- **terrestrial_rehearsal**: failures — autonomy_threshold 77, lp_infeasible 42; top binding — element:C 21, element:Cu 15, element:Cr 14, element:Fe 11.
- **lunar_strategic_material_bridge**: failures — autonomy_threshold 54, lp_infeasible 20; top binding — element:Ni 42, element:C 34, element:Cu 21, element:Cr 15.
- **lunar_strict**: failures — lp_infeasible 167, autonomy_threshold 33; top binding — n/a.
- **moon_asteroid_network**: failures — autonomy_threshold 13; top binding — throughput:refining 81, element:dopants 43, throughput:asteroid_mining 28, throughput:asteroid_transport 24.

These are rank screens inside the declared independent multiplier measure, not causal effects or global sensitivity. Sector resolution changes both signs and magnitudes relative to the scalar-state run; the machine-readable table is authoritative and no previous depreciation-direction claim is carried forward.

## Strict-lunar infeasibility certificate (r4.0)

Elastic relaxation of the exact seed LP (every row receives a nonnegative slack; the slack sum is minimized in row-native units). This is a minimum total-violation certificate, not a strict irreducible infeasible subsystem. Machine-readable: `tables/infeasibility_certificate.csv`.

**lunar_strict** — unsatisfiable requirement rows (minimum shortfall over the horizon):

| constraint | minimum shortfall | units |
|---|---:|---|
| element:Ni | 19.07 | tonnes over the horizon |
| element:Cu | 18.50 | tonnes over the horizon |
| element:C | 15.36 | tonnes over the horizon |
| element:Co | 3.63 | tonnes over the horizon |
| element:Cr | 3.12 | tonnes over the horizon |
| element:rare_earths | 2.29 | tonnes over the horizon |
| element:Li | 2.25 | tonnes over the horizon |
| element:H | 0.23 | tonnes over the horizon |
| element:dopants | 0.12 | tonnes over the horizon |

The strict-lunar cut is material, category-specific, and quantified: the configured lunar yields cannot supply the Ni, Cu, C, Co, Cr, rare-earth, Li, and H demands of the declared electronics and process-equipment stack within the horizon's throughput and energy limits. Substituting recipes, richer measured deposits, or a different electronics architecture would change this table, which is exactly what makes it a useful engineering target list.

## Equation-review sensitivity outputs

Additional deterministic tables keep the newly explicit Part I relations separate from the calibrated-status claims of the core model:

- `tables/digital_progress_regimes.csv`: diminishing, saturating-frontier, and innovation-interrupted trajectories, with experiment, technical-validation, and internal-adoption throughput plus marginal gain reported separately.
- `tables/internal_public_capability_trajectories.csv`: zero-lag, slower-publication, and internal-overhang assumption cases with separate internal/public capability and event clocks.
- `tables/digital_channel_ablations.csv`, `tables/digital_elasticity_bounds.csv`, and `tables/digital_loop_bottlenecks.csv`: one-channel freezes, bounded elasticities with declared correlations, and period-specific loop limits.
- `tables/digital_release_backtest.csv` and `tables/digital_release_backtest_summary.csv`: coefficients fitted only on 2020–2022 releases, out-of-time 2023 validation, and a 2024 holdout for compute-only and compute-plus-data-balance relations.
- `tables/milestone_order_branches.csv`: separate AI-R&D, embodiment, Earth/space capital-closure, and control-readiness clocks across all four digital/physical speed combinations and a terrestrial-first counterfactual.
- `tables/closure_loop_ablation_matrix.csv`: orthogonal verified AI-R&D-loop and reproductive-capital-loop switches for the central Moon–asteroid scenario.
- `tables/intergenerational_learning_faults.csv`: repeated and hidden structural-transfer faults across controller generations with latency, retention, recurrence, recovery, verification, and regression gates.
- `tables/digital_learning_feedback.csv`: campaign-derived stage-rate and verified-yield feedback compared with the unadjusted digital loop.
- `tables/matched_lifecycle_cost_contributions.csv`: paired Earth/space categories with uncertainty intervals, contribution shares, difference ranks, and explicit omission labels.
- `tables/data_advantage_profile.csv`: seven component values, uncertainty widths, hard gates, weights, and the assumption-class scalarization.
- `tables/coordination_sensitivity.csv`: dependency topology, complexity, uncertainty, intelligence, and the irreducible coordination floor.
- `tables/coordination_form_uncertainty.csv` and `tables/coordination_form_summary.csv`: common-draw power, logarithmic, and saturating edge responses with one-way schedule, capacity, reliability, and labor-cost mappings.
- `tables/embodiment_compatibility_matrix.csv`: physical gate failures, hardware ceilings, intelligence thresholds, verification status, and first passage by task and hardware portfolio.
- `tables/embodiment_two_direction_sweep.csv` and `tables/terrestrial_rehearsal_embodiment_faults.csv`: independent intelligence/hardware sweeps and declared degraded-hardware cases.
- `tables/embodiment_bom_requirements.csv`: sensor, actuator, tooling, spares, calibration, and control-hardware additions to the material bill and replacement-service graph.
- `tables/orbital_lifecycle_states.csv`: nine capacity-equivalent lifecycle stocks plus repair, recycling, retrieval, and irreversible-loss flows.
- `tables/orbital_lifecycle_strategy_comparison.csv`: serviceability and circular-design portfolios with mass penalties and lifecycle outcomes.
- `tables/orbital_transport_service_network.csv`: four named origin-destination routes, maturity gates, rocket-equation propellant, and one-at-a-time service-economics sensitivities.
- `tables/orbital_transport_break_even_surface.csv`: a multi-axis client, failure, serviceability, fleet, recovery, reuse, route, propellant-source, and lunar-maturity break-even surface.
- `tables/orbital_service_decision_comparison.csv`: nine service or disposition actions across six orbit regimes, two asset classes, and three fleet architectures with separate technical, economic, governance, and deployable gates.
- `tables/orbital_regime_assumptions.csv`, `tables/orbital_fleet_amortization.csv`, and `tables/orbital_governance_constraints.csv`: orbit-specific operating conditions, fleet fixed-cost sharing, and unresolved legal/authorization dependencies.
- `tables/orbital_control_policy.csv`: common-cause loss-budget checks, shell-state triggers, and deterministic mitigation actions.
- `tables/orbital_cluster_layout_optimization.csv`: physical/logical failure-domain layouts with common-cause, fragment-correlation, communications, concentration, and Pareto diagnostics.
- `tables/orbital_breakup_cloud_summary.csv` and `tables/orbital_breakup_cloud_trajectory.csv`: explicit-node Earth/lunar breakup propagation, losses, maneuvers, interruption, repair, and restoration.
- `tables/orbital_degraded_control_stress.csv`: tracking, communications, navigation, and centralized-coordination failures with fallback checks.
- `tables/orbital_mitigation_portfolio_pareto.csv`: 256 portfolios over eight controls with risk, cost, delivered capacity, and non-dominance.
- `tables/orbital_environment_strategy_comparison.csv` and `tables/orbital_multi_operator_capacity.csv`: distinct Earth/lunar operating regimes and shared-shell governance/carrying-capacity gates.
- `tables/partial_closure_metrics.csv`: strict autonomy, mass closure, external-support intensity, import leverage, and critical residual inputs.
- `tables/partial_closure_support_policies.csv` and `tables/partial_closure_dashboard.csv`: fixed, proportional, stockpile, and disrupted import policies with continuous closure and runway metrics.
- `tables/partial_closure_substitution_programs.csv`: discrete dependency program gates, outcomes, and resource-accounted expansion opportunity cost.
- `tables/partial_closure_supplier_boundary.csv`: resource-specific external factory, material, labor, energy, finance, transport, reliability, growth, and utilization constraints.
- `tables/partial_closure_allocation_policies.csv`: immediate expansion, replacement reserve, balanced, and substitution-first allocation outcomes.

All coefficients in these tables are `ASSUMPTION`-class scenario inputs unless a row says otherwise. The tables expose comparative behavior and falsification targets; they are not empirical forecasts.

## Reproducibility

```bash
uv run --locked rsi-run-integrated
pytest tests/test_extensions.py tests/test_integrated.py tests/test_integrated_analysis.py -q
```

Every generated table is derived from the same in-memory run. `outputs/integrated/MANIFEST.md` hashes the parameter file, implementation, runner, report, tables, and figures.
