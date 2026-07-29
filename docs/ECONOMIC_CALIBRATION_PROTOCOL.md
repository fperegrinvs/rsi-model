# Economic calibration protocol for Part II and P3b

Status: data contract ready; empirical calibration pending.

The machine-readable authority is
`params/economic_calibration.yaml`. It closes a methodological gap, not the
empirical one: no row in the protocol is evidence that an orbital or
terrestrial architecture has achieved the assumed cost, availability,
service life, throughput, financing, or expansion response.

## Architecture and workload boundary

Calibration is separated into three cases: a terrestrial reference data
center, a serviceable space platform with replaceable compute, and an
integrated disposable AI1-style spacecraft. A record cannot be transferred
between them without an explicit transformation.

Earth and space must perform the same named workload. Inference records name
the model and version, precision, quantization, batch and sequence shape,
memory capacity and bandwidth, energy, latency distribution, accuracy or
quality gate, availability, failures, and retries. Training also records the
topology, synchronization, checkpoint, and fault policy. Delivered kW or peak
operations alone are not a workload-equivalence result.

## Evidence packages and correlated uncertainty

Six evidence packages cover workload benchmarks, space-asset reliability,
link and ground-network performance, thermal/mass/power reconciliation,
terrestrial resource buildout, and dated cash flows and financing. Their
required fields bind directly to the current anchors and dynamic-economics
parameters.

The protocol forbids independent sampling where the underlying risks share a
physical or market cause. It preregisters five groups:

- qualification, useful life, availability, insurance, and financing;
- link cost, latency, outages, and delivered throughput;
- launched mass, power, thermal design, and reliability margin;
- Earth grid, land, water, labor, permitting, cost, and delay; and
- demand, price, borrowing capacity, and investment timing.

Each group requires a joint or hierarchical fit and held-out validation.
Marginal ranges without dependence information remain sensitivity bounds.

## Cash-flow event contract

The ledger preserves dated commitments and payments, construction,
launch/transfer, commissioning, operation, failures and repair, insurance,
financing, regulation, retirement, disposal, residual proceeds, and Earth
resource expansion. Every event carries the project, architecture, document
hash, currency, price base date, amount, and physical quantity.

Capacity growth does not stand in for cash flow. Failed projects, delays,
cancellations, active-asset right censoring, zero-revenue periods, claims, and
unrecovered losses stay in the record.

## Calibration and promotion rule

The split is chronological and declared before fitting. Later projects or
periods are held out, and at least one independent operator, jurisdiction, or
architecture supplies external validation. Missingness and selective
disclosure are reported, including a sensitivity that removes confidential
or selectively available records.

No coefficient leaves `ASSUMPTION` without an immutable evidence archive,
exact extraction and transformation, denominator and units, uncertainty
model, correlation fit, failed and censored observations, held-out result,
architecture scope, and independent audit. Partial evidence can narrow a
scenario bound but cannot make P3b empirically resolved.

The generated
`outputs/integrated/tables/economic_calibration_readiness.csv` is the acquisition
and review checklist. Its rows remain `data_pending` until audited evidence
populates a separate calibration release.

A current complete-shape template can be generated with:

    rsi-evaluate-evidence economic_calibration \
      --write-template economic_calibration_bundle.json

It enumerates every package, fit, cash-flow event type, and parameter
decision, but remains invalid until measurements, hashes, holdouts, and
independent reviews replace its placeholders. A calibration release is
ingested with
`rsi-evaluate-evidence economic_calibration BUNDLE.json`. The
evaluator requires all six normalized evidence packages, all five
correlation fits and holdout results, every cash-flow event type, immutable
hashes, and a reviewed retain/promote decision for every bound parameter.
Supplying point estimates without failed/censored records and validation is
rejected.

## Public-evidence baseline

Run the reproducible public-record calibration with:

    rsi-write-economic-baseline

The generated bundle and evaluation under `outputs/integrated/evidence/`
populate all six evidence packages, all five correlation groups, all eleven
cash-flow event classes, and every parameter decision. Missing project-ledger
amounts remain visibly labeled sentinels rather than inferred observations.
The current result is `holdout_failed`: all five joint holdouts fail and all
forty parameters retain `ASSUMPTION` status. This is a completed negative
calibration against the public evidence boundary, not a substitute for the
architecture-matched audited histories required for empirical promotion.
