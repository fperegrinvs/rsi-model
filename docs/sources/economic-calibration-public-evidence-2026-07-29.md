# Economic-calibration public-evidence baseline

**As of:** 2026-07-29

**Purpose:** extraction and missingness record for the symmetric compute
economics calibration

**Result:** the public record constrains selected scenario axes but fails every
correlation holdout and promotes no model parameter.

The public record is not an audited project ledger. This baseline records
available observations and all missing fields so they cannot be silently
completed with assumptions.

## Evidence-package boundary

| Package | Public evidence | Decisive missing evidence |
|---|---|---|
| E01 equal-workload benchmark | Company and paper claims describe compute power or cost-per-token concepts | Same model, precision, batch/sequence, memory, accepted output, latency, availability, retries, topology, and measured energy on Earth and in orbit |
| E02 space reliability | NASA has historical spacecraft mortality and reliability datasets, including censored operating lives | Architecture-matched orbital AI hardware qualification, failure, repair, downtime, retirement, insurance, and residual-value history |
| E03 links and ground | The FCC accepted SpaceX's orbital-data-center application for filing; geometry and proposed spectrum are identifiable | Operating link budget, delivered workload throughput, outages, latency distribution, gateway capex, and recurring cost |
| E04 thermal, mass, and power | Starmind AI1 discloses 120 kW average compute, a 150 kW solar array, 110 m² radiator area, and 70 kW/t vehicle-level efficiency | Heat duty, rejection temperature, radiator mass, pumping power, shielding, redundancy, degradation, failures, and full BOM |
| E05 Earth buildout | EIA reports 2025 U.S. commercial electricity at 13.41¢/kWh and industrial electricity at 8.62¢/kWh; regional variation is large | Matched data-center project land, water, queue, permits, construction cost, labor, PUE, availability, cancellation, and retirement records |
| E06 cash flow | Public filings describe strategy, selected commitments, and consolidated company accounts | Project-architecture-period commitments, paid amounts, financing, insurance, operating revenue/cost, failures, repairs, disposal, and residual proceeds |

## Primary sources

- [NASA satellite mortality study](https://ntrs.nasa.gov/citations/20150008736)
- [NASA on-orbit spacecraft reliability study](https://ntrs.nasa.gov/citations/19790004282)
- [FCC Public Notice DA 26-113](https://docs.fcc.gov/public/attachments/DA-26-113A1.pdf)
- [U.S. EIA electricity prices](https://www.eia.gov/energyexplained/electricity/prices-and-factors-affecting-prices.php)
- [SpaceX Starmind AI1 product record](https://www.spacex.com/starmind)
- repository source records:
  `docs/sources/starmind-ai1-2026-07-27.md`,
  `docs/sources/spacexai-economic-thesis-2026-07-29.md`, and
  `params/orbital_ai_scenario_registry.json`.

## Calibration disposition

All five declared correlation groups receive a chronological holdout status of
`fail`, because the public records do not contain the required joint
architecture-period observations. All forty bound parameters retain
`ASSUMPTION` status. Zero-valued cash-flow amounts in the generated gap ledger
are missing-data sentinels, not observations of zero cost or revenue; each row
is labeled `record_status=evidence_missing`.

This is a completed negative calibration against the declared public evidence
boundary. It does not satisfy the stronger promotion rule, replace a
confidential audited ledger, or show that empirical calibration is
impossible.
