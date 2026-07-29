# Appendix D: Complete model specification {#appendix-d-complete-model-specification}

Everything a reader needs to reconstruct the Part I model without opening
the implementation. Part II's cost model is fully specified by its affine
form (II.2) plus the anchor table (A.4), with two implementation details: the
annualization applies component-specific lives (compute hardware and its
replacement launch mass on `compute.life_years_space`; PV, radiator,
storage, structure, and their launch spend on
`power_systems.infrastructure_life_years`, floored at the hardware life —
the LCO remains exactly affine in launch $/kg), and each Monte Carlo
iteration resolves every anchor once per cached AnchorSet so Earth and
space share common physical draws while retaining separate financing
anchors. This appendix covers the multisector
dynamics and then specifies the paper layer that runs beside it.

## D.1 Integrated-bootstrap layer {#d.1-integrated-bootstrap-layer}

**State space.** The implementation has 18 sectors: power, mining,
refining, robotics, machine tools, construction, thermal, transport,
repair, recycling, interconnects/boards, passives/power,
sensors/control, packaging/test, mature logic, advanced logic/memory,
process equipment/metrology, and compute. It tracks 17 material categories:
O, Si, Al, Fe, Mg, Ca, Ti, H, C, N, Cu, Ni, Co, Cr, Li, rare earths, and
dopants — 15 elements plus two material classes, so the model is
material-category-resolved rather than element-resolved: stoichiometric
and process-chemical closure is not checked at the species level. The
full coefficient set is the machine-readable specification in
`params/integrated_model.yaml`.

**Material and service closure.** For material category $e$, sector $j$,
and source/transfer arc $a$:

::: {#eq:appendix-material-balance .equation}
$$
\Delta M_e
= \sum_s Y_{s,e}X_s + I_e + \sum_a F^{\mathrm{in}}_{a,e}
- \sum_j B_{e,j}x_j - L_e - \sum_a F^{\mathrm{out}}_{a,e},
$$
:::

where $B_{e,j}$ is the amount of material category $e$ required per unit
of sector-$j$ build, $Y_{s,e}$ is the recoverable yield from source and
process $s$, and $F_{a,e}$ is material flow across an Earth, lunar
surface, orbital, or asteroid transfer arc. Concentration alone does not
set $Y$; mineral form, beneficiation, refining energy, purity, and loss
remain outside the occurrence citations. Service closure uses
$A_{i,j}$, the sector-$i$ service output needed to build and replace
sector $j$. Recoverable lunar and asteroid yields, rather than bulk
inventory, enter the constraints. Earth material appears only as the
bounded initial strategic-material import stock $v_e$.

**Process environment and autonomy.** For each process $j$, task coverage
at AI level $I$ is

::: {#eq:task-coverage .equation}
$$
c_j(I)=\min\{c_j^{\max},\ c_j^0+\alpha_j\max(I-1,0)\}.
$$
:::

Effective productivity is multiplied by $(0.5+0.5c_j)$ — a declared
ASSUMPTION-class convention assigning fully scripted, conventionally
automated operation half of full productivity at zero unscripted-task
coverage, not a measured relation. Residual annual
intervention is $h_j(1-c_j)z_j$ and its sum must fit the scenario budget;
the linear form treats missing autonomy as smoothly divisible labor
demand and does not represent threshold effects, where one unrecoverable
diagnosis, calibration, or repair task stops a line despite high average
coverage.
Where declared required acceleration $g_j^\ast$ exceeds lunar gravity
$g_L=0.165g$, the acceleration gap adds centrifuge structural material
and parasitic power. The reported centrifuge speed follows

::: {#eq:centrifuge-speed .equation}
$$
\mathrm{rpm}_j=\frac{60}{2\pi}
\sqrt{\frac{9.80665\max(g_j^\ast-g_L,0)}{r_j}}.
$$
:::

This is an equipment penalty, not a claim that a whole lunar factory or
habitat requires artificial gravity.

**Seed sizing.** Decision variables are sector capacities $z_j$, annual
lunar and asteroid feed $p_L,p_A$, and initial Earth strategic-material
stocks $v_e$.
The linear program minimizes

::: {#eq:seed-mass-objective .equation}
$$
M_{\mathrm{seed}}
= M_{\mathrm{digital}}+\sum_j z_j\sum_e B_{e,j}^{\mathrm{eff}}
+\sum_e v_e,
$$
:::

subject to minimum viable sector capacities, task coverage and intervention
limits, service output sufficient for replacement plus one complete second
cell, element balances through each scenario horizon, and mining, refining,
transport, and energy throughput. Sector commissioning lags and half-ramp
loss reduce productive years. $M_{\mathrm{digital}}=5$ t represents the
software, simulation, industrial-memory, and experimental package; its
value is an assumption, not a storage-mass estimate.

The LP can also minimize Earth-import mass or intervention demand, using
installed mass as a lexicographic secondary objective. All three objectives
return the same central design in every LP-feasible scenario. This is not a
Pareto frontier: it shows that the present variables contain no alternative
process or redundancy choices capable of trading those objectives.

**Dynamic sector-capacity growth.** A feasible seed begins as one installed and
operating cell — delivery, unloading, site preparation, and first
commissioning are outside the model, so seed mass refers to an installed
operating nucleus, not a self-deploying delivered package. Each quarter,
lunar production, commissioned asteroid production, and recovered
retirement enter inventory. New orders use the complete balanced
sector-and-material vector of the seed design. For each sector $j$,
installed capacity $K_j$, operating capacity $O_j$, ordered capacity, its
declared commissioning lag, yield ramp, and depreciation $\delta_j$ remain
stateful. Retired material is recovered by category at the declared 82%
fraction. Lunar feed scales with operating mining, refining, and power;
asteroid feed additionally requires operating transport. An incomplete
packet contributes only the output $q_jO_j$ of sectors already operating.
The reported cell-equivalent aggregate is derived as
$\min_j O_j/z_j$, and the doubling threshold is first passage of that
minimum to 2.0. It is not the discrete commissioning of a second factory's
subsystems and not, by itself, evidence of sustained growth. Balanced
packets remain a restriction: the dynamic allocator cannot yet choose an
independent sector composition or explicit repair action.

Installed compute raises the model's normalized capability index according to
the implemented discrete update

::: {#eq:intelligence-update .equation}
$$
I_{t+\Delta t}
= \min\{I_{\max}, I_t
+\ell\,\nu_v(t)\,
\eta_{\mathrm{hw}}\eta_{\mathrm{util}}
\eta_{\mathrm{alg}}\eta_{\mathrm{arch}}\,
\log_2(1+C_t/C_0)
\left(\frac{I_{\max}-I_t}{I_{\max}-I_0}\right)^{\beta_I}
\Delta t\},
$$
:::

where $I_t$ is the dimensionless capability index at elapsed year $t$;
$I_0=1$ and $I_{\max}=3$ are the declared initial level and fixed-regime
frontier; $\ell=0.025$ is capability-index gain per verified-loop equivalent
at unit compute signal, unit frontier factor, and unit efficiency;
$\nu_v(t)=v\min_s\nu_s(t)$ is verified loops per year after the
$v=0.85$ verification yield and the train, data, experiment, evaluate,
safety, deploy, and observe stage bottleneck; and
$\eta_{\mathrm{hw}},\eta_{\mathrm{util}},\eta_{\mathrm{alg}},
\eta_{\mathrm{arch}}$ are dimensionless effective-compute ratios. $C_t$ is
installed compute capacity converted into the model's compute units, $C_0$ is
its initial value, $\beta_I=1.25$ is the frontier-gap curvature, and
$\Delta t=0.25$ yr. The train-stage rate alone scales with
$(C_t/C_0)^{1/2}$, capped at twice its baseline; the other stages do not
automatically accelerate with compute. Every coefficient in this update is
**ASSUMPTION**-class. It is a bounded sensitivity structure, not an empirical
law or a forecast of intelligence.

Intelligence above the scenario starting level raises both industrial
productivity and autonomy, which raises cell output and future compute.
Earth and Earth-fed orbital counterfactuals instead add capacity at constant,
scenario-specific build/delivery rates, subtract 0.16/yr depreciation, and
impose terrestrial site ceilings. Moon→orbit compute has a 0.5-year lag, a
35% share of new endogenous capacity, and a transport-capacity ceiling.

**Debris state.** A separate stress test evolves active assets, derelicts,
and a fragment index. Failures, controlled disposal, retrieval, collisions,
fragment creation, natural clearance, and active removal are explicit.
$R_{\mathrm{debris}}$ — the five-year fragment creation-to-clearance
ratio — is fragments created divided by fragments cleared
over the last five years: a flow ratio, not a branching-process
reproduction number. Realized
clearance is capped by the fragments available, so at an empty fragment
stock the ratio reads exactly one. The distributed case multiplies the collision
kernel by 0.01; it is therefore a declared topology test, not a derived
property of heliocentric space.

**Orbital lifecycle and common-cause controls.** A separate
capacity-equivalent mass-flow sensitivity implements Equation
[@eq:orbital-lifecycle-state] with the nine reported states operating,
degraded, awaiting service, under repair, cannibalized, salvaged, recycled
feedstock, disposed waste, and uncontrolled debris. Repairs return capacity
only after service start, completion, and repair yield; salvaged mass returns
to production only after recycling yield and manufacturing capacity.
Collision losses and disposed or recycling waste enter the irreversible-loss
diagnostic, while successful debris retrieval subtracts from it. Tests require
nonnegative stocks and conservation after external deployment is included.
This layer does not model mission-specific capture trajectories, qualification
of repaired hardware, or species-level recycling.

The common-cause control sensitivity evaluates Equation
[@eq:orbital-common-cause-budget] against explicit node capacities and hazard
sets. Its shell-state controller maps crossed thresholds to deterministic
actions: pause deployment and dispatch removal for creation/clearance,
hazardous-descendant, or derelict-mass violations; increase spacing and reserve
maneuver propellant for conjunction or maneuver violations; reduce cluster
caps and isolate failure domains when tracking or communications degrades; and
tighten disposal reliability or retire a shell after disposal violations.
Zero-valued conjunction, maneuver, tracking, and communications metrics in the
current table mean “not simulated by this run,” not observed safety.

**Scenarios and uncertainty.** The four named cases are terrestrial
rehearsal, lunar strategic-material bridge, strict lunar-only, and Moon–asteroid
network. Their horizons, AI levels, import caps, intervention budgets, and
source commissioning dates are all explicit in the YAML. Each 200-run
ensemble uses stable crc32 names from seed 404 to draw independent
log-uniform multipliers for service productivity, bills of material, lunar
and asteroid yield, depreciation, lag, and autonomy gap. Frequencies across
those draws are design-space occupancy, not empirical probabilities.
Tests verify dimensions, nonnegative balances, strict-lunar infeasibility,
finite-import-stock behavior, gravity overhead, aggregate-capacity
doubling, named-draw stability, and the
debris threshold. `outputs/integrated/MANIFEST.md` binds the configuration,
implementation, runner, tests, tables, figures, and report.

**Analysis module.** `src/rsimodel/integrated_analysis.py` adds derived
diagnostics over the same declared coefficients, inventing none:
terminal-window endpoints (retention at horizon, final-five-year net
capacity change, import-pool exhaustion timing); strategic-import-stock
resolution; zero/freeze intelligence-coupling ablations; the
installed-mass-versus-aggregate-doubling oversize frontier
(`simulate_capacity_growth(initial_cells=f)` installs f cell-equivalents of
the fixed minimum-mass design); per-draw ensemble diagnostics over the
identical named crc32 draws (failure reasons, binding-constraint
frequencies, Spearman sensitivity); and an elastic-relaxation
infeasibility certificate that interrogates the exact seed LP through a
shared matrix builder. The expanded module also compares independent
allocation and explicit repair, observable knowledge/autonomy outages,
process-environment profiles, finite-mass shell debris, policy and
structural-shock sweeps, shelf-limited electronics architectures, symmetric
dynamic economics, and composition-changing robust-seed Pareto designs.
The full table set and five figures regenerate with the run, including the
full sector trajectory and an 80-year central extension. These diagnostics
add structure and falsification plumbing; their coefficients remain
assumptions pending empirical calibration.

**Equation-review sensitivity module.** `src/rsimodel/extensions.py` implements
the newly explicit Part I relations without claiming calibration:

- [digital progress regimes](../outputs/integrated/tables/digital_progress_regimes.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_progress_regimes.csv"} compares smooth diminishing effort,
  fixed-frontier saturation, and discrete frontier-shift cases while reporting
  experiment, technical-validation, and internal-adoption throughput plus
  marginal gain separately;
- [internal/public capability trajectories](../outputs/integrated/tables/internal_public_capability_trajectories.csv){.artifact-link data-artifact="outputs/integrated/tables/internal_public_capability_trajectories.csv"} reports
  zero-lag, slower-publication, and internal-overhang assumption cases with
  separate internal/public capability and event clocks;
- [AI R&D compute allocation](../outputs/integrated/tables/ai_rd_compute_allocation.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rd_compute_allocation.csv"} conserves one physical accelerator-hour
  budget across training, research inference, experiments, data generation
  and filtering, verification and safety, and external productive service;
  compares raw-capability, verified-progress, and physical-growth objectives;
  and sweeps effective-compute conversion without creating physical hours;
- [cognitive physical labor table](../outputs/integrated/tables/cognitive_physical_labor.csv){.artifact-link data-artifact="outputs/integrated/tables/cognitive_physical_labor.csv"} separates model instances, inference
  capacity, robots/machines, experiment stations, and independently
  verifiable work cells; assigns surplus copies to nonphysical tasks or
  waiting/contention; and reports parallel and serial experiment time,
  coordination edges, duplicate work, onboarding, and verification demand;
- [AI electronics supply chain table](../outputs/integrated/tables/ai_electronics_supply_chain.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_electronics_supply_chain.csv"} decomposes the AI hardware chain into
  front-end logic, memory, advanced packaging, substrates/interposers,
  high-speed interconnect, power electronics, test/metrology, and
  radiation-qualified system integration, with heterogeneous shelf life,
  physical failure, obsolescence, local/import supply, reuse/down-bin,
  shortfall, closure sequence, and Earth-umbilical fields;
- [compute cohort summary](../outputs/integrated/tables/compute_cohort_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_cohort_summary.csv"} and [compute cohort trajectory](../outputs/integrated/tables/compute_cohort_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_cohort_trajectory.csv"} retain
  age/generation cohorts and separate physical failure, radiation-adjusted
  performance, economic frontier obsolescence, and reassignment to inference,
  verification, control, or non-frontier simulation under both continued
  hardware progress and an architectural-convergence branch;
- [verification hierarchy table](../outputs/integrated/tables/verification_hierarchy.csv){.artifact-link data-artifact="outputs/integrated/tables/verification_hierarchy.csv"} reports formal invariants, destructive
  physical acceptance, independent held-out experiments, causal operational
  outcomes, human/AI rubrics, and self-assessment separately, with candidate
  and verifier throughput, five evaluator-independence coordinates,
  false-positive stress, direction-setting capacity, and preservation of
  positive, negative, and null industrial-memory records;
- [industrial reliability ladder table](../outputs/integrated/tables/industrial_reliability_ladder.csv){.artifact-link data-artifact="outputs/integrated/tables/industrial_reliability_ladder.csv"} maps each task from single-attempt
  success through repeated, long-context, production, safety-field,
  unscripted-recovery, and sustained-operation evidence, with
  consequence-specific reliability, human checking/recovery/cleanup,
  rollback, intervention, and out-of-distribution recovery gates;
- [data evaluator coevolution table](../outputs/integrated/tables/data_evaluator_coevolution.csv){.artifact-link data-artifact="outputs/integrated/tables/data_evaluator_coevolution.csv"} separates synthetic generation,
  deduplication, filtering, provenance, evaluator error/bias, diversity,
  accepted signal, held-out transfer, physical causal episodes and their
  time/wear/sample/verification accounts, plus proprietary-data erosion
  through publication, espionage, mobility, distillation, and replication;
- [replication governance externalities summary](../outputs/integrated/tables/replication_governance_externalities_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/replication_governance_externalities_summary.csv"} and
  [replication governance externalities trajectory](../outputs/integrated/tables/replication_governance_externalities_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/replication_governance_externalities_trajectory.csv"} separate productive,
  legitimately authorized, unauthorized, and contested-resource-preempting
  capacity; track debris, remaining contested resources, declining material
  leverage, output claims, and externality costs; and evaluate engineering,
  private-objective, and governance endpoints independently;
- [digital channel ablations](../outputs/integrated/tables/digital_channel_ablations.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_channel_ablations.csv"}, [digital elasticity bounds](../outputs/integrated/tables/digital_elasticity_bounds.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_elasticity_bounds.csv"}, and
  [digital loop bottlenecks](../outputs/integrated/tables/digital_loop_bottlenecks.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_loop_bottlenecks.csv"} expose one-channel freezes, separately
  bounded elasticities with an explicit correlation matrix, and the binding
  verified-loop stage in each declared period;
- [digital release backtest table](../outputs/integrated/tables/digital_release_backtest.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest.csv"} and
  [digital release backtest summary](../outputs/integrated/tables/digital_release_backtest_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest_summary.csv"} fit the declared relations only on
  2020–2022 releases, score 2023 validation observations, and then expose a
  2024 holdout, with source locators and lower-bound inputs retained per row;
- [milestone order branches](../outputs/integrated/tables/milestone_order_branches.csv){.artifact-link data-artifact="outputs/integrated/tables/milestone_order_branches.csv"} keeps verified AI-R&D, embodiment,
  Earth/space reproductive-capital closure, and control readiness as separate
  clocks across four speed regimes and a terrestrial-first counterfactual;
- [closure loop ablation matrix](../outputs/integrated/tables/closure_loop_ablation_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/closure_loop_ablation_matrix.csv"} crosses the implemented verified
  AI-R&D proxy with permission to order new capital, proving that digital
  improvement and reproductive-capital closure are separate model switches;
- [authorized capacity control summary](../outputs/integrated/tables/authorized_capacity_control_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_summary.csv"} and
  [authorized capacity control trajectory](../outputs/integrated/tables/authorized_capacity_control_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_trajectory.csv"} keep task, coordination,
  evaluator, and controllability coordinates separate and constrain gross
  capacity by independent reliability, adversarial-verification,
  secure-command, environmental, treaty, and human-comprehension rates;
- [intelligence marginal response table](../outputs/integrated/tables/intelligence_marginal_response.csv){.artifact-link data-artifact="outputs/integrated/tables/intelligence_marginal_response.csv"} applies the same 0.1
  capability-index finite perturbation across material-starved,
  source-network, import-buffer, and operationally governed regimes while
  holding every other declared complement fixed;
- [bottleneck upgrade projects](../outputs/integrated/tables/bottleneck_upgrade_projects.csv){.artifact-link data-artifact="outputs/integrated/tables/bottleneck_upgrade_projects.csv"} and
  [bottleneck upgrade trajectory](../outputs/integrated/tables/bottleneck_upgrade_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/bottleneck_upgrade_trajectory.csv"} classify reducible, physical-floor,
  observation-time, and external-authority constraints and admit a capacity
  increment only after budget, productive-sector, causal-verification, and
  lag gates pass;
- [compute demand allocation summary](../outputs/integrated/tables/compute_demand_allocation_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_demand_allocation_summary.csv"} and
  [compute demand allocation trajectory](../outputs/integrated/tables/compute_demand_allocation_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/compute_demand_allocation_trajectory.csv"} compare non-saturating and
  bounded valuable-demand paths plus an early humanitarian-priority branch,
  while keeping relocation, total expansion, and use allocation as separate
  welfare-relevant accounts rather than producing a welfare scalar;
- [intergenerational learning faults](../outputs/integrated/tables/intergenerational_learning_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/intergenerational_learning_faults.csv"} runs repeated and structurally
  similar sensor, actuator, calibration, and communication faults across four
  controller generations while keeping transfer cases hidden and checking
  retention and prior-task regression;
- [digital learning feedback table](../outputs/integrated/tables/digital_learning_feedback.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_learning_feedback.csv"} feeds the synthetic campaign's measured
  latency, retention, transfer, recurrence, and verification cost into loop
  stage rates and verified yield while preserving its non-empirical status;
- [matched lifecycle cost contributions table](../outputs/integrated/tables/matched_lifecycle_cost_contributions.csv){.artifact-link data-artifact="outputs/integrated/tables/matched_lifecycle_cost_contributions.csv"} uses one category order for
  Earth and space, reports paired p10/p50/p90 values, ranks the central
  difference drivers, and labels unpriced categories as omissions;
- [data advantage profile](../outputs/integrated/tables/data_advantage_profile.csv){.artifact-link data-artifact="outputs/integrated/tables/data_advantage_profile.csv"} reports all seven normalized components,
  uncertainty widths, hard gates, and the visibly assumption-class geometric
  scalar;
- [coordination sensitivity](../outputs/integrated/tables/coordination_sensitivity.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_sensitivity.csv"} evaluates modular, centralized, and
  all-to-all dependency graphs across complexity, uncertainty, and effective
  intelligence, retaining the irreducible floor;
- [coordination form uncertainty](../outputs/integrated/tables/coordination_form_uncertainty.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_form_uncertainty.csv"} and
  [coordination form summary](../outputs/integrated/tables/coordination_form_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/coordination_form_summary.csv"} compare power, logarithmic-edge, and
  saturating-edge relations under common parameter draws and map the primary
  coordination-hours account once into schedule, output, reliability, and
  labor cost;
- [embodiment compatibility matrix](../outputs/integrated/tables/embodiment_compatibility_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_compatibility_matrix.csv"} separates failed physical dimensions,
  hardware ceilings, intelligence thresholds, verification, and first
  passage for every declared task and hardware portfolio;
- [embodiment two direction sweep table](../outputs/integrated/tables/embodiment_two_direction_sweep.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_two_direction_sweep.csv"} and
  [terrestrial rehearsal embodiment faults](../outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv"} vary intelligence and hardware
  independently and inject declared sensor, actuator, calibration,
  communication, tool, observability, and out-of-distribution degradations;
- [embodiment bill-of-materials requirements](../outputs/integrated/tables/embodiment_bom_requirements.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_bom_requirements.csv"} makes the assumed sensor, actuator,
  end-effector, spare, calibration-equipment, and local-controller material
  additions and annual replacement-service coefficients explicit by target
  sector;
- [orbital lifecycle states](../outputs/integrated/tables/orbital_lifecycle_states.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_lifecycle_states.csv"} reports the nine lifecycle stocks and the
  repair, recycling, retrieval, and irreversible-loss flows;
- [orbital lifecycle strategy comparison](../outputs/integrated/tables/orbital_lifecycle_strategy_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_lifecycle_strategy_comparison.csv"} exposes design-for-service and
  design-for-circularity variables rather than hiding them in a lower
  depreciation coefficient;
- [orbital transport service network](../outputs/integrated/tables/orbital_transport_service_network.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_transport_service_network.csv"} compares four named
  origin-destination routes using the rocket equation and reports maturity
  gates plus client-value, reliability, serviceability, fleet, recovery, and
  reuse sensitivities; [orbital transport break even surface table](../outputs/integrated/tables/orbital_transport_break_even_surface.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_transport_break_even_surface.csv"} crosses
  those axes over all four route and propellant-source architectures;
- [orbital service decision comparison](../outputs/integrated/tables/orbital_service_decision_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_service_decision_comparison.csv"} compares nine disposition actions
  over six orbit regimes, two asset classes, and three fleet architectures on
  one lifetime-output and risk boundary while keeping technical, economic,
  governance, and deployable gates separate;
- [orbital regime assumptions](../outputs/integrated/tables/orbital_regime_assumptions.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_regime_assumptions.csv"}, [orbital fleet amortization table](../outputs/integrated/tables/orbital_fleet_amortization.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_fleet_amortization.csv"}, and
  [orbital governance constraints](../outputs/integrated/tables/orbital_governance_constraints.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_governance_constraints.csv"} expose orbit-specific physics and
  disposal assumptions, fleet capacity/fixed-cost sharing, and authorization,
  liability, export, custody, provenance, and qualification dependencies;
- [orbital control policy table](../outputs/integrated/tables/orbital_control_policy.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_control_policy.csv"} reports common-cause budget compliance,
  shell-state triggers, and selected actions; and
- [orbital cluster layout optimization table](../outputs/integrated/tables/orbital_cluster_layout_optimization.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_cluster_layout_optimization.csv"} compares physical and logical
  failure-domain layouts over altitude, inclination, plane, spacing, shell,
  gateway, control, shared-service, communications, concentration, and
  common-cause dimensions;
- [orbital breakup cloud summary](../outputs/integrated/tables/orbital_breakup_cloud_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_breakup_cloud_summary.csv"} and
  [orbital breakup cloud trajectory](../outputs/integrated/tables/orbital_breakup_cloud_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_breakup_cloud_trajectory.csv"} propagate Earth-orbit and lunar-orbit
  clouds through explicit node geometry and report losses, expected secondary
  collisions, maneuvers, interruption, repair load, and restoration;
- [orbital degraded control stress](../outputs/integrated/tables/orbital_degraded_control_stress.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_degraded_control_stress.csv"} tests tracking, communications,
  navigation, and coordination failures before and after declared fallback
  actions;
- [orbital mitigation portfolio pareto](../outputs/integrated/tables/orbital_mitigation_portfolio_pareto.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_mitigation_portfolio_pareto.csv"} reports the complete 256-point,
  eight-axis mitigation surface and its three-objective non-dominated set;
- [orbital environment strategy comparison](../outputs/integrated/tables/orbital_environment_strategy_comparison.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_environment_strategy_comparison.csv"} prevents Earth-orbit and
  lunar-orbit clearance, tracking, residence, station-keeping, and disposal
  assumptions from being shared; and
- [orbital multi operator capacity table](../outputs/integrated/tables/orbital_multi_operator_capacity.csv){.artifact-link data-artifact="outputs/integrated/tables/orbital_multi_operator_capacity.csv"} applies shell carrying-capacity,
  authorization, tracking-data, maneuver, and disposal-compliance gates
  across multiple operators; and
- [partial closure metrics table](../outputs/integrated/tables/partial_closure_metrics.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_metrics.csv"} reports strict autonomy, mass closure,
  external-support intensity, import leverage, residual critical inputs, and
  the initial installed seed mass that is deliberately excluded from the
  ongoing-support autonomy indicator; and
- [partial closure support policies](../outputs/integrated/tables/partial_closure_support_policies.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_support_policies.csv"} and
  [partial closure dashboard](../outputs/integrated/tables/partial_closure_dashboard.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_dashboard.csv"} compare fixed, proportional, finite
  stockpile, and disrupted residual-import policies while placing autonomy,
  continuous closure, entry mass, supplier utilization, binding input,
  runway, and capacity loss in one view; and
- [partial closure substitution programs table](../outputs/integrated/tables/partial_closure_substitution_programs.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_substitution_programs.csv"} records threshold, ancestry,
  evidence, intelligence/embodiment/physical gates, probability-free outcome,
  and the resource-accounted expansion effort consumed by each dependency
  program;
- [partial closure supplier boundary table](../outputs/integrated/tables/partial_closure_supplier_boundary.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_supplier_boundary.csv"} places factories, materials, labor,
  energy, finance, transport, reliability, and growth inside the external
  support boundary; and
- [partial closure allocation policies](../outputs/integrated/tables/partial_closure_allocation_policies.csv){.artifact-link data-artifact="outputs/integrated/tables/partial_closure_allocation_policies.csv"} compares expansion-first,
  stockpile-first, balanced, and substitution-first uses of the same supported
  local base.

These tables are deterministic implications of
`params/integrated_model.yaml`. Each row carries its source class, and tests
cover domains, limiting cases, diminishing response, first-passage
attribution, conservation, graph effects, and control triggers.

## D.2 Ten-sector model {#d.2-ten-sector-model}

**Sectors and units.** n = 10 sectors, ordered: power, mining, refining,
robotics, machine_tools, electronics, thermal, transport, repair,
recycling. Capacity K_j is in abstract capacity units (K_j(0) = 1 for all
j unless stated); sector j produces q_j output units per capacity unit per
year (q below is the central set after environment q-scaling for the lunar
architecture is applied via `environments.yaml`; the tabulated q is the
pre-scaling set value). Repair and recycling are service sectors: their
rows in A are zero, and their outputs are consumed as described below.

**Time.** Discrete steps of Δt = 0.25 yr (0.5 yr for cut-set enumeration),
default horizon 35–40 yr. This layer has no construction lags,
commissioning delays, yield ramps, or minimum efficient scales — all its
outputs are stylized model outputs, not engineering timescale forecasts.

**Imports.** m_i(t) = B₀ · e^(−t/τ) · φ_i, with per-sector cutoffs
(m_i := 0 for i in the cut set after the cutoff year). Stockable sectors'
imports flow into the stockpile; non-stockable flow into the current
balance. Mars: stockable imports arrive as synodic batches of size
m·(2.14 yr) every 2.14 yr.

**Allocation (per step): three-stage lexicographic optimization.** Variables: builds
x ∈ ℝⁿ₊, wear-repair u ∈ ℝⁿ₊, recycling activity w ∈ ℝ₊, stockpile
drawdown d ∈ ℝⁿ₊ (d_i = 0 for non-stockable i), growth floor g ∈ ℝ.

Stage 1 — maximize g subject to:

::: {#eq:lexicographic-growth-stage .equation}
$$
\begin{aligned}
x_j + u_j - \delta_j K_j
  &\ge gK_j && \forall j, \\
u_j
  &\le \delta_{\mathrm{wear},j}K_j && \forall j, \\
\sum_j A_{ij}x_j
+ s_f\sum_j A_{ij}u_j
&\\[-0.2em]
\quad
+ \mathbf{1}_{i=\mathrm{repair}}\frac{1}{\eta_{\mathrm{rep}}}\sum_j u_j
+ \mathbf{1}_{i=\mathrm{recycling}}w
&\\[-0.2em]
\quad
+ o_iw-\rho_iw-d_i
  &\le q_iK_i+m_{\mathrm{direct},i} && \forall i, \\
w+\eta_{\mathrm{scrap}}\sum_j f_{\mathrm{wear},j}u_j
  &\le \eta_{\mathrm{scrap}}
  \sum_{j,c}f_{c,j}\delta_{c,j}K_j, \\
d_i
  &\le \frac{S_i}{\Delta t}.
\end{aligned}
$$
:::

with s_f = spares fraction (0.15), η_rep = repair efficiency (0.75
central), η_scrap = processing yield (0.40 central, < 1 always), o =
recycling opex vector, ρ = recycling output profile, and f_c,j = the
recoverable share of loss component c in sector j. Equivalently, available
retirement before processing is

::: {#eq:recoverable-retirement .equation}
$$
R(K,u)=\sum_{j,c}f_{c,j}\delta_{c,j}K_j
-\sum_j f_{\mathrm{wear},j}u_j.
$$
:::

The environment defaults are:

| environment | wear | catastrophic | obsolescence | logistics |
|---|---:|---:|---:|---:|
| LEO | 1.00 | 0.00 | 1.00 | 0.00 |
| lunar | 1.00 | 0.50 | 1.00 | 0.00 |
| Mars | 1.00 | 0.25 | 1.00 | 0.00 |
| Earth | 1.00 | 0.80 | 1.00 | 0.00 |

: Default environmental modifiers for the ten-sector model. {#tbl-d-environment-defaults}

Stage 2 holds g at its optimum and minimizes dimensionless stock draw
$\sum_i\omega_i d_i$, where $\omega_i$ is the inverse of a same-unit
scale based on current supply and available stock, normalized by the
largest weight. Stock is a buffer, not fuel, and the objective is invariant
to changes in sector row units.

Stage 3 holds the stage-1 and stage-2 optima within solver tolerance and
minimizes a strictly convex normalized action norm:

::: {#eq:normalized-tie-break .equation}
$$
\min\left[
\sum_j\frac{x_j^2+u_j^2}{\widehat K_j^2}
+\frac{w^2}{\widehat R^2}
+\sum_i\frac{d_i^2}{\widehat D_i^2}
+g^2\right].
$$
:::

All scales are positive state-derived quantities with numerical floors.
The positive-definite Hessian makes the selected action, and therefore the
state transition, unique. Stage 1 and 2 use HiGHS; stage 3 uses OSQP with a
public SLSQP fallback for rare narrow-face numerical failures.

**State updates and shocks.**

::: {#eq:state-updates .equation}
$$
\begin{aligned}
K_j &\leftarrow
\max\!\left(K_j+\Delta t\,(x_j+u_j-\delta_jK_j),10^{-9}\right), \\
S_i &\leftarrow
\operatorname{clip}\!\left(
S_i+\mathrm{inflow}_i-d_i\Delta t-\frac{S_i\Delta t}{L_i},
0,C_i
\right).
\end{aligned}
$$
:::

with shelf life L_i (electronics 5 yr central), capacity cap
C_i = c_years · Σ_j A[i,j] δ_j K_j (replacement demand), initial stock
S_i(0) = s_years · replacement demand at t = 0, stockable sectors only
(robotics, machine tools, electronics, repair). Common-cause shocks are
applied after this deterministic capacity update; the stock cap is then
recomputed from the damaged capacity. Reported timestamps and shock-log
timestamps are the step end $t+\Delta t$. The headline realized growth is

::: {#eq:realized-growth .equation}
$$
g_{\mathrm{real}}=
\min_j\frac{K_{j,\mathrm{postshock}}-K_{j,\mathrm{prestep}}}
{\Delta t\,K_{j,\mathrm{prestep}}},
$$
:::

while the allocator's pre-shock $g^*$ is retained separately as
`g_alloc`.

**Depreciation.** δ_j = δ_wear,j + δ_catastrophic,j + δ_obsolescence,j +
δ_logistics,j per environment (`environments.yaml`), anchored entries
resolved at geometric mids (deterministic) or loguniform draws (MC), one
shared draw per anchor per run. Obsolescence is included on the reading
that K is frontier-equivalent capacity (A.1's five-quantity separation).

**Shocks.** Per step and per shock class: N ~ Poisson(rate · Δt) events;
each multiplies K over its sector group by (1 − f), f ~ U(f_lo, f_hi).
Rates jittered ±30% per MC run (ASSUMPTION).

**Outcome definitions.** *Expanding at year 30*: realized
post-shock g > 0 at the step ending at year 30 — the instantaneous, weakest
endpoint; it does not preclude import- or stock-supported growth or
near-zero absolute capacity (a minimum-viable-scale criterion needs an
authorial threshold and is queued). The pre-shock allocation endpoint uses
`g_alloc` and is diagnostic only. *Sustained*: realized g > 0 at every
recorded step ending in years 25–30. *Earth-import cutoff*: a separate
central-set ensemble with all Earth imports cut at year 30; the endpoint is
realized g > 0 throughout 30–35 (stock draw permitted). LEO retains capture
feed and is labeled accordingly, not as autonomy.
*Balanced doubling* (headline replication metric): first t with
λ(t) = min_j K_j(t)/K_j(0) ≥ 2 — unit-invariant, requires every sector to
double in its own capacity units; it is not a claim that a complete second
physical seed has been commissioned. *Aggregate doubling* (continuity diagnostic): first t
with Σ_j K_j(t) ≥ 2 Σ_j K_j(0), measured against the supplied K(0) —
unit-dependent, reported alongside but never as "system replication".
Both doubling metrics are reported over all runs that ever reach the
criterion and conditioned on year-30 survivors — the difference is the
doubled-then-failed class.

**Binding sector and co-binding.** At each allocation step, each
material-balance supply is relaxed by 1% and stage 1 is re-solved. The
finite response $\Delta g_i$ is unit-invariant because both the
perturbation and row quantity scale together. Every positive response
within 5% of the largest forms the co-binding set and shares fractional
credit. If all responses are numerically zero, relative slack supplies a
display fallback only. The baseline and allocation-policy comparison use
the same definition.

**Central-set structural coefficients** (ASSUMPTION-class; conservative =
central with A×1.35, δ×1.4, τ=10 yr, and reduced repair/recycling/stock
scales; optimistic = A×0.75, δ×0.8, τ=25 yr, increased scales; full
machine-readable sets in `params/assumptions.yaml`):

| A[i,j] | pow | min | ref | rob | mt | el | th | tr | rep | rec |
|---|---|---|---|---|---|---|---|---|---|---|
| **pow** | 0.30 | 0.35 | 0.40 | 0.25 | 0.30 | 0.45 | 0.20 | 0.30 | 0.20 | 0.40 |
| **min** | 0.20 | 0.15 | 0.30 | 0.15 | 0.20 | 0.10 | 0.15 | 0.20 | 0.10 | 0.08 |
| **ref** | 0.25 | 0.20 | 0.15 | 0.25 | 0.30 | 0.30 | 0.20 | 0.25 | 0.18 | 0.20 |
| **rob** | 0.15 | 0.20 | 0.15 | 0.10 | 0.15 | 0.15 | 0.10 | 0.15 | 0.25 | 0.18 |
| **mt** | 0.10 | 0.10 | 0.10 | 0.20 | 0.10 | 0.25 | 0.10 | 0.10 | 0.30 | 0.22 |
| **el** | 0.08 | 0.06 | 0.06 | 0.20 | 0.15 | 0.10 | 0.08 | 0.12 | 0.15 | 0.10 |
| **th** | 0.05 | 0.05 | 0.08 | 0.05 | 0.05 | 0.10 | 0.05 | 0.05 | 0.06 | 0.15 |
| **tr** | 0.10 | 0.15 | 0.10 | 0.08 | 0.08 | 0.08 | 0.08 | 0.05 | 0.10 | 0.12 |
| **rep** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **rec** | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **q** | 1.00 | 1.20 | 1.00 | 0.80 | 0.50 | 0.40 | 0.90 | 0.70 | 1.00 | 0.90 |
| **φ (import share)** | 0.00 | 0.00 | 0.05 | 0.10 | 0.20 | 0.55 | 0.05 | 0.00 | 0.05 | 0.00 |

: Central ten-sector input-output matrix and strategic import shares. {#tbl-d-input-output-matrix}

Column j of A is the recipe for one unit of sector-j capacity; rows are
the supplying sectors (pow=power, min=mining, ref=refining, rob=robotics,
mt=machine_tools, el=electronics, th=thermal, tr=transport, rep=repair,
rec=recycling).
