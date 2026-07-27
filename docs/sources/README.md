# External sources

Primary/secondary sources kept locally for citation stability. Each entry:
what it is, where it came from, what this project uses it for, and its
source_class under the epistemic rules.

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
  arithmetic but does not change the r3.5 model inputs.

- **starmind-ai1-2026-07-27.md** and
  **spacex-ai-aspirations-2026-06.md** — direct SpaceX product specifications
  and the separately quarantined company-target best case. Source_class:
  `company_statement` for disclosed values and targets, `ASSUMPTION` for
  derived or favorable unpublished values. Used for: the current AI1 scenario,
  the deterministic $185/kg + 100 kW/t aspiration case, and the accompanying
  launch-cadence feasibility audit in Part II.

- **lunar-surface-orbit-architecture-2026-07-27.md** — evidence boundary for
  endogenous orbital-debris feedback, low-lunar-orbit breakup behavior,
  lunar-surface resources and hazards, NRHO as a service/gateway geometry,
  and Sun-synchronous versus heliocentric terminology. Source_class: mixed
  peer-reviewed and NASA technical material. Used for: the qualitative
  lunar surface–orbit partition and the Fourth Edition model requirements;
  it adds no r3.5 numerical inputs.

See also `../transcripts/` for podcast/interview transcripts with per-file
provenance headers.

**Public-repository note.** The PDF archived here is a third-party
copyrighted work and is excluded from the public repository (.gitignore);
obtain it from https://situational-awareness.ai. The Moonshots #266 full
transcript in `../transcripts/` is likewise excluded; see the episode at
https://www.youtube.com/watch?v=kPSLLeccrik. Local archives exist for
citation stability only.
