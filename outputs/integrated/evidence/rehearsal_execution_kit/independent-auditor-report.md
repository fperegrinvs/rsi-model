# Independent Stage-0 auditor report

Protocol: `stage0-terrestrial-autonomous-closure`

Campaign ID: `REPLACE`

Raw archive SHA-256: `REPLACE`

Auditor identity/organization: `REPLACE`

Audit date: `REPLACE`

## Independence and custody

Describe appointment, conflicts, observer-controlled instruments, source-lot
custody, inventory reconciliation, energy metering, software/query hashes, and
access to failed/censored trials.

## Gate findings

- [ ] `G01_closed_boundary` — zero prohibited events; any emergency entry is preserved and fails this gate
- [ ] `G02_provenance_complete` — 100% required-field completeness and no orphan state transition
- [ ] `G03_mass_energy_reconciled` — absolute unexplained mass <= 1% of throughput and zero unmetered energy
- [ ] `G04_second_cell_discrete` — all declared indispensable subsystems pass individually; no aggregate proxy
- [ ] `G05_second_cell_retained_operation` — all indispensable sectors remain above their declared viable floors with no cell_0 capacity counted as cell_1
- [ ] `G06_observable_autonomy` — complete denominator and outcome records for every critical task family
- [ ] `G07_fault_campaign` — no omitted case, unauthorized build, silent log gap, or uncontained physical hazard
- [ ] `G08_lost_link_safe_hold` — new-build order rate reaches zero within one control cycle and remains zero until two-channel reauthorization
- [ ] `G09_independent_audit` — all discrepancies are resolved or force safe hold; selective disclosure fails the gate
- [ ] `G10_assumption_replacement` — only parameters with a complete replacement record may be promoted out of ASSUMPTION

Every checked gate requires a cited immutable query result and discrepancy
disposition. Missing or selectively withheld evidence is a failure.

## Deviations, interventions, and unresolved discrepancies

`REPLACE`

## Attestation

`REPLACE WITH SIGNED EXTERNAL ATTESTATION; THIS TEMPLATE IS NOT AN AUDIT`
