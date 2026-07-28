# Declared off-world industrial direction, technical coordination, and control

r4.0 strategy and governance case-study draft

## Abstract

Public materials document a broad off-world industrial portfolio spanning
orbital compute, internal semiconductor production, lunar manufacturing and
energy, in-space manufacturing, and asteroid-resource concepts. They do not
establish a coordinated recursive-closure program. We test three matched
hypotheses: H0, adjacent projects sharing ownership, finance, branding,
suppliers, and ordinary commercial motives; H1, coordinated capability with
shared technical interfaces, binding milestones, and joint resource
allocation; and H2, H1 plus an explicit reproduction and closure roadmap.
The evidence strongly supports declared portfolio direction, provides limited
support for coordinated implementation, and does not establish H2. We then
translate the technical model into a governance threat register covering
accidental, cyber, insider, owner-incentive, jurisdictional, common-mode,
autonomy, and source failures. Normal, delayed, and lost-link authority is
specified, with build authorization, rate limits, compartmentalization,
verification, rollback, safe-hold, and independent audit mapped to physical
sector and source states. Every control remains unvalidated. Corporate
direction does not validate technical feasibility, and a requirements model
does not constitute a safety case.

## Keywords

space policy; industrial strategy; autonomous systems; governance; safety;
corporate evidence

## Highlights

- Public evidence supports portfolio direction but not recursive closure.
- Matched hypotheses prevent shared ownership from proving coordination.
- Lost-link authority halts new growth while preserving immediate safety.
- Every proposed governance control remains physically unvalidated.

## 1. Proposition boundary

This case study addresses:

- P4a: whether public evidence supports deliberate off-world industrial
  direction;
- P4b: whether recursive industrial closure is an explicit coordinated
  objective;
- governance requirements that follow if autonomous capacity can expand.

It does not use strategic intent as evidence for technical feasibility or
economic competitiveness. The technical and economics papers are independent
conditional analyses.

## 2. Matched hypotheses

H0 predicts adjacent projects under common ownership. Shared finance,
branding, suppliers, data, bilateral interfaces, commercial reliability,
supply security, recycling, and radiation-hardening are all compatible with
H0.

H1 requires evidence that is harder for H0 to explain: shared systems
engineering, common architecture documents, binding cross-program milestones,
joint resource allocation, or cross-subsidy tied to an integrated technical
plan.

H2 requires H1 plus closure-specific artifacts: an explicit closure program,
seed bill of materials, second-cell criterion, minimum cuts, source-resolved
material plan, and equipment designed to reproduce indispensable production
capacity.

This structure prevents a long initiative list from defeating an artificially
narrow null hypothesis.

## 3. Evidence assessment

Primary offering materials and first-party project descriptions document
orbital compute, chip design and manufacturing ambitions, lunar manufacturing
and energy, in-orbit and Moon/Mars manufacturing, asteroid mining, and
interplanetary industrialization [1,2]. This is meaningful evidence of
declared portfolio direction.

The same materials do not disclose a common technical architecture, binding
interfaces, a closure metric, a seed BOM, a second-cell milestone, or a
source-resolved reproduction plan [1,2]. Some indicators—stockpiles, radiation
tolerance, packaging, repair, and recycling—also follow from ordinary
commercial reliability and supply-security motives.

The cumulative assessment is:

- declared portfolio direction: documented;
- coordinated integrated technical implementation: not established;
- recursive closure as an explicit program objective: not established.

The strongest future H1 evidence would be shared systems engineering and
binding cross-program milestones. The strongest H2 evidence would be an
auditable second-cell program and closure-specific material/service cuts.

## 4. Threat model

The governed system includes mission authority, owner/operator, local
autonomy and maintenance controllers, remote operators, source suppliers,
independent auditors, and regulators. Protected assets include build
authority, recipes, sector/repair state, source/inventory state, verification
capacity, calibration, logs, and communication keys.

Eight threat classes are traced:

1. accidental configuration error;
2. external command compromise;
3. privileged insider override;
4. owner/operator growth incentive;
5. jurisdictional conflict;
6. common-mode verification failure;
7. autonomous objective drift;
8. contaminated or captured source.

Controls include signed cohort manifests, hardware rate limits, independent
authorization channels, sector compartmentalization, source provenance,
diverse verification, append-only logs, recovery/safe-hold, and independent
capacity audit. Each control has a verification method, rollback behavior,
and residual-risk statement. These controls adapt general risk-governance
and cyber-resilience principles [3,4]; those frameworks do not validate this
paper's space-specific control design.

## 5. Authority under communication loss

Under normal communication, new replication packets, source changes, and
safety-envelope changes require mission authority plus an independent
verifier. Local control may execute approved cohorts and routine repair.

Under delayed communication, local control may preserve viable floors, make
bounded repairs, and complete signed cohorts. It may not open a new source or
change the safety envelope, and growth is rate-limited.

Under lost communication, net new replication and source expansion stop.
Repair, collision avoidance, passivation, environmental protection, and
life/safety functions remain authorized. Two independent channels must
restore signed authority.

The rule preserves immediate harm prevention while withholding authority to
expand the system’s replication envelope.

## 6. Physical traceability

Governance gates map to model state:

- build authorization limits gross sector orders;
- viable-floor protection reads the weakest indispensable sector;
- repair-only authority reads failures, parts, intervention, and repair queue;
- source authorization reads lunar/asteroid flow, inventory, assay, and
  outage;
- commissioning authorization binds each cohort to its BOM and verification
  state;
- debris authorization reads shell and fragment criticality;
- independent audit compares reported and independently sensed capacity and
  inventory.

An unresolved discrepancy sets new-build authority to zero but does not
disable bounded repair or passivation.

## 7. Limitations and conclusion

The evidence set is public and incomplete. Absence of a disclosed architecture
is not proof that no private coordination exists. Conversely, co-occurrence of
initiatives is not evidence of a closure program.

The threat model is a requirements artifact. Control effectiveness, common
mode behavior, legal authority, cyber resistance, and recovery have not been
demonstrated. Validation requires injected faults, link-loss drills,
independent red teams, and physical interlock tests.

The result is discriminating but modest: declared off-world industrial
direction is credible; coordinated recursive closure is not established; and
the governance work is at the requirements stage.

## Data and code availability

The coded evidence ledger, exact filing provenance, threat/control register,
physical traceability table, tests, and manifests accompany the r4.0
repository release. The final statement must cite the immutable tag, archive
URL, and version DOI.

## References

[1] Space Exploration Technologies Corp., Form S-1 registration statement,
filed May 20, 2026, SEC accession 0001628280-26-036936, especially pp. 7,
10, 12, 24–25, 154, 164, and 171.
https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm.

[2] Space Exploration Technologies Corp., Rule 433 free-writing
prospectus, filed June 4, 2026, SEC accession 0001628280-26-040610,
roadshow slides 42–44.
https://www.sec.gov/Archives/edgar/data/1181412/000162828026040610/spacexfwp.htm.

[3] E. Tabassi, *Artificial Intelligence Risk Management Framework (AI
RMF 1.0)*, NIST AI 100-1, National Institute of Standards and Technology,
2023. https://doi.org/10.6028/NIST.AI.100-1.

[4] R. Ross, V. Pillitteri, R. Graubart, D. Bodeau, and R. McQuaid,
*Developing Cyber-Resilient Systems: A Systems Security Engineering
Approach*, NIST SP 800-160 Vol. 2 Rev. 1, 2021.
https://doi.org/10.6028/NIST.SP.800-160v2r1.
