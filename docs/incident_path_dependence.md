# Incident Path-Dependence: Analysis and Research Brief

> Flagged 2026-04-05, session 14. Context for a follow-up research session.

## The Finding

5-seed heuristic runs (seeds 7/12/42/88/103, 40 rounds, post-OS-cleanup) show that market outcomes are **highly sensitive to which provider receives a major/critical incident and when**. A single critical incident can swing 30+ percentage points of market share.

### Aggregate Results (5 seeds, 40 rounds each)

| Seed | Winner (share) | OpenCore | Orion | Apex | Key incident(s) |
|------|---------------|----------|-------|------|-----------------|
| 7 | OpenCore (45%) | 45% | 15% | 21% | Orion: 4+ incidents (autonomous system failure, hospital suspensions, inconsistent outputs) |
| 12 | Orion (38%) | 25% | 38% | 21% | Mirage: critical medical error. Spark: critical infrastructure failure |
| 42 | OpenCore (31%) | 31% | 49% | 6% | Very quiet seed -- only Apex data leak |
| 88 | Mirage (55%) | 14% | 7% | 13% | **Orion: critical security failure (10M user conversations exposed)** -- Orion collapses from 43% to 7% |
| 103 | Apex (53%) | 24% | 11% | 53% | Genesis: state-sponsored misinfo (critical). Apex escapes all incidents |

### Key Observations

1. **Four different providers win across 5 seeds.** The simulation does not have a predetermined winner.
2. **The winner is essentially whichever high-R&D provider avoids a major incident.** Providers that maintain high R&D allocation grow fastest, but a single critical incident can erase that advantage.
3. **Seed 88 is the clearest case:** Orion (the market leader at 43%) suffers a critical data breach and collapses to 7%. Mirage, which normally languishes at 5-11%, wins at 55% purely by staying clean while maintaining high R&D (69%).
4. **Seed 42 (fewest incidents) produces the most "strategic" outcome** -- outcomes are driven by investment dynamics rather than incident luck.
5. **Portfolio collapse is universal for large incumbents** -- Orion and Apex drop to ~10% R&D in every seed as they shift to safety/product. Providers that maintain high R&D (OpenCore, Mirage in seed 88) benefit from compounding capability growth.

### The Question

Is this level of incident-driven path dependence:
- **(a) A valid emergent finding** -- real markets exhibit similar dynamics where a single safety failure reshapes competitive standing for years, or
- **(b) A calibration artifact** -- incident severity and market share impact are tuned too high relative to other forces in the simulation?

If (a), this is a reportable result. If (b), we need to dampen incident effects or increase the strength of countervailing forces (brand loyalty, switching costs, recovery dynamics).

## Real-World Anchors (Starting Points)

### Cruise (self-driving, 2023)
The most directly analogous case. Cruise (GM's autonomous vehicle subsidiary) was operating robotaxis in San Francisco when a pedestrian was dragged by one of its vehicles in October 2023. The aftermath:
- California DMV revoked Cruise's permit to operate
- GM paused all Cruise operations nationwide
- Cruise laid off ~25% of staff (900 employees)
- CEO Kyle Vogt resigned
- GM wrote down $583M and later pivoted Cruise away from robotaxis entirely
- Competitors (Waymo) captured the market Cruise vacated

**A single critical incident effectively ended a multi-billion dollar competitive position.**

### Other potential cases to investigate
- **Boeing 737 MAX** (aviation, 2018-2019): Two crashes -> global grounding -> $20B+ losses -> market share shift to Airbus
- **Samsung Galaxy Note 7** (consumer electronics, 2016): Battery fires -> global recall -> market share shift to competitors
- **Theranos** (health tech, 2015-2018): Fraudulent test results -> complete company collapse -> regulatory tightening for the sector
- **Clinical trial failures** (pharma): Single adverse event in trials can terminate a drug program and shift investment to competitors
- **Nuclear power** (energy): Three Mile Island (1979), Chernobyl (1986), Fukushima (2011) each reshaped the entire sector's trajectory for decades

### What Would Make This Empirically Defensible

1. **Magnitude calibration:** In the simulation, a critical incident causes ~30pp market share loss over several rounds. Do real-world cases show similar magnitudes? (Cruise: arguably went from viable competitor to zero. Boeing: lost ~10-15pp narrowbody market share to Airbus over 3 years.)
2. **Recovery dynamics:** The simulation currently has limited recovery mechanics. Do real firms recover from critical incidents, and on what timescale? (Boeing is recovering after 5+ years. Cruise has not.)
3. **Sector-level effects:** Do incidents in one firm affect the whole sector? (737 MAX affected public trust in aviation AI generally. Cruise incident slowed robotaxi permitting industry-wide.)
4. **Frequency:** How often do market-reshaping incidents actually occur in high-stakes AI-adjacent sectors?

## Empirical Research Findings (2026-04-05)

Cross-sector survey of real-world safety incidents and their market share impacts, organized by sector.

### Master Calibration Table

| Case | Sector | Market Share Swing | Timeframe | Recovery | Permanent? |
|------|--------|--------------------|-----------|----------|------------|
| Cruise robotaxi (2023) | AVs | ~50pp (to 0%) | 14 months | None | Yes -- GM exited market entirely |
| Boeing 737 MAX (2019) | Aviation | 39pp delivery share (48% to 9%) | 2 years | Partial to ~41% by 2022, then door plug setback | Semi-permanent (~13-18pp sustained loss) |
| Avandia/rosiglitazone (2007) | Pharma | 34pp within TZD class (42.6% to 8.6%) | 12 months | None -- revenue fell 99.6% by 2012 | Yes |
| Vioxx/rofecoxib (2004) | Pharma | Class-wide: COX-2 prescriptions -56% in 4 months | Immediate | Celebrex captured 58% of switchers short-term, but class contagion hit it too | Partial -- class permanently diminished |
| Samsung Galaxy Note 7 (2016) | Consumer tech | 4-5pp overall; ~18pp in premium segment | 1-2 quarters | Full recovery in ~6 months (Galaxy S8) | No |
| Toyota recalls (2009-10) | Automotive | 4-5pp (18.4% to ~13.5%) | 12-18 months | Full recovery | No |
| Uber ATG fatality (2018) | AVs | Complete program exit ($7.25B to ~$4B sale) | 33 months | None | Yes -- sold to Aurora |
| Arthur Andersen (2002) | Audit | ~20pp redistributed to Big Four | Months | None | Yes -- permanent market exit |
| Takata airbags (2010s) | Automotive parts | 20% airbag market to bankruptcy | Years | None | Yes -- acquired by Joyson |
| VW Dieselgate on *non-VW* German brands (2015) | Automotive | 34.6% annual sales reduction for BMW/Mercedes in US | Multi-year | Partial | Collective reputation effect |
| Character.AI teen suicides (2024-25) | AI | ~8pp MAU decline (28M to 20M), confounded | Months | Rebounded to ~45M MAU by Sep 2025 | No (but niche provider) |
| QuitGPT / Pentagon boycott (Feb 2026) | AI | 0.17% of WAU (1.5M/900M); Claude briefly #1 app | Days-weeks | Unknown (too recent) | Likely no |
| ChatGPT 34-hour outage (Jun 2025) | AI | ~0pp (400M users affected, no detectable growth impact) | Hours | Immediate | No |
| Google Gemini image controversy (2024) | AI | ~0pp (Gemini grew to ~18-21% chatbot share) | Weeks | N/A | No measurable impact |
| ChatGPT hallucination incidents (2023-) | AI | ~0pp (ChatGPT grew 8x during controversy period) | Ongoing | N/A | No measurable impact |

### Sector 1: Self-Driving / Autonomous Vehicles

**Cruise (2023)** is the clearest case of total market destruction from a single incident.

- **Pre-incident:** ~950 vehicles, $30B valuation, full 24/7 commercial permit in SF, 66K monthly passengers
- **Incident:** Oct 2, 2023 -- robotaxi dragged pedestrian ~20 feet. Aggravated by Cruise filing a false report with NHTSA (omitting the dragging).
- **Cascade:** CA DMV revoked permit (Oct 24) -> nationwide suspension (Oct 27) -> CEO resigned (Nov 19) -> 24% layoff (Dec 14) -> internal share price halved to $11.80 -> GM exited robotaxi market entirely (Dec 10, 2024)
- **Competitor capture:** Waymo grew from ~10K weekly rides (May 2023) to 500K+ (Mar 2026) -- 50x growth. Waymo captured 27% of SF rideshare dollars by mid-2025, overtaking Lyft.
- **Key amplifier:** The cover-up (false NHTSA report) transformed a manageable safety incident into an existential regulatory crisis. DOJ found Cruise "filed false documents to impede, obstruct, or influence the investigation."

**Uber ATG (2018)** followed a similar pattern. First AV pedestrian fatality (Tempe, AZ). Uber suspended all testing, eventually sold ATG to Aurora for ~$4B (Dec 2020), having spent $2.5B+ on the program.

**Pattern:** In the AV sector, a single incident + regulatory response = permanent market exit. No recovery in either case.

### Sector 2: Aviation (Boeing 737 MAX)

The most data-rich case with the longest timeline.

- **Pre-crisis (2018):** Boeing ~48% narrowbody delivery share
- **Two crashes:** Lion Air (Oct 2018, 189 dead), Ethiopian Airlines (Mar 2019, 157 dead). 20-month global grounding.
- **Nadir (2020):** Boeing ~9% delivery share -- a **39pp drop**
- **Partial recovery (2022-23):** Back to ~41%, but...
- **Second incident (Jan 2024):** Alaska Airlines door plug blowout. Not fatal, but knocked Boeing back to ~33% delivery share. FAA capped production, new quality audits.
- **As of 2025:** Still 13-18pp below pre-crisis levels. Stock not recovered (while S&P 500 doubled). $21B+ in direct charges. Debt ballooned from $12B to $52-58B.

**Key calibration insight:** Recovery is nonlinear and fragile. A second, less severe incident during recovery can reset the clock. The duopoly structure creates both a floor (airlines need a second supplier) and a ceiling (fleet commonality lock-in). **Estimated permanent share loss: 8-15pp.**

### Sector 3: Pharma / Clinical Trials

**Avandia (GSK, 2007)** provides the cleanest documented 30+pp swing:

- **Pre-crisis:** 42.6% of thiazolidinedione (TZD) class fills (Q3 2006). $2.5B annual revenue.
- **Crisis:** Nissen & Wolski NEJM meta-analysis linking rosiglitazone to increased MI risk (May 2007).
- **1 year later:** 8.6% TZD class share -- a **34pp drop**. Actos (Takeda) captured essentially the entire remaining market.
- **By 2012:** Revenue collapsed from $2.5B to $9.5M (99.6% decline). Fewer than 1,000 prescriptions/year.
- **Competitor capture:** Actos soared from $2.4B (2008) to $4.5B (2010-11).

**Vioxx (Merck, 2004)** shows a different pattern -- class-wide contagion:

- Merck stock fell 26.8% in a single day ($25B market cap erased). Total litigation: ~$6.6B.
- But competitors also suffered: Celebrex prescriptions plummeted 56% in 4 months despite being the "safe" alternative, because the safety concern implicated the entire COX-2 class.
- The class went from $5B+ annually to a single remaining drug.

**Calibration insight:** When the safety concern is molecule-specific (Avandia), competitors capture 30+pp. When it implicates the mechanism of action (COX-2), it destroys the entire category (contagion dominates competition).

**Clinical trial failures as R&D redirectors:** Pfizer's torcetrapib Phase III failure (2006) wiped $21B off market cap overnight and effectively killed the entire CETP inhibitor hypothesis. Three subsequent CETP inhibitors from other firms also failed. A single failure can redirect billions in sector-wide R&D.

### Sector 4: Consumer Tech (Samsung Galaxy Note 7)

The counterpoint case -- a major incident with rapid recovery.

- **Overall share drop:** 4-5pp (22.3% to 17.8%), recovered in ~2 quarters
- **Premium segment:** ~18pp (35% to 17%), recovered with Galaxy S8 (Apr 2017)
- **Financial impact:** $5.3B profit impact, $26B peak market cap loss, but stock hit *all-time high* by Apr 2017 (semiconductor division offsetting mobile losses)
- **Brand surveys:** 75% of Samsung users were neutral or positive about Samsung's handling of the recall

**Why the swing was "only" 4-5pp:** (1) Samsung sells across all price tiers -- Note 7 was one SKU; (2) Android ecosystem lock-in creates high switching costs; (3) rapid transparent response + strong successor product.

**Calibration insight:** Diversified, multi-product firms with strong brand equity and high switching costs are buffered. The simulation's model providers are closer to single-product firms, making larger swings more plausible.

### Sector 5: AI-Specific Incidents

**The dominant pattern: usage growth overwhelms incident-driven churn.** ChatGPT grew from 100M to 900M WAU (late 2023 to early 2026) straight through every controversy. Trust surveys show concern rising (37% to 50% of Americans "more concerned than excited," Pew 2021-2025), but this concern does not translate into reduced usage.

| AI Incident | Market Impact |
|------------|---------------|
| AI-assisted suicides (Character.AI, ChatGPT, 2023-2025) | 5 documented deaths. Character.AI: 28M to ~20M MAU (confounded by competition/guardrails). ChatGPT: zero detectable decline. 19+ states legislating. |
| QuitGPT / Pentagon boycott (Feb-Mar 2026) | 1.5M+ cancellations, 295% spike in ChatGPT uninstalls. Claude hit #1 app store. But 1.5M/900M WAU = 0.17%. |
| Google Gemini image controversy (Feb 2024) | $97B temp market cap loss. Gemini grew to ~750M MAU anyway. |
| ChatGPT 34-hour outage (Jun 2025) | 400M+ users affected. Zero detectable impact on growth curve. Enterprises added backup vendors rather than switching. |
| ChatGPT hallucinations (2023-) | Lawyers sanctioned. ChatGPT grew from 100M to 900M+ WAU through it all. |
| AI-generated CSAM (2024-2025) | Reports to NCMEC: 6,835 (2024) to 440,419 (H1 2025). TAKE IT DOWN Act signed. No impact attributed to specific providers. |
| Samsung/corporate data leaks via ChatGPT (2023) | 75% of firms "considered bans." Enterprise AI adoption doubled (55% to 78%). Bans didn't stick. |
| OpenAI March 2023 data leak | 1.2% of Plus subscribers affected. No measurable adoption impact. |
| Clearview AI regulatory fines (2020-) | EUR 100M+ in fines. Restricted to gov't-only in US. Private market access lost. |

**Two partial exceptions to the ~0pp pattern:**

**Character.AI** experienced a genuine decline (28M MAU peak to ~20M trough) amid multiple teen suicide lawsuits (Sewell Setzer, 14; Juliana Peralta, 13). But critical confounds: co-founders left for Google (Aug 2024), cheaper competitors emerged, and the safety guardrails Character.AI added (content filters, break reminders, suicide hotline pop-ups) alienated power users. Revenue still grew 112% YoY through the crisis. This suggests niche/smaller providers are more vulnerable than market leaders.

**QuitGPT (Feb-Mar 2026)** is the first documented mass switching event in AI. Triggered when OpenAI signed a Pentagon classified-network deal hours after Anthropic's CEO publicly refused the same contract. 1.5M+ participants, ChatGPT uninstalls surged 295% in a single day, Claude claimed #1 app store position. But: (a) this was political/ethical, not safety; (b) 1.5M is 0.17% of ChatGPT's 900M WAU; (c) persistence of the shift is unknown.

**Outages don't cause switching.** The 34-hour ChatGPT outage (Jun 2025, the longest ever) affected 400M+ users. Growth trajectory was undetectable from the curve -- ChatGPT doubled WAU in the 5 months following. The AWS Oct 2025 outage (13-19 hours) cascaded to 400+ SaaS providers but produced no documented permanent user migration. Enterprise response: add redundancy (37% now use 5+ AI models), not switch primary provider.

**The trust-behavior gap is the central finding.** Public concern about AI is rising steadily (Pew, Edelman, KPMG all show growing worry), but usage grows even faster. Regulatory/legislative responses are real (19+ states legislating on AI chatbot safety, FTC investigating, CA SB 243 signed), but these manifest as compliance costs and product constraints, not user churn. Dietvorst, Simmons & Massey (2015) established "algorithm aversion" in lab settings, but it has not manifested as market share shifts in real AI markets.

**Why AI markets are (so far) resilient to incidents:** (1) Market growing so fast that even damaged players grow in absolute terms; (2) distribution advantages (Google Search/Android, OpenAI's first-mover network effects) overwhelm trust effects; (3) switching costs for API integrations are non-trivial; (4) no AI incident has involved physical fatalities + regulatory shutdown (the combination that produces permanent exits in other sectors); (5) the product is perceived as too useful to abandon even if trust is low.

### Sector 6: Cross-Sector Academic Synthesis

**Key theoretical frameworks relevant to calibration:**

**1. Contagion vs. Competition (Jarrell & Peltzman, 1985; Freedman et al., 2012)**
Two opposing effects operate simultaneously after a safety incident:
- *Contagion:* Industry-wide demand destruction (dominates when the failure raises questions about the entire product category)
- *Competition:* Customer switching to rivals (dominates when the failure is clearly firm-specific)

The Vioxx case illustrates contagion (COX-2 class destroyed). The Avandia case illustrates competition (Actos captured Avandia's share). For the simulation: incident effects should depend on whether the failure is perceived as provider-specific or evaluation-methodology-wide.

**2. Liability of Good Reputation (Rhee & Haunschild, 2006)**
Highly reputed firms suffer MORE from recalls because expectations are violated more severely. In the simulation, the market leader should be more vulnerable to incident shocks, not less.

**3. Quadruple Jeopardy (Van Heerde, Helsen & Dekimpe, 2007)**
A crisis simultaneously: (1) destroys baseline demand, (2) reduces own marketing effectiveness, (3) increases vulnerability to rival actions, (4) reduces ability to compete against rivals. Market share shifts should be multiplicative, not just additive.

**4. Collective Reputation (Bachmann et al., 2023)**
VW Dieselgate caused a 34.6% sales reduction for *non-VW German automakers* (BMW, Mercedes). Safety failures spill over to firms sharing a collective identity. Relevant if evaluation firms share a "type" identity.

**5. Trust IS the Product (Arthur Andersen precedent)**
Firms where trust is the core product (audit, evaluation, certification) are existentially vulnerable to integrity failures. Arthur Andersen's 100% market exit and ~20pp redistribution to Big Four is the most relevant analogue for AI evaluation providers.

**6. Reputational losses >> direct costs (Karpoff & Lott, 1993; Armour et al., 2017)**
Reputational losses are 5-9x the size of direct legal/regulatory penalties. Markets impose reputational discipline far exceeding formal sanctions.

**7. Incident frequency (base rates)**
Market-restructuring safety incidents occur at roughly 1-3 per decade per mature sector. In AI (a younger, less regulated sector with tight coupling and high complexity), the base rate is harder to estimate but structural conditions suggest it could be higher.

### Verdict: Is the Simulation's Path Dependence Empirically Justified?

**Answer: (a) -- Valid emergent finding, with calibration refinements needed.**

The simulation's 30+pp swings are supported by real-world evidence across multiple sectors:

| Condition | Empirical Support | Simulation Mapping |
|-----------|------------------|--------------------|
| 30+pp absolute swing | Boeing (39pp), Avandia (34pp), Cruise (50+pp) | Directly validated |
| Single incident destroying a competitor | Cruise ($30B to $0), Arthur Andersen (100% exit) | Directly validated |
| Different winners across runs based on incident luck | Boeing/Airbus order balance swings with incidents | Validated -- "whoever avoids the incident wins" |
| Limited recovery mechanics | Cruise (never recovered), Boeing (6+ years, still not recovered) | Validated -- recovery is slow and fragile |

**Calibration refinements suggested by the evidence:**

1. **Incident type should gate severity.** Physical harm + regulatory shutdown -> 30+pp possible. Pure reputational/trust incidents -> 0-5pp typical. The simulation should distinguish between these.

2. **Recovery should be partial and fragile.** Boeing recovered to ~41% in 3 years but was knocked back by a second incident. Recovery should be slow (years, not rounds) and vulnerable to compounding.

3. **Market structure matters.** Duopolies/oligopolies with switching costs show 10-15pp permanent shifts, not 30+pp permanent shifts. The 30+pp cases involve either market exit (Cruise, Arthur Andersen) or close substitutes in low-switching-cost markets (Avandia -> Actos). If the simulation's providers have moderate switching costs, permanent 30+pp shifts should require market exit, not just reputation damage.

4. **Diversification buffers the shock.** Samsung lost only 4-5pp because the Note 7 was one SKU. If simulation providers are effectively single-product firms (like Cruise), larger swings are justified. If they're diversified (like Samsung), cap the swing at 5-10pp.

5. **"Liability of good reputation"** -- the market leader should be MORE vulnerable to incident shocks, consistent with Rhee & Haunschild (2006).

6. **Contagion vs. competition** -- some incidents should damage the entire evaluation sector (like COX-2 class destruction), not just the affected firm.

### Confidence Assessment

| Claim | Evidence Strength |
|-------|------------------|
| 30+pp swings are possible from single incidents | **Strong** -- Boeing, Avandia, Cruise all documented |
| Incidents can cause permanent market exit | **Strong** -- Cruise, Arthur Andersen, Takata, Uber ATG |
| Recovery takes years, not months | **Strong** -- Boeing (6+ years), Merck (3 years to stock recovery, needed new portfolio) |
| Second incidents compound the first | **Moderate** -- Boeing door plug is the main case |
| AI-specific incidents cause market share shifts | **Weak** -- no documented case to date |
| Market leader is most vulnerable | **Moderate** -- Rhee & Haunschild (2006) lab + auto data; Boeing was market leader |
| 30+pp swings are typical | **Weak** -- they are tail events requiring specific conditions |
