# Stage 0 terrestrial autonomous-closure rehearsal

Status: protocol ready; physical execution pending.

The machine-readable authority is
`params/rehearsal_protocol.yaml`. This document is a preregistered
falsification and data-collection design, not evidence that autonomous
closure, a second cell, or any governance control has been demonstrated.

## Boundary and experimental claim

The test closes a terrestrial site around a delivered seed (`cell_0`), an
assayed material stock mapped to the model's terrestrial-rehearsal/lunar
palette, and an energy emulator with preregistered availability, storage,
peak-power, and outage behavior. Routine human entry, unrecorded spares,
off-ledger material, hidden actuation, and undeclared calibration decisions
are prohibited. Emergency entry remains available for safety, but is logged
and fails the autonomous-closure gate.

The test succeeds only if the site commissions a discrete `cell_1`. Every
indispensable subsystem must independently pass its bill of materials,
construction, commissioning, achieved-yield, service-connection, and
viable-floor gates. A continuous aggregate capacity crossing does not count.
The completed cell must then remain operating for a preregistered 30-day
window without borrowing `cell_0` capacity under the identity of `cell_1`.

## Evidence contract

Every event shares a timestamp, monotonic clock, cell and controller
identity, signed campaign/build identifier, software and recipe version,
sensor source, and external witness hash. Typed records cover:

- build states from delivery through retirement;
- species- and grade-resolved material custody;
- named autonomous tasks and interventions;
- process inputs, outputs, energy, yield, contamination, rework,
  consumables, and tool wear;
- natural and injected faults with detection, containment, and recovery;
- governance decisions under normal, delayed, and lost communication; and
- electrical, thermal, storage, and unserved-energy metering.

The protocol has ten binary acceptance gates: closed boundary, complete
provenance, reconciled mass/energy, discrete second cell, retained second-cell
operation, observable autonomy, complete fault campaign, lost-link safe hold,
independent audit, and a valid assumption-replacement record. Failed,
emergency, censored, and abandoned trials remain in the denominator.

## Fault and control campaign

The campaign exercises every threat in
`params/governance_controls.yaml`: invalid configuration, external command
compromise, insider override, owner growth pressure, jurisdictional
conflict, common-mode verification failure, producer–evaluator common mode,
oversight-bandwidth exhaustion, objective drift, contaminated or captured
source, and progressive communication loss. Each injection names the expected
controls in advance. A silent omission, unauthorized build, uncontained
physical hazard, log gap, or failure to enter safe hold is a failed gate, not
an editable protocol exception.

Under complete link loss, net-new replication and source expansion must reach
zero within one control cycle. Bounded repair, passivation, environmental
protection, and immediate safety action remain authorized. New growth can
resume only after two independent channels restore signed authority.

## Model update rule

The protocol maps raw events to commissioning lag, yield ramp, intervention
intensity, deployment and recovery rates, process-environment multipliers,
verification throughput, repair behavior, and material recovery. No
coefficient is promoted out of `ASSUMPTION` merely because a run completed.
A replacement requires a denominator, uncertainty, failed trials, censoring
rule, immutable query, protocol deviations, and an independent audit trail.

The generated
`outputs/integrated/tables/rehearsal_acceptance_matrix.csv` is the execution
checklist. Until an immutable raw event archive and auditor report populate
it, all rows remain `execution_pending`.

## Raw-event capture

The repository includes a hash-chained JSONL recorder and deterministic
coverage report for facility instrumentation. Create one archive per signed
campaign, append individually witnessed event objects, and verify the chain
before copying its digest into an evidence bundle:

```bash
uv run --locked rsi-rehearsal-archive init /secure/campaign/events.jsonl
uv run --locked rsi-rehearsal-archive append \
  /secure/campaign/events.jsonl /secure/incoming/event.json
uv run --locked rsi-rehearsal-archive verify \
  /secure/campaign/events.jsonl \
  --output /secure/campaign/acquisition-report.json
```

The recorder rejects missing schema fields, malformed witness hashes,
duplicate event identifiers, backward monotonic time, broken sequence
numbers, and any content change that breaks the record chain. The report
measures event/fault coverage and metered totals only. It cannot pass an
acceptance gate, certify physical truth, replace the independent audit, or
turn an unexecuted rehearsal into evidence.

Generate the complete facility handoff package with:

```bash
uv run --locked rsi-write-rehearsal-kit
```

The content-addressed kit under
`outputs/integrated/evidence/rehearsal_execution_kit/` includes portable JSON
Schema, one template per event type, gate-query and fault-campaign plans, the
parameter-replacement plan, a second-cell build record, and an independent
auditor-report template. Its manifest remains
`facility_handoff_ready_physical_execution_pending`; generating the kit does
not sign the protocol or execute any physical gate.

A current complete-shape template can be generated with:

```bash
rsi-evaluate-evidence rehearsal \
  --write-template rehearsal_bundle.json
```

It contains every event type, fault case, gate, and replacement record, but
its null measurements and invalid hash placeholders make it impossible to
pass before execution. A completed campaign is ingested with
`rsi-evaluate-evidence rehearsal BUNDLE.json`. The evaluator
requires every typed event, all ten independently witnessed binary gate
results, all fault cases, immutable archive/auditor hashes, and complete
parameter-replacement records. A claimed pass without those records is
rejected rather than interpreted as missing-at-random evidence.
