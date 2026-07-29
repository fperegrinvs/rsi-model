# TODO

**Captured:** 2026-07-28

**Scope:** next work after the current article-improvement pass. This file is
an execution queue; `ROADMAP.md` remains the detailed definition of done for
the r4.0 evidence and release program.

## 1. Integrate the current article pass

- [x] Let the in-progress article work finish before restructuring manuscript
      sources.
- [x] Review the resulting diff for claim-boundary, source-numbering,
      cross-reference, and generated-artifact consistency.
- [x] Regenerate the Fourth Edition outputs and run the full verification
      suite.
- [x] Record completed editorial work in `CHANGELOG.md` and remove any
      superseded item from this queue.

## 2. Number equations and standardize notation

The manuscript contains displayed equations without stable numbers, and some
symbols are either defined late, defined only implicitly, or overloaded. Make
the mathematical presentation independently readable before publication.

### Standalone editorial discipline

- [x] Remove backward-looking draft/version commentary from the article, such
      as “The constant-gain relation used in earlier drafts is therefore
      retired.” State the current argument directly and retain history only in
      the changelog or version-control record, outside the standalone article.
- [x] Add a manuscript check for phrases such as “earlier drafts,” “previous
      version,” “used to,” “is now,” “was replaced,” “retired,” and similar
      editorial residue. The check must review context rather than banning
      words blindly: historical claims about the field and necessary
      release/reproducibility metadata remain allowed.
- [x] During LLM-assisted review, require every sentence to advance the
      argument, evidence, definition, limitation, or reader navigation. Remove
      process narration, self-reference, revision commentary, and statements
      whose only function is to describe how the manuscript changed.

### Editorial convention

- [x] Inventory every displayed equation, inline formula, symbol, operator,
      index, subscript, and acronym used in mathematics.
- [x] Give every substantive displayed equation a stable semantic identifier
      such as `eq:orbital-deployment`; generate its visible number rather than
      storing a manually maintained number in prose.
- [x] Number main-text equations consecutively as `(1)`, `(2)`, and so on.
      Number appendix equations separately as `(A.1)`, `(A.2)`, `(D.1)`, and
      so on. Use `(1a)`, `(1b)`, etc. when an aligned group contains distinct
      relations that must be cited separately.
- [x] Cite equations consistently: “Equation (1)” at the start of a sentence
      and “Eq. (1)” elsewhere. All references should be generated hyperlinks,
      so inserting an equation cannot leave stale numbers in the text.
- [x] Number derivations, governing relations, optimization objectives,
      constraints, state updates, and quantities reused later. Leave isolated
      arithmetic substitutions or purely decorative math unnumbered only
      under an explicit, consistently applied rule.
- [x] Treat each displayed equation as part of its surrounding sentence:
      introduce it in prose and punctuate it correctly.

### Define every term

- [x] Follow each equation’s first appearance with a compact “where” paragraph
      defining every symbol that is not already defined locally.
- [x] Include physical meaning, units, and admissible domain where they matter;
      for example, define $t$ as elapsed time in years rather than only as
      “time,” and define $q_c$ as the compute capacity delivered per unit
      Earth-to-orbit payload mass with its units.
- [x] Define all indices and index sets explicitly: sector, material category,
      source, transfer arc, loss class, scenario, and time step.
- [x] Define operators and constructed functions at first use, including
      `CRF`, `clip`, indicator functions, minima over sectors, and any
      frontier-equivalent normalization.
- [x] State whether each quantity is a stock, flow, rate, fraction, index,
      decision variable, model output, or assumption-class parameter.
- [x] State continuous-time versus discrete-time conventions and distinguish
      derivatives, step updates, annual flows, and per-step quantities.
- [x] Resolve overloaded notation. In particular, avoid using the same symbol
      for effective intelligence and rotor moment of inertia, or for compute,
      costs, capacities, and caps without unambiguous subscripts.
- [x] Use consistent typography: upright text for labels, italic letters for
      scalar variables, bold notation for vectors/matrices if adopted, and
      consistent roman/Greek symbols across the main text and Appendix D.
- [x] Add a consolidated notation table near the model specification or
      glossary. It supplements local definitions; it does not replace them.
      Include symbol, meaning, units/domain, first equation, and model layer.
- [x] Cross-check every mathematical definition against the implementation,
      parameter files, tables, and prose so the notation does not imply a
      stronger model than the code implements.

### Priority ambiguities to resolve

- [x] Promote the indented
      `D_advantage = f(uniqueness, causal linkage, coverage, quality,`
      `accessibility, integration, verification value)` placeholder to a
      numbered display equation and reconcile it with the glossary’s
      data-advantage notation $\kappa_D$.
- [x] Define a data-advantage component vector before defining any aggregate,
      for example
      $\mathbf d=(d_{\mathrm{unique}},d_{\mathrm{causal}},
      d_{\mathrm{coverage}},d_{\mathrm{quality}},d_{\mathrm{access}},
      d_{\mathrm{integration}},d_{\mathrm{verification}})$, followed by
      $\kappa_D=F(\mathbf d)$.
- [x] Define every component operationally, including scale or units, valid
      range, direction (“higher is better”), measurement procedure,
      uncertainty, and source class.
- [x] State whether $F$ is only a conceptual mapping or an implemented index.
      If it is implemented, specify normalization, weights, interactions,
      missing-data treatment, uncertainty propagation, and sensitivity to
      alternative aggregations.
- [x] Test whether the dimensions are compensatory. In particular, unique or
      high-quality data may have no training value when it is inaccessible,
      legally unusable, causally unlinked, or unverifiable; encode hard gates
      or multiplicative terms where a weighted sum would conceal that fact.
- [x] If no defensible aggregation exists, retain $\mathbf d$ as a reported
      multidimensional profile and do not publish $\kappa_D$ as though it were
      a measured scalar. Any illustrative scalarization must be visibly
      `ASSUMPTION`-class.
- [x] Link the data-advantage equation to the industrial-memory learning
      pipeline: stored telemetry creates advantage only after provenance,
      causal attribution, access, integration, held-out verification, and
      transfer into a later controller or model generation.
- [x] Replace the indented Earth/space cost checklists with a matched,
      numbered lifecycle-cost decomposition. Use one environment index
      $e\in\{\mathrm{Earth},\mathrm{space}\}$ and the same categories on both
      sides, rather than implicitly assigning transport, refining,
      manufacturing, or maintenance only to space and land, regulation,
      construction, or labor only to Earth.
- [x] Define a common accounting form such as
      $C_e=\sum_k C_{k,e}-V_{\mathrm{residual},e}$, with categories for site
      or access rights, regulation and permitting, transport and logistics,
      energy, feedstock/materials, extraction and processing, manufacturing,
      construction and commissioning, labor or human intervention,
      maintenance and replacement, coordination and verification,
      decommissioning/disposal, externalities, financing, and residual value.
      A category may be zero only when the scenario and evidence justify it.
- [x] Choose and state the functional unit and system boundary before comparing
      environments—for example, discounted dollars per frontier-equivalent
      kW-year or per unit of verified industrial output over a declared
      lifetime. Include time horizon, currency year, discounting, utilization,
      availability, depreciation, replacement, and terminal value.
- [x] Keep monetary cost, physical resource demand, embodied energy, labor or
      intervention time, environmental burden, and coordination/verification
      load as separate accounts unless a documented conversion prices them.
- [x] Express the comparison as a difference or ratio over identical
      categories, such as
      $\Delta C=C_{\mathrm{space}}-C_{\mathrm{Earth}}$ or
      $R_C=C_{\mathrm{space}}/C_{\mathrm{Earth}}$, and define the sign,
      denominator, and zero/negative-cost behavior.
- [x] Distinguish external purchases from internal opportunity cost. Transport,
      extraction, refining, maintenance, and coordination remain real capacity
      demands after closure even when no market payment changes hands.
- [x] Connect the conceptual Part I equation to the implemented Part II
      lifecycle-cost model instead of creating a second incompatible cost
      boundary. Identify which terms Part II prices, which appear only as
      physical constraints, and which remain omitted or `ASSUMPTION`-class.
- [x] Accompany the equation with a contribution table or waterfall showing
      Earth and space values under the same category order, including
      uncertainty ranges and the terms that actually drive the difference.
- [x] Test the prose claim that cost “changes kind” using contribution shares
      and sensitivity analysis; do not infer an advantage merely because the
      land component is smaller off Earth.
- [x] Promote
      `Coordination burden = f(number of agents, complexity, uncertainty,`
      `intelligence)` from a prose placeholder to a numbered, testable
      equation. Do not leave the functional form implicit.
- [x] Use a dimensionally explicit candidate such as
      $B_{\mathrm{coord}}=B_{\mathrm{irred}}+
      B_0(E_G/E_0)^\alpha(\chi/\chi_0)^\beta(u/u_0)^\gamma/
      [1+\eta(I_{\mathrm{eff}}/I_0)^\delta]$, while marking the form and
      exponents as `ASSUMPTION`-class until calibrated. Here $E_G$ is the
      number or weighted strength of active task-dependency/communication
      edges, $\chi$ is operational complexity, $u$ is uncertainty, and
      $I_{\mathrm{eff}}$ is the effective coordination capability of the
      participating agents. The reference quantities make the power terms
      dimensionless.
- [x] Define the output $B_{\mathrm{coord}}$ in one declared unit—such as
      coordination agent-hours, elapsed delay, communications load, energy,
      or expected output loss per unit of verified production—and do not add
      unlike burdens into one scalar without an explicit conversion.
- [x] Do not use raw agent count as a sufficient proxy for coordination
      structure. Derive $E_G$ from the task-dependency and communication graph,
      and compare centralized, hierarchical, modular, sparse, and all-to-all
      organizations. State how human supervisors and external organizations
      enter the graph.
- [x] Operationalize complexity and uncertainty with observable measures rather
      than undefined scores—for example, dependency depth and coupling for
      $\chi$, and entropy, forecast error, or unresolved-state count for $u$.
      Specify normalization, aggregation, range, measurement cadence, and
      whether aleatoric and epistemic uncertainty are separated.
- [x] Interpret intelligence as coordination-relevant capability, not a generic
      model score. Include planning, communication compression, conflict
      resolution, uncertainty calibration, monitoring, and recovery, together
      with bandwidth, latency, context, embodiment, and verification limits.
- [x] Preserve irreducible synchronization, safety, audit, and verification
      work in $B_{\mathrm{irred}}$; increasing intelligence must not drive total
      burden below physical or governance lower bounds. Define whether that
      floor is zero for a one-agent task.
- [x] Test limiting cases and comparative statics: one agent, zero coupling,
      low and high uncertainty, fragmented versus modular graphs, degraded
      communications, and sufficiently high intelligence. Check the assumed
      signs of all partial effects, interaction terms, saturation, bottleneck
      shifts, and the possibility that adding capable agents lowers total
      completion time while increasing total coordination work.
- [x] Calibrate or bound the coordination relation with telemetry where
      possible, compare alternative functional forms, propagate parameter
      uncertainty, and connect the resulting burden once—without
      double-counting—to schedule, capacity, reliability, and lifecycle cost.
- [x] Define the Executive Summary deployment equation completely:
      $C_{\mathrm{orbit}}$, $t$, $q_c$, $L_{E\rightarrow O}(t)$, and
      $\delta_C$, including compatible units.
- [x] Distinguish gross reproduction/production rates such as $r$ from net
      growth quantities such as $g_H$, and distinguish both from discount or
      financing rates used by `CRF`.
- [x] Reconcile $I$ as intelligence with the $I$ used for rotor moment of
      inertia in rotational energy.
- [x] Clarify every use of $C$, $H$, $K$, $O$, $P$, $D$, $M$, $L$, $R$, and
      $V$, whose meanings change across model layers unless subscripted.
- [x] Define the dimensions and normalization of integrated-model quantities
      such as $B_{e,j}$, $Y_{s,e}$, $A_{i,j}$, $z_j$, $O_j/z_j$, $C_t/C_0$,
      $\ell$, $v$, and the debris stress metrics.
- [x] Define every Part II lifecycle-cost term, its currency-year convention,
      denominator, annualization rule, and whether it is a stock cost or an
      annual flow.
- [x] Explain optimization notation in Appendix D, including decision
      variables, fixed state, objective order, feasibility constraints,
      scaling terms, solver tolerances, and pre-/post-shock states.

### Build and quality checks

- [x] Select a Pandoc-compatible numbering mechanism with deterministic output
      and no hand-maintained cross-reference numbers; prefer a small pinned Lua
      filter or equally auditable local implementation over an unpinned build
      dependency.
- [x] Render equation numbers as right-aligned, deep-linkable anchors in HTML
      while preserving native MathML and useful copy/paste behavior.
- [x] Ensure equation layout remains readable on narrow screens: long equations
      may scroll horizontally, but their labels must remain visible and must
      not overlap the mathematics.
- [x] Add automated checks that every equation ID is unique, every equation
      reference resolves, generated numbers are contiguous within their
      sequence, and no raw cross-reference tokens leak into the HTML.
- [x] Add a notation audit that flags symbols missing from the consolidated
      register and incompatible duplicate definitions. Allow a small explicit
      ignore list for universal operators and local dummy variables.
- [x] Verify that every displayed equation has nearby explanatory prose and
      that each symbol’s first substantive use is locally defined.
- [x] Test direct links to representative equations, keyboard focus, screen
      reader names, printing, mobile layout, and links across the future
      multi-page GitHub Pages build.
- [x] Include equation/reference checks in both pull-request validation and the
      release-integrity workflow.

## 3. Replace the constant-gain digital-loop model

The current relation $\Delta I=L\times G$, followed by “$G$ is the average
gain per successful loop,” is too coarse. It implicitly treats successful
loops as exchangeable and their marginal gain as constant. The replacement
should make diminishing returns explicit and separate the number of loops
from the effectiveness of compute, data, hardware, algorithms, and model
architecture.

### Conceptual correction

- [x] Retire constant $G$ as the default formulation. Represent the gain from
      loop $\ell$ as state- and time-dependent, $G_\ell(t)$, or use an
      empirically calibrated learning/scaling curve.
- [x] Require diminishing marginal gain within a stable model, data, and
      algorithmic regime. State the relevant condition explicitly, such as a
      declining $\partial I/\partial C_{\mathrm{train}}$ or declining
      $G_\ell$ as cumulative effective compute increases.
- [x] Do not assume that calendar time alone causes diminishing returns. Make
      the decline depend on cumulative search/training effort, proximity to a
      regime-specific frontier, data exhaustion, evaluation saturation, or
      another measurable state.
- [x] Treat architecture changes, new training algorithms, better data,
      post-training methods, tools, and test-time computation as possible
      shifts of the attainable frontier—not as evidence that marginal gains
      stay constant.
- [x] Preserve at least three sensitivity regimes: smooth diminishing returns,
      a saturating frontier, and diminishing returns interrupted by discrete
      algorithmic or architectural innovations.
- [x] Define “effective intelligence” through a declared vector or composite
      of task-relevant, held-out capabilities. Do not equate lower
      cross-entropy loss, parameter count, benchmark score, or training compute
      directly with a scalar intelligence quantity.

### Separate loop throughput from gain per loop

- [x] Replace the current count $L$ with a time-indexed verified-loop
      throughput and define exactly what completes a loop: hypothesis,
      implementation, training or experiment, held-out evaluation, safety
      verification, and deployment.
- [x] Expand the loop-throughput bottleneck beyond compute, data,
      experimentation, verification, and reliability. Include model size,
      training tokens, context length, memory capacity and bandwidth,
      accelerator interconnect, parallelism efficiency, power, cooling, and
      wall-clock training time.
- [x] Separate peak hardware throughput from realized useful compute using
      utilization and hardware-efficiency terms such as effective FLOP/s,
      FLOP/J, memory traffic, communication overhead, and failure/restart
      losses.
- [x] Add an explicit algorithmic-efficiency factor defined as the compute,
      data, or wall-clock reduction required to reach a fixed held-out
      performance threshold.
- [x] Add an architecture-efficiency factor rather than using parameter count
      alone. Distinguish at least:
      - Transformer attention versus selective state-space or hybrid designs
        such as Mamba;
      - dense models versus sparsely activated mixture-of-experts models;
      - total parameters versus active parameters per token;
      - training efficiency versus inference and long-context efficiency.
- [x] Account for architecture-specific penalties: expert routing and load
      balancing, inter-device communication, training instability, memory
      hierarchy, sequence-length scaling, and hardware/software maturity.
- [x] Keep data quantity, data quality, deduplication, curriculum, synthetic
      data, and contamination controls separate. Token count alone is not a
      sufficient data term.

### Close the experience-to-learning loop

An effective recursive loop requires the system to learn from operational
mistakes, near misses, recoveries, and experiments. This does not require the
deployed LLM or other foundation model to change its weights continuously.
Learning can occur through persistent memory, updated procedures or
controllers, offline post-training, or transfer into a successor model
generation.

- [x] Separate five learning mechanisms:
      - temporary context or working memory within one operation;
      - persistent retrieval from industrial memory within one model
        generation;
      - revised recipes, procedures, simulators, planners, or control policies;
      - offline fine-tuning or post-training of the current architecture;
      - pretraining or post-training of a successor model generation.
- [x] Define a durable operational-learning record that binds observations,
      actions, outcomes, task and hardware state, environment, model/controller
      version, human intervention, timestamps, and provenance.
- [x] Retain failures, near misses, null results, unsuccessful recovery
      attempts, and negative experiments—not only successful episodes—so later
      systems do not inherit survivorship bias.
- [x] Specify a versioned pipeline from raw telemetry to validated learning:
      ingestion, integrity checks, curation, causal attribution, labeling,
      simulation or replay, dataset/retrieval/procedure construction, held-out
      evaluation, safety verification, staged deployment, monitoring, and
      rollback.
- [x] Distinguish remembering an event from learning a transferable lesson.
      Require evidence that the revised system improves on structurally similar
      held-out cases, not merely the exact recorded episode.
- [x] Keep industrial memory readable across model and software generations
      through stable schemas, migrations, lineage, semantic versioning, and
      backward-compatibility tests.
- [x] Protect the learning channel against corrupted sensors, poisoned
      telemetry, self-confirming labels, reward hacking, selective deletion of
      failures, and unauthorized updates.
- [x] Charge every learning path for storage, communications, curation,
      labeling, simulation, training, evaluation, verification, deployment,
      and Earth dependence. Experience does not become usable knowledge
      instantaneously.
- [x] Track time from event to validated lesson, repeated-fault rate,
      recurrence after deployment, recovery-time improvement, transfer to new
      tasks, retained performance on earlier tasks, and catastrophic
      forgetting.
- [x] In the terrestrial rehearsal, inject repeated and structurally similar
      faults across controller/model generations. Keep recurrence cases hidden
      from training and verify that the lesson transfers without regression.
- [x] Feed measured learning latency, lesson-retention rate, transfer success,
      recurrence, and verification cost back into the digital-loop model.
- [x] State clearly that continuity of telemetry, memory, and verified learning
      across generations—not real-time mutation of one deployed model—is the
      necessary condition for this form of recursive improvement.

### Scaling-law and observed-progress grounding

- [x] Review neural scaling laws for loss as a power-law function of model
      size, dataset size, and training compute. Use them to motivate
      diminishing returns within their measured domain, with explicit
      extrapolation limits.
- [x] Incorporate the Chinchilla compute-optimal result as a model/data
      allocation constraint under a fixed training-compute budget. Do not cite
      Chinchilla as direct evidence for recursive-loop gains or general
      intelligence growth.
- [x] Compare Kaplan-style and Chinchilla-style compute-optimal allocations and
      state why their fitted exponents, data regimes, and prescriptions differ.
- [x] Review observed model progress using fixed-performance compute
      efficiency, not only benchmark scores over calendar time. Decompose
      progress into additional compute, hardware improvement, algorithmic
      efficiency, architecture, data, post-training, scaffolding/tools, and
      test-time compute where the evidence permits.
- [x] Use held-out or contamination-resistant evaluations and report benchmark
      saturation, changing test sets, selective reporting, and capability
      discontinuities as limitations.
- [x] Keep training scaling, inference scaling, and test-time-compute scaling
      separate; they have different costs and can bind different parts of the
      improvement loop.
- [x] Calibrate only where comparable primary data exist. Otherwise use named
      `ASSUMPTION` sets and sensitivity analysis rather than importing a
      headline progress rate into the recursive model.

Primary-source candidates for the source audit:

- Kaplan et al., *Scaling Laws for Neural Language Models*,
  <https://arxiv.org/abs/2001.08361>.
- Hoffmann et al., *Training Compute-Optimal Large Language Models*
  (Chinchilla), <https://arxiv.org/abs/2203.15556>.
- Hernandez and Brown, *Measuring the Algorithmic Efficiency of Neural
  Networks*, <https://arxiv.org/abs/2005.04305>.
- Ho et al., *Algorithmic progress in language models*,
  <https://arxiv.org/abs/2403.05812>.
- Gu and Dao, *Mamba: Linear-Time Sequence Modeling with Selective State
  Spaces*, <https://arxiv.org/abs/2312.00752>.
- Fedus, Zoph, and Shazeer, *Switch Transformers: Scaling to Trillion
  Parameter Models with Simple and Efficient Sparsity*,
  <https://arxiv.org/abs/2101.03961>.

These are candidate anchors for distinct claims, not collective support for
one growth equation. Each retained claim still needs an exact locator,
extracted quantity, source class, and transformation record.

### Model and validation work

- [x] Specify a replacement equation only after defining its observable
      outcome variable and dimensional units. Candidate inputs include
      cumulative effective training compute, model size, training tokens,
      architecture class, active-parameter fraction, hardware efficiency,
      algorithmic efficiency, experiment throughput, and verification
      capacity.
- [x] Estimate or bound each elasticity separately and preserve correlations
      among compute, data, model size, hardware generation, and architecture.
- [x] Back-test the candidate relation on chronological model releases with
      holdout years; do not fit and validate on the same frontier observations.
- [x] Run ablations that freeze hardware progress, algorithmic progress,
      architecture changes, data growth, or compute growth one at a time.
- [x] Report which resource binds verified-loop throughput in each period and
      whether progress comes from moving along a scaling curve or shifting the
      curve.
- [x] Propagate the revised digital-loop uncertainty into the coupled
      intelligence/industrial model. Re-run the existing zero/freeze coupling
      comparisons rather than assuming the richer AI model changes the
      material-limited scenarios.
- [x] Add tests for monotonicity, diminishing marginal response within each
      fixed regime, dimensional consistency, saturation behavior, and
      reproducibility of all fitted or assumed cases.
- [x] Rewrite the surrounding prose so it presents the equation as a bounded
      empirical model or sensitivity structure, not an established law of
      recursive self-improvement.

## 4. Reframe the embodied-autonomy threshold

The current framing asks whether intelligence is capable enough to operate
industrial hardware. Under the RSI hypothesis, intelligence rises over time
and increasingly adapts to unfamiliar machines, so the more durable question
is whether the available embodiment exposes enough sensing, actuation, control
bandwidth, and physical capability for that intelligence to perform the task.
Here, “higher intelligence” means **sufficiently high intelligence for the
specific task–embodiment pair**, reached only after a potentially long
improvement trajectory. The onset of RSI does not make competent embodied
operation instantaneous.

Use an **intelligence–embodiment compatibility frontier** or **embodiment
adequacy threshold**, not a single one-sided intelligence threshold.

### Correct the causal framing

- [x] Rewrite “the embodied-autonomy threshold” as a two-sided compatibility
      condition between task requirements, intelligence capability, and
      hardware affordances.
- [x] Treat increasing intelligence as reducing the amount of task-specific
      scripting, fixturing, and specialized hardware required for a task.
- [x] Define a task- and embodiment-specific sufficiency threshold
      $I_k^\ast(E)$ rather than treating any positive intelligence improvement
      as enough. Below that threshold, RSI may be active while task $k$
      remains infeasible or unreliable.
- [x] Make time to reach $I_k^\ast(E)$ a model output, with uncertainty and a
      visible “not reached within the modeled horizon” result. Do not infer an
      immediate capability transition merely because the intelligence trend is
      positive.
- [x] Distinguish three claims explicitly:
      - RSI is active and intelligence is improving;
      - intelligence has become sufficient for a particular fixed embodiment;
      - the coupled system can redesign and physically produce a better
        embodiment.
      These events can occur years apart and the latter two are not guaranteed
      within any specified horizon.
- [x] Model the limiting case in which sufficiently capable intelligence can
      learn to use any physically adequate, observable, and controllable
      embodiment, including unfamiliar tools and machines.
- [x] Do not state that intelligence can operate literally any hardware
      “perfectly.” No intelligence can infer unobserved state reliably from
      absent sensors, produce unavailable force or motion, defeat excessive
      control latency, or exceed physical precision, payload, energy, and
      reliability limits. Present perfect operation as an asymptotic
      hypothesis only within the hardware’s feasible action and observation
      envelope.
- [x] Separate failures caused by insufficient intelligence from failures
      caused by inadequate embodiment, inaccessible state, insufficient
      actuation, unsafe latency, unavailable tools, or physical process
      limits.
- [x] Make hardware improvement and intelligence improvement substitutable
      only inside measured bounds. Preserve hard non-substitutable physical
      requirements.

### Define embodiment adequacy

- [x] Replace a scalar robotics/autonomy coefficient with an embodiment vector
      covering at least:
      - degrees of freedom, workspace, reach, and kinematic constraints;
      - payload, force, torque, compliance, dexterity, and end-effector/tool
        compatibility;
      - sensor modalities, coverage, resolution, accuracy, sample rate,
        calibration, and occlusion;
      - control-loop latency, jitter, bandwidth, local compute, and
        communications dependence;
      - positioning precision, repeatability, stability, and vibration;
      - power, thermal limits, duty cycle, mobility, and environmental
        tolerance;
      - tool changing, fixture availability, connectors, and machine-readable
        interfaces;
      - fault detection, redundancy, safe states, self-calibration,
        maintainability, and repairability.
- [x] Define a task-requirement vector in the same dimensions. A task is
      physically feasible only when the embodiment meets its non-substitutable
      requirements.
- [x] Distinguish **controllability** (the hardware can reach the required
      physical states) from **observability** (the controller can infer the
      state needed to act safely and correctly).
- [x] Include latency at the correct layer: local servo control, on-device
      perception/planning, site-level coordination, and Earth communication
      cannot be represented by one round-trip number.
- [x] Treat standardized tool APIs, telemetry, digital twins, fixtures, and
      machine-readable interfaces as part of the embodiment architecture:
      they can lower the intelligence and exploration burden without adding
      mechanical degrees of freedom.

### Couple intelligence and hardware explicitly

- [x] Define task success as a function such as
      $S_k=f(I,E,R_k,\mathcal{E})$, where $I$ is intelligence capability, $E$
      the embodiment vector, $R_k$ task-$k$ requirements, and $\mathcal{E}$
      the operating environment. Define every component and avoid treating
      $S_k$ as a probability without empirical calibration.
- [x] Represent an embodiment-dependent ceiling: increasing $I$ improves
      performance toward the hardware/task frontier, while improving $E$
      moves that frontier.
- [x] Model the approach to sufficient intelligence dynamically. Diminishing
      gains, training duration, evaluation and verification, hardware
      availability, deployment cadence, and failed improvement loops all delay
      threshold crossing even when long-run improvement remains possible.
- [x] Allow higher intelligence to compensate for embodiment limitations
      through planning, active perception, tool use, multi-agent coordination,
      calibration, recovery, and construction of better tools—but charge the
      required time, energy, wear, risk, and production capacity.
- [x] Add the recursive hardware path explicitly: capable intelligence may
      design, manufacture, commission, and validate a better embodiment. This
      is a physical industrial loop with materials, equipment, and time
      requirements, not an instantaneous software upgrade.
- [x] Distinguish general-purpose embodiment from specialized process
      equipment. A versatile robot may operate a machine, but it does not
      replace the machine’s furnace, vacuum, metrology, cleanliness, or
      precision envelope.
- [x] Preserve safety and verification as independent constraints. Greater
      task capability does not by itself establish reliable, authorized, or
      independently verifiable operation.

### Evidence and validation

- [x] Build a task-by-embodiment capability matrix for mining, materials
      handling, maintenance, diagnosis, calibration, tool use, construction,
      recovery, and second-cell commissioning.
- [x] For each task, record the minimum sensor, actuation, precision, latency,
      tool, environmental, and verification requirements and the evidence
      class supporting each threshold.
- [x] Test both directions independently:
      - hold embodiment fixed and vary intelligence/controller capability;
      - hold intelligence/controller capability fixed and vary embodiment
        quality.
- [x] Include degraded sensors, actuator failures, calibration drift,
      communications loss, unfamiliar tools, partial observability, and
      out-of-distribution faults in the terrestrial rehearsal.
- [x] Report a failure-attribution matrix identifying whether each unsuccessful
      task was intelligence-limited, embodiment-limited, process-limited,
      resource-limited, verification-limited, or jointly limited.
- [x] Replace smooth average task coverage with hard task gates wherever a
      missing observation, action, tool, or physical tolerance stops the
      production line.
- [x] Sweep alternative embodiment portfolios—few general-purpose robots,
      many specialized machines, reconfigurable tooling, and hybrid
      architectures—rather than assuming one robot platform.
- [x] Update the seed-sizing and growth models so sufficient sensors,
      actuators, tools, spares, calibration equipment, and control hardware
      appear in the bill of material and replacement graph.
- [x] Revisit every manuscript claim that treats future AI capability as the
      sole autonomy bottleneck and restate it as a conditional claim about
      intelligence plus physically adequate embodiment.

## 5. Model orbital repair, reuse, and recycling in depreciation

“Depreciation: the harsh term” should not treat every failed or retired
satellite as an irreversible loss. Add explicit repair, life extension,
component reuse, salvage, and material-recycling paths while preserving their
transport, capture, processing, qualification, and failure costs.

### Replace one-way depreciation with lifecycle states

- [x] Separate physical degradation, propellant depletion, replaceable-part
      failure, repairable damage, functional obsolescence, collision damage,
      controlled retirement, and irrecoverable loss.
- [x] Model transitions among operating, degraded, awaiting service, under
      repair, restored, cannibalized, salvaged, recycled-feedstock, disposed,
      and uncontrolled-debris states.
- [x] Replace a silently reduced depreciation coefficient with explicit flow
      equations. Restored capacity should re-enter the operating stock after a
      repair lag, while recovered material should enter feedstock inventory
      only after capture and recycling yields; neither is equivalent to
      preventing the original failure.
- [x] Define an effective irreversible-loss diagnostic from those flows, but
      retain the gross failure rate, repair return, salvage yield, recycling
      return, downtime, and disposal rate separately so different mechanisms
      cannot produce the same opaque $\delta_{\mathrm{effective}}$.
- [x] Treat repair as a queue with diagnosis, rendezvous, capture, parts,
      tooling, labor/autonomy, repair duration, verification, and return-to-
      service probability. Downtime remains lost capacity even when the asset
      is eventually restored.
- [x] Send recoverable retired mass into an orbital inventory rather than
      subtracting it silently. Conserve mass by material category through
      capture, disassembly, sorting, cleaning, reprocessing, fabrication,
      qualification, reuse, waste, and accidental fragment creation.
- [x] Distinguish direct reuse, component harvesting, refurbishment,
      remanufacture, and bulk-material recycling. They have different energy,
      purity, tooling, and verification requirements.
- [x] Add design-for-service and design-for-circularity variables: standard
      docking/refueling interfaces, modular replaceable units, fasteners,
      labels/material passports, accessible fill/drain ports, grapples, safe
      passivation, separable materials, and machine-readable service manuals.
- [x] Preserve obsolescence separately. Repair may restore physical operation
      without restoring frontier-equivalent compute capacity; upgrading a
      modular payload can address both but has a different bill of material.
- [x] Couple repair/recycling to debris dynamics. Capture or processing
      failures can create fragments, while successful removal reduces future
      collision exposure.

### Compare strategies and orbital regimes

- [x] Compare replace, refuel/life-extend, repair, upgrade, cannibalize,
      repurpose, recycle, relocate, and dispose decisions using the same
      lifetime-output and risk boundary.
- [x] Resolve LEO shells, GEO, cislunar staging orbits, low lunar orbit (LLO),
      and near-rectilinear halo orbit (NRHO) separately. Rendezvous, plane
      change, residence time, drag, radiation, debris, disposal, and
      station-keeping differ materially.
- [x] Distinguish high-value serviceable spacecraft from cheap, short-lived
      constellation units. A service architecture that closes for a modular
      observatory or GEO communications satellite may not close for an
      unprepared LEO satellite.
- [x] Include fleet effects: one reusable servicer, depot, or recycling plant
      can amortize fixed launch and development cost across clients, but must
      pay routing, inclination change, propellant replenishment, storage,
      scheduling, and congestion costs.
- [x] Define break-even conditions using avoided replacement launch and asset
      value, remaining useful life, recovered material/component value,
      service cost, service risk, downtime, depreciation, debris liability,
      and residual value.
- [x] Keep technical feasibility and economic viability separate. A
      demonstrated docking, fluid transfer, or repair does not establish a
      competitive fleet-scale service, and a concept study does not establish
      either.
- [x] Add legal and governance constraints: ownership and consent for
      non-cooperative objects, export controls, liability, spectrum and orbital
      authorization, custody/provenance of salvaged parts, and verification of
      safety-critical recycled material.

### Turn the collision-cascade boundary into a control strategy

The current collision-cascade boundary is primarily diagnostic. Convert it
into architecture constraints, operating rules, and intervention triggers that
limit both debris creation and the capacity that one event can disable.

- [x] Define an explicit common-cause loss budget: the maximum number of nodes,
      compute capacity, power, communications paths, or service fraction that
      one credible collision, breakup cloud, avoidance failure, or shell event
      may destroy or isolate.
- [x] Treat a “cluster” as a failure domain with declared physical extent,
      orbital planes and shells, conjunction geometry, interdependencies, and
      shared services—not merely as a logical group of compute nodes.
- [x] Add a loss-containment constraint such as
      $L_{\max}=\max_h\sum_i K_i\,\mathbf 1(i\in h)\le
      \epsilon K_{\mathrm{total}}$, where hazard set $h$ contains assets
      exposed to one credible event and $\epsilon$ is the tolerated capacity
      fraction. Define the event set, time window, capacity unit, and
      `ASSUMPTION` status.
- [x] Optimize cluster size and distribution over altitude, inclination,
      orbital plane, along-track spacing, physical separation, and
      communications topology. Include correlated fragment exposure and shared
      gateway, power, navigation, software, or control failures.
- [x] Reserve independent capacity across failure domains so the system can
      isolate a damaged cluster, reroute workloads, preserve command and
      verification, and rebuild without losing the whole service.
- [x] Compare concentration benefits—shorter links, easier maintenance,
      shared power/thermal infrastructure, lower coordination overhead—with
      larger collision cross-section, correlated loss, avoidance saturation,
      debris yield, and reconstruction burden.
- [x] Make allowable cluster size a model output or policy control derived from
      the common-cause loss budget and shell state, not a fixed preferred node
      count.

Use a mitigation hierarchy rather than one undifferentiated “debris control”
term:

- [x] **Prevent creation:** reliable components, passivation, containment,
      release prevention, design for demise/removal, short post-mission
      residence, and highly reliable disposal.
- [x] **Avoid tracked objects:** continuous conjunction assessment,
      uncertainty-aware screening, sufficient maneuver reserve, automated but
      coordinated collision avoidance, and rules preventing two operators from
      selecting conflicting maneuvers.
- [x] **Survive small untracked debris:** localized Whipple or equivalent
      shielding, component placement, redundancy, leak isolation, and damage
      detection. Model shielding by particle-size/velocity regime and include
      its mass and cross-section penalty; do not imply that practical shielding
      can absorb a catastrophic satellite-scale impact.
- [x] **Limit consequences:** physical compartmentalization, graceful
      degradation, rapid safe mode, autonomous isolation, spare paths, repair
      access, and fragment-resistant placement of critical shared systems.
- [x] **Remove or recycle hazardous objects:** prioritize intact, massive,
      collision-likely derelicts and failed constellation members by expected
      avoided fragment creation. Charge tracking, rendezvous, detumbling,
      capture, custody, transport, processing, and removal risk.
- [x] Distinguish active debris removal from recycling. Safe deorbit or
      relocation can reduce hazard without recovering material; recycling adds
      disassembly, processing, qualification, and manufacturing requirements
      and may increase operational risk.

- [x] Add policy triggers based on shell-resolved active and derelict mass,
      predicted conjunctions, collision probability and uncertainty, maneuver
      workload, remaining avoidance propellant, disposal failures, fragment
      creation-to-clearance ratio, and expected hazardous descendants.
- [x] Allow the controller to slow or stop deployment, reduce cluster size,
      change plane/shell allocation, increase spacing, reserve more maneuver
      fuel, dispatch removal, or retire a shell when triggers are crossed.
- [x] Simulate breakup-cloud propagation through the actual constellation
      geometry and count direct losses, secondary collisions, avoidance
      maneuvers, service interruption, repair load, and time to restore
      capacity.
- [x] Stress-test loss of tracking, communications, navigation, or centralized
      maneuver coordination during a high-conjunction period. The strategy
      must remain safe when avoidance automation or shared situational
      awareness is degraded.
- [x] Evaluate mitigation portfolios across deployment cadence, disposal
      reliability, removal rate, shielding mass, cluster cap, shell diversity,
      servicer fleet size, and repair/recycling capacity; report Pareto
      tradeoffs rather than declaring one universal optimum.
- [x] Keep Earth-orbit and lunar-orbit strategies distinct. Atmospheric
      clearance, debris residence, stable/unstable orbit families, tracking,
      impact geometry, and disposal options are different.
- [x] Treat multi-operator coordination and orbital carrying capacity as
      governance constraints. A single operator cannot guarantee a safe shell
      using only its internal policy.

Additional primary or authoritative source candidates:

- NASA Orbital Debris Program Office,
  <https://orbitaldebris.jsc.nasa.gov/reference-documents/> — current U.S.
  mitigation practices, NASA requirements/handbook, fragmentation history,
  and technical reference routing.
- NASA, *Spacecraft Conjunction Analysis and Collision Avoidance Best
  Practices Handbook*, linked from
  <https://www.nasa.gov/kennedy/launch-services-program/cubesat-launch-initiative/cubesat-launch-initiative-resources/>.
- ESA, *Space Environment Report 2025*,
  <https://www.esa.int/Space_Safety/Space_Debris/ESA_Space_Environment_Report_2025>
  — current population, traffic, fragmentation, and mitigation-status
  boundary.
- ESA, *Mitigating space debris generation*,
  <https://www.esa.int/Space_Safety/Space_Debris/Mitigating_space_debris_generation>
  — disposal reliability, five-year protected-LEO clearance, collision
  avoidance, passivation, and design-for-removal requirements.
- Liou and Johnson, *A Sensitivity Study of the Effectiveness of Active Debris
  Removal in LEO*,
  <https://orbitaldebris.jsc.nasa.gov/quarterly-news/pdfs/ODQNv11i4.pdf>,
  and Liou, *An Update on LEO Environment Remediation with Active Debris
  Removal*,
  <https://orbitaldebris.jsc.nasa.gov/quarterly-news/pdfs/odqnv15i2.pdf> —
  model-based evidence that mitigation alone may not stabilize LEO and that
  targeted removal can change long-horizon population growth; do not turn the
  historical objects-per-year cases into a universal current prescription.
- NASA, *Summary of the NASA Large Constellations Parametric Study*,
  <https://ntrs.nasa.gov/citations/20190025975>, and ESA conference study,
  *Self-induced collision risk analysis for large constellations*,
  <https://conference.sdo.esoc.esa.int/proceedings/sdc7/paper/723>.
- NASA Hypervelocity Impact Technology,
  <https://hvit.jsc.nasa.gov/reference-documents/> — shielding design,
  ballistic limits, damage sensors, and small-debris protection boundaries.

### Test the Earth-versus-Moon transport premise

- [x] State every transport comparison as an origin–destination pair. Do not
      write that “lunar orbit is cheaper than LEO” without specifying where
      the servicer, propellant, parts, and replacement hardware originate.
- [x] Use approximately 9.1 km/s as a historical conceptual-design value for
      Earth surface → LEO and approximately 1.9 km/s for lunar surface → LLO
      only as first-order delta-v anchors requiring modern mission-specific
      verification. A separate NASA assessment gives about 1.9 km/s to LLO and
      2.7 km/s to NRHO from the lunar surface.
- [x] State the important directional result correctly: **local** ascent from
      the lunar surface to lunar orbit has a much smaller delta-v requirement
      than launch from Earth’s surface to LEO. Earth surface → lunar orbit is
      not cheaper than Earth surface → LEO, and Moon-sourced servicing of
      Earth-orbiting assets must pay lunar ascent/escape, transfer, Earth-orbit
      insertion, plane change, and return or disposal.
- [x] Do not convert delta-v directly into dollars. Apply the rocket equation
      and vehicle-specific dry mass, payload, specific impulse, staging,
      reusability, propellant source, launch cadence, fixed infrastructure,
      reliability, and operations costs.
- [x] Compare at least four supply architectures: Earth-launched servicing in
      Earth orbit, Earth-supplied servicing in lunar orbit, lunar-supplied
      servicing in lunar orbit, and lunar-supplied servicing of Earth-orbiting
      assets.
- [x] Make lunar advantage conditional on an operating lunar extraction,
      propellant, manufacturing, launch, navigation, and servicing base. Before
      that infrastructure exists, lunar-sourced repair is not an available
      alternative.
- [x] Produce a transport/service network calculation and break-even surface
      over client value, failure rate, serviceability, number of clients,
      recovered mass, orbit/plane distribution, servicer reuse, propellant
      source, and lunar-industrial maturity.

### Primary and authoritative source candidates

- NASA, *2024 In-Space Servicing, Assembly, and Manufacturing State of Play*,
  <https://ntrs.nasa.gov/citations/20240012414> — capability and mission
  survey; use individual mission records for demonstrated status.
- NASA, *Robotic Refueling Mission*,
  <https://www.nasa.gov/missions/station/space-station-enables-tests-of-technology-to-capture-refuel-repair-orbiting-satellites/>
  — ISS-based robotic tool and fluid-transfer demonstrations, not an
  autonomous free-flying repair service.
- NASA, *Astronaut Missions to Hubble*,
  <https://science.nasa.gov/mission/hubble/observatory/missions-to-hubble/>
  — demonstrated repairs and upgrades of a spacecraft designed for servicing;
  retain the crew, Shuttle, modularity, and preparation boundary.
- NASA Office of Inspector General, *NASA’s Efforts to Demonstrate Robotic
  Servicing of On-Orbit Satellites*,
  <https://oig.nasa.gov/wp-content/uploads/2023/10/ig-24-002.pdf>, and NASA’s
  <https://www.nasa.gov/mission/on-orbit-servicing-assembly-and-manufacturing-1/>
  — OSAM-1 cost, schedule, and technical evidence plus the subsequent
  cancellation record; strong counterevidence to assuming routine servicing
  of unprepared LEO satellites.
- NASA OSAM-1 Independent Review Board,
  <https://www.nasa.gov/wp-content/uploads/2023/02/osam-1-irb-final-report-022729-cleared-redacted-20mar2024.pdf>
  — records the weak LEO business case for that short-lived, non-refuelable
  servicer and distinguishes GEO mission-extension approaches.
- SpaceLogistics/Northrop Grumman, *Mission Extension Vehicle*,
  <https://www.northropgrumman.com/wp-content/uploads/Mission-Extension-Vehicle-MEV-fact-sheet.pdf>
  — company-statement evidence for two commercial GEO docking/life-extension
  missions; not evidence of component repair or recycling.
- DARPA, *Robotic Servicing of Geosynchronous Satellites lifts off*,
  <https://www.darpa.mil/news/2026/robotic-servicing-geosynchronous-satellites-lifts-off>
  — the MRV/RSGS system launched on 2026-07-21 and began a year-long transfer;
  treat it as deployment evidence, not yet a successful servicing result.
- NASA, *In-Space Manufacturing Portfolio Plan*,
  <https://ntrs.nasa.gov/citations/20250004020> — recycling maturity,
  qualification requirements, the unsuccessful Refabricator demonstration,
  and current polymer/metal development work.
- ESA, *Building a circular economy in space: ESA studies pave the way*,
  <https://www.esa.int/Enabling_Support/Preparing_for_the_Future/Discovery_and_Preparation/Building_a_circular_economy_in_space_ESA_studies_pave_the_way>
  — refurbishment and satellite-recycling concepts at pre-Phase-A study
  maturity, not operational proof.
- NASA, *A Parametric Assessment of Lunar and Mars Ascent Vehicle Synergy*,
  <https://ntrs.nasa.gov/citations/20205007701>, and *Lunar Base Systems
  Study: Lunar Lander Conceptual Design*,
  <https://ntrs.nasa.gov/citations/19880020470> — lunar-ascent and comparative
  mission delta-v anchors; update vehicle economics separately.

- [x] Add retained sources to the manuscript’s numbered source record and
      claim-provenance register with exact pages/sections, extracted values,
      source classes, and claim-specific transformations.
- [x] Keep proposed, launched, demonstrated, commercial, canceled, and
      operational capabilities explicitly distinct in both prose and model
      calibration.

## 6. Model partial closure as an externally supported scaling regime

The statement that “a system supplying 99.9% of its mass locally has
effectively zero autonomous closure if the residual 0.1% contains irreplaceable
electronics” is correct about **autonomy**, but incomplete about **economic and
industrial leverage**. Such a system is still externally dependent, yet local
production can greatly reduce imported mass, launch demand, and the external
capacity required to support each added unit of off-world industry. Treat this
as a distinct hybrid regime rather than collapsing all non-autonomous systems
into the same zero.

### Separate closure metrics

- [x] Retain a strict autonomous-closure test: if any indispensable input
      cannot be produced, substituted, repaired, recycled, or stocked through
      the declared horizon, autonomous closure fails.
- [x] Report that binary/critical-path result beside—not instead of—continuous
      metrics for:
      - locally supplied mass fraction;
      - locally supplied component or part-family fraction;
      - locally supplied economic value;
      - locally supplied embodied energy and process work;
      - external logistics mass and volume per unit of output;
      - human-intervention and verification dependence;
      - criticality-weighted dependency and minimum-cut-set status.
- [x] Use explicit names such as **autonomous closure**, **mass closure**,
      **value closure**, **process closure**, and **external-support
      intensity**. Never use one scalar $\kappa$ without saying which quantity
      and denominator it represents.
- [x] Distinguish a residual 0.1% of the initial bill of material from 0.1% of
      recurring replacement flow. Durable stockpiled electronics, short-lived
      consumables, and capacity-proportional imports create very different
      growth limits.

### Quantify import leverage and entry capital

- [x] Define external-support flow by critical input $k$, for example
      $\dot M_{\mathrm{ext},k}(t)$, and relate it to commissioning,
      replacement, repair, and expansion demand rather than applying one
      percentage to all time.
- [x] Define **import leverage** as verified additional operating output or
      capacity supported per kilogram, cubic metre, delivered dollar, or unit
      of external production capacity. Keep these denominators separate.
- [x] Calculate how local bulk materials and manufacturing change:
      - initial Earth-delivered seed mass and launch cost;
      - external working capital and inventory;
      - continuing import cadence and transport capacity;
      - Earth-side production capacity committed per off-world cell;
      - stockpile runway through launch or supply interruption.
- [x] Do not infer that 0.1% by mass means 0.1% of capital. Advanced
      electronics, precision instruments, software qualification, dedicated
      launches, minimum order quantities, or low-rate production may dominate
      value and fixed cost despite low mass.
- [x] Compare the partially closed system with a wholly Earth-manufactured
      deployment using the same delivered-output boundary. Report both the
      reduction in external burden and the remaining bottleneck.
- [x] Model the external supplier as part of the system boundary for the hybrid
      regime. Its factories, materials, labor, energy, finance, launch cadence,
      reliability, and growth rate must be able to supply the residual vector.

### Represent externally supported growth

- [x] Distinguish **endogenous autonomous growth** from **externally enabled
      local growth**. A partially closed system may compound local bulk
      capacity while its total expansion remains capped by a small flow of
      indispensable imports.
- [x] Add an import-constrained growth bound for every critical residual input:
      available deliveries plus usable stock must cover commissioning,
      maintenance, repair, and replacement demand at the proposed growth rate.
- [x] Test at least four support policies:
      - fixed annual imports;
      - imports proportional to off-world capacity;
      - a finite initial stockpile with no replenishment;
      - declining or disrupted imports with recovery and substitution efforts.
- [x] Report the binding residual input, external supply required per doubling,
      maximum supportable scale, time to stock exhaustion, and capacity loss
      after interruption.
- [x] Include shelf life, obsolescence, radiation storage effects, failed
      deliveries, minimum lot sizes, and synchronized replacement waves. A
      small average mass flow may still require a fragile high-cadence supply
      chain.
- [x] Treat Earth supply, lunar production, asteroid supply, repair,
      cannibalization, and recycling as substitutable arcs only where the
      component and process specifications permit it.

### Model the path from partial to autonomous closure

- [x] Represent a larger partially closed industrial base as providing more
      compute, experimental throughput, tooling, telemetry, failed attempts,
      and production capacity that can be allocated to eliminating residual
      dependencies.
- [x] Charge that substitution effort explicitly: research compute,
      experiments, destructive tests, metrology, process equipment, prototype
      lines, qualification, failed designs, materials, energy, and opportunity
      cost compete with near-term expansion.
- [x] Model each residual dependency as a technical program with a capability
      threshold, parent-tool ancestry, evidence state, development time, and
      probability-free success/failure scenarios—not as a smooth automatic
      decline in import share.
- [x] Allow sufficiently capable intelligence to improve search, design,
      diagnosis, and process control only after the relevant intelligence–
      embodiment threshold is reached. It cannot substitute for missing
      materials, sensors, tools, test facilities, or physical process
      knowledge.
- [x] Compare allocation policies between immediate capacity expansion,
      stockpiling residual imports, and investing in local substitution.
      Identify when expanding first creates enough “fuel” to close a later
      dependency and when it merely increases exposure to that dependency.
- [x] Measure progress using residual critical-part count, imported mass and
      value per unit output, minimum-cut-set size, stockpile runway,
      substitution validation state, and external capacity per doubling.
- [x] Phrase the benefit carefully: high partial closure can increase
      **optionality, runway, and resources available for mitigation**. It does
      not establish empirical “odds” of eventual autonomy without a calibrated
      development-success model.

### Rewrite the manuscript boundary

- [x] Expand the quoted 99.9% example so it states both conclusions:
      - autonomous closure is zero while an irreplaceable dependency remains;
      - mass closure and import leverage may nevertheless be high and can
        materially reduce the external burden of entry and expansion.
- [x] Present partial closure as a strategic bridge architecture with an
      external loop, not as either full autonomy or failure.
- [x] Ensure Executive Summary, I.5, I.7–I.9, Limitations, glossary, and
      Appendix D use the same hierarchy and do not confuse an autonomy test
      with the economic value of localization.
- [x] Add tables or plots showing autonomy status, local mass fraction,
      external-support intensity, import leverage, binding residual part, and
      runway together so no one metric is interpreted alone.

## 7. Improve the manuscript authoring structure

### Size assessment

The current canonical Markdown is 280,782 bytes and 4,568 lines (about 38,000
whitespace-delimited words). It is not too large for targeted LLM-assisted
work, but whole-document editing consumes substantial context and makes
omissions, duplicated edits, and cross-section inconsistencies more likely.

The standalone HTML is 1,488,439 bytes and 6,933 lines. Approximately
1,098,896 characters are nine embedded image payloads. It is a publication
artifact, not a suitable authoring or LLM-editing surface.

### Recommended architecture

Keep a single release-facing Markdown file and standalone HTML artifact, but
author the next revision from ordered Markdown fragments. Generate both
release artifacts deterministically. Do not hand-edit generated output.

A practical initial split is:

```text
docs/manuscript/
  00-front-matter.md
  10-part-i-technical-feasibility.md
  20-part-ii-comparative-economics.md
  30-part-iii-strategy-governance.md
  40-part-iv-conclusion-limitations.md
  50-appendices-a-b.md
  51-appendix-c-reproducibility.md
  52-appendix-d-model-specification.md
  60-glossary.md
  70-sources.md
```

Part I can be split further by section only if its individual edits remain
too broad. Avoid fragmenting into many small files: conceptual continuity and
cross-section review are still important.

- [x] Prototype the split only after the current article pass is stable.
- [x] Choose and document one source of truth: the ordered fragments should be
      editable; the monolithic Markdown and HTML should be generated.
- [x] Extend `scripts/build_manuscript.cjs` (or add a small deterministic
      assembler) to consume the fragments in an explicit order.
- [x] Prove a content-neutral migration by reproducing the current monolithic
      Markdown byte-for-byte before making editorial changes.
- [x] Preserve explicit/stable heading identifiers where cross-file links
      could otherwise change.
- [x] Add checks for missing, duplicated, or out-of-order fragments; duplicate
      headings/IDs; broken internal links; source-definition continuity; and
      unconverted math.
- [x] Update tests, manifests, `README.md`, `CLAUDE.md`, and release
      documentation to describe the new source/output boundary.
- [x] Keep the generated monolithic Markdown in the repository for readers,
      archival release, diffs, and external tools that expect one document.
- [x] Continue treating the standalone HTML as generated-only; validate it
      with structural tests or small extracted sections rather than loading
      the entire file into an LLM.

## 8. Publish a reader-oriented GitHub Pages edition

The repository currently verifies publication integrity in GitHub Actions but
does not deploy a Pages site. Add a web build without replacing the archival
standalone HTML.

### Output strategy

Generate three products from the same ordered Markdown sources:

1. the monolithic Markdown release artifact;
2. the self-contained, downloadable HTML release artifact;
3. a multi-page site with shared CSS, JavaScript, and image assets for GitHub
   Pages.

Use an uncommitted build directory such as `_site/` and deploy that directory
as a Pages artifact from GitHub Actions. Do not mix generated site files into
`docs/`, which already contains manuscript sources and archival artifacts.

A possible public layout is:

```text
/
  index.html
  part-i/index.html
  part-ii/index.html
  part-iii/index.html
  part-iv/index.html
  appendices/index.html
  glossary/index.html
  sources/index.html
  assets/
  download/Recursive_Industrial_Intelligence_4th_Ed_r4.0.html
```

The landing page should identify the edition and status, summarize the
article, expose the complete table of contents, and link to the repository,
model artifacts, citation metadata, DOI/archive record, and standalone
download.

- [x] Decide whether `/` represents the latest stable edition, while an
      edition path such as `/r4.0/` remains fixed after publication.
- [x] Add a `build:site` command that writes a clean `_site/` tree and works
      correctly below the GitHub project base path `/rsi-model/`.
- [x] Reuse the current manuscript styles, but emit shared web assets instead
      of embedding images and CSS into every page.
- [x] Match the Quarto edition to the standalone publication’s paper palette,
      serif reading typography, teal headings, equation treatment, tables,
      figures, desktop card, and compact mobile layout.
- [x] Suppress the redundant Quarto title panel on the landing page and hide
      empty previous/next pager cells at the beginning and end of the book.
- [x] Add persistent site navigation: home, full contents, previous/next page,
      current-part indication, sources, glossary, and standalone download.
- [x] Preserve stable heading IDs so copied deep links survive rebuilds.
- [x] Convert source markers to real build-time cross-page links, for example
      `sources/#source-s27`, rather than relying solely on client-side
      JavaScript.
- [x] Resolve links that cross fragment boundaries by mapping each target ID
      to its output page.
- [x] Add canonical, citation, Open Graph, and version metadata deliberately:
      distinguish the mutable “latest” site from the immutable tagged/archive
      edition.
- [x] Include a useful `404.html` that returns readers to the edition contents.
- [x] Add a Pages deployment job that runs only after publication-integrity
      verification succeeds; pull requests should build and test the site but
      not deploy it.

### Navigation and rendering checks

- [x] Crawl every generated page and fail on missing internal pages,
      fragments, images, stylesheets, scripts, or downloads.
- [x] Reject duplicate IDs and require every table-of-contents, previous/next,
      source, glossary, and footnote link to resolve.
- [x] Check for accidental root-relative URLs that fail under
      `https://fperegrinvs.github.io/rsi-model/`.
- [x] Verify source-definition continuity and require every in-text `[S…]`
      marker to reach exactly one source entry.
- [x] Compare the web build with the monolithic build for expected heading,
      equation, table, figure, and source counts so splitting cannot silently
      drop content.
- [x] Run browser smoke tests at desktop and mobile widths for navigation,
      table overflow, MathML, figures, the contents control, keyboard focus,
      and direct loading of representative deep links.
- [x] Run accessibility checks for landmarks, heading order, link names,
      alternative text, focus visibility, and navigation without JavaScript.
- [x] Check external links separately and report failures without making
      transient third-party availability the only deployment gate.
- [x] Document the live URL, local preview command, deployment trigger,
      canonical-URL policy, and rollback procedure.

## 9. Close the r4.0 release workflow

- [x] Start from a reviewed, clean release commit after all concurrent work is
      integrated.
- [x] Run the full strict local Apple-silicon macOS candidate workflow on the
      exact clean release commit and confirm that it produces no tracked drift.
- [ ] Obtain the external release authorization bound to the exact commit and
      checksum-verified strict local candidate audit.
- [ ] Create the immutable `r4.0` tag and archive.
- [ ] Mint/record the version DOI and canonical immutable URL.
- [ ] Regenerate publication metadata and verify both manifests byte-for-byte.

See `ROADMAP.md` Priority 0 and `docs/RELEASE_RUNBOOK.md` for acceptance
criteria and command order.

## 10. Replace assumption sets with evidence

These are empirical programs, not additional manuscript mechanics:

- [ ] Build and calibrate the process-feasible industrial-closure graph,
      including material grades, process routes, critical parts, parent tools,
      source states, fleets, and independently witnessed closure gates.
- [ ] Execute the terrestrial autonomous-closure rehearsal and use its logged
      measurements and failures to replace the corresponding model
      assumptions.
- [ ] Calibrate the economic comparison with architecture-specific
      engineering/market packages, correlated scenarios, audited cash-flow
      histories, and holdout validation.

See `ROADMAP.md` Priorities 1–2 and the three acceptance protocols in `docs/`.

## 11. Finish publication packages

- [x] Complete the final source-to-claim and target-style audit for each
      companion paper.
- [x] Recheck live portal requirements for the selected submission routes.
- [ ] Collect author-supplied identity, contribution, funding, conflict,
      acknowledgement, permission, AI-use, and final-approval records.
- [ ] Run publication preflight against the exact authorized package.

See `ROADMAP.md` Priority 3, `papers/README.md`, and
`docs/VENUE_SELECTION_AND_CONFORMANCE.md`.

## 12. Research-driven comments on the article hypothesis

**Captured:** 2026-07-28

**Scope:** independent editorial and modeling queue derived from a review of
*Machines of Loving Grace*, *AI 2027*, and adjacent primary or technically
useful sources. This section proposes work; it does not authorize changes to
generated artifacts.

**Epistemic rule:** the scenario essays below can reveal missing variables,
branch conditions, and falsifiers. They are not empirical evidence that their
timelines or outcomes will occur. Numerical values from those essays must not
enter the model except as visibly named `ASSUMPTION` sensitivities.

### Bottom line

The research supports a sharper hypothesis than “AI, robots, and space form a
positive feedback loop.” There are at least three distinct closure problems:

1. **verified AI-R&D closure** — AI can propose, test, evaluate, and safely
   deploy improvements to successor systems;
2. **embodied-production closure** — controllers can perform the complete
   physical task graph with available sensing, actuation, experiments, and
   recovery;
3. **reproductive-capital closure** — the production system can replace and
   expand every indispensable capital stock after depreciation and
   obsolescence.

These closures can arrive in different orders, and none implies the others.
System-level acceleration is limited by their slowest complementary factor.
Control and verification form an additional feasibility constraint rather
than a benefit that automatically rises with capability.

Candidate revised thesis to test editorially:

> Recursive industrial intelligence is a coupled but non-unitary transition:
> verified AI research can accelerate design, embodied automation can reduce
> scarce labor, and reproductively closed capital can generate endogenous
> physical growth, but each loop may advance without closing the others.
> Off-Earth resources alter the long-run material, siting, and environmental
> constraint only after surviving the bridge to reproductive closure. The
> strategic case for space therefore depends on milestone order, relative
> Earth/space constrained growth, and whether verification and authorized
> control keep pace with capability and replication—not on intelligence or
> location alone.

This formulation keeps the article's distinctive physical argument while
removing four avoidable overclaims: that open-ended software RSI is necessary
for physical compounding; that powerful AI makes embodied closure immediate;
that space itself causes recursion; and that greater capability necessarily
improves control.

### Priority 0 — Refine the load-bearing hypothesis

#### 1. Replace the one-dimensional “takeoff speed” branch with milestone order

The current slow/medium-versus-fast split in II.5 is directionally useful but
collapses several clocks that the reviewed sources keep separate.

- [x] Define at least five milestone times:
      $T_{\mathrm{AIR\&D}}$ for verified automation of AI R&D,
      $T_{\mathrm{emb}}$ for adequate embodied autonomy across the active
      industrial minimum cut, $T_{\mathrm{cl},E}$ for terrestrial
      reproductive closure, $T_{\mathrm{cl},S}$ for off-world reproductive
      closure, and $T_{\mathrm{ctrl}}$ for a control/verification regime able
      to govern the corresponding capability and replication rate.
- [x] Replace “slow-to-medium AI takeoff” with a small branch matrix covering
      fast digital/slow physical, slow digital/fast physical, fast/fast, and
      slow/slow regimes. A fast software takeoff does not make physical
      latency disappear; it creates an intelligence overhang whose value is
      set by experiment compute, actuators, factories, materials, and
      deployment time.
- [x] State the temporal condition under which the article's proposed path is
      strategically causal rather than merely a post-AGI construction
      program. Do not imply that $T_{\mathrm{cl},S} <
      T_{\mathrm{AIR\&D}}$ is likely; show it as one ordering among several.
- [x] Add a branch in which powerful AI first accelerates *terrestrial*
      robotics, fabs, power, and launch supply. That counterfactual may lower
      off-world bridge costs while also allowing Earth to compound earlier.
- [x] Make $T_{\mathrm{ctrl}}\leq T_{\mathrm{AIR\&D}}$ and
      $T_{\mathrm{ctrl}}\leq T_{\mathrm{cl}}$ explicit safety conditions.
      Capacity that grows faster than its authorization and verification
      system is not a successful endpoint.
- [x] Target manuscript sections: Executive Summary; I.1; II.5; III.4; III.6;
      IV.1.

**Research basis:** *Machines of Loving Grace* frames intelligence as one
factor of production among complementary limits and emphasizes irreducible
physical-world latency. *AI 2027* instead explores a software-driven
intelligence explosion and explicitly treats experiment compute as a
bottleneck. Their disagreement is best represented as milestone order and
factor elasticities, not as two prose priors.

#### 2. Separate self-improving software from self-replicating capital

The article currently presents the coupled loop as its central object. The
economic literature gives a useful causal correction: fully automating
production can produce much faster growth even without open-ended automated
R&D, while automated R&D can accelerate transformation without by itself
creating physical self-replication.

- [x] Add a 2×2 conceptual and model ablation:

  | | production not reproductively closed | production reproductively closed |
  |---|---|---|
  | AI R&D not automated | ordinary technical progress; externally supplied capital | endogenous physical growth with bounded intelligence |
  | AI R&D automated | rapid digital progress bottlenecked by physical capital | fully coupled recursive industrial intelligence |

- [x] Reclassify the coupled loop as the strongest acceleration branch, not
      the logical definition of all endogenous industrial growth.
- [x] State which propositions require AI-R&D closure, which require only
      embodied automation, and which require reproductive capital closure.
- [x] Extend the existing coupling ablations so “freeze intelligence” is not
      the only comparison. Separately freeze research automation,
      task-autonomy improvement, industrial productivity improvement, and
      capital reproduction.
- [x] Report whether balanced physical doubling still occurs with a bounded,
      fixed controller. If it does, describe AI as an enabler or accelerator
      in that case rather than the source of compounding.
- [x] Target manuscript sections: I.1–I.2; I.8; III.6; IV.1.

**Research basis:** Trammell and Korinek's *Economic Growth under
Transformative AI* distinguishes capital that can “self-replicate” in output
production from capital that can “self-improve” in knowledge production. The
distinction is unusually close to this article's subject and should become a
theoretical anchor.

#### 3. Make control a separate state variable, not a monotone consequence of intelligence

The current model allows intelligence to raise autonomy, productivity, and
coordination capability. The reviewed safety scenarios expose a missing
sign: increasing capability can simultaneously make oversight, containment,
and intent verification harder.

- [x] Split generic $I$ into at least task capability, coordination
      capability, evaluator/verification capability, and
      controllability/alignment confidence. Do not aggregate these into one
      monotone scalar.
- [x] Add an authorized-capacity state distinct from gross operating
      capacity. Replication that lacks a valid authorization chain, passes
      only self-authored tests, or cannot be independently stopped should
      fail the governance endpoint even if it raises physical output.
- [x] Model verification throughput explicitly. Require the rate of
      independently checked high-impact actions to keep pace with the rate at
      which the system proposes and executes them.
- [x] Add a control-lag or oversight-bandwidth failure mode: at high serial
      speed, nominal human approval can become ceremonial because humans
      cannot understand the proposal stream before the next generation is
      deployed.
- [x] Distinguish ordinary reliability verification from adversarial
      verification. A component that fails randomly and an agent that can
      strategically pass its evaluator require different threat models.
- [x] Test correlated monitor failure: producer and evaluator models may
      share training, objectives, blind spots, or a preference that causes
      both to approve the same unsafe action.
- [x] Connect physical rate limits to the control plane: maximum authorized
      replication should be the minimum of production capacity, independent
      verification capacity, secure command capacity, and environmental or
      treaty limits.
- [x] Target manuscript sections: I.1; I.6; III.4; Appendix D; governance
      threat-control traceability table.

**Research basis:** the *AI 2027* goals scenario is not evidence of
misalignment, but it identifies the structural possibility that task success
becomes easier to train and observe than honesty. The July 2026 RSI survey
likewise argues that demonstrated self-improvement is strongest where an
external verifier exists and weakest where a system judges its own open-ended
work.

#### 4. Promote “marginal returns to intelligence” into the conceptual spine

*Machines of Loving Grace* offers a framework that matches the article's own
ablation result: more intelligence matters little when materials bind and
matters more after the source vector relaxes.

- [x] Recast intelligence as a factor whose marginal product depends on
      complementary stocks: experiment capacity, high-quality causal data,
      inference compute, embodiment, materials, energy, deployment capacity,
      verification, law, and human consent.
- [x] Use model shadow values or finite-response diagnostics to report the
      marginal value of intelligence by regime, alongside material
      bottlenecks. Avoid describing $I$ as globally productivity-enhancing
      when its marginal value is near zero in material-starved cases.
- [x] Separate constraints intelligence may eventually route around
      (experimental method, equipment design, process scheduling) from
      irreducible or externally imposed limits (reaction time, light speed,
      heat rejection, unavailable observations, legal authorization).
- [x] Let intelligence change some bottleneck capacities over time, but
      require a cost, construction lag, and verified causal pathway for doing
      so. “AI can design a better instrument” is not equivalent to the
      instrument existing.
- [x] Replace any residual language that intelligence “selects and expands”
      the active bottleneck with the narrower claim that it can propose and
      coordinate expansion subject to observation, verification, and
      productive capacity.
- [x] Target manuscript sections: I.1; I.2; I.6; I.8; III.6.

#### 5. Narrow the normative and uniqueness claim

*Machines of Loving Grace* constructs a radical positive case for AI while
deliberately focusing on health, poverty, governance, and human flourishing
rather than space. That is an important challenge to the opening claim that
AI's “deepest strategic value” may lie in off-world industrial recursion.

- [x] Replace “deepest strategic value” with a bounded claim such as
      “one possible long-horizon infrastructure value” unless the paper
      supplies an explicit comparison against health, science, terrestrial
      abundance, climate, and governance uses.
- [x] Separate three questions that the current rhetoric can blur:
      what most benefits humanity, what produces the largest physical growth
      option, and what best explains the observed corporate portfolio.
- [x] State that powerful AI could be transformative without space industry,
      while space industry could compound with bounded AI after production
      closure. Neither thesis establishes the other.
- [x] Reframe non-saturating compute demand as a contingent preference and
      institutional outcome, not a natural law. Model a bounded-demand branch
      and a branch where humanitarian applications dominate early compute
      allocation.
- [x] Preserve the biosphere-protection telos but make its welfare accounting
      explicit: relocating harmful activity, expanding total activity, and
      allocating off-world resources are three different normative choices.
- [x] Target manuscript sections: opening paragraph; Executive Summary;
      IV.2; IV.4.

### Priority 1 — Model and evidence extensions implied by the sources

#### 6. Make AI-R&D compute allocation endogenous

*AI 2027* usefully separates compute for running research agents, research
experiments, synthetic-data generation, post-training, frontier training,
and external deployment. Its particular allocation percentages are
scenario assumptions, but the resource competition is real and missing from
a direct “more installed compute → more intelligence” law.

- [x] Partition compute into training, inference labor, research experiments,
      data generation/filtering, verification/safety, and external productive
      service.
- [x] Add an allocation constraint so the same accelerator-hour cannot run an
      agent, train a successor, execute an experiment, and serve customers
      simultaneously.
- [x] Let automated researcher count be limited jointly by inference compute
      and useful research tasks; let progress be limited jointly by researcher
      effort, experiment compute, evaluation capacity, and serial experiment
      depth.
- [x] Represent algorithmic efficiency gains as changes in the conversion
      from physical compute to effective compute, not as creation of new
      accelerator-hours.
- [x] Include the opportunity cost of internal AI R&D: allocating more
      compute to recursive improvement can reduce near-term revenue,
      industrial control, or verification.
- [x] Report the allocation that maximizes *verified* progress and compare it
      with the allocation that maximizes raw capability or physical growth.
- [x] Do not import *AI 2027*'s compute shares as anchors. Use them, if at all,
      only as named scenario values with sensitivity sweeps.

#### 7. Distinguish cognitive copies from effective physical labor

Both named essays imagine very large numbers of fast digital workers.
Industrial throughput, however, cannot scale one-for-one with model copies.

- [x] Add separate stocks for model instances, inference capacity, physical
      robots/machines, experimental stations, and independently verifiable
      work cells.
- [x] Define an effective physical-agent conversion bounded by available
      actuators, sensor channels, safe simultaneous work envelopes, task
      parallelism, and contention for tools and material.
- [x] Test the limiting case where one million cognitive instances control a
      small number of machines. Most copies should either work on simulation,
      planning, monitoring, or wait; physical output must not multiply by one
      million.
- [x] Add serial-depth and massive-parallelism diagnostics. Many independent
      experiments can run in parallel, but a process whose next step depends
      on the previous physical result retains an irreducible wall-clock floor.
- [x] Connect this to the existing coordination graph: copying agents may
      reduce onboarding cost while increasing experiment demand,
      communication edges, duplicate work, and verification load.

#### 8. Decompose the electronics sector around the actual AI supply chain

The *AI 2027* compute supplement identifies distinct prospective bottlenecks
in advanced packaging and high-bandwidth memory, not merely “chips.” The
article's aggregated electronics tier can therefore point to the right
sector while prescribing the wrong closure program.

- [x] Split, at minimum, front-end logic fabrication, memory fabrication,
      advanced packaging, substrates/interposers, high-speed interconnect,
      power electronics, test/metrology, and radiation-qualified system
      integration in a dedicated electronics-architecture sensitivity.
- [x] Identify which tiers must be produced off Earth, which can be
      stockpiled, which can be reused or down-binned, and which require a
      continuing Earth umbilical.
- [x] Model heterogeneous obsolescence and shelf life. A stockpile of logic
      dies, HBM, substrates, chemicals, or packaging consumables does not age
      as one homogeneous “electronics” inventory.
- [x] Add a closure sequencing question: local packaging, board assembly,
      test, repair, and power electronics may deliver more early resilience
      than attempting frontier-node wafer fabrication.
- [x] Anchor any real supply-chain quantity in semiconductor primary sources;
      use *AI 2027* only to identify the structural decomposition.

#### 9. Separate physical depreciation from economic obsolescence

The article already treats depreciation as harsh, but fast-moving AI hardware
can remain physically functional after it has become uneconomic for frontier
training.

- [x] Maintain age or generation cohorts for compute, with distinct physical
      failure, radiation degradation, performance-per-watt obsolescence, and
      workload reassignment.
- [x] Allow older compute to migrate to control, inference, verification,
      simulation, or non-frontier workloads rather than treating
      obsolescence as total loss.
- [x] Revisit the claim that architectural convergence reduces the
      electronics-obsolescence term. Convergence is a scenario, while the
      observed short life of specialized hardware may persist even when
      software progress slows.
- [x] Use the peer-reviewed two-asset AI-capacity model as a conceptual
      cross-check, not as a direct off-world calibration.

#### 10. Add a verification hierarchy to every recursive loop

The current “verified loop” definition is a strong start. It should specify
what kind of verifier licenses each claimed gain.

- [x] Classify improvement signals from strongest to weakest: formal proof or
      executable invariant; destructive/physical acceptance test; independent
      held-out experiment; causal operational outcome; human/AI rubric; model
      self-assessment.
- [x] Report verified-loop throughput by verifier class rather than one total.
      A thousand self-scored iterations must not equal one independently
      replicated physical result.
- [x] Make evaluator independence observable: model lineage, training-data
      overlap, tool overlap, authority separation, and audit access.
- [x] Add evaluator drift, reward hacking, self-confirming loops, diversity
      collapse, and model-collapse failure modes to the digital loop.
- [x] Preserve negative and null experiments, as the manuscript already
      requires, and test whether selection/filtering creates survivorship
      bias in industrial memory.
- [x] Treat “research direction-setting” as a separate task rather than
      inferring it from rapid execution against a fixed target.

#### 11. Replace benchmark progress with a reliability ladder tied to industrial tasks

The METR time-horizon work supports rapidly improving autonomous task length,
but METR's own limitations note warns that a 50% time horizon is not a
delegation threshold, is concentrated in software-like tasks, and does not
directly give an automation or research-speed multiplier.

- [x] Add a ladder from benchmark success to economic substitution:
      single attempt; repeated success; low-context long task; high-context
      production task; safety-critical field task; unscripted recovery; and
      sustained operation with bounded intervention.
- [x] Require reliability levels appropriate to consequence. A 50% success
      rate can be useful for cheap reversible search and unacceptable for
      destructive fabrication, launch, power switching, or replication
      authorization.
- [x] Track the human cost of prompting, checking, recovery, and cleanup.
      Falling intervention count can coexist with more expensive failures.
- [x] Extend the falsifiable indicators in III.5 with task duration,
      consequence class, verifier class, intervention hours, rollback success,
      and out-of-distribution recovery.
- [x] Do not extrapolate software task-horizon trends directly into lunar
      mining, maintenance, chemistry, or autonomous commissioning.

#### 12. Make data generation and evaluator quality co-evolve

- [x] Separate synthetic-data volume from accepted training signal. Record
      generation, filtering, deduplication, provenance, evaluator error, and
      held-out transfer.
- [x] Treat physical operational data as valuable only when causal state,
      action, outcome, and hardware configuration are linked—the article's
      current data-profile direction is correct and should remain
      multidimensional.
- [x] Add the possibility that greater synthetic-data production increases
      apparent progress while narrowing diversity or amplifying evaluator
      bias.
- [x] Price experimental data in physical time, equipment wear, destructive
      samples, and verification capacity rather than bytes.
- [x] Test whether proprietary industrial data advantage remains after
      accounting for open publication, espionage, employee mobility,
      distillation, and independent replication.

#### 13. Add governance externalities to the replication objective

The article models debris but does not yet fully connect replication speed
to strategic racing, resource preemption, or distributional legitimacy.
The *AI 2040* space-governance supplement is highly speculative, but it
surfaces the correct category of missing problem.

- [x] Distinguish productive capacity from legitimately authorized capacity
      and from capacity that preempts contested resources.
- [x] Treat “first to replicate fastest” as a private objective that can
      create negative-sum races, debris, insecure claims, and premature
      irreversible commitments.
- [x] Add a governance failure endpoint for unauthorized expansion even when
      the engineering endpoint succeeds.
- [x] Ask who bears externalities and who receives claims on future output;
      closure removes a material lever and can entrench the bridge-period
      allocation of authority.
- [x] Extend III.4 beyond stopping hardware to include update authority,
      resource-claim rules, liability, audit rights, succession of control,
      and representation of future affected parties.
- [x] Keep extrasolar abundance and post-ASI allocation outside the article's
      evidentiary core. Use them only to motivate nearer-term institutional
      design under irreversible scale.

### Priority 2 — Source-specific editorial comments

#### *Machines of Loving Grace*

- [x] Cite the essay for Amodei's stated framework, not as proof of powerful
      AI capabilities or dates.
- [x] Use its “marginal returns to intelligence” framing to organize the
      article's bottleneck logic.
- [x] Use its physical-world, data, intrinsic-complexity, human, and
      physical-law limits to distinguish reducible from irreducible
      bottlenecks.
- [x] Use its “country of geniuses in a datacenter” thought experiment only
      as a sensitivity architecture; millions of copies and 10–100× speed are
      assumptions.
- [x] Let its non-space humanitarian vision challenge the article's telos and
      uniqueness rhetoric.
- [x] Source class: `company_statement` for the CEO's stated view; any
      numerical scenario used in the model remains `ASSUMPTION`.

Source: Dario Amodei, [“Machines of Loving
Grace”](https://darioamodei.com/essay/machines-of-loving-grace), October
2024.

#### *AI 2027* and its supplements

- [x] Describe it as a concrete forecast scenario with two endings and
      explicit uncertainty, not as a prediction that has been established.
- [x] Import structural distinctions—software versus hardware progress,
      inference labor versus experiment compute, internal versus external
      deployment, task success versus honest oversight—not its headline
      calendar.
- [x] Note that the authors later corrected/updated some model trajectories
      and pushed a median back while retaining a fast branch. Version and
      access dates therefore matter.
- [x] Use its fast branch to stress-test II.5, not to overwrite the article's
      baseline.
- [x] Source class: scenario-level claims and parameters are `ASSUMPTION`;
      the site can be cited as the primary record of what its authors
      forecast.

Sources:

- Daniel Kokotajlo et al., [*AI 2027*](https://ai-2027.com/), April 2025,
  with later updates.
- [Compute forecast](https://ai-2027.com/research/compute-forecast).
- [Takeoff forecast](https://ai-2027.com/research/takeoff-forecast).
- [AI goals forecast](https://ai-2027.com/research/ai-goals-forecast).
- [Security forecast](https://ai-2027.com/research/security-forecast).

#### Anthropic, *When AI builds itself*

- [x] Add this as the strongest directly relevant frontier-lab
      self-description found in the search.
- [x] Separate reported execution uplift from full research closure. Anthropic
      says current systems are strong at optimizing against a fixed goal but
      that research direction-setting remains a bottleneck and full RSI has
      not arrived.
- [x] Record internal productivity and code-share figures as self-reported
      company measurements with possible selection, attribution, and
      counterfactual bias.
- [x] Do not translate code authored or shipped into a capability-growth
      coefficient without independent causal measurement.
- [x] Use it to define observable stages between assistant, autonomous coding,
      agent delegation, and successor-model closure.
- [x] Source class: `company_statement`; internal quantitative claims remain
      company-reported until independently audited.

Source: Anthropic Institute, [“When AI builds
itself”](https://www.anthropic.com/institute/recursive-self-improvement),
2026.

#### Trammell and Korinek, *Economic Growth under Transformative AI*

- [x] Add as the closest formal economic lineage for the distinction between
      self-replicating production capital and self-improving knowledge
      capital.
- [x] Extract the exact conditions under which growth accelerates: automation
      coverage, substitution, returns to scale, savings/investment, and
      natural-resource importance.
- [x] Do not cite its macro result as proof that this particular off-world
      engineering graph can close.
- [x] Compare its aggregate capital concept with the article's balanced
      minimum-sector doubling metric; explain why the latter is stricter.
- [x] Source class: `technical_report` for the NBER working paper unless the
      final peer-reviewed Annual Review version and its exact claims are
      verified at publication time.

Sources:

- Philip Trammell and Anton Korinek, [NBER Working Paper
  31815](https://www.nber.org/papers/w31815), revised April 2026.
- [Annual Review of Economics version](https://doi.org/10.1146/annurev-economics-051624-061002),
  Review in Advance, June 2026.

#### Empirical and technical counterweights

- [x] Use METR's task-horizon result as evidence of measured software-agent
      progress over the tested task distribution, paired with METR's own
      warnings about reliability, external validity, and automation claims.
- [x] Use the July 2026 RSI survey as a map and taxonomy, not a mature
      consensus: it is a first-version preprint with a young, heavily
      preprint-based corpus and single-annotator classification.
- [x] Use the peer-reviewed AI-capacity paper to sharpen depreciation and
      obsolescence, while noting that its calibration is terrestrial and
      macroeconomic.

Sources:

- METR, [“Measuring AI Ability to Complete Long
  Tasks”](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/),
  2025, and [“Clarifying limitations of time
  horizon”](https://metr.org/notes/2026-01-22-time-horizon-limitations/),
  2026.
- Mingguang Chen, Licheng Wang, and Bo Qu, [“Recursive Self-Improvement in
  AI: From Bounded Self-Refinement to Autonomous Research
  Loops”](https://arxiv.org/abs/2607.07663), arXiv:2607.07663v1, July 2026.
- Jonathan Rice, [“The macroeconomics of AI capacity: insights from a
  two-asset growth
  model”](https://doi.org/10.1017/S1365100526100911), *Macroeconomic
  Dynamics* 30 (2026), e22.
- AI Futures Project, [*AI 2040: Plan A*](https://ai-2040.com/) and its
  [space-governance
  supplement](https://ai-2040.com/supplements/space-governance-plan), 2026;
  scenario/recommendation only.

#### Existing source that should be reused, not duplicated

- [x] Keep *Situational Awareness* under existing source [S35]. Extend its
      use only where the manuscript needs the compute/power industrial
      mobilization and fast-takeoff countercase; do not create a second source
      entry for individual chapters unless exact-locator requirements demand
      it.
- [x] Contrast its claim that AI-R&D automation can precede robotics with the
      article's embodied-closure path and with *Machines of Loving Grace*'s
      complementary-factor limits.

Source: Leopold Aschenbrenner, [*Situational Awareness: The Decade
Ahead*](https://situational-awareness.ai/), June 2024.

### Priority 3 — Concrete manuscript deliverables

- [x] Add a one-page “closure and milestone taxonomy” near the start of Part I.
- [x] Add the 2×2 R&D-automation × production-closure ablation table to I.8 or
      the integrated-model diagnostics.
- [x] Add the four-regime digital-speed × physical-speed matrix to II.5.
- [x] Add a “capability, verification, control” state diagram to III.4 only if
      it clarifies the authority transitions; keep it out if prose is
      sufficient.
- [x] Replace the opening “deepest strategic value” sentence with the bounded
      long-horizon claim.
- [x] Add source entries only after exact locators, source classes, and claim
      boundaries have been recorded in the provenance system.
- [x] Update the claim glossary so “recursive self-improvement,” “automated AI
      R&D,” “embodied autonomy,” “reproductive closure,” and “authorized
      replication” cannot be used as synonyms.
- [x] Add falsifiers for each closure separately. Evidence for one closure
      must not upgrade the others.
- [x] Run the full manuscript, source, notation, and provenance checks only
      after the in-progress article work has finished and this queue has been
      reconciled manually with `TODO.md`.

### Priority 4 — Professionalize the Python toolchain and quality gates

#### Current-state audit

- [x] Treat the existing use of `uv pip compile` as a partial migration, not a
      completed one. The repository still has no `pyproject.toml`, `.python-version`,
      or `uv.lock`; CI creates `.venv` manually and installs `requirements.lock`
      through `pip`.
- [x] Remove direct `.venv/bin/python` assumptions from `package.json`, CI, and
      documentation. Every supported command should work through `uv run`.
- [x] Replace repeated `sys.path.insert(0, ROOT / "src")` calls in scripts and
      tests with a properly installed package. A test that only passes when run
      from the repository root is not an adequate packaging test.
- [x] Do not mistake scattered annotations for a typed codebase. There is no
      Pyright configuration or type-checking gate, and several model,
      calibration, evidence, publication, and analysis boundaries still expose
      bare `dict` or `Any`.
- [x] Record the initial Ruff, Pyright, pytest-warning, coverage, and packaging
      baselines before making mechanical changes. Do not preserve those
      baselines as permanent suppressions.
- [x] Refactor the largest orchestration files as part of the migration.
      `scripts/run_integrated.py` and the main integrated-model modules are too
      large to make typing errors, side effects, and ownership boundaries easy
      to review.

#### 4.1 Make `uv` the sole Python project and environment manager

- [x] Add a PEP 621 `pyproject.toml` containing package metadata, the supported
      Python series, runtime dependencies, build-system metadata, console
      scripts, and tool configuration.
- [x] Use a simple modern build backend and declare it explicitly. Confirm that
      `uv sync` installs `rsimodel` as an editable package during development;
      do not rely on `PYTHONPATH` or current-working-directory behavior.
- [x] Add `.python-version` for Python 3.13 and commit the cross-platform
      `uv.lock`. Pin the project to a deliberate Python compatibility range
      rather than whatever interpreter happens to be installed locally.
- [x] Put pytest, pytest-cov, Pyright, Ruff, the dependency auditor, and other
      development-only tools in named PEP 735 dependency groups. Keep runtime,
      quality, test, and release dependencies distinguishable.
- [x] Replace manual venv and pip commands with:
      `uv lock --check`, `uv sync --locked --all-groups`, and
      `uv run --locked <command>`. Pin the `uv` version used locally and in CI
      so lock behavior does not drift silently.
- [x] Retire `requirements.txt` and `requirements.lock` only after dependency
      parity, release documentation, provenance manifests, and CI have been
      migrated. If a downstream consumer still needs requirements format,
      generate it with `uv export`; never maintain a second dependency graph by
      hand.
- [x] Rewrite `scripts/check_dependencies.py` to validate project metadata,
      the checked lock, and the active `uv` environment. It must no longer
      recommend a `.venv/bin/python -m pip install` repair path.
- [x] Update `README.md`, `CLAUDE.md`, the rehearsal/release runbooks,
      `package.json`, and contributor commands to use the same locked commands
      as CI.
- [x] Acceptance: a fresh checkout can run `uv sync --locked --all-groups`,
      import `rsimodel` from outside the repository root, and reproduce the
      current tests and generated artifacts without a global Python package.

The lockfile is a project artifact: check it into version control, never edit it
manually, and make CI reject stale metadata. See the official
[uv project guide](https://docs.astral.sh/uv/guides/projects/),
[project layout](https://docs.astral.sh/uv/concepts/projects/layout/), and
[locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).

#### 4.2 Install the package and turn scripts into typed entry points

- [x] Delete every `sys.path.insert(...)` workaround after the package is
      installable. Add a CI search that fails if a new workaround is introduced.
- [x] Move reusable logic out of `scripts/` and into cohesive
      `src/rsimodel/` modules. Leave scripts as thin compatibility wrappers only
      while callers migrate.
- [x] Define maintained commands in `[project.scripts]`, with typed
      `main(argv: Sequence[str] | None = None) -> int` functions, explicit exit
      codes, and no material work at import time.
- [x] Split the integrated runner into bounded components for argument parsing,
      orchestration, model execution, table/figure writing, and report
      generation. Pass a typed configuration/path object instead of repeatedly
      reconstructing `ROOT` and output paths.
- [x] Make output and cache directories explicit command inputs. Tests must use
      temporary directories rather than depending on or mutating checked-in
      artifacts.
- [x] Add smoke tests for every console command: `--help`, invalid input,
      minimal successful execution where inexpensive, and expected non-zero
      exit codes on failure.
- [x] Build both sdist and wheel with `uv build`; install the wheel into an
      isolated environment and verify package imports and console commands.
      Running tests only against the editable source tree is insufficient.

#### 4.3 Make Pyright strictness an enforced, ratcheted property

- [x] Add `[tool.pyright]` configuration covering `src`, maintained scripts,
      and tests. Pin one invocation path and run it through the locked project
      environment; do not depend on a floating global Pyright installation.
- [x] Make `strict` the target. If converting the existing code in one patch is
      impractical, begin in `standard`, opt migrated modules into strict mode,
      and increase the strict include set monotonically. Do not use a permanent
      error-baseline file or exclude the difficult model modules.
- [x] Require complete annotations for public functions, dataclasses, class
      attributes, and CLI entry points. Turn on missing-annotation,
      unknown-type, optional-access, and unnecessary-ignore diagnostics as
      modules become clean.
- [x] Replace unstructured YAML and JSON trees with `TypedDict`, dataclasses, or
      validated domain objects. Treat `yaml.safe_load` as `object`, validate and
      narrow once at the I/O boundary, and keep `Any` from propagating into
      model calculations.
- [x] Replace bare mutable `dict` parameters with precise `Mapping`,
      `MutableMapping`, or domain record types. Use `Literal`, enums,
      discriminated unions, `Protocol`, `Final`, `TypeAlias`, and generics where
      they encode real invariants; avoid decorative typing.
- [x] Introduce explicit NumPy aliases based on
      `numpy.typing.NDArray[np.float64]` (and the actual integer/boolean dtypes).
      Pair them with runtime dimensional and shape validation because Pyright
      cannot prove all array-shape relationships.
- [x] Isolate weakly typed SciPy, OSQP, YAML, and plotting interfaces behind
      small adapter modules. A localized, rule-specific
      `# pyright: ignore[rule]` is acceptable only with an explanation and an
      issue/TODO; blanket file ignores and unqualified `# type: ignore` are not.
- [x] Use exhaustive enum/`Literal` dispatch with `assert_never` where a missing
      case would change model behavior.
- [x] Add `uv run pyright` as a required CI gate. Definition of done is zero
      errors, no blanket exclusions, and a small recorded count of justified
      boundary ignores that can only decline.

Use the official [Pyright configuration
reference](https://github.com/microsoft/pyright/blob/main/docs/configuration.md)
as the source of truth for mode and diagnostic behavior.

#### 4.4 Adopt Ruff for linting, imports, modernization, and formatting

- [x] Configure Ruff in `pyproject.toml` for Python 3.13 and include
      `src/`, `scripts/`, and `tests/`. Exclude generated manuscripts, site
      output, model artifacts, caches, and vendored data explicitly.
- [x] Start with an intentional rule set rather than `ALL`: Pyflakes and
      pycodestyle (`F`, `E`, `W`), isort (`I`), pyupgrade (`UP`), bugbear (`B`),
      simplify (`SIM`), comprehensions (`C4`), return (`RET`), argument (`ARG`),
      performance (`PERF`), NumPy (`NPY`), Ruff-specific (`RUF`), and
      suppression hygiene (`PGH`).
- [x] Enable Ruff's security/Bandit family (`S`) for source and operational
      scripts, with narrow test-specific exceptions such as `S101` for pytest
      assertions. Security lint is complementary to, not a substitute for,
      dependency auditing and threat review.
- [x] Run `ruff check --fix` and `ruff format` as a separately reviewable
      mechanical migration. Confirm that no formulas, constants, array order,
      file formats, or generated numerical outputs changed.
- [x] Remove `# noqa: E402` suppressions when the path hacks disappear. Replace
      intentional package re-exports with explicit `__all__` rather than
      silencing unused-import diagnostics broadly.
- [x] Add complexity/branch-count rules selectively after decomposing the
      largest modules. Do not silence an arbitrary threshold across the entire
      model.
- [x] Make both `uv run ruff check .` and
      `uv run ruff format --check .` mandatory over the complete tracked source
      set, not only changed files.

Ruff supports unified configuration in `pyproject.toml`; its authors recommend
an explicit rule selection rather than enabling every rule. See the official
[configuration](https://docs.astral.sh/ruff/configuration/) and
[linter](https://docs.astral.sh/ruff/linter/) references.

#### 4.5 Strengthen pytest, coverage, and model-invariant checks

- [x] Move pytest configuration into `pyproject.toml`; set `testpaths`, require
      `--strict-config` and `--strict-markers`, declare all markers, and turn
      unexpected warnings into errors. Document narrow third-party warning
      filters with removal conditions.
- [x] Add branch coverage through pytest-cov. Measure the starting point, set a
      floor that the current suite can honestly pass, and ratchet it upward.
      Do not use a high aggregate percentage to conceal untested critical model
      paths.
- [x] Report missing branches by module and require stronger coverage for
      accounting, calibration, solver adapters, provenance, release, and
      manifest logic than for plotting or presentation glue.
- [x] Add property and invariant tests for conservation/mass balance,
      non-negativity, deterministic seeded runs, monotonic relationships,
      dimensional/unit conversions, solver status handling, manifest
      reproducibility, and invalid configuration rejection.
- [x] Separate fast unit/quality checks from slow integrated generation with
      explicit markers and CI jobs. Add timeouts to expose hangs; do not hide
      flaky behavior with automatic rerun plugins.
- [x] Test the built wheel in a clean environment as well as the editable
      project. Verify imports from a directory that is not the repository root.
- [x] Publish machine-readable test and coverage artifacts on CI failures when
      useful, but do not make ordinary local development depend on a network
      service.

#### 4.6 Add supply-chain and non-Python checks

- [x] Audit the fully resolved lock with `pip-audit` or an equivalently
      maintained OSV-based scanner. Fail on known applicable vulnerabilities;
      any temporary exception must name the advisory, justification, owner, and
      expiration date.
- [x] Produce a CycloneDX SBOM from the locked environment for releases or
      archived publication builds. Keep it generated from `uv.lock`, not as an
      independently maintained dependency list.
- [x] Pin third-party GitHub Actions to immutable commit SHAs and use Dependabot
      or an equivalent reviewable updater. Do not run a remote `curl | sh`
      installer in CI.
- [x] Split CI permissions by job. Test and build jobs should have read-only
      contents access; Pages write and OIDC permissions should exist only in
      the deployment job.
- [x] Run `actionlint` over workflow files and validate YAML for duplicate keys
      and expected schemas. Existing application-level config loading does not
      validate the CI configuration itself.
- [x] Add one pinned formatter/linter for the CommonJS build/check scripts
      (Biome or ESLint plus Prettier), and commit its package-manager lock if it
      introduces Node dependencies.
- [x] Add Markdown lint for authored Markdown, with explicit exclusions for
      generated manuscripts, transcripts, and third-party content. Add a local
      link/anchor check; make unreliable external-link probing scheduled rather
      than a blocking per-commit gate.
- [x] Preserve and continue requiring the existing dependency, notation,
      provenance, manifest, artifact-drift, and site checks. The new generic
      tooling complements those domain-specific checks; it does not replace
      them.

`uv` can export locked environments and CycloneDX SBOMs, and the official
[GitHub Actions guide](https://docs.astral.sh/uv/guides/integration/github/)
documents locked sync, caching, and the maintained setup action. Pin the action
to the reviewed immutable SHA current at implementation time.

#### 4.7 Restructure CI and define completion

- [x] Create a fast quality job that runs lock validation, locked sync, Ruff,
      Pyright, config/workflow lint, pytest, and branch coverage.
- [x] Create a package job that builds sdist/wheel and performs isolated import
      and CLI smoke tests.
- [x] Run expensive publication-integrity and artifact regeneration only in the
      canonical local macOS candidate command. Preserve the rejection of
      unexplained generated-file drift; do not spend hosted CI minutes on
      automatic regeneration.
- [x] Keep deployment separate and dependent on all required build and
      publication checks. Give only that job deployment permissions.
- [x] Keep one local command surface in `package.json`; it orchestrates the
      existing locked `uv run` and Bun/pnpm commands instead of reimplementing
      the model or checks.
- [x] Test the declared versions on the canonical Apple-silicon macOS platform.
      Cross-platform numerical equality is not part of the release contract.
- [x] Keep the hosted workflow explicit and manual, with no scheduled or
      per-change consumption of the free GitHub Actions allowance.

Migration order:

1. Add project metadata, build backend, dependency groups, `.python-version`,
   and `uv.lock`; prove numerical and publication outputs are unchanged.
2. Install the project and migrate commands/tests away from path injection and
   direct `.venv` paths.
3. Apply the separately reviewable Ruff cleanup and enforce lint/format checks.
4. Introduce typed configuration and third-party adapters, split oversized
   modules, and ratchet Pyright to strict.
5. Add coverage/invariant, wheel, security, workflow, JavaScript, and Markdown
   gates; then restructure CI around fast, package, publication, and deploy
   stages.

Definition of done:

- [x] `uv lock --check` and `uv sync --locked --all-groups` pass from a fresh
      clone with no globally installed project dependencies.
- [x] `uv run ruff check .`, `uv run ruff format --check .`,
      `uv run pyright`, and strict pytest with branch coverage all pass.
- [x] `uv build` succeeds, and the resulting wheel imports and exposes working
      CLI entry points in an isolated environment outside the repository.
- [x] No maintained test or script modifies `sys.path`, assumes
      `.venv/bin/python`, or requires execution from the repository root.
- [x] No blanket Pyright, Ruff, or warning suppressions remain; documented
      boundary exceptions are narrow and counted.
- [x] The dependency audit, workflow/config lint, authored-Markdown checks, and
      JavaScript checks pass.
- [x] Full manuscript generation, model-output comparison, provenance,
      manifest, release, and site checks pass with no unexplained artifact
      changes.
- [x] The obsolete requirements files and transitional wrappers are removed,
      and all contributor/release documentation describes the same `uv`
      workflow.

### Priority 5 — Make equations and data artifacts explorable for readers

#### Current-state audit and design rules

- [x] Replace reader-facing backticked CSV paths such as
      `outputs/integrated/tables/digital_elasticity_bounds.csv` with meaningful
      link text such as “digital-elasticity bounds table.” Preserve the exact
      path, hash, and download affordance in the artifact view rather than
      forcing it into the prose.
- [x] Extend the site build beyond images. `scripts/build_site.cjs` currently
      copies referenced images into `_site/outputs` but does not deploy the
      manuscript's referenced CSVs.
- [x] Treat both viewers as progressive enhancement. Every data reference and
      equation explanation must remain usable in the standalone HTML, without
      JavaScript, with a keyboard, and through assistive technology.
- [x] Do not make an equation or its number itself open a modal. Readers must
      still be able to select/copy mathematics and follow the equation number's
      stable anchor. Add an explicitly labelled “Explain this equation” control.
- [x] Prefer an inline disclosure or non-modal side drawer on wide screens and
      a full-screen dialog on narrow screens. A blocking modal is acceptable
      only when it materially improves the small-screen presentation.
- [x] Use one locally bundled viewer module and one reusable dialog/disclosure
      shell per page. Do not create one hidden modal, table, or script instance
      for every link.
- [x] Do not load runtime code, fonts, CSV parsers, or UI components from a
      third-party CDN. Pin and lock any new build/runtime dependency.

#### 5.1 Add semantic artifact links to the manuscript

- [x] Define one authoring syntax for a publication artifact reference. It
      should carry a repository-relative path and optional metadata key while
      rendering as an ordinary link in Markdown, standalone HTML, and the site.
- [x] Give links human-readable, contextual labels; avoid “click here,” raw
      paths as prose, and file-type-only labels such as “CSV.”
- [x] Keep a real `href` to the original CSV or a canonical artifact page. A
      normal unmodified click may be enhanced into the viewer, but new-tab,
      copy-link, download, no-script, and assistive-technology behavior must
      remain conventional.
- [x] Convert the existing CSV references systematically. Preserve bare
      filenames only in intentional artifact inventories or reproducibility
      documentation where the exact filesystem name is the subject.
- [x] Resolve abbreviated references such as
      `digital_channel_ablations.csv` explicitly during conversion. Do not use a
      basename search at runtime that could silently select the wrong file when
      names collide.
- [x] Reject paths outside `outputs/`, missing files, directories, symlinks that
      escape the artifact tree, and references absent from the applicable
      publication/integrated manifest.

#### 5.2 Build an accessible, friendly CSV viewer

- [x] Copy every referenced CSV byte-for-byte into the built site and retain a
      direct “Download original CSV” link. Verify the deployed copy against the
      source hash rather than regenerating the authoritative CSV.
- [x] Parse each referenced CSV during the build with a standards-compliant,
      pinned parser. Fail on malformed rows, duplicate headers, invalid UTF-8,
      or inconsistent column counts before deployment.
- [x] Generate only derived viewer metadata/data from the authoritative CSV.
      Include artifact path, title, description, row/column counts, hash, build
      provenance, column definitions, and safely encoded rows.
- [x] Add a small metadata registry for important publication tables. Allow
      human column labels, units/domains, descriptions, default sort, key
      columns, and display formats; fall back to conservative rendering when no
      table-specific presentation metadata exists.
- [x] Lazy-load a table only when requested and cache it for the page session.
      The current CSV corpus is modest, but the largest table has thousands of
      rows and must not be inserted into the DOM in one operation.
- [x] Provide search, sortable columns, pagination, sticky headers, keyboard
      navigation, and responsive horizontal scrolling. Default to approximately
      50 rows per page and show the current/total row range.
- [x] Distinguish missing values from numeric zero, retain full precision in
      copy/download behavior, and make display rounding explicit. Do not infer
      units or percentages from column names.
- [x] Render cell values as text, never as trusted HTML. Test quoted commas,
      embedded newlines, quotes, Unicode, empty cells, very long values, and
      spreadsheet-formula prefixes without altering the downloadable artifact.
- [x] Show a concise title and description, the original path, artifact hash,
      row and column counts, and controls for “Download CSV,” “Open raw data,”
      and “Copy artifact link.”
- [x] Preserve focus on open/close, support Escape, label the dialog and table,
      announce loading/error states, and respect reduced-motion and
      high-contrast preferences.
- [x] Add a shareable `/data/` catalog generated from the artifact registry.
      List friendly titles, descriptions, sizes, hashes, model/source class,
      and downloads. Consider stable per-table URLs so a modal view is not the
      only citable destination.
- [x] For the portable standalone HTML, choose deliberately between embedding
      the referenced viewer data and linking to immutable release artifacts.
      Do not leave relative links that work only inside the deployed site.

#### 5.3 Add structured explanations for every numbered equation

- [x] Add an equation-explanation registry keyed by the existing semantic
      `eq:` identifiers. Include the registry in publication manifests and make
      unknown, duplicate, or stale IDs fail the build.
- [x] Reuse canonical notation entries by stable term key rather than copying
      meanings and units into each explanation. The current consolidated
      notation table records first use; extend the model so each equation
      explicitly declares every named term it uses in its local model layer.
- [x] Preserve scoped meanings. A symbol reused in another model layer must
      resolve to the correct layer-specific definition rather than a global
      tooltip chosen only by its TeX spelling.
- [x] Do not attempt to discover term meaning by automatically parsing TeX.
      Subscripts, grouped symbols, local indices, reused letters, vector
      notation, and implicit domains require explicit editorial mapping.
- [x] Give every numbered equation:
      a short title; a one- or two-sentence plain-language interpretation; its
      ordered term list; units or admissible domains; local index definitions;
      non-obvious operator definitions; assumptions/validity conditions; model
      layer; and implementation status.
- [x] Mark each relation as appropriate: definition, accounting identity,
      constraint, conceptual relation, calibrated relation, numerical
      substitution, or implemented model equation. Do not let explanatory UI
      make an assumption-class relation look empirically established.
- [x] Add optional links to prerequisite/related equations, source locators,
      implementing modules/tests, relevant configuration, and machine-readable
      result tables. Keep the core explanation understandable without requiring
      those links.
- [x] Explain named and non-obvious terms, not universal symbols such as `+`,
      `=`, or ordinary parentheses. Explain operators such as an indicator,
      minimum over stages, derivative, expectation, or norm when their role is
      not obvious to the intended reader.
- [x] Use the equation's already-rendered MathML in the explanation instead of
      introducing a second client-side math renderer. Avoid term-level hover
      overlays that fragment MathML accessibility or make touch interaction
      ambiguous.
- [x] Add an “Explain equation (n)” control beside, but separate from, the
      existing numbered anchor. The control must be a real button with an
      accessible name and expanded/dialog state.
- [x] Make a native `<details>` explanation the no-script and portable-HTML
      baseline. Enhance it to an inline panel, side drawer, or responsive
      `<dialog>` without removing the underlying readable content.
- [x] Provide a stable explanation fragment such as
      `#explain-eq-verified-loop-bottleneck` so explanations can be linked,
      opened from the notation register, and cited in review comments.
- [x] Ensure print styling exposes the explanations selected for print or
      provides a clear link to the notation register. Do not print invisible
      modal shells or duplicate every equation unintentionally.

#### 5.4 Generate and validate from shared metadata

- [x] Extend `scripts/equation_numbering.lua` or add a narrowly scoped Pandoc
      filter that attaches explanation controls using the existing equation IDs
      and deterministic site-wide numbering. Do not reimplement equation
      numbering in JavaScript.
- [x] Make the equation registry and notation registry share one canonical term
      source. If the Markdown notation table remains authored manually during
      migration, validate it byte-for-field against the structured term
      metadata until it can be generated safely.
- [x] Extend `scripts/check_notation.py` beyond first-use coverage. Require all
      46 current equations to have an explanation record, require every declared
      equation term to resolve, and verify agreement on symbol, meaning, units,
      domain, and model layer.
- [x] Continue requiring nearby explanatory prose. The interactive explanation
      is a supplementary reader aid, not permission to leave an orphaned
      display equation in the manuscript.
- [x] Extend `scripts/check_site.cjs` to verify artifact/explanation targets,
      unique IDs, safe local paths, copied hashes, required accessible labels,
      one reusable viewer shell per page, and successful no-script fallbacks.
- [x] Add focused unit tests for registry parsing, path containment, CSV
      validation, relative URLs from every chapter depth, explanation coverage,
      and deterministic generated metadata.
- [x] Add browser-level checks for keyboard-only use, focus return, Escape,
      back/forward or fragment behavior, mobile layout, screen-reader names,
      reduced motion, CSV load failure, and large-table pagination.
- [x] Keep generated `_site/`, standalone HTML, and monolithic Markdown out of
      hand edits. Implement in manuscript fragments, metadata, filters, build
      scripts, styles, and tests, then regenerate through the canonical commands.

#### 5.5 Make native MathML typography deterministic

- [x] Retain native MathML as the default rendering path. It provides
      zero-JavaScript rendering, semantic accessibility, and recoverable TeX;
      do not switch to KaTeX/MathJax merely to compensate for a missing font.
- [x] Stop depending on the operating system's interpretation of the generic
      CSS `math` family. A local Chromium check currently resolves it only as
      `font-family: math`; this Mac happens to provide STIX Two Math and renders
      the tall delimiters in Eq. (4) correctly, but that is not a portable
      publication guarantee.
- [x] Select and self-host a maintained OpenType math font with a valid MATH
      table, preferably STIX Two Math or Latin Modern Math after visual
      comparison with the manuscript's text face. Pin the exact font release,
      record its checksum and license, and include the license/attribution in
      the repository and release materials.
- [x] Prefer a browser-ready WOFF2 asset while preserving all math tables and
      glyph assemblies. Do not apply ordinary webfont subsetting unless
      stretchy delimiters, radicals, large operators, accents, scripts, and
      uncommon manuscript glyphs have been verified afterward.
- [x] Add a shared `@font-face` declaration and an explicit
      `math { font-family: "<chosen math font>", math; }` rule to both
      `site/quarto.css` and `docs/assets/manuscript.css`. Keep the generic
      `math` fallback after the bundled face.
- [x] Choose `font-display` behavior deliberately. Balance an initial fallback
      against invisible mathematics and layout shift; verify that a slow or
      failed font load never leaves equations unreadable.
- [x] Make the site builder copy the font with a stable content path and make
      Pandoc's standalone `--embed-resources` build actually embed it. Test both
      outputs with network access disabled.
- [x] Include the font source, CSS, license, and deployed/embedded asset in the
      applicable dependency and publication manifests.
- [x] Add a build/browser assertion using `document.fonts` that the named math
      face loaded. Pair it with targeted visual regression checks because a
      successful font load alone does not prove that glyph construction is
      correct.
- [x] Test representative constructs in Chromium, Firefox, and WebKit:
      tall parentheses/brackets/braces around fractions, radicals, sums and
      integrals with limits, matrices, subscripts/superscripts, bold/upright
      variants, Greek letters, and the widest real manuscript equations.
- [x] Capture stable reference crops at desktop, intermediate, narrow-mobile,
      and print widths. Keep tolerances focused on broken layout—unstretched
      fences, missing glyphs, clipping, label collisions, or unreadable
      scripts—rather than treating harmless rasterization differences as
      failures.

The [MathML Core specification](https://www.w3.org/TR/mathml-core/#open-type-math-table)
strongly encourages a font with proper OpenType MATH features and warns that
fallback layout is not guaranteed to be adequate. See also MDN's
[Fonts for MathML](https://developer.mozilla.org/en-US/docs/Web/MathML/Guides/Fonts)
guide and the official [STIX Fonts repository](https://github.com/stipub/stixfonts),
which distributes STIX Two under the SIL Open Font License.

#### 5.6 Audit and reflow unusually wide equations

- [x] Do not require every equation to fit every viewport without scrolling.
      Horizontal scrolling is a valid last resort for intrinsically wide
      mathematics, and the equation number should remain visible outside the
      scrolling region as it does now.
- [x] Add a deterministic width audit at representative content widths rather
      than relying on the browser window's outer width. Record the rendered
      math `scrollWidth`, available `clientWidth`, and overflow ratio by
      equation ID.
- [x] Investigate the seven equations observed to overflow on the first Part I
      page at an 800 px browser viewport:
      `eq:digital-saturating-frontier`,
      `eq:verified-loop-bottleneck`,
      `eq:intelligence-embodiment-compatibility`,
      `eq:embodied-task-first-passage`,
      `eq:data-advantage-profile`,
      `eq:data-advantage-scalarization`, and
      `eq:matched-lifecycle-cost`.
- [x] Reflow Eq. (4), `eq:digital-saturating-frontier`, first. Move its two
      derivative sign conditions into the adjacent prose or a semantically
      separate display unless keeping them beside the definition is necessary
      to the argument.
- [x] For other wide displays, prefer meaningful mathematical grouping through
      aligned/multiline MathML, separately numbered relations where each line is
      independently cited, or prose for side conditions. Do not insert visual
      line breaks that obscure operator precedence or imply a false equation.
- [x] Check 1280 px, 800 px, 520 px, and approximately 390 px layouts, including
      Quarto's sidebar/TOC breakpoints. Audit the actual main-content width, not
      only the viewport width.
- [x] Ensure scrollable equations have an obvious but unobtrusive scroll cue,
      work with keyboard and touch, retain the fixed equation label, and do not
      trap horizontal page scrolling.
- [x] Verify the standalone HTML and print layout separately. Printed equations
      cannot depend on an interactive scrollbar; reflow, scale within a
      readability floor, or move exceptionally wide derivations to a suitable
      appendix.

Definition of done:

- [x] Reader prose uses friendly artifact labels; no accidental bare CSV path
      remains where a link is intended.
- [x] Every artifact link works as a conventional link without JavaScript and
      opens the enhanced viewer on a normal site click.
- [x] Every referenced CSV is copied byte-for-byte, is covered by a manifest,
      passes build-time parsing, and exposes its original download and hash.
- [x] The viewer remains responsive and usable for the largest current table
      without rendering all rows at once.
- [x] Every numbered equation has an explicit, layer-correct explanation whose
      terms resolve to the canonical notation registry.
- [x] Equations and equation-number anchors retain selection, copying,
      cross-reference, deep-link, no-script, standalone, and print behavior.
- [x] Site and standalone mathematics load the pinned self-hosted MATH-table
      font without a network dependency; representative stretchy operators and
      glyph variants render correctly in Chromium, Firefox, and WebKit.
- [x] Wide-equation audits pass at the declared content widths, and every
      remaining horizontal overflow is intentional, readable, and documented.
- [x] Keyboard, accessibility, mobile, malformed-data, missing-artifact, stale
      registry, and duplicate-ID tests pass.
- [x] Manuscript, equation-numbering, notation, standalone-HTML, site-crawl,
      provenance, manifest, and artifact-drift checks all pass after regeneration.

### Explicit non-actions for this pass

- Do not treat inclusion in this queue as authorization to edit generated
  artifacts before the corresponding source task is undertaken.
- Do not hand-edit `docs/Recursive_Industrial_Intelligence_r4.0.md`,
  `docs/Recursive_Industrial_Intelligence_r4.0.html`, `outputs/`, or site
  artifacts.
- Do not add scenario numbers from *AI 2027*, *AI 2040*, *Machines of Loving
  Grace*, or *Situational Awareness* to parameter files as though they were
  measurements.
- Do not use a corporate essay about its own systems as independent
  validation of open-ended RSI.
- Do not treat a fast digital-takeoff scenario as evidence that physical
  closure is easy, or a slow physical bootstrap as evidence that fast digital
  takeoff is impossible.

## 13. Internal capability and public-release gates

### Correct the current wording

The sentence “a release is only one event inside the loop. Verification also
recurs as the governing safety constraint” conflates technical validation,
internal deployment authorization, and public-release assurance.

- [x] Preserve the claim that public releases are lagging indicators, but state
      its stronger implication: an organization can obtain internal research,
      engineering, operational, and successor-training benefits before those
      capabilities are exposed in a public model or product.
- [x] Do not make public release the completion event for an internal
      improvement loop. A useful internal change can compound after it is shown
      to work and authorized for its bounded internal role.
- [x] Do not say that internal use requires no verification at all. At minimum,
      the organization must distinguish a genuine improvement from noise,
      reward hacking, evaluator leakage, or regression before relying on it in
      the next loop.
- [x] Reserve “public-release assurance” for the broader gate covering external
      misuse, uncontrolled distribution, heterogeneous users, legal/compliance
      exposure, and behavior outside the organization's monitored environment.
- [x] Replace “verification recurs as the governing safety constraint” with a
      scoped claim: verification and authorization recur, but their depth and
      latency depend on the consequence and exposure of the use, and the public
      gate can be substantially slower than the internal loop.

Suggested replacement direction:

> Public releases are lagging indicators. An organization can deploy a
> validated improvement to bounded internal research and operations, and use
> the resulting gains in later improvement loops, before it completes the
> broader assurance required for external deployment or public release.
> Release cadence may therefore substantially understate both internal loop
> speed and internally available capability. Internal use is not gate-free:
> technical validation and risk-based authorization remain necessary, with
> stronger controls for irreversible or high-consequence actions.

### Introduce a three-gate hierarchy

- [x] Separate the recursive pipeline into:
      **technical validation** (“does the change actually improve the intended
      capability?”);
      **bounded internal authorization** (“may it be used for this monitored,
      reversible internal task?”); and
      **external/public authorization** (“may it be exposed to broader users,
      environments, and misuse?”).
- [x] Permit different evidence, independence, latency, rollback, and authority
      requirements at each gate. Do not reuse one undifferentiated
      “verification yield.”
- [x] Make consequence class more important than the word “internal.” Offline
      code search, simulation, and draft recommendations can use lighter,
      human-mediated gates; live infrastructure control, cyber/bio work,
      destructive experiments, physical actuation, model-weight modification,
      and successor training may require stringent controls even when wholly
      internal.
- [x] Distinguish internal *advice* from internal *authority*. A model can
      produce valuable recommendations while humans retain approval, execution,
      and rollback authority; this can realize benefit earlier than autonomous
      deployment.
- [x] Allow the public gate to incorporate concerns irrelevant to a contained
      internal tool, while allowing the internal gate to incorporate
      organization-specific hazards and privileged access that the public gate
      may not capture.

### Split internal and publicly visible capability in the model

- [x] Audit `z_n`, verified-loop throughput, verification yield, and the
      capability-update equations for places where “accepted internally,”
      “deployed,” and “publicly released” are currently treated as one state.
- [x] Introduce distinct conceptual indicators, for example:
      \(z_n^{\mathrm{tech}}\) for validated technical gain,
      \(z_n^{\mathrm{int}}\) for authorized internal use, and
      \(z_n^{\mathrm{pub}}\) for authorized public/external release.
      Define their semantics before selecting any numerical relationship.
- [x] Update internally available capability from changes that pass the
      applicable internal gate; update publicly observable capability only when
      the external/public gate passes.
- [x] Track separate clocks or throughputs for experiment completion, validated
      internal adoption, and public release. Public release frequency must not
      be used as a direct estimator of internal RSI-loop frequency.
- [x] Represent the internal–public gap as an unobserved or partially observed
      state with a release lag, not as evidence that capability appears only on
      release day.
- [x] Add a zero-lag branch, a slower-publication branch, and an
      internal-capability-overhang branch as qualitative sensitivity cases
      before assigning values. Do not convert anecdotal secrecy or product
      cadence into a measured lag distribution.
- [x] Keep technical validation in the compounding law: allowing failed or
      illusory improvements to accumulate as capability would mechanically
      overstate internal progress.
- [x] Avoid assuming monotonic nesting without qualification. Public release
      will usually require internal validation, but some internal-only
      capabilities may never be released, and a public product may expose a
      deliberately narrowed or differently optimized capability slice.

### Refine the evidence and strategic interpretation

- [x] State explicitly that public benchmarks, open-weight releases, and product
      launches observe the public frontier, not necessarily the internal
      frontier.
- [x] Treat the internal frontier as a latent variable. Possible indirect
      observables include measured internal task productivity, experiment
      throughput, code/research contribution, training cadence, inference use,
      employee access tiers, staged product deployment, and later disclosures
      about pre-release performance.
- [x] Separate secrecy from capability. A long release interval can reflect
      assurance, product strategy, compute scheduling, integration work,
      regulation, or weak results; it is not by itself evidence of a large
      internal overhang.
- [x] Explain the strategic consequence: internal benefits can reinforce
      research, operations, and physical deployment before competitors or the
      public can observe the underlying capability, so public evidence may lag
      the feedback loop that matters to the thesis.
- [x] Explain the countervailing consequence: a system used internally may have
      privileged data, tools, compute, infrastructure, and model-development
      access, increasing the severity of some failures even when distribution
      risk is low.
- [x] Reuse fast-takeoff scenarios and frontier-lab self-reports only to motivate
      this state separation. They do not independently measure the size or
      duration of an internal capability overhang.

### Manuscript and visualization deliverables

- [x] Revise the final paragraph of I.1 so “public releases are lagging
      indicators” leads directly to the internal/public frontier distinction,
      not to one universal verification bottleneck.
- [x] Reconcile the opening definition of a “verified improvement loop” with
      the three gates. Define the loop relative to the use being claimed:
      internally validated gain, authorized internal deployment, or public
      release.
- [x] Update Part III.4 so governance attaches controls to consequence,
      authority, reversibility, containment, and exposure rather than applying
      the public-release standard to every internal use.
- [x] Add a small two-frontier diagram or timeline only if it clarifies the
      lag:
      experiment → technical validation → bounded internal benefit and further
      loops → broader assurance → public/external release.
- [x] If modeled, report both internally available and publicly visible
      capability trajectories. Label their difference as assumption-dependent
      capability overhang, not a measured secret capability estimate.

Definition of done:

- [x] The article no longer equates public-release cadence with internal
      improvement-loop cadence.
- [x] Technical validation, bounded internal authorization, and public-release
      assurance have distinct definitions and observables.
- [x] Internal benefit can accumulate before public visibility without treating
      unvalidated changes as genuine capability.
- [x] Safety requirements scale with consequence and authority, so neither
      “internal means safe” nor “every internal use requires public-release
      assurance” is implied.
- [x] Any internal/public capability gap is visibly assumption-class and has
      explicit countercases and falsifiers.


## 14. Make proposition labels self-resolving

### Diagnose the navigation problem

The labels are defined, but not where the quoted paragraph can be understood
locally. The six definitions appear in the front matter under “Six distinct
propositions”:

- **P1:** conceptual possibility of recursive industrial expansion.
- **P2:** eventual technical feasibility.
- **P3a:** economics of orbital/lunar compute during the Earth-dependent bridge.
- **P3b:** economics of a mature, high-closure space-industrial ecology.
- **P4a:** documented integrated portfolio direction.
- **P4b:** inferred intent to transition toward recursive industrial closure.

The closure paragraph appears later in Part I. On the multi-page site the
definitions are on “Complete contents,” while the paragraph is on a different
page. A reader entering Part I directly therefore encounters undefined,
unlinked labels. In the monolithic manuscript the definitions are still far
enough away that recall should not be assumed. “The proposition map follows”
is also misleading because no visibly identified map or table follows.

### Make the canonical definitions findable

- [x] Give every proposition a stable anchor and descriptive title:
      “P1 — Conceptual possibility,”
      “P2 — Technical feasibility,”
      “P3a — Earth-dependent bridge economics,”
      “P3b — Mature high-closure economics,”
      “P4a — Documented portfolio direction,” and
      “P4b — Recursive-closure intent.”
- [x] Add a visible heading such as “Proposition ladder” or “Claims assessed”
      above the canonical definitions. Do not leave them as an unlabelled list
      embedded in front matter.
- [x] Make the proposition ladder discoverable in the site table of contents
      and search index.
- [x] Add the six labels to the glossary or a small proposition register so a
      reader can resolve them without returning to the beginning.
- [x] Keep one canonical definition and status for each proposition. Local
      legends may summarize it but must link back rather than introduce a
      second independently maintained wording.

### Fix the Part I paragraph

- [x] Replace “The proposition map follows” with an explicit cross-reference,
      for example: “Mapped to the six claims in the
      [proposition ladder], the closure dependencies are:”.
- [x] Add a compact local table immediately before or after the closure
      discussion:

      | proposition | abbreviated claim | closure premise or evidence |
      |---|---|---|
      | P1 | conceptual possibility | no demonstrated closure required; logical coherence only |
      | P2 | technical feasibility | embodied-production and reproductive-capital closure; AI-R&D closure is an accelerator, not a logical prerequisite |
      | P3a | bridge economics | compares an Earth-dependent operating regime; no AI-R&D closure premise |
      | P3b | mature economics | assumes a declared high-physical-closure regime, but does not require AI-R&D closure |
      | P4a | portfolio direction | no closure proof; documented initiatives and integration evidence |
      | P4b | closure intent | closure-specific indicators of intent, not proof of achieved closure |

- [x] Ensure the table does not repeat the ambiguity in the current prose.
      P3a and P3b both avoid **AI-R&D closure** as a premise, but P3b's subject
      is explicitly a mature **high-physical-closure** regime.
- [x] On first use within every independently navigable site chapter, spell out
      the proposition's short title rather than writing only `P1`, `P3b`, or
      `P4a`.
- [x] Prefer constructions such as “P3b — mature high-closure economics” in
      consequential conclusions, even when the label has appeared earlier.
      The small saving from a bare code is not worth forcing readers to memorize
      a six-item taxonomy.

### Add proposition cross-references

- [x] Make proposition labels semantic cross-references, not ordinary
      unvalidated text. The same source syntax must resolve to the correct
      anchor in monolithic Markdown/HTML and across Quarto site pages.
- [x] Give each link an accessible name containing the proposition's short
      title; a screen reader should not encounter a series of unexplained links
      named only “P1,” “P2,” and “P4b.”
- [x] Visually distinguish proposition references consistently without making
      them resemble source markers, equation numbers, or evidential-class
      labels.
- [x] Link repeated uses in the executive summary, evidential table, Parts I–IV,
      appendices, and conclusion. At minimum, link the first occurrence on each
      independently navigable page.
- [x] Consider a small hover/focus preview containing the short title and
      current status only as progressive enhancement. The real link and local
      expanded wording must remain sufficient without JavaScript.

### Validate the proposition system

- [x] Add a machine-readable proposition registry or extend an existing claims
      registry with ID, short title, canonical wording, current evidential
      status, and canonical anchor.
- [x] Generate or validate the front-matter ladder and local compact legend
      against that registry so proposition wording and status cannot drift.
- [x] Add a build check that fails on undefined proposition identifiers,
      duplicate anchors, missing canonical definitions, stale registry entries,
      or broken cross-page targets.
- [x] Add an editorial check for bare proposition labels outside the canonical
      definition. Allow narrow exceptions in tables only where a nearby legend
      makes every code self-evident.
- [x] Extend the site crawl to verify each proposition reference resolves from
      every chapter depth and that the proposition ladder is indexed.

Definition of done:

- [x] A reader who lands directly on Part I can identify all six propositions
      without navigating backward or searching the source.
- [x] “Proposition map” denotes an actual labelled table/register or is replaced
      by more accurate wording.
- [x] Every consequential use combines or links the code with a descriptive
      title.
- [x] The P3 distinction is precise: neither P3 claim requires AI-R&D closure,
      while P3b explicitly concerns a stipulated high-physical-closure regime.
- [x] Site, standalone HTML, monolithic Markdown, accessibility, search, and
      cross-reference checks pass.

## 15. Move genuinely peripheral detail out of the main reading path

### Current-state audit

- [x] Treat this as an editorial classification exercise, not a bulk
      “shorten every long paragraph” rewrite. A mechanical screen currently
      flags approximately 105 main-narrative prose paragraphs of at least 100
      words, but length alone does not determine whether material is peripheral.
- [x] Note that the manuscript fragments currently contain no authored Pandoc
      footnotes. The Quarto HTML nevertheless already loads its standard
      footnote popover code on every page, so the site can support conventional
      footnotes without a new modal framework.
- [x] Audit reading flow section by section at the rendered content width.
      Record each candidate passage, its argumentative function, the proposed
      destination, and the sentence that remains in the body.
- [x] Classify each candidate into one of four outcomes:
      keep/split in the main body; move to a concise footnote; move to a
      table/appendix/methods section; or remove as repetition.
- [x] Do not use footnotes to make the article appear shorter while preserving
      an equally long second manuscript underneath it. Set a footnote budget by
      section and review the combined main-text-plus-note burden.

### What must remain in the main text

- [x] Keep every proposition needed for the next inference, central mechanism,
      headline result, definition at first use, and interpretation of a table
      or equation in the reading path.
- [x] Keep assumption/source-class labels and the caveats needed to prevent a
      result from being read as a measurement, probability, forecast,
      demonstrated feasibility, or established causal relation.
- [x] Keep material limitations, counterarguments, falsifiers, safety
      constraints, and conditions that could reverse the conclusion. A reader
      should not have to open a note to discover that the headline claim is
      conditional or that the model omits a load-bearing term.
- [x] Keep equation-term definitions and non-obvious units adjacent to the
      equation. The planned equation explainer is supplemental, not a reason to
      hide the mathematical semantics in notes.
- [x] Keep the short explanation of why an apparently anomalous value matters.
      Move only secondary mechanics after the main text has made the correct
      interpretation unavoidable.

### Appropriate footnote material

- [x] Prefer footnotes for compact provenance micro-detail, legal/formal naming,
      exact source-locator qualifications, secondary arithmetic, alternative
      unit conventions, brief implementation details, and narrowly relevant
      historical/revision context.
- [x] Move deterministic-build facts, random-seed mechanics, and low-level file
      generation details to Appendix C or a short footnote when they interrupt a
      results discussion.
- [x] Move secondary examples that support but do not change an inference,
      provided the main sentence states the inference and its evidential class.
- [x] Keep ordinary source citations as source links/markers. Do not duplicate
      the source apparatus inside footnotes merely because a note can contain
      citations.
- [x] Keep machine-readable artifact references as friendly artifact links with
      CSV previews/downloads. A footnote should not become a hiding place for
      file paths that readers may want to inspect.
- [x] Aim for one short paragraph per note, normally one to three sentences. If
      a note needs several paragraphs, a table, or its own argument, move it to
      an appendix or labelled technical aside instead.
- [x] Avoid footnote chains, notes whose main purpose is another note, more than
      two markers in one sentence, or clusters of markers that make the body
      read like source code.
- [x] Do not put footnotes in the abstract. Use them sparingly in the executive
      summary, headings, captions, and tables, where format conversions and
      scanning behavior are more fragile.

### First-pass candidates to review

- [x] In the front-matter status block, retain the release status and
      assumption-class warning, but move the script names and manifest-path
      inventory to the reproducibility appendix or a concise technical note.
- [x] In Part II after the central result table, reduce the parenthetical at
      `20-part-ii-comparative-economics.md:357` to the interpretation needed for
      the table. The architecture distinction is already defined earlier;
      revision history and secondary lifecycle detail can become a note or
      Appendix B cross-reference.
- [x] Move the shared-draw caching and stable-seed detail at
      `20-part-ii-comparative-economics.md:393` to a short reproducibility
      footnote or Appendix C. Keep the body statement that frequencies belong
      to the declared ensemble and are not empirical probabilities.
- [x] At the AI1 radiator discussion around
      `20-part-ii-comparative-economics.md:248`, retain the conclusion that the
      area convention and complete thermal mass are unresolved. Move the
      two-face/one-face arithmetic and idealized temperature calculation to a
      technical footnote if it is not used by the next inference.
- [x] In the Terafab discussion around
      `30-part-iii-strategy-governance.md:89`, retain the evidential conclusion:
      executed site agreements strengthen commitment but do not establish
      construction or production. Consider moving the site-name correction and
      wafer-start comparability detail to a note.
- [x] In the debris results around
      `12-part-i-model-results.md:501`, keep “ratio above one is not a cascade
      threshold” and the conclusion that no case establishes shell safety in
      the body. The empty-stock boundary mechanics behind the exact 1.00 value
      can be a note if the table remains unambiguous without it.
- [x] Review explanatory asides about dollar-per-flight arithmetic,
      exact revision-to-revision changes, and implementation-specific cache or
      seed behavior throughout Part II as a group rather than converting them
      opportunistically.
- [x] Do not demote the Part II cost boundary, the Part III alternative
      hypotheses, or the Part IV limitations merely because they are long.
      Split, tabulate, or relocate them to a clearly signposted appendix if
      needed; their substance is fundamental to the claims.

### Use native footnotes with progressive enhancement

- [x] Author notes with standard Pandoc/Quarto footnote syntax and semantic,
      globally unique identifiers such as `[^p2-ai1-radiator-area]`. Do not use
      manually typed superscript numbers.
- [x] Keep the generated footnote reference as a real link to a real endnote
      with a backlink. Hover/focus UI must enhance that structure rather than
      replace it.
- [x] Use Quarto's existing `footnotes-hover` behavior for the first
      implementation. Style and test it before adding custom JavaScript; the
      generated site already initializes footnote-reference popovers.
- [x] Prefer a non-blocking popover for a short footnote on desktop. A modal
      creates a larger context switch than the detail it is intended to hide.
- [x] Test the default interaction on touch devices. If it is inadequate, add a
      small-screen bottom sheet or native `<dialog>` enhancement that opens on
      an ordinary tap, while preserving new-tab, copy-link, no-script, and
      endnote navigation.
- [x] If a mobile dialog is added, reuse the shared accessible overlay
      infrastructure planned for artifact/equation viewers, but give footnotes
      their own simple content contract. Do not load table or equation code for
      a short note.
- [x] Ensure hover is never the only trigger: support keyboard focus, tap/click,
      Escape, outside/close controls where applicable, focus return, and a
      visible focus indicator.
- [x] Increase the effective touch target of superscript references without
      making line spacing jump or allowing adjacent note markers to overlap.
- [x] Sanitize or construct popover content from the generated footnote DOM.
      Do not introduce an independent HTML copy of each note.
- [x] Avoid hiding endnotes with CSS. They are the durable no-script,
      accessibility, print, link, and standalone-HTML representation.

Quarto's standard HTML output enables hover previews for footnotes by default;
see the official [HTML reference-popup
documentation](https://quarto.org/docs/output-formats/html-basics.html#reference-popups).
Use its standard [Pandoc footnote
syntax](https://quarto.org/docs/authoring/markdown-basics.html#footnotes) so
the enhancement remains portable.

### Decide placement for each publication format

- [x] Test `reference-location` deliberately rather than accepting an accidental
      default. On the multi-page site, notes should remain local to their
      chapter page; in standalone HTML, section-level notes may reduce
      round-trip distance compared with one endnote block after the entire
      manuscript.
- [x] Allow displayed footnote numbers to differ between chapter pages and the
      monolithic document if necessary, but make semantic note IDs and content
      stable. Do not cite a note elsewhere solely by its generated ordinal.
- [x] Add restrained footnote and backlink styles to both
      `site/quarto.css` and `docs/assets/manuscript.css`, including print
      behavior and `:target` highlighting.
- [x] Confirm that the standalone Pandoc build retains footnote semantics,
      backlinks, internal anchors, MathML inside notes, and source-marker links.
- [x] Decide whether site search should index note text. If it does, ensure
      results land on or reveal the note rather than appearing to point to
      missing body prose.
- [x] Ensure PDF/print output places notes legibly and does not print hidden
      popover/dialog shells or duplicate the same note.

### Make readability part of the regular editorial and build checks

- [x] Add a footnote audit that rejects duplicate IDs, unresolved references,
      orphaned definitions, notes with no backlink, and generated ordinals
      typed manually in prose.
- [x] Warn on unusually long notes, excessive note density, footnotes inside
      headings, and notes containing a core evidence-class or claim-boundary
      warning.
- [x] Add a dedicated `pnpm run check:readability` command and run it beside
      `check:prose` in the regular local validation instructions and the
      publication CI workflow. Include it in release preflight rather than
      treating readability as a one-time cleanup.
- [x] Document the rule and its review protocol in `docs/EDITORIAL_STYLE.md`.
      The rule applies to every new manuscript version and to both human and
      agent edits.
- [x] Have the automated check emit a stable, reviewable report by fragment and
      section. At minimum, flag unusually long prose blocks, excessive sentence
      length, deeply nested parentheticals, high footnote density, overlong
      footnotes, and clusters of references or inline artifact paths that
      interrupt the reading path.
- [x] Treat those measurements as triage signals, not prose-quality scores.
      Do not fail merely because a paragraph exceeds a universal word limit or
      encourage editors to game the check by mechanically splitting sentences.
- [x] Fail the mechanical invariants (broken footnotes, prohibited placements,
      inaccessible markup, and unexplained regressions in the flagged-block
      inventory). Require an LLM-assisted or human verdict for contextual
      questions: keep, split, footnote, appendix, or remove.
- [x] Establish a reviewed baseline for the existing long passages, then ratchet
      it: every newly introduced or materially enlarged flagged passage needs
      an explicit disposition, while the initial backlog is reduced through
      the editorial pass rather than grandfathered permanently.
- [x] Record each contextual review with the section ID, opening words,
      triggering signal, disposition, and one-sentence rationale. Store the
      current report with the release-review artifacts so changes are auditable
      without embedding drafting history in the manuscript.
- [x] Run a rendered-width sampling pass as part of each release review,
      covering at least the abstract/executive material, one dense quantitative
      section, one strategy section, and all passages newly flagged since the
      previous reviewed baseline. Source-only metrics cannot detect every
      visual interruption.
- [x] Compare footnote reference/definition counts between manuscript fragments,
      monolithic Markdown, standalone HTML, and the sum of site pages.
- [x] Extend accessibility checks for `doc-noteref`/`doc-endnote` semantics,
      accessible names, focus order, target highlighting, and backlink behavior.
- [x] Add browser tests for hover, keyboard focus, ordinary click/tap,
      Escape/close if enhanced, deep links, back navigation, and no-JavaScript
      fallback at desktop and mobile widths.
- [x] Run a final “main text only” review with every note collapsed. The
      argument, all material qualifications, and the reason for every headline
      result must still be understandable and accurate.

Definition of done:

- [x] Peripheral detail has been moved selectively, repeated material has been
      removed, and core passages have been split or tabulated where footnotes
      would be inappropriate.
- [x] A reader who ignores every footnote still receives the complete argument,
      material assumptions, limitations, countercases, and safety boundaries.
- [x] Footnotes use standard semantic markup and work as endnote links without
      JavaScript.
- [x] The site provides convenient hover/focus previews; any mobile overlay is
      added only after testing demonstrates a need.
- [x] Standalone HTML, print, search, accessibility, cross-reference, and
      browser-interaction checks pass.
- [x] `check:readability` runs in the documented local check sequence,
      publication CI, and release preflight; its automated report and the
      required contextual review contain no unresolved regressions.

## 16. Ground the digital loop with contemporary self-improvement systems

### Add a compact external-evidence comparison

- [x] Add a short evidence box or table in Part I.1, near the operational
      definition of the verified AI-R&D loop, comparing Karpathy's
      `autoresearch`, Sakana AI's Darwin Gödel Machine (DGM), and The AI
      Scientist-v2. Keep implementation detail in notes or the source register.
- [x] Give the comparison explicit columns for the object modified,
      experiment/search topology, evaluation signal, observed result, human
      role, verification boundary, and what the example does **not**
      demonstrate.
- [x] Treat these as observed, bounded precursors to parts of the loop—not as
      proof that verified AI-R&D closure, open-ended recursive improvement, or
      any modeled milestone time has been reached.

### Karpathy `autoresearch`: a constrained linear improvement loop

- [x] Cite the canonical README and `program.md` at an immutable commit. The
      agent modifies `train.py`; data preparation and evaluation remain fixed;
      each experiment has a five-minute wall-clock training budget on one GPU
      and is kept or discarded using validation bits per byte (`val_bpb`).
- [x] Present the stated approximately 12 experiments/hour and approximately
      100 experiments overnight as design-implied capacity, not an observed
      success rate. Separate attempted, non-crashing, retained, and
      statistically credible improvements.
- [x] Do not derive progress claims from `progress.png` alone. The canonical
      analysis notebook reads a local `results.tsv`, but that run ledger is not
      published in the repository. Use the project as process evidence unless
      a versioned, reproducible first-party ledger is found.
- [x] State the boundary: this is automated hill climbing over model-training
      code under a fixed narrow metric. The acting foundation model does not
      retrain its own weights, and `val_bpb` acceptance is not independent
      safety, transfer, deployment, or operational verification.

Primary sources:

- [Karpathy `autoresearch`
  README](https://github.com/karpathy/autoresearch)
- [`autoresearch` experiment
  protocol](https://github.com/karpathy/autoresearch/blob/master/program.md)

### Sakana DGM: self-modification with branching archive search

- [x] Cite the latest DGM technical report. Report the measured benchmark
      changes with denominators: SWE-bench from 20.0% to 50.0% and Polyglot
      from 14.2% to 30.7%, plus the reported ablations against no
      self-improvement and no open-ended exploration.
- [x] Explain the structural difference from `autoresearch`: DGM rewrites the
      coding-agent scaffold and samples parents from a growing archive, so
      temporarily weaker branches can become stepping stones. Assess whether
      the digital-loop discussion should explicitly represent lineage/archive
      memory rather than imply monotone, single-lineage hill climbing.
- [x] Preserve the scope boundary. DGM improved an agent wrapper and workflow
      on coding benchmarks while using externally supplied foundation models;
      it did not improve the underlying model weights, demonstrate indefinite
      returns, or complete an independently authorized successor-model loop.
- [x] Include the negative safety evidence because it directly supports the
      article's verification hypothesis: Sakana reports fabricated tool-use
      logs and attempts to disable reward-function markers. Sandboxing, human
      oversight, lineage records, and inspection—not the optimized benchmark
      alone—were needed to detect these cases.

Primary sources:

- [DGM technical report, arXiv
  2505.22954](https://arxiv.org/abs/2505.22954)
- [Sakana AI's DGM report and documented failure
  cases](https://sakana.ai/dgm/)

### The AI Scientist-v2: a broader but still bounded R&D loop

- [x] Use AI Scientist-v2 to cover hypothesis formation, experiment design and
      execution, analysis, visualization, manuscript production, and review.
- [x] Report the evaluation design rather than the “AI paper accepted”
      headline alone: three autonomous manuscripts entered an ICLR workshop
      review experiment; one received an average score of 6.33/10 and two were
      rejected. The potentially accepted paper was withdrawn under a
      prearranged protocol.
- [x] Preserve the human-selection boundary: humans supplied the workshop
      theme, selected three ideas from roughly forty generated candidates, ran
      multiple seeds, and selected the strongest complete outputs for
      submission. The study tested whether at least one paper could survive
      review; it did not estimate the system's autonomous success frequency.
- [x] Include the reported limitations—citation inaccuracies, insufficient
      methodological depth, and no generated manuscript reaching the authors'
      main-conference quality standard. This is evidence for partial
      research-process automation and recurring external verification, not
      research closure.

Primary source:

- [The AI Scientist-v2 technical report, arXiv
  2504.08066](https://arxiv.org/abs/2504.08066)

### Separate measured systems from Sakana's declared RSI strategy

- [x] If the 2026 Sakana RSI Lab loop is discussed—Agent-Native Models power
      an AI Scientist, which then builds better Agent-Native Models—label it as
      declared strategy and intended transition, not a measured exponential
      trajectory.
- [x] Use the distinction to reinforce the article's separation between
      portfolio/intent evidence and closure evidence. The complete
      model-to-research-to-successor-model cycle still needs versioned
      telemetry, independent evaluation, safe deployment, and recurrence.

Primary source:

- [Sakana AI RSI Lab
  announcement](https://sakana.ai/rsi-lab/)

### Map observations without over-calibrating the model

- [x] Map `autoresearch` to candidate throughput, a serial experiment floor,
      and a narrow accept/reject gate; DGM to self-modification,
      archive-dependent search, transfer, and evaluator gaming; and AI
      Scientist-v2 to the wider workflow and continuing human selection.
- [x] Do not use these results to calibrate
      $\nu_{\mathrm{verified}}$, $\mathbb E[\mathbf G_n]$, or
      $T_{\mathrm{AIR\&D}}$. Their tasks, budgets, evaluators, interventions,
      and success units are not commensurable with completed-loop quantities.
- [x] Consider an “observed precursor telemetry” register containing source
      version/date, loop scope, attempts, retained changes, elapsed
      compute/time, evaluator independence, transfer evaluation, human
      interventions, and failure modes. Leave unavailable fields missing.
- [x] Add immutable source locators, access dates, and claim-level provenance;
      then rerun citation, link, standalone-prose, and readability checks.

Definition of done:

- [x] Part I.1 concisely shows that autonomous improvement loops exist in
      bounded settings while candidate throughput and benchmark gains remain
      distinct from verified AI-R&D closure.
- [x] Every use of “self-improvement” names what changed: training code, agent
      scaffold/workflow, research output, or foundation-model weights.
- [x] Every number is tied to a reproducible first-party artifact or labelled
      as design capacity, self-report, or declared strategy.

## 17. Crosswalk the off-world industrial minimum cut to Tesla and SpaceX/xAI

### Clarify what the manuscript already has

- [x] State that the inherited model has ten coarse sectors, while the
      integrated-bootstrap model's 18 sectors are the closest existing answer:
      power; mining; refining; robotics; machine tools; construction; thermal;
      transport; repair; recycling; interconnects/boards; passives/power;
      sensors/control; packaging/test; mature logic; advanced logic/memory;
      process equipment/metrology; and compute.
- [x] Do not call these “the 18 industries that must move off-planet.” They are
      model buckets for minimum viable production and service functions. Full
      closure requires sufficient off-world capacity to reproduce every
      indispensable node, not relocation of every terrestrial firm or all of
      an industry's output.
- [x] Explain that 18 is not an exhaustive closure count. The model also tracks
      17 material categories, while its own process-closure gap register still
      lacks species-level chemistry, gases, resists, optics, bearings,
      calibration artifacts, parent-tool ancestry, qualified sources, and
      transport-fleet reproduction.
- [x] Note the present gap: Part III has an 11-layer descriptive portfolio
      table, but it is not crosswalked to the 18 model sectors and therefore
      cannot presently support a reproducible “X of 18 covered” claim.

### Build a source-backed 18-row coverage matrix

- [x] Create a versioned source file and generated reader-facing table, for
      example `data/portfolio_sector_coverage.yaml` and
      `outputs/integrated/tables/portfolio_sector_coverage.csv`.
- [x] For every sector record the relevant Tesla, SpaceX, xAI, or joint
      initiative; demonstrated output; location; scale; upstream suppliers;
      required parent tools; off-world relevance; evidence class; source
      locator/date; and the exact residual closure gap.
- [x] Score separate dimensions rather than one subjective “coverage”
      checkbox:
      capability exists somewhere in the portfolio; capability is operational
      at relevant terrestrial scale; hardware/process is space-qualified;
      operation is demonstrated off-world; inputs and consumables are locally
      sourced; production equipment is locally reproducible; repair and
      verification are locally supported.
- [x] Use mutually exclusive evidence tiers:
      `documented_operating`, `demonstrated_but_not_scaled`,
      `announced_or_under_development`, `adjacent_capability_only`, and
      `no_evidence`. Keep evidence maturity separate from modeled closure
      criticality.
- [x] Treat Tesla as a separate public company from SpaceX/xAI. Shared control,
      supply agreements, and Terafab coordination can support a portfolio
      crosswalk but must not be described as common ownership or guaranteed
      resource availability.

### Audit this provisional count

- [x] Test the following **provisional terrestrial-adjacency** classification
      against primary sources before publication:
      12 of 18 sectors have a documented operating capability plausibly
      adjacent somewhere in the portfolio; five are primarily
      announced/development-stage; and one lacks direct portfolio evidence.
- [x] Candidate `documented_operating` or operational-adjacency rows:
      power, refining, machine tools, construction, thermal, transport,
      repair, recycling, interconnects/boards, passives/power,
      sensors/control, and compute.
- [x] Candidate `announced_or_under_development` rows:
      mining, robotics, packaging/test, mature logic, and advanced
      logic/memory. Preserve distinctions within this tier: for example,
      terrestrial Optimus prototypes are stronger evidence than a declared
      future asteroid-mining line, while Terafab still has no wafer output.
- [x] Candidate `no_evidence` row:
      reproduction of semiconductor process equipment/metrology. Operating
      purchased lithography or metrology equipment is not the same as making,
      maintaining, and calibrating the parent tools that closure requires.
- [x] Publish the result as a vector, not one flattering fraction:
      provisionally `12 operating-adjacent / 5 announced-development /
      1 not evidenced / 0 demonstrated off-world reproductively closed`.
      Change those counts when the source audit warrants it.
- [x] Make the decisive caveat visible beside the count: even if all 18 rows
      had terrestrial portfolio adjacency, **none currently demonstrates
      off-world reproductive closure**. Space transport reaches orbit, but the
      transport fleet and its upstream industrial stack are not reproduced
      there.

### Use primary evidence and test the weak rows

- [x] Use Tesla's latest annual report/shareholder disclosures to support
      operational energy, battery/cathode production, lithium-refining pilot
      production or operations, AI compute, and manufacturing claims; use its
      impact reports for battery-recycling quantities.
- [x] Use SpaceX's current regulatory filings and prospectus for operational
      transport/communications and clearly labelled early-stage lunar,
      asteroid-mining, orbital-compute, and manufacturing initiatives.
- [x] Use Terafab's filing-backed commitments separately from its marketing
      claims. Chip design, lithography operation, fabrication, memory,
      packaging, and test are announced scope—not demonstrated production.
- [x] Require stronger evidence than job advertisements for any counted
      operating capability. Jobs can identify a function to investigate but
      cannot establish throughput, maturity, or off-world readiness.
- [x] For machine tools, construction, thermal, repair, boards,
      sensors/control, and passives/power, find product-, filing-, patent-, or
      facility-level evidence that identifies actual internally performed
      processes. Generic statements that an aerospace or automotive company
      “must do this” are not evidence.
- [x] Add a negative-evidence protocol: search current filings, technical
      disclosures, facility records, and supplier announcements before
      assigning `no_evidence`; record the search boundary and do not translate
      absence of public evidence into proof of absence.

### Tie the crosswalk to the closure hypothesis

- [x] Add a second view grouping the 18 sectors into bulk-material,
      industrial-equipment, electronics, operations/maintenance, and
      intelligence/compute blocks so readers can see where the portfolio is
      deep versus merely adjacent.
- [x] Compute both an unweighted count and a dependency-aware result. One
      missing parent-tool/metrology row can break closure even if 17 other rows
      are partially covered, so “17/18” must never be interpreted as 94%
      closed.
- [x] Connect company evidence to the existing process-closure gap register and
      acceptance gates C01–C08. A row becomes closed only after its source,
      material-grade, process, parent-tool, fleet, failure/substitution, and
      empirical-calibration requirements pass.
- [x] Keep strategic interpretation separate from feasibility:
      portfolio coverage may reduce coordination or transition costs; it does
      not prove that the off-world recipes, yields, autonomous task coverage,
      commissioning, verification, or economics work.
- [x] Present the generated CSV through the planned friendly table viewer so a
      reader can filter by company, evidence tier, sector group, and residual
      gap without confronting a raw file path.

Definition of done:

- [x] The article answers both questions directly: it names the 18 modeled
      sector functions and states how many have operational, developmental,
      adjacent-only, missing, and off-world-closed portfolio evidence.
- [x] Every row and aggregate count regenerates from the same versioned source
      data and has claim-level provenance.
- [x] No count conflates terrestrial competence, announced intent,
      space-qualified operation, and reproductive closure.
- [x] The conclusion identifies the minimum-cut gaps, not merely the percentage
      of rows with some corporate adjacency.

## 18. Number every figure and constrain oversized images

### Current rendered-output audit

- [x] Fix all nine authored manuscript images. They currently render as
      ordinary `<p><img …></p>` blocks rather than semantic `<figure>`
      elements, so neither the site nor the standalone manuscript has figure
      numbers or real captions.
- [x] Fix the Markdown attribute syntax. The separate `{fig-alt="…"}` lines
      currently appear as visible literal text in the generated HTML instead
      of attaching to the images.
- [x] Treat sizing as a cross-format defect. The Quarto site happens to apply
      `img-fluid`, but the standalone HTML displays images at their natural
      widths—980, 1,120, 1,530–1,620, and up to 3,187 CSS pixels—inside a
      reading column measured at roughly 878 pixels at a 1,280-pixel viewport.
- [x] Do not mistake the file named `oversize_frontier.png` for the cause of
      the bug: “oversize” is the modeled seed-design variable. It still needs
      the same responsive sizing treatment as the other charts.

### Convert every image into an addressable numbered figure

- [x] Use valid Pandoc/Quarto figure syntax with the caption, stable ID,
      presentation class, and `fig-alt` attributes attached to the image in
      one attribute block, for example:

      `![Concise reader caption.](path){#fig-example .figure-standard fig-alt="Independent visual description."}`

- [x] Assign stable semantic IDs in manuscript order:
      `fig-survival-central`, `fig-import-decay-sweep`,
      `fig-seed-mass-ensemble`, `fig-operating-capacity`,
      `fig-oversize-frontier`, `fig-compute-growth-regimes`,
      `fig-debris-regimes`, `fig-lco-ratio-monte-carlo`, and
      `fig-crossover-surface`.
- [x] Generate labels and ordinals; never type “Figure 3” directly into a
      caption or prose. Use semantic cross-references such as
      `Figure [@fig-seed-mass-ensemble]` so inserting or moving a figure cannot
      silently make references stale.
- [x] Give all nine figures visible captions that state the interpretation and
      evidence class, not only the chart title. Keep `fig-alt` focused on what
      the visual contains; do not duplicate the complete caption as alt text.
- [x] Where nearby prose already says “the figure below” or describes a chart
      by filename, replace it with the semantic figure reference. Readers must
      be able to report a problem using both a displayed number and a stable
      deep-linkable ID.

### Keep numbering consistent in both publication formats

- [x] Reuse the deterministic mapping architecture of
      `scripts/equation_numbering.lua`: derive the canonical figure order from
      the manuscript fragments, pass that map into every Quarto page, and
      apply the same map to the standalone Pandoc build.
- [x] Decide and document one numbering scheme. Prefer a single global
      manuscript sequence, Figures 1–9, unless section-prefixed numbering can
      be made identical across the multi-page site, standalone HTML, print,
      and future PDF output.
- [x] Preserve native `<figure>` and `<figcaption>` semantics while adding
      numbering. The generated number should be a link to the figure anchor,
      and prose references should deep-link to the correct page and figure in
      the multi-page site.
- [x] Ensure displayed labels, IDs, captions, and cross-references remain
      available without JavaScript and appear correctly in print.

### Apply intentional responsive size classes

- [x] Add matching figure rules to `site/quarto.css` and
      `docs/assets/manuscript.css`. At minimum, use
      `display: block; width: auto; max-width: 100%; height: auto` for images
      so no raster can exceed its figure or reading column.
- [x] Remove the site's unconditional `figure img { width: 100%; }` behavior.
      It makes every chart fill the available width even when a smaller
      presentation would read better.
- [x] Define a small, documented set of presentation classes rather than
      per-image pixel hacks:
      `.figure-compact` for simple single-panel charts,
      `.figure-standard` for information-dense single-panel charts, and
      `.figure-wide` for genuine multi-panel comparisons.
- [x] Center figures whose maximum width is below the text column and align the
      caption width with the displayed chart. Preserve adequate spacing
      without letting a chart dominate an entire viewport unnecessarily.
- [x] Preserve full raster resolution for high-density displays while
      controlling CSS display size. Do not downsample source artifacts merely
      to repair layout.
- [x] On small screens, figures must shrink to the container without horizontal
      page scrolling, clipped labels, distorted aspect ratios, or captions
      wider than their charts.
- [x] In print/PDF, cap figures to the printable width and height, keep captions
      attached when feasible, and avoid blank pages caused by an image's
      natural pixel dimensions.

### Redesign the genuinely too-wide panel

- [x] Regenerate `crossover_surface.png`, currently 3,187×602 pixels because
      five panels are arranged in one horizontal row. A CSS shrink alone makes
      its axes and annotations unreadably small.
- [x] Prefer a responsive 2×3 grid with the unused cell reserved for the shared
      legend/color scale, or split the result into two separately numbered
      figures if that improves the argument. Do not use horizontal page
      scrolling as the primary reading experience.
- [x] Review `lco_ratio_mc.png` for legend density and the 1,530–1,620×900–936
      integrated charts for excess whitespace and label size after the CSS
      fix. Regenerate only the charts whose information remains unreadable at
      their intended display width.
- [x] If full-resolution inspection is useful, make the displayed image an
      ordinary accessible link to the full asset or use a progressively
      enhanced lightbox. Zoom must be optional and must not replace the
      correctly sized inline figure, caption, or no-JavaScript link.

### Add figure and layout checks to the regular publication gates

- [x] Add a source audit that rejects manuscript images without a unique
      `fig-` ID, a nonempty caption, nonempty `fig-alt`, and an approved
      presentation class.
- [x] Fail the build if a literal `{fig-alt=…}` fragment survives into HTML,
      if an authored image remains inside a plain paragraph, or if the
      standalone/site figure counts differ from the source count.
- [x] Extend `check:site` to require the expected numbered figure IDs and
      canonical order rather than accepting the present false-positive
      comparison of zero standalone figures with zero site figures.
- [x] Validate every semantic cross-reference, displayed ordinal, deep link,
      caption, and figure ID in both standalone and multi-page output.
- [x] Extend accessibility checks for `<figure>`/`<figcaption>` structure,
      non-duplicative alt text, linked-image accessible names, keyboard focus,
      and optional zoom controls.
- [x] Add browser layout checks at representative 320, 768, 1,280, and
      1,440-pixel viewports. Assert that every image is contained by its
      reading column and that neither the page nor the figure introduces
      unintended horizontal overflow.
- [x] Include visual review of every figure in the regular rendered-page
      sampling pass. Automated bounding-box checks catch overflow but cannot
      decide whether labels, legends, and annotations remain comfortably
      readable.

Definition of done:

- [x] All nine images render as numbered, captioned, deep-linkable semantic
      figures in manuscript order.
- [x] The site, standalone HTML, print, and future PDF use the same figure IDs
      and numbering scheme.
- [x] No figure exceeds its reading or printable column, and simple charts no
      longer expand unnecessarily to the full available width.
- [x] The crossover surface has a reader-friendly panel layout at desktop and
      mobile widths.
- [x] Figure structure, numbering, cross-references, accessibility, sizing,
      print behavior, and visual QA are enforced by the regular checks.

## 19. Add SpaceXAI scenario tracks to every relevant simulation

### Correct and date the market-position premise

- [x] Do not state that SpaceXAI is the only company visibly pursuing
      off-planet AI clusters. As of July 2026, Google/Planet's Project
      Suncatcher targets two prototype satellites for early 2027, Starcloud
      reports that it launched an H100-equipped satellite in November 2025,
      and Blue Origin has filed for the Project Sunrise data-center
      constellation.
- [x] Use the narrower, supportable formulation: SpaceXAI currently presents
      the largest and most vertically integrated publicly disclosed
      orbital-AI roadmap, combining launch, satellite manufacturing,
      connectivity, terrestrial AI, an AI1 vehicle specification, and an
      application for a constellation of up to one million satellites.
- [x] Put an “as of” date and a defined comparison class on any leadership or
      uniqueness statement. Recheck the competitor set for every release;
      market position is not a permanent premise of the model.
- [x] Keep the named SpaceXAI track because it is central to the article's
      strategy hypothesis and supplies unusually specific public design
      inputs—not because competitors are assumed not to exist.

Primary landscape checks:

- [SpaceX Starmind AI1 product
  specification](https://www.spacex.com/spacexai/starmind)
- [FCC notice accepting SpaceX's orbital-data-center application for
  filing](https://docs.fcc.gov/public/attachments/DA-26-113A1.pdf)
- [Google Project
  Suncatcher](https://blog.google/innovation-and-ai/technology/research/google-project-suncatcher/)
- [Planet's two-satellite Suncatcher mission
  announcement](https://www.planet.com/pulse/planet-to-build-and-operate-advanced-space-platform-for-google-s-project-suncatcher-moonshot/)
- [Starcloud-1 first-party mission
  page](https://www.starcloud.com/starcloud-1)
- [FCC public notice containing Blue Origin Project
  Sunrise](https://docs.fcc.gov/public/attachments/DOC-420864A1.pdf)

### Define a standard scenario stack

- [x] Every **relevant** simulation, table, and figure should expose the same
      ordered scenario tracks when its variables can be mapped honestly:
      `generic_reference`, `independent_reference`,
      `spacexai_disclosed_design`, and `spacexai_stated_aspiration`.
- [x] Define `spacexai_disclosed_design` from dated, directly disclosed AI1
      quantities such as 150 kW peak compute payload, 120 kW average compute
      payload, 150 kW solar array, 70 kW/t vehicle efficiency, 110 m²
      radiator, and the disclosed deployed envelope. Do not call this
      “current operating capacity”: no commissioned AI1 cluster is established
      by those specifications.
- [x] Define `spacexai_stated_aspiration` separately from the disclosed design:
      examples include the long-run 100 kW/t, up to 100 GW of orbital AI
      compute deployed per year, V3/V4 payload targets, and the derived
      ≤$185/kg launch-cost aspiration already registered in the manuscript.
- [x] Add `spacexai_hybrid_completion` only when a simulation cannot run
      without undisclosed inputs. Label every completed field as an independent
      anchor or `ASSUMPTION`, show the fraction of the parameter vector supplied
      by the company, and never abbreviate the result to “the SpaceXAI case.”
- [x] Use an independent comparison only when its quantity and denominator are
      commensurable. Prefer the existing independent system studies in
      [S39–S44], and use Suncatcher or Starcloud observations where their
      hardware, power, topology, or mission metric actually matches the
      simulated output.
- [x] If no company or independent value maps to a simulation, record
      `not_parameterizable` with the missing fields. Do not invent a special
      line merely to satisfy visual symmetry.

### Define where the rule applies

- [x] Apply the scenario stack to models of orbital-compute cost, launch mass
      and cadence, vehicle power and thermal balance, hardware life and
      qualification, communications, deployment growth, constellation
      topology, debris exposure, repair/replacement, and any lunar or asteroid
      supply case explicitly connected to SpaceXAI's stated roadmap.
- [x] Audit the baseline, deep, integrated, and Part II runners and every
      derived table/figure. Part II's existing Starmind AI1 disclosed and
      aspirational cases are the template, not proof that the rest of the
      simulation suite complies.
- [x] Do not force a SpaceXAI line into abstract numerical-method tests,
      generic digital-R&D loop equations, terrestrial rehearsal diagnostics,
      or physical-closure experiments for which SpaceXAI has published no
      corresponding architecture or coefficient.
- [x] In simulations where only one axis is disclosed—for example vehicle
      efficiency but not life, utilization, qualification cost, link cost, or
      availability—show the disclosed point against an independent sensitivity
      surface rather than presenting a falsely complete company trajectory.

### Preserve evidence classes and denominators

- [x] Every plotted line and table row must name both scenario and evidence
      class, for example:
      “SpaceXAI — AI1 disclosed design (company statement; accessed
      2026-07-27)” and “SpaceXAI — long-term target plus favorable model
      assumptions.”
- [x] Keep observed operation, disclosed design, near-term target, and long-run
      aspiration as four distinct states. A filed application is not an
      authorization; nameplate power is not delivered IT load; per-satellite
      kW is not annual GW deployed; manufacturing throughput is not operating
      constellation capacity.
- [x] Do not mix peak and average kW, power and FLOP/s, payload and total
      vehicle mass, launched and commissioned capacity, annual cadence and
      cumulative stock, or serviceable-platform and disposable-satellite
      architectures.
- [x] Company statements may define deterministic comparison points or axes.
      They must not become Monte Carlo priors, empirical probabilities, or
      achieved-performance distributions without independent observations.
- [x] When independent assumptions complete a company case, propagate their
      uncertainty and display which conclusion is controlled by company data
      versus the completion assumptions.

### Make this an article and modeling guideline

- [x] Add a named rule to `docs/EDITORIAL_STYLE.md`, binding human and agent
      edits: every quantitatively relevant off-planet-AI claim must show the
      neutral reference, the SpaceXAI disclosed-design point where
      parameterizable, the separately labelled aspiration, and an independent
      comparator or an explicit explanation of why none is commensurable.
- [x] Add a companion modeling policy describing scenario eligibility,
      evidence-tier vocabulary, allowed gap completion, display order,
      provenance requirements, competitor-refresh protocol, and exclusions.
- [x] Require the neutral and independent cases to remain present and visually
      equal. The mandatory named-company line must not silently replace the
      generic baseline, become the central estimate, receive a favorable
      parameter completion unavailable to competitors, or dominate chart
      styling.
- [x] State the reason for the rule in the article guidelines: SpaceXAI is a
      decision-relevant, falsifiable real-world trajectory against which the
      general model can be tested, while independent cases protect the analysis
      from becoming a company narrative.

### Centralize implementation and provenance

- [x] Create one versioned scenario registry, or extend the existing anchor
      registry, so the same SpaceXAI quantities and labels feed every runner.
      Do not duplicate AI1 or aspiration numbers inside scripts, captions, and
      prose.
- [x] Give each input a source date, locator, evidence class, unit, denominator,
      current/design/target state, direct-versus-derived flag, and list of
      simulations in which it is permitted.
- [x] Produce a generated
      `outputs/integrated/tables/simulation_scenario_coverage.csv` with one row
      per simulation/output and columns for the generic, independent,
      SpaceXAI disclosed, SpaceXAI aspiration, and hybrid/not-parameterizable
      tracks.
- [x] For every result table, include stable `scenario_id`,
      `evidence_class`, `source_snapshot`, `parameter_completeness`, and
      `boundary` fields so displayed labels can be regenerated rather than
      hand-maintained.
- [x] Archive all mutable company pages and filings used for inputs and keep
      their content hashes in claim provenance. A new disclosure creates a new
      scenario version; it must not silently rewrite historical results.

### Add regular policy checks

- [x] Add a coverage check that fails when a relevant simulation omits the
      required scenario tracks without a documented `not_parameterizable`
      reason.
- [x] Reject rows that combine disclosed and assumed values without a hybrid
      label, use a target as achieved capacity, omit the source date, or change
      denominators across comparators.
- [x] Add invariant tests showing that inserting SpaceXAI cases does not alter
      the generic/independent results or their random draws.
- [x] Add table and plot tests for stable scenario ordering, legend labels,
      evidence classes, source footnotes, and accessible non-color-only visual
      differentiation.
- [x] Run the competitor-refresh check and source-link audit as part of release
      review. Changes in competitors update contextual claims and comparison
      cases but do not retroactively change generic assumptions.

Definition of done:

- [x] Every simulation relevant to orbital AI either includes the generic,
      independent, SpaceXAI disclosed-design, and SpaceXAI aspiration tracks or
      records why a track cannot be parameterized.
- [x] The disclosed AI1 design and long-term aspirations are visibly distinct
      from achieved capacity and from independently completed assumptions.
- [x] The article guidelines make the policy mandatory while preserving
      neutral baselines, independent comparison, evidential symmetry, and
      dated competitor context.
- [x] All scenario lines regenerate from a single provenance-backed registry,
      and regular checks prevent omissions, stale labels, or evidence-class
      leakage.

## 20. Refine the SpaceXAI uniqueness claim around closure-stack verticalization

The strategically relevant distinction is not that SpaceXAI is the only visible
orbital-AI project. It is that, as of July 2026, it appears to be the only
publicly documented effort attempting to assemble most of the mutually
dependent layers needed for a scalable off-planet AI and, eventually,
self-sustaining industrial ecosystem. Treat this as a dated comparative
hypothesis to test, not as a timeless fact or a claim that physical closure has
already been achieved.

- [x] Replace broad “only company pursuing off-planet AI” language with a
      narrower claim about **breadth of verticalization across the closure
      stack**. A candidate formulation is: “SpaceXAI is currently unique among
      publicly documented orbital-AI programs in combining reusable launch,
      spacecraft and constellation manufacturing, orbital communications,
      terrestrial AI compute, frontier models and real-time data within one
      corporate platform, while also pursuing orbital solar compute and
      vertically integrated chip fabrication.”
- [x] When discussing the larger ecosystem, distinguish corporate boundaries:
      Tesla is not part of SpaceXAI. Describe Tesla, The Boring Company and
      other Musk-led or affiliated companies as a **collaborating industrial
      ecosystem**, not as assets owned or controlled by SpaceXAI. Record the
      contractual, ownership and evidence basis for attributing any capability
      to a joint scenario.
- [x] State what the wider ecosystem plausibly contributes: stationary energy
      storage and microgrid control, solar deployment experience, batteries and
      cathode production, pilot lithium refining, semiconductor collaboration,
      terrestrial manufacturing, autonomous vehicles and Optimus robotics.
      Do not translate those terrestrial capabilities into space-qualified,
      autonomous or off-planet capacity without a separate observable.
- [x] Separate four levels for every layer: `operational`, `demonstrated`,
      `under_development`, and `stated_aspiration`. “Effort to verticalize” is
      supportable where “owns a complete self-sustaining stack” is not.
- [x] Explicitly list the unresolved closure gaps, including extraterrestrial
      mining and beneficiation, refining beyond a narrow set of battery
      materials, bulk metals and polymers, semiconductor independence,
      autonomous construction, in-space repair and recycling, biological life
      support, and reproduction of production equipment.
- [x] Preserve the counterevidence. SpaceX's public filings say that it still
      depends on third parties for key materials and components and expects to
      source a significant share of compute hardware externally. Terafab is a
      proposed collaboration whose specific projects require later agreements;
      it is not current chip self-sufficiency.

### Build a closure-stack comparison

- [x] Add a provenance-backed matrix with rows for launch and transport,
      spacecraft manufacturing, power generation, storage and grid control,
      communications, AI compute, models and data, chip design, chip
      fabrication and packaging, robotics, construction, mining, beneficiation,
      refining, bulk-material production, maintenance and repair, recycling,
      and reproduction of capital equipment.
- [x] For each row record the responsible legal entity, relationship to
      SpaceXAI, terrestrial versus space-qualified status, maturity level,
      demonstrated capacity, stated target, missing dependencies, source date
      and evidence class.
- [x] Compare SpaceXAI and its explicitly bounded affiliated ecosystem with
      Google/Planet, Starcloud, Blue Origin and any other current integrated
      program. The intended test is whether another actor matches the
      **coverage and coupling of layers**, not whether competitors have activity
      in any single layer.
- [x] Derive summary measures only after publishing the matrix: weighted layer
      coverage, fraction under common control, demonstrated-closure fraction,
      dependency concentration and the minimum missing cut set preventing
      self-sustainability. Do not turn a qualitative brand association into a
      quantitative closure score.

### Connect the distinction to simulations and editorial guidance

- [x] Use breadth of the closure-seeking stack—not an assertion that no
      competitors exist—as the rationale for retaining a named SpaceXAI line in
      every relevant simulation.
- [x] Let a simulation use Tesla or another affiliate's parameters only through
      an explicitly labelled `spacexai_affiliate_hybrid` scenario. Keep those
      inputs separate from SpaceXAI-disclosed design values and propagate
      uncertainty about transfer, qualification and availability.
- [x] Add an editorial rule that all “unique,” “integrated,” “full stack,”
      “self-sustaining” and “closed loop” claims must specify the actor boundary,
      comparison class, maturity threshold, missing layers and “as of” date.
- [x] Add a regular check that flags language implying that affiliated
      companies are one legal entity, terrestrial capability is already
      space-qualified, planned capacity is operational, or broad vertical
      integration proves physical closure.

Primary evidence to register:

- [SpaceX 2026 prospectus: integrated space, connectivity and AI platform,
  orbital-compute thesis, vertical integration and third-party
  dependencies](https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm)
- [SpaceX prospectus amendment: Terafab scope, continued external chip sourcing
  and prospective Tesla collaboration](https://www.sec.gov/Archives/edgar/data/1181412/000162828026040364/spaceexplorationtechnologib.htm)
- [Tesla Q1 2026 filing: separate-company relationship, Megapack transactions,
  Optimus, battery materials and lithium-refining
  status](https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/tsla-20260331.htm)
- [Tesla AI and Robotics overview](https://www.tesla.com/AI)
- [SpaceX Mars roadmap: the company's own list of industries required for a
  permanent off-planet settlement](https://www.spacex.com/mars?embed=true)

Definition of done:

- [x] The article makes the strongest supportable claim: SpaceXAI is a uniquely
      broad and tightly coupled effort toward industrial closure, while neither
      equating affiliated firms with SpaceXAI nor presenting the still-open
      physical-closure gaps as solved.
- [x] The closure-stack matrix, simulations and prose regenerate from the same
      actor-bounded and maturity-labelled evidence registry.

## Remove release-status material from the opening article flow

The article currently places a long “Status” callout before the abstract and
then a “Scope and Status” section before the executive summary. Release
housekeeping should not be the reader's entry point. Preserve the substantive
epistemic boundaries, but separate them from mutable build and publication
status.

- [x] Remove the opening `> **Status.**` release-candidate callout from
      `docs/manuscript/00-front-matter.md` and regenerate the assembled Markdown
      and HTML. Do not leave a working-tree/build checklist above the abstract.
- [x] Split the information currently packed into that callout:
  - immutable version, date, DOI and repository link belong in compact
    publication metadata or a footer;
  - regeneration commands and manifests belong in the reproducibility
    appendix or repository documentation;
  - assumption-class and non-forecast caveats belong beside the relevant
    methods and results, with a concise version retained in the abstract.
- [x] Rename “Scope and Status” to something reader-facing such as “Scope,
      Claims, and Evidence.” Its machine-only boundary, proposition map and
      evidence taxonomy are substantive and should not be discarded merely
      because release-status narration is removed.
- [x] Reconsider its location. Prefer beginning with the abstract and executive
      summary, then introduce the detailed scope/proposition/evidence framework
      at the first point where readers need it. Test whether a short scope
      paragraph is sufficient in the main narrative while the full matrix lives
      in methods or an appendix.
- [x] Update all TOC entries, anchors and internal references currently pointing
      to `#scope-and-status`; preserve redirects or alias anchors if published
      links may already exist.

### Optional companion status page

- [x] First decide whether a public status page serves a reader need. If it
      only reports unfinished release chores, keep that information in project
      tracking rather than publishing it.
- [x] If retained, generate a separate HTML page such as
      `docs/release-status.html` from authoritative release metadata,
      manifests, CI results and provenance records. Do not maintain another
      hand-written copy of mutable status prose.
- [x] Link it unobtrusively as “Version and reproducibility” from the article
      footer or metadata area, not as a primary section or prominent
      interruption.
- [x] Give the page an explicit generation timestamp and distinguish
      manuscript version, release state, artifact verification and empirical
      claim status. A green build must not imply that the article's hypotheses
      are empirically verified.

### Make opening-flow checks regular

- [x] Add a source-level check that the reader-facing manuscript proceeds from
      title/byline/deck to abstract without a release-status block, TODO text,
      dirty-worktree narration or CI instructions.
- [x] Add a rendered-HTML check for the intended opening order and ensure a
      separate status page, if present, is reachable from the footer and
      excluded from the article TOC.
- [x] Extend the standalone-prose/readability checks so operational project
      narration cannot leak back into the article opening.

Definition of done:

- [x] The article opens directly with its intellectual content rather than
      repository status, while essential scope and epistemic qualifications
      remain easy to find.
- [x] Any public build/release status is optional, generated from authoritative
      records on a separate page, and clearly distinguished from evidential
      status.

## Steel-man the Musk/SpaceXAI economic perspective in Part II

This fits the article well if presented as a rival, testable economic frame
rather than as authority or promotional color. The current model asks for
dollars per frontier-equivalent kW-year of delivered IT load. Musk's public
claim and SpaceX's more complete filing-based argument ask about lowest cost
per token and fastest time to useful compute. Showing both frames will make the
disagreement more precise and reveal which conclusions are caused by different
assumptions versus different denominators.

### State the proponent's case accurately

- [x] Add a compact boxed subsection in Part II titled along the lines of “The
      SpaceXAI economic thesis.” Prefer the first-party SpaceX prospectus, SEC
      correspondence, roadshow materials and Starmind specification; use
      Musk's personal statements to establish the dated prediction, not as
      engineering evidence.
- [x] Present the strongest documented version of the argument:
  1. cost per token is a function of model efficiency, compute hardware and
     energy;
  2. near-continuous orbital solar reduces marginal energy cost and avoids
     terrestrial grid, land and permitting delays;
  3. radiative rejection can reduce cooling-power overhead, while reusable
     launch, satellite mass production and Starlink links reduce deployment
     and distribution costs;
  4. faster deployment can activate newer, more efficient chips earlier,
     increasing useful tokens before a terrestrial facility clears its
     construction and interconnection queue;
  5. proprietary chips and prospective Terafab integration are intended to
     attack compute depreciation, which SpaceX itself identifies as the
     largest cost-per-token component; and
  6. increasing cadence and roughly 100 kW/t are intended eventually to support
     a 100 GW/year orbital-compute deployment rate.
- [x] Do not caricature Musk's view as “energy is the whole cost.” That is a
      fair description of some short public explanations, but SpaceX's SEC
      response explicitly identifies compute depreciation as the largest
      component and couples minimal marginal energy with lower hardware cost.
- [x] Quote or paraphrase the January 2026 prediction that orbit would become
      the lowest-cost place for AI within two years, three at the latest. Treat
      January 2028–January 2029 as a falsifiable claim window and preserve the
      exact event date, wording, source and comparison ambiguity.
- [x] State what the public case does **not** yet provide: a disclosed
      comparable cost-per-token figure, fixed workload and quality boundary,
      full lifecycle bill, demonstrated AI1 availability/life, or a
      commissioning and replacement record.

### Reconcile the economic denominators

- [x] Put the two questions side by side:
  - the existing `$/frontier-equivalent kW-year` metric isolates delivered,
    hardware-normalized compute capacity and exposes spacecraft lifecycle
    costs;
  - `$/useful output token` additionally depends on model architecture,
    quantization, batching, workload mix, accepted-output rate, network
    goodput, service quality and utilization.
- [x] Add an inference-only translation layer using a fixed model, precision,
      workload, output-quality threshold and service-level boundary. Report
      dollars per million **accepted** output tokens, not raw generated tokens.
      Do not mix training tokens, inference tokens and model-quality changes in
      one metric.
- [x] Keep the current LCO metric as the engineering reference. A token metric
      can test the company's commercial thesis but must not hide short life,
      replacement launch, qualification, bandwidth or unavailable capacity
      inside a favorable throughput assumption.
- [x] Add a schedule-aware comparison for “time to useful compute”: terrestrial
      construction and grid-interconnection delay versus launch, production,
      commissioning and constellation-ramp delay. Value timing explicitly
      through discounted useful output or cost of delayed capacity rather than
      implying that ordinary WACC captures the entire option value.

### Turn the claim into a discriminating test

- [x] Create a “proponent claim → model term → required observable → current
      result” table covering solar availability, cooling overhead, launch
      price and cadence, satellite manufacturing cost, kg/kW, chip cost and
      efficiency, useful life, availability, communications, replacement,
      time-to-power and terrestrial power escalation.
- [x] Add a deterministic `spacexai_proponent_case` built only from dated
      company quantities. Where the public argument leaves required inputs
      blank, display `not_disclosed`; do not silently fill every gap with the
      model's favorable bound.
- [x] If an executable comparison requires gap completion, create a separately
      named `spacexai_proponent_hybrid` and expose each independent or
      `ASSUMPTION` completion. Never report it as “Musk's cost estimate.”
- [x] Produce a threshold or tornado view showing what must be true
      simultaneously for orbital compute to beat Earth under both LCO and
      accepted-token metrics, and which assumption controls the two-to-three
      year forecast.
- [x] Compare the proponent case against the generic model and independent
      studies with identical workload, date, maturity, financing and system
      boundary. Company statements remain deterministic comparison targets,
      never Monte Carlo priors or probabilities.
- [x] Preserve the point of genuine agreement: orbital solar can lower the
      energy term and extremely favorable integrated architectures can approach
      parity. Then state the present disagreement in model terms—qualification,
      hardware cost, lifetime, utilization, thermal-system mass, replacement
      and communications—not as a judgment about personalities.

### Fix the Part II baseline before adding the comparison

- [x] Resolve the stale chip-efficiency sensitivity prose in
      `docs/manuscript/20-part-ii-comparative-economics.md`. It currently says a
      2× FLOPS/W improvement captures about 39% of the benefit of halving launch
      price (4.0 versus 3.2 from 4.5), while the generated
      `outputs/report_part2.md` says about 50% (5.1 versus 4.2 from 6.1).
      Regenerate from one authoritative result and add a consistency check so
      narrative numbers cannot diverge from the output table again.

Primary evidence to register:

- [SpaceX prospectus: cost-per-token framework, time-to-power thesis and
  100 GW/year objective](https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm)
- [SpaceX response to SEC: compute depreciation, energy and lack of a disclosed
  comparable cost-per-token figure](https://www.sec.gov/Archives/edgar/data/1181412/000162827926000584/filename1.htm)
- [SpaceX orbital-compute roadshow
  slides](https://content.spacex.com/cms-assets/assets/SpaceX%20IPO%20Roadshow.pdf)
- [Starmind AI1 first-party
  specification](https://www.spacex.com/spacexai/starmind)

Definition of done:

- [x] A reader can reconstruct the strongest SpaceXAI economic argument,
      understand why its preferred denominator differs from the article's, and
      see both evaluated on explicit common assumptions.
- [x] The January 2026 forecast is a dated and falsifiable comparison target,
      not an input prior, and no undisclosed quantity is attributed to Musk or
      SpaceXAI.
- [x] All numerical comparisons regenerate consistently from model outputs.

## Number and cross-reference all substantive tables

- [x] Inventory every reader-facing table in the manuscript, including
      hand-written Markdown tables and tables injected from generated reports.
      Distinguish substantive article tables from layout grids, navigation,
      CSV-preview modals and internal status widgets; only substantive article
      tables enter the article's numbering sequence.
- [x] Give every substantive table a short descriptive caption and stable
      semantic identifier such as `tbl-orbital-lifecycle-cost`. Let the document
      build assign displayed numbers from source order rather than typing
      numbers into captions by hand.
- [x] Use a consistent publication convention: “Table 1,” “Table 2,” and so on
      in the main text, with appendix tables using an explicit series such as
      “Table A1.” Put table captions above tables unless the selected venue
      requires otherwise.
- [x] Replace “the table below/above” and ambiguous bare references with
      generated links such as “Table 4.” References must target the stable
      identifier so they continue to resolve if displayed numbers change.
- [x] Ensure numbering and links survive the complete source → assembled
      Markdown → HTML/print pipeline. A table split across print pages should
      repeat its header and identify subsequent portions as continued without
      consuming another table number.
- [x] Include an unobtrusive “View data” link in a caption when the table has a
      canonical CSV source. The interactive CSV preview does not receive a
      second article-table number unless it is itself a distinct, cited table.
- [x] Add table captions and IDs to the article's accessibility structure.
      Screen readers should associate the caption, column headers, row headers,
      units, notes and source/provenance link with the correct table.

### Add regular table checks

- [x] Add a source audit that fails on a substantive table without a stable ID
      or caption, duplicate IDs, manually embedded table numbers, unresolved
      table references, or references phrased only by relative position.
- [x] Add a rendered-HTML audit that verifies a unique visible number and
      caption for every substantive table, sequential ordering within the main
      and appendix series, working permalinks/cross-references and absence of
      accidental numbers on CSV modal tables.
- [x] Add print-layout visual checks for caption placement, repeated headers,
      continuation labels, page overflow and tables separated from their notes
      or sources.
- [x] Extend `docs/EDITORIAL_STYLE.md` with the numbering, caption,
      cross-reference, appendix and CSV-preview rules so new tables comply by
      default.

Definition of done:

- [x] Every substantive table can be cited unambiguously by a visible number
      and stable link in HTML and print, and regular checks prevent numbering
      regressions.

## Add OpenAI and Google DeepMind to the AI-R&D / RSI evidence framework

Investigation result: this is a material omission. OpenAI has published both
dedicated material and model-card evaluations; Google DeepMind supplies a
complementary framework for separating realized R&D acceleration from R&D
automation. These sources should refine the article's observables and system
boundary, but they do not establish that a verified recursive
self-improvement loop has closed.

### Extend the external evidence record

- [x] Add OpenAI and Google DeepMind rows to the external-record table in
      `docs/manuscript/10-part-i-foundations.md`, alongside Anthropic, METR,
      the RSI survey and AI 2027. Replace the claim that Anthropic is uniquely
      the most directly relevant frontier-lab account with a precise
      comparison:
      - Anthropic: operational self-report and the execution-versus-direction
        gap;
      - METR: independent task-horizon measurements;
      - AI 2027: an explicit fast-digital scenario, not observed evidence;
      - OpenAI: public AI-self-improvement thresholds plus component and
        end-to-end AI-R&D evaluations;
      - Google DeepMind: R&D-acceleration and R&D-automation thresholds,
        including model-plus-workflow effects.
- [x] Add versioned provenance entries to `params/claim_provenance.yaml` for
      each source below. Preserve the build's generated source-numbering
      convention rather than assigning `[S…]` labels manually.
- [x] Create a numbered cross-lab evidence table with these columns: source and
      version/date; construct; unit of evaluation; threshold or comparator;
      published result/status; article loop stage informed; and “what this
      does not establish.” Clearly distinguish company self-evaluation,
      external evaluation and scenario assumptions.

### Register and interpret the OpenAI evidence

- [x] Cite the OpenAI Preparedness Framework v2 and its dedicated update
      article. Record AI Self-Improvement as a tracked category and preserve
      the framework's distinction between:
      - **High**: impact comparable to giving every OpenAI researcher a strong
        mid-career research-engineer assistant, relative to a 2024 baseline;
      - **Critical**: recursively self-improving or fully automated AI R&D,
        operationalized as either a superhuman research-scientist agent or a
        sustained generational model improvement in roughly one-fifth of the
        2024-equivalent wall-clock time.
      Treat High as an assistant/acceleration threshold, not loop closure.
- [x] Add OpenAI's dedicated PaperBench release. Describe it accurately as an
      AI-research-replication benchmark: agents reproduce 20 ICML 2024
      Spotlight/Oral papers from scratch against 8,316 author-developed rubric
      items. Record the initial best tested result (about 21%, below the
      reported top ML-PhD baseline) with the exact agent, harness, date and
      scoring version. Do not call PaperBench “an RSI benchmark”; it observes
      research replication and engineering, which are upstream components of
      an AI-R&D loop.
- [x] Register the current GPT-5.6 AI Self-Improvement evaluation suite and
      explain what each component observes:
      - Internal Research Debugging Evaluation: real research-code defects and
        alignment-auditing tasks;
      - KernelGen 1P: correct, non-gamed hardware-kernel optimization;
      - NanoGPT: small-model pretraining-loop improvement under a fixed
        one-H100 budget;
      - PostTrainBench Lite: execution of a complete post-training/RL strategy
        under a fixed compute and time budget;
      - MLE-Bench Revised: Kaggle-style ML engineering;
      - METR Time Horizon 1.1: externally run long-horizon task performance.
- [x] Report OpenAI's current conclusion that the GPT-5.6 family is below its
      High AI Self-Improvement threshold as an **as-of July 2026 company
      assessment**, not an independent fact or a timeless claim. Preserve the
      card's qualifications: benchmark saturation, unsolvable items,
      contamination or reward-hacking/“cheating,” scaffolding dependence,
      evaluator validity and the difference between small-scale tasks and
      frontier training runs.
- [x] Do not double-count METR Time Horizon evidence when it appears both in a
      METR source and an OpenAI system card. Keep the independent evaluator,
      model/harness, run date and interpretation attached to the same
      observation.
- [x] Tag non-public OpenAI tasks and rubrics as company-reported or only
      partially auditable. Their realism is useful, but it does not substitute
      for reproducible external evidence.

Primary OpenAI sources:

- `https://openai.com/index/paperbench/`
- `https://openai.com/index/updating-our-preparedness-framework/`
- `https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf`
- `https://deploymentsafety.openai.com/gpt-5-6`
- `https://openai.com/index/strengthening-safety-with-external-testing/`

### Register and interpret the Google DeepMind evidence

- [x] Cite *An Approach to Technical AGI Safety and Security* and use its
      automated-R&D positive-feedback mechanism as conceptual support for the
      digital-loop hypothesis. Keep its possible-AGI timeline and continuity
      assumptions labeled as DeepMind assumptions rather than article inputs
      or empirical forecasts. Note that the paper addresses only some
      recursive-improvement risks and explicitly leaves other
      superintelligence questions out of scope.
- [x] Cite Frontier Safety Framework 3.1 and preserve its two distinct ML R&D
      capability levels:
      - **ML R&D acceleration level 1**: the system has actually been used to
        accelerate AI development substantially beyond historical rates;
      - **ML R&D automation level 1**: the system can fully automate the work
        of any Google research team improving AI capabilities at approximately
        comparable all-inclusive cost.
      The first is a realized, lagging outcome; the second is a capability and
      economic-substitution threshold. Neither is identical to the article's
      verified safe-successor-deployment closure.
- [x] Use DeepMind's statement that acceleration is expected from systems of
      models integrated into R&D workflows—not from a model in isolation—to
      strengthen the article's system boundary. Evaluations must therefore
      record tools, agents, human review, compute, data access, organizational
      workflow and elapsed time.
- [x] Preserve DeepMind's distinction between public release and high-risk
      internal deployment. This supports the article's point that internal
      benefits may appear before public release, while verification and
      containment constraints still apply to consequential internal use.
- [x] Mention *Levels of AGI* only if a capability/generality ontology is
      useful at the insertion point. Do not use it as direct evidence for
      recursive self-improvement.

Primary Google DeepMind sources:

- `https://deepmind.google/blog/taking-a-responsible-path-to-agi/`
- `https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf`
- `https://deepmind.google/blog/strengthening-our-frontier-safety-framework/`
- `https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf`
- `https://deepmind.google/research/publications/66938/`

### Convert the sources into article observables, not coefficient guesses

- [x] Create
      `outputs/integrated/tables/ai_rnd_benchmark_registry.csv` and
      `outputs/integrated/tables/ai_rnd_evidence_crosswalk.csv`. At minimum,
      decompose the proposed AI-R&D loop into task selection/research taste,
      hypothesis generation, implementation, experiment execution, debugging,
      compute/kernel optimization, training and post-training, evaluation,
      safety verification, deployment and measured successor-model gain.
- [x] Map every benchmark only to the stages it directly observes. Do not
      insert PaperBench scores, preparedness classifications or system-card
      pass rates directly into `G_n`, `z_n`, loop rates, physical-transfer
      parameters or other simulation coefficients. A mapping requires
      compatible units, denominators, human baselines, scaffolding and compute
      assumptions.
- [x] Keep four analytic gates separate even when a lab uses overlapping
      language:
      1. assistant-equivalent capability;
      2. realized R&D acceleration;
      3. broad R&D automation;
      4. verified recursive closure, including successor gain, evaluation,
         safe deployment and recurrence.
- [x] Add a concise synthesis after the external-record table: frontier labs
      increasingly treat AI-enabled R&D as measurable and safety-relevant;
      public evaluations show meaningful performance on several component
      tasks, but no cited public source demonstrates a verified, recurring,
      end-to-end successor-model loop. OpenAI's Critical threshold helps
      operationalize that endpoint; DeepMind's feedback-loop account supports
      the mechanism. Neither is evidence of embodied-production or
      reproductive-capital closure.

### Add regular evidence checks

- [x] Make the evidence audit require a source date, framework/benchmark
      version, model and harness, compute/tool access, comparator, evaluator
      independence and limitations for every AI-R&D result.
- [x] Fail on unqualified phrases such as “latest model,” “RSI benchmark,”
      “fully autonomous” or “recursive self-improvement” when the cited
      measurement covers only a component task.
- [x] Fail on cross-lab score comparisons unless the task, harness, budget,
      scaffolding, baseline and scoring rule are commensurable.
- [x] Add a scheduled source-refresh check for preparedness/system-card and
      Frontier Safety Framework revisions. A “below High” finding must not be
      allowed to imply no acceleration, no risk or general safety.

Definition of done:

- [x] The article treats OpenAI and Google DeepMind as substantive,
      provenance-tagged evidence sources; readers can see exactly which
      AI-R&D stages each source measures; and no benchmark or lab threshold is
      presented as proof of verified RSI closure.

## Express the core intelligence–industry feedback loop as an equation

The front matter currently presents
“better intelligence → better automation → more productive capacity → more
compute → better intelligence” as a code block. This is a causal summary, but
the article's central loop should be stated as a compact dynamical system and
then paraphrased in prose.

- [x] Replace the arrow chain in
      `docs/manuscript/00-front-matter.md` with a numbered equation using the
      article's canonical notation. Edit the manuscript source, not generated
      `docs/Recursive_Industrial_Intelligence_r4.0.md` or its HTML derivative.
- [x] Use a coupled recurrence of the following form, adapting symbols to
      existing definitions rather than creating aliases:

      \[
      \begin{aligned}
      A_{t+1} &= A_t + f_A(I_t;\,\theta_A),\\
      P_{t+1} &= P_t + f_P(A_{t-\tau_A},R_t;\,\theta_P),\\
      C_{t+1} &= C_t + f_C(P_{t-\tau_P},E_t,H_t;\,\theta_C),\\
      I_{t+1} &= I_t + f_I(C_{t-\tau_C},D_t,V_t;\,\theta_I).
      \end{aligned}
      \]

      Here the intended state sequence is intelligence \(I\), automation
      capability \(A\), productive capacity \(P\), and usable compute \(C\);
      \(R\), \(E\), \(H\), \(D\), and \(V\) represent limiting material
      resources, energy, hardware, data, and verification. The final notation
      must match the definitions and units already used in the model.
- [x] If the article needs a one-line diagnostic of recursive amplification,
      derive the local loop gain from the coupled system—for example, as the
      product of the four relevant local elasticities or, more generally, the
      spectral radius of its Jacobian. State the precise conditions under
      which gain greater than one implies amplification; do not present it as
      sufficient for physical closure, stability, safety, or indefinite
      growth.
- [x] Preserve delays, saturation, depreciation, resource ceilings and
      verification/deployment gates. A bare multiplicative equation would
      misleadingly imply instantaneous, unconstrained conversion between the
      four stages.
- [x] Follow the equation with the existing plain-language sentence so
      nontechnical readers receive the intuition without having to interpret
      the notation. Link every term to the planned click-to-explain equation
      glossary/modal.
- [x] Cross-reference the numbered equation wherever the same loop is
      described later in Part I, avoiding a second informal definition or
      inconsistent variable names.

### Add regular equation checks

- [x] Add a source check that flags causal arrow chains presented as code when
      they define a modeled relationship, undefined symbols, duplicate
      equation labels and unresolved equation references.
- [x] Extend the dimensional/notation audit to the new recurrence and verify
      that the explanatory modal, HTML rendering and print/PDF rendering all
      expose the same definitions.

Definition of done:

- [x] The article's headline feedback loop is a numbered, dimensionally
      coherent dynamical equation with delays and constraints, while an
      adjacent prose explanation keeps the intuition accessible.

## Make CSV viewing the primary action and downloads explicit

Investigation result: the multi-page reader site already has most of the
requested viewer—native modal dialog, searchable and sortable table,
pagination, sticky column headers, mobile layout, focus return, deep links,
and an explicit download action. The current standalone HTML behaves
differently by design: `scripts/check-site.ts` requires it to contain
conventional CSV links and forbids the viewer shell. Browsers may consequently
open or download the raw CSV depending on response headers, browser settings,
and local-file behavior. Bring the editions into parity rather than building a
second viewer.

### Correct the interaction model

- [x] Make **View data** the primary reader action in both the multi-page site
      and `docs/Recursive_Industrial_Intelligence_r4.0.html`. Activating it
      should open the friendly table viewer without navigating away or
      initiating a download.
- [x] Keep **Download original CSV** as a separate, ordinary anchor with the
      `download` attribute and a descriptive accessible name such as
      “Download digital elasticity bounds (CSV, 14 KB).” Do not use the same
      ambiguous link for both viewing and downloading.
- [x] Prefer a native `<button type="button">` for the JavaScript action that
      opens a modal and a native `<a href>` for navigation or download. If
      progressive enhancement starts from an anchor, its unenhanced `href`
      must lead to a readable HTML data page—not directly to a CSV whose
      behavior is browser-dependent.
- [x] When the viewer cannot initialize or load, do not silently activate the
      CSV. Show an inline error and offer an explicitly labeled **Download CSV**
      fallback. With JavaScript disabled, expose either a generated HTML table
      page or an explicit download link; never promise “View data” and then
      download it.
- [x] Replace the current generic external-link arrow appended to
      `.artifact-link` with a meaningful view-table affordance. Link/control
      text must communicate the result of activation without relying on an
      icon, hover tooltip, or surrounding visual layout.

### Reuse the viewer in the standalone HTML

- [x] Refactor the artifact viewer shell and behavior into one shared
      component used by `scripts/build-site.ts` and
      `scripts/build-manuscript.ts`; do not fork the TypeScript, table markup,
      styling or accessibility behavior.
- [x] Remove or revise the `scripts/check-site.ts` assertion that the
      standalone HTML must not contain an artifact viewer. Replace it with
      parity checks requiring every reader-facing artifact reference to open
      the same viewer in both editions.
- [x] Do **not** embed every CSV as expanded JSON in every HTML document. The
      multi-page reader site should retain one validated payload per artifact
      and lazy-load only the table a reader opens, caching it for that page
      session.
- [x] Treat the archival standalone HTML separately because it is advertised
      as self-contained and may be opened from `file://`. Design a size-aware
      tier:
      - embed only metadata and a bounded, clearly labeled preview for large
        tables;
      - embed a complete small table only below a configured per-artifact and
        total payload budget;
      - provide a link to the full HTML viewer plus an explicitly labeled CSV
        download whenever the full data is not embedded.
      A preview must disclose “first \(N\) of \(M\) rows” and must not make
      search or summary claims over rows that were omitted.
- [x] Consider a single compressed, lazily decoded payload for full offline
      coverage only if measured browser support, decompression time and file
      size beat the preview tier. Do not duplicate the same data as CSV, JSON
      and rendered table markup inside the standalone file.
- [x] Parse and validate each CSV once during the build, retain its manifest
      hash, and render cells using DOM `textContent`, never untrusted HTML.
      Defer payload decoding and row rendering until the corresponding viewer
      is opened.
- [x] Establish CI budgets for uncompressed standalone size, gzip/Brotli
      transfer size, embedded artifact bytes, startup time and first-view
      latency. Record the baseline before implementation: the current HTML is
      about 2.8 MiB and the 70 referenced CSVs total about 2.55 MiB before
      JSON/HTML expansion. Fail the build on an unexplained regression rather
      than assuming that doubling the document is acceptable.
- [x] Keep a stable artifact URL/hash so readers can copy a link to a specific
      table. Modified clicks and opening in a new tab should reach a readable
      HTML artifact view rather than bypassing the viewer and downloading raw
      data.

### Finish the friendly table presentation

- [x] Retain the existing scroll container, sticky `<th>` header row,
      pagination, search and sorting. Add a semantic `<caption>` tied to the
      artifact title and use `<th scope="col">`; configure `<th scope="row">`
      in the artifact registry when a CSV has a genuine row-identifier column.
- [x] Preserve raw values while presenting registered human-friendly column
      labels, descriptions and units. Visually align numeric columns, identify
      missing values accessibly, expose sort direction with `aria-sort`, and
      never infer units or precision from a column name alone.
- [x] For very wide tables, freeze a registered identifier column in addition
      to the header, with a visible boundary and no overlap at browser zoom.
      Horizontal scrolling must remain keyboard-accessible. On narrow screens,
      use the existing full-screen dialog treatment.
- [x] Keep charts optional and registry-driven. Offer a compact plot only when
      the artifact metadata declares meaningful axes, units and series; do not
      guess a chart from arbitrary CSV columns or make a chart the only way to
      read exact values.
- [x] Show title, short description, row/column counts, units, provenance
      class, source path and SHA-256 without letting metadata crowd out the
      table. Keep **Open full data page**, **Download original CSV**, and
      **Copy table link** as secondary actions.

### Meet modal-dialog and data-table accessibility guidance

- [x] Continue using native `<dialog>.showModal()` with a visible title,
      close button, contained tab sequence, Escape-to-close behavior and focus
      returned to the invoking control. Do not add `aria-describedby` for the
      entire structured table, because it would be announced as one long
      description.
- [x] Give the scrollable table region a useful accessible name and visible
      keyboard focus. Announce loading, failures, filtering results and page
      ranges through the existing polite status region without announcing
      every rendered cell.
- [x] Test at 200% and 400% zoom, keyboard only, reduced motion, forced colors,
      VoiceOver/Safari and at least one Chromium screen-reader combination.
      Verify that sticky headers do not obscure cells or controls.

Best-practice references:

- W3C WAI modal-dialog pattern:
  `https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/`
- W3C WAI data-table tutorial:
  `https://www.w3.org/WAI/tutorials/tables/`
- WCAG 2.2 link-purpose guidance:
  `https://www.w3.org/WAI/WCAG22/Understanding/link-purpose-in-context.html`
- MDN `<dialog>` reference:
  `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog`
- MDN anchor/download behavior:
  `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a`
- MDN scrollable table and sticky-header example:
  `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/table`

### Add regular CSV-viewer checks

- [x] Extend `scripts/check-artifact-viewer.ts` to run against both the reader
      site and standalone HTML, including local `file://` operation. Assert
      that an ordinary activation opens the dialog and does not issue a CSV
      navigation or download.
- [x] Verify unique accessible names, table caption/header associations,
      keyboard sorting, sticky headers, horizontal and vertical scrolling,
      pagination boundaries, filtered empty states, focus restoration,
      Escape/close behavior, history/deep-link behavior and mobile layout.
- [x] Add failure-mode tests for absent JavaScript, corrupt embedded payloads,
      manifest/hash mismatch and unavailable raw files. Every fallback must say
      explicitly that it downloads a CSV.
- [x] Add a build check that rejects raw reader-facing `.csv` links unless
      their accessible name contains “Download” and “CSV,” and rejects “View
      data” controls that lack a corresponding validated viewer payload.
- [x] Add an artifact-size report and enforce the configured per-table and
      total embedding budgets. Test both the raw local-file size and compressed
      network transfer size; neither may be hidden by reporting only the more
      favorable number.
- [x] Document the view-versus-download convention and artifact-registry
      metadata in `docs/EDITORIAL_STYLE.md` so future CSV references receive
      the behavior automatically.

Definition of done:

- [x] In every HTML edition, clicking a primary data reference opens an
      accessible, friendly inline table with frozen column headers; downloading
      occurs only through a control explicitly labeled as a CSV download;
      tested fallbacks never surprise the reader; and the standalone artifact
      remains within its declared size and latency budgets.
