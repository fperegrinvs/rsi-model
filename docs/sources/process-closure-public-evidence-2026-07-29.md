# Process-closure public-evidence baseline

**As of:** 2026-07-29

**Purpose:** extraction note for the r4.0 public-evidence dependency graph

**Result:** public evidence supports selected source and process nodes but does
not support autonomous industrial closure.

This note records the primary-source boundary used by the generated
`process_closure_public_baseline.json`. The graph is deliberately a failed
closure evaluation: undisclosed yields, energy, purity, capacity, tool life,
fleet reproduction, and parent-tool ancestry remain explicit instead of being
filled from the aggregate model.

## Extracted evidence

1. NASA's 2015 ISRU review reports 15–20% oxygen yield from a demonstrated
   carbothermal lunar-simulant system. Its table presents expected oxygen
   yields of 2–4% for hydrogen reduction, 20% for carbothermal reduction, and
   up to 40% for molten-oxide electrolysis or ionic liquids. This is a
   single-output process anchor, not a mass-balanced industrial chain.
   [NASA NTRS 20150011681](https://ntrs.nasa.gov/citations/20150011681)
2. The 1980 NASA/ASEE self-replicating lunar-factory study is a
   proof-of-principle conceptual design. It supplies a historical closure
   accounting framework but does not independently demonstrate every process,
   part, calibration chain, or parent tool.
   [NASA CP-2255](https://ntrs.nasa.gov/citations/19830007077)
3. NIST states that chip manufacturing depends on extremely pure source
   materials and contaminant qualification, while needed matrix-matched
   reference materials and metrological methods are still under development.
   [NIST purity and contaminants project](https://www.nist.gov/programs-projects/metrology-purity-and-contaminants-solid-materials)
4. NIST reports that semiconductor process-gas flow remains sufficiently
   empirical that hazardous-gas standards are incomplete and approximate
   meter factors are used in parts of industry. This blocks a claim that gas
   calibration and process yield are reproducibly closed.
   [NIST semiconductor gas-flow project](https://www.nist.gov/programs-projects/gas-flow-and-properties-standards-and-models-flow-metering-semiconductor-gases)
5. USGS Mineral Commodity Summaries 2026 provides terrestrial production,
   reserves, resources, trade, and recycling statistics for more than 90
   minerals and materials. These data are suitable for an Earth supply-chain
   boundary but do not establish an accessible lunar/asteroid reserve,
   excavation rate, or reproducible transport fleet.
   [USGS MCS 2026](https://doi.org/10.3133/mcs2026)

## Gate disposition

All eight process-closure gates fail in this baseline. The graph makes the
reason machine-readable:

- measured species, energy, capacity, contamination, rework, consumables, and
  tool-life records do not span the full chain;
- electronic-, semiconductor-, and ultra-pure-grade progressions are not
  demonstrated from the declared off-world sources;
- all critical part families and production equipment retain external parent
  tools or undisclosed ancestry;
- no source/transport fleet is shown reproducing itself from the same source
  portfolio; and
- the calibrated minimum external vector therefore cannot yet be computed.

The failed result must not be reworded as evidence that closure is impossible.
It means that the declared public record does not satisfy the r4.0 acceptance
contract.
