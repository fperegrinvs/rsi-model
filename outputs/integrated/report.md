# Current integrated-bootstrap model

- model version: `integrated-model-1`
- assumption ensemble: n=200 per scenario, seed=404
- epistemic status: scenario implications, not measurements or forecasts

## Headline results

| scenario | central installed seed mass | Earth strategic-material import stock | aggregate operating-capacity doubling (80y extension) | cell-equivalents at year 40 | design-space occupancy | ensemble seed p10/p50/p90 |
|---|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | 206.7 t | 48.1 t | — | 0.47 | 83/200 | 171/201/228 t |
| lunar_strategic_material_bridge | 216.7 t | 58.1 t | — | 0.54 | 126/200 | 181/212/247 t |
| lunar_strict | infeasible | — | — | — | 0/200 | — |
| moon_asteroid_network | 185.5 t | 0.0 t | 34.8 yr | 3.61 | 187/200 | 155/204/310 t |

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
- tight constraints: `element:Cr` (-2.22e-15), `element:Ni` (-1.78e-15), `element:C` (-8.88e-16), `element:rare_earths` (-4.44e-16), `element:H` (-5.55e-17)

### lunar_strategic_material_bridge

- status: lexicographic installed_mass optimum within the declared linear seed architecture
- minimum task coverage: 0.807
- residual intervention: 130.5 h/year
- lunar feed: 540.0 t/year
- asteroid feed: 0.0 t/year
- tight constraints: `element:Cu` (-2.66e-15), `element:Ni` (-1.78e-15), `element:C` (-8.88e-16), `element:Li` (-1.11e-16), `element:H` (-5.55e-17)

### lunar_strict

- status: The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)
- minimum task coverage: 0.894

### moon_asteroid_network

- status: lexicographic installed_mass optimum within the declared linear seed architecture
- minimum task coverage: 0.952
- residual intervention: 30.6 h/year
- lunar feed: 366.2 t/year
- asteroid feed: 173.8 t/year
- tight constraints: `element:dopants` (+0.00e+00), `throughput:asteroid_mining` (+0.00e+00), `throughput:asteroid_transport` (+0.00e+00), `throughput:refining` (+2.84e-14), `autonomy:intervention_budget` (+9.74e-01)

## Delivered-to-operating seed stage (r4.0)

The LP mass is an installed-seed quantity. The deployment diagnostic adds transport packaging, unloading and site equipment, calibration references, initial spares, and startup-energy storage, then moves the core seed through distinct states. Eight percent of newly commissioned core mass enters a declared startup-failure queue and must consume spares before it can operate. All deployment coefficients are explicit `ASSUMPTION`s with a bounding argument; they are not a mission estimate. Machine-readable: `tables/seed_deployment_trajectory.csv`.

| scenario | installed seed | delivered seed | logistics increment | startup energy | first operation | full operating seed | recovered startup failures |
|---|---:|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | 206.7 t | 290.2 t | 83.5 t | 103.3 MWh | 1.5 yr | 5.5 yr | 16.5 t |
| lunar_strategic_material_bridge | 216.7 t | 303.3 t | 86.5 t | 108.4 MWh | 1.5 yr | 5.8 yr | 17.3 t |
| moon_asteroid_network | 185.5 t | 262.7 t | 77.2 t | 92.8 MWh | 1.5 yr | 5.0 yr | 14.8 t |

## Compute regimes at year 40

| regime | normalized capacity |
|---|---:|
| off-world endogenous total | 5.82 |
| Moon→orbit endogenous export | 0.78 |
| Earth-fed orbit, tight | 1.56 |
| Earth-fed orbit, base | 2.81 |
| Earth-fed orbit, responsive | 4.99 |

The endogenous curve compounds only after the seed survives commissioning and source constraints. Earth-fed orbital capacity remains an affine deployment process and approaches a depreciation-limited stock at constant delivery. The terrestrial curves are rate-and-site-ceiling scenarios, not forecasts of actual buildout.

## Debris condition

| case | creation-to-clearance ratio, last 5 yr | clearance >= creation | fragment index, year 40 |
|---|---:|:---:|---:|
| Earth-fed orbit / weak mitigation | 0.61 | yes | 1.602 |
| Earth-fed orbit / strong mitigation | 0.35 | yes | 0.284 |
| dense endogenous / weak mitigation | 4.79 | no | 3.840 |
| dense endogenous / strong mitigation | 4.45 | no | 2.214 |
| distributed endogenous / sparse topology | 1.00 | yes | 0.000 |

A dense shell is not licensed by industrial closure alone. In this scenario record, rapid endogenous deployment creates several times the fragments it clears under both weak and strong shell mitigation (the ratio is a flow ratio, not a branching-process reproduction number). The sparse/distributed topology sits at the boundary ratio only because its collision kernel is explicitly lower; that multiplier is an assumption to be replaced by shell- and trajectory-specific data.

### Finite-mass, shell-resolved diagnostic

A second diagnostic resolves 400-km LEO, 650-km LEO, and cislunar regions; active assets, intact derelicts, trackable fragments, and untrackable fragments; density/volume kernels; avoidance saturation; cross-shell fragment transport; disposal, natural clearance, retrieval, and active removal. Requested deployment consumes a finite feed inventory supplied by time-limited Earth import, depletion of a finite capture reservoir, and recovered retirements. Collision losses reduce returned active capacity and enter replacement/import cost.

| shell | active capacity, year 40 | intact derelicts | trackable | untrackable | expected hazardous-descendant ratio |
|---|---:|---:|---:|---:|---:|
| leo_400 | 0.187 | 0.010 | 0.000 | 0.007 | 0.000 |
| leo_650 | 0.480 | 0.027 | 0.000 | 0.221 | 0.026 |
| cislunar | 0.075 | 0.004 | 0.000 | 0.032 | 0.000 |

At year 40 the finite reservoir retains 220.0 t and feed inventory retains 539.5 t; cumulative requested-deployment shortfall is 0.00 normalized units. Replacement/import cost under the declared delivered-mass price is $327.0M. The descendant ratio is a branching-style stress metric rather than the legacy creation/clearance flow ratio. Machine-readable: `tables/orbital_mass_balance.csv` and `tables/shell_debris_trajectory.csv`.

## Governance threat/control traceability (r4.0)

The governance model now names actors, assets, trust boundaries, normal/delayed/lost-link authority, eight threat paths, and nine controls with verification, rollback, and residual risk. Controls map to live build rate, sector floors, repair queues, source flows, commissioning cohorts, debris state, and independent inventory measurements. Every control remains `requirement_unvalidated`; this is not a solved safety case. See `docs/GOVERNANCE_THREAT_MODEL.md` and `tables/governance_threat_control_traceability.csv`.

The linked Stage-0 protocol converts those controls into ten binary acceptance gates, a typed raw-event contract, a fault campaign that covers every registered threat plus communication loss, and explicit model-parameter replacement rules. Every checklist row is still `execution_pending` or `data_pending`: the protocol is executable, but no physical rehearsal result is claimed. See `docs/TERRESTRIAL_REHEARSAL_PROTOCOL.md` and `tables/rehearsal_acceptance_matrix.csv`.

## Terminal-window operating-capacity endpoints (r4.0)

Aggregate operating-capacity doubling is a threshold crossing of the slowest normalized sector; these endpoints separately report retention and final-five-year direction. The central 80-year extension is in `tables/long_horizon_endpoints.csv`; the complete sector trajectory is in `tables/sector_capacity_trajectory.csv`.

| scenario | aggregate doubling | at year 40 | retained >= 2 | net final-5y | ensemble retained | ensemble terminal-window expanding |
|---|---:|---:|:---:|---:|---:|---:|
| terrestrial_rehearsal | — | 0.47 | no | -0.022 | 0/83 | 0/83 |
| lunar_strategic_material_bridge | — | 0.54 | no | -0.027 | 0/126 | 0/126 |
| lunar_strict | — | — | — | — | 0/200 | 0/200 |
| moon_asteroid_network | 34.8 yr | 3.61 | yes | +1.530 | 150/187 | 187/187 |

Reading: the terrestrial rehearsal and lunar strategic-material bridge never reach aggregate doubling in the 80-year extension and are contracting at year 40. The Moon–asteroid network is terminal-window expanding, reaches 3.61 equivalents at year 40, and first crosses two at year 34.75. Import-pool exhaustion years are per-category first dips of the pooled inventory (initial Earth stock plus recycled returns and local production) and are reported in `tables/import_stock_composition.csv`; pools can refill later from local production, so a first dip is not permanent depletion.

## Intelligence-coupling ablations (r4.0)

Zero/freeze ablations of the declared coupling coefficients; the seed LP does not read the intelligence block, so dynamics variants share the central seed. Machine-readable: `tables/ablations.csv`.

| scenario | variant | aggregate doubling | at year 40 | growth share of baseline |
|---|---|---:|---:|---:|
| terrestrial_rehearsal | baseline | — | 0.47 | 100% |
| terrestrial_rehearsal | no_intelligence_growth | — | 0.47 | 100% |
| terrestrial_rehearsal | productivity_channel_only | — | 0.47 | 100% |
| terrestrial_rehearsal | autonomy_channel_only | — | 0.47 | 100% |
| terrestrial_rehearsal | fully_uncoupled | — | 0.47 | 100% |
| terrestrial_rehearsal | seed_sized_at_base_autonomy | — | 0.47 | 100% |
| lunar_strategic_material_bridge | baseline | — | 0.54 | 100% |
| lunar_strategic_material_bridge | no_intelligence_growth | — | 0.54 | 100% |
| lunar_strategic_material_bridge | productivity_channel_only | — | 0.54 | 100% |
| lunar_strategic_material_bridge | autonomy_channel_only | — | 0.54 | 100% |
| lunar_strategic_material_bridge | fully_uncoupled | — | 0.54 | 100% |
| lunar_strategic_material_bridge | seed_sized_at_base_autonomy | — | infeasible | — |
| moon_asteroid_network | baseline | 34.75 yr | 3.61 | 100% |
| moon_asteroid_network | no_intelligence_growth | 36.75 yr | 2.70 | 65% |
| moon_asteroid_network | productivity_channel_only | 35.50 yr | 3.16 | 83% |
| moon_asteroid_network | autonomy_channel_only | 35.75 yr | 3.06 | 79% |
| moon_asteroid_network | fully_uncoupled | 36.75 yr | 2.70 | 65% |
| moon_asteroid_network | seed_sized_at_base_autonomy | — | infeasible | — |

Finding: sector resolution separates regimes that the former scalar state conflated (terrestrial_rehearsal: 145/160; lunar_strategic_material_bridge: 146/160; moon_asteroid_network: 48/160 steps material-limited). The terrestrial and lunar-bridge trajectories remain overwhelmingly material-limited, so coupling ablations move their year-40 endpoints by less than a tenth of one percent. In the Moon–asteroid network, however, the fully uncoupled run reaches 2.70 sector-balanced equivalents versus 3.61 at baseline, retaining about 65% of baseline net growth. The dynamic coupling is therefore operative only after the diverse source vector relaxes the material bottleneck. The declared starting AI level also remains load-bearing statically: sizing at base autonomy makes the bridge and network seeds infeasible.

The exhaustive primary-constraint classification is terrestrial_rehearsal: material 145, service 0, order-cap 15; lunar_strategic_material_bridge: material 146, service 0, order-cap 14; moon_asteroid_network: material 48, service 0, order-cap 112 (160 quarterly steps each). Machine-readable: `tables/dynamic_regime_summary.csv`.

## Knowledge and observable autonomy gates (r4.0)

The 5 t knowledge package is now decomposed into storage/compute, software/toolchains, calibration references, laboratory equipment, consumables/recipes, and test articles. Each sector reports named-task completion, intervention demand, fault diagnosis, verification throughput, engineering-cycle time, process yield, repair success, mean time to recovery, and a non-divisible stop-line pass. These are ASSUMPTION-class diagnostic mappings pending Stage-0 measurements, not evidence that the capabilities exist. Machine-readable: `tables/knowledge_autonomy_observables.csv`.

Two-year zero-capacity windows isolate the autonomy, verification, and compute regimes; a 90% advanced-logic/memory loss at year 5 isolates repair. The zero-capacity windows are adversarial boundary tests, not frequency estimates.

| scenario | variant | at year 40 | doubling | material | autonomy | verification | repair | compute | service | order-cap |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | declared | 0.47 | — | 145 | 0 | 0 | 0 | 0 | 0 | 15 |
| terrestrial_rehearsal | communication_outage_years10_12 | 0.47 | — | 136 | 8 | 0 | 0 | 0 | 0 | 16 |
| terrestrial_rehearsal | verification_outage_years10_12 | 0.47 | — | 136 | 0 | 8 | 0 | 0 | 0 | 16 |
| terrestrial_rehearsal | compute_outage_years10_12 | 0.47 | — | 136 | 0 | 0 | 0 | 8 | 0 | 16 |
| terrestrial_rehearsal | repair_after_advanced_logic_90pct_loss_year5 | 1.71 | 14.2 yr | 139 | 0 | 0 | 3 | 0 | 0 | 18 |
| lunar_strategic_material_bridge | declared | 0.54 | — | 146 | 0 | 0 | 0 | 0 | 0 | 14 |
| lunar_strategic_material_bridge | communication_outage_years10_12 | 0.54 | — | 137 | 8 | 0 | 0 | 0 | 0 | 15 |
| lunar_strategic_material_bridge | verification_outage_years10_12 | 0.54 | — | 137 | 0 | 8 | 0 | 0 | 0 | 15 |
| lunar_strategic_material_bridge | compute_outage_years10_12 | 0.54 | — | 137 | 0 | 0 | 0 | 8 | 0 | 15 |
| lunar_strategic_material_bridge | repair_after_advanced_logic_90pct_loss_year5 | 2.19 | 18.5 yr | 148 | 0 | 0 | 3 | 0 | 0 | 9 |
| moon_asteroid_network | declared | 3.61 | 34.8 yr | 48 | 0 | 0 | 0 | 0 | 0 | 112 |
| moon_asteroid_network | communication_outage_years10_12 | 3.11 | 36.0 yr | 40 | 8 | 0 | 0 | 0 | 0 | 112 |
| moon_asteroid_network | verification_outage_years10_12 | 3.11 | 36.0 yr | 40 | 0 | 8 | 0 | 0 | 0 | 112 |
| moon_asteroid_network | compute_outage_years10_12 | 3.11 | 36.0 yr | 40 | 0 | 0 | 0 | 8 | 0 | 112 |
| moon_asteroid_network | repair_after_advanced_logic_90pct_loss_year5 | 4.60 | 28.0 yr | 105 | 0 | 0 | 54 | 0 | 0 | 1 |

The declared central cases remain material/order-cap limited. The adversarial windows create the named regimes mechanically and reduce the Moon–asteroid endpoint; this demonstrates classification and falsification plumbing, not calibrated outage risk. Machine-readable: `tables/knowledge_regime_summary.csv`.

## Operating-environment/process coupling (r4.0)

The central release remains on the identity `centrifuge_only` profile for continuity. Separate nominal and adverse lunar profiles apply process-specific throughput, quality-yield, power-demand, and depreciation multipliers for dust, traction, reduced convection, vacuum behavior, radiation, thermal cycling, contamination, and calibration drift. Every multiplier is an explicit bounding `ASSUMPTION`; Earth rehearsal results do not transfer to these profiles automatically.

| scenario | environment | feasible | seed mass | top binding row | at year 40 | doubling | survived |
|---|---|:---:|---:|---|---:|---:|:---:|
| terrestrial_rehearsal | centrifuge_only | yes | 206.7 t | element:Cr | 0.47 | — | no |
| terrestrial_rehearsal | lunar_nominal | yes | 210.4 t | element:C | 0.51 | — | yes |
| terrestrial_rehearsal | lunar_adverse | no | — t | — | — | — | — |
| lunar_strategic_material_bridge | centrifuge_only | yes | 216.7 t | element:Cu | 0.54 | — | no |
| lunar_strategic_material_bridge | lunar_nominal | yes | 222.9 t | element:Ni | 0.59 | — | no |
| lunar_strategic_material_bridge | lunar_adverse | no | — t | — | — | — | — |
| lunar_strict | centrifuge_only | no | — t | — | — | — | — |
| lunar_strict | lunar_nominal | no | — t | — | — | — | — |
| lunar_strict | lunar_adverse | no | — t | — | — | — | — |
| moon_asteroid_network | centrifuge_only | yes | 185.5 t | element:dopants | 3.61 | 34.8 yr | yes |
| moon_asteroid_network | lunar_nominal | yes | 192.6 t | throughput:asteroid_mining | 3.78 | 34.2 yr | yes |
| moon_asteroid_network | lunar_adverse | yes | 206.2 t | throughput:asteroid_transport | 3.96 | 34.0 yr | yes |

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
| moon_asteroid_network | perfect_foresight | 19 | 19 | 19 |

The machine-readable sweep reports minimum live sector margin and first aggregate doubling for every case, making failure boundaries inspectable rather than reducing them to one rank correlation. `tables/policy_robustness_sweep.csv` is authoritative.

## Tiered electronics closure and inventory life (r4.0)

The integrated layer no longer uses the inherited scalar electronics productivity range in its headline analysis. Seven tiers now carry separate local-producibility, replacement, shelf-life, obsolescence, and substitution assumptions. Imported tier inventory decays before use, and the architecture comparison includes frontier-local, permanent-import, mature/repairable, and cannibalization-based cases.

| scenario | architecture | viable tiers | total tier shortfall | gross permanent-import mass | first shortfall |
|---|---|---:|---:|---:|---:|
| lunar_strategic_material_bridge | frontier_local | 5/7 | 0.478 | 0.0 t | 2.2 yr |
| lunar_strategic_material_bridge | permanent_import | 7/7 | 0.000 | 110.7 t | — |
| lunar_strategic_material_bridge | mature_repairable | 6/7 | 0.002 | 11.1 t | 11.0 yr |
| lunar_strategic_material_bridge | cannibalization_based | 6/7 | 0.028 | 0.0 t | 7.8 yr |
| moon_asteroid_network | frontier_local | 5/7 | 1.345 | 0.0 t | 2.2 yr |
| moon_asteroid_network | permanent_import | 5/7 | 0.307 | 110.7 t | 32.5 yr |
| moon_asteroid_network | mature_repairable | 5/7 | 0.177 | 11.1 t | 25.2 yr |
| moon_asteroid_network | cannibalization_based | 5/7 | 0.452 | 0.0 t | 16.5 yr |

Every tested architecture still develops a shortfall in advanced logic/memory or process-equipment/metrology under the expanding Moon–asteroid demand path; fixed imports proportional to the initial seed do not scale with endogenous demand. The most decision-reducing measurements are therefore demonstrated mature-node wafer yield and parent-tool/calibration replacement demand, followed by useful life and permanent-import mass per service-year. The strict-lunar minimum cut remains tiered in the seed LP and is not erased by these dynamic inventory cases. Machine-readable: `tables/electronics_architecture_comparison.csv`.

The empirical-calibration contract separates the Earth reference, serviceable space platform, and integrated disposable cases; requires equal-workload records; binds six evidence packages to current model parameters; preserves correlated reliability, link, thermal, Earth-resource, demand, and financing uncertainty; and defines an audited cash-flow event ledger with chronological holdout validation. All readiness rows remain `data_pending`. See `docs/ECONOMIC_CALIBRATION_PROTOCOL.md` and `tables/economic_calibration_readiness.csv`.

The publication contract names target and fallback venues for all three papers and measures each draft against current publisher requirements. Machine-checkable structure now passes where supplied, while references, fallback word-count expansion, live-portal fields, and every author-controlled declaration remain explicitly pending. See `docs/VENUE_SELECTION_AND_CONFORMANCE.md` and `tables/publication_readiness.csv`.

## Symmetric dynamic economics (r4.0)

Earth and space now use the same reinvestment/debt logic: endogenous investment, learning, depreciation/obsolescence, regulatory build queues, debt-to-revenue limits, interest, bridge financing, market demand, and expanding resource ceilings. Space is additionally capped by the physical model and pays for its funded share of industrial orders, source transfer, and intervention. The coefficients are ASSUMPTION-class scenario mechanics, not a valuation.

| market | technical space at year 40 | funded space | Earth | space finance-limited steps | Earth finance-limited steps | space self-financing | Earth self-financing |
|---|---:|---:|---:|---:|---:|---:|---:|
| commodity_compute | 5.82 | 0.57 | 68.97 | 36 | 0 | — | — |
| space_native_services | 5.82 | 3.59 | 25.86 | 0 | 0 | — | 27.2 yr |

Physical compounding does not automatically fund deployment. In the commodity case, finance activates only a small fraction of technically available space capacity while Earth expands endogenously. A space-native price premium funds more of the physical path, but the space case still does not repay its declared external capital inside 40 years. P3b therefore remains a conditional economic proposition, not a consequence of the physical growth curve. Machine-readable: `tables/symmetric_dynamic_economics.csv`.

## Composition-changing robust-seed Pareto search (r4.0)

The design search now changes process route, sector redundancy, and lunar/asteroid source allocation instead of merely relabeling one LP objective or scaling a fixed vector. It minimizes delivered mass, Earth import, intervention, and doubling time while maximizing year-40 capacity and capacity after a five-year asteroid-source outage. Dominance is computed across all six objectives.

| route | redundancy | source portfolio | delivered mass | doubling | year 40 | after outage | Pareto | robust |
|---|---|---|---:|---:|---:|---:|:---:|:---:|
| baseline | minimum | baseline | 262.7 t | 26.5 yr | 7.72 | 5.19 | yes | yes |
| baseline | minimum | asteroid_reserve | 303.5 t | 23.5 yr | 10.57 | 6.59 | yes | yes |
| mature_node | minimum | baseline | 258.2 t | 23.5 yr | 7.09 | 5.25 | yes | yes |
| mature_node | minimum | asteroid_reserve | 297.8 t | 23.5 yr | 9.10 | 6.47 | yes | yes |
| modular_tools | minimum | asteroid_reserve | 303.2 t | 24.0 yr | 11.06 | 5.09 | yes | yes |

The minimum delivered-mass robust candidate in this enumerated design space is `mature_node` / `minimum` / `baseline` at 258.2 t. This is an ASSUMPTION-conditioned discrete frontier, not a globally optimal mission design. Machine-readable dominated and non-dominated points: `tables/robust_seed_pareto.csv`.

## Allocation, repair, and shock-policy comparison (r4.0)

The published central case retains balanced build packets for continuity. The structural diagnostic below instead maximizes the weakest live sector margin, then minimizes installed mass at that margin. Repair uses the declared ASSUMPTION-class parts, service, intervention, and lag coefficients. The shock removes 50% of the advanced-logic/memory sector at year 20; it is a deterministic stress case, not a frequency estimate. Machine-readable: `tables/allocation_repair_comparison.csv`.

| scenario | policy | repair | shock | doubling | at year 40 | minimum sector margin | survived | shock recovery |
|---|---|:---:|---|---:|---:|---:|:---:|---:|
| terrestrial_rehearsal | balanced | no | none | — | 0.47 | 0.47 | no | — |
| terrestrial_rehearsal | maximin_sector | no | none | — | 1.11 | 1.11 | yes | — |
| terrestrial_rehearsal | maximin_sector | yes | none | 19.8 yr | 1.77 | 1.77 | yes | — |
| terrestrial_rehearsal | maximin_sector | yes | advanced_logic_memory:50%@year20 | 19.8 yr | 1.67 | 1.67 | yes | 26.0 yr |
| lunar_strategic_material_bridge | balanced | no | none | — | 0.54 | 0.54 | no | — |
| lunar_strategic_material_bridge | maximin_sector | no | none | 31.0 yr | 1.19 | 1.19 | yes | — |
| lunar_strategic_material_bridge | maximin_sector | yes | none | 16.5 yr | 2.19 | 2.19 | yes | — |
| lunar_strategic_material_bridge | maximin_sector | yes | advanced_logic_memory:50%@year20 | 16.5 yr | 2.14 | 2.14 | yes | 25.2 yr |
| moon_asteroid_network | balanced | no | none | 34.8 yr | 3.61 | 3.61 | yes | — |
| moon_asteroid_network | maximin_sector | no | none | 32.0 yr | 3.50 | 3.50 | yes | — |
| moon_asteroid_network | maximin_sector | yes | none | 28.0 yr | 4.16 | 4.16 | yes | — |
| moon_asteroid_network | maximin_sector | yes | advanced_logic_memory:50%@year20 | 28.2 yr | 4.62 | 4.62 | yes | 23.8 yr |

These policy outcomes are not new feasibility claims: the allocator and repair coefficients expose how strongly the result depends on construction policy and recoverability. They replace the earlier implicit claim that only balanced copies can be ordered.

## Installed-mass versus aggregate-doubling frontier (r4.0)

A factor-f seed installs f cell-equivalents of the minimum-mass design (capacities, feeds, strategic import stock scale with f; the digital package is shared). Time is first passage to one *additional* operating cell-equivalent, so f = 1 coincides with the canonical metric. The oversize factor is a sweep axis, not a new assumption. Machine-readable: `tables/oversize_frontier.csv`; figure: `figures/oversize_frontier.png`.

| scenario | factor | installed mass | time to +1 cell | additional cells at year 40 |
|---|---:|---:|---:|---:|
| terrestrial_rehearsal | ×1 | 206.7 t | — | -0.53 |
| terrestrial_rehearsal | ×1.25 | 257.1 t | — | -0.66 |
| terrestrial_rehearsal | ×1.5 | 307.5 t | — | -0.80 |
| terrestrial_rehearsal | ×2 | 408.3 t | — | -1.06 |
| lunar_strategic_material_bridge | ×1 | 216.7 t | — | -0.46 |
| lunar_strategic_material_bridge | ×1.25 | 269.7 t | — | -0.58 |
| lunar_strategic_material_bridge | ×1.5 | 322.6 t | — | -0.70 |
| lunar_strategic_material_bridge | ×2 | 428.5 t | — | -0.93 |
| moon_asteroid_network | ×1 | 185.5 t | 34.75 yr | +2.61 |
| moon_asteroid_network | ×1.25 | 230.6 t | 33.75 yr | +3.26 |
| moon_asteroid_network | ×1.5 | 275.8 t | 33.00 yr | +3.91 |
| moon_asteroid_network | ×2 | 366.0 t | 32.00 yr | +5.21 |

The sector-resolved frontier reverses the earlier scalar-state reading. Neither the terrestrial nor lunar bridge design reaches one additional balanced cell-equivalent at any tested scale by year 40. The Moon–asteroid minimum-mass design also misses that threshold, while 1.25x, 1.5x, and 2x scaled designs reach it at 39.25, 38.5, and 37.25 years. Scaling one fixed composition is still not a multi-objective redesign.

## Alternative seed objectives (r4.0)

The same seed LP was solved lexicographically for minimum installed mass, minimum Earth-import mass, and minimum annual intervention, with installed mass as the secondary tie-break for the latter two. Machine-readable: `tables/seed_objective_comparison.csv`.

| scenario | objective | installed mass | import mass | intervention | capacity-vector distance from mass optimum |
|---|---|---:|---:|---:|---:|
| terrestrial_rehearsal | installed_mass | 206.7 t | 48.1 t | 193.2 h/yr | 0 |
| terrestrial_rehearsal | earth_import_mass | 206.7 t | 48.1 t | 193.2 h/yr | 0 |
| terrestrial_rehearsal | intervention_hours | 206.7 t | 48.1 t | 193.2 h/yr | 0 |
| lunar_strategic_material_bridge | installed_mass | 216.7 t | 58.1 t | 130.5 h/yr | 0 |
| lunar_strategic_material_bridge | earth_import_mass | 216.7 t | 58.1 t | 130.5 h/yr | 0 |
| lunar_strategic_material_bridge | intervention_hours | 216.7 t | 58.1 t | 130.5 h/yr | 0 |
| lunar_strict | installed_mass | infeasible | — | — | — |
| lunar_strict | earth_import_mass | infeasible | — | — | — |
| lunar_strict | intervention_hours | infeasible | — | — | — |
| moon_asteroid_network | installed_mass | 185.5 t | 0.0 t | 30.6 h/yr | 0 |
| moon_asteroid_network | earth_import_mass | 185.5 t | 0.0 t | 30.6 h/yr | 0 |
| moon_asteroid_network | intervention_hours | 185.5 t | 0.0 t | 30.6 h/yr | 0 |

All three objectives return the identical central design in every LP-feasible scenario. This is a negative structural result: the current variables and constraints do not expose a mass/import/intervention tradeoff for the optimizer to choose. A genuine Pareto front requires alternative process routes, sector composition, redundancy, or deployment decisions; relabeling the objective alone cannot create it.

## Ensemble diagnostics (r4.0)

Per-draw failure reasons, top binding constraints among feasible draws, and Spearman rank sensitivity of the named multipliers (machine-readable: `tables/diagnostics_histograms.csv`, `tables/ensemble_sensitivity.csv`):

- **terrestrial_rehearsal**: failures — autonomy_threshold 77, lp_infeasible 40; top binding — element:Cu 25, element:Cr 15, element:C 13, element:Fe 7.
- **lunar_strategic_material_bridge**: failures — autonomy_threshold 54, lp_infeasible 20; top binding — element:C 32, element:Ni 30, element:Cu 29, element:Cr 13.
- **lunar_strict**: failures — lp_infeasible 167, autonomy_threshold 33; top binding — n/a.
- **moon_asteroid_network**: failures — autonomy_threshold 13; top binding — element:dopants 62, throughput:refining 58, throughput:asteroid_transport 42, throughput:asteroid_mining 15.

These are rank screens inside the declared independent multiplier measure, not causal effects or global sensitivity. Sector resolution changes both signs and magnitudes relative to the scalar-state run; the machine-readable table is authoritative and no previous depreciation-direction claim is carried forward.

## Strict-lunar infeasibility certificate (r4.0)

Elastic relaxation of the exact seed LP (every row receives a nonnegative slack; the slack sum is minimized in row-native units). This is a minimum total-violation certificate, not a strict irreducible infeasible subsystem. Machine-readable: `tables/infeasibility_certificate.csv`.

**lunar_strict** — unsatisfiable requirement rows (minimum shortfall over the horizon):

| constraint | minimum shortfall | units |
|---|---:|---|
| element:Ni | 19.05 | tonnes over the horizon |
| element:Cu | 18.44 | tonnes over the horizon |
| element:C | 15.34 | tonnes over the horizon |
| element:Co | 3.63 | tonnes over the horizon |
| element:Cr | 3.11 | tonnes over the horizon |
| element:rare_earths | 2.28 | tonnes over the horizon |
| element:Li | 2.25 | tonnes over the horizon |
| element:H | 0.23 | tonnes over the horizon |
| element:dopants | 0.12 | tonnes over the horizon |

The strict-lunar cut is material, category-specific, and quantified: the configured lunar yields cannot supply the Ni, Cu, C, Co, Cr, rare-earth, Li, and H demands of the declared electronics and process-equipment stack within the horizon's throughput and energy limits. Substituting recipes, richer measured deposits, or a different electronics architecture would change this table, which is exactly what makes it a useful engineering target list.

## Reproducibility

```bash
python scripts/run_integrated.py
pytest tests/test_integrated.py tests/test_integrated_analysis.py -q
```

Every generated table is derived from the same in-memory run. `outputs/integrated/MANIFEST.md` hashes the parameter file, implementation, runner, report, tables, and figures.
