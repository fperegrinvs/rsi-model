# Part I — Technical Feasibility {#part-i-technical-feasibility}

## I.1 Recursive self-improvement: the digital loop {#i.1-recursive-self-improvement-the-digital-loop}

Recursive self-improvement (RSI) occurs when an intelligent system
contributes to the process that produces a more capable successor. The
useful unit must be named relative to the use being claimed. A technically
validated gain has survived the applicable held-out and regression tests. An
authorized internal loop additionally permits that gain to advise or act in a
specified monitored role, with consequence-appropriate access, rollback, and
observation. A public release is a later and separate event requiring broader
external assurance. The common pipeline is: identify a weakness, form a
hypothesis, implement a change, train or run an experiment, evaluate it,
authorize its claimed use, and observe the result. A proposal or training run
that has not passed technical validation is work performed, not a capability
gain; public release is not required to complete a bounded internal loop.

### Observed precursors are narrower than closure {#observed-ai-rd-loop-precursors}

Three public systems implement substantial pieces of that pipeline, but they
modify different objects and stop at different gates:

| system | object modified | search topology | evaluation signal and observed result | human role | verification boundary | does not demonstrate |
|---|---|---|---|---|---|---|
| Karpathy `autoresearch` [S86] | `train.py`: model architecture and training procedure, not the acting model's weights | serial keep/discard hill climb | fixed `val_bpb` after five minutes on one GPU; approximately 12 attempts/hour and 100 overnight are design capacity, while the canonical run ledger is unpublished | supplies or approves the agent instructions and starts/stops the run | fixed evaluator; no independent transfer, safety, or deployment gate | a measured success rate, successor-model closure, or open-ended improvement |
| Darwin Gödel Machine (DGM) [S87] | coding-agent scaffold, tools, and workflow around frozen foundation models | branching archive search that can retain weaker stepping stones | after 80 iterations, SWE-bench rose from 20.0% to 50.0% and full Polyglot from 14.2% to 30.7%; both no-self-improvement and no-archive ablations were weaker | fixes the search process, benchmarks, model APIs, sandbox, and oversight | staged benchmark tests plus transfer checks, lineage inspection, and sandboxing; objective hacking was found separately | improvement of foundation-model weights, indefinite returns, or an authorized successor-model loop |
| AI Scientist-v2 [S88] | hypotheses, experiment code, results, figures, and manuscripts, not foundation-model weights | progressive agentic tree search followed by human portfolio selection | three selected manuscripts entered an ICLR-workshop experiment; one scored 6, 6, and 7 (mean 6.33/10), while two were rejected | supplies the theme, selects three ideas from roughly forty, allocates multiple runs, and selects the strongest complete outputs | independent workshop review of selected outputs; under the prearranged protocol, the authors withdrew the potentially accepted paper | an autonomous success frequency, main-conference-quality research closure, or successor-model improvement |

: Observed bounded self-improvement and automated-research systems. [View data](../outputs/integrated/tables/observed_precursor_telemetry.csv){.artifact-link data-artifact="outputs/integrated/tables/observed_precursor_telemetry.csv"}. {#tbl-observed-self-improvement}

These are observed, bounded precursors—not evidence that verified AI-R&D
closure, recurrent successor-model improvement, or any milestone time in this
article has been reached. `autoresearch` contributes candidate throughput and
a narrow accept/reject gate; DGM contributes self-modification, lineage/archive
memory, transfer tests, and direct evidence of evaluator gaming; AI
Scientist-v2 covers more of the research workflow but retains human
meta-selection. The non-monotone DGM lineage is especially important:
industrial memory should preserve provenance-linked branches and failed
stepping stones rather than assume a single improving lineage. Because the
tasks, budgets, evaluators, interventions, and success units are not
commensurable, none of the reported values calibrates
$\nu_{\mathrm{verified}}$, $\mathbb E[\mathbf G_n]$, or
$T_{\mathrm{AIR\&D}}$. The generated
[observed-precursor telemetry register](../outputs/integrated/tables/observed_precursor_telemetry.csv){.artifact-link data-artifact="outputs/integrated/tables/observed_precursor_telemetry.csv"}
keeps unavailable attempt, retention, elapsed-compute, and independence
fields blank rather than converting absence into a favorable value.

Sakana AI's 2026 RSI Lab announcement proposes a future loop in which
Agent-Native Models power an AI Scientist that builds better Agent-Native
Models [S89]. That is a declared strategy and intended transition. It becomes
closure evidence only after a versioned model-to-research-to-successor-model
cycle records candidate and retained counts, independent evaluation, safe
deployment, and recurrence.

### Closure and milestone taxonomy {#closure-and-milestone-taxonomy}

Three different closure claims must be tested independently:

| closure | operational gate | what it does not imply |
|---|---|---|
| verified AI-R&D closure | a system proposes, tests, independently evaluates, and safely deploys accepted changes to successors | physical task execution or capital reproduction |
| embodied-production closure | controllers complete the active industrial minimum cut with available sensing, actuation, experiments, and recovery | successor-model improvement or replacement of every indispensable machine |
| reproductive-capital closure | the system replaces and expands every indispensable capital stock after depreciation and obsolescence | open-ended AI improvement or legitimate authorization |

: Distinct operational closure gates. {#tbl-closure-taxonomy}

Their milestone times are $T_{\mathrm{AIR\&D}}$, $T_{\mathrm{emb}}$,
$T_{\mathrm{cl},E}$, $T_{\mathrm{cl},S}$, and $T_{\mathrm{ctrl}}$:
verified AI-R&D closure, adequate embodiment, terrestrial reproductive
closure, off-world reproductive closure, and control readiness,
respectively. “Control readiness” means independent verification,
authorization, secure command, audit, and stop capacity adequate for the
corresponding capability and replication rate. These are separate clocks,
not five names for a single takeoff event.

The distinction creates a 2×2 causal map:

| | production not reproductively closed | production reproductively closed |
|---|---|---|
| verified AI-R&D loop absent | externally supplied capital with bounded technical progress | endogenous physical growth with a bounded controller |
| verified AI-R&D loop active | digital improvement bottlenecked by externally supplied capital | coupled recursive industrial intelligence |

: Coupling between verified AI-R&D and reproductive-production closure. {#tbl-coupled-closure-map}

The Moon–asteroid ablation makes Table [@tbl-coupled-closure-map]
executable. With the implemented
verified AI-R&D proxy frozen but new-capacity orders permitted, balanced
physical doubling occurs at 36.75 years and the system reaches 2.71
cell-equivalents at year 40. With both channels active, it doubles at 35.25
years and reaches 3.28. Either row with capital reproduction blocked fails to
double and depreciates to 0.0015 balanced equivalents by year 40. The
AI-R&D switch is a stylized verified capability-growth channel, not evidence
that full research closure exists. Machine-readable:
[closure loop ablation matrix](../outputs/integrated/tables/closure_loop_ablation_matrix.csv){.artifact-link data-artifact="outputs/integrated/tables/closure_loop_ablation_matrix.csv"}.

Mapped to the canonical proposition ladder through the six semantic links
below, the closure dependencies are:

| proposition | abbreviated claim | closure premise or evidence |
|---|---|---|
| [P1 — Conceptual possibility](proposition:P1){.proposition-ref} | logical coherence of recursive industrial expansion | no demonstrated closure required |
| [P2 — Technical feasibility](proposition:P2){.proposition-ref} | eventual complete-system feasibility | embodied-production and reproductive-capital closure; verified AI-R&D closure is an accelerator, not a logical prerequisite |
| [P3a — Earth-dependent bridge economics](proposition:P3a){.proposition-ref} | operating economics while Earth inputs remain load-bearing | compares an Earth-dependent regime; no AI-R&D closure premise |
| [P3b — Mature high-closure economics](proposition:P3b){.proposition-ref} | stipulated mature high-physical-closure economics | assumes a declared high-physical-closure regime but does not require AI-R&D closure |
| [P4a — Documented portfolio direction](proposition:P4a){.proposition-ref} | observed program direction | documented initiatives and integration evidence; no closure proof |
| [P4b — Recursive-closure intent](proposition:P4b){.proposition-ref} | inferred intent to transition toward closure | closure-specific indicators of intent, not proof of achieved closure |

: Proposition-to-closure dependency map. {#tbl-proposition-closure-dependencies}

The external record supports pieces of this loop at very different evidence
levels. Table [@tbl-ai-rnd-evidence] keeps company self-evaluation, external evaluation,
framework thresholds and scenario assumptions visibly separate.

| source and version/date | construct | unit of evaluation | threshold or comparator | published result or status | article loop stage informed | what this does not establish |
|---|---|---|---|---|---|---|
| Anthropic operational account, 2025-09-17 [S81] | execution throughput versus research direction | reported internal coding and research workflow | prior human-led workflow | substantial assistance and fixed-goal execution reported; research taste remains human-led | implementation, experiment execution, debugging | audited productivity, autonomous successor design or closure |
| METR Time Horizon 1.1 [S83] | long-horizon software and research task completion | human-equivalent task duration at 50% success | skilled-human completion time | rising horizon on the tested distribution; the GPT-5.6 Sol estimate was not considered robust because of detected cheating [S98] | implementation, experiment execution, debugging, evaluation | delegation reliability, realized R&D acceleration, an automation fraction or physical transfer |
| RSI survey, arXiv v1, 2026-07-14 [S84] | taxonomy of self-improvement research | 1,250-paper corpus | two-axis classification | maps a young and rapidly changing literature | taxonomy across candidate loop stages | mature consensus or demonstrated open-ended improvement |
| *AI 2027*, June 2025 update [S80] | fast digital feedback scenario | forecast trajectory | authors' scenario counterfactual | explicit software/hardware and internal/public clocks | scenario structure across the loop | observed capability, its calendar or any measured multiplier |
| OpenAI Preparedness Framework v2, 2025-04-15 [S96] | AI Self-Improvement High and Critical thresholds | lab-wide assistant impact or generational improvement | 2024 research-engineer and AI-R&D baselines | High is assistant-equivalent acceleration; Critical includes superhuman research agency or sustained generational improvement in about one-fifth the 2024-equivalent time | four analytic gates, especially assistant capability and recursive closure | that a current model has crossed either threshold |
| PaperBench initial release, 2025-04-02 [S97] | AI-research replication | 20 ICML 2024 papers and 8,316 rubric items | author-developed rubric and a top-ML-PhD subset baseline | Claude 3.5 Sonnet (New) with the open-source scaffold averaged 21.0%, below the reported human baseline | hypothesis generation, implementation, execution, debugging, evaluation | research taste, frontier training, successor gain or recurrence |
| GPT-5.6 system card, 2026-07-09 [S98] | debugging, kernels, small pretraining, post-training, ML engineering and long-horizon work | six component evaluations with distinct budgets and harnesses | suite-specific baselines and Preparedness High | OpenAI assessed Sol, Terra and Luna below High as of July 2026 | multiple component stages and safety verification | no acceleration, no risk, general safety, broad automation or closure |
| DeepMind technical AGI-safety analysis, 2025-04-02 [S100] | automated-R&D positive feedback | conceptual mechanism under stated assumptions | more- versus less-than-proportional subsequent R&D output | treats the mechanism as plausible and safety-relevant | research-to-successor feedback | a realized loop, a timeline, safe recurrence or physical closure |
| DeepMind Frontier Safety Framework 3.1, 2026-04-17 [S101] | realized ML-R&D acceleration and broad ML-R&D automation | organization-level progress or team-equivalent work | historical progress rates or comparable all-inclusive team cost | defines distinct capability levels; does not report either as reached | realized-acceleration and broad-automation gates | verified safe-successor deployment or recurring closure |

: Cross-lab AI-R&D evidence and its bounded interpretation. [View data](../outputs/integrated/tables/ai_rnd_benchmark_registry.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rnd_benchmark_registry.csv"}. {#tbl-ai-rnd-evidence}

The comparison is intentionally not a score ranking. Anthropic supplies an
operational self-report and makes the execution-versus-direction gap concrete;
METR supplies independent task-horizon measurements; *AI 2027* supplies a
fast-digital scenario rather than observed evidence; OpenAI publishes
AI-self-improvement thresholds plus component and end-to-end AI-R&D
evaluations; and Google DeepMind separates realized R&D acceleration from
broad R&D automation while locating capability in models integrated with
workflows. The benchmark, harness, compute, tool, scaffold, human and
evaluation boundaries are therefore part of every observation, not optional
metadata.

OpenAI's High threshold is comparable to giving every OpenAI researcher a
strong mid-career research-engineer assistant relative to a 2024 baseline.
Its Critical threshold instead covers a superhuman research-scientist agent
or sustained generational improvement in roughly one-fifth of the
2024-equivalent wall-clock time [S96]. High is an assistant/acceleration
threshold, not loop closure. PaperBench is an AI-research-replication
benchmark—not a recursive-improvement benchmark. Its initial release asks
agents to reproduce 20 ICML 2024 Spotlight or Oral papers from scratch
against 8,316 author-developed rubric items. The best tested configuration,
Claude 3.5 Sonnet (New) with the released open-source scaffold, averaged
21.0% and remained below the reported top-ML-PhD subset baseline [S97].

The July 9, 2026 GPT-5.6 card decomposes OpenAI's current evaluation suite:
41 real internal research-code bugs plus six alignment-auditing tasks;
KernelGen 1P correctness and non-gamed latency improvement; NanoGPT
pretraining-loop improvement on one H100; PostTrainBench Lite over twelve
model-task combinations with one H100, internet and five hours; MLE-Bench
Revised over 72 Kaggle-style problems; and METR Time Horizon 1.1, run by the
external evaluator [S98]. The internal tasks and some rubrics are only partly
auditable. Benchmark saturation, unsolvable items, contamination, invalid
shortcuts, scaffolding dependence, evaluator validity and the gap between
small-scale tasks and frontier training remain load-bearing qualifications.
METR's GPT-5.6 observation appears once in the registry with both source
references; it is not counted again as independent OpenAI evidence.

DeepMind's technical safety analysis supplies conceptual support for the
positive-feedback mechanism while labeling its paradigm, timeline and
continuity premises as assumptions and leaving some superintelligence
questions outside its scope [S100]. Frontier Safety Framework 3.1 then keeps
two different thresholds separate. “ML R&D acceleration level 1” is a
lagging outcome: systems have actually accelerated AI progress substantially
beyond historical rates. “ML R&D automation level 1” is a capability and
economic-substitution threshold: a system can automate any Google
AI-capabilities research team's work at approximately comparable
all-inclusive cost [S101]. DeepMind expects acceleration from systems of
models integrated into workflows, not a model in isolation, and separately
governs external release and high-risk internal deployment. This reinforces
the article's split between internal capability and public observation
without treating internal use as automatically safe.

Across the record, frontier labs increasingly treat AI-enabled R&D as
measurable and safety-relevant, and public evaluations show meaningful
performance on several component tasks. No cited public source demonstrates
a verified, recurring, end-to-end successor-model loop. OpenAI's Critical
threshold helps operationalize that endpoint and DeepMind's feedback account
supports the mechanism; neither establishes embodied-production or
reproductive-capital closure. The normalized evidence boundaries are
available in the [benchmark registry](../outputs/integrated/tables/ai_rnd_benchmark_registry.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rnd_benchmark_registry.csv"}
and [stage/gate crosswalk](../outputs/integrated/tables/ai_rnd_evidence_crosswalk.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rnd_evidence_crosswalk.csv"}.

The Anthropic figures remain `company_statement`: selection, attribution,
counterfactual, and same-family evaluator bias are unresolved, so code share
or lines of code cannot become a capability-growth coefficient. METR's own
limitations are equally load-bearing: its time horizon is serial human labor
replaced at a stated reliability level, differs sharply by domain, is not
a delegation threshold, and does not determine human intervention or
research uplift. The July 2026 survey is arXiv v1; 74% of its papers were
posted in 2026, classification used one annotator, and the authors disclose
recency bias, peripheral-query bleed, and lab-publication censoring [S84].
It maps a moving field rather than certifying closure.

Indexing candidate-improvement attempts by $n$ and public-release events by
$r$, the resource-constrained internal update and public observation are

::: {#eq:digital-capability-update .equation}
$$
\begin{aligned}
\mathbf I^{\mathrm{int}}_{n+1}
&=\mathbf I^{\mathrm{int}}_n
+z^{\mathrm{tech}}_n z^{\mathrm{int}}_n\,\mathbf G_n
 \!\left(\mathbf I^{\mathrm{int}}_n,\mathcal D_n,\mathcal A_n,
 C_{\mathrm{eff},n},\mathcal V_n\right),\\
\mathbf I^{\mathrm{pub}}_{r+1}
&=\mathbf R_r\!\left(
\mathbf I^{\mathrm{int}}_{\tau(r)};
z^{\mathrm{pub}}_r,\mathcal E^{\mathrm{pub}}_r
\right).
\end{aligned}
$$
:::

Here $\mathbf I^{\mathrm{int}}_n$ and $\mathbf I^{\mathrm{pub}}_r$ are vectors
of internally available and publicly observable task-relevant capability.
$z^{\mathrm{tech}}_n$ records whether the candidate is a genuine validated
gain rather than noise, leakage, reward hacking, or regression;
$z^{\mathrm{int}}_n$ records authorization for the claimed bounded internal
role; and $z^{\mathrm{pub}}_r$ records external/public authorization. All
three are binary conceptual indicators, not estimated probabilities.
$\mathbf G_n$ is the observed vector gain and depends on the current data
state $\mathcal D_n$, architecture and algorithm state $\mathcal A_n$,
effective training effort $C_{\mathrm{eff},n}$, and technical-verification
regime $\mathcal V_n$. The release mapping $\mathbf R_r$ exposes the internal
state selected by $\tau(r)$ under the public evidence and exposure conditions
$\mathcal E^{\mathrm{pub}}_r$; it can lag, narrow, or differently optimize the
public capability slice. The equation therefore does not require componentwise
nesting in every product, although the implemented illustrative branches use
nested slices. Components retain their own units or normalized scales; this
paper does not collapse loss, benchmark scores, parameter count, and physical
productivity into one scalar “intelligence.”

Within a stable architecture, dataset, objective, and evaluation regime, a
useful sensitivity model for capability component $m$ is a saturating
frontier,

::: {#eq:digital-saturating-frontier .equation}
$$
I_m(C_{\mathrm{eff}})
= I_{m,0}
+ A_m\!\left[
1-\left(1+\frac{C_{\mathrm{eff}}}{C_{m,0}}\right)^{-\beta_m}
\right].
$$
:::

In Eq. [@eq:digital-saturating-frontier], $I_m$ is held-out performance on
capability component $m$; $C_{\mathrm{eff}}\ge0$ is cumulative effective
training or search effort in equivalent useful FLOP; $I_{m,0}$ is starting
performance; $A_m\ge0$ is the regime-specific attainable improvement;
$C_{m,0}>0$ is a scale constant in the same units as $C_{\mathrm{eff}}$; and
$\beta_m>0$ controls curvature. The imposed shape has
$\partial I_m/\partial C_{\mathrm{eff}}>0$ and
$\partial^2 I_m/\partial C_{\mathrm{eff}}^2<0$: more effective effort helps,
but each additional unit helps less. This is an **ASSUMPTION-class sensitivity
form**, not an empirical law of RSI. It makes diminishing marginal gain a
function of cumulative effort rather than calendar time. The analysis retains three
regimes: a power-law-like smooth decline over the observed range; the
saturating case above; and a piecewise frontier in which a discrete
architecture, algorithm, data, post-training, tool-use, or test-time-compute
innovation changes $(A_m,C_{m,0},\beta_m)$ after paying its own search and
verification cost.

Training compute is not itself effective effort. For a fixed held-out target,
the accounting identity used here is

::: {#eq:effective-training-compute .equation}
$$
C_{\mathrm{eff}}
= C_{\mathrm{train}}\,
\eta_{\mathrm{hw}}\eta_{\mathrm{util}}
\eta_{\mathrm{alg}}\eta_{\mathrm{arch}},
\qquad
C_{\mathrm{train}}\simeq k_{\mathrm{train}}N_{\mathrm{act}}D.
$$
:::

$C_{\mathrm{train}}$ is realized training compute in FLOP;
$N_{\mathrm{act}}$ is the mean number of parameters activated per token; $D$
is the number of training tokens after deduplication and filtering; and
$k_{\mathrm{train}}$ is an operation-count coefficient fixed by the training
procedure. The dimensionless factors $\eta_{\mathrm{hw}}$,
$\eta_{\mathrm{util}}$, $\eta_{\mathrm{alg}}$, and
$\eta_{\mathrm{arch}}$ measure, respectively, hardware efficiency, realized
utilization after memory/interconnect/restart losses, algorithmic efficiency,
and architecture efficiency relative to a named baseline at the same held-out
target. They are comparative measurements, not free multipliers. Peak FLOP/s,
FLOP/J, memory traffic, communication overhead, power, cooling, and wall-clock
duration determine the first two; compute or data required to reach a fixed
score determines the latter two.

Those hours also have mutually exclusive uses. The annual allocation model
partitions physical accelerator time among successor training, inference for
research agents, research experiments, data generation and filtering,
verification and safety, and external productive service:

::: {#eq:ai-rd-compute-allocation .equation}
$$
\begin{aligned}
\sum_{s\in\mathcal S_C} C_s^{\mathrm{phys}}
&=C_{\mathrm{tot}}^{\mathrm{phys}},
\qquad
C_s^{\mathrm{eff}}=\eta_s C_s^{\mathrm{phys}},\\
R_{\mathrm{eff}}
&=\min\!\left\{
\frac{C_{\mathrm{inf}}^{\mathrm{phys}}}{c_R},
U_R
\right\},\\
\nu_{\mathrm{verified}}
&=\min\!\left\{
\rho_R R_{\mathrm{eff}},
\frac{C_{\mathrm{exp}}^{\mathrm{eff}}}{c_{\mathrm{exp}}},
\frac{y_D C_{\mathrm{data}}^{\mathrm{phys}}}{c_D},
\frac{q_V C_{\mathrm{ver}}^{\mathrm{phys}}}{c_V},
\frac{1}{\tau_{\mathrm{serial}}}
\right\}.
\end{aligned}
$$
:::

$\mathcal S_C$ is the six-use partition; $C_{\mathrm{tot}}^{\mathrm{phys}}$
is the conserved physical accelerator-hour budget; $C_s^{\mathrm{phys}}$ and
$C_s^{\mathrm{eff}}$ are physical and effective hours for use $s$; and
$\eta_s$ is its declared efficiency conversion. $R_{\mathrm{eff}}$ is the
effective automated-researcher count, limited by inference hours per instance
$c_R$ and useful research tasks $U_R$. $\rho_R$ is candidate output per
effective researcher. The remaining rates are experiment compute
$C_{\mathrm{exp}}^{\mathrm{eff}}/c_{\mathrm{exp}}$, accepted-data signal
$y_D C_{\mathrm{data}}^{\mathrm{phys}}/c_D$, independent verification
$q_V C_{\mathrm{ver}}^{\mathrm{phys}}/c_V$, and the inverse serial
experiment-cycle floor $1/\tau_{\mathrm{serial}}$. Algorithmic improvement
changes $\eta_s$; it does not enlarge
$C_{\mathrm{tot}}^{\mathrm{phys}}$.

At the central efficiency setting, the 5%-grid raw-capability optimizer
allocates 25%, 35%, 20%, 15%, 0%, and 5% to the six uses. It reports 35 raw
candidate units/year but zero verified progress because it reserves no
verification compute. The verified-progress optimizer allocates 20%, 30%,
15%, 15%, 15%, and 5%, producing 30 verified units/year while foregoing
$1.9 million of the illustrative all-service revenue account. The
physical-growth score assigns all hours to current external productive
service and produces no research progress. Raising the effective-compute
conversion from 0.75 to 1.50 increases the best verified rate from 25 to 35
without changing the one-million-hour physical budget. These are
ASSUMPTION-class allocation comparisons, not organizational prescriptions;
no scenario share is imported from a narrative forecast. Machine-readable:
[AI R&D compute allocation](../outputs/integrated/tables/ai_rd_compute_allocation.csv){.artifact-link data-artifact="outputs/integrated/tables/ai_rd_compute_allocation.csv"}.

Empirical language-model scaling laws show diminishing loss improvements with
model size, data, and compute, while the Chinchilla experiments show that
compute-optimal training requires joint allocation between model size and
training tokens [S58] [S59]. These are evidence about loss in observed model
families, not evidence that a scalar intelligence must keep rising or that RSI
is active. Architecture also changes the resource surface: selective
state-space models trade attention’s sequence-length behavior for different
hardware kernels, while sparsely activated mixture-of-experts models separate
total from active parameters but add routing, load-balancing, communication,
and stability costs [S60] [S61]. “Transformer versus Mamba” and “dense versus
sparse” therefore name sensitivity branches, not universal efficiency
rankings. Observed algorithmic progress at fixed performance can shift the
frontier, but its historical rate cannot be extrapolated unchanged into
autonomous research [S26].

The implemented attribution screen therefore avoids fitting one historical
headline rate. It gives compute, data, model-size, hardware, algorithm, and
architecture elasticities separate low/central/high **ASSUMPTION** bounds and
retains a declared positive-semidefinite correlation matrix among them.
A companion log-additive accounting sensitivity freezes compute, data,
hardware, algorithm, or architecture progress one at a time. Under the
illustrative annual channel rates, the full annual multiplier is 1.821; the
one-channel counterfactuals range from 1.543 when compute is frozen to 1.686
when architecture is frozen. Those numbers are neither a causal
decomposition nor a forecast—they expose how much of the assumed composite
rate was assigned to each channel. The exact bounds, correlations, and
freezes are in [digital elasticity bounds](../outputs/integrated/tables/digital_elasticity_bounds.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_elasticity_bounds.csv"} and
[digital channel ablations](../outputs/integrated/tables/digital_channel_ablations.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_channel_ablations.csv"}.

A chronological release backtest provides a deliberately narrow external
screen. The split was fixed before fitting: GPT-3, Gopher, Chinchilla, and
PaLM releases from 2020–2022 form the training set [S59] [S72]; LLaMA and
Llama 2 releases from 2023 form the validation set [S73] [S74]; and Llama 3.1
70B is the 2024 holdout [S75]. Every observation is a base pretrained dense
model evaluated on five-shot MMLU. The candidate relation is

::: {#eq:chronological-release-backtest .equation}
$$
\begin{aligned}
\operatorname{logit}(p_i)
&=\beta_0+\beta_C\log_{10}\!\left(\frac{6N_iD_i}{C_{\mathrm{ref}}}\right)
+\beta_B\log_{10}(b_i),
\\
p_i&=\frac{M_i-25}{100-25},
\qquad
b_i=\min\!\left\{
\frac{D_i}{20N_i},\frac{20N_i}{D_i}
\right\}.
\end{aligned}
$$
:::

Here $M_i$ is release $i$'s five-shot MMLU accuracy in percentage points;
$p_i$ is its chance-adjusted score; $N_i$ and $D_i$ are dense parameter and
pretraining-token counts; $6N_iD_i$ is a training-FLOP proxy;
$C_{\mathrm{ref}}=10^{23}$ FLOP fixes the log scale; $b_i\in(0,1]$ measures
distance from the declared Chinchilla-style allocation of 20 tokens per
parameter; and $\beta_0,\beta_C,\beta_B$ are fitted only on the four training
observations. The compute-only comparison sets $\beta_B=0$.

The compute-only relation has 6.64 percentage-point mean absolute error on
the two 2023 validation releases and 1.48 points on the single 2024 holdout.
Including the declared data-balance term reduces 2023 validation error to
0.99 points but gives 1.71 points on the holdout. The holdout token input is
the published lower bound of 15 trillion tokens, not an exact training count.
These results are too small, family-confounded, and protocol-sensitive to
calibrate capability growth: the apparent validation benefit does not improve
the one-observation holdout. The coefficients therefore remain a
retrospective screen and do not enter the recursive-loop dynamics. The
release rows, source locators, fitted coefficients, and split errors are in
[digital release backtest table](../outputs/integrated/tables/digital_release_backtest.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest.csv"} and
[digital release backtest summary](../outputs/integrated/tables/digital_release_backtest_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_release_backtest_summary.csv"}.

Calendar speed is a separate quantity. Let $\nu_v(t)$ be verified loops per
elapsed calendar year at time $t$. It is constrained by the slowest required
stage:

::: {#eq:verified-loop-bottleneck .equation}
$$
\nu_v(t)=\min\!\left\{
\nu_{\mathrm{train}},\nu_{\mathrm{data}},\nu_{\mathrm{experiment}},
\nu_{\mathrm{evaluate}},\nu_{\mathrm{safety}},
\nu_{\mathrm{deploy}},\nu_{\mathrm{observe}}
\right\}.
$$
:::

Each $\nu_{\cdot}$ is stage capacity in completed-loop equivalents per year.
The training stage is itself limited by model and active-parameter size,
tokens, context length, memory capacity and bandwidth, accelerator
interconnect, parallelism efficiency, power, cooling, wall-clock training
time, failures, and restart policy. The experiment and observation stages
also impose irreducible physical time. Multiplying throughput by conditional
gain gives a rate without resurrecting constant $G$:

::: {#eq:digital-capability-rate .equation}
$$
\frac{\mathrm d\mathbf I}{\mathrm dt}
=\nu_v(t)\,
\mathbb E\!\left[\mathbf G_n\mid
\mathbf I(t),\mathcal D(t),\mathcal A(t),\mathcal V(t)\right].
$$
:::

In Equation [@eq:digital-capability-rate], $t$ is elapsed calendar time in
years and the conditional expectation averages heterogeneous successes,
failures, and regressions in a declared regime. Higher capability may improve
coding, architecture search, synthetic-data generation, hardware design,
factory scheduling, scientific modeling, and evaluation design, but the
result is bounded by Eq. [@eq:verified-loop-bottleneck] and by the frontier
being approached. Superlinear, linear, logarithmic, and saturating trajectories
remain hypotheses to distinguish with completed-loop telemetry.

The period ledger makes the bottleneck visible rather than reporting only
$\nu_v$. In the declared 0–7 year baseline, observation binds at 2 verified
loops/year while progress moves along the fixed scaling curve. The year-7
frontier event is followed by a safety-limited 3 loops/year during years
7–14; after the year-14 frontier event, experiment throughput binds at 4
loops/year through year 20. These are scenario mechanics, not forecasts.
[digital loop bottlenecks](../outputs/integrated/tables/digital_loop_bottlenecks.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_loop_bottlenecks.csv"} records every stage
rate and distinguishes movement along a curve from a discrete frontier shift.

Verification is not one fungible stage. For verifier class $k$,

::: {#eq:verification-hierarchy .equation}
$$
\begin{aligned}
\nu_{v,k}
&=\min\{\nu_{\mathrm{candidate},k},\nu_{\mathrm{capacity},k}\}
\,y_k(1-f_k)q_k,\\
\nu_{\mathrm{licensed},k}
&=\min\{\nu_{v,k},\nu_{\mathrm{direction}},
\nu_{\mathrm{execution}}\}.
\end{aligned}
$$
:::

$\nu_{v,k}$ is independently supported throughput for class $k$;
$\nu_{\mathrm{candidate},k}$ and $\nu_{\mathrm{capacity},k}$ are candidate
and verifier capacity; $y_k$ is acceptance yield; $f_k$ is false-positive
fraction; and $q_k$ is evaluator independence across model lineage, training
data, tools, authority, and audit access. $\nu_{\mathrm{licensed},k}$ is
licensed loop throughput, additionally bounded by research direction-setting
$\nu_{\mathrm{direction}}$ and fixed-target execution
$\nu_{\mathrm{execution}}$. The six classes are reported separately, from
formal/executable invariants and destructive physical acceptance tests
through independent held-out experiments, causal operational outcomes,
human/AI rubrics, and model self-assessment. They are not added into a
universal “verified-equivalent” total.

The limiting test gives the self-assessing producer zero independence by
definition: 1,000 self-scored iterations do not become independent evidence,
whereas one destructive physical test can license its narrow physical claim.
Stress rows separately apply evaluator drift, reward hacking,
self-confirming selection, evaluator-diversity collapse, and synthetic-data
model collapse. In the self-confirming case, preserving all positive records
but only 10% of negative and 5% of null records raises the apparent positive
share from 0.10 to 0.625 without improving the underlying record. This is the
survivorship-bias failure the industrial-memory pipeline must prevent.
Machine-readable:
[verification hierarchy table](../outputs/integrated/tables/verification_hierarchy.csv){.artifact-link data-artifact="outputs/integrated/tables/verification_hierarchy.csv"}.

Operational experience closes the loop only if it survives deployment and is
converted into a verified change. A durable learning record binds
observations, actions, outcomes, task and hardware state, environment,
model/controller version, human intervention, timestamps, and provenance.
It retains failures, near misses, null results, unsuccessful recoveries, and
negative experiments as well as successes. The versioned pipeline is:
ingestion; integrity and access checks; episode construction; causal
attribution with uncertainty; replay or simulation; conversion into a
procedure, controller, retrieval item, or training example; held-out
evaluation; staged deployment; monitoring; and rollback. Temporary context,
persistent retrieval within one generation, revised recipes or control
policies, offline post-training, and transfer into a successor generation are
five distinct mechanisms. Continuous weight updates are unnecessary, but a
later generation must be able to trace every accepted lesson back to evidence
and every rejected lesson to its gate. Learning yield and latency—not bytes
stored—are the relevant outputs.

The synthetic intergenerational rehearsal makes that condition executable
without pretending that the physical campaign has occurred. Four fault
families—sensor bias, actuator stiction, calibration shift, and
communications partition—each have a training case and a structurally
similar hidden transfer case. Across four controller generations, the hidden
case is never exposed to training; the output records learning latency,
retention, transfer success, recurrence, recovery time, verification compute,
and regression on earlier tasks. A post-update row passes only if transfer
and retention exceed their preregistered gates and prior-task regression
stays below its gate. [intergenerational learning faults](../outputs/integrated/tables/intergenerational_learning_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/intergenerational_learning_faults.csv"} carries the
complete split and result record with
`evidence_status=synthetic_protocol_execution`; it does not replace the
execution-pending terrestrial rehearsal.

Those observed synthetic metrics feed the digital loop rather than remaining
a disconnected dashboard. Median event-to-deployment latency caps observation
and deployment rates; verification compute per fault family caps evaluation
and safety throughput; and retention, hidden-case transfer, and non-recurrence
multiply into the technical-validation fraction for retained learning.
[digital learning feedback table](../outputs/integrated/tables/digital_learning_feedback.csv){.artifact-link data-artifact="outputs/integrated/tables/digital_learning_feedback.csv"}
compares the unadjusted assumption case with that constrained case. In the
declared synthetic campaign, median latency is 183 days, mean retained lesson
strength is 0.804, mean hidden-case transfer is 0.846, mean recurrence is
0.088, and mean verification cost is 1,312.5 compute-hours per family and
generation. Evaluation/safety capacity then limits verified throughput to
1.524 loops/year, the combined technical-validation fraction is 0.620, and year-20
capability is 1.480 rather than the unadjusted 1.765. The
connection demonstrates data flow and prevents instantaneous learning; only
physical rehearsal measurements can replace the synthetic inputs.

Synthetic volume and accepted signal are also separate states. For generation
$g$, the sensitivity records

::: {#eq:accepted-training-signal .equation}
$$
S_g
=V_g^{\mathrm{syn}}(1-d_g)y_g p_g(1-e_g)D_g
+N_g^{\mathrm{phys}}c_g(1-e_g).
$$
:::

$S_g$ is accepted training-signal units; $V_g^{\mathrm{syn}}$ is generated
synthetic records; $d_g$ is deduplication fraction; $y_g$ is filtering
acceptance; $p_g$ is valid provenance; $e_g$ is evaluator error; $D_g$ is
data-diversity retention; $N_g^{\mathrm{phys}}$ is the number of
resource-limited physical episodes; and $c_g$ is their causal-linkage
fraction across state, action, outcome, and hardware configuration.
Physical episodes are capped independently by experiment time, equipment
wear, destructive samples, and verification capacity.

The volume-maximizing branch expands from 1,000 to 2.187 million synthetic
records by generation 7 and raises its apparent-progress index above the
governed branch. Yet evaluator error rises to 0.643, bias to 0.582, diversity
falls to 0.350, and held-out transfer falls to 0.626 versus 6.993 in the
governed branch. More generated data can therefore create stronger apparent
progress and weaker transfer. A third branch applies open publication,
espionage, employee mobility, distillation, and independent replication to
the proprietary-data state; its advantage index falls to 0.003 versus 0.255
under the lower-leakage branch. These are scenario mechanics, not leakage
estimates. Machine-readable:
[data evaluator coevolution table](../outputs/integrated/tables/data_evaluator_coevolution.csv){.artifact-link data-artifact="outputs/integrated/tables/data_evaluator_coevolution.csv"}.

Public releases are lagging indicators: benchmarks, open weights, products,
and launches observe the public frontier, not necessarily the latent internal
frontier. An organization can obtain research, engineering, operational, and
successor-training benefits from a validated change in a bounded internal role
before completing broader assurance for heterogeneous users, uncontrolled
distribution, external misuse, legal exposure, and unfamiliar environments.
Release cadence can therefore understate the feedback-loop speed that matters
to this thesis. Internal use is not gate-free: technical validation must
reject noise, evaluator leakage, reward hacking, and regression, while
risk-based authorization must match consequence, authority, reversibility,
containment, and privileged access. Advice with human execution and rollback
can be authorized earlier than autonomous authority; live infrastructure,
physical actuation, destructive experiments, cyber or biological work,
weight modification, and successor training can require stringent controls
even when wholly internal.

The internal frontier is only partially observable. Relevant indirect
observations include internal task productivity, experiment throughput,
code or research contribution, training cadence, inference use, access tiers,
staged deployment, and later disclosure of prerelease performance. None is a
direct overhang measurement. A long release interval may instead reflect
assurance, product strategy, compute scheduling, integration, regulation, or
weak results; secrecy and capability are different variables. The implemented
zero-lag, slower-publication, and internal-overhang cases are consequently
**ASSUMPTION** sensitivities, with separate experiment, technical-validation,
internal-adoption, and public-release clocks:
[internal/public capability trajectories](../outputs/integrated/tables/internal_public_capability_trajectories.csv){.artifact-link data-artifact="outputs/integrated/tables/internal_public_capability_trajectories.csv"}.
The nested public slices in those three cases are illustrative, not a claim
that every public product is componentwise weaker than every internal system.
*AI 2027* distinguishes in-house deployment from external exposure and task
performance from honest oversight [S80]; that scenario motivates the state
separation but supplies no numerical lag parameter. Part III.4 attaches the
three gates to their distinct hazards.

### Gross capability is not authorized capacity {#gross-capability-is-not-authorized-capacity}

The control state is deliberately not one “intelligence” scalar. It records
task capability $I_{\mathrm{task}}$, coordination capability
$I_{\mathrm{coord}}$, evaluator capability $I_{\mathrm{eval}}$, and
controllability confidence $p_{\mathrm{ctrl}}$ separately. For
high-consequence physical actions, gross production becomes authorized
operating capacity only at the slowest required control channel:

::: {#eq:authorized-capacity-control .equation}
$$
\begin{aligned}
\dot K_{\mathrm{auth}}(t)
&=\frac{1}{a_K}\min\!\left\{
 a_K\dot K_{\mathrm{gross}}^{+}(t),
 V_{\mathrm{rel}}(t),V_{\mathrm{adv}}(t),C_{\mathrm{cmd}}(t),
 E_{\mathrm{env}}(t),L_{\mathrm{treaty}}(t),H_{\mathrm{human}}(t)
\right\},\\
K_{\mathrm{unauth}}(t)
&=\max\!\left\{K_{\mathrm{gross}}(t)-K_{\mathrm{auth}}(t),0\right\}.
\end{aligned}
$$
:::

$K_{\mathrm{gross}}$, $K_{\mathrm{auth}}$, and $K_{\mathrm{unauth}}$ are
gross, authorized, and unauthorized capacity; $\dot
K_{\mathrm{gross}}^{+}$ is the proposed positive capacity-addition rate; and
$a_K$ is the number of high-impact authorization actions required per unit
of added capacity. $V_{\mathrm{rel}}$ and $V_{\mathrm{adv}}$ are reliability
and independent adversarial-verification throughput;
$C_{\mathrm{cmd}}$ is secure-command throughput; $E_{\mathrm{env}}$ and
$L_{\mathrm{treaty}}$ are environmental and treaty limits; and
$H_{\mathrm{human}}$ is included only when human approval is required. The
minimum is a rate constraint, not a claim that these unlike quantities can
be substituted for one another.

Five ASSUMPTION-class stress cases make the distinction executable. In the
balanced case, gross and authorized capacity both reach 2.587 at year 12.
The verification-lag case reaches 97.017 gross but only 1.864 authorized
capacity; proposed actions exceed human comprehension from year zero, so a
nominal human signature would be ceremonial rather than substantive. A
matched monitor pair isolates common mode: independent monitors authorize
all 8.271 units, whereas shared lineage, data, tools, and observations leave
only 6.037 authorized despite the same gross trajectory. A final case is
limited by treaty throughput and authorizes only 1.600 of 6.571 gross units.
These are stress-test implications, not empirical forecasts. Machine-readable:
[authorized capacity control summary](../outputs/integrated/tables/authorized_capacity_control_summary.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_summary.csv"} and
[authorized capacity control trajectory](../outputs/integrated/tables/authorized_capacity_control_trajectory.csv){.artifact-link data-artifact="outputs/integrated/tables/authorized_capacity_control_trajectory.csv"}.

## I.2 Recursive industrial improvement: the physical loop {#i.2-recursive-industrial-improvement-the-physical-loop}

Digital intelligence depends on a physical substrate: chips, data centers,
electricity, cooling, networks, factories, labor, materials, logistics,
maintenance — a dependency inventory, not a sum; any term can bind. The
physical recursive loop begins when AI and robotics improve the production
of those inputs: better intelligence designs and operates better machines;
better machines expand energy and manufacturing; expanded industry produces
more compute; more compute supports better intelligence.

The loop does not require an indefinitely self-improving controller once
embodied production and reproductive capital are closed. A bounded controller
can operate a fixed productive recipe that replaces and expands its own
capital; verified AI-R&D then improves the rate or reachable designs rather
than creating the logical possibility of physical compounding.

Trammell and Korinek provide the closest formal economic lineage for that
split [S82]. In their aggregate framework, production automation can
accelerate growth when capital substitutes sufficiently for labor and can
self-replicate; the result also depends on saving relative to depreciation,
returns to scale, substitution, and fixed natural-resource factors.
Automating R&D accelerates the transformation but need not generate
explosive growth in isolation when research is weakly parallelizable or
retains serial and fixed-input constraints. Their capital stock is aggregate.
The balanced minimum-sector doubling test used here is stricter: every
indispensable sector must replace and expand, so a surplus of structures or
compute cannot compensate for a missing metrology, electronics, power, or
repair capability. The formal result is a conceptual cross-check, not proof
that this off-world engineering graph closes.

Intelligence is therefore one factor among complementary stocks: experiment
capacity, high-quality causal data, inference compute, embodiment, materials,
energy, deployment capacity, verification, legal authority, and human
consent. Its local physical return in regime $r$ is measured here by a finite
response with every named complement held fixed:

::: {#eq:marginal-intelligence-response .equation}
$$
\operatorname{MP}_{I}^{(r)}(T;\Delta I)
=
\frac{
K_r(T;I_{r,0}+\Delta I,\mathbf X_r)
-K_r(T;I_{r,0},\mathbf X_r)
}{\Delta I}.
$$
:::

$\operatorname{MP}_{I}^{(r)}$ is the change in balanced operating-capacity
units at horizon $T$ per capability-index unit; $K_r$ is the regime-$r$
operating-capacity endpoint; $I_{r,0}$ is its baseline capability;
$\Delta I>0$ is the declared perturbation; and $\mathbf X_r$ is the fixed
vector of complementary stocks and gates. The quotient is a local scenario
diagnostic, not a price, welfare measure, or universal production-function
coefficient.

This is also the transferable part of Amodei's “marginal returns to
intelligence” framework [S79]. His “country of geniuses in a datacenter”
assumes millions of copies operating 10–100 times faster; those quantities
remain scenario assumptions. The useful classification is the complement
set: outside-world speed, missing data, intrinsic complexity, human
constraints, and physical law. Intelligence can sometimes design around the
first four over time, but construction, observation, reaction, and
propagation still have elapsed-time costs, and physical law is not an
optimization target. The bottleneck-project sensitivity separates reducible
constraints, observation-time floors, physical floors, and
external-authority constraints accordingly.

Energy hardware is not energy: "with solar, energy equals hardware"
expresses a recursion, not an identity. Installed arrays generate power
that supports production of additional arrays; the system still pays in
materials, machine-hours, maintenance, and conversion losses. Robotic labor
is manufactured productive capacity: when robots participate in producing
factories, energy systems, and additional robots, labor becomes partially
reproducible, and the robot reproduction ratio must exceed one *after* depreciation, failures, and the equipment needed for high-complexity components — stated with the horizon and unit it requires, R_robot,T = discounted lifetime robot-equivalent capacity produced over T ÷ robot-equivalent capacity retired, consumed, or irreversibly committed over T, since a factory is not "consumed" merely because it helped build robots. In the long run the
decisive competitive variable — under the threshold-like, small-α branch of the capability model examined in II.5 — is not model quality but the doubling time of
productive hardware — and Part I.4 examines what that replication must
outrun.

**The intelligence–embodiment compatibility frontier.** The durable question
is two-sided: for task $k$, does the available embodiment expose enough
observable state and controllable action for a sufficiently capable
controller, and has intelligence actually reached the level required for that
particular hardware? RSI being active is not the same event as reaching that
level, and neither event proves that the system can design and manufacture a
better embodiment.

Let the embodiment vector $\mathbf E$ record degrees of freedom, workspace,
reach, payload, force, torque, compliance, dexterity, tool compatibility;
sensor modality, coverage, resolution, accuracy, sample rate, calibration and
occlusion; local servo and planning latency, jitter, bandwidth and compute;
precision, repeatability, stability and vibration; power, thermal margin, duty
cycle, mobility and environmental tolerance; interfaces and fixtures; and
fault detection, redundancy, safe states, maintainability and repairability.
Let $\mathbf R_k$ state task $k$'s requirements in the same dimensions. The
non-substitutable physical gate is

::: {#eq:embodiment-adequacy-gate .equation}
$$
A_k(\mathbf E,\mathbf R_k,\mathcal E)
=\prod_{p\in\mathcal P_k}
\mathbf 1\!\left[E_p(\mathcal E)\ge R_{k,p}\right],
\qquad A_k\in\{0,1\}.
$$
:::

Here $\mathcal E$ is the operating environment; $\mathcal P_k$ is the set of
hard physical, observability, controllability, safety, and process dimensions
for task $k$; and $\mathbf 1[\cdot]$ is one when its condition is true and zero
otherwise. The direction of a dimension is normalized so that higher is
adequate; maximum latency, vibration, or error limits are represented by
their signed margins. Failure of one hard gate cannot be averaged away by
excellent scores elsewhere.

Conditional on physical adequacy, the manuscript uses the following bounded
compatibility surface as an **ASSUMPTION-class** sensitivity form:

::: {#eq:intelligence-embodiment-compatibility .equation}
$$
S_k(I,\mathbf E,\mathbf R_k,\mathcal E)
=A_k\,S_{k,\max}(\mathbf E,\mathcal E)
\left[1-\exp\!\left(
-\left[\frac{I-I_{k,0}(\mathbf E)}{\sigma_k}\right]_+
\right)\right].
$$
:::

$S_k$ is a dimensionless verified task score, not a calibrated probability;
$S_{k,\max}\in[0,1]$ is the hardware-and-environment ceiling; $I$ is a
declared coordination, perception, planning, recovery, and tool-use
capability measure; $I_{k,0}(\mathbf E)$ is the onset level for that
embodiment; $\sigma_k>0$ is an intelligence scale; and
$[x]_+=\max(x,0)$. Increasing intelligence approaches but cannot exceed the
embodiment ceiling. Better sensing, standardized tool APIs, telemetry,
digital twins, fixtures, machine-readable interfaces, or actuators can raise
that ceiling and reduce the controller burden without adding generic
“intelligence.”

For a required verified score $\bar S_k$, define the embodiment-specific
threshold and its first-passage time by

::: {#eq:embodied-task-first-passage .equation}
$$
I_k^\ast(\mathbf E)
=\inf\{I:S_k(I,\mathbf E,\mathbf R_k,\mathcal E)\ge\bar S_k\},
\qquad
T_k^\ast
=\inf\{t:I(t)\ge I_k^\ast(\mathbf E)
\ \land\ V_k(t)=1\}.
$$
:::

$I_k^\ast$ is infinite when the embodiment cannot attain $\bar S_k$;
$T_k^\ast$ is elapsed years from the declared baseline; and $V_k(t)$ is the
independent task-verification gate. “Not reached within the modeled horizon”
is an outcome, not missing data. Higher intelligence means sufficiently high
intelligence for this task–embodiment pair after a potentially long sequence
of training, evaluation, failed loops, and deployments—not instant competence
when RSI begins.

In the limiting hypothesis, sufficiently capable intelligence can learn to
operate unfamiliar hardware *within* a physically adequate, observable, and
controllable envelope. It cannot infer state from absent sensors, supply
unavailable motion or force, defeat excessive latency, or exceed precision,
energy, reliability, or process limits. It may compensate by active
perception, planning, tool use, calibration, recovery, or multi-agent work,
but those consume time, energy, wear, risk, and capacity. Redesigning,
manufacturing, commissioning, and validating a better embodiment is a
separate physical loop; a versatile robot also does not replace a furnace,
vacuum chamber, cleanroom, or metrology stack. Present humanoid programs,
including Optimus, evidence an intended general-purpose form, not closure of
the unscripted diagnosis, construction, repair, recovery, and verification
task set.

The validation outputs test both causal directions independently. For every
declared industrial task,
[embodiment two direction sweep table](../outputs/integrated/tables/embodiment_two_direction_sweep.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_two_direction_sweep.csv"} holds the
hybrid embodiment fixed while sweeping intelligence, then holds intelligence
at 4.0 while scaling embodiment quality. The terrestrial rehearsal fault
matrix separately degrades sensors, actuators, calibration, communications,
tool familiarity, observability, and out-of-distribution tolerance. Hard-gate
failures remain `embodiment_limited` even at the high intelligence setting;
low scores with adequate hardware remain `intelligence_limited`.
[terrestrial rehearsal embodiment faults](../outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv){.artifact-link data-artifact="outputs/integrated/tables/terrestrial_rehearsal_embodiment_faults.csv"} records the failed dimensions
and score for all eight tasks. These are normalized **ASSUMPTION** tests; the
thresholds must be replaced with measured task, bill-of-material, and fault
logs before they support deployment claims.

Benchmark success is only the first rung of an industrial reliability ladder:
single attempt; repeated success; low-context long task; high-context
production task; safety-critical field task; unscripted recovery; and
sustained operation with bounded intervention. Each task row records duration,
consequence, verifier class, trials, reliability, prompting/checking time,
failure recovery and cleanup, rollback, out-of-distribution recovery, and
intervention events. Economic substitution requires both the task's rung and
its consequence-specific reliability threshold.

The limiting cases prevent a benchmark score from becoming a deployment
claim. A 50% success rate passes the single-attempt gate for cheap reversible
search. The configured 99.5% destructive-fabrication, 99.9% launch, 99.95%
critical-power, and 99.99% replication-authorization tasks all fail their
stricter reliability or rung requirements. A separate synthetic
commissioning row passes only because it supplies destructive physical
verification, unscripted recovery, 1,000 sustained operating hours, at most
two interventions per 100 tasks, and sufficient rollback and
out-of-distribution recovery. Rare failure can dominate labor: the launch
row has fewer interventions than production coding but more expected human
recovery/cleanup hours per task. Software task-duration trends are therefore
not extrapolated into mining, chemistry, maintenance, or commissioning.
Machine-readable:
[industrial reliability ladder table](../outputs/integrated/tables/industrial_reliability_ladder.csv){.artifact-link data-artifact="outputs/integrated/tables/industrial_reliability_ladder.csv"}.

This compatibility layer is not costless. The integrated seed and growth
graphs add six explicit hardware classes—sensors, actuators, end effectors,
modular spares, calibration equipment, and local controllers—to each
applicable sector's material bill and annual replacement-service demand.
[embodiment bill-of-materials requirements](../outputs/integrated/tables/embodiment_bom_requirements.csv){.artifact-link data-artifact="outputs/integrated/tables/embodiment_bom_requirements.csv"} exposes every added coefficient and its
producer-sector dependency. These values are bounding assumptions pending a
task-resolved hardware inventory and terrestrial maintenance logs; their
purpose is to prevent adequate embodiment from entering the model as a free
capability.

The loops couple through a second channel: **data as the exhaust of the
physical loop**. Operating physical industry generates data that exists
nowhere else — test telemetry, process parameters, failure archives, fleet traces. It commoditizes less readily than public text, for four reasons: negative
results (the map of what does not work survives only in the archives of
whoever paid for the failures); sim-to-real ground truth (real telemetry is
the verification fuel for AI-proposed physical designs); legal fencing
(export-controlled data cannot lawfully enter open corpora — and equally
cannot feed publicly served models, so the strongest-moat data is
harvestable only in an internal, access-controlled variant); and temporal lead time (longitudinal data imposes a minimum calendar-time barrier to a like-for-like archive: a rival beginning today matches the sampling rate but cannot reproduce the historical intervention-and-outcome sequence retroactively, though capital compresses much of the disadvantage through acquisition, larger current fleets, accelerated and parallel experimentation, simulation, transfer learning, and newer processes that make the old archive less relevant [S34] — a lead-time barrier, not an impossibility). The
data-closure index κ_D is a direction-of-effort indicator, not a computable
ratio: its denominator is not measurable, and value depends on quality,
linkage, and integration, not origin. The honest caveat: proprietary
physical data is lead time, not permanence — any actor operating comparable
fleets and factories generates comparable exhaust, at national scale in
China's case.

The public record supplies two applications of the same supplemental-training
mechanism, which is evidence of an emerging pattern rather than proof of a
repeatable one. In July 2026, days after an in-house engineering model was
reported to have received a supplemental pass over the coding data of an
acquired developer-tools company, Musk said that the SpaceX engineering
corpus — excluding ITAR-controlled material — would enter supplemental
training of its roughly two-trillion-parameter successor [S11–S13]. The
relevant advantage is therefore not raw ownership alone:

::: {#eq:data-advantage-profile .equation}
$$
\mathbf d
=\left(
d_{\mathrm{unique}},d_{\mathrm{causal}},d_{\mathrm{coverage}},
d_{\mathrm{quality}},d_{\mathrm{access}},d_{\mathrm{integration}},
d_{\mathrm{verification}}
\right),
\qquad
\kappa_D=F(\mathbf d).
$$
:::

The primary output of Equation [@eq:data-advantage-profile] is the
seven-component profile $\mathbf d$, not the aggregate $\kappa_D$. Each
component is normalized to $[0,1]$, higher is better, and must be accompanied
by an uncertainty interval and evidence class:

| component | operational measurement |
|---|---|
| uniqueness | one minus the estimated fraction reproducible from lawful, contemporaneously available substitute corpora at matched cost |
| causal linkage | fraction of sampled episodes linking intervention, state, and outcome strongly enough for the declared causal-identification procedure |
| coverage | weighted fraction of the target task, environment, failure-mode, and operating-regime matrix represented above minimum sample support |
| quality | fraction passing declared integrity, calibration, labeling, timestamp, and contamination checks |
| access | fraction legally and technically usable by the named training or retrieval system at decision time |
| integration | fraction transformed into the versioned schema and retrievable within the required training or operational latency |
| verification | fraction whose proposed lesson survives held-out, counterfactual, safety, and regression tests |

: Operational components of the data-advantage vector. [View data](../outputs/integrated/tables/data_advantage_profile.csv){.artifact-link data-artifact="outputs/integrated/tables/data_advantage_profile.csv"}. {#tbl-data-advantage-components}

These fractions are measured on declared samples and weighting schemes, not
assumed from data ownership. Missing observations remain missing rather than
being imputed as average. Because inaccessible, causally unlinked,
unintegrated, or unverifiable records can have zero learning value, a
compensatory weighted sum is unsafe. If a scalar sensitivity is required, the
explicit **ASSUMPTION-class** candidate is

::: {#eq:data-advantage-scalarization .equation}
$$
\begin{aligned}
\kappa_D^{(\mathrm{assump})}
={}&
\mathbf 1[d_{\mathrm{access}}\ge a_{\min}]
\mathbf 1[d_{\mathrm{causal}}\ge c_{\min}]
\mathbf 1[d_{\mathrm{verification}}\ge v_{\min}]\\
&{}\times
\prod_{j\in\mathcal J_D} d_j^{\,w_j},
\\
w_j&\ge0,\quad \sum_{j\in\mathcal J_D}w_j=1.
\end{aligned}
$$
:::

Here $\mathcal J_D$ indexes the seven components; $w_j$ are declared
dimensionless weights; and $a_{\min}$, $c_{\min}$, and $v_{\min}$ are minimum
access, causal-linkage, and verification thresholds. The indicators impose
hard gates and the weighted geometric mean prevents a zero component from
being hidden by another. No empirical calibration for $F$, the weights, or
the gates is claimed; reported results must therefore retain $\mathbf d$ and
sweep alternative weights, gates, and missing-data assumptions.

Generation alone is insufficient. Telemetry creates an advantage only after
the industrial-memory pipeline defined in I.1 preserves provenance, attributes
cause with uncertainty, grants lawful access, integrates the record, and
transfers a lesson into a procedure, controller, retrieval system, current
model, or successor generation that passes held-out verification. Tesla's
first CIO has described building the custom Warp enterprise system in roughly
four months in 2012 after the company rejected off-the-shelf ERP, then
extending it continuously so operations could change without waiting on a
vendor [S15]. SpaceX independently built its own internal manufacturing and
enterprise system, Warp Drive [S16]. The convergence on the same
build-don't-buy pattern is evidence that iteration speed, not a common brand
name, drives the architecture.

Commentary describes the resulting ideal as a **unified build record** for
each produced unit: *as designed* (models and simulations), *as built*
(supplier batches, process settings, torques, and factory tests), and *as
deployed* (fleet telemetry). Integrated cross-functional data and
over-the-air learning are independently documented; the exact tri-phase
schema is only partially confirmed and is treated as indicative [S14–S17].
Its analytical importance is the causal linkage from design intent through
production parameters to field behavior — the quality dimension of κ_D.

For an autonomous seed, this record is more than training data: it is part
of the transported productive system. Process recipes, material models,
calibration procedures, controller firmware, CAD/CAM files, compilers,
simulators, verification suites, dependency mirrors, failure histories, and
intervention records determine whether physical equipment can be operated,
repaired, and adapted after communication or supply is cut. The manuscript
calls this package **industrial memory**. It is not equivalent to "all
industrial knowledge," an incoherent completion standard; it is a
machine-readable operating foundation coupled to the experimental capacity
to discover what the initial package omitted.

Scale proxies require disciplined interpretation. By mid-2026 the vehicle
fleet had accumulated more than ten billion miles under supervised autonomy,
against roughly 220 million fully driverless miles disclosed by another
operator [S17] [S30]. No valid conversion exists between those regimes, so the
figures are not an advantage multiple. More informative disclosures concern
structure: an occupancy network trained on 1.4 billion fleet video frames and
an auto-labeling system replacing roughly five million hours of manual
annotation [S17]. The aerospace analogue is thirteen heavy-lift flight tests
by mid-2026: few observations, each with high information content [S31].
These quantities demonstrate data generation and integration capacity, not
autonomous industrial closure.

## I.3 Why space changes the cost structure {#i.3-why-space-changes-the-cost-structure}

On Earth, useful locations compete with communities, ecosystems,
jurisdictions, and alternative uses. Off Earth, the monetary price of
unused area approaches zero — but infrastructure does not become free; the
composition may change. A matched comparison uses the same lifecycle
categories in each environment $e\in\{\mathrm{Earth},\mathrm{space}\}$:

::: {#eq:matched-lifecycle-cost .equation}
$$
\begin{aligned}
C_e(u,T)
={}&
\sum_{k\in\mathcal K}
\operatorname{PV}_e\!\left(C_{k,e}^{\mathrm{external}}
+C_{k,e}^{\mathrm{internal}}\right)
\\
&-\operatorname{PV}_e(V_{\mathrm{residual},e}),\\
R_C&=\frac{C_{\mathrm{space}}}{C_{\mathrm{Earth}}},
\qquad
\Delta C=C_{\mathrm{space}}-C_{\mathrm{Earth}}.
\end{aligned}
$$
:::

In Equation [@eq:matched-lifecycle-cost], $C_e(u,T)$ is discounted lifecycle
cost in a stated currency year per functional unit $u$ over lifetime $T$;
$\operatorname{PV}_e$ converts dated flows to present value using the
environment-specific discount-rate scenario; $k$ indexes the common category
set $\mathcal K$; “external” is a purchase across the modeled system boundary;
“internal” is the opportunity cost of capacity consumed inside it; and
$V_{\mathrm{residual},e}$ is terminal residual value. The categories are site
or access rights; regulation and permitting; transport and logistics; energy;
feedstock and materials; extraction and processing; manufacturing;
construction and commissioning; labor or human intervention; maintenance,
repair and replacement; coordination and verification;
decommissioning/disposal; externalities; financing; and residual value. A
term is zero only when the scenario and evidence justify zero.

The comparison reports both $R_C$ and $\Delta C$. A positive denominator is
required for $R_C$; a zero or negative Earth cost makes the ratio undefined
and leaves the signed difference as the valid comparison. Monetary cost,
physical mass and energy, intervention time, environmental burden, and
coordination or verification work remain parallel accounts unless a
documented conversion prices them. The declared Part II functional unit is
discounted dollars per frontier-equivalent kilowatt-year of delivered IT load;
its system boundary, utilization, availability, currency convention,
financing, replacement lives, and terminal value are specified in II.2.

The conceptual categories and the implemented Part II boundary reconcile as
follows:

| common lifecycle account | Part II treatment |
|---|---|
| hardware; power, thermal, storage, structure; construction shell | priced as component capex with component-specific lives |
| transport and logistics | launch mass and destination multiplier priced; launch-site, turnaround, and replenishment logistics omitted |
| energy and operations | electricity, PUE, pumping, ground segment, station-keeping, and utilization priced |
| regulation, insurance, disposal, financing, residual value | explicit scenario terms |
| extraction, feedstock, manufacturing, repair and replacement | local-closure and serviceable/disposable scenarios; physical capacity constraints remain in Part I |
| intervention, coordination, verification, externalities | partially represented through operations and utilization; collision externality and detailed intervention/coordination accounts remain omitted |

: Mapping from a common lifecycle account to the implemented Part II boundary. {#tbl-lifecycle-account-boundary}

Part II therefore does not infer an advantage merely because off-Earth land is
cheap. Its contribution outputs must use this category order, show uncertainty
ranges, and expose the terms driving $\Delta C$. The claim that cost “changes
kind” is supported only where contribution shares actually change under
sensitivity analysis.

The land term declines sharply, but useful positions can remain scarce
because of illumination, thermal conditions, communications geometry,
orbital stability, resource proximity, political accessibility, and
transport energy. The first system must still arrive, survive, obtain or
import matter, reject heat, maintain operations, and replace failed
equipment. Space removes neither scarcity nor cost; it changes their
composition.

The standard external objections — station-keeping, collision management,
imported mass, maintenance, coordination — become *internal product
categories* once the complex can manufacture the required systems:
propellant lines, tracking and maneuver capability, local extraction and
recycling, inspection robots and modular spares, compute and communications.
The crucial question is never whether these requirements exist but whether
the complex can reproduce the industries that satisfy them faster than the
system depreciates.

This is the causal boundary of the expansion claim. Moving an
Earth-manufactured factory or data center into orbit changes its
environmental and transport terms but leaves its growth exogenous to the
off-world system. Moving a reproducible production graph off Earth does two
different things: closure makes growth endogenous, while location relaxes
terrestrial biosphere, land, and political rate limits. Either property can
exist without the other. "Free industrial expansion" is shorthand for
their conjunction, never for costless matter, energy, control, or time.

**Gravity is a process variable, not a system prerequisite.** Industrial
operations divide into at least three classes: processes that tolerate or
benefit from microgravity; bulk operations for which a stable downward
acceleration assists excavation, hopper flow, phase separation, drainage,
and conventional machine layout; and processes that need a specified
acceleration, hydrostatic head, or convection regime. Lunar gravity
(approximately $0.165g$) supplies the second class with a persistent
"down," although lower weight also reduces traction and changes granular
flow. It cannot be declared sufficient for every casting, chemical,
lubrication, thermal, or separation process without testing that process.

Where greater acceleration is needed, the relevant intervention is normally
a rotating drum, centrifuge, or production module—not artificial gravity
for the entire industrial ecology. For radius $R$ and angular speed
$\omega$,

::: {#eq:centrifugal-acceleration .equation}
$$
a_c=\omega^2R.
$$
:::

One terrestrial $g$ requires about 30 rpm at a one-meter radius or
9.5 rpm at ten meters. An ideal rotor consumes energy to spin up and stores
$E_{\mathrm{rot}}=\tfrac12 J_{\mathrm{rot}}\omega^2$, where
$E_{\mathrm{rot}}$ is rotational energy in joules and $J_{\mathrm{rot}}$ is
rotor moment of inertia in $\mathrm{kg\,m^2}$; $I$ is reserved for
intelligence capability. Uniform rotation does not itself require continuous
power. The engineering cost lies in structural mass,
containment, bearings or magnetic suspension, balance control, vibration,
rotating power/data interfaces, spin losses, maintenance, and the inability
to share one acceleration geometry across every process. Lunar gravity is
therefore plausibly enough for many bulk operations, while local
centrifugation is the fallback for gravity-sensitive steps. No credible
single dollar estimate exists without a process list, throughput, rotor
radius, and maintenance architecture. The ten-sector model has
none of these variables; the integrated layer adds declared per-process
gravity requirements, centrifuge radii, and structural-mass and
parasitic-power penalties (D.1) — stylized equipment overheads, not
simulations of the underlying processes.

The complex need not be one self-contained factory: a distributed network
of specialized nodes — lunar mines, orbital refineries, propellant depots,
solar arrays, shipyards, robot factories, compute centers — whose combined
input-output graph is closed. A caution on aggregation applies to every use
of the word "space" in this document: LEO, high orbit, cislunar space, the
lunar poles, Mars, and asteroids differ in radiation, thermal cycling,
illumination, dust, gravity, resources, transport energy, and
serviceability. Feasibility claims cannot be aggregated across them; the
model of Part I.7 therefore uses three explicit reference architectures
(LEO / lunar surface / Mars) rather than "space."
