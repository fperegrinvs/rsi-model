# SpaceX Starmind AI1 — captured architecture disclosures

Source: <https://www.spacex.com/spacexai/starmind>

Accessed: 2026-07-27

Source class: `company_statement`

This file records the numeric disclosures used by the model's conditional
`starmind_ai1` scenario. It is a provenance snapshot, not evidence that the
planned vehicle has achieved the stated performance, cost, reliability, or
deployment schedule.

## Numeric disclosures

| quantity | disclosed value | model role |
|---|---:|---|
| deployed height | 20 m | context only |
| wingspan | 70 m | context only |
| compute payload | 150 kW peak / 120 kW average | average value sets the delivered-load denominator; peak is context |
| vehicle efficiency | 70 kW/tonne | used to constrain aggregate vehicle mass, with a peak-vs-average interpretation range |
| deployable liquid radiator | 110 m² | context only; no areal mass or cost disclosed |
| solar array | 150 kW | used with 120 kW average compute to set a 1.25 design power ratio |
| solar power density | 250 W/m² | context only |

## Qualitative disclosures not converted into numeric inputs

- Redundant pumped thermal loops and integrated micrometeoroid/orbital-debris
  shielding are disclosed, but their mass, cost, and reliability effects are
  not.
- The architecture uses high-speed laser links through Starlink, but link
  equipment mass, service cost, delivered bandwidth, and availability are not
  disclosed.
- SpaceX describes sun-synchronous operation and continuous solar power. The
  scenario retains the generic LEO utilization range because continuous
  illumination does not establish achieved compute availability.
- SpaceX describes modular, vendor-agnostic compute and future processor
  upgrades. The model retains its existing component-specific lives; it does
  not add an unquantified modularity or residual-value credit.
- The page describes planned factory output and Starship deployment but gives
  neither satellite capex nor a realized Starship launch price. Existing cost
  anchors and launch-price sweeps therefore remain in force.

## Derived mass range

The page does not state whether the `70 kW/tonne` numerator is peak or average
compute power:

- average-power interpretation: `1000 / 70 = 14.286 kg` per average kW;
- peak-power interpretation: `(150 / 70 tonnes) / 120 kW = 17.857 kg` per
  average kW.

The scenario samples this 14.286–17.857 kg/kW range and labels it
`ASSUMPTION`, while retaining the underlying direct disclosures as
`company_statement`.

The separate `starmind_ai1_aspirational` sensitivity instead uses the older
100 kW/t long-term assumption and $185/kg launch-cost target recorded in
`spacex-ai-aspirations-2026-06.md`. It does not overwrite this current-product
scenario or enter its Monte Carlo.
