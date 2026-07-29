# External sources

Primary/secondary sources kept locally for citation stability. Each entry:
what it is, where it came from, what this project uses it for, and its
source_class under the epistemic rules.

- **`../../params/claim_provenance.yaml`** — authoritative claim-level
  register for every non-`ASSUMPTION` anchor and the load-bearing [S27]
  strategy claims. Each record carries the modeled endpoint, units, exact
  author or organization, title, date, page/table/section or slide,
  persistent URL/DOI or content-hashed repository snapshot, extracted value,
  transformation, source class, and verification status. The deterministic
  public rendering is `../../outputs/tables/claim_provenance.csv`; tests
  reject missing records, source-class or endpoint drift, collective [S36]
  support, and unpinned SEC claims.

- **situational-awareness-aschenbrenner-2024-06.pdf** — Leopold Aschenbrenner,
  *Situational Awareness: The Decade Ahead* (June 2024, 165 pp.), retrieved
  2026-07-27 from https://situational-awareness.ai. Source_class: reporting /
  analyst estimate (independent essay; back-of-envelope calculations
  documented in its appendix). Used for: the responsive-Earth gas floor
  (`earth.gas_power_price_floor_kwh`, `earth.gas_power_capex_per_kw` in
  `params/anchors.yaml`, ch. IIIa); the external cross-checks in
  `docs/PART_III_HYPOTHESES.md` (terrestrial resolution of the power wall,
  CoWoS/HBM chokepoints, fast-takeoff as the competing assumption class); the
  non-saturation branch and capital-mobilization reference classes in
  `docs/PART_IV_SPECULATIVE.md`.

- **orbital-compute-calibration-2026-07-27.md** — structured extraction from
  the post-IPO orbital-data-center studies cited as [S39–S44]. Source_class:
  mixed, recorded per source (technical preprint, peer-reviewed conference
  paper, NASA technical memorandum, and policy report). Used for: the
  architecture-specific mass envelopes, full thermal-system cross-check,
  launch-plus-build inequality, platform-life qualification, and
  inference-versus-training boundary in Part II. It records evidence and
  arithmetic but does not change the current model inputs.

- **starmind-ai1-2026-07-27.md** and
  **spacex-ai-aspirations-2026-06.md** — direct SpaceX product specifications
  and the separately quarantined company-target best case. Source_class:
  `company_statement` for disclosed values and targets, `ASSUMPTION` for
  derived or favorable unpublished values. Used for: the current AI1 scenario,
  the deterministic $185/kg + 100 kW/t aspiration case, and the accompanying
  launch-cadence feasibility audit in Part II.

- **spacexai-economic-thesis-2026-07-29.md** — dated first-party boundary for
  SpaceX's cost-per-token framework, SEC admissions, roadshow time-to-power
  thesis, AI1 missing quantities, and Musk's January 2026 prediction.
  Source_class: `company_statement` for company filings and specifications
  and `personal_statement` for the forecast. Used for the company-only,
  explicitly completed hybrid, accepted-output, schedule, and threshold
  comparisons in Part II.

- **orbital-ai-landscape-2026-07-28.md** — dated first-party and regulatory
  comparison of SpaceXAI, Google/Planet Project Suncatcher, Starcloud, and
  Blue Origin Project Sunrise, including the Tesla legal-entity boundary and
  negative-evidence protocol. Source_class: mixed company statement,
  regulatory filing, and analyst synthesis. Its SHA-256 hash is pinned in
  `../../params/orbital_ai_scenario_registry.json`; every release repeats the
  competitor search and creates a new registry version when the record changes.

- **publication-venue-requirements-2026-07-29.md** — dated first-party
  conformance snapshot for the selected Acta Astronautica, Space Policy, and
  Astropolitics routes. It records numeric limits, file and reference rules,
  and the unresolved conflict between Astropolitics' two live peer-review
  statements. Source_class: `publisher_instructions`.

- **process-closure-public-evidence-2026-07-29.md** — NASA, NIST, USGS, and
  portfolio evidence boundary for the generated typed industrial dependency
  graph. It supports a negative evaluation—eight failed closure gates—and
  forbids filling missing yields, purity, tool life, fleet, or parent-tool
  records from the aggregate model.

- **economic-calibration-public-evidence-2026-07-29.md** — primary-source
  extraction and missingness record for all six calibration packages. It
  records the available NASA reliability, FCC regulatory, Starmind design,
  EIA energy-price, and filing evidence while preserving five failed
  correlation holdouts and zero empirical parameter promotions.

The r4.0 provenance audit deliberately reclassified reporting-derived model
bands as `ASSUMPTION` when the cited material did not directly support both
modeled endpoints and their transformation. Contextual reporting remains
useful for bounding scenarios; it no longer confers a stronger source class
on an analyst-constructed distribution.

- **lunar-surface-orbit-architecture-2026-07-27.md** — evidence boundary for
  endogenous orbital-debris feedback, low-lunar-orbit breakup behavior,
  lunar-surface resources and hazards, NRHO as a service/gateway geometry,
  and Sun-synchronous versus heliocentric terminology. Source_class: mixed
  peer-reviewed and NASA technical material. Used for: the qualitative
  lunar surface–orbit partition and the integrated model requirements;
  it adds no current numerical inputs.

See also `../transcripts/` for podcast/interview transcripts with per-file
provenance headers.

**Public-repository note.** The PDF archived here is a third-party
copyrighted work and is excluded from the public repository (.gitignore);
obtain it from https://situational-awareness.ai. The Moonshots #266 full
transcript in `../transcripts/` is likewise excluded; see the episode at
https://www.youtube.com/watch?v=kPSLLeccrik. Local archives exist for
citation stability only.
