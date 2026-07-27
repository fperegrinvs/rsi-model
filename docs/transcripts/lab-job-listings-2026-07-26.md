# Source note — "1,171 job listings" tweet (OpenAI + Anthropic hiring corpus)

**"i went through all 1,171 current job listings from OpenAI and Anthropic. this is the closest thing we have to a public AGI roadmap."**

- Source: https://x.com/imjustnewatai/status/2081221459226034524 (@imjustnewatai;
  posted 2026-07-26T03:33:57Z per snowflake ID; retrieved 2026-07-27 — text
  confirmed via page title, full thread login-walled)
- Provenance class: reporting (viral aggregation tweet) over **company_statement**
  primary sources (the job listings themselves). Every claim below was
  re-verified 2026-07-27 against the live boards: Anthropic via the official
  Greenhouse board API (`boards-api.greenhouse.io/v1/boards/anthropic/jobs`,
  full text of all 418 open listings — phrase searches are exhaustive for the
  current board); OpenAI via openai.com/careers / Ashby (see verdicts).
- Why it's here: bears on Part III's external cross-checks (the software-RSI /
  fast-takeoff prior, [S35]) and on the measurement asymmetry behind E10 and
  discriminating indicator 2 — see assessment at the end. Job listings are
  evidence of **intent, not feasibility** (epistemic rule 3); the tweet itself
  concedes this ("job listings aren't proof these capabilities already exist").

---

## Tweet text (verbatim, as supplied)

> i went through all 1,171 current job listings from OpenAI and Anthropic.
> this is the closest thing we have to a public AGI roadmap.
>
> Anthropic is hiring people to: measure recursive self-improvement; study
> "self-improving, highly autonomous AI"; build an "AI scientist" and
> "scientific AGI"; train Claude to design silicon; create simulated
> "universes" for long-horizon agents; develop "superhuman epistemics" and
> superhuman science assistants.
>
> OpenAI is hiring people to: build persistent, proactive agents that operate
> computers and collaborate with other agents; turn ChatGPT into an "infinitely
> capable and personalized superassistant"; give consumer devices long-term
> memory and evolving user models; improve models through synthetic data,
> simulators and self-play; let agents operate Stargate infrastructure through
> closed-loop automation; build robots with "AGI-level intelligence"; defend
> OpenAI from future internal AI agents that could compromise it.
>
> put everything together: AI designs better chips → trains inside simulated
> worlds → operates computers → performs scientific research → manages the
> infrastructure training its successors → helps improve AI research itself.
> and both companies are hiring people to measure when that loop starts
> accelerating. job listings aren't proof these capabilities already exist.
> but they reveal exactly what future the labs are preparing for. we keep
> waiting for an AGI announcement. they're building the self-improvement loop
> piece by piece.

## Verification — Anthropic claims (all 418 open listings full-text searched, 2026-07-27)

| Claim | Verdict | Listing (open 2026-07-27 unless noted) |
|---|---|---|
| "measure recursive self-improvement" | CLOSE PARAPHRASE, weakest item | Anthropic Fellows Program (Institute, Economics & Policy), greenhouse 5183053008 + umbrella 5023394008. One example project bullet: "Identifying which metrics relating to AI R&D could service [sic] as early warning signals for recursive self-improvement." A fellows-program bullet (application window closed 2026-07-26), not a dedicated role. Only current listings containing the phrase. |
| study "self-improving, highly autonomous AI" | VERBATIM — but a **safety/red-team** context the tweet omits | Research Engineer/Scientist, Frontier Red Team (Cyber), greenhouse 5076477008: "In 2026, we're focused on researching and ensuring safety with self-improving, highly autonomous AI systems, especially ones related to cyberphysical capabilities." Same listing: "We think 2026 will be the year where models reach expert-level, even superhuman, in several cybersecurity domains." |
| build an "AI scientist" / "scientific AGI" | VERBATIM (both phrases) | Discovery team: Research Engineer 4669581008, Staff RE 4593216008, Research Ops 5188237008. "Our team is organized around the north star goal of building an AI scientist"; "identifying and addressing key infra blockers on the path to scientific AGI"; "evaluation frameworks for measuring progress towards scientific AGI." |
| train Claude to design silicon | VERBATIM | Research Engineer, Chip Design RL (Code RL team), greenhouse 5231612008: "you'll advance our models' ability to design silicon"; "Hardware design is difficult and unforgiving — exactly the sort of domain we want Claude to excel at." Distinct from the contemporaneous Samsung custom-chip press reports; the claim matches the listing itself. |
| simulated "universes" for long-horizon agents | VERBATIM team name; "simulated" is the tweet's gloss | Research Engineer, Universes, greenhouse 5061517008: "The Universes team within Research is responsible for training AI models to perform complex, difficult, long-horizon agentic tasks in ultra-realistic settings." Listing says "ultra-realistic settings"/"training environments," not "simulated." |
| "superhuman epistemics" + superhuman science assistants | VERBATIM phrase (open listing); assistant half is CLOSE PARAPHRASE | Research Engineer, Knowledge Foundations, greenhouse 5197337008: "We own the science behind superhuman epistemics." Fuller definition ("parse evidence at enormous scale and draw rigorous conclusions") was in Search & Knowledge Post-Training — since CLOSED. Research Scientist, Life Sciences, greenhouse 5239733008: "making Claude a superhuman life sciences research assistant." |

Anthropic summary: all six claims trace to real listings, five currently open;
none traces solely to a blog post. The two inflations: RSI-measurement is one
fellowship bullet, and the "self-improving, highly autonomous AI" quote is a
red-team *safety* role, not a build role.

## Verification — OpenAI claims (all 752 board postings full-text searched via Ashby API, 2026-07-27)

| Claim | Verdict | Listing (open 2026-07-27 unless noted) |
|---|---|---|
| persistent, proactive agents that operate computers and collaborate with other agents | CLOSE PARAPHRASE (near-verbatim) | Agent Post-Training Research, ashby 4acc3515: "persistent, proactive intelligence that can operate computers, collaborate with people and other agents, and expand what people and organizations can imagine, attempt, and achieve." Same boilerplate in 10 current listings (incl. Computer Use Research, Codex, Frontier Evals & Environments). |
| "infinitely capable and personalized superassistant" | VERBATIM | Research Engineer/Scientist – Personal AGI, North Stars (Post-training), ashby 171ebca6: "We aim to evolve ChatGPT from a chatbot to an infinitely capable and personalized superassistant supporting human flourishing." Only 1 of 752 listings has the word. Origin correction: this is live listing language, NOT the leaked antitrust-trial "ChatGPT: H1 2025 Strategy" doc (that doc says "super-assistant," hyphenated, without "infinitely capable"). |
| consumer devices with long-term memory and evolving user models | CLOSE PARAPHRASE ("evolving" is the tweet's gloss) | Research Scientist – Multimodal Agent, Consumer Devices, ashby 09253a0e (posted 2026-07-21): "This includes long-term memory, user modeling, and personalization systems"; "AI systems that know you over time, act at the right moment." 16 current "Consumer Devices" listings (io-derived hardware org). |
| synthetic data, simulators and self-play | CLOSE PARAPHRASE (all three terms verbatim in one team blurb) | Researcher, Synthetic RL, ashby 60d3700b: "reinforcement learning methods that leverage synthetic data, environments, and feedback… approaches such as self-play, simulators, and other synthetic evaluations." Only current listing containing "self-play." |
| agents operating Stargate infrastructure through closed-loop automation | CLOSE PARAPHRASE — **STALE**: off the board as of 2026-07-27 | IC Agentic Engineering Manager – Stargate (posted ~2026-03-31; recovered via LinkedIn/JSON-LD mirrors): "lead the development and application of agent-based systems for infrastructure delivery and operations within Stargate"; "enable closed-loop automation." Absent from the current Ashby feed — the tweet's present-tense "is hiring" is stale for this one item. |
| robots with "AGI-level intelligence" | VERBATIM (nuance: "pushing **towards** AGI-level intelligence") | Robotics-org boilerplate in **17** current listings (e.g. Robotics Software Engineer, ashby fabfc6c5): "unlocking general-purpose robotics and pushing towards AGI-level intelligence in dynamic, real-world settings." |
| defend OpenAI from future internal AI agents | CLOSE PARAPHRASE (near-verbatim inversion of a responsibility bullet) | Security Researcher, Agentic AI Threats (Preparedness, Safety Systems), ashby e0eef869 (posted 2026-05-18): "help OpenAI prepare for security threats from advanced AI agent insiders"; bullet: "Identify paths by which capable future internal AI agents could compromise OpenAI." Companion open role: Security Preparedness Lead, Coding Agents (defending the agents; the Researcher role defends against them). |

OpenAI summary: six of seven claims trace to live listings (two with the quoted
phrases word-for-word); the Stargate closed-loop item existed as described but
has dropped off OpenAI's own board. The tweet's closer ("both companies are
hiring people to measure when that loop starts accelerating") is also
supported on both sides: the Anthropic fellows RSI-early-warning bullet, and
OpenAI Preparedness roles (the May 2026 listing seeking "strong technical
executors to support preparations for recursive self-improvement," per
Business Insider, plus the open Agentic AI Threats role above).

## Count check

- Anthropic: **exactly 418** open postings (Greenhouse board API `meta.total`,
  2026-07-27).
- OpenAI: **752** listed postings (Ashby posting API, 2026-07-27; 707 unique
  titles — same role in multiple cities counts multiply).
- Combined: **1,170** vs the tweet's 1,171 (posted ~36h earlier) — consistent
  to within a day's board churn. The author evidently did enumerate the actual
  boards.
- Independent snapshot: Pierguido Iezzi (Zenita Group) via Help Net Security,
  2026-07-08 — ~670 OpenAI + ~400 Anthropic ≈ 1,080 open roles.
  https://www.helpnetsecurity.com/2026/07/08/openai-anthropic-agentic-ai-security-risk/
  Same corpus, different extraction: Iezzi's headline reading is OpenAI →
  sovereign compute (Stargate), defense/public-sector, agentic dev tools;
  Anthropic → trust infrastructure, CBRN/behavioral risk. The "AGI roadmap"
  narrative is the tweet author's frame, not the only one the corpus supports —
  a caution on analyst-supplied framing over identical evidence.

## Related primary sources (context, not listings)

- Anthropic Institute, "When AI builds itself" (May–June 2026),
  https://www.anthropic.com/institute/recursive-self-improvement — first-party
  RSI *measurement*: ">80% of the code we merge into Anthropic's codebase was
  authored by Claude"; engineers ship "8x as much code per quarter" vs 2021–25;
  "We are not there yet, and recursive self-improvement is not inevitable. But
  it could come sooner than most institutions are prepared for." (Axios
  coverage 2026-06-04.)
- OpenAI Preparedness-team listing (May 2026, via Business Insider): seeking
  "strong technical executors to support preparations for recursive
  self-improvement" ($295–445k) — i.e., the "measure/prepare for RSI" hiring
  exists at **both** labs, and at OpenAI it is closer to a dedicated role than
  the Anthropic fellowship bullet the tweet used.

## Assessment under this project's framework

1. **Class discipline.** Everything here is company_statement (intent), same
   class as E2/E4/E14. Hiring is costlier than rhetoric (salary budgets are
   real allocations) but far cheaper than capex; treat as declared direction
   with a real budget behind it, never as capability evidence.
2. **Bears on the [S35] prior, not the H1/H2 evidence table.** The actors are
   OpenAI/Anthropic, not the space-industrial cluster of E1–E15. What the
   corpus shows is that both labs allocate real budget to preparing for and
   measuring *software* RSI — corroborating that the fast-takeoff scenario has
   institutional weight behind it. Per the Part III cross-check, that operates
   on the prior: if software RSI arrives first, the rationale for physical
   recursive closure (H1/H2) weakens regardless of item-level evidence.
3. **The measurement asymmetry is the diagnostic.** The software loop has a
   *published measurement program* (Claude-authored code share, R&D
   acceleration metrics, RSI early-warning-signal research; both labs hiring
   for it). The industrial loop has none: no κ-vector metrics, no seed BOM, no
   closure program (E10; discriminating indicator 2). Labs measure the loops
   they are actually trying to close. By that revealed-preference logic, the
   absence of industrial-closure measurement anywhere in either 2026 hiring
   corpus is a small additional update **against H2** — and it sharpens what
   indicator 2 would look like if it ever appeared (the industrial analog of
   "When AI builds itself").
4. **The loop's industrial scope stops at design.** Assembled, the tweet's
   loop (chips → simulated training worlds → computer operation → science →
   infrastructure → AI research) is a *cognitive/operational* loop that
   touches hardware only at **design** (Chip Design RL; the Samsung custom-
   chip reports) and **operation** (Stargate automation, robotics). Neither
   corpus contains fabrication, packaging/test, materials, or
   production-equipment reproduction — the substrate stays imported
   (TSMC/Samsung/ASML as the vitamin). That is precisely Part I's electronics
   minimum cut restated from the demand side: even a maximal software-RSI
   program, on the labs' own declared scope, leaves the fabrication import
   line intact. Software RSI rides on the existing industrial base; recursive
   industrial closure is about reproducing it. The two theses are
   complements, not substitutes — and only one of them currently has a
   hiring corpus.
5. **The tweet's own epistemics are sound** ("listings aren't proof these
   capabilities exist… they reveal what future the labs are preparing for") —
   it is the quote selection that editorializes: the two strongest-sounding
   Anthropic items are, respectively, a fellowship bullet and a *safety/red-
   team* role; the OpenAI robotics line is "pushing **towards** AGI-level
   intelligence"; and the Stargate item had already left the board. None of
   these reverse the picture; all of them shave its edge.
