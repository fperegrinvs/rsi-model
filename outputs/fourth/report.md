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

## Reproducibility

```bash
python scripts/run_fourth.py
pytest tests/test_fourth.py -q
```

Every generated table is derived from the same in-memory run. `outputs/fourth/MANIFEST.md` hashes the parameter file, implementation, runner, report, tables, and figures.
