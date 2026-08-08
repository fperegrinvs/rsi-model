# Orbital compute as an industrial seed: the economics of the Earth-dependent bridge

## Abstract

We compare terrestrial compute with LEO, cislunar, lunar-surface, and disclosed
Starmind AI1 architectures using levelized cost per delivered
frontier-equivalent kW-year and workload-specific inference and
network-effective training units. The completed boundary includes qualified
hardware, power, thermal transport, spacecraft bus, communications, ground
network, program NRE, insurance, spectrum and regulatory cost, disposal,
residual value, utilization, component-specific life, and separate Earth and
space financing. Central serviceable-platform costs are approximately 5.29×
Earth for generic LEO, 8.97× for cislunar batch, 263× for Earth-supplied lunar
surface compute, and 3.17× for the disclosed AI1 mass/power case. Even a
quarantined $185/kg, 100 kW/t aspirational case is 1.09× Earth after the
omitted-cost boundary is completed; the corresponding incomplete boundary
produces 0.76×. Training is less favorable because orbital network efficiency
is an explicit gate. Present bridge architectures therefore do not reach
commodity terrestrial parity under the declared ranges. Mature high-closure
economics remain unresolved and require a dynamically financed physical
system. These results do not test whether orbital compute could serve as
anchor demand for launch, spacecraft manufacturing, power, communications,
silicon, robotics, and servicing. They show that such an industrial-seeding
thesis cannot be justified by present commodity-compute parity alone; it
requires separately measured learning spillovers, deployment-speed value,
cross-program reuse, and progress toward physical closure.

## Keywords

orbital compute; space economics; levelized cost; data centers; launch cost;
techno-economics

## Highlights

- Complete system accounting reverses the favorable aspirational crossover.
- Generic serviceable LEO compute costs 5.29 times the Earth reference.
- Network-effective training is less favorable than local inference.
- Physical capacity growth does not imply economic self-financing.

## 1. Scope

This paper addresses P3a: the bridge-economy cost boundary for orbital
compute. It does not establish physical industrial closure (P2), corporate
coordination (P4), or mature high-closure economic advantage (P3b).
The strategic motivation is broader than a standalone data-center product.
Orbital compute could in principle be an anchor customer for a shared
physical stack: launch, mass-produced spacecraft, energy, thermal management,
laser communications, qualified silicon, autonomy, and servicing. An early
system could then be strategically useful while remaining more expensive per
delivered compute unit, if its cumulative learning, time-to-capacity, or
cross-program reuse exceeded the cost gap. Those benefits are not credited in
the levelized-cost result. Naming them prevents a narrow cost comparison from
silently rejecting the strategic hypothesis, while preventing the strategic
hypothesis from silently erasing present costs.
Recent orbital-compute studies span clustered accelerators, system-level
spacecraft constraints, mass-integrated inference concepts, and
microdatacenters [1–4]. Their differing architectures and workloads are a
reason to preserve explicit boundaries rather than combine headline
cost-per-kilogram claims.

The principal unit is dollars per frontier-equivalent kW-year of delivered IT
load. Two additional units prevent electrical input from standing in for all
computational output:

- cost per million inferences for a declared model, precision, batch,
  accuracy, latency, memory, and availability envelope;
- cost per network-effective training kW-year after interconnect,
  synchronization, and fault overhead.

The numerical workload-throughput bounds are assumptions until tied to a
specific workload.

## 2. System boundary

Space capex includes:

1. qualified compute hardware;
2. PV, storage, pumping, thermal transport, radiators, structure, and
   reliability margin;
3. spacecraft bus, avionics, propulsion, shielding, and integration;
4. communications and ground network;
5. program NRE and disposal provision;
6. launch of hardware and infrastructure.

Annual terms include operations, insurance, spectrum/regulatory expense, and
capital recovery. Residual value differs between a serviceable platform and
an integrated disposable satellite. Space and Earth financing distributions
are separate.

Earth includes hardware refresh, data-center shell, PUE, electricity,
financing, and a responsive alternative that can induce firm power and choose
older-node hardware when its performance-adjusted cost is lower.

Communications geometry, collision externalities, and landing/turnaround
infrastructure remain outside the cost model and should not be inferred to be
zero. Network topology is especially material for distributed training:
published orbital-mesh comparisons report much lower bisection bandwidth and
higher latency than the terrestrial fabric used in their comparison [5].

## 3. Architectures

The serviceable-platform case refreshes compute on its hardware life while
power, thermal, structure, and their original launch amortize over a longer
infrastructure life. The disposable case retires all components together.
Neither architecture is treated as demonstrated.

The AI1 conditional case uses the disclosed 150 kW peak compute, 120 kW
average compute, 150 kW array, 70 kW/t vehicle efficiency, radiator area, and
envelope [6]. Lifetime, availability, qualification, cost, and component mass
split remain bounded assumptions. Heritage radiator references separate panel
areal density from the mass of a complete heat-transport and deployment
system [7].

The aspirational case uses the company target arithmetic of $185/kg and
100 kW/t plus favorable, non-company values for qualification, seven-year
life, and 95% utilization. It is excluded from Monte Carlo because targets
and selected favorable bounds are not probability distributions. The
underlying launch and power-density statements are company projections in
offering material, not achieved prices or demonstrated systems [8].

## 4. Results

Against the central Earth counterfactual:

| Space case | Central cost ratio |
|---|---:|
| generic LEO inference, serviceable | 5.29× |
| cislunar batch, serviceable | 8.97× |
| Earth-supplied lunar surface | 263× |
| disclosed AI1, serviceable | 3.17× |
| aspirational AI1 target case | 1.09× |

Completing the omitted-cost boundary reverses the aspirational result:
without the added communications, bus, NRE, insurance, regulation, disposal,
thermal, and financing terms it is 0.76× Earth; with them it is 1.09×. The
directional conclusion is stronger than either point estimate: qualification,
useful life, utilization, platform architecture, network efficiency, and
non-launch system cost can dominate launch price.

For inference, identical assumed request throughput leaves the space/Earth
ratio aligned with the kW-year ratio. For frontier training, the central
orbital network-efficiency bound is much lower than Earth’s, so cost per
network-effective training kW-year widens sharply. Per-node inference,
preprocessing, and space-native sensing are analytically separate from a
distributed frontier-training cluster.

## 5. Dynamic counterfactual

A companion scenario model gives Earth and space the same investment,
reinvestment, learning, depreciation, regulatory delay, debt, interest,
bridge-finance, and demand mechanics. Space is capped by technically
available physical capacity and pays for industrial orders, source transfer,
and intervention. Earth expands an induced resource/site ceiling.

In the declared commodity case, financing activates substantially less than
the technically available space capacity while Earth expands endogenously. A
space-native price premium funds more of the off-world path, but the space
case does not repay declared external capital within 40 years. Physical
compounding is therefore not equivalent to economic self-financing.

An industrial-seeding interpretation would require an additional value
account rather than a favorable relabeling of the same cash flow. Candidate
terms include reductions in later spacecraft and launch cost attributable to
cumulative Starmind production; earlier activation of compute than the
responsive terrestrial alternative; reuse of power, thermal, communications,
silicon, autonomy, or servicing assets by other programs; and measurable
declines in imported mass or external services per unit of operating orbital
capacity. None is assigned a positive value here. A future model can admit a
term only after it specifies the beneficiary, counterfactual, attribution
rule, timing, and evidence class.

## 6. Limitations and conclusion

All completed-boundary additions have wide assumption ranges. Correlated
qualification, service life, repairability, and availability need
architecture evidence. Workload units need a named model and service-level
objective. Spectrum, insurance, and financing depend on jurisdiction and
market structure. Earth can respond technologically and geographically.

The defensible conclusion is narrow: present bridge-economy orbital compute
does not beat responsive terrestrial compute in the declared complete-system
cases. Orbital compute may still function as an industrial seed, but that
claim must earn the difference through measured anchor-demand effects,
learning spillovers, faster capacity activation, cross-program reuse, or
progress toward lower Earth dependence. Mature high-closure advantage is not
refuted, but it is unpriced and unproven. It requires physical closure,
reliable serviceability, source logistics, and cash-flow conditions that this
result does not assume away. The current cost gap is therefore a strategic
test, not a quantity that the strategic narrative can omit.

## Data and code availability

The model, anchor register, deterministic draws, workload and cost tables,
figures, tests, and byte-verifiable manifests accompany the r4.0 repository
release. The final statement must replace the release-candidate location with
the immutable tag, archive URL, and version DOI.

## References

[1] B. Agüera y Arcas et al., “Towards a future space-based, highly
scalable AI infrastructure system design,” arXiv:2511.19468v2, June 17,
2026. https://arxiv.org/abs/2511.19468.

[2] S. G. Turyshev, “Orbital Data Centers: Spacecraft Constraints and
Economic Viability,” arXiv:2604.27197, April 29, 2026.
https://arxiv.org/abs/2604.27197.

[3] S. Gaalema, S. Indyk, and C. Staley, “Reduced-Mass Orbital AI
Inference via Integrated Solar, Compute, and Radiator Panels,”
arXiv:2604.07760, April 2026. https://arxiv.org/abs/2604.07760; I.
Bargatin, D. Jin, Z. Alansari, and J. R. Raney, “Tether-Based Architecture
for Solar-Powered Orbital AI Data Centers,” arXiv:2512.09044 and AIAA
SciTech 2026. https://arxiv.org/abs/2512.09044.

[4] R. Eason, N. Bleier, M. Lembeck, and R. Kumar, “Architecting Space
Microdatacenters: A System-level Approach,” IEEE International Symposium
on High-Performance Computer Architecture, 2025.
https://passat.crhc.illinois.edu/hpca25.pdf.

[5] K. van Berkel, “The Cost and Network Limits of Space-Based AI
Compute,” arXiv:2607.14172, July 15, 2026.
https://arxiv.org/abs/2607.14172.

[6] Space Exploration Technologies Corp., “Starmind AI1,” product page,
accessed July 27, 2026. https://www.spacex.com/spacexai/starmind.

[7] NASA Glenn Research Center, *Radiator Concepts for
Nuclear-Electric-Propulsion Vehicles*, NASA/TM—2005-213442, 2005.
https://ntrs.nasa.gov/citations/20050238492.

[8] Space Exploration Technologies Corp., European Union Prospectus,
approved June 5, 2026, pp. 63, 70–72, 80–82, 97, and 137.
https://content.spacex.com/cms-assets/FINAL_Documents%20and%20Updates/SpaceX%20-%20EU%20Prospectus%20%28Approved%20by%20Bafin%29%20-%20June%205%2C%202026.pdf.
