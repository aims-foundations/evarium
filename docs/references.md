# References

Empirical sources used to ground simulation parameters. Organized by simulation component.

---

## Design-Grounding Citations

Sources directly cited to justify specific parameter values or design choices in the simulation code.

| Parameter / Design Choice | Value | Primary Source(s) |
|---------------------------|-------|-------------------|
| `market_growth_rate` | 0.03/month (~43% annual) | S&P Global 451 Research (40% CAGR); Bloomberg Intelligence (42% CAGR) |
| Consumer population weights | archetype shares | Bick, Blandin & Deming (2024) NBER; Stanford HAI (2025) |
| `leaderboard_trust` archetype differentiation | varies by archetype | Hardy et al. (2024); Woodruff et al. (2018); Cai et al. (2019) |
| Exploration churn = media-driven, not satisfaction-direct | structural | Hardy et al. (2024); Brennen et al. (2018); Vergeer (2020) |
| Satisfaction = experience-based, not benchmark-based | structural | Beede et al. (2020); Lebovitz et al. (2022); Amershi et al. (2019) |
| Benchmark scores as lossy signals | structural | Elish & boyd (2018); Denton et al. (2021); Bandy & Vincent (2021) |
| Benchmark lock-in / path dependence | structural | Denton et al. (2021); Hutchinson et al. (2021) |
| Media = event-driven amplifier | structural | Fast & Horvitz (2017); Chuan et al. (2019); Vergeer (2020) |
| Regulator: information-constrained, implementation gap | structural | Lawrence et al. (2023); Veale et al. (2018); Wei et al. (2024) |
| US vs. EU regulatory presets | structural | Radu (2021); Ulnicane et al. (2021); Bareis & Katzenbach (2022) |
| VC funder: growth > profitability | structural | Kenney & Zysman (2019); Gompers et al. (2020); Lerner & Nanda (2020) |
| Gov vs. corporate funder logic | structural | Mazzucato (2018); Rikap & Lundvall (2022) |
| Evaluator ecosystem: independence, access, fragmentation | structural + future (eval-as-org) | Costanza-Chock et al. (2022); Raji et al. (2022); Buolamwini & Gebru (2018) |
| Compliance burden (regulator) | 1-3% revenue | IAPP/EY (2017) GDPR cost study |
| Developer AI adoption rate | 62% | Stack Overflow (2024) Developer Survey |
| Incident base rates | probabilistic | AI Incident Database (AIID) |

---

## Market Expansion Rate

- **S&P Global Market Intelligence / 451 Research (2025).** "Generative AI Market Revenue Projected to Grow at a 40% CAGR from 2024-2029." GenAI software market: $16B (2024) to $85B (2029). Grounds the 0.03/month market_growth_rate parameter (40% annual ≈ 2.8%/month).
- **Bloomberg Intelligence (2023).** "Generative AI to Become a $1.3 Trillion Market by 2032." GenAI market from $40B (2022) at 42% CAGR over the decade. Grounds the upper bound of the calibration range (42% annual ≈ 3.0%/month). Broad definition including infrastructure, services, and ads.

---

## Consumer Need Weights and Population Shares

### Adoption rates / population weights

- **Bick, A., Blandin, A., & Deming, D. J. (2024).** "The Rapid Adoption of Generative AI." *NBER Working Paper 32966.* Nationally representative occupation-level adoption data: computer/math 49.6%, management 49.0%, blue-collar 22.1%, overall 23% weekly use. Most methodologically sound population-representative source.
- **Stanford HAI (2025).** *AI Index Report 2025.* 78% organizational adoption; function-level breakdown (IT, marketing/sales lead).
- **McKinsey & Company (2025).** "The State of AI in 2025." 78% org adoption, 71% GenAI in at least one function. Marketing/sales and IT consistently lead adoption.
- **Pew Research Center (2025).** "Workers' Exposure to AI." 21% of US workers use AI on the job; variation by occupation and education.

### Software developers

- **Stack Overflow (2024).** *Developer Survey 2024, AI Section.* 62% developer AI tool adoption; 82% use primarily for code writing; 81% cite productivity as top benefit.
- **Stack Overflow (2025).** *Developer Survey 2025, AI Section.* Trust in AI accuracy dropped to 29%; 45% say AI is bad at complex tasks; #1 frustration is "solutions that are almost right."
- **GitHub (2024).** *Copilot statistics.* 15M+ users, 50% daily developer use, 90% of Fortune 100.
- **Menlo Ventures (2025).** "State of GenAI in the Enterprise." $37B enterprise GenAI spend; coding $4B (55% of department spend).
- **GitClear (2025).** AI-assisted code quality: 4x growth in code clones from AI-assisted coding.
- **METR/ArXiv (2025).** Longitudinal developer study: experienced developers 19% slower on complex tasks with AI; juniors see 26-39% gains.

### Legal professionals

- **ABA (2024).** *TechReport 2024, AI Section.* 74.7% of lawyers cite accuracy/hallucinations as #1 concern.
- **ABA (2024).** *Formal Opinion 512.* Maps AI usage to Rules 1.1 (competence) and 3.3 (candor); requires output verification.
- **Thomson Reuters (2025).** *Legal AI Survey.* 26% of legal orgs actively using GenAI (up from 14%); larger firms (51+) at 39%.
- **LawNext (2025).** AI hallucination database: 700+ court cases involving AI-generated fabricated citations; sanctions $3K-$31K per incident.
- **InPractice (2025).** Legal AI tools usage: legal research +9% YoY, case law summarization +34% YoY, contract analysis +17% YoY.

### Healthcare

- **AMA (2024).** "Physician AI Sentiment Survey." 66% of physicians use health AI (up 78% from 2023).
- **FDA (2025).** Draft guidance on AI-Enabled Device Software Functions. Centers on safety, accuracy, bias mitigation, lifecycle monitoring.
- **ECRI (2024).** "Top 10 Patient Safety Concerns." Ranks insufficient AI governance as #2.
- **Frontiers in Medicine (2024).** Systematic review: general-purpose LLMs hallucinate 17-45% in clinical contexts.
- **NEJM AI (2024).** LLMs achieve <50% exact-match accuracy on medical code mapping.
- **Menlo Ventures (2025).** Healthcare AI: $1.5B vertical AI spend (43% of all vertical AI); ambient scribes = $600M market.

### Finance / banking

- **Federal Reserve (2011).** *SR 11-7: Guidance on Model Risk Management.* Requires documentation, validation, governance, monitoring for all models influencing financial decisions. Explainability is primary regulatory concern.
- **EU AI Act (2024).** Classifies credit assessments and insurance pricing as high-risk; requires transparency, human oversight, bias mitigation.
- **EBA (2024).** AI Act implications for EU banking sector report.
- **IOSCO (2025).** Report on AI in securities markets.
- **FSOC (2024).** Annual report elevating AI as systemic financial risk: opaque decision-making, embedded bias, operational dependencies.
- **RGP (2025).** "AI in Financial Services 2025." 85% of financial firms use AI; primarily fraud detection and risk modeling.

### Customer service / content creation

- **Gartner (2025).** Prediction: agentic AI will autonomously resolve 80% of common customer service issues by 2029.
- **CoSchedule (2025).** 97% of content marketers plan AI use in 2026; 3x faster content production; 45% organic traffic increases.
- **Wondercraft (2025).** AI content creation report.
- **Peak Support (2024).** Customer service AI KPIs: target 85%+ accuracy, <15% escalation rate.
- **EdgeTier (2025).** Chatbot risk landscape: hallucination rates 25%+ in complex multi-step scenarios.
- **ScienceDirect (2024).** Empathic chatbots study: boost satisfaction in short interactions, undermine under time pressure.

### Education

- **Gallup (2024-25).** "Teachers & AI." 60% used AI tool; 32% weekly; saving ~6 weeks/year equivalent.

### Creative professionals

- **Adobe (2025).** "Creators Toolkit Survey." 86% of creators use creative GenAI; 83% integrated into workflows.

### Government

- **NIST (2023).** *AI Risk Management Framework 1.0 (AI RMF).* Four core functions: Govern, Map, Measure, Manage.
- **NIST (2024).** *AI 600-1: GenAI Profile.* Extension of AI RMF for generative AI risks.
- **OMB (2025).** *M-25-21, M-25-22.* Minimum risk management practices for high-impact AI in federal procurement; vendors must provide NIST RMF-aligned documentation.
- **GSA (2026).** Proposed AI procurement clause: contractors must disclose all AI systems; 72-hour security incident reporting to CISA.
- **GAO (2025).** *GAO-25-107933.* Identified 94 AI-related government-wide requirements across federal laws and executive orders.
- **Gallup (2025).** "AI in Public Sector." 43% of public-sector employees use AI.

### Worklytics (cross-sector)

- **Worklytics (2025).** "Employee AI Adoption Benchmarks by Department and Industry." Department-level median adoption: Tech engineering 65-75%, Sales/Marketing 55-70%, Customer Success 60-75%.

---

## Benchmark Gaming / Goodhart's Law

- **Goodhart, C. A. E. (1975).** "Problems of Monetary Management: The UK Experience." *Papers in Monetary Economics, Reserve Bank of Australia.*
- **Raji, I. D., et al. (2021).** "AI and the Everything in the Whole Wide World Benchmark." *NeurIPS 2021.*
- **Kiela, D., et al. (2021).** "Dynabench: Rethinking Benchmarking in NLP." *NAACL 2021.*
- **Guo, et al.** Benchmark contamination studies.
- **"Are We Done with MMLU?" (2024).** Benchmark saturation analysis.

### Benchmark scores as lossy signals

Grounds the design choice that benchmark scores lose context as they propagate through the ecosystem (provider -> evaluator -> media -> consumer). Scores are information-lossy at each hop.

- **Elish, M. C. & boyd, d. (2018).** "Situating Methods in the Magic of Big Data and AI." *Communication Monographs, 85*(1), 57-80. DOI: 10.1080/03637751.2017.1375130. "Magic" narratives around AI obscure sociotechnical labor; benchmark results are stripped of context as they move from technical papers to press coverage to public understanding.
- **Bandy, J. & Vincent, N. (2021).** "Addressing 'Documentation Debt' in Machine Learning: A Retrospective Datasheet for BookCorpus." *NeurIPS 2021 Datasets and Benchmarks Track.* arXiv: 2105.05241. BookCorpus became a de facto standard through citation cascading and convenience, not deliberate fitness evaluation. Illustrates path dependence in benchmark adoption.
- **Denton, E., Hanna, A., Amironesei, R., Smart, A. & Nicole, H. (2021).** "On the Genealogy of Machine Learning Datasets: A Critical History of ImageNet." *Big Data & Society, 8*(2). DOI: 10.1177/20539517211035955. Genealogical analysis of ImageNet tracing how a single benchmark shaped an entire field's research direction; category choices encode particular worldviews. Paradigmatic case of benchmark lock-in.

### Benchmark lock-in and path dependence

Grounds the simulation's modeling of how benchmarks become entrenched focal points that coordinate provider behavior regardless of quality, and why benchmark deprecation/replacement is slow.

- **Denton et al. (2021)** — see above.
- **Bandy & Vincent (2021)** — see above.
- **Hutchinson, B., Smart, A., Hanna, A., Denton, E., et al. (2021).** "Towards Accountability for Machine Learning Datasets: Practices from Software Engineering and Infrastructure." *FAccT 2021.* DOI: 10.1145/3442188.3445918. Interviews and participatory design with ML practitioners reveal systematic gaps in dataset governance: no version control norms, no deprecation procedures, no clear maintenance ownership. Benchmarks degrade if not maintained, and maintenance labor is invisible and under-resourced.

## Safety Underinvestment / Race Dynamics

- **Dafoe, A. (2018).** "AI Governance: A Research Agenda." *Future of Humanity Institute.*
- **Chan, A., et al. (2023).** "Harms from Increasingly Agentic AI Systems." *arXiv.*
- **Krakovna, V., et al.** Specification gaming examples.
- **NIST AI RMF (2023).** Empirical safety investment framing.

## Incident-Driven Market Dynamics

Empirical evidence and theoretical frameworks for how safety incidents reshape market structure. Grounds the simulation's incident severity parameters and path-dependence findings. See `docs/incident_path_dependence.md` for the full analysis.

### Reputational damage and competitive spillovers

- **Jarrell, G. & Peltzman, S. (1985).** "The Impact of Product Recalls on the Wealth of Sellers." *Journal of Political Economy, 93.* Foundational study: shareholders lose ~2.48% from recalls; negative spillover to competitors (contagion > competition). Establishes the dual contagion/competition framework.
- **Karpoff, J. M. & Lott, J. R. (1993).** "The Reputational Penalty Firms Bear from Committing Criminal Fraud." *Journal of Law and Economics, 36.* Reputational losses are several times larger than direct legal penalties. Markets impose discipline far exceeding formal sanctions.
- **Rhee, M. & Haunschild, P. R. (2006).** "The Liability of Good Reputation: A Study of Product Recalls in the U.S. Automobile Industry, 1966-1995." *Organization Science, 17*(1), 101-117. Highly reputed firms suffer MORE from recalls. Grounds the simulation's "market leader is most vulnerable" dynamic.
- **Van Heerde, H., Helsen, K. & Dekimpe, M. G. (2007).** "The Impact of a Product-Harm Crisis on Marketing Effectiveness." *Marketing Science, 26*(2), 230-245. "Quadruple jeopardy": crisis simultaneously destroys baseline demand, reduces own marketing effectiveness, increases vulnerability to rivals, and decreases competitive impact.
- **Armour, J., Mayer, C. & Polo, A. (2017).** "Regulatory Sanctions and Reputational Damage in Financial Markets." *Journal of Financial and Quantitative Analysis, 52*(4), 1429-1448. Reputational losses are ~9x the size of regulatory fines (UK financial firms, 2001-2011).
- **Bachmann, R., Ehrlich, G., Fan, Y., Ruzic, D. & Leard, B. (2023).** "Firms and Collective Reputation: A Study of the Volkswagen Emissions Scandal." *Journal of the European Economic Association, 21*(2), 484-525. NBER WP 26117. Non-VW German automakers suffered 34.6% annual US sales reduction from VW's scandal. Strongest evidence for collective-reputation spillovers.
- **Freedman, S., Kearney, M. & Lederman, M. (2012).** "Product Recalls, Imperfect Information, and Spillover Effects: Lessons from the Consumer Response to the 2007 Toy Recalls." *Review of Economics and Statistics, 94*(2), 499-516. 25% decline in Christmas sales for non-recalled toy categories. Shows safety incidents can destroy category demand, not just redistribute share.

### Product recall competitive dynamics

- **Coombs, W. T. (2007).** "Protecting Organization Reputations During a Crisis: The Development and Application of Situational Crisis Communication Theory." *Corporate Reputation Review, 10*(3), 163-177. Crisis type (victim/accidental/intentional) determines reputational threat level. "Preventable" crises generate the highest damage.
- **Cleeren, K., van Heerde, H. J. & Dekimpe, M. G. (2013).** "Rising from the Ashes: How Brands and Categories Can Overcome Product-Harm Crises." *Journal of Marketing, 77*(2), 58-77. Analysis of 60 FMCG product crises. Post-crisis recovery depends on negative publicity volume and blame attribution.
- **Chen, Y., Ganesan, S. & Liu, Y. (2009).** "Does a Firm's Product-Recall Strategy Affect Its Financial Value? An Examination of Strategic Alternatives During Product-Harm Crises." *Journal of Marketing, 73*(6), 214-226. Proactive recalls have more negative short-term stock impact (market interprets as signal of larger exposure).
- **Dawar, N. & Pillutla, M. M. (2000).** "Impact of Product-Harm Crises on Brand Equity: The Moderating Role of Consumer Expectations." *Journal of Marketing Research, 37*(2), 215-226. Prior brand equity moderates crisis impact; strong-equity firms survive ambiguous crises.
- **Astvansh, V., Antia, K. D. & Tellis, G. J. (2025).** "Product Recall: A Synthesis of Multidisciplinary Findings." *Marketing Letters, 36,* 65-77. Most comprehensive recent cross-sector review of recall causes, consequences, and strategies.
- **Fang, X., Astvansh, V., et al. (2025).** "How Do Brands Change Their Advertising in Response to a Rival's Product Recall?" *Production and Operations Management.* Competitors increase price advertising by 25% and decrease quality advertising by 71% after rival recalls.

### Sector-specific incident evidence

- **Koopman, P. (2024).** "Anatomy of a Robotaxi Crash: Lessons from the Cruise Pedestrian Dragging Mishap." *SAFECOMP 2024 / IEEE Reliability Magazine.* arXiv: 2402.06046. Technical analysis of organizational failures at Cruise.
- **Collings, D., Corbet, S., Hou, Y., Hu, Y., Larkin, C. & Oxley, L. (2022).** "The Effects of Negative Reputational Contagion on International Airlines: The Case of the Boeing 737-MAX Disasters." *International Review of Financial Analysis, 80.* Pricing contagion from Boeing to airlines with MAX orders.
- **Cioroianu, I., Corbet, S. & Larkin, C. (2021).** "Guilt Through Association: Reputational Contagion and the Boeing 737-MAX Disasters." *Economics Letters, 198.* Negative social media response to Boeing influenced share prices of undiversified airlines.
- **Cro, S., et al. (2024).** "Stock Market Reaction to the Recurring Incidents at Boeing: An Event Study Analysis." *International Journal of Finance & Economics.* Cumulative abnormal returns of -3.65% to -6.30% for Boeing; positive abnormal returns for Airbus and Embraer.
- **Chintagunta, P. K., Jiang, R. & Jin, G. Z. (2009).** "Information, Learning, and Drug Diffusion: The Case of Cox-2 Inhibitors." *Quantitative Marketing and Economics, 7*(4), 399-443. NBER WP 14252. Bayesian learning model of physician prescription switching after Vioxx withdrawal.
- **Shah, N. D., et al. (2016).** "How Did Multiple FDA Actions Affect the Utilization and Reimbursed Costs of Thiazolidinediones in US Medicaid?" *Clinical Therapeutics.* Quantified TZD prescription shifts after Avandia safety actions: 34pp class share drop in 12 months.
- **Downing, N. S., et al. (2023).** "Major Shifts in Acid Suppression Drug Utilization After the 2019 Ranitidine Recalls." *Digestive Diseases and Sciences.* Interrupted time series: ranitidine -53%/-99% (US/Canada); famotidine +37%/+128%.
- **Basse Mama, H., et al. (2022).** "Reputation Effects in the Market for Corporate Social Responsibility: Evidence from the BP Oil Spill." *PLOS ONE.* BP reputation declined ~50% vs. synthetic control; persisted through 2017. No significant spillover to competitor oil/gas firms.
- **Hammond, R. G. (2013).** "Sudden Unintended Used-Price Deceleration? The 2009-2010 Toyota Recalls." *Journal of Economics & Management Strategy.* Toyota used-car price impact <2%; contrast with Audi 1986 (16% slide). Brand establishment moderates shock severity.

### Algorithm aversion and AI trust

- **Dietvorst, B. J., Simmons, J. P. & Massey, C. (2015).** "Algorithm Aversion: People Erroneously Avoid Algorithms After Seeing Them Err." *Journal of Experimental Psychology: General, 144,* 114-126. People avoid algorithmic forecasters after seeing them err, even when the algorithm outperforms humans. Follow-up (Management Science, 2018): slight ability to modify the algorithm overcomes aversion.
- **Stanford HAI (2025).** *AI Index Report 2025.* 233 AI incidents reported in 2024, up 56.4% from 2023. Trust in AI companies to protect data: 50% (2023) to 47% (2024).
- **KPMG/University of Queensland (2023).** "Trust in Artificial Intelligence: A Global Study." N=17,000 across 17 countries. 61% wary of trusting AI; 75% would trust more with assurance mechanisms.
- **KPMG (2025).** "Trust, Attitudes, and Use of Artificial Intelligence." N=48,000 across 47 countries. 46% willing to trust AI; 81% of US consumers want laws/policies in place before trusting.
- **Pew Research Center (2025-2026).** "Americans and Artificial Intelligence" series. Concern rising: 37% (2021) to 50% (2025) "more concerned than excited" about AI in daily life. Usage rising simultaneously -- trust-behavior gap.
- **Nature Human Behaviour (2025).** "AI Characters Are Dangerous Without Guardrails." Analysis of character chatbot risks; supports legislative responses (CA SB 243, NY S 3008).

### Path dependence and market structure

- **Arthur, W. B. (1994).** *Increasing Returns and Path Dependence in the Economy.* University of Michigan Press. Foundational work: increasing returns to adoption create lock-in; single events can permanently shift equilibrium.
- **Perrow, C. (1984).** *Normal Accidents: Living with High-Risk Technologies.* Princeton University Press. Accidents in tightly coupled, complex systems are structurally inevitable.
- **Haunschild, P. R. & Sullivan, B. N. (2002).** "Learning from Complexity: Effects of Prior Accidents and Incidents on Airlines' Learning." *Administrative Science Quarterly, 47,* 609-643. Firms learn more from heterogeneous accident causes; specialist firms learn from complex information.

## Incident Rates and Severity

- **AI Incident Database (AIID).** Base rates for AI safety incidents.
- **Weidinger, L., et al. (2023).** "Sociotechnical Safety Evaluation of Generative AI Systems." *arXiv.*

## Dynamic Consumer Market / Enterprise Adoption

Sources grounding the dynamic consumer market composition change (enterprise share growth from ~25% to ~55% over 30 rounds) and longitudinal AI usage shifts.

### Enterprise adoption trajectory

- **McKinsey & Company (2024, 2025).** "The State of AI" (annual). GenAI adoption: 33% (2023) to 65% (2024) to 79% (2025). Only 7% report full-scale deployment (2025) — adoption wide, depth shallow.
- **Menlo Ventures (2024, 2025).** "State of Generative AI in the Enterprise." Enterprise GenAI spending: $1.7B (2023) to $11.5B (2024) to $37B (2025). Coding/developer tools: $7.3B (largest app category, 2025). Vertical AI (healthcare, legal, finance): $1.2B (2024) to $3.5B (2025). Build-to-buy shift: 47% build (2024) to 24% build (2025).
- **Stanford HAI (2024, 2025).** *AI Index Reports.* Business adoption 55% (2023) to 78% (2024). Corporate AI investment: $252.3B (2024), private investment up 44.5% YoY. GPT-3.5-level inference cost dropped 280x (Nov 2022 to Oct 2024).

### Enterprise vs consumer revenue differentiation

- **Axios (2026).** "AI Enterprise Revenue: Anthropic Turns Tables on OpenAI." Anthropic enterprise-heavy (~80% of revenue); ~$211/user/month.
- **Tanay Jaipuria (2025).** "OpenAI and Anthropic Revenue Breakdown." OpenAI enterprise ~25% of 2025 revenue; ChatGPT Enterprise seats: 150K (Jan 2024) to 2M+ (Feb 2025) to 9M+ (Feb 2026).
- **SaaStr (2025).** "OpenAI Crosses $12B ARR." OpenAI ARR trajectory: $2B (2023) to $6B (2024) to $20B (2025).

### Longitudinal usage pattern shifts (existing users changing behavior)

- **Anthropic (2024-2026).** "Anthropic Economic Index" series. Computer/math tasks: ~37-40% of conversations (stable). Educational instruction: rose 40%+ (9% to 13%). Directive conversations: 27% to 39% (Dec 2024 to mid-2025). Automation surpassed augmentation (49.1% vs 47%); API is 75% automated. New code creation doubled over 8 months; debugging declined.
- **OpenAI / Deming (2025).** "How People Use ChatGPT." NBER Working Paper, 1.5M conversations. Information seeking surged 14% to 24% YoY. Feminine-name users 37% (Jan 2024) to 52% (Jul 2025) — evidence of new user segments joining. 4x growth in low/middle-income countries.
- **Stack Overflow (2023-2025).** Developer Surveys. AI tool usage: 70% (2023) to 76% (2024) to 84% (2025). Trust in AI output declined: ~40% (2024) to 29% (2025). Usage-trust divergence — adoption rises while trust falls.

### Agentic AI demand (capability-driven demand creation)

- **MarketsandMarkets (2024).** Agentic AI market: $5.25B (2024), CAGR 43.8%.
- **Gartner (2024).** Enterprise software with agentic AI: <1% (2024), projected 33% by 2028.
- **Databricks (2025).** "State of AI: Enterprise Adoption Growth Trends." 43% of companies directing >50% of AI budget to agentic systems.

### GitHub Copilot / coding assistant adoption

- **GitHub (2024, 2025).** Octoverse reports. Users: ~1M (early 2024) to 15M (early 2025) to 20M (Jul 2025). Paid subscribers: 1.3M to 4.7M (Jan 2026). 80% of new GitHub developers use Copilot within first week. Code acceptance rate: 27-30%; Copilot generates 46% of all code.

---

## Market Share and Consumer Switching

- **Hardy, A., Reuel, A., Jafari Meimandi, K., Soder, L., Griffith, A., Asmar, D. M., Koyejo, S., Bernstein, M. S., & Kochenderfer, M. J. (2024).** "More than Marketing? On the Information Value of AI Benchmarks for Practitioners." *arXiv:2412.05520.* Interview study (N=19) finding benchmarks function as negative filters (poor scores disqualify) rather than positive adoption drivers; product/policy practitioners develop internal evals and rely on direct experience over public leaderboards; high-trust-in-benchmarks is concentrated in research contexts. Grounds the `leaderboard_trust` archetype differentiation and the asymmetry between score-driven attention vs. experience-driven switching.
- **Stanford HAI.** *AI Index Annual Reports.* Segment-level AI adoption and sensitivity parameters.
- Standard discrete-choice / logit switching models.

### Consumer satisfaction is experience-driven, not benchmark-driven

Grounds the design choice that satisfaction = `dot(cap, needs) - incident_penalty + cost_bonus` (purely experience-based), not a function of published benchmark scores.

- **Beede, E., Baylor, E., Hersch, F., et al. (2020).** "A Human-Centered Evaluation of a Deep Learning System Deployed in Clinics for the Detection of Diabetic Retinopathy." *CHI 2020.* DOI: 10.1145/3313831.3376718. Ethnographic field study of AI diagnostic tool in Thai clinics. Real-world performance diverged sharply from benchmarks due to environmental factors and workflow integration. Practitioners developed their own heuristics for when to trust the AI.
- **Lebovitz, S., Lifshitz-Assaf, H. & Levina, N. (2022).** "To Engage or Not to Engage with AI for Critical Judgments: How Professionals Deal with Opacity When Using AI for Medical Diagnosis." *Organization Science, 33*(1), 126-148. DOI: 10.1287/orsc.2021.1549. Three engagement patterns (full/selective/disengaged) driven not by benchmark accuracy but by practitioners' ability to build mental models of when the AI fails. Prior experience with errors was the strongest predictor of appropriate calibration.
- **Amershi, S., Begel, A., Bird, C., et al. (2019).** "Software Engineering for Machine Learning: A Case Study." *ICSE-SEIP 2019*, 291-300. DOI: 10.1109/ICSE-SEIP.2019.00042. Interview study (N=47) at Microsoft. Teams found benchmarks insufficient for real-world evaluation; frequently chose models with lower benchmark scores but more predictable behavior. Supports modeling consumer utility as a function of variance, not just mean quality.
- **Jussupow, E., Spohrer, K., Heinzl, A. & Gawlitza, J. (2021).** "Augmenting Medical Diagnosis Decisions? An Investigation into Physicians' Decision-Making Process with Artificial Intelligence." *Information Systems Research, 32*(3), 713-735. DOI: 10.1287/isre.2020.0980. Physicians' reliance on AI was mediated by assessment of AI's "competence boundaries" — trusted AI more for patterns they believed it was trained on. Prior experience with AI errors was the strongest predictor of appropriate calibration, more than reported accuracy.

### Leaderboard trust varies by archetype / heterogeneous adoption

Grounds the `leaderboard_trust` parameter variation across consumer archetypes and the modeling of heterogeneous engagement strategies.

- **Hardy et al. (2024)** — see above.
- **Woodruff, A., Fox, S. E., Rousso-Schindler, S. & Warshaw, J. (2018).** "A Qualitative Exploration of Perceptions of Algorithmic Fairness." *CHI 2018.* DOI: 10.1145/3173574.3174230. Interview study (N=44). Trust was heavily mediated by institutional context — the same algorithm was judged differently depending on who deployed it and for what purpose. Supports modeling consumer need weights varying by segment and provider identity mattering independently of product quality.
- **Cai, C. J., Reif, E., Hegde, N., et al. (2019).** "Human-Centered Tools for Coping with Imperfect Algorithms During Medical Decision-Making." *CHI 2019.* DOI: 10.1145/3290605.3300234. Pathologists prioritized interpretability and failure-mode transparency over raw accuracy when choosing whether to adopt AI tools. Those given uncertainty estimates were more willing to adopt even with lower overall accuracy. Supports multi-dimensional consumer preferences beyond headline scores.
- **Lebovitz et al. (2022)** — see above.

## Media Coverage and AI Hype Dynamics

Grounds the design choice that media acts as an event-driven amplifier (responding to announcements, incidents, policy events) rather than independently assessing capability. Media coverage drives exploration churn, not direct quality perception.

- **Brennen, J. S., Howard, P. N. & Nielsen, R. K. (2018).** "An Industry-Led Debate: How UK Media Cover Artificial Intelligence." *Reuters Institute for the Study of Journalism, Factsheet.* Industry sources dominate AI coverage; journalists rely on corporate press releases and demos; coverage tends toward binary utopian/dystopian framing with little independent technical evaluation.
- **Chuan, C.-H., Tsai, W.-H. S. & Cho, S. Y. (2019).** "Framing Artificial Intelligence in American Newspapers." *AIES 2019*, 339-344. DOI: 10.1145/3306618.3314285. Framing analysis of NYT, WSJ, Washington Post. Economic framing dominated; coverage correlated strongly with industry product launches. Ethics framing grew over time but remained secondary.
- **Fast, E. & Horvitz, E. (2017).** "Long-Term Trends in the Public Perception of Artificial Intelligence." *AAAI 2017, 31*(1). DOI: 10.1609/aaai.v31i1.10635. 30 years of NYT AI coverage. Coverage became substantially more optimistic after 2009, tracking closely with industry investment cycles. Optimism-tracks-funding finding grounds the coupling of media sentiment to funder activity.
- **Vergeer, M. (2020).** "Artificial Intelligence in the Dutch Press: An Analysis of Topics and Trends." *Communication Studies, 71*(3), 373-392. DOI: 10.1080/10510974.2020.1733038. Media coverage peaks lagged actual technical developments by 6-18 months, triggered more by policy events and corporate announcements than by technical breakthroughs. Grounds the event-driven (not capability-tracking) media timing model.
- **Natale, S. & Ballatore, A. (2020).** "Imagining the Thinking Machine: Technological Myths and the Rise of Artificial Intelligence." *Convergence, 26*(1), 3-18. DOI: 10.1177/1354856517715164. Journalists recycle familiar narrative templates when covering new AI developments, leading to predictable hype-fear cycles. Supports modeling media with narrative frames activated by trigger events.

## Evaluator Ecosystem Structure

Grounds the current benchmark-need weight mismatch (evaluator design choices determine what's measured) and the future evaluator-as-organization modeling (business models, independence, access barriers). See also `docs/evaluator_business_model_case_study.md`.

- **Raji, I. D., et al. (2020).** "Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Auditing." *FAT* 2020.* DOI: 10.1145/3351095.3372873. Insider account of Google's SMACTR audit framework. Internal audits face friction with product teams; documents the lag between capability development and safety assessment. Internal vs. external evaluation serve different organizational functions.
- **Costanza-Chock, S., Raji, I. D. & Buolamwini, J. (2022).** "Who Audits the Auditors? Recommendations from a Field Scan of the Algorithmic Auditing Ecosystem." *FAccT 2022.* DOI: 10.1145/3531146.3533213. Field scan of 152 auditing organizations. Ecosystem is fragmented: no consensus on what constitutes an audit, significant access barriers, tension between commercial auditing (paid by auditee) and independent auditing. Directly maps the organizational ecology the simulation models — evaluator funding, independence, and capture dynamics.
- **Raji, I. D., Xu, P., Honigsberg, C. & Ho, D. (2022).** "Outsider Oversight: Designing a Third Party Audit Ecosystem for AI Governance." *AIES 2022.* DOI: 10.1145/3514094.3534181. Draws on interviews with auditors and comparative analysis with financial auditing, food safety, and environmental compliance. Key structural problems: lack of access, no mandate, no standards body, conflicting incentives between auditor independence and need for platform cooperation. Provides empirically-grounded archetypes for different evaluator ecosystem configurations.
- **Buolamwini, J. & Gebru, T. (2018).** "Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification." *FAT* 2018, PMLR 81:77-91.* Constructed a new benchmark because existing ones were inadequate, then audited commercial systems. Benchmark composition (what data to include, how to stratify) directly determines what performance problems are visible or invisible. Demonstrates how evaluator design choices create or hide information asymmetries — the mechanism underlying the benchmark-need weight mismatch.
- UK DSIT evaluator landscape reports.

## Regulatory Interventions

- **EU AI Act (2024).** Precautionary threshold parameters; high-risk classification; conformity assessment.
- **NIST AI RMF (2023).** US light-touch framing.
- **IAPP/EY (2017).** GDPR compliance cost study: 1-3% revenue. Basis for compliance burden parameter.
- **EO 14110 (2023).** US executive order on AI safety.
- **SB 1047 (2024).** California AI safety bill (proposed).

### Regulator is information-constrained / implementation gap

Grounds the design choices that regulators observe only public state (scores, incidents, media), that lever cooldowns create implementation lag, and that the default equilibrium is inaction requiring significant evidence to escalate.

- **Veale, M., Van Kleek, M. & Binns, R. (2018).** "Fairness and Accountability Design Needs for Algorithmic Support in High-Stakes Public Sector Decision-Making." *CHI 2018.* DOI: 10.1145/3173574.3174014; arXiv: 1802.01029. Interviews with 27 public-sector ML practitioners across 5 OECD countries. Regulators lack technical tools and domain expertise to evaluate algorithmic systems directly; organizational silos between data teams and frontline decision-makers. Grounds the regulator's reliance on observable proxies (benchmark scores, incident reports, media) rather than direct system assessment.
- **Lawrence, C., Cui, I. & Ho, D. E. (2023).** "The Bureaucratic Challenge to AI Governance: An Empirical Assessment of Implementation at U.S. Federal Agencies." *AIES 2023 (Best Paper).* DOI: 10.1145/3600211.3604701. Fewer than 40% of 45 legal AI governance requirements could be verified as implemented; 88% of agencies failed to submit required AI plans. Root causes: lack of expertise, absent leadership, insufficient personnel, ambiguous language. Directly calibrates the gap between regulatory intent and real-world impact — justifies the cooldown mechanic and why regulation is slow to bite.
- **Wei, K., Ezell, C., Gabrieli, N. & Deshpande, C. (2024).** "How Do AI Companies 'Fine-Tune' Policy? Examining Regulatory Capture in AI Governance." *AIES 2024.* DOI: 10.1609/aies.v7i1.31745; arXiv: 2410.13042. Interviews with 17 AI policy experts identifying six channels of industry influence: agenda-setting, lobbying, academic capture, information management, cultural capture, media capture. 85% of DC AI lobbyists hired by industry. Industry's primary strategy is preventing regulation entirely, not just weakening it. Grounds the regulator's high inertia threshold and why the default is inaction.

### Regulatory framing shapes intervention style (US vs. EU presets)

Grounds the simulation's US (light-touch, industry-led) vs. EU (precautionary, rule-based) regulatory preset configurations and the mechanisms by which framing shifts regulatory ambition.

- **Radu, R. (2021).** "Steering the Governance of Artificial Intelligence: National Strategies in Perspective." *Policy and Society, 40*(2), 178-193. DOI: 10.1080/14494035.2021.1929728. Qualitative analysis of ~12 national AI strategies. Strong predominance of ethics-oriented framing over rule-based regulation; deliberate "functional indetermination" keeping governance vague. Industry actors embedded in strategy formulation from the outset.
- **Ulnicane, I., Knight, W., Leach, T., Stahl, B. C. & Wanjiku, W.-G. (2021).** "Framing Governance for a Contested Emerging Technology: Insights from AI Policy." *Policy and Society, 40*(2), 158-177. DOI: 10.1080/14494035.2020.1855800. Frame analysis of 49 AI policy documents. Widespread enthusiasm for ethics guidelines but cautious attitude toward binding regulation. Economic competitiveness framing weakens regulatory ambition — when "innovation race" narratives dominate, regulators are less likely to intervene aggressively.
- **Bareis, J. & Katzenbach, C. (2022).** "Talking AI into Being: The Narratives and Imaginaries of National AI Strategies and Their Performative Politics." *Science, Technology, & Human Values, 47*(5), 855-881. DOI: 10.1177/01622439211030007. National AI strategies overwhelmingly frame AI through economic competitiveness narratives, shaping which types of research get government funding and how regulation is scoped. Government priorities set by geopolitical narratives, not technical merit.
- **Kaminski, M. E. (2023).** "Regulating the Risks of AI." *Boston University Law Review, 103*, 1347-1420. SSRN: 4195066. Identifies four distinct models of AI risk regulation (environmental, financial, pharmaceutical, product safety precedents). Framing AI harms as "risks" privileges quantifiable harms and tends toward "fix the tech" rather than "don't use it."

## Funder Behavior

- **PitchBook / CB Insights.** AI investment reports; VC funding patterns.
- **Cihon, P., et al.** "Corporate Governance of AI." Non-commercial funder type modeling.

### Funder herd behavior and media influence on investment

Grounds the simulation's modeling of media sentiment feeding into funder scoring, VC herd dynamics, and growth-over-profitability investment logic.

- **Gompers, P. A., Gornall, W., Kaplan, S. N. & Strebulaev, I. A. (2020).** "How Do Venture Capitalists Make Decisions?" *Journal of Financial Economics, 135*(1), 169-190. DOI: 10.1016/j.jfineco.2019.06.011. Survey of 885 VCs. Team quality is the dominant factor (cited by 95%); VCs use relatively little quantitative analysis compared to pattern matching and "gut feel." Grounds the weight placed on team/founder signals over financial metrics in VC funder scoring.
- **Lerner, J. & Nanda, R. (2020).** "Venture Capital's Role in Financing Innovation: What We Know and How Much We Still Need to Learn." *Journal of Economic Perspectives, 34*(3), 237-261. DOI: 10.1257/jep.34.3.237. Reviews evidence on VC herd behavior and sector concentration. Capital floods into sectors based on a few visible successes ("hot market" phenomenon), driven by signals from peer investors and media coverage. Directly grounds coupling media sentiment to funder behavior.
- **Kenney, M. & Zysman, J. (2019).** "Unicorns, Cheshire Cats, and the New Dilemmas of Entrepreneurial Finance." *Venture Capital, 21*(1), 35-50. DOI: 10.1080/13691066.2018.1517430. "Blitz-scaling" norms where investors fund companies to achieve market dominance before profitability. Metrics like user growth and market share replaced traditional financial metrics. Grounds why VC funder type weights market share and growth trajectory over profitability.

### Government vs. corporate funder logic

Grounds the differentiation between VC, corporate, government, and foundation funder types in the simulation's funder scoring formulas.

- **Mazzucato, M. (2018).** "Mission-Oriented Innovation Policies: Challenges and Opportunities." *Industrial and Corporate Change, 27*(5), 803-815. DOI: 10.1093/icc/dty034. Public funders don't just fill market failures but actively shape and create markets through directed investment. DARPA's program manager model and EU Horizon's challenge-based framework represent fundamentally different evaluation logics from VC. Grounds why government funder scoring weights policy-mission alignment and spec compliance differently from private funders.
- **Rikap, C. & Lundvall, B.-A. (2022).** "Big Tech, Knowledge Predation and the Implications for Development." *Innovation and Development, 12*(3), 389-416. DOI: 10.1080/2157930X.2020.1855825. Large tech corporations strategically fund and acquire AI startups to control knowledge flows rather than purely for financial return ("knowledge predation"). Grounds corporate funder type's strategic-fit and defensive-investment motives beyond expected revenue.
- **Bareis & Katzenbach (2022)** — see Regulatory Interventions above. Also grounds government funder priorities as set by geopolitical competition narratives.
