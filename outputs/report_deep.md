# RSI model run report — 2026-07-27

All replication/doubling times below are MODEL OUTPUTS. No single trajectory is
"the" answer: results span assumption sets (conservative/central/optimistic,
`params/assumptions.yaml`) and Monte Carlo over anchored ranges
(`params/anchors.yaml`). Structural coefficients are ASSUMPTION-class.

## Deterministic sweeps (central anchor values)

| set | environment | g @10yr | g @30yr | doubling (yr) | last binding sector |
|---|---|---|---|---|---|
| conservative | leo | -0.002 | -0.010 | never | mining |
| conservative | lunar | +0.007 | -0.023 | never | electronics |
| conservative | mars | -0.064 | +0.042 | never | electronics |
| central | leo | +0.041 | +0.031 | 15.0 | mining |
| central | lunar | +0.049 | +0.016 | 4.8 | electronics |
| central | mars | -0.023 | +0.074 | never | electronics |
| optimistic | leo | +0.096 | +0.069 | 6.2 | mining |
| optimistic | lunar | +0.084 | +0.047 | 3.0 | electronics |
| optimistic | mars | +0.007 | +0.104 | 4.8 | electronics |

## Monte Carlo (anchored ranges + common-cause shocks)

- [conservative/leo] expanding @30yr: 48/400 = 0.12 (95% CI 0.09-0.16) | doubling: never | binds: mining 72%, electronics 28%
  (shocks/run: 6.5; q jitter sigma=0.1, ASSUMPTION-class)
- [conservative/lunar] expanding @30yr: 41/400 = 0.10 (95% CI 0.08-0.14) | doubling: 9.6 yr (IQR 8.0-11.8, n=74) | binds: electronics 82%, repair 15%, machine_tools 2%
  (shocks/run: 17.0; q jitter sigma=0.1, ASSUMPTION-class)
- [conservative/mars] expanding @30yr: 85/400 = 0.21 (95% CI 0.18-0.26) | doubling: never | binds: electronics 86%, power 8%, machine_tools 4%
  (shocks/run: 24.9; q jitter sigma=0.1, ASSUMPTION-class)
- [central/leo] expanding @30yr: 364/400 = 0.91 (95% CI 0.88-0.93) | doubling: 16.0 yr (IQR 14.5-17.5, n=369) | binds: mining 65%, electronics 35%
  (shocks/run: 6.1; q jitter sigma=0.1, ASSUMPTION-class)
- [central/lunar] expanding @30yr: 257/400 = 0.64 (95% CI 0.59-0.69) | doubling: 5.0 yr (IQR 4.2-6.0, n=393) | binds: electronics 97%, machine_tools 3%
  (shocks/run: 17.0; q jitter sigma=0.1, ASSUMPTION-class)
- [central/mars] expanding @30yr: 247/400 = 0.62 (95% CI 0.57-0.66) | doubling: 10.8 yr (IQR 8.8-13.2, n=127) | binds: electronics 89%, power 7%, machine_tools 4%
  (shocks/run: 24.6; q jitter sigma=0.1, ASSUMPTION-class)
- [optimistic/leo] expanding @30yr: 400/400 = 1.00 (95% CI 0.99-1.00) | doubling: 6.2 yr (IQR 5.8-6.5, n=400) | binds: mining 60%, electronics 40%
  (shocks/run: 6.2; q jitter sigma=0.1, ASSUMPTION-class)
- [optimistic/lunar] expanding @30yr: 396/400 = 0.99 (95% CI 0.97-1.00) | doubling: 3.0 yr (IQR 2.8-3.2, n=400) | binds: electronics 98%, machine_tools 2%
  (shocks/run: 16.8; q jitter sigma=0.1, ASSUMPTION-class)
- [optimistic/mars] expanding @30yr: 356/400 = 0.89 (95% CI 0.86-0.92) | doubling: 5.0 yr (IQR 4.8-6.8, n=376) | binds: electronics 90%, power 6%, machine_tools 4%
  (shocks/run: 24.7; q jitter sigma=0.1, ASSUMPTION-class)

## Minimum-cut-set analysis

**central/lunar** (horizon 30 yr, 74 simulations)
- baseline self-expanding: yes
- no import cut set prevents self-expansion by the horizon (imports accelerate but are not load-bearing at these central values)
- indispensable sectors (capacity knockout unrecoverable): power, mining, robotics, machine_tools, electronics, thermal, transport, repair

**central/leo** (horizon 30 yr, 138 simulations)
- baseline self-expanding: yes
- no import cut set prevents self-expansion by the horizon (imports accelerate but are not load-bearing at these central values)
- indispensable sectors (capacity knockout unrecoverable): power, mining, robotics, machine_tools, electronics, thermal, transport


## Cut-set fatality over the MC ensemble

Cut sets appear only near the feasibility margin, so central-value
cut analysis understates dependency risk. Over sampled anchors
(no shocks; structural question only):

**central/lunar** (n=40, horizon 30 yr): P(baseline expands) = 0.85
- P(fatal | baseline ok) cutting electronics: 0.09
- P(fatal | baseline ok) cutting ALL import lines: 0.09

**central/leo** (n=40, horizon 30 yr): P(baseline expands) = 0.90
- no candidate cut fatal in any sampled draw

**central/mars** (n=40, horizon 30 yr): P(baseline expands) = 1.00
- P(fatal | baseline ok) cutting electronics: 0.75
- P(fatal | baseline ok) cutting ALL import lines: 0.75

**optimistic/lunar** (n=40, horizon 30 yr): P(baseline expands) = 1.00
- P(fatal | baseline ok) cutting electronics: 0.05
- P(fatal | baseline ok) cutting ALL import lines: 0.05

## Figures

![survival_deep_lunar](figures/survival_deep_lunar.png)

![survival_deep_central](figures/survival_deep_central.png)

![import_decay_sweep_deep](figures/import_decay_sweep_deep.png)

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
| A matrix (all entries) | — | ASSUMPTION | — | assumptions.yaml set 'central' |
| q (incl. environment q_scale) | — | ASSUMPTION | — | assumptions.yaml + environments.yaml |
| import profile/budget/decay | — | ASSUMPTION | — | assumptions.yaml + environments.yaml |
| repair efficiency/spares | — | ASSUMPTION | — | assumptions.yaml |
| recycling recovery/profile/opex | — | ASSUMPTION | — | assumptions.yaml |
| stockpile sizes/shelf life | — | ASSUMPTION | — | assumptions.yaml |
| shock rates/fractions/groups | — | ASSUMPTION | — | environments.yaml |

## Allocation-policy robustness (paired draws, shocks off)

**central/lunar** (n=30): myopic: 22/30 expanding | horizon: 22/30 expanding | aggregate: 0/30 expanding
**central/leo** (n=30): myopic: 28/30 expanding | horizon: 28/30 expanding | aggregate: 0/30 expanding

Receding-horizon lookahead reproduces the myopic maximin; the aggregate-growth-with-floor policy collapses. The maximin allocation is load-bearing, not incidental.


## Global sensitivity (Spearman rho of anchor draw vs g@30yr)

central/lunar, n=300, null band ~ +/-0.11 (wider under multiplicity):

- `closure.space_electronics_q_scale`: rho_g30 = +0.78, rho_expand = +0.50
- `delta.logistics_penalty_space`: rho_g30 = -0.57, rho_expand = -0.57
- `earth.power_price_kwh`: rho_g30 = -0.18, rho_expand = -0.18
- `earth.wacc`: rho_g30 = +0.12, rho_expand = +0.08
- `earth.gas_power_price_floor_kwh`: rho_g30 = +0.11, rho_expand = +0.09
- `delta.catastrophic_leo`: rho_g30 = -0.11, rho_expand = -0.07
- `compute.utilization_leo`: rho_g30 = +0.10, rho_expand = +0.05
- `compute.space_qual_multiplier`: rho_g30 = +0.10, rho_expand = +0.08
