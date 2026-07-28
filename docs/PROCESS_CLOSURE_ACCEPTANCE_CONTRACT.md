# Process-feasible industrial-closure acceptance contract

Status: acceptance contract ready; process graph and calibration pending.

The current integrated model tracks 17 material categories and 18
industrial sectors. That is sufficient to expose category-level cuts, but it
does not represent minerals, chemical species, grades, unit operations,
critical part ancestry, or a reproducible source and transport fleet. The
machine-readable authority for replacing that abstraction is
`params/process_closure_requirements.yaml`.

## Versioned process graph

The replacement graph has seven typed nodes: source lots, process units,
materials/species, part families, production equipment, transport legs, and
waste/recycle streams. Edges carry stoichiometry or BOM quantities, units,
yield and energy distributions, contamination and rework, consumables, tool
wear, capacity, cycle time, and an exact evidence record.

At minimum, material state progresses through raw mineral, concentrate,
bulk, structural-alloy, electronic, semiconductor, and ultra-pure
process-input grades. Each transition requires an assay and acceptance
specification. Elemental occurrence cannot bypass beneficiation,
purification, contamination control, or grade qualification.

## Critical parts and ancestry

The graph explicitly includes process gases and chemicals, masks and
reticles, resists, filters, optics, coatings, seals, lubricants, bearings,
calibration artifacts, metrology/test, controls/power electronics, and
parent tools. Each production-equipment node must expose the tools and
calibration chain needed to reproduce it. Circular ancestry without an
external input or independently supported bootstrap route fails closure.

## Source and fleet boundary

Every source is a named body or defensible source class with mineral form,
composition and grade distributions, accessible recoverable reserve,
spatial variability, uncertainty, depletion, and failed-source rules.
Delivered supply also requires delta-v, transfer windows, transit and
turnaround time, payload and dry mass, propellant, processing rate, vehicle
reliability, and the fleet's own manufacture and replacement BOM.
Candidate bundles must carry non-empty source and fleet registers. Every
source-lot node names its source-register record and every transport-leg node
names its fleet record; an unlinked narrative description cannot satisfy the
graph.

## Binary acceptance

Eight gates cover species mass balance, energy and capacity, grade
progression, part and parent-tool ancestry, source/transport/fleet closure,
failures and substitution, terrestrial calibration, and the recomputed
minimum external source vector. The generated
`outputs/integrated/tables/process_closure_gap_register.csv` reports every gate,
required grade, critical part family, and graph node type as
`evidence_pending`.

The register does not make the process graph exist. It prevents future work
from declaring closure on aggregate mass alone and provides the exact
promotion boundary: only a versioned, calibrated graph passing all eight
gates can replace the current internal-consistency certificate.

A current complete-shape template can be generated with:

    scripts/evaluate_evidence_bundle.py process_closure \
      --write-template process_closure_bundle.json

The generated file is deliberately invalid until real values, immutable
hashes, and witnessed results replace its placeholders. A candidate graph is
then ingested with
`scripts/evaluate_evidence_bundle.py process_closure BUNDLE.json`. The
evaluator checks node and edge fields, references to immutable evidence
records, linked source and fleet registers, the complete grade ladder, every
critical part family, every process stage, and all eight independently
witnessed binary results. Empty,
aggregate-only, or provenance-free graphs fail validation.
