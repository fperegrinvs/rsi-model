# Orbital-compute post-IPO calibration snapshot

- Accessed: 2026-07-27
- Manuscript use: Third Edition r3.5, Part II and Appendix A.6
- Epistemic role: independent engineering and economic cross-checks
- Model role: **not inputs in r3.5**; architecture partition and roadmap evidence

This note records the values carried into the manuscript so later revisions
can distinguish source statements, arithmetic derived from them, and proposed
model changes. Company specifications remain company statements; pre-prototype
architectures remain technical concepts.

## 1. Conventional system closure

S. G. Turyshev, "Orbital Data Centers: Spacecraft Constraints and Economic
Viability," arXiv:2604.27197:

https://arxiv.org/abs/2604.27197

Representative 1 MW high-sunlight case:

- BOL PV area: 5,640 m²
- radiator area: 2,500 m²
- PV + storage + radiator mass: 29.4 kg/kW
- total after fixed spacecraft functions: 34–59 kg/kW
- at 40 kg/kW and a terrestrial infrastructure benchmark of
  $10,000–40,000/kW, allowed launch + spacecraft-build expenditure:
  $250–1,000/kg before communications, operations, utilization, and finite
  lifetime
- illustrative five-year lifetime penalties: 1.27× at 10% annual hazard and
  1.58× at 20%

Model comparison: the generic r3.5 LEO case has a 46.1 kg/kW central value
and approximately 25–91 kg/kW component-corner envelope. The central value is
well bracketed; the current tail range spans both advanced integration and
small-node overhead and should be partitioned by architecture in a later
model revision.

## 2. Low-mass concepts

S. Gaalema, S. Indyk, and C. Staley, "Reduced-Mass Orbital AI Inference via
Integrated Solar, Compute, and Radiator Panels," arXiv:2604.07760:

https://arxiv.org/abs/2604.07760

- authors' design basis: 112.5 kW/t, or approximately 8.9 kg/kW
- large example: approximately 150 t and 16 MW, with a roughly 2.2 km array
- enabling assumptions: integrated PV/radiator/compute panels, vapor chambers,
  thin tandem PV, custom ASICs
- intended workload: inference

I. Bargatin et al., "Tether-Based Architecture for Solar-Powered Orbital AI
Data Centers," arXiv:2512.09044 / AIAA SciTech 2026:

https://arxiv.org/abs/2512.09044

- 2–20 MW architecture
- representative node: approximately 10 kg and 2 kW, or 5 kg/kW
- intended workload: inference
- major open gates: tether deployment and dynamics, micrometeoroid damage,
  shielding, station-keeping, and end-of-life disposal

These concepts define stretch scenarios. They are not evidence for replacing
the conventional 34–59 kg/kW envelope with a single 5–10 kg/kW prior.

## 3. Network boundary

K. van Berkel, "The Cost and Network Limits of Space-Based AI Compute,"
arXiv:2607.14172:

https://arxiv.org/abs/2607.14172

Compared 8,000-accelerator systems:

- terrestrial Clos bisection: 28,800 TB/s
- two-dimensional orbital mesh at 100 Gbps links: 2.25 TB/s
- three-dimensional orbital mesh at 100 Gbps links: 10 TB/s
- modeled network latency: 150–450× terrestrial

The paper's aggressive 200 $/kg launch and 10 kg/kW mass assumptions are not
adopted as economic anchors. Its network calculation supports a workload
partition: per-node inference, preprocessing, and communication-integrated
edge compute can be modeled; frontier distributed training requires an
explicit interconnect-performance model.

## 4. Space-microdatacenter reference class

R. Eason, N. Bleier, M. Lembeck, and R. Kumar, "Architecting Space
Microdatacenters: A System-level Approach," IEEE HPCA 2025:

https://passat.crhc.illinois.edu/hpca25.pdf

- scale: bespoke 0.5–10 kW nodes for space-native workloads
- power and thermal functions: roughly one-third of modeled spacecraft TCO
- compute hardware: less than 1% of bespoke spacecraft TCO in the evaluated
  cases
- energy efficiency: up to 2.5× more valuable in space; modeled TCO reduction
  around two-thirds in the cited comparison
- selected life: five years, reflecting radiation and hardware generations

This is strong evidence for small edge-processing satellites, but not a
direct cost reference for megawatt Earth-substitution compute.

## 5. Full thermal-system mass

NASA Glenn, NASA/TM—2005-213442:

https://ntrs.nasa.gov/api/citations/20050238492/downloads/20050238492.pdf

- ISS two-sided radiator panel: 2.75 kg/m²
- ISS radiator including fluid loop and deployment: 8.8 kg/m²
- JIMO complete radiator-system estimate: 5 kg/m²
- at 353 K, emissivity 0.86, environment 173 K: approximately 1.4 m²/kW

Derived complete-system range at that temperature:

- 5 kg/m² × 1.4 m²/kW = 7.0 kg/kW
- 8.8 kg/m² × 1.4 m²/kW = 12.3 kg/kW

AI1 arithmetic from the official 110 m² and 120 kW average specification:

- quoted area intensity: 110 / 120 = 0.917 m²/kW
- two emitting faces: 120,000 W / 220 m² = 545 W/m²
- one quoted emitting area: 120,000 W / 110 m² = 1,091 W/m²

Using

`q = ε σ (T_rad^4 - T_env^4)`

with ε = 0.86 and T_env = 173 K gives approximately 332 K (59 °C) for
545 W/m² and 391 K (118 °C) for 1,091 W/m². These are ideal surface
temperatures, not coolant or chip junction temperatures, and omit solar/Earth
view, degradation, nonuniform heat spreading, and transport temperature
drops.

## 6. Directional public economic cross-check

University of Virginia National Security Data Policy Institute, "Evaluating
Space-Based Data Center Architectures: Capabilities, Constraints, and
Trade-Offs," May 19, 2026:

https://nationalsecurity.virginia.edu/sites/default/files/files/2026-05/00036_20260519%29_nsdpi_evaluating_space-based_data_center_architectures-capabilitites%2C_constraints%2C_and_trade-offs.pdf

- present-style simplified five-year 1 GW case: $135.6B orbital versus
  $16.6B terrestrial
- joint aggressive case: $15.4B orbital at $30/kg launch, $10/W spacecraft
  hardware, 100 W/kg specific power, 80% sunlight, 1% annual degradation,
  and 1% GPU failure
- important exclusions: GPUs, financing, insurance, logistics overhead, and
  downtime

Use only as a joint-condition cross-check, not as a replacement for the
companion model.

## 7. Model changes implied, but not made in r3.5

1. Partition total mass by architecture: conventional modular, AI1 company
   specification, and integrated/tether stretch.
2. Replace radiator-only mass with a full thermal-system representation:
   cold plates, transport, pumps, emitter, deployment, and controls.
3. Add spacecraft bus/manufacture/integration cost or a combined
   launch-plus-build $/kg axis.
4. Condition 10–25 year infrastructure life on demonstrated payload exchange
   or platform reuse; otherwise use whole-vehicle life.
5. Factor utilization into sunlight duty, availability, workload utilization,
   network efficiency, and reserve.
6. Add communication intensity and sustained-bandwidth gates.
7. Model distributed training separately from per-node inference.
