# Orbital-AI scenario and closure-stack policy

This policy defines how a real company program may test the article's general
models without replacing their neutral basis. It applies to orbital-compute
cost, launch mass and cadence, vehicle power and thermal balance, hardware
life and qualification, communications, deployment growth, constellation
topology, debris exposure, repair and replacement, and physical-supply cases
explicitly connected to an orbital-AI roadmap.

## Canonical scenario stack

Use these tracks in this order:

1. `generic_reference` — the actor-neutral model and its declared
   `ASSUMPTION` ranges.
2. `independent_reference` — a commensurable independent study or observation.
   If units, denominators, architecture, or state do not match, publish
   `not_parameterizable` instead of synthesizing a trajectory.
3. `spacexai_disclosed_design` — dated quantities directly disclosed for AI1.
   This is a design point, not current operating capacity.
4. `spacexai_stated_aspiration` — dated near-term or long-run targets,
   displayed as deterministic axes and never sampled as empirical priors.
5. `spacexai_affiliate_hybrid` — a separately named completion case containing
   affiliate evidence or analyst assumptions. Every completed field identifies
   its legal entity, evidence class, transfer assumption, and uncertainty.

The registry may encode `hybrid_completion` within the disclosed or aspiration
track when a calculation requires missing inputs, but the displayed result
must say so. A result composed from company statements and assumptions cannot
be shortened to “the SpaceXAI case.”

## Evidence states and eligibility

The allowed claim states are:

- `observed_operation`: measured or directly reported operation in the stated
  environment and denominator;
- `demonstrated`: a bounded working system or mission, not scaled operation;
- `disclosed_design`: a published technical specification without commissioned
  capacity;
- `near_term_target`: a dated intended next-stage quantity;
- `long_run_aspiration`: a directional or scale target without demonstrated
  delivery;
- `regulatory_filing`: an application or notice, which is not authorization;
- `independent_study`: a technical comparison at its own declared boundary;
  and
- `ASSUMPTION` or `hybrid_completion`: analyst-supplied values needed to close
  a calculation.

Promote a record only when its source supports the exact state, unit,
denominator, environment, legal entity, and date. Keep peak versus average
power, nameplate versus delivered load, payload versus total mass, launched
versus commissioned capacity, annual flow versus installed stock, and
terrestrial versus space-qualified performance separate.

## Gap completion

Independent or analyst inputs may complete a named company case only when:

- the company-supplied fraction of the required parameter vector is published;
- every missing input retains its original evidence class and uncertainty;
- the scenario is explicitly labelled hybrid;
- the conclusion identifies whether company data or completion assumptions
  control the result; and
- equivalent completion rules are available to independent comparators.

Targets and company statements may set deterministic points or sensitivity
axes. They may not define success probabilities, Monte Carlo priors, or
achieved-performance distributions without independent observations.

## Display and accessibility

Keep the canonical order in tables, legends, captions, and generated metadata.
Neutral and independent references remain present and receive equal line
weight, contrast, marker prominence, and explanatory space. Use marker shape,
line pattern, labels, and table text as well as color. A named-company line
must not visually dominate or receive a favorable completion unavailable to
competitors.

Every result row includes `scenario_id`, `evidence_class`, `source_snapshot`,
`parameter_completeness`, and `boundary`. Every relevant simulation/output is
listed in `simulation_scenario_coverage.csv`, including explicit
`not_parameterizable` reasons.

## Actor-bounded closure stack

The closure matrix compares named legal entities across the 18 ordered layers
in `params/orbital_ai_scenario_registry.json`. Maturity is one of
`operational`, `demonstrated`, `under_development`, `stated_aspiration`, or
`no_evidence`. Each row keeps terrestrial/space status, demonstrated capacity,
target, missing dependencies, date, source class, common-control status, and
off-world reproductive closure separate.

Tesla is a separate public company. Its evidence may appear in the bounded
affiliate-hybrid ecosystem but never as a SpaceXAI-owned capability.
Relationship, transfer, qualification, availability, and control uncertainty
remain visible. The same rule applies to every partner or affiliate.

Publish the full matrix before summary measures. Evidence-weighted layer
breadth compares documented activity; it is not a physical-closure
percentage. Dependency-aware reproductive closure requires every
indispensable layer, its inputs, repair path, and capital-equipment ancestry
to be closed off-world. One missing minimum-cut dependency keeps closure false.
`no_evidence` follows the dated negative-evidence protocol and is not proof of
absence.

## Provenance, refresh, and exclusions

Every input records source date, locator, evidence class, unit, denominator,
state, direct-versus-derived status, permitted simulations, archived snapshot,
and SHA-256 hash. Mutable pages and filings are preserved in a dated evidence
snapshot. A disclosure change creates a new registry version; it does not
rewrite historical results.

Before every release:

1. repeat the named-program, first-party, regulatory, and independent-study
   search in the registry's declared comparison class;
2. update contextual claims and competitor rows without changing neutral
   assumptions merely because the market changed;
3. run the scenario-policy, provenance, artifact, external-link, and full
   publication checks; and
4. record exclusions: job advertisements, generic company-type inference,
   third-party rumor, brand affiliation without a disclosed relationship, and
   operation of purchased equipment as evidence of reproducing its upstream
   production chain.

Abstract numerical-method tests, generic digital-R&D equations, terrestrial
rehearsal diagnostics, and physical-closure experiments without a published
company architecture remain actor-neutral. Do not add a company line for
visual symmetry alone.
