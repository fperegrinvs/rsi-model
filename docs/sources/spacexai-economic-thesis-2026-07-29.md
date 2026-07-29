# SpaceXAI economic thesis — dated primary-source snapshot

- Accessed: 2026-07-29
- Manuscript use: Part II economic steel-man and falsifiable forecast check
- Source class: `company_statement` for SpaceX filings, specifications, and
  targets; `personal_statement` for Elon Musk's dated prediction
- Model role: comparison target only; company statements are not Monte Carlo
  priors or evidence that a target has been achieved

## 1. Cost-per-token framework and missing comparison

Space Exploration Technologies Corp., response to the U.S. Securities and
Exchange Commission, May 7, 2026, comment 7, pp. 5–6:

https://www.sec.gov/Archives/edgar/data/1181412/000162827926000584/filename1.htm

The response defines cost per token as a function of three primary inputs:
the model, compute hardware, and energy. It says SpaceX expects advantages in
hardware and energy through proprietary-chip integration and orbital solar,
and identifies compute depreciation as the current largest component. It
also records several important negative facts:

- SpaceX does not disclose a specific cost-per-token figure.
- It says competitors generally do not publish directly comparable figures.
- It removed the earlier superlative that SpaceX would achieve the lowest
  cost per token.
- Management did not then use cost per token to evaluate performance,
  allocate resources, or set operating targets.
- The metric and the orbital program were still developing.

The same response explains at pp. 24–25 that capitalized internal satellite
launch cost includes incremental launch expenditures and allocated flight
vehicle depreciation. A launch-cost comparison must therefore not equate
propellant or marginal cash expense with full lifecycle launch cost.

## 2. Prospectus and roadshow thesis

Space Exploration Technologies Corp., Form S-1 filed May 20, 2026:

https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm

Space Exploration Technologies Corp., SEC-filed Rule 433 roadshow materials,
June 4, 2026:

https://www.sec.gov/Archives/edgar/data/1181412/000162828026040610/spacexfwp.htm

The filings present the following coupled argument:

1. near-continuous orbital solar can reduce the energy term and avoid some
   terrestrial grid, land, cooling, and interconnection constraints;
2. reusable launch, scaled satellite manufacturing, and Starlink links could
   reduce deployment and distribution costs;
3. faster access to power could activate newer chips earlier, increasing
   useful output before a terrestrial facility is commissioned;
4. proprietary chips and prospective vertical integration are intended to
   reduce hardware cost and depreciation; and
5. rising launch/manufacturing cadence and a long-run 100 kW/t assumption are
   intended to support as much as 100 GW/year of orbital-compute deployment.

The roadshow describes possible initial orbital-compute deployment as early
as 2028 and rapid payload iteration, but its stated goals are not projections
or assurances. The prospectus identifies approvals, spectrum, launch scale,
reliability, terrestrial competition, and other execution risks.

## 3. AI1 disclosed design boundary

Space Exploration Technologies Corp., Starmind AI1:

https://www.spacex.com/spacexai/starmind

The page reports a 150 kW peak / 120 kW average compute payload, 150 kW solar
array, 70 kW/t vehicle efficiency, 110 m² radiator, laser connectivity, and
planned mass production beginning as soon as late 2027. It does not disclose
satellite manufacturing cost, achieved life or availability, accelerator
cost and qualification multiplier, delivered network goodput, replacement
cost, a full commissioning schedule, or a comparable accepted-token metric.
The detailed numeric extraction remains in
`docs/sources/starmind-ai1-2026-07-27.md`.

## 4. Dated personal prediction

World Economic Forum, “Conversation with Elon Musk,” January 22, 2026,
16:30–17:00 CET:

https://www.weforum.org/meetings/world-economic-forum-annual-meeting-2026/sessions/conversation-with-elon-musk/

Official transcript:

https://www.weforum.org/podcasts/meet-the-leader/episodes/conversation-with-elon-musk-davos-2026/

Musk said that space would be the lowest-cost place to put AI “within two
years, maybe three, three at the latest.” The model treats this as a dated,
falsifiable comparison window:

- earliest boundary: 2028-01-22;
- latest boundary: 2029-01-22.

“Place to put AI” does not specify whether the comparator is marginal energy,
installed compute, inference service, accepted output, or full lifecycle
cost. The manuscript therefore reports the ambiguity rather than selecting a
favorable interpretation after the fact. The statement establishes the
forecast window; it is not engineering evidence and supplies no model input.

## 5. Fixed comparison boundary used by the model

The executable translation is inference-only. Every computable scenario uses
the same reference model, precision, batch, input/output length, acceptance
test, currency year, financing boundary, and evaluation date. It reports:

- lifecycle dollars per frontier-equivalent kW-year as the engineering
  denominator;
- dollars per million accepted output tokens, where accepted output is raw
  output multiplied by a fixed held-out quality pass fraction and the
  scenario's latency/network-goodput fraction; and
- discounted accepted output through the two forecast boundaries under an
  explicit construction, launch, commissioning, and ramp schedule.

Training tokens are excluded. Company-only rows remain `not_disclosed` or
`not_computable` wherever required quantities are absent. The separately
named hybrid fills every gap with an explicitly labeled independent input or
`ASSUMPTION`; it is not represented as a SpaceX or Musk cost estimate.
