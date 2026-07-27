# SpaceX orbital-AI and Starship aspirations — model provenance

Primary source: [SpaceX EU Prospectus, approved 2026-06-05](https://content.spacex.com/cms-assets/FINAL_Documents%20and%20Updates/SpaceX%20-%20EU%20Prospectus%20%28Approved%20by%20Bafin%29%20-%20June%205%2C%202026.pdf)

Current-product cross-check: [SpaceX Starmind AI1](https://www.spacex.com/spacexai/starmind)

Accessed: 2026-07-27

Source class: `company_statement` for company targets; `ASSUMPTION` for
analyst-selected favorable values.

This file records the inputs and arithmetic used by the model's deterministic
`starmind_ai1_aspirational` sensitivity. It is deliberately not a forecast,
baseline, or Monte Carlo prior. A company target is evidence of intent, not
evidence that the cost, cadence, reliability, or regulatory conditions have
been achieved.

## Company numbers used

| quantity | company statement | model value | status |
|---|---:|---:|---|
| historical launch cost | $18,500/kg | comparison basis | prospectus pp. 63, 70, 137 |
| aimed launch-cost reduction | 99% or more | $185/kg | exact 99% ceiling: `$18,500 × 0.01`; target, not quoted customer price |
| long-term compute efficiency | 100 kW/t | 10 kg/kW | scale assumption in prospectus p. 82 |
| V3 reusable payload | 100 t | 100 t/launch | design target, pp. 71–72 |
| possible future V4 payload | 200 t | 200 t/launch | future target, pp. 71–72 |
| long-term orbital-compute deployment | up to 100 GW/year | 100 GW/year | target, pp. 82, 97 |

The later AI1 product page discloses **70 kW/t**, not 100 kW/t. Thus the
prospectus scale assumption is 43% above the current disclosed design
efficiency; equivalently, AI1 is 30% below the target.

## Favorable values that are not company specifications

| quantity | best-case value | provenance |
|---|---:|---|
| space qualification multiplier | 1.2× | `ASSUMPTION`; favorable bound of the existing model range |
| compute-hardware life | 7 years | `ASSUMPTION`; favorable bound of the existing model range |
| compute utilization | 0.95 | `ASSUMPTION`; favorable bound of the existing model range |

SpaceX does not publish achieved AI1 values for these three quantities. The
prospectus reports high Starlink network uptime, but communications-network
uptime is not evidence of AI-compute spacecraft availability; the prospectus
also says AI processors may have higher failure rates and require extensive
testing.

## Scale arithmetic

At 100 GW/year and 100 kW/t:

- deployed mass is `100,000,000 kW / 100 kW/t = 1,000,000 t/year`;
- V3 requires 10,000 full 100-t payload launches/year, or 27.4/day;
- a possible 200-t V4 requires 5,000 launches/year, or 13.7/day;
- 120-kW-average AI1-class spacecraft imply about 833,333 spacecraft/year;
- at $185/kg, launch cost alone is `$185 billion/year`.

At the currently disclosed 70 kW/t, the same 100-GW flow requires about
1.43 million tonnes and 14,286 full V3 launches per year.

These are unit conversions, not cadence predictions. The prospectus itself
describes roughly one million tonnes/year and thousands of launches/year. It
also says full and rapid reuse of both stages is required for the intended
cost and cadence, while upper-stage recovery/reflight and in-orbit propellant
transfer remain key planned unlocks in the document.

## Feasibility gates kept outside the point estimate

- launch/landing turnaround infrastructure and maintenance needed to sustain
  14–27 full-payload launches per day;
- realized upper-stage reuse, refurbishment burden, fleet size, propellant,
  range capacity, weather resilience, and launch licensing;
- whole-spacecraft seven-year reliability, 95% useful compute utilization,
  accelerator radiation behavior, repair/replacement, and obsolescence;
- spectrum, domestic and international approvals, collision avoidance, debris
  mitigation, and constellation replenishment for a potentially enormous fleet;
- networking service, ground operations, insurance, program NRE, and financing;
- improvement in the terrestrial counterfactual, including cheaper generation,
  chips, cooling, permitting, and data-center construction.

The prospectus expressly identifies approvals and spectrum as dependencies and
warns that improvements in terrestrial energy could diminish the orbital
architecture's relative advantage. The best case is therefore a useful
boundary—what must all go right—not a probability-weighted forecast.
