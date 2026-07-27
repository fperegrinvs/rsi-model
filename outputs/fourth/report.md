# Fourth Edition integrated-bootstrap model

- model version: `fourth-edition-1`
- assumption ensemble: n=200 per scenario, seed=404
- epistemic status: scenario implications, not measurements or forecasts

## Headline results

| scenario | central installed seed mass | Earth vitamin stock | first passage to two cell-equivalents | cell-equivalents at year 40 | model-feasible draws | ensemble seed p10/p50/p90 |
|---|---:|---:|---:|---:|---:|---:|
| terrestrial_rehearsal | 206.7 t | 48.1 t | 9.2 yr | 1.93 | 83/200 | 171/201/228 t |
| lunar_vitamin_bridge | 216.7 t | 58.1 t | 11.2 yr | 2.29 | 126/200 | 181/212/247 t |
| lunar_strict | infeasible | — | — | — | 0/200 | — |
| moon_asteroid_network | 185.5 t | 0.0 t | 22.8 yr | 12.55 | 187/200 | 155/204/310 t |

The strict lunar-only case is a structural infeasibility inside the declared architecture: trace lunar yields cannot reproduce the configured electronics and process-equipment stack, in the central case and in every ensemble draw. It is not a proof that lunar-only closure is physically impossible; substitution, different recipes, new processes, or measured richer deposits could change the constraint graph.

The Moon–asteroid case is likewise conditional. Its `diverse_asteroid_portfolio` is a deliberately composite source with ASSUMPTION-class recoverable yields. The model says what those yields would imply; it does not establish that a specific accessible portfolio has them.

## What changed from the inherited model

- 18 sectors, including seven separate electronics tiers.
- 17 element/material categories with explicit bills of material.
- Earth→Moon vitamin stock, asteroid→Moon feed, and Moon→orbit finished-compute arcs.
- Task coverage, intervention demand, lunar-gravity process compatibility, and centrifuge mass/power overhead.
- Construction lag, commissioning ramp, minimum viable scale, and an explicit second operating production cell.
- Coupled local compute, verified intelligence improvement, autonomy, and productivity.
- Rate-limited Earth and Earth-fed orbital counterfactuals.
- Active, derelict, and fragment stocks with a five-year fragment creation-to-clearance ratio.

## Central process and seed diagnostics

### terrestrial_rehearsal

- status: optimal within the declared linear seed architecture
- minimum task coverage: 0.720
- residual intervention: 193.2 h/year
- lunar feed: 540.0 t/year
- asteroid feed: 0.0 t/year
- tight constraints: `element:Cr` (-2.22e-15), `element:Ni` (-1.78e-15), `element:C` (-8.88e-16), `element:rare_earths` (-4.44e-16), `element:H` (-5.55e-17)

### lunar_vitamin_bridge

- status: optimal within the declared linear seed architecture
- minimum task coverage: 0.807
- residual intervention: 130.5 h/year
- lunar feed: 540.0 t/year
- asteroid feed: 0.0 t/year
- tight constraints: `element:Cu` (-2.66e-15), `element:Ni` (-1.78e-15), `element:C` (-8.88e-16), `element:Li` (-1.11e-16), `element:H` (-5.55e-17)

### lunar_strict

- status: The problem is infeasible. (HiGHS Status 8: model_status is Infeasible; primal_status is None)
- minimum task coverage: 0.894

### moon_asteroid_network

- status: optimal within the declared linear seed architecture
- minimum task coverage: 0.952
- residual intervention: 30.6 h/year
- lunar feed: 366.2 t/year
- asteroid feed: 173.8 t/year
- tight constraints: `element:dopants` (+0.00e+00), `throughput:asteroid_mining` (+0.00e+00), `throughput:asteroid_transport` (+0.00e+00), `throughput:refining` (+2.84e-14), `autonomy:intervention_budget` (+9.74e-01)

## Compute regimes at year 40

| regime | normalized capacity |
|---|---:|
| off-world endogenous total | 12.55 |
| Moon→orbit endogenous export | 1.63 |
| Earth-fed orbit, tight | 1.56 |
| Earth-fed orbit, base | 2.81 |
| Earth-fed orbit, responsive | 4.99 |

The endogenous curve compounds only after the seed survives commissioning and source constraints. Earth-fed orbital capacity remains an affine deployment process and approaches a depreciation-limited stock at constant delivery. The terrestrial curves are rate-and-site-ceiling scenarios, not forecasts of actual buildout.

## Debris condition

| case | creation-to-clearance ratio, last 5 yr | clearance >= creation | fragment index, year 40 |
|---|---:|:---:|---:|
| Earth-fed orbit / weak mitigation | 0.61 | yes | 1.602 |
| Earth-fed orbit / strong mitigation | 0.35 | yes | 0.284 |
| dense endogenous / weak mitigation | 5.53 | no | 16.497 |
| dense endogenous / strong mitigation | 5.58 | no | 12.632 |
| distributed endogenous / sparse topology | 1.00 | yes | 0.000 |

A dense shell is not licensed by industrial closure alone. In this scenario record, rapid endogenous deployment creates several times the fragments it clears under both weak and strong shell mitigation (the ratio is a flow ratio, not a branching-process reproduction number, and is not monotonic in mitigation strength). The sparse/distributed topology sits at the boundary ratio only because its collision kernel is explicitly lower; that multiplier is an assumption to be replaced by shell- and trajectory-specific data.

## Durable reproduction endpoints (r4.1)

First passage to two cell-equivalents is a reproduction *event*; these endpoints ask whether it was durable. Machine-readable: `tables/durable_endpoints.csv`.

| scenario | first passage | at year 40 | retained >= 2 | net final-5y | ensemble retained | ensemble durable final-5y |
|---|---:|---:|:---:|---:|---:|---:|
| terrestrial_rehearsal | 9.2 yr | 1.93 | no | -0.059 | 11/83 | 0/83 |
| lunar_vitamin_bridge | 11.2 yr | 2.29 | yes | -0.036 | 126/126 | 0/126 |
| lunar_strict | — | — | — | — | 0/200 | 0/200 |
| moon_asteroid_network | 22.8 yr | 12.55 | yes | +5.169 | 187/187 | 187/187 |

Reading: the lunar vitamin bridge retains two cell-equivalents in every feasible draw but is contracting over the final five years in every one of them; the terrestrial rehearsal reproduces once and falls back below two; only the Moon-asteroid network is durably expanding. Vitamin-pool exhaustion years are per-category first dips of the pooled inventory (initial Earth stock plus recycled returns and local production) and are reported in `tables/vitamin_composition.csv`; pools can refill later from local production, so a first dip is not permanent depletion.

## Intelligence-coupling ablations (r4.1)

Zero/freeze ablations of the declared coupling coefficients; the seed LP does not read the intelligence block, so dynamics variants share the central seed. Machine-readable: `tables/ablations.csv`.

| scenario | variant | first passage | at year 40 | growth share of baseline |
|---|---|---:|---:|---:|
| terrestrial_rehearsal | baseline | 9.25 yr | 1.93 | 100% |
| terrestrial_rehearsal | no_intelligence_growth | 9.25 yr | 1.93 | 100% |
| terrestrial_rehearsal | productivity_channel_only | 9.25 yr | 1.93 | 100% |
| terrestrial_rehearsal | autonomy_channel_only | 9.25 yr | 1.93 | 100% |
| terrestrial_rehearsal | fully_uncoupled | 9.25 yr | 1.93 | 100% |
| terrestrial_rehearsal | seed_sized_at_base_autonomy | 9.25 yr | 1.93 | 100% |
| lunar_vitamin_bridge | baseline | 11.25 yr | 2.29 | 100% |
| lunar_vitamin_bridge | no_intelligence_growth | 11.25 yr | 2.29 | 100% |
| lunar_vitamin_bridge | productivity_channel_only | 11.25 yr | 2.29 | 100% |
| lunar_vitamin_bridge | autonomy_channel_only | 11.25 yr | 2.29 | 100% |
| lunar_vitamin_bridge | fully_uncoupled | 11.25 yr | 2.29 | 100% |
| lunar_vitamin_bridge | seed_sized_at_base_autonomy | — | infeasible | — |
| moon_asteroid_network | baseline | 22.75 yr | 12.55 | 100% |
| moon_asteroid_network | no_intelligence_growth | 22.75 yr | 12.55 | 100% |
| moon_asteroid_network | productivity_channel_only | 22.75 yr | 12.55 | 100% |
| moon_asteroid_network | autonomy_channel_only | 22.75 yr | 12.55 | 100% |
| moon_asteroid_network | fully_uncoupled | 22.75 yr | 12.55 | 100% |
| moon_asteroid_network | seed_sized_at_base_autonomy | — | infeasible | — |

Finding: every dynamics ablation reproduces the baseline exactly, because realized cell orders are capped by material availability at every step (terrestrial_rehearsal: 160/160; lunar_vitamin_bridge: 160/160; moon_asteroid_network: 160/160 steps material-limited). Under the central coefficients the recursive intelligence-industry coupling contributes nothing to the reported growth trajectories; the declared AI level is instead load-bearing *statically*, through seed feasibility and sizing — re-sizing the seed at AI level 1.0 (base autonomy) leaves the terrestrial rehearsal unchanged and makes the lunar-bridge and Moon-asteroid scenarios infeasible on the autonomy threshold. The headline growth numbers are therefore material-throughput results, not artifacts of the assumed AI feedback; and the coupling's dynamic coefficients are currently untestable from these trajectories.

## Installed-mass versus reproduction-time frontier (r4.1)

A factor-f seed installs f cell-equivalents of the minimum-mass design (capacities, feeds, vitamin stock scale with f; the digital package is shared). Time is first passage to one *additional* operating cell-equivalent, so f = 1 coincides with the canonical metric. The oversize factor is a sweep axis, not a new assumption. Machine-readable: `tables/oversize_frontier.csv`; figure: `figures/oversize_frontier.png`.

| scenario | factor | installed mass | time to +1 cell | additional cells at year 40 |
|---|---:|---:|---:|---:|
| terrestrial_rehearsal | ×1 | 206.7 t | 9.25 yr | +0.93 |
| terrestrial_rehearsal | ×1.25 | 257.1 t | 8.25 yr | +1.16 |
| terrestrial_rehearsal | ×1.5 | 307.5 t | 7.75 yr | +1.40 |
| terrestrial_rehearsal | ×2 | 408.3 t | 6.75 yr | +1.86 |
| lunar_vitamin_bridge | ×1 | 216.7 t | 11.25 yr | +1.29 |
| lunar_vitamin_bridge | ×1.25 | 269.7 t | 10.00 yr | +1.62 |
| lunar_vitamin_bridge | ×1.5 | 322.6 t | 9.25 yr | +1.94 |
| lunar_vitamin_bridge | ×2 | 428.5 t | 8.00 yr | +2.59 |
| moon_asteroid_network | ×1 | 185.5 t | 22.75 yr | +11.55 |
| moon_asteroid_network | ×1.25 | 230.6 t | 21.75 yr | +14.43 |
| moon_asteroid_network | ×1.5 | 275.8 t | 21.00 yr | +17.32 |
| moon_asteroid_network | ×2 | 366.0 t | 20.00 yr | +23.09 |

Minimum mass is not time-optimal: oversizing the lunar-bridge seed by 2x cuts the first reproduction from 11.25 to 8.0 years. Returns diminish along the axis, and mass-optimal versus time-optimal designs are different points on this frontier.

## Ensemble diagnostics (r4.1)

Per-draw failure reasons, top binding constraints among feasible draws, and Spearman rank sensitivity of the named multipliers (machine-readable: `tables/diagnostics_histograms.csv`, `tables/ensemble_sensitivity.csv`):

- **terrestrial_rehearsal**: failures — autonomy_threshold 77, lp_infeasible 40; top binding — element:Cu 25, element:Cr 15, element:C 13, element:Fe 7.
- **lunar_vitamin_bridge**: failures — autonomy_threshold 54, lp_infeasible 20; top binding — element:C 32, element:Ni 30, element:Cu 29, element:Cr 13.
- **lunar_strict**: failures — lp_infeasible 167, autonomy_threshold 33; top binding — n/a.
- **moon_asteroid_network**: failures — autonomy_threshold 13; top binding — element:dopants 62, throughput:refining 58, throughput:asteroid_transport 42, throughput:asteroid_mining 15.

The depreciation multiplier correlates *positively* with year-40 cell-equivalents (rho about +0.8 to +0.98) while shortening first passage: higher assumed sector depreciation forces the minimum-mass LP to install more service and feed capacity per cell, and that oversizing accelerates reproduction — the same mechanism the oversize frontier isolates deliberately. It is a within-model consequence of minimum-mass sizing, not a claim that wear helps.

## Strict-lunar infeasibility certificate (r4.1)

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
python scripts/run_fourth.py
pytest tests/test_fourth.py -q
```

Every generated table is derived from the same in-memory run. `outputs/fourth/MANIFEST.md` hashes the parameter file, implementation, runner, report, tables, and figures.
