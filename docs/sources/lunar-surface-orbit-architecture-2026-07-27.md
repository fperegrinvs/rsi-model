# Lunar surface–orbit architecture and debris boundary

Date: 2026-07-27

Scope: qualitative architecture partition for the current manuscript. This note
does **not** supply numerical parameters to Parts I–II. The coupled
surface–orbit network and endogenous debris process require new transfer,
collision, fragmentation, disposal, and removal inputs before they can be
executed without silently inventing ASSUMPTION-class values.

## Evidence record

| Question | Source | What it supports | What it does not establish |
|---|---|---|---|
| What is collision cascading? | D. J. Kessler and B. G. Cour-Palais, ["Collision Frequency of Artificial Satellites: The Creation of a Debris Belt"](https://doi.org/10.1029/JA083iA06p02637), *Journal of Geophysical Research* 83(A6), 1978 | A collision creates fragments that increase the probability of subsequent collisions: debris risk is an endogenous stock-and-feedback problem | A universal object-count threshold or a prediction that every dense constellation must cascade |
| Does the current LEO model implement that feedback? | `params/environments.yaml`; `src/rsimodel/model.py` | No. The current `debris_event` is an exogenous Poisson shock with a fixed event rate and sampled fractional loss | Any density-dependent collision rate, fragment production, cross-shell transport, avoidance saturation, atmospheric decay, or debris removal |
| Is lunar orbit automatically debris-safe? | N. R. Boone and R. A. Bettinger, ["Simulation of Debris Events in Selected Low Lunar Orbits"](https://doi.org/10.1007/s40295-023-00382-y), *Journal of the Astronautical Sciences* 70, 16 (2023) | Breakup propagation is strongly orbit-dependent; some low-lunar-orbit debris populations are long-lasting, while other fragments impact the Moon, with nonuniform surface-impact geography | That present lunar traffic is near a cascade threshold, or that all lunar debris persists indefinitely |
| Why prefer a lunar surface material backbone? | NASA, ["Artemis Base Camp on the Moon Will Need Light, Water, Elevation"](https://www.nasa.gov/humans-in-space/nasas-artemis-base-camp-on-the-moon-will-need-light-water-elevation/); NASA NTRS, ["Lunar Dust Mitigation: A Guide and Reference"](https://ntrs.nasa.gov/citations/20220018746); NASA NTRS, ["Archway for Radiation and Micrometeorite Occurrence Resistance"](https://ntrs.nasa.gov/citations/20130009378) | The south-polar design trade combines long illumination periods, access to shadowed volatile deposits, and local regolith usable as bulk shielding; surface operations also face abrasive dust and landing ejecta | Proven reserve size, extraction economics, continuous solar power at a selected site, or advanced-manufacturing closure |
| What role fits cislunar orbit? | D. C. Davis et al., ["Phase Control and Eclipse Avoidance in Near Rectilinear Halo Orbits"](https://ntrs.nasa.gov/citations/20200000733), 2020 | An NRHO can be designed for eclipse avoidance and low-cost stationkeeping, supporting a gateway, relay, or transfer function | That NRHO is the cheapest site for bulk industry or that it is passively stable and maintenance-free |
| Is “Sun-synchronous” the next destination after the Moon? | NASA, ["Basics of Space Flight: Planetary Orbits"](https://science.nasa.gov/learn/basics-of-space-flight/chapter5-1/) | A Sun-synchronous orbit is a planet-centered precessing orbit selected to preserve local solar time; the familiar Earth case remains an Earth-orbit architecture | A heliocentric expansion destination or a collision-free high-capacity shell |

## Architecture implication

For long-run industrial closure, the qualitative division of labor is:

1. **Lunar surface backbone:** extraction, bulk refining, shielding,
   construction, durable storage, and the production stages that benefit
   from a physical foundation and local mass.
2. **Sparse lunar/cislunar service layer:** communications, navigation,
   observation, transfer depots, reusable transports, and orbital assembly or
   compute only where the zero-g/illumination advantage pays for exposed
   shielding, stationkeeping, and imported or surface-launched mass.
3. **Distributed heliocentric expansion:** after the lunar network can export
   productive equipment, spread nodes across separated heliocentric orbital
   elements and resource trajectories rather than recreating a single dense
   shell. Near-Earth resources are a candidate feedstock, not an established
   next-step optimum.

The first two layers are complementary rather than competing terminal
locations. A lunar-orbit complex without a surface or asteroid supply chain
has no local ore body; a surface complex without orbital infrastructure pays
more for communications, transfers, navigation, and export.

The third layer is an inference from the collision and closure constraints,
not a computed result. “Heliocentric” means orbiting the Sun. It should not
be labeled “Sun-synchronous,” which is a different, planet-centered orbital
geometry.

## Required model additions

- Per orbital shell or trajectory family: active assets, intact derelicts,
  trackable fragments, and untrackable fragments.
- A collision kernel that depends on population density, effective
  cross-section, relative velocity, maneuverability, and tracking quality.
- Fragment yield and transfer between debris classes and neighboring orbital
  regions.
- Removal through atmospheric decay where applicable, lunar/planetary impact,
  controlled disposal, retrieval/recycling, and active debris removal.
- Avoidance workload, propellant, downtime, and capacity saturation.
- A debris reproduction ratio: expected future hazardous objects generated
  per hazardous object removed or naturally cleared. A ratio above one marks
  the cascade regime; no numerical threshold is assigned here.
- A multi-location production graph with lunar-surface nodes, orbital nodes,
  and explicit transfer arcs carrying mass, energy, equipment, and
  replacement capacity.
