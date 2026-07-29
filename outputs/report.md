# RSI model run report — 2026-07-29

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

| set | environment | g @10yr | g @30yr | balanced dbl (yr) | aggregate dbl (yr) | last binding sector |
|---|---|---|---|---|---|---|
| conservative | leo | -0.015 | -0.023 | never | never | mining |
| conservative | lunar | +0.008 | -0.023 | never | never | electronics |
| conservative | mars | -0.064 | -0.064 | never | never | electronics |
| central | leo | +0.021 | +0.010 | never | never | mining |
| central | lunar | +0.050 | +0.016 | 4.2 | 4.2 | electronics |
| central | mars | -0.023 | -0.023 | 13.2 | 13.2 | electronics |
| optimistic | leo | +0.064 | +0.051 | 9.0 | 9.0 | mining |
| optimistic | lunar | +0.085 | +0.047 | 2.5 | 2.5 | electronics |
| optimistic | mars | +0.007 | +0.007 | 4.8 | 4.8 | electronics |

## Monte Carlo (anchored ranges + common-cause shocks)

- [central/lunar] expanding @30yr: 22/40 = 0.55 (95% CI 0.40-0.69) | sustained [25-30]: 6/40 | pre-shock alloc endpoint: 22/40 | balanced dbl: 4.5 yr (IQR 4.2-5.2, n=33) | aggregate dbl: 4.5 yr (IQR 3.8-5.0, n=38) | λ@30 med 2.72 | binds: electronics 96%, power 4%, machine_tools 0%
  (shocks/run: 17.1; q jitter sigma=0.1, ASSUMPTION-class)
- [conservative/lunar] expanding @30yr: 6/40 = 0.15 (95% CI 0.07-0.29) | sustained [25-30]: 2/40 | pre-shock alloc endpoint: 7/40 | balanced dbl: 11.5 yr (IQR 8.5-13.8, n=10) | aggregate dbl: 8.1 yr (IQR 7.6-8.7, n=10) | λ@30 med 0.78 | binds: electronics 90%, power 5%, repair 4%
  (shocks/run: 17.1; q jitter sigma=0.1, ASSUMPTION-class)
- [central/mars] expanding @30yr: 5/40 = 0.12 (95% CI 0.05-0.26) | sustained [25-30]: 1/40 | pre-shock alloc endpoint: 8/40 | balanced dbl: 9.0 yr (IQR 9.0-10.1, n=3) | aggregate dbl: 9.2 yr (IQR 9.0-11.2, n=17) | λ@30 med 0.43 | binds: electronics 55%, power 45%
  (shocks/run: 24.6; q jitter sigma=0.1, ASSUMPTION-class)

## Minimum-cut-set analysis

**central/lunar** (horizon 30 yr, 74 simulations)
- baseline self-expanding: yes
- no import cut set prevents self-expansion by the horizon (imports accelerate but are not load-bearing at these central values)
- indispensable sectors (capacity knockout unrecoverable): power, mining, refining, robotics, machine_tools, electronics, thermal, transport, repair

**central/leo** (horizon 30 yr, 138 simulations)
- baseline self-expanding: yes
- no import cut set prevents self-expansion by the horizon (imports accelerate but are not load-bearing at these central values)
- indispensable sectors (capacity knockout unrecoverable): power, mining, refining, robotics, machine_tools, electronics, thermal, transport


## Figures

![capacity_by_set_lunar](figures/capacity_by_set_lunar.png)

![delta_decomposition](figures/delta_decomposition.png)

![electronics_cutoff](figures/electronics_cutoff.png)

![stockpiles_cutoff](figures/stockpiles_cutoff.png)

![survival](figures/survival.png)

![import_decay_sweep](figures/import_decay_sweep.png)

## Parameter provenance (central/lunar)

| quantity | value | source_class | anchor | note |
|---|---|---|---|---|
| delta.wear[power] | 0.0099 | peer_reviewed | delta.wear_space_solar | GEO telemetry, 11 sats (2018); GaAs low, Si high |
| delta.wear[mining] | 0.0600 | ASSUMPTION | — | environments.yaml |
| delta.wear[refining] | 0.0400 | ASSUMPTION | — | environments.yaml |
| delta.wear[robotics] | 0.0700 | ASSUMPTION | — | environments.yaml |
| delta.wear[machine_tools] | 0.0400 | ASSUMPTION | — | environments.yaml |
| delta.wear[electronics] | 0.0200 | ASSUMPTION | — | environments.yaml |
| delta.wear[thermal] | 0.0500 | ASSUMPTION | — | environments.yaml |
| delta.wear[transport] | 0.0500 | ASSUMPTION | — | environments.yaml |
| delta.wear[repair] | 0.0300 | ASSUMPTION | — | environments.yaml |
| delta.wear[recycling] | 0.0300 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[power] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[mining] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[refining] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[robotics] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[machine_tools] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[electronics] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[thermal] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[transport] | 0.0200 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[repair] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.catastrophic[recycling] | 0.0040 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[power] | 0.0050 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[mining] | 0.0050 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[refining] | 0.0050 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[robotics] | 0.0100 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[machine_tools] | 0.0100 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[electronics] | 0.0600 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[thermal] | 0.0050 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[transport] | 0.0050 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[repair] | 0.0100 | ASSUMPTION | — | environments.yaml |
| delta.obsolescence[recycling] | 0.0050 | ASSUMPTION | — | environments.yaml |
| delta.logistics[power] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[mining] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[refining] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[robotics] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[machine_tools] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[electronics] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[thermal] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[transport] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[repair] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| delta.logistics[recycling] | 0.0291 | ASSUMPTION | delta.logistics_penalty_space | internal repair-chain overhead as capacity tax; UNANCHORED |
| q_scale[power] | 1.0000 | ASSUMPTION | — | environments.yaml |
| q_scale[mining] | 1.0000 | ASSUMPTION | — | environments.yaml |
| q_scale[refining] | 1.0000 | ASSUMPTION | — | environments.yaml |
| q_scale[robotics] | 1.0000 | ASSUMPTION | — | environments.yaml |
| q_scale[machine_tools] | 0.7000 | ASSUMPTION | — | environments.yaml |
| q_scale[electronics] | 0.1732 | ASSUMPTION | closure.space_electronics_q_scale | Fraction of the electronics sector's output mix producible off-world (the vitamin gap). UNANCHORED — no published measurement exists. Bounding argument: UPPER ~0.3 because advanced-node logic/memory (EUV lithography, metrology, ultra-pure feedstocks — the Section 13 residual chokepoint) is not locally closable in this scenario class, and boards/passives/power electronics are a minority of electronics value; LOWER ~0.1 because thick-film PCB, wiring, and discrete/power devices are plausibly closable with generic machine tools. THE single most results-driving number in Part I — see ROADMAP. |
| q_scale[thermal] | 1.0000 | ASSUMPTION | — | environments.yaml |
| q_scale[transport] | 0.9000 | ASSUMPTION | — | environments.yaml |
| q_scale[repair] | 1.0000 | ASSUMPTION | — | environments.yaml |
| q_scale[recycling] | 0.9000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[power] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[mining] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[refining] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[robotics] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[machine_tools] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[electronics] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[thermal] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[transport] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[repair] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.wear[recycling] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[power] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[mining] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[refining] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[robotics] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[machine_tools] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[electronics] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[thermal] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[transport] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[repair] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.catastrophic[recycling] | 0.5000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[power] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[mining] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[refining] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[robotics] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[machine_tools] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[electronics] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[thermal] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[transport] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[repair] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.obsolescence[recycling] | 1.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[power] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[mining] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[refining] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[robotics] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[machine_tools] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[electronics] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[thermal] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[transport] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[repair] | 0.0000 | ASSUMPTION | — | environments.yaml |
| salvage.logistics[recycling] | 0.0000 | ASSUMPTION | — | environments.yaml |
| A matrix (all entries) | — | ASSUMPTION | — | assumptions.yaml set 'central' |
| q (incl. environment q_scale) | — | ASSUMPTION | — | assumptions.yaml + environments.yaml |
| import profile/budget/decay | — | ASSUMPTION | — | assumptions.yaml + environments.yaml |
| repair efficiency/spares | — | ASSUMPTION | — | assumptions.yaml |
| recycling recovery/profile/opex | — | ASSUMPTION | — | assumptions.yaml |
| stockpile sizes/shelf life | — | ASSUMPTION | — | assumptions.yaml |
| shock rates/fractions/groups | — | ASSUMPTION | — | environments.yaml |
