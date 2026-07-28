# r4.0 governance threat and control model

Status: requirements model; not a validated safety case.

The machine-readable authority is `params/governance_controls.yaml`. This
document explains its interpretation. Every control remains
`requirement_unvalidated`: naming a control does not establish that it works.

## System boundary

The governed system includes the Earth mission authority, owner/operator,
local autonomy and maintenance controllers, remote operators, source
suppliers, independent auditors, and jurisdictional regulators. Protected
assets include build authority, signed recipes, live sector and repair state,
source/inventory state, compute and verification capacity, calibration
references, audit logs, and communication keys.

Five boundaries receive explicit treatment: the Earth link, corporate-to-site
authority, control-to-actuator commands, source custody, and the independent
audit boundary. The threat register covers accidental configuration,
external cyber compromise, privileged insiders, owner incentives,
jurisdictional conflict, common-mode verification failure, autonomous
objective drift, and contaminated or captured sources.

## Authority during communication loss

- Normal communication permits execution of signed cohorts. A new
  replication packet, source change, or safety-envelope change requires the
  mission authority and an independent verifier.

- Delayed communication permits maintenance, bounded repair, viable-floor
  protection, and completion of already signed cohorts. It does not permit a
  new source or safety-envelope change, and reduces the growth-rate limit.

- Lost communication enters safe-hold. Repair, collision avoidance,
  passivation, environmental protection, and life/safety functions remain
  authorized. Net new replication and source expansion stop until two
  independent channels restore signed authority.

This is a deliberate asymmetry: loss of Earth contact preserves the ability
to prevent immediate physical harm but removes the authority to increase the
system's replication or source-acquisition envelope.

## Physical-model connection

Controls bind to quantities already exposed by the integrated model:

| Governance gate | Physical state |
|---|---|
| build-rate interlock | gross sector orders and communication-state rate cap |
| viable-floor protection | minimum operating capacity of each indispensable sector |
| repair-only safe-hold | failed capacity, repair queue, parts, intervention, and recovery time |
| source interlock | lunar/asteroid flow, finite inventory, assay/provenance, and outage state |
| commissioning authorization | cohort BOM, commissioning queue, verification throughput, and yield |
| debris gate | shell active/derelict/fragment state and hazardous-descendant ratio |
| independent audit | reported versus independently sensed sector, inventory, and source state |

An unresolved discrepancy sets new-build authority to zero; it does not
disable bounded repair or passivation. A communication or audit failure is
therefore capable of changing the physical model's allowed order rate, rather
than appearing only as prose.

## Residual risk

The register retains a residual-risk statement for every threat. The hardest
residuals are collusion across nominally independent authorities, shared
calibration or specification errors, regulator capture, and novel behavior
inside a formally permitted envelope. No ordinal label or checklist converts
those residuals into a calculated probability. Validation requires injected
faults, link-loss drills, independent red-team exercises, and evidence that
physical interlocks fail safe under common-mode software and sensor faults.
